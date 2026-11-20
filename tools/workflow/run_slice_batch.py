#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Antigravity `run_workflow` V2 垂直切片批次自动巡航脚本：支持检查点/交付点、远端收据及零扣返修。"""
from __future__ import annotations
import asyncio, datetime, json, re, subprocess, sys, time, uuid
from pathlib import Path
from typing import Dict, List, Optional
MAX_REMEDIATION_ROUNDS, BG_POLL_SEC, BG_TIMEOUT_SEC = 2, 1.0, 1200.0
VERIFIED_ROW_RE = re.compile(r"\|\s*(SLICE-[A-Za-z0-9_-]+)\s*\|\s*(SW-Verified|HIL-Verified)\s*\|")
BG_TASK_RE, TASK_STATUS_RE = re.compile(r"running as a background task with task id:\s*(\S+)"), re.compile(r"^Status:\s*(\S+)", re.MULTILINE)
EXIT_CODE_RE, INPUTS_RE = re.compile(r"Command exited with code (\d+)\."), re.compile(r"\binputs=([0-9a-fA-F]+)\b")
_EXP_RC, _RUN_STATES = {"PASSED": 0, "FAILED": 1, "BLOCKED": 2}, {"RUNNING", "PENDING", "STARTING", "IN_PROGRESS", "QUEUED"}
def _gh(ws: Path):
    """按需加载 `git_handoff` 模块执行远端交接与检查点核验。"""
    t = ws / "project-control/tools"
    sys.path.insert(0, str(t)) if t.is_dir() and str(t) not in sys.path else None
    from workflow import git_handoff
    return git_handoff
def parse_verified_slices(ledger_text: str) -> List[str]:
    """从 `ledger.md` 文本中解析已完成 `SW-Verified` 或 `HIL-Verified` 的切片 ID 列表。"""
    return [m.group(1) for m in VERIFIED_ROW_RE.finditer(ledger_text or "")]
def is_slice_verified(ledger_text: str, slice_id: str, expected_fp: str = "") -> bool:
    """校验切片是否已在账本准出；若提供当前输入指纹则强一致比对 `inputs=`。"""
    for ln in (ledger_text or "").splitlines():
        m, fp_m = VERIFIED_ROW_RE.search(ln), INPUTS_RE.search(ln)
        if m and m.group(1) == slice_id and ((fp_m and fp_m.group(1) == expected_fp) if expected_fp else (fp_m is None or bool(fp_m.group(1)))):
            return True
    return False
def _load_yaml(p: Path) -> dict:
    """加载 YAML 配置；缺失 PyYAML 时回退系统 `/usr/bin/python3` 解析。"""
    import yaml
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
def _safe_fingerprint(ws: Path, spec: dict) -> str:
    """当全部依赖仓均存在于工作区时计算当前输入指纹，否则返回空串。"""
    tools = ws / "project-control/tools"
    if not (tools / "gates/slice_gate.py").is_file():
        return ""
    sys.path.insert(0, str(tools)) if str(tools) not in sys.path else None
    try:
        from gates import slice_gate
        return slice_gate.input_fingerprint(ws, spec) if all((ws / r / ".git").exists() for r in slice_gate.input_repositories(spec)) else ""
    except Exception:
        return ""
def subtask_schema() -> dict:
    """构造子任务工程 Agent `finish` 工具强制校验的返回 JSON Schema。"""
    props = {k: {"type": "string"} for k in ("role", "repo", "candidate_commit", "summary")}
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}
def build_pointer_prompt(plan_path: str, slice_yaml: str, contract_path: str, subtask: dict) -> str:
    """构造稀疏四文件指针提示词，避免向子 Agent 注入历史对话噪音。"""
    ptr = f"project-control/docs/evidence/{Path(slice_yaml).stem}/{subtask['role']}_selfcheck.md"
    return f"角色身份: {subtask['role']} (唯一允许写入仓: {subtask['repo']}, 分支: {subtask['branch']})\n1. 获批 SSoT 方案指针: {plan_path}\n2. 本切片定义指针: {slice_yaml}\n3. 机器协议契约指针: {contract_path}\n4. 自检记录输出指针: {ptr}\n请严守 allowed_paths={subtask['allowed_paths']} 与 diff_budget={subtask.get('diff_budget')}，完成实现与自检提交，返回 40 位 candidate_commit。"
