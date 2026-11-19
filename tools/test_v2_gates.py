#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI SoC V2 无状态门禁三件套与 `run_workflow` 批次巡航单元测试套件。"""
from __future__ import annotations
import ast, asyncio, hashlib, json, subprocess, sys, tempfile, unittest
from pathlib import Path
from typing import List
from unittest import mock
import yaml

TOOLS_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = TOOLS_DIR.parent.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
from gates import codex_review, fast_gate, slice_gate
import sync_contracts

def _load_workflow_ns(ws_root: Path, call_tool_fn: object, calls: List[str]) -> dict:
    """加载 `run_slice_batch.py` 并在隔离全局命名空间注入测试桩。"""
    class FakeWorker:
        """模拟保活工程子 Agent 会话。"""
        async def __call__(self, prompt: str) -> dict:
            """记录提示词并返回模拟提交哈希。"""
            calls.append(prompt)
            return {"role": "ENG-AP", "repo": "printer-soc", "candidate_commit": "a" * 40, "summary": "ok"}
    async def fake_parallel(items: list, fn: object) -> list:
        """并发原语桩函数。"""
        return [await fn(x) for x in items]
    ns = {"WORKSPACES": (str(ws_root),), "phase": lambda _: None, "log": lambda _: None, "agent": lambda **_: FakeWorker(), "parallel": fake_parallel, "call_tool": call_tool_fn}
    wf_path = TOOLS_DIR / "workflow/run_slice_batch.py"
    coro = eval(compile(wf_path.read_text(encoding="utf-8"), str(wf_path), "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT), ns)
    ns["BG_POLL_SEC"] = 0.01
    if asyncio.iscoroutine(coro):
        asyncio.run(coro)
    return ns

def _write_min_slice(ws: Path, sid: str, cmd: str = "true") -> Path:
    """在临时目录生成含有效字段的最小切片 YAML 配置。"""
    p = ws / f"{sid}.yaml"
    p.write_text(yaml.safe_dump({"slice_id": sid, "batch_id": "B1", "integration_cmd": cmd, "subtasks": [{"role": "ENG-AP", "repo": "printer-soc", "branch": "main", "allowed_paths": ["*"]}]}), encoding="utf-8")
    return p

def _write_qa_bundle(qa_dir: Path, sid: str, passed: bool = True, commit: str = "a" * 40) -> list:
    """生成模拟 `qa_runner.py` 证据包并返回返回码为 0 或 1 的占位命令。"""
    qa_dir.mkdir(parents=True, exist_ok=True)
    vb = json.dumps({"task_id": sid, "verdict": "PASSED" if passed else "FAILED", "exit_code": 0 if passed else 1}).encode()
    lb = json.dumps({"repositories": [{"name": "printer-soc", "commit": commit}]}).encode()
    (qa_dir / "server_verdict.json").write_bytes(vb)
    (qa_dir / "server_lock.json").write_bytes(lb)
    proof = {"task_id": sid, "fresh_checkout": True, "passed": passed, "summary": "ok" if passed else "ctest fail", "sandbox": {"container_id": "cid1234567890"}, "server_verdict": {"path": "sv", "sha256": hashlib.sha256(vb).hexdigest()}, "server_lock": {"path": "sl", "sha256": hashlib.sha256(lb).hexdigest()}}
    (qa_dir / "server_qa.json").write_text(json.dumps(proof), encoding="utf-8")
    return ["python3", "-c", "import sys; sys.exit(0)"]

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
        """硬性门禁自检：生产 6 文件 <=900 行、含单测 <=1150 行且通过 AST 与防伪扫描。"""
        prod_files = [TOOLS_DIR / "sync_contracts.py", TOOLS_DIR / "gates/__init__.py", TOOLS_DIR / "gates/fast_gate.py", TOOLS_DIR / "gates/codex_review.py", TOOLS_DIR / "gates/slice_gate.py", TOOLS_DIR / "workflow/run_slice_batch.py"]
        prod_lines = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in prod_files)
        all_files = prod_files + [TOOLS_DIR / "test_v2_gates.py"]
        total_lines = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in all_files)
        self.assertLessEqual(prod_lines, 900, f"生产 6 文件 {prod_lines} 超出 900 行预算")
        self.assertLessEqual(total_lines, 1150, f"含单测总行数 {total_lines} 超出 1150 行预算")
        for fp in all_files:
            self.assertEqual(fast_gate.check_python_ast(fp), [], f"AST 自检未通过: {fp}")
            self.assertEqual(fast_gate.check_anti_fake_markers(fp, fp.name), [], f"防伪检查未通过: {fp}")

    def test_fast_gate_catches_scale_unverified_and_shim(self) -> None:
        """核验 Fast-Gate 拦截超 4 参数、缺中文注释、残留未验证标记、改包垫片及 C 指针自增。"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bad_py, shim_c = root / "bad_mod.py", root / "twin_bridge.c"
            bad_py.write_text("def f(a, b, c, d, e):\n    return '" + "[" + "UNVERIFIED]'\n", encoding="utf-8")
            shim_c.write_text("void h(int *p){ *p++; while(1); frame[5] = 0x14U; }\n", encoding="utf-8")
            py_errs = fast_gate.check_files_static([bad_py], root)
            self.assertTrue(any("入参 5 > 4" in e for e in py_errs) and any("未消解" in e for e in py_errs))
            self.assertGreaterEqual(len(fast_gate.check_files_static([shim_c], root)), 3)

    def test_subtask_boundary_blocks_bootloader_main_and_path_escape(self) -> None:
        """核验双 Bootloader 切入 main 分支或修改白名单外路径时立即被阻断。"""
        with tempfile.TemporaryDirectory() as tmp:
            ws, repo = Path(tmp), Path(tmp) / "boot/bootloadermc"
            repo.mkdir(parents=True)
            for args in (["init", str(repo)], ["-C", str(repo), "checkout", "-b", "main"]):
                subprocess.run(["git"] + args, check=True, capture_output=True)
            (repo / "init.txt").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-m", "init"], check=True, capture_output=True)
            (repo / "secret.c").write_text("int x = 1;\n", encoding="utf-8")
            errs = fast_gate.check_subtask_boundary(ws, {"repo": "boot/bootloadermc", "branch": "soc_debug", "allowed_paths": ["bootloader/**"], "diff_budget": {"max_files": 1}})
            self.assertTrue(any("严禁在 main 分支" in e for e in errs) and any("路径越界" in e for e in errs))

class V2CodexAndWorkflowCruiseTest(unittest.TestCase):
    """验证三态门禁、非空目录拒复用、后台等待及冲突拦截机制。"""
    def test_docker_wait_is_extended_only_for_system_profile(self) -> None:
        """正式制镜有独立外层时限，宿主与应用维持原有上限。"""
        for profile, expected in (("host-software", 600), ("c308l-app", 600), ("c308l-system", 7200)):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                mock_timeout = subprocess.TimeoutExpired(["runner"], expected)
                with mock.patch.object(slice_gate, "_qa_command", return_value=["runner"]), \
                        mock.patch.object(slice_gate.subprocess, "run", side_effect=mock_timeout) as runner:
                    _, verdict = slice_gate._run_docker_qa(root, {"slice_id": "SLICE-T", "profile": profile}, {}, root)
                self.assertEqual(runner.call_args.kwargs["timeout"], expected)
                self.assertEqual(verdict["status"], "BLOCKED")

    def test_graded_codex_verdict_and_missing_cli_blocked(self) -> None:
        """核验分级一致校验，并验证 Codex CLI 缺失抛出 `CodexGateBlockedError`。"""
        ok = {"slice_id": "SLICE-01", "decision": "APPROVED", "axis_spec_realism": "ok", "axis_embedded_safety": "ok", "findings": [{"id": "M1", "severity": "MINOR", "axis": "embedded_safety", "location": "a.c:1", "message": "改进注释"}]}
        self.assertEqual(codex_review.validate_graded_verdict(ok, "SLICE-01")[0], 0)
        with self.assertRaises(ValueError):
            codex_review.validate_graded_verdict(dict(ok, findings=[dict(ok["findings"][0], severity="BLOCKER")]), "SLICE-01")
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict("os.environ", {"CODEX_BIN": str(Path(tmp) / "missing_codex")}):
            with self.assertRaises(codex_review.CodexGateBlockedError):
                codex_review.run_codex_audit("hi", "SLICE-01", Path(tmp), Path(tmp) / "out")

    def test_slice_gate_tristate_nonempty_reuse_and_qa_conflict(self) -> None:
        """核验三态输出、非空证据目录拒复用及 Docker QA 退出码与证据冲突拦截。"""
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            sp, out_f = _write_min_slice(ws, "SLICE-T1"), ws / "out_fast_fail"
            with mock.patch.object(slice_gate.fast_gate, "run_fast_gate", return_value=(False, ["bad"])):
                r1 = slice_gate.execute_slice_funnel(ws, sp, out_f)
            self.assertEqual((r1["status"], r1["exit_code"], r1["stage"]), ("FAILED", 1, "fast_gate"))
            r_reuse = slice_gate.execute_slice_funnel(ws, sp, out_f)
            self.assertEqual((r_reuse["status"], r_reuse["exit_code"], r_reuse["stage"]), ("BLOCKED", 2, "gate_init"))
            with mock.patch.object(slice_gate.fast_gate, "run_fast_gate", return_value=(True, [])):
                r2 = slice_gate.execute_slice_funnel(ws, sp, ws / "out_fast_only", fast_only=True)
            self.assertEqual((r2["status"], r2["exit_code"]), ("FAST-PASSED", 0))
            with mock.patch.object(slice_gate.fast_gate, "run_fast_gate", return_value=(True, [])), mock.patch.object(slice_gate, "input_fingerprint", return_value="fp1"), mock.patch.object(slice_gate, "_collect_locked_commits", return_value={"printer-soc": "a" * 40}):
                with mock.patch.object(slice_gate, "_qa_command", return_value=["python3", "-c", "import sys; sys.exit(1)"]):
                    self.assertEqual(slice_gate.execute_slice_funnel(ws, sp, ws / "out_blk")["status"], "BLOCKED")
                out_c1 = ws / "out_c1"
                with mock.patch.object(slice_gate, "_qa_command", side_effect=lambda *_: (_write_qa_bundle(out_c1 / "docker_qa", "SLICE-T1", True), ["python3", "-c", "import sys; sys.exit(1)"])[1]):
                    self.assertEqual((slice_gate.execute_slice_funnel(ws, sp, out_c1)["status"], slice_gate.execute_slice_funnel(ws, sp, ws / "out_c0", fast_only=False)["stage"]), ("BLOCKED", "docker_qa"))
                out_c2 = ws / "out_c2"
                with mock.patch.object(slice_gate, "_qa_command", side_effect=lambda *_: _write_qa_bundle(out_c2 / "docker_qa", "SLICE-T1", False)):
                    self.assertEqual(slice_gate.execute_slice_funnel(ws, sp, out_c2)["status"], "BLOCKED")
                out_ok, cv = ws / "out_ok", codex_review.CodexVerdict("s1", "APPROVED", 0, [], 10, {"findings": []})
                with mock.patch.object(slice_gate, "_qa_command", side_effect=lambda *_: _write_qa_bundle(out_ok / "docker_qa", "SLICE-T1", True)), mock.patch.object(slice_gate.codex_review, "run_codex_audit", return_value=cv):
                    self.assertEqual((slice_gate.execute_slice_funnel(ws, sp, out_ok)["status"], (ws / "project-control/slices/ledger.md").is_file()), ("PASSED", True))

    def test_workflow_rework_and_missing_verdict_always_blocked(self) -> None:
        """核验合法 `FAILED` 触发 2 轮返修，而缺失 `verdict.json`（不论退出码/异常）一律 `BLOCKED` 零扣次。"""
        with tempfile.TemporaryDirectory() as tmp:
            ws, dirs, calls = Path(tmp), [], []
            _write_min_slice(ws, "SLICE-01")
            async def real_fail(name: str, **kw: object) -> str:
                """写入合法 FAILED 裁决并返回退出码 1。"""
                out_p = ws / kw["CommandLine"].split("--out-dir ")[1].split(";")[0]
                dirs.append(str(out_p))
                out_p.mkdir(parents=True, exist_ok=True)
                (out_p / "verdict.json").write_text(json.dumps({"slice_id": "SLICE-01", "status": "FAILED", "stage": "codex", "reason": "B1", "next_step": "fix"}), encoding="utf-8")
                return "Command exited with code 1."
            res = asyncio.run(_load_workflow_ns(ws, real_fail, calls)["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["SLICE-01.yaml"]}))
            self.assertEqual((res["status"], res["remediation_used"], len(calls), len(set(dirs))), ("FAILED", 2, 3, 3))
            for ret in ("Command exited with code 1.", "Command exited with code 0.", RuntimeError("crash")):
                c_miss = []
                async def miss_cmd(name: str, r=ret, **kw: object) -> str:
                    """不写 verdict.json 以模拟裁决缺失。"""
                    if isinstance(r, Exception):
                        raise r
                    return r
                rb = asyncio.run(_load_workflow_ns(ws, miss_cmd, c_miss)["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["SLICE-01.yaml"]}))
                self.assertEqual((rb["status"], rb["remediation_used"], len(c_miss)), ("BLOCKED", 0, 1))

    def test_workflow_bg_wait_conflict_and_restart_isolation(self) -> None:
        """核验后台门禁等待结束、重启续跑目录独立、双层冲突拦截及权限拒绝零扣次。"""
        with tempfile.TemporaryDirectory() as tmp:
            ws, dirs, polls = Path(tmp), [], [0]
            _write_min_slice(ws, "SLICE-01")
            async def bg_tool(name: str, **kw: object) -> str:
                """模拟 run_command 转后台并经 manage_task 等待后成功结束。"""
                if name == "run_command":
                    out_p = ws / kw["CommandLine"].split("--out-dir ")[1].split(";")[0]
                    dirs.append(str(out_p))
                    bg_tool.out_p = out_p
                    return "Tool is running as a background task with task id: conv/t-88"
                polls[0] += 1
                if polls[0] < 3:
                    return "Task: conv/t-88\nStatus: RUNNING"
                out_p = bg_tool.out_p
                _write_qa_bundle(out_p / "docker_qa", "SLICE-01", True)
                (out_p / "gate_exit.rc").write_text("0\n", encoding="utf-8")
                (out_p / "verdict.json").write_text(json.dumps({"slice_id": "SLICE-01", "status": "PASSED", "stage": "codex", "reason": "ok", "next_step": "next"}), encoding="utf-8")
                return "Task: conv/t-88\nStatus: DONE\nCommand exited with code 0."
            calls = []
            ns = _load_workflow_ns(ws, bg_tool, calls)
            r_ok = asyncio.run(ns["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["SLICE-01.yaml"]}))
            polls[0] = 0
            r_ok2 = asyncio.run(ns["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["SLICE-01.yaml"]}))
            self.assertEqual((r_ok["status"], r_ok["completed_slices"], r_ok2["status"], len(set(dirs))), ("PASSED", ["SLICE-01"], "PASSED", 2))
            for rc_txt, vst, qap in (("1", "PASSED", True), ("0", "FAILED", True), ("0", "PASSED", False)):
                c_cf = []
                async def cf_tool(name: str, rt=rc_txt, vs=vst, qp=qap, **kw: object) -> str:
                    """制造退出码与裁决或 Docker QA 证据冲突。"""
                    out_p = ws / kw["CommandLine"].split("--out-dir ")[1].split(";")[0]
                    _write_qa_bundle(out_p / "docker_qa", "SLICE-01", qp)
                    (out_p / "verdict.json").write_text(json.dumps({"slice_id": "SLICE-01", "status": vs, "stage": "codex"}), encoding="utf-8")
                    return f"Command exited with code {rt}."
                rcf = asyncio.run(_load_workflow_ns(ws, cf_tool, c_cf)["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["SLICE-01.yaml"]}))
                self.assertEqual((rcf["status"], rcf["remediation_used"], len(c_cf)), ("BLOCKED", 0, 1))
            class DeniedErr(RuntimeError):
                """模拟权限被拒异常。"""
                denied = True
            c_den = []
            async def den_cmd(name: str, **kw: object) -> str:
                """抛出权限被拒异常。"""
                raise DeniedErr("Tool denied")
            rden = asyncio.run(_load_workflow_ns(ws, den_cmd, c_den)["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["SLICE-01.yaml"]}))
            self.assertEqual((rden["status"], rden["remediation_used"], len(c_den)), ("BLOCKED", 0, 1))
            row = "| 2026-11-18 | B1 | SLICE-01 | SW-Verified | `p:123; inputs=aaaa1111` | `c` | `s` | `v` |"
            self.assertFalse(ns["is_slice_verified"](row, "SLICE-01", "bbbb2222"))
            self.assertTrue(ns["is_slice_verified"](row, "SLICE-01", "aaaa1111"))

if __name__ == "__main__":
    unittest.main()
