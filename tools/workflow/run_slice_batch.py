#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Antigravity `run_workflow` V2 垂直切片批次自动巡航脚本 (`run_slice_batch.py`)。

承载 Phase 2 有界自动执行：按 `slices/ledger.md` 幂等跳过已 `SW-Verified`/`HIL-Verified` 切片，
使用 `workspace="inherit"` 并发派发跨子仓 `ENG-*` 保活会话（仅传 4 个文件路径指针），
串联 `slice_gate.py` 四阶漏斗并在 `BLOCKER` 时执行最多 2 轮原会话保活返修，超限立即熔断。
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Dict, List

import yaml

MAX_REMEDIATION_ROUNDS = 2
VERIFIED_ROW_RE = re.compile(r"\|\s*(SLICE-[A-Za-z0-9_-]+)\s*\|\s*(SW-Verified|HIL-Verified)\s*\|")


def parse_verified_slices(ledger_text: str) -> List[str]:
    """从 `ledger.md` 文本中解析已完成 `SW-Verified` 或 `HIL-Verified` 的切片 ID 列表。"""
    return [m.group(1) for m in VERIFIED_ROW_RE.finditer(ledger_text or "")]


def subtask_schema() -> dict:
    """构造子任务工程 Agent `finish` 工具强制校验的返回 JSON Schema。"""
    props = {
        "role": {"type": "string"},
        "repo": {"type": "string"},
        "candidate_commit": {"type": "string"},
        "summary": {"type": "string"},
    }
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def build_pointer_prompt(plan_path: str, slice_yaml: str, contract_path: str, subtask: dict) -> str:
    """构造稀疏四文件指针提示词，避免向子 Agent 注入历史对话噪音。"""
    report_ptr = f"project-control/docs/evidence/{Path(slice_yaml).stem}/{subtask['role']}_selfcheck.md"
    return (
        f"角色身份: {subtask['role']} (唯一允许写入仓: {subtask['repo']}, 分支: {subtask['branch']})\n"
        f"1. 获批 SSoT 方案指针: {plan_path}\n"
        f"2. 本切片定义指针: {slice_yaml}\n"
        f"3. 机器协议契约指针: {contract_path}\n"
        f"4. 自检记录输出指针: {report_ptr}\n"
        f"请严守 allowed_paths={subtask['allowed_paths']} 与 diff_budget={subtask.get('diff_budget')}，"
        "完成契约驱动 TDD 实现与本地自检提交，返回 40 位 candidate_commit。"
    )


async def run_single_slice(workspace_str: str, plan_path: str, slice_yaml: str) -> dict:
    """执行单个垂直切片的并发实现、四阶门禁漏斗与最多 2 轮原会话保活返修。"""
    ws = Path(workspace_str)
    spec = yaml.safe_load((ws / slice_yaml).read_text(encoding="utf-8"))
    sid = spec["slice_id"]
    contract_ref = spec.get("contract_ref", "project-control/contracts/minimc_v2_contract.yaml")
    phase(f"{sid}: 并发子仓实现")
    workers: Dict[str, object] = {}
    for st in spec["subtasks"]:
        workers[st["role"]] = agent(role=f"{sid} {st['role']}", workspace="inherit", schema=subtask_schema())
    await parallel(
        spec["subtasks"],
        lambda st: workers[st["role"]](build_pointer_prompt(plan_path, slice_yaml, contract_ref, st)),
    )
    # 顺序冲击四阶漏斗，若遇门禁拦截或 Codex BLOCKER 则唤醒原会话修复（上限 2 轮）
    for attempt in range(MAX_REMEDIATION_ROUNDS + 1):
        phase(f"{sid}: 四阶门禁核验 (第 {attempt + 1} 次)")
        out_dir = f"project-control/docs/evidence/{sid}/run_{attempt + 1:02d}"
        cmd = f"python3 project-control/tools/gates/slice_gate.py --workspace . --slice {slice_yaml} --out-dir {out_dir}"
        try:
            gate_out = await call_tool("run_command", CommandLine=cmd, WaitMsBeforeAsync=10000, toolSummary=f"Gate {sid}")
            log(f"[{sid}] 门禁全绿 SW-Verified: {gate_out[:160]}")
            return {"slice_id": sid, "status": "SW-Verified", "requires_hil": bool(spec.get("requires_hil_immediately"))}
        except Exception as err:
            log(f"[{sid}] 第 {attempt + 1} 次门禁未通过: {err}")
            if attempt >= MAX_REMEDIATION_ROUNDS:
                raise RuntimeError(f"[{sid}] 连续 {MAX_REMEDIATION_ROUNDS} 轮返修未决，触发 Fail-Fast 熔断升级人工！") from err
            await parallel(
                spec["subtasks"],
                lambda st, e=str(err): workers[st["role"]](f"门禁/Codex BLOCKER 退修日志:\n{e}\n请定向修复并产生新提交。"),
            )
    raise RuntimeError(f"[{sid}] 异常退出循环")


async def run_batch_cruise(cfg: dict) -> dict:
    """按序巡航批次内全部垂直切片，支持幂等断点跳过与 HIL 红线停机。"""
    ws_str = cfg.get("workspace") or (WORKSPACES[0] if "WORKSPACES" in globals() and WORKSPACES else ".")
    ledger_p = Path(ws_str) / "project-control/slices/ledger.md"
    done_ids = set(parse_verified_slices(ledger_p.read_text(encoding="utf-8") if ledger_p.is_file() else ""))
    completed: List[str] = []
    for slice_yaml in cfg.get("slice_files", []):
        spec = yaml.safe_load((Path(ws_str) / slice_yaml).read_text(encoding="utf-8"))
        if spec["slice_id"] in done_ids:
            log(f"[SKIP] {spec['slice_id']} 已在 ledger.md 登记准出，幂等跳过。")
            continue
        res = await run_single_slice(ws_str, cfg["plan_path"], slice_yaml)
        completed.append(res["slice_id"])
        if res["requires_hil"]:
            log(f"[HIL-GATE] {res['slice_id']} 涉及底层硬件/升级链路，停机请求 Human Gate #2 真机穿刺！")
            break
    phase("批次巡航完成 (等待 Human Gate #2 真机 HIL / 发布授权)")
    return {"completed_slices": completed, "next_gate": "HUMAN_GATE_2_HIL_AND_PUBLISH"}


if "WORKSPACES" in globals():
    await run_batch_cruise(args if "args" in globals() else {})