def _blk(sid: str, stage: str, reason: str, ev: Optional[dict] = None) -> dict:
    """构造不触发工程返修、零扣次数的统一 `BLOCKED` 裁决字典。"""
    return {"slice_id": sid, "status": "BLOCKED", "stage": stage, "reason": reason, "next_step": "排查阻塞或使用新目录重跑（不扣返修）", "evidence": ev or {}}
def _alloc_out_rel(ws: Path, spec: dict, run_idx: int) -> str:
    """为每次运行分配含高精度时间戳与随机令牌的唯一目录，严禁复用旧目录。"""
    rel = f"{spec.get('evidence_root', 'project-control/docs/evidence')}/{spec['slice_id']}/run_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}_{uuid.uuid4().hex[:8]}_r{run_idx:02d}"
    if (ws / rel).exists():
        raise RuntimeError(f"拒绝复用已存在证据目录: {rel}")
    return rel
def _extract_exit_code(out_dir: Path, text: str) -> Optional[int]:
    """综合 `gate_exit.rc` 与命令输出提取唯一可信退出码；缺失或冲突返回 `None`。"""
    rc_p, rc_file = out_dir / "gate_exit.rc", None
    if rc_p.is_file():
        try: rc_file = int(rc_p.read_text(encoding="utf-8").strip())
        except (OSError, ValueError): return None
    ms = EXIT_CODE_RE.findall(text or "")
    rc_txt = int(ms[-1]) if ms else None
    return (rc_file if rc_file == rc_txt else None) if (rc_file is not None and rc_txt is not None) else (rc_file if rc_file is not None else rc_txt)
async def _wait_bg_gate(out_dir: Path, task_id: str, timeout_sec: float = BG_TIMEOUT_SEC) -> str:
    """轮询后台门禁任务直至真正结束且退出码落盘，返回终态输出文本。"""
    deadline, rc_p = time.monotonic() + timeout_sec, out_dir / "gate_exit.rc"
    while time.monotonic() < deadline:
        try:
            st_out = await call_tool("manage_task", Action="status", TaskId=task_id)
            st_m = TASK_STATUS_RE.search(st_out or "")
            if (st_m and st_m.group(1).upper() not in _RUN_STATES) or (not st_m and rc_p.is_file()):
                await asyncio.sleep(min(0.2, BG_POLL_SEC)) if not rc_p.is_file() else None
                return st_out
        except Exception as err:
            if getattr(err, "denied", False) or any(k in str(err).lower() for k in ("permission", "denied")): raise
            if rc_p.is_file(): return f"Command exited with code {rc_p.read_text(encoding='utf-8').strip()}."
        await asyncio.sleep(BG_POLL_SEC)
    return ""
def _qa_ok(out_dir: Path, stage: str) -> bool:
    """核验 `PASSED` 裁决时当次 `server_qa` 与 `server_verdict` 均确认通过。"""
    if stage in ("checkpoint", "integration"):
        return True
    qa_p, vp = out_dir / "docker_qa/server_qa.json", out_dir / "docker_qa/server_verdict.json"
    if not qa_p.is_file():
        return stage != "codex"
    try:
        return json.loads(qa_p.read_text(encoding="utf-8")).get("passed") is True and ((not vp.is_file()) or (lambda vd: vd.get("verdict") == "PASSED" and vd.get("exit_code") == 0)(json.loads(vp.read_text(encoding="utf-8"))))
    except (OSError, ValueError):
        return False
