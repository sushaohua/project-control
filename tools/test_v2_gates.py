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
sys.path.insert(0, str(TOOLS_DIR)) if str(TOOLS_DIR) not in sys.path else None
from gates import codex_review, fast_gate, slice_gate
from workflow import git_handoff
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
    asyncio.run(coro) if asyncio.iscoroutine(coro) else None
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
    (qa_dir / "server_verdict.json").write_bytes(vb); (qa_dir / "server_lock.json").write_bytes(lb)
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
        self.assertEqual(sync_contracts.validate_endpoint("GEN", sync_contracts.parse_header_constants(sync_contracts.render_canonical_header(contract)), contract, True), [])
    def test_contract_negative_collisions_and_bad_crc(self) -> None:
        """核验 0x05 禁用码、命令码碰撞及 <520B 容量违例均被确定性拦截。"""
        contract = sync_contracts.load_contract(WORKSPACE_ROOT / "project-control/contracts/minimc_v2_contract.yaml")
        bad = dict(sync_contracts.parse_header_constants(sync_contracts.render_canonical_header(contract)), MINIMC_CMD_ESTOP_ACK=0x05, MINIMC_CMD_OTA_START=0x1D, MINIMC_MAX_PAYLOAD_SIZE=256)
        self.assertGreaterEqual(len(sync_contracts.validate_endpoint("NEG", bad, contract, True)), 3)
    def test_v2_python_tools_pass_fast_gate_self_check(self) -> None:
        """硬性门禁自检：生产 6 文件 <=900 行、含单测 <=1150 行且通过 AST 与防伪扫描。"""
        prod = [TOOLS_DIR / "sync_contracts.py", TOOLS_DIR / "gates/__init__.py", TOOLS_DIR / "gates/fast_gate.py", TOOLS_DIR / "gates/codex_review.py", TOOLS_DIR / "gates/slice_gate.py", TOOLS_DIR / "workflow/run_slice_batch.py"]
        prod_lines = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in prod)
        all_files = prod + [TOOLS_DIR / "test_v2_gates.py"]
        total_lines = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in all_files)
        self.assertLessEqual(prod_lines, 900, f"生产 6 文件 {prod_lines} 超出 900 行预算")
        self.assertLessEqual(total_lines, 1150, f"含单测总行数 {total_lines} 超出 1150 行预算")
        for fp in all_files + [TOOLS_DIR / "workflow/git_handoff.py"]:
            self.assertEqual((fast_gate.check_python_ast(fp), fast_gate.check_anti_fake_markers(fp, fp.name)), ([], []), f"自检失败: {fp}")
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
            ws, repo = Path(tmp), Path(tmp) / "boot/bootloadermc"; repo.mkdir(parents=True); (repo / "init.txt").write_text("base\n")
            for args in (["init", str(repo)], ["-C", str(repo), "checkout", "-b", "main"], ["add", "."], ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-m", "init"]): subprocess.run(["git", "-C", str(repo)] + args if args[0] != "init" else ["git"] + args, check=True, capture_output=True)
            (repo / "secret.c").write_text("int x = 1;\n")
            errs = fast_gate.check_subtask_boundary(ws, {"repo": "boot/bootloadermc", "branch": "soc_debug", "allowed_paths": ["bootloader/**"], "diff_budget": {"max_files": 1}})
            self.assertTrue(any("严禁在 main 分支" in e for e in errs) and any("路径越界" in e for e in errs))
class V2CodexAndWorkflowCruiseTest(unittest.TestCase):
    """验证三态门禁、检查点/交付点巡航、远端交接及冲突拦截机制。"""
    def test_docker_wait_is_extended_only_for_system_profile(self) -> None:
        """正式制镜有独立外层时限，宿主与应用维持原有上限。"""
        for profile, expected in (("host-software", 600), ("c308l-app", 600), ("c308l-system", 7200)):
            with tempfile.TemporaryDirectory() as tmp:
                root, mock_to = Path(tmp), subprocess.TimeoutExpired(["runner"], expected)
                with mock.patch.object(slice_gate, "_qa_command", return_value=["runner"]), mock.patch.object(slice_gate.subprocess, "run", side_effect=mock_to) as runner:
                    self.assertEqual((slice_gate._run_docker_qa(root, {"slice_id": "SLICE-T", "profile": profile}, {}, root)[1]["status"], runner.call_args.kwargs["timeout"]), ("BLOCKED", expected))
    def test_graded_codex_verdict_and_missing_cli_blocked(self) -> None:
        """核验分级一致校验，并验证 Codex CLI 缺失抛出 `CodexGateBlockedError`。"""
        ok = {"slice_id": "SLICE-01", "decision": "APPROVED", "axis_spec_realism": "ok", "axis_embedded_safety": "ok", "findings": [{"id": "M1", "severity": "MINOR", "axis": "embedded_safety", "location": "a.c:1", "message": "改进注释"}]}
        self.assertEqual(codex_review.validate_graded_verdict(ok, "SLICE-01")[0], 0)
        with self.assertRaises(ValueError): codex_review.validate_graded_verdict(dict(ok, findings=[dict(ok["findings"][0], severity="BLOCKER")]), "SLICE-01")
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict("os.environ", {"CODEX_BIN": str(Path(tmp) / "missing_codex")}), self.assertRaises(codex_review.CodexGateBlockedError):
            codex_review.run_codex_audit("hi", "SLICE-01", Path(tmp), Path(tmp) / "out")
    def test_slice_gate_tristate_nonempty_reuse_and_qa_conflict(self) -> None:
        """核验三态输出、非空证据目录拒复用及 Docker QA 退出码与证据冲突拦截。"""
        with tempfile.TemporaryDirectory() as tmp:
            ws, sp, out_f = Path(tmp), _write_min_slice(Path(tmp), "SLICE-T1"), Path(tmp) / "out_fast_fail"
            with mock.patch.object(slice_gate.fast_gate, "run_fast_gate", return_value=(False, ["bad"])):
                r1 = slice_gate.execute_slice_funnel(ws, sp, out_f)
            self.assertEqual((r1["status"], r1["exit_code"], r1["stage"], slice_gate.execute_slice_funnel(ws, sp, out_f)["stage"]), ("FAILED", 1, "fast_gate", "gate_init"))
            with mock.patch.object(slice_gate.fast_gate, "run_fast_gate", return_value=(True, [])):
                self.assertEqual(slice_gate.execute_slice_funnel(ws, sp, ws / "out_fast_only", fast_only=True)["status"], "FAST-PASSED")
            with mock.patch.object(slice_gate.fast_gate, "run_fast_gate", return_value=(True, [])), mock.patch.object(slice_gate, "input_fingerprint", return_value="fp1"), mock.patch.object(slice_gate, "_collect_locked_commits", return_value={"printer-soc": "a" * 40}):
                with mock.patch.object(slice_gate, "_qa_command", return_value=["python3", "-c", "import sys; sys.exit(1)"]):
                    self.assertEqual(slice_gate.execute_slice_funnel(ws, sp, ws / "out_blk")["status"], "BLOCKED")
                out_c1, out_c2, out_ok = ws / "out_c1", ws / "out_c2", ws / "out_ok"
                with mock.patch.object(slice_gate, "_qa_command", side_effect=lambda *_: (_write_qa_bundle(out_c1 / "docker_qa", "SLICE-T1", True), ["python3", "-c", "import sys; sys.exit(1)"])[1]):
                    self.assertEqual((slice_gate.execute_slice_funnel(ws, sp, out_c1)["status"], slice_gate.execute_slice_funnel(ws, sp, ws / "out_c0")["stage"]), ("BLOCKED", "docker_qa"))
                with mock.patch.object(slice_gate, "_qa_command", side_effect=lambda *_: _write_qa_bundle(out_c2 / "docker_qa", "SLICE-T1", False)):
                    self.assertEqual(slice_gate.execute_slice_funnel(ws, sp, out_c2)["status"], "BLOCKED")
                cv = codex_review.CodexVerdict("s1", "APPROVED", 0, [], 10, {"findings": []})
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
                (out_p / "verdict.json").write_text(json.dumps({"slice_id": "SLICE-01", "status": "FAILED", "stage": "codex"}), encoding="utf-8")
                return "Command exited with code 1."
            res = asyncio.run(_load_workflow_ns(ws, real_fail, calls)["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["SLICE-01.yaml"]}))
            self.assertEqual((res["status"], res["remediation_used"], len(calls), len(set(dirs))), ("FAILED", 2, 3, 3))
            for ret in ("Command exited with code 1.", "Command exited with code 0.", RuntimeError("crash")):
                c_miss = []
                async def miss_cmd(name: str, r=ret, **kw: object) -> str:
                    """不写 verdict.json 以模拟裁决缺失。"""
                    if isinstance(r, Exception): raise r
                    return r
                rb = asyncio.run(_load_workflow_ns(ws, miss_cmd, c_miss)["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["SLICE-01.yaml"]}))
                self.assertEqual((rb["status"], rb["remediation_used"], len(c_miss)), ("BLOCKED", 0, 1))
    def test_workflow_bg_wait_conflict_and_restart_isolation(self) -> None:
        """核验后台门禁等待结束、重启续跑目录独立、双层冲突拦截及权限拒绝零扣次。"""
        with tempfile.TemporaryDirectory() as tmp:
            ws, dirs, polls = Path(tmp), [], [0]; _write_min_slice(ws, "SLICE-01")
            async def bg_tool(name: str, **kw: object) -> str:
                """模拟 run_command 转后台并经 manage_task 等待后成功结束。"""
                if name == "run_command":
                    out_p = ws / kw["CommandLine"].split("--out-dir ")[1].split(";")[0]
                    dirs.append(str(out_p)); bg_tool.out_p = out_p
                    return "Tool is running as a background task with task id: conv/t-88"
                polls[0] += 1
                if polls[0] < 3: return "Task: conv/t-88\nStatus: RUNNING"
                _write_qa_bundle(bg_tool.out_p / "docker_qa", "SLICE-01", True); (bg_tool.out_p / "gate_exit.rc").write_text("0\n")
                (bg_tool.out_p / "verdict.json").write_text(json.dumps({"slice_id": "SLICE-01", "status": "PASSED", "stage": "codex"}))
                return "Task: conv/t-88\nStatus: DONE\nCommand exited with code 0."
            ns = _load_workflow_ns(ws, bg_tool, [])
            r_ok = asyncio.run(ns["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["SLICE-01.yaml"]}))
            polls[0] = 0; r_ok2 = asyncio.run(ns["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["SLICE-01.yaml"]}))
            self.assertEqual((r_ok["status"], r_ok["completed_slices"], r_ok2["status"], len(set(dirs))), ("PASSED", ["SLICE-01"], "PASSED", 2))
            for rc_txt, vst, qap in (("1", "PASSED", True), ("0", "FAILED", True), ("0", "PASSED", False)):
                c_cf = []
                async def cf_tool(name: str, rt=rc_txt, vs=vst, qp=qap, **kw: object) -> str:
                    """制造退出码与裁决或 Docker QA 证据冲突。"""
                    out_p = ws / kw["CommandLine"].split("--out-dir ")[1].split(";")[0]; _write_qa_bundle(out_p / "docker_qa", "SLICE-01", qp)
                    (out_p / "verdict.json").write_text(json.dumps({"slice_id": "SLICE-01", "status": vs, "stage": "codex"}))
                    return f"Command exited with code {rt}."
                rcf = asyncio.run(_load_workflow_ns(ws, cf_tool, c_cf)["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["SLICE-01.yaml"]}))
                self.assertEqual((rcf["status"], rcf["remediation_used"], len(c_cf)), ("BLOCKED", 0, 1))
            class DeniedErr(RuntimeError):
                """模拟权限被拒异常。"""
                denied = True
            async def den_cmd(name: str, **kw: object) -> str:
                """抛出权限被拒异常。"""
                raise DeniedErr("Tool denied")
            rden = asyncio.run(_load_workflow_ns(ws, den_cmd, [])["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["SLICE-01.yaml"]}))
            row = "| 2026-11-18 | B1 | SLICE-01 | SW-Verified | `p:123; inputs=aaaa1111` | `c` | `s` | `v` |"
            self.assertEqual((rden["status"], rden["remediation_used"], ns["is_slice_verified"](row, "SLICE-01", "bbbb2222"), ns["is_slice_verified"](row, "SLICE-01", "aaaa1111")), ("BLOCKED", 0, False, True))
    def test_handoff_roundtrip_and_negative_blocks(self) -> None:
        """核验 Git 交接准备与远端读回、LFS 阻塞、私有路径/失效 ref/非可达提交拒收。"""
        with tempfile.TemporaryDirectory() as tmp:
            base, bare, work, sha_ok = Path(tmp), Path(tmp) / "bare.git", Path(tmp) / "work", "1" * 39 + "a"
            git = lambda *a: subprocess.check_output(["git", *a], text=True, stderr=subprocess.DEVNULL).strip()
            git("init", "--bare", str(bare)); git("init", str(work)); git("-C", str(work), "symbolic-ref", "HEAD", "refs/heads/main")
            (work / "ev").mkdir(); (work / "ev/log.txt").write_text("ok\n", encoding="utf-8")
            meta = {"slice_id": "S1", "stage": "docker_qa", "status": "PASSED", "inputs": {"repos": {"printer-soc": {"ref": "refs/heads/main", "commit": sha_ok}}}, "evidence_paths": ["log.txt"]}
            git_handoff.prepare_handoff(work / "ev", meta, work / "ev/receipt.json")
            for args in (["add", "."], ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-m", "r1"], ["push", str(bare), "HEAD:refs/heads/main"], ["checkout", "-b", "side"]):
                git("-C", str(work), *args)
            c_main = git("-C", str(work), "rev-parse", "main"); (work / "s.txt").write_text("x\n")
            for args in (["add", "."], ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-m", "s"], ["push", str(bare), "side:refs/heads/side"]):
                git("-C", str(work), *args)
            c_side = git("-C", str(work), "rev-parse", "HEAD")
            loc = {"repo": "project-control", "ref": "refs/heads/main", "commit": c_main, "path": "ev/receipt.json", "sha256": hashlib.sha256((work / "ev/receipt.json").read_bytes()).hexdigest()}
            exp = {"stage": "docker_qa", "commits": {"printer-soc": sha_ok}, "remote_urls": {"project-control": str(bare)}}
            with self.assertRaises(git_handoff.HandoffError):
                git_handoff.verify_handoff(json.dumps(loc), {**exp, "remote_urls": {"project-control": "file://" + str(bare)}}, base / "dl_f")
            with mock.patch.object(git_handoff, "_validate_url", side_effect=lambda u: u):
                self.assertEqual(git_handoff.verify_handoff(json.dumps(loc), exp, base / "dl_ok")["receipt"]["status"], "PASSED")
                for i, (bl, be) in enumerate(((dict(loc, ref="refs/heads/miss"), exp), (dict(loc, commit=c_side), exp), (loc, {**exp, "commits": {"printer-soc": "2" * 40}}), ("/tmp/verdict.json", exp))):
                    with self.assertRaises(git_handoff.HandoffError):
                        git_handoff.verify_handoff(bl if isinstance(bl, str) else json.dumps(bl), be, base / f"dl_{i}")
            with self.assertRaises(git_handoff.HandoffError):
                git_handoff.prepare_handoff(work / "ev", {**meta, "verdict_ref": "/tmp/priv.json"}, work / "ev/bad.json")
            (work / "ev/big.bin").write_text("version https://git-lfs.github.com/spec/v1\noid sha256:" + "0" * 64 + "\nsize 10\n")
            with mock.patch("subprocess.run", return_value=subprocess.CompletedProcess(["git"], 1, "", "")), self.assertRaises(git_handoff.HandoffError):
                git_handoff._hydrate_lfs(work, "ev/big.bin", work / "ev/big.bin")
    def test_checkpoint_deliverable_cruise_and_qa_reuse(self) -> None:
        """核验检查点免冷审禁写账本、交付点核查检查点、多交付与 QA 复用/拒用。"""
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp); (ws / "project-control/config/qa_runner").mkdir(parents=True)
            (ws / "project-control/config/qa_runner/default_config.yaml").write_text("sandbox:\n  image: qa-sandbox:20261029\n")
            cp_p, d1_p, d2_p = ws / "CP1.yaml", ws / "D1.yaml", ws / "D2.yaml"
            cp_p.write_text(yaml.safe_dump({"slice_id": "SLICE-CP1", "batch_id": "B1", "delivery_kind": "checkpoint", "integration_cmd": "true", "subtasks": []}))
            d1_p.write_text(yaml.safe_dump({"slice_id": "SLICE-D1", "batch_id": "B1", "delivery_kind": "deliverable", "covered_checkpoints": ["SLICE-CP1"], "integration_cmd": "true", "qa_commands": [{"kind": "test", "subpath": ".", "command": "ok"}], "subtasks": [{"role": "ENG-AP", "repo": "printer-soc", "branch": "main", "allowed_paths": ["*"]}]}))
            d2_p.write_text(yaml.safe_dump({"slice_id": "SLICE-D2", "batch_id": "B1", "integration_cmd": "true", "subtasks": [{"role": "ENG-AP", "repo": "printer-soc", "branch": "main", "allowed_paths": ["*"]}]}))
            with mock.patch.object(slice_gate.fast_gate, "run_fast_gate", return_value=(True, [])), mock.patch.object(slice_gate, "input_fingerprint", return_value="fp1"), mock.patch.object(slice_gate, "_collect_locked_commits", return_value={"printer-soc": "a" * 40}):
                self.assertEqual((slice_gate.execute_slice_funnel(ws, cp_p, ws / "out_cp")["stage"], (ws / "project-control/slices/ledger.md").exists()), ("checkpoint", False))
            qa_src = ws / "project-control/docs/evidence/SLICE-D1/run_01/docker_qa"; _write_qa_bundle(qa_src, "SLICE-D1", True)
            sq = json.loads((qa_src / "server_qa.json").read_text()); sq.update({"qa_commands": [{"kind": "test", "subpath": ".", "command": "ok"}], "sandbox": {**sq["sandbox"], "image": "qa-sandbox:20261029"}})
            (qa_src / "server_qa.json").write_text(json.dumps(sq)); d1 = slice_gate.load_slice_spec(d1_p)
            self.assertIsNotNone(git_handoff.try_reuse_qa(ws, d1, {"printer-soc": "a" * 40}, ws / "q0"))
            self.assertIsNone(git_handoff.try_reuse_qa(ws, {**d1, "qa_commands": [{"kind": "test", "subpath": ".", "command": "ch"}]}, {"printer-soc": "a" * 40}, ws / "q1"))
            self.assertIsNone(git_handoff.try_reuse_qa(ws, d1, {"printer-soc": "b" * 40}, ws / "q2"))
            (ws / "project-control/config/qa_runner/default_config.yaml").write_text("sandbox:\n  image: qa-sandbox:other\n")
            self.assertIsNone(git_handoff.try_reuse_qa(ws, d1, {"printer-soc": "a" * 40}, ws / "q3"))
            async def pass_tool(name: str, **kw: object) -> str:
                """写出通过裁决与模拟 QA 证据。"""
                cmd = kw["CommandLine"]; out_p = ws / cmd.split("--out-dir ")[1].split(";")[0]
                sid = "SLICE-CP1" if "CP1" in cmd else ("SLICE-D1" if "D1" in cmd else "SLICE-D2")
                _write_qa_bundle(out_p / "docker_qa", sid, True)
                (out_p / "verdict.json").write_text(json.dumps({"slice_id": sid, "status": "PASSED", "stage": "checkpoint" if "CP1" in cmd else "codex"}))
                return "Command exited with code 0."
            ns = _load_workflow_ns(ws, pass_tool, [])
            self.assertEqual(asyncio.run(ns["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["D1.yaml"], "require_remote_handoff": True}))["status"], "BLOCKED")
            (ws / "project-control/docs/evidence/SLICE-CP1/checkpoint_receipt.json").unlink()
            self.assertEqual(asyncio.run(ns["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["D1.yaml"]}))["status"], "BLOCKED")
            r_two = asyncio.run(ns["run_batch_cruise"]({"workspace": str(ws), "plan_path": "p.md", "slice_files": ["CP1.yaml", "D1.yaml", "D2.yaml"]}))
            self.assertEqual((r_two["status"], r_two["completed_slices"]), ("PASSED", ["SLICE-D1", "SLICE-D2"]))
            (ws / "workspace.json").write_text(json.dumps({"workspace_project": {"branch": "main"}, "repositories": [{"path": "printer-soc", "branch": "main"}]}))
            for args in (["init", str(ws)], ["add", "workspace.json"], ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-m", "r"]): subprocess.run(["git", "-C", str(ws)] + args, check=True, capture_output=True)
            r_sha = subprocess.check_output(["git", "-C", str(ws), "rev-parse", "HEAD"], text=True).strip()
            cmd_a = slice_gate._qa_command(ws, d1, {"printer-soc": "a" * 40}, ws / "q_cmd")
            self.assertEqual(("--root-commit" in cmd_a, r_sha in cmd_a, git_handoff.try_reuse_qa(ws, d1, {"printer-soc": "a" * 40}, ws / "q4")), (True, True, None))
            with mock.patch.object(slice_gate, "_qa_command", side_effect=lambda *_: _write_qa_bundle(ws / "qb/docker_qa", "SLICE-D1", True)):
                self.assertEqual(slice_gate._run_docker_qa(ws, d1, {"printer-soc": "a" * 40}, ws / "qb")[1]["status"], "BLOCKED")
if __name__ == "__main__":
    unittest.main()
