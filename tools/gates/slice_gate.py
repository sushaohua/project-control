#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V2 垂直切片四阶无状态门禁漏斗 (`slice_gate.py`)。

顺序串联：`fast_gate` ➔ 合龙 ➔ `qa_runner` Docker ➔ Codex 冷审；统一输出 `PASSED(0)`/`FAILED(1)`/`BLOCKED(2)` 与当次证据。
"""
from __future__ import annotations
import argparse, datetime, hashlib, json, subprocess, sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1])) if str(Path(__file__).resolve().parents[1]) not in sys.path else None
from gates import codex_review, fast_gate

_STATUS_EXIT = {"PASSED": 0, "FAST-PASSED": 0, "FAILED": 1, "BLOCKED": 2}
_STAGE_IDX = {"fast_gate": 0, "integration": 1, "docker_qa": 2, "codex": 3}
_EVIDENCE_ITEMS = (("fast_gate_log", "fast_gate.log", 0), ("integration_log", "integration.log", 1), ("qa_runner_log", "docker_qa/qa_runner_call.log", 2), ("server_qa_json", "docker_qa/server_qa.json", 2), ("server_verdict_json", "docker_qa/server_verdict.json", 2), ("docker_runtime_log", "docker_qa/runtime.log", 2), ("docker_checkout_log", "docker_qa/checkout.log", 2), ("codex_final_json", "codex/final.json", 3), ("codex_jsonl", "codex/codex.jsonl", 3), ("codex_stderr", "codex/codex.stderr", 3))

def load_slice_spec(slice_path: Path) -> dict:
    """加载并校验垂直切片 YAML 配置必填字段。"""
    spec = yaml.safe_load(slice_path.read_text(encoding="utf-8"))
    miss = [k for k in ("slice_id", "batch_id", "subtasks", "integration_cmd") if k not in spec]
    if miss:
        raise ValueError(f"切片定义 {slice_path} 缺失必填字段: {miss[0]}")
    return spec

def _last_line(text: str, default: str) -> str:
    """提取输出文本最后一个非空行作为精简原因摘要。"""
    lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]
    return lines[-1][:180] if lines else default

def _collect_evidence_uris(out_dir: Path, stage: str = "codex") -> Dict[str, str]:
    """仅收集本次 `--out-dir` 内截至当前阶段的实际证据文件 `file://` 链接。"""
    max_idx = _STAGE_IDX.get(stage, 3)
    return {"verdict_json": (out_dir / "verdict.json").resolve().as_uri(), **{k: (out_dir / rel).resolve().as_uri() for k, rel, idx in _EVIDENCE_ITEMS if idx <= max_idx and (out_dir / rel).is_file()}}

def _write_gate_verdict(out_dir: Path, spec: dict, doc: dict) -> dict:
    """固化带三态结论与当次证据链接的 `verdict.json`，返回精简门禁结果。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    ev = _collect_evidence_uris(out_dir, doc.get("stage", "codex"))
    payload = {"slice_id": spec.get("slice_id", ""), "batch_id": spec.get("batch_id", ""), "profile": spec.get("profile", "host-software"), **doc, "evidence": ev}
    raw = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
    v_sha, st = hashlib.sha256(raw).hexdigest(), payload["status"]
    (out_dir / "verdict.json").write_bytes(raw)
    return {"slice_id": payload["slice_id"], "status": st, "passed": st in ("PASSED", "FAST-PASSED"), "exit_code": _STATUS_EXIT[st], "stage": payload["stage"], "reason": payload["reason"], "next_step": payload["next_step"], "evidence": ev, "verdict_sha256": v_sha, "verdict": payload}