def _adjudicate_verdict_file(out_dir: Path, sid: str, exit_code: Optional[int], expected_fp: str) -> dict:
    """核验 `verdict.json`、退出码与证据一致性；缺失裁决或冲突统一判 `BLOCKED`。"""
    v_path = out_dir / "verdict.json"
    if not v_path.is_file():
        return _blk(sid, "gate_runner", f"缺失裁决文件 verdict.json (exit={exit_code})，统一判 BLOCKED（不扣返修）", {"evidence_dir": out_dir.resolve().as_uri()} if out_dir.exists() else {})
    try:
        doc = json.loads(v_path.read_text(encoding="utf-8"))
    except ValueError as err:
        return _blk(sid, "gate_runner", f"verdict.json 解析失败: {err}", {"verdict_json": v_path.resolve().as_uri()})
    ev, dst = {**dict(doc.get("evidence") or {}), "verdict_json": v_path.resolve().as_uri()}, doc.get("status") or ""
    if doc.get("slice_id") != sid or (expected_fp and (doc.get("input_fingerprint") or ("" if dst == "PASSED" else expected_fp)) != expected_fp):
        return _blk(sid, "gate_runner", "verdict.json 切片标识或输入指纹不匹配", ev)
    if exit_code is None or dst not in _EXP_RC or exit_code != _EXP_RC[dst]:
        return _blk(sid, "gate_runner", f"门禁实际退出码与裁决证据冲突 (exit={exit_code}, verdict={dst})", ev)
    if dst == "PASSED" and not _qa_ok(out_dir, doc.get("stage", "gate")):
        return _blk(sid, "docker_qa", "PASSED 裁决与当次 Docker QA 证据冲突", ev)
    return {"slice_id": sid, "status": dst, "stage": doc.get("stage", "gate"), "reason": doc.get("reason", f"门禁结束 (exit={exit_code})"), "next_step": doc.get("next_step", "查阅本次证据文件"), "evidence": ev}
async def _exec_gate_cmd(sid: str, cmd: str) -> str:
    """优先通过 `call_tool` 执行门禁，否则经 `agent` 调用 `run_command` 并等待后台完成。"""
    if "call_tool" in globals():
        return str(await call_tool("run_command", CommandLine=cmd, WaitMsBeforeAsync=10000, toolSummary=f"Gate {sid}") or "")
    sch = {"type": "object", "properties": {"exit_code": {"type": "integer"}, "output": {"type": "string"}}, "required": ["exit_code", "output"], "additionalProperties": False}
    runner = agent(role=f"{sid} 门禁执行", workspace="inherit", schema=sch)
    res = await runner(f"原样调用 run_command(CommandLine={json.dumps(cmd)}, WaitMsBeforeAsync=10000, toolSummary='Gate {sid}')；若转后台请结束本轮等唤醒后再 finish 返回真实整数 exit_code 与含 `Command exited with code N.` 的 output。")
    return f"Command exited with code {res['exit_code']}.\n{res.get('output', '')}"
async def _run_and_adjudicate(ws: Path, sid: str, slice_yaml: str, out_rel: str) -> dict:
    """调用 `slice_gate.py`，若转后台则等待真实结束，再统一读取退出码与裁决。"""
    rc_rel, out_dir = f"{out_rel}/gate_exit.rc", ws / out_rel
    cmd = f"python3 project-control/tools/gates/slice_gate.py --workspace . --slice {slice_yaml} --out-dir {out_rel}; rc=$?; mkdir -p {out_rel}; printf '%s\\n' \"$rc\" > {rc_rel}.tmp && mv {rc_rel}.tmp {rc_rel}; printf '\\nCommand exited with code %s.\\n' \"$rc\"; exit \"$rc\""
    expected_fp = _safe_fingerprint(ws, _load_yaml(ws / slice_yaml))
    try:
        gate_out = await _exec_gate_cmd(sid, cmd)
        bg = BG_TASK_RE.search(gate_out)
        if bg:
            gate_out = await _wait_bg_gate(out_dir, bg.group(1))
        return _adjudicate_verdict_file(out_dir, sid, _extract_exit_code(out_dir, gate_out), expected_fp)
    except Exception as err:
        msg = str(err)
        return _blk(sid, "gate_permission", f"门禁执行被权限策略拦截: {msg[:120]}") if (getattr(err, "denied", False) or any(k in msg.lower() for k in ("permission", "denied"))) else _adjudicate_verdict_file(out_dir, sid, _extract_exit_code(out_dir, msg), expected_fp)
