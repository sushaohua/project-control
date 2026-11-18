#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V2 独立异构 Codex 只读双轴分级冷审门禁。

调用本机独立 Codex CLI (`--sandbox read-only -m gpt-6-luna --output-schema`)，
执行 `Spec真实性` 与 `嵌入式安全/Diff预算` 双轴审查，强制校验 `BLOCKER/MINOR/NIT` 分级自洽性。
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import subprocess
from typing import List, Optional, Tuple

DEFAULT_CODEX_BIN = Path("/home/sushaohua/.local/bin/codex")
DEFAULT_CODEX_MODEL = "gpt-6-luna"


@dataclass
class CodexVerdict:
    """独立 Codex 双轴分级审查的结构化裁决结果。"""
    session_id: str
    decision: str
    blocker_count: int
    minor_findings: List[dict]
    tokens_used: int
    payload: dict


def v2_audit_schema() -> dict:
    """生成强制约束 Codex 输出双轴三级审查结论的 JSON Schema。"""
    item = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "severity": {"type": "string", "enum": ["BLOCKER", "MINOR", "NIT"]},
            "axis": {"type": "string", "enum": ["spec_realism", "embedded_safety"]},
            "location": {"type": "string"},
            "message": {"type": "string"},
        },
        "required": ["id", "severity", "axis", "location", "message"],
        "additionalProperties": False,
    }
    props = {
        "slice_id": {"type": "string"},
        "decision": {"type": "string", "enum": ["APPROVED", "REJECTED", "BLOCKED"]},
        "axis_spec_realism": {"type": "string"},
        "axis_embedded_safety": {"type": "string"},
        "findings": {"type": "array", "items": item},
    }
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def parse_codex_jsonl(stdout: str) -> Tuple[Optional[str], int]:
    """从 Codex `--json` 事件流中提取真实 `thread_id` 与累计 Token 用量。"""
    session_id: Optional[str] = None
    tokens = 0
    for line in stdout.splitlines():
        try:
            evt = json.loads(line)
        except ValueError:
            continue
        if isinstance(evt, dict) and evt.get("type") == "thread.started":
            session_id = evt.get("thread_id")
        elif isinstance(evt, dict) and evt.get("type") == "turn.completed":
            u = evt.get("usage") or {}
            tokens += int(u.get("input_tokens", 0)) + int(u.get("output_tokens", 0))
    return session_id, tokens


def validate_graded_verdict(payload: dict, expected_slice: str) -> Tuple[int, List[dict]]:
    """校验审查结论与 `BLOCKER/MINOR/NIT` 分级条目的逻辑自洽性，返回 `(阻断数, MINOR列表)`。"""
    if payload.get("slice_id") != expected_slice:
        raise ValueError(f"切片 ID 不匹配: {payload.get('slice_id')} != {expected_slice}")
    decision = payload.get("decision")
    if decision not in ("APPROVED", "REJECTED", "BLOCKED"):
        raise ValueError(f"非法审查决定: {decision}")
    findings = payload.get("findings") or []
    blockers = [f for f in findings if f.get("severity") == "BLOCKER"]
    minors = [f for f in findings if f.get("severity") == "MINOR"]
    if blockers and decision == "APPROVED":
        raise ValueError("存在 BLOCKER 级问题时严禁判定 APPROVED")
    if not blockers and decision == "REJECTED":
        raise ValueError("0 BLOCKER 时严禁以 MINOR/NIT 拒单 REJECTED")
    return len(blockers), minors


def _build_codex_cmd(codex_bin: Path, model: str, workdir: Path, out_dir: Path) -> List[str]:
    """构造带只读沙箱、禁止交互审批与 JSON Schema 约束的 Codex CLI 命令。"""
    return [
        str(codex_bin), "exec", "--skip-git-repo-check", "--sandbox", "read-only",
        "-c", 'approval_policy="never"', "-m", model, "-C", str(workdir.resolve()), "--json",
        "--output-schema", str(out_dir / "schema.json"),
        "--output-last-message", str(out_dir / "final.json"), "-",
    ]


def run_codex_audit(prompt: str, slice_id: str, workdir: Path, out_dir: Path) -> CodexVerdict:
    """启动全新只读独立 Codex 会话执行切片双轴审查并落盘审计物证。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    codex_bin = Path(os.environ.get("CODEX_BIN", str(DEFAULT_CODEX_BIN)))
    model = os.environ.get("CODEX_MODEL", DEFAULT_CODEX_MODEL)
    if not codex_bin.is_file() or not os.access(codex_bin, os.X_OK):
        raise RuntimeError(f"独立 Codex CLI 不可用: {codex_bin}")
    (out_dir / "schema.json").write_text(json.dumps(v2_audit_schema()), encoding="utf-8")
    (out_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    timeout_sec = int(os.environ.get("CODEX_TIMEOUT_SEC", "420"))
    with (out_dir / "codex.jsonl").open("w", encoding="utf-8") as f_out, (out_dir / "codex.stderr").open("w", encoding="utf-8") as f_err:
        proc = subprocess.run(_build_codex_cmd(codex_bin, model, workdir, out_dir), input=prompt, text=True, stdout=f_out, stderr=f_err, timeout=timeout_sec)
    if proc.returncode != 0:
        raise RuntimeError(f"Codex 审阅进程非零退出 ({proc.returncode}): {out_dir}")
    session_id, tokens = parse_codex_jsonl((out_dir / "codex.jsonl").read_text(encoding="utf-8"))
    if not session_id:
        raise RuntimeError("Codex 事件流缺失真实 thread.started 会话标识")
    payload = json.loads((out_dir / "final.json").read_text(encoding="utf-8").strip())
    blocker_cnt, minors = validate_graded_verdict(payload, slice_id)
    return CodexVerdict(session_id, payload["decision"], blocker_cnt, minors, tokens, payload)