def _run_shell_step(cmd: str, cwd: Path, timeout_sec: int = 180) -> Tuple[int, str]:
    """在指定目录执行受超时保护的子进程命令并返回 `(退出码, 合并输出)`。"""
    try:
        proc = subprocess.run(["bash", "-lc", cmd], cwd=str(cwd), text=True, capture_output=True, timeout=timeout_sec)
        return proc.returncode, ((proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")).strip()
    except subprocess.TimeoutExpired as err:
        return 124, f"命令执行超时 ({timeout_sec}s): {err}"
    except OSError as err:
        return 126, f"命令启动失败: {err}"

def _collect_locked_commits(workspace: Path, subtasks: List[dict]) -> Dict[str, str]:
    """读取切片涉及各子仓当前的完整 40 位 HEAD Commit SHA。"""
    return {st["repo"]: subprocess.check_output(["git", "-C", str(workspace / st["repo"]), "rev-parse", "HEAD"], text=True).strip() for st in subtasks}

def input_repositories(spec: dict) -> List[str]:
    """返回 spec 的业务及只读输入仓路径；重复输入只保留一次。"""
    return list(dict.fromkeys([item["repo"] for item in spec["subtasks"]] + spec.get("input_repositories", [])))

def input_fingerprint(workspace: Path, spec: dict) -> str:
    """以 workspace 当前提交、spec 内容及工作区清单形成完整输入摘要。"""
    payload = {"spec": spec, "commits": _collect_locked_commits(workspace, [{"repo": n} for n in input_repositories(spec)])}
    if (workspace / "workspace.json").is_file():
        payload["workspace_manifest"] = hashlib.sha256((workspace / "workspace.json").read_bytes()).hexdigest()
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

def _qa_command(workspace: Path, spec: dict, commits: dict, qa_dir: Path) -> list:
    """按 Runner 的实际参数接口生成命令；四参数分别为工作区、切片、候选与证据目录。"""
    cmd = [sys.executable, str(workspace / "project-control/tools/qa_runner/qa_runner.py"), "--task", spec["slice_id"], "--revision", str(spec.get("revision", 1)), "--profile", spec.get("profile", "host-software"), "--output-dir", str(qa_dir)]
    branches = {r["path"]: r["branch"] for r in json.loads((workspace / "workspace.json").read_text())["repositories"]}
    branches.update({item["repo"]: item["branch"] for item in spec["subtasks"]})
    for name, commit in commits.items():
        cmd.extend(["--repo-commit", f"{name}={commit}:refs/heads/{branches[name]}"])
    return cmd + [x for ck in spec.get("qa_commands", []) for x in ("--cmd", f"{ck['kind']}:{ck['subpath']}:{ck['command']}")]

def _verify_qa_evidence(qa_dir: Path, spec: dict, commits: Dict[str, str], proof: dict) -> str:
    """核验 `server_qa`、`server_verdict` 与 `server_lock` 摘要、状态及提交均确认通过。"""
    sid, vp, lp = spec.get("slice_id", ""), qa_dir / "server_verdict.json", qa_dir / "server_lock.json"
    if proof.get("passed") is not True or proof.get("fresh_checkout") is not True or proof.get("task_id") != sid:
        return f"server_qa 状态或任务标识未确认通过 (passed={proof.get('passed')})"
    if not (vp.is_file() and lp.is_file()):
        return "缺失 server_verdict.json 或 server_lock.json"
    try:
        vb, lb = vp.read_bytes(), lp.read_bytes()
        if hashlib.sha256(vb).hexdigest() != (proof.get("server_verdict") or {}).get("sha256") or hashlib.sha256(lb).hexdigest() != (proof.get("server_lock") or {}).get("sha256"):
            return "server_verdict 或 server_lock 摘要与 server_qa 不一致"
        vd, ld = json.loads(vb.decode("utf-8")), json.loads(lb.decode("utf-8"))
    except (OSError, ValueError) as err:
        return f"QA 证据读取或解析失败: {err}"
    if vd.get("verdict") != "PASSED" or vd.get("exit_code") != 0 or vd.get("task_id") != sid:
        return f"server_verdict 未确认通过 ({vd.get('verdict')}, exit={vd.get('exit_code')})"
    return "" if {r.get("name"): r.get("commit") for r in (ld.get("repositories") or []) if isinstance(r, dict)} == commits else "server_lock.json 锁定提交不一致"

def _run_docker_qa(workspace: Path, spec: dict, commits: Dict[str, str], out_dir: Path) -> Tuple[Optional[dict], Optional[dict]]:
    """调用 `qa_runner.py` 执行隔离容器回归，强一致校验退出码与当次证据。"""
    qa_dir, proof_path = out_dir / "docker_qa", out_dir / "docker_qa/server_qa.json"
    qa_dir.mkdir(parents=True, exist_ok=True)
    blk = lambda r: (None, _write_gate_verdict(out_dir, spec, {"commits": commits, "status": "BLOCKED", "stage": "docker_qa", "reason": r, "next_step": "核查 Docker QA 环境与当次证据后使用新目录重跑（不扣返修）"}))
    try:
        proc = subprocess.run(_qa_command(workspace, spec, commits, qa_dir), cwd=str(workspace), text=True, capture_output=True, timeout=600)
        call_log = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
        (qa_dir / "qa_runner_call.log").write_text(call_log + "\n", encoding="utf-8")
    except (subprocess.TimeoutExpired, OSError) as err:
        (qa_dir / "qa_runner_call.log").write_text(f"qa_runner 执行异常: {err}\n", encoding="utf-8")
        return blk(f"Docker QA 超时或异常: {err}")
    if not proof_path.is_file():
        return blk(_last_line(call_log, "未生成 server_qa.json（远端或容器环境阻塞）"))
    try:
        proof = json.loads(proof_path.read_text(encoding="utf-8"))
    except ValueError as err:
        return blk(f"server_qa.json 解析失败: {err}")
    if proc.returncode != 0:
        return (None, _write_gate_verdict(out_dir, spec, {"commits": commits, "status": "FAILED", "stage": "docker_qa", "reason": proof.get("summary") or "Docker 隔离沙箱测试失败", "next_step": "查阅 docker_runtime_log 与 server_verdict_json 修复失败项"})) if proof.get("passed") is False else blk(f"Docker QA 退出码与当次证据冲突 (rc={proc.returncode}, passed={proof.get('passed')})")
    err = _verify_qa_evidence(qa_dir, spec, commits, proof)
    return blk(f"Docker QA 退出码为 0 但当次证据未确认通过: {err}") if err else (proof, None)

def _build_review_prompt(spec: dict, commits: Dict[str, str], qa_proof: dict, int_log: str = "") -> str:
    """构造仅含精确元数据、验收条款与客观沙箱摘要的双轴冷审提示词。"""
    criteria = "\n".join(f"- {item}" for item in spec.get("acceptance_criteria", []))
    vp, rp = qa_proof.get("server_verdict", {}).get("path", ""), qa_proof.get("runtime_log", {}).get("path", "")
    return f"独立只读双轴冷审切片: {spec['slice_id']}\n契约: {spec.get('contract_ref')}\n方案: {spec.get('plan_ref')}\n锁定提交: {json.dumps(commits, ensure_ascii=False)}\n容器: {qa_proof.get('sandbox', {}).get('container_id', 'ok')}\n当前沙箱产物: server_verdict={vp} runtime_log={rp} integration_log={int_log}\n验收判据:\n{criteria}\n请严格按 BLOCKER / MINOR / NIT 分级。"

def append_ledger_entry(ledger_path: Path, entry: dict) -> None:
    """将通过四阶漏斗的切片记录与 `MINOR` 技术债幂等追加写入 `slices/ledger.md`。"""
    text = ledger_path.read_text(encoding="utf-8") if ledger_path.is_file() else ""
    now, identity = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), entry.get("input_fingerprint", "")
    commit_text = entry["commits_short"] + (f"; inputs={identity}" if identity else "")
    row, marker = f"| {now} | {entry['batch_id']} | {entry['slice_id']} | {entry['status']} | `{commit_text}` | `{entry['container_id']}` | `{entry['codex_session']}` | `{entry['verdict_sha256'][:16]}` |\n", "## 2. 非阻断技术债登记表"
    if not any(f"| {entry['slice_id']} | {entry['status']} |" in ln and (f"inputs={identity}" in ln if identity else True) for ln in text.splitlines()):
        text = text.replace(marker, row + "\n" + marker, 1) if marker in text else text + "\n" + row
    for item in entry.get("minors", []):
        debt = f"| {now} | {entry['slice_id']} | `{item['axis']}` | `{item['location']}` | {item['message']} |\n"
        text = text + debt if debt not in text else text
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(text, encoding="utf-8")

def _run_codex_stage(workspace: Path, spec: dict, commits: Dict[str, str], ctx: dict) -> dict:
    """执行第 4 阶独立 Codex 审查，输出 `PASSED`/`FAILED`/`BLOCKED` 并维护账本。"""
    out_dir = ctx["out_dir"]
    try:
        v = codex_review.run_codex_audit(_build_review_prompt(spec, commits, ctx["qa_proof"], str(out_dir / "integration.log")), spec["slice_id"], workspace, out_dir / "codex")
    except (codex_review.CodexGateBlockedError, ValueError) as err:
        blk = isinstance(err, codex_review.CodexGateBlockedError)
        return _write_gate_verdict(out_dir, spec, {"commits": commits, "input_fingerprint": ctx["fp"], "status": "BLOCKED" if blk else "FAILED", "stage": "codex", "decision": "BLOCKED" if blk else "REJECTED", "reason": err.reason if blk else f"Codex 裁决校验失败: {err}", "next_step": "恢复 Codex 环境后重跑（不扣返修）" if blk else "查看 codex_final_json 后重审"})
    blockers = [f for f in v.payload.get("findings", []) if f.get("severity") == "BLOCKER"]
    top = f"{blockers[0]['id']}: {blockers[0]['message'][:120]}" if blockers else "存在阻断问题"
    st, reason, nxt = {"APPROVED": ("PASSED", f"四阶门禁全绿 (0 BLOCKER, {len(v.minor_findings)} MINOR)", "申请 Human Gate #2 执行真机 HIL 验收" if spec.get("requires_hil_immediately") else "已登记 SW-Verified，可推进后续切片"), "BLOCKED": ("BLOCKED", "独立 Codex 判定环境或物证缺失阻塞", "按 codex_final_json 补齐环境或物证后重跑（不扣返修）"), "REJECTED": ("FAILED", f"独立 Codex 拒单 ({v.blocker_count} BLOCKER): {top}", "按 codex_final_json 修复 BLOCKER 项后重过四阶门禁")}[v.decision]
    res = _write_gate_verdict(out_dir, spec, {"commits": commits, "input_fingerprint": ctx["fp"], "status": st, "stage": "codex", "decision": v.decision, "codex_session": v.session_id, "blocker_count": v.blocker_count, "findings": v.payload["findings"], "reason": reason, "next_step": nxt})
    if st == "PASSED":
        append_ledger_entry(workspace / spec.get("ledger_ref", "project-control/slices/ledger.md"), {"batch_id": spec["batch_id"], "slice_id": spec["slice_id"], "status": "SW-Verified", "commits_short": ",".join(f"{k}:{v[:7]}" for k, v in commits.items()), "container_id": ctx["qa_proof"].get("sandbox", {}).get("container_id", "n/a")[:12], "codex_session": v.session_id, "verdict_sha256": res["verdict_sha256"], "minors": v.minor_findings, "input_fingerprint": ctx["fp"]})
    return res

def execute_slice_funnel(workspace: Path, slice_path: Path, out_dir: Path, fast_only: bool = False) -> dict:
    """顺序执行四阶门禁漏斗并统一落盘 `PASSED`/`FAILED`/`BLOCKED`，严禁复用非空证据目录。"""
    spec = load_slice_spec(slice_path)
    if out_dir.is_symlink() or (out_dir.exists() and (not out_dir.is_dir() or any(out_dir.iterdir()))):
        return {"slice_id": spec["slice_id"], "status": "BLOCKED", "passed": False, "exit_code": 2, "stage": "gate_init", "reason": f"拒绝复用非空证据目录: {out_dir}", "next_step": "每次运行须指定全新独立证据目录（不扣返修）", "evidence": {"existing_dir": out_dir.resolve().as_uri()}, "verdict_sha256": ""}
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        ok_fast, fast_errs = fast_gate.run_fast_gate(workspace, slice_path=slice_path)
        (out_dir / "fast_gate.log").write_text("\n".join(fast_errs) + "\n" if fast_errs else "PASS\n", encoding="utf-8")
    except (subprocess.CalledProcessError, OSError, KeyError, ValueError) as err:
        return _write_gate_verdict(out_dir, spec, {"status": "BLOCKED", "stage": "fast_gate", "reason": f"Fast-Gate 环境异常: {err}", "next_step": "修复仓库或工具链后重跑（不扣返修）"})
    if not ok_fast:
        return _write_gate_verdict(out_dir, spec, {"status": "FAILED", "stage": "fast_gate", "reason": f"Fast-Gate 未通过 ({len(fast_errs)} 项): {fast_errs[0][:140]}", "next_step": "查阅 fast_gate_log 修复契约/代码/边界问题"})
    rc_int, int_log = _run_shell_step(spec["integration_cmd"], workspace)
    (out_dir / "integration.log").write_text((int_log or "") + "\n", encoding="utf-8")
    if rc_int != 0:
        is_blk = rc_int == 124 or "docker daemon" in int_log.lower() or "ssh:" in int_log.lower()
        return _write_gate_verdict(out_dir, spec, {"status": "BLOCKED" if is_blk else "FAILED", "stage": "integration", "reason": _last_line(int_log, f"合龙阶段退出码 {rc_int}"), "next_step": "恢复运行环境后重跑（不扣返修）" if is_blk else "查阅 integration_log 修复合龙失败"})
    if fast_only:
        return _write_gate_verdict(out_dir, spec, {"status": "FAST-PASSED", "stage": "integration", "reason": "前两阶 Fast-Gate 与合龙预检通过 (--fast-only)", "next_step": "运行完整四阶 slice_gate.py 完成容器 QA 与 Codex 准出"})
    try:
        fp, commits = input_fingerprint(workspace, spec), _collect_locked_commits(workspace, [{"repo": n} for n in input_repositories(spec)])
    except (subprocess.CalledProcessError, OSError, KeyError) as err:
        return _write_gate_verdict(out_dir, spec, {"status": "BLOCKED", "stage": "docker_qa", "reason": f"采集锁定提交失败: {err}", "next_step": "检查子仓 Git 与 workspace.json（不扣返修）"})
    qa_proof, qa_fail = _run_docker_qa(workspace, spec, commits, out_dir)
    return qa_fail if qa_fail is not None else _run_codex_stage(workspace, spec, commits, {"out_dir": out_dir, "fp": fp, "qa_proof": qa_proof})
def main(argv: Optional[List[str]] = None) -> int:
    """命令行入口：执行指定 `SLICE-XX.yaml` 四阶门禁并按 `0/1/2` 输出精简裁决。"""
    p = argparse.ArgumentParser(description="AI SoC V2 垂直切片四阶无状态门禁")
    for opt, kw in (("--workspace", {"type": Path, "default": Path(__file__).resolve().parents[3]}), ("--slice", {"type": Path, "required": True}), ("--out-dir", {"type": Path, "required": True}), ("--fast-only", {"action": "store_true"})):
        p.add_argument(opt, **kw)
    ns = p.parse_args(argv)
    res = execute_slice_funnel(ns.workspace, ns.slice, ns.out_dir, ns.fast_only)
    print(json.dumps({k: res[k] for k in ("slice_id", "status", "stage", "reason", "next_step", "evidence", "verdict_sha256")}, ensure_ascii=False, indent=2))
    return int(res["exit_code"])
if __name__ == "__main__":
    sys.exit(main())