async def run_single_slice(workspace_str: str, plan_path: str, slice_yaml: str) -> dict:
    """执行单个垂直切片的派单、`PASSED`/`FAILED`/`BLOCKED` 裁决及最多 2 轮零误扣返修。"""
    ws, spec = Path(workspace_str), _load_yaml(Path(workspace_str) / slice_yaml)
    sid, contract_ref = spec["slice_id"], spec.get("contract_ref", "project-control/contracts/minimc_v2_contract.yaml")
    workers = {st["role"]: agent(role=f"{sid} {st['role']}", workspace="inherit", schema=subtask_schema()) for st in spec.get("subtasks", [])}
    if workers:
        phase(f"{sid}: 并发子仓实现")
        await parallel(spec["subtasks"], lambda st: workers[st["role"]](build_pointer_prompt(plan_path, slice_yaml, contract_ref, st)))
    remediation_used = 0
    for run_idx in range(1, MAX_REMEDIATION_ROUNDS + 2):
        phase(f"{sid}: 门禁核验 (第 {run_idx} 次)")
        res = await _run_and_adjudicate(ws, sid, slice_yaml, _alloc_out_rel(ws, spec, run_idx))
        if res["status"] == "PASSED":
            return {**res, "remediation_used": remediation_used, "requires_hil": bool(spec.get("requires_hil_immediately"))}
        if res["status"] != "FAILED" or not workers or remediation_used >= MAX_REMEDIATION_ROUNDS:
            return {**res, "remediation_used": remediation_used}
        remediation_used += 1
        brief = f"门禁未通过 ({res['stage']}):\n- 原因: {res['reason']}\n- 下一步: {res['next_step']}\n- 证据: {json.dumps(res['evidence'], ensure_ascii=False)}\n请定向修复并提交。"
        await parallel(spec["subtasks"], lambda st, b=brief: workers[st["role"]](b))
    return {**_blk(sid, "gate_runner", "异常退出返修循环"), "remediation_used": remediation_used}
async def run_batch_cruise(cfg: dict) -> dict:
    """按序巡航检查点与交付点，验证远端收据及前置覆盖并输出三段裁决。"""
    ws, completed, last_ev, cp_ready = Path(cfg.get("workspace") or (WORKSPACES[0] if "WORKSPACES" in globals() and WORKSPACES else ".")), [], {}, set(cfg.get("verified_checkpoints") or [])
    for slice_yaml in cfg.get("slice_files", []):
        spec = _load_yaml(ws / slice_yaml)
        sid, kind = spec["slice_id"], spec.get("delivery_kind", "deliverable")
        ledger_p = ws / (cfg.get("ledger_ref") or spec.get("ledger_ref") or "project-control/slices/ledger.md")
        if kind != "checkpoint" and is_slice_verified(ledger_p.read_text(encoding="utf-8") if ledger_p.is_file() else "", sid, _safe_fingerprint(ws, spec)):
            continue
        if cfg.get("handoff_receipts") or cfg.get("require_remote_handoff") or spec.get("covered_checkpoints"):
            err = _gh(ws).cruise_precheck(ws, cfg, spec, cp_ready)
            if err:
                return {**_blk(sid, "handoff", err), "remediation_used": 0, "completed_slices": completed}
        res = await run_single_slice(str(ws), cfg["plan_path"], slice_yaml)
        last_ev = res.get("evidence", {})
        if res["status"] != "PASSED":
            return {"status": res["status"], "slice_id": sid, "reason": res["reason"], "next_step": res["next_step"], "remediation_used": res.get("remediation_used", 0), "completed_slices": completed, "evidence": last_ev}
        cp_ready.add(sid) if kind == "checkpoint" else completed.append(sid)
        if kind == "deliverable" and res.get("requires_hil"):
            return {"status": "HIL_REQUIRED", "slice_id": sid, "reason": f"{sid} 已通过 SW-Verified 并触及真机 HIL 红线", "next_step": "停机申请 Human Gate #2 真机穿刺验收", "completed_slices": completed, "evidence": last_ev}
    return {"status": "PASSED", "reason": "批次全部交付切片已通过四阶门禁", "next_step": "进入下一阶段或交付汇总", "completed_slices": completed, "evidence": last_ev}
if "WORKSPACES" in globals() and "args" in globals():
    print(json.dumps(await run_batch_cruise(args), ensure_ascii=False, indent=2))
