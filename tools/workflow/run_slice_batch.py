#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Antigravity `run_workflow` V2 垂直切片批次自动巡航脚本 (`run_slice_batch.py`)。

沿用四阶漏斗执行幂等续跑与三态推进：仅 `PASSED` 推进，`FAILED` 触发最多 2 轮 `ENG-*` 定向返修，
`BLOCKED` 或权限拒绝立即停机且零扣减返修次数，汇报仅含结果/原因/下一步与当次 `file://` 证据链接。
"""

from __future__ import annotations

import json, re, sys
from pathlib import Path
from typing import Dict, List
import yaml

MAX_REMEDIATION_ROUNDS = 2
VERIFIED_ROW_RE = re.compile(r"\|\s*(SLICE-[A-Za-z0-9_-]+)\s*\|\s*(SW-Verified|HIL-Verified)\s*\|")
EXIT_CODE_RE = re.compile(r"Command exited with code (\d+)\.")
INPUTS_RE = re.compile(r"\binputs=([0-9a-fA-F]+)\b")

def parse_verified_slices(ledger_text: str) -> List[str]:
    """从 `ledger.md` 文本中解析已完成 `SW-Verified` 或 `HIL-Verified` 的切片 ID 列表。"""
    return [m.group(1) for m in VERIFIED_ROW_RE.finditer(ledger_text or "")]

def is_slice_verified(ledger_text: str, slice_id: str, expected_fp: str = "") -> bool:
    """校验切片是否已在账本准出；若提供当前输入指纹则强一致比对 `inputs=`。"""
    for line in (ledger_text or "").splitlines():
        m = VERIFIED_ROW_RE.search(line)
        if not m or m.group(1) != slice_id:
            continue
        fp_m = INPUTS_RE.search(line)
        if (fp_m and fp_m.group(1) == expected_fp) if expected_fp else (fp_m is None or bool(fp_m.group(1))):
            return True
    return False

def _safe_fingerprint(ws: Path, spec: dict) -> str:
    """当全部依赖仓均存在于工作区时计算当前输入指纹，否则返回空串。"""
    tools_dir = ws / "project-control/tools"
    if str(tools_dir) not in sys.path and tools_dir.is_dir():
        sys.path.insert(0, str(tools_dir))
    try:
        from gates import slice_gate
        repos = slice_gate.input_repositories(spec)
        return slice_gate.input_fingerprint(ws, spec) if all((ws / r / ".git").exists() for r in repos) else ""
    except Exception:
        return ""

def subtask_schema() -> dict:
    """构造子任务工程 Agent `finish` 工具强制校验的返回 JSON Schema。"""
    props = {"role": {"type": "string"}, "repo": {"type": "string"}, "candidate_commit": {"type": "string"}, "summary": {"type": "string"}}
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}

def build_pointer_prompt(plan_path: str, slice_yaml: str, contract_path: str, subtask: dict) -> str:
    """构造稀疏四文件指针提示词，避免向子 Agent 注入历史对话噪音。"""
    report_ptr = f"project-control/docs/evidence/{Path(slice_yaml).stem}/{subtask['role']}_selfcheck.md"
    return f"角色身份: {subtask['role']} (唯一允许写入仓: {subtask['repo']}, 分支: {subtask['branch']})\n1. 获批 SSoT 方案指针: {plan_path}\n2. 本切片定义指针: {slice_yaml}\n3. 机器协议契约指针: {contract_path}\n4. 自检记录输出指针: {report_ptr}\n请严守 allowed_paths={subtask['allowed_paths']} 与 diff_budget={subtask.get('diff_budget')}，完成实现与自检提交，返回 40 位 candidate_commit。"


def _adjudicate_verdict_file(out_dir: Path, sid: str, gate_out: str, expected_fp: str) -> dict:
    """结合 `run_command` 退出码与当次 `verdict.json` 严格裁决 `PASSED`/`FAILED`/`BLOCKED`。"""
    text = str(gate_out or "")
    m = EXIT_CODE_RE.search(text)
    exit_code = -1 if "running as a background task" in text else (int(m.group(1)) if m else 0)
    v_path = out_dir / "verdict.json"
    if not v_path.is_file():
        st = "FAILED" if exit_code == 1 else "BLOCKED"
        return {"slice_id": sid, "status": st, "stage": "gate_runner", "reason": f"未产出当次 verdict.json (exit={exit_code})", "next_step": "查看门禁调用输出或恢复环境后重跑", "evidence": {}}
    try:
        doc = json.loads(v_path.read_text(encoding="utf-8"))
    except ValueError as err:
        return {"slice_id": sid, "status": "BLOCKED", "stage": "gate_runner", "reason": f"verdict.json 解析失败: {err}", "next_step": "核查 verdict.json 文件完整性", "evidence": {"verdict_json": v_path.resolve().as_uri()}}
    ev = {**dict(doc.get("evidence") or {}), "verdict_json": v_path.resolve().as_uri()}
    if doc.get("slice_id") != sid or (expected_fp and doc.get("input_fingerprint") and doc["input_fingerprint"] != expected_fp):
        return {"slice_id": sid, "status": "BLOCKED", "stage": "gate_runner", "reason": "verdict.json 切片标识或输入指纹不匹配", "next_step": "清理过期输出目录并重跑门禁（不扣返修）", "evidence": ev}
    dst = doc.get("status") or ("PASSED" if doc.get("decision") == "APPROVED" else "BLOCKED" if doc.get("decision") == "BLOCKED" else "FAILED")
    st = "PASSED" if (exit_code == 0 and dst == "PASSED") else ("BLOCKED" if (dst == "BLOCKED" or exit_code == 2) else "FAILED")
    return {"slice_id": sid, "status": st, "stage": doc.get("stage", "gate"), "reason": doc.get("reason", f"门禁结束 (exit={exit_code}, status={dst})"), "next_step": doc.get("next_step", "查阅本次证据文件"), "evidence": ev}


async def _run_and_adjudicate(ws: Path, sid: str, slice_yaml: str, out_rel: str) -> dict:
    """调用 `slice_gate.py` 并处理权限拒绝/异常与真实裁决文件。"""
    cmd = f"python3 project-control/tools/gates/slice_gate.py --workspace . --slice {slice_yaml} --out-dir {out_rel}"
    spec = yaml.safe_load((ws / slice_yaml).read_text(encoding="utf-8"))
    expected_fp = _safe_fingerprint(ws, spec)
    try:
        gate_out = await call_tool("run_command", CommandLine=cmd, WaitMsBeforeAsync=10000, toolSummary=f"Gate {sid}")
        return _adjudicate_verdict_file(ws / out_rel, sid, gate_out, expected_fp)
    except Exception as err:
        msg = str(err)
        if getattr(err, "denied", False) or "permission" in msg.lower() or "denied" in msg.lower():
            return {"slice_id": sid, "status": "BLOCKED", "stage": "gate_permission", "reason": f"门禁执行被权限策略拦截: {msg[:120]}", "next_step": "授予门禁执行权限后重跑巡航（不扣返修）", "evidence": {}}
        if (ws / out_rel / "verdict.json").is_file():
            return _adjudicate_verdict_file(ws / out_rel, sid, f"Command exited with code 1.\n{msg}", expected_fp)
        return {"slice_id": sid, "status": "BLOCKED" if "BLOCKED" in msg.upper() else "FAILED", "stage": "gate_exec", "reason": msg[:160], "next_step": "排查失败原因或环境阻塞后重跑", "evidence": {}}


async def run_single_slice(workspace_str: str, plan_path: str, slice_yaml: str) -> dict:
    """执行单个垂直切片的派单、`PASSED`/`FAILED`/`BLOCKED` 裁决及最多 2 轮零误扣返修。"""
    ws = Path(workspace_str)
    spec = yaml.safe_load((ws / slice_yaml).read_text(encoding="utf-8"))
    sid, contract_ref = spec["slice_id"], spec.get("contract_ref", "project-control/contracts/minimc_v2_contract.yaml")
    workers = {st["role"]: agent(role=f"{sid} {st['role']}", workspace="inherit", schema=subtask_schema()) for st in spec.get("subtasks", [])}
    if workers:
        phase(f"{sid}: 并发子仓实现")
        await parallel(spec["subtasks"], lambda st: workers[st["role"]](build_pointer_prompt(plan_path, slice_yaml, contract_ref, st)))
    remediation_used = 0
    for run_idx in range(1, MAX_REMEDIATION_ROUNDS + 2):
        phase(f"{sid}: 四阶门禁核验 (第 {run_idx} 次)")
        res = await _run_and_adjudicate(ws, sid, slice_yaml, f"project-control/docs/evidence/{sid}/run_{run_idx:02d}")
        log(f"[{sid}] 结果={res['status']} | 原因={res['reason']} | 下一步={res['next_step']} | 证据={res['evidence'].get('verdict_json', '')}")
        if res["status"] == "PASSED":
            return {**res, "remediation_used": remediation_used, "requires_hil": bool(spec.get("requires_hil_immediately"))}
        if res["status"] == "BLOCKED" or not workers or remediation_used >= MAX_REMEDIATION_ROUNDS:
            return {**res, "remediation_used": remediation_used}
        remediation_used += 1
        brief = f"门禁未通过 ({res['stage']}):\n- 原因: {res['reason']}\n- 下一步: {res['next_step']}\n- 证据: {json.dumps(res['evidence'], ensure_ascii=False)}\n请定向修复并提交。"
        await parallel(spec["subtasks"], lambda st, b=brief: workers[st["role"]](b))
    return {"slice_id": sid, "status": "BLOCKED", "reason": "异常退出返修循环", "next_step": "检查巡航脚本", "remediation_used": remediation_used, "evidence": {}}


async def run_batch_cruise(cfg: dict) -> dict:
    """按序巡航批次切片，依据真实裁决推进并输出精简三段汇报。"""
    ws_str = cfg.get("workspace") or (WORKSPACES[0] if "WORKSPACES" in globals() and WORKSPACES else ".")
    ws = Path(ws_str)
    ledger_p = ws / "project-control/slices/ledger.md"
    ledger_text = ledger_p.read_text(encoding="utf-8") if ledger_p.is_file() else ""
    completed: List[str] = []
    last_ev: Dict[str, str] = {}
    for slice_yaml in cfg.get("slice_files", []):
        spec = yaml.safe_load((ws / slice_yaml).read_text(encoding="utf-8"))
        sid = spec["slice_id"]
        if is_slice_verified(ledger_text, sid, _safe_fingerprint(ws, spec)):
            log(f"[SKIP] {sid} 账本输入指纹匹配，幂等跳过。")
            continue
        res = await run_single_slice(ws_str, cfg["plan_path"], slice_yaml)
        last_ev = res.get("evidence", {})
        if res["status"] != "PASSED":
            phase(f"批次停止 ({res['status']}: {sid})")
            return {"status": res["status"], "slice_id": sid, "reason": res["reason"], "next_step": res["next_step"], "remediation_used": res.get("remediation_used", 0), "completed_slices": completed, "evidence": last_ev}
        completed.append(sid)
        if res.get("requires_hil"):
            phase("Human Gate #2 真机 HIL 待审批")
            return {"status": "HIL_REQUIRED", "slice_id": sid, "reason": f"{sid} 已通过 SW-Verified 并触及真机 HIL 红线", "next_step": "停机申请 Human Gate #2 真机穿刺验收", "completed_slices": completed, "evidence": last_ev}
    phase("批次巡航通过")
    return {"status": "PASSED", "reason": "批次全部切片已通过四阶门禁", "next_step": "进入下一阶段或交付汇总", "completed_slices": completed, "evidence": last_ev}


if "WORKSPACES" in globals():
    await run_batch_cruise(args if "args" in globals() else {})
