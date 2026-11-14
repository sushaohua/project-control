#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI SoC V2 无状态门禁三件套与 `run_workflow` 批次巡航单元测试套件。"""

from __future__ import annotations

import ast
import asyncio
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import List
import unittest

import yaml

TOOLS_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = TOOLS_DIR.parent.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from gates import codex_review, fast_gate, slice_gate
import sync_contracts


class V2ContractAndFastGateTest(unittest.TestCase):
    """验证单一契约源 `sync_contracts.py` 与秒级门禁 `fast_gate.py` 的正反例行为。"""

    def test_workspace_five_endpoints_and_header_render(self) -> None:
        """核验真实工作区五端头文件与黄金帧 CRC 全绿，且生成头文件可被重解析通过。"""
        ok, errs = sync_contracts.verify_workspace_contracts(WORKSPACE_ROOT)
        self.assertTrue(ok, f"真实五端契约校验失败: {errs}")
        contract = sync_contracts.load_contract(WORKSPACE_ROOT / "project-control/contracts/minimc_v2_contract.yaml")
        parsed = sync_contracts.parse_header_constants(sync_contracts.render_canonical_header(contract))
        self.assertEqual(sync_contracts.validate_endpoint("GEN", parsed, contract, True), [])

    def test_contract_negative_collisions_and_bad_crc(self) -> None:
        """核验 0x05 禁用码、命令码碰撞及 <520B 容量违例均被确定性拦截。"""
        contract = sync_contracts.load_contract(WORKSPACE_ROOT / "project-control/contracts/minimc_v2_contract.yaml")
        consts = sync_contracts.parse_header_constants(sync_contracts.render_canonical_header(contract))
        bad = dict(consts, MINIMC_CMD_ESTOP_ACK=0x05, MINIMC_CMD_OTA_START=0x1D, MINIMC_MAX_PAYLOAD_SIZE=256)
        self.assertGreaterEqual(len(sync_contracts.validate_endpoint("NEG", bad, contract, True)), 3)

    def test_v2_python_tools_pass_fast_gate_self_check(self) -> None:
        """硬性门禁自检：新增全部 V2 Python 模块满足总预算 <=900 行、单函数 <=50 行、<=4 参与中文注释。"""
        prod_files = [
            TOOLS_DIR / "sync_contracts.py", TOOLS_DIR / "gates/__init__.py",
            TOOLS_DIR / "gates/fast_gate.py", TOOLS_DIR / "gates/codex_review.py",
            TOOLS_DIR / "gates/slice_gate.py", TOOLS_DIR / "workflow/run_slice_batch.py",
        ]
        all_files = prod_files + [TOOLS_DIR / "test_v2_gates.py"]
        total_lines = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in all_files)
        self.assertLessEqual(total_lines, 900, f"新增 V2 工具含测试总行数 {total_lines} 超出 900 行预算")
        for fp in all_files:
            self.assertEqual(fast_gate.check_python_ast(fp), [], f"自检未通过: {fp}")

    def test_fast_gate_catches_scale_unverified_and_shim(self) -> None:
        """核验 Fast-Gate 拦截超 4 参数、缺中文注释、残留 [UNVERIFIED]、改包垫片及 C 指针自增。"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bad_py, shim_c = root / "bad_mod.py", root / "twin_bridge.c"
            bad_py.write_text("def f(a, b, c, d, e):\n    return '[UNVERIFIED]'\n", encoding="utf-8")
            shim_c.write_text("void h(int *p){ *p++; while(1); frame[5] = 0x14U; }\n", encoding="utf-8")
            py_errs = fast_gate.check_files_static([bad_py], root)
            self.assertTrue(any("入参 5 > 4" in e for e in py_errs) and any("[UNVERIFIED]" in e for e in py_errs))
            self.assertGreaterEqual(len(fast_gate.check_files_static([shim_c], root)), 3)

    def test_subtask_boundary_blocks_bootloader_main_and_path_escape(self) -> None:
        """核验双 Bootloader 切入 main 分支或修改白名单外路径时立即被阻断。"""
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            repo = ws / "boot/bootloadermc"
            repo.mkdir(parents=True)
            subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(repo), "checkout", "-b", "main"], check=True, capture_output=True)
            (repo / "init.txt").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-m", "init"], check=True, capture_output=True)
            (repo / "secret.c").write_text("int x = 1;\n", encoding="utf-8")
            errs = fast_gate.check_subtask_boundary(ws, {"repo": "boot/bootloadermc", "branch": "soc_debug", "allowed_paths": ["bootloader/**"], "diff_budget": {"max_files": 1}})
            self.assertTrue(any("严禁在 main 分支" in e for e in errs) and any("路径越界" in e for e in errs))


class V2CodexAndWorkflowCruiseTest(unittest.TestCase):
    """验证双轴三级 Codex 裁决校验、账本幂等续跑与 2 轮保活返修熔断。"""

    def test_graded_codex_verdict_consistency(self) -> None:
        """核验 0 BLOCKER + MINOR 允许 APPROVED，而含 BLOCKER 标 APPROVED 必抛异常。"""
        ok = {"slice_id": "SLICE-01", "decision": "APPROVED", "axis_spec_realism": "ok", "axis_embedded_safety": "ok", "findings": [{"id": "M1", "severity": "MINOR", "axis": "embedded_safety", "location": "a.c:1", "message": "改进注释"}]}
        b_cnt, minors = codex_review.validate_graded_verdict(ok, "SLICE-01")
        self.assertEqual((b_cnt, len(minors)), (0, 1))
        with self.assertRaises(ValueError):
            codex_review.validate_graded_verdict(dict(ok, findings=[dict(minors[0], severity="BLOCKER")]), "SLICE-01")

    def test_workflow_idempotent_skip_and_remediation_breaker(self) -> None:
        """加载真实 `run_slice_batch.py` 验证账本跳过已绿切片、追加账本与 >2 轮失败熔断。"""
        wf_path = TOOLS_DIR / "workflow/run_slice_batch.py"
        calls: List[str] = []

        class FakeWorker:
            """模拟保活工程子 Agent 会话。"""
            async def __call__(self, prompt: str) -> dict:
                """记录提示词并返回模拟提交哈希。"""
                calls.append(prompt)
                return {"role": "ENG-AP", "repo": "soc-ap", "candidate_commit": "a" * 40, "summary": "ok"}

        async def fake_parallel(items: list, fn: object) -> list:
            """并发原语桩函数。"""
            return [await fn(x) for x in items]

        async def fail_tool(name: str, **kwargs: object) -> str:
            """门禁命令失败桩。"""
            _ = (name, kwargs)
            raise RuntimeError("BLOCKER")

        ns = {"phase": lambda _: None, "log": lambda _: None, "agent": lambda **_: FakeWorker(), "parallel": fake_parallel, "call_tool": fail_tool}
        code = compile(wf_path.read_text(encoding="utf-8"), str(wf_path), "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
        coro = eval(code, ns)
        if asyncio.iscoroutine(coro):
            asyncio.run(coro)
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            ledger = ws / "project-control/slices/ledger.md"
            ledger.parent.mkdir(parents=True)
            ledger.write_text("## 2. 非阻断技术债登记表\n", encoding="utf-8")
            slice_gate.append_ledger_entry(ledger, {"batch_id": "B1", "slice_id": "SLICE-01", "status": "SW-Verified", "commits_short": "soc-ap:1234567", "container_id": "cid", "codex_session": "sid", "verdict_sha256": "f" * 64, "minors": []})
            for sid in ("SLICE-01", "SLICE-02"):
                (ws / f"{sid}.yaml").write_text(yaml.safe_dump({"slice_id": sid, "batch_id": "B1", "integration_cmd": "true", "subtasks": [{"role": "ENG-AP", "repo": "soc-ap", "branch": "main", "allowed_paths": ["*"]}]}), encoding="utf-8")
            with self.assertRaises(RuntimeError):
                asyncio.run(ns["run_batch_cruise"]({"workspace": str(ws), "plan_path": "docs/p.md", "slice_files": ["SLICE-01.yaml", "SLICE-02.yaml"]}))
            self.assertEqual(len(calls), 3)


if __name__ == "__main__":
    unittest.main()
