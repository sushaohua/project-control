#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V2 垂直切片四阶无状态门禁漏斗 (`slice_gate.py`)。

顺序串联：`fast_gate` (`<3s`) ➔ 零篡改跨仓合龙 ➔ `qa_runner` Docker 干净构建回归 ➔ 异构 Codex 双轴冷审。
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Dict, List, Optional, Tuple

import yaml

TOOLS_ROOT = Path(__file__).resolve().parents[1]
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from gates import codex_review, fast_gate


def load_slice_spec(slice_path: Path) -> dict:
    """加载并校验垂直切片 YAML 配置必填字段。"""
    spec = yaml.safe_load(slice_path.read_text(encoding="utf-8"))
    for key in ("slice_id", "batch_id", "subtasks", "integration_cmd"):
        if key not in spec:
            raise ValueError(f"切片定义 {slice_path} 缺失必填字段: {key}")
    return spec


def _run_shell_step(cmd: str, cwd: Path, timeout_sec: int = 180) -> Tuple[int, str]:
    """在指定目录执行受超时保护的子进程命令并返回 `(退出码, 合并输出)`。"""
    proc = subprocess.run(["bash", "-lc", cmd], cwd=str(cwd), text=True, capture_output=True, timeout=timeout_sec)
    out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    return proc.returncode, out.strip()


def _collect_locked_commits(workspace: Path, subtasks: List[dict]) -> Dict[str, str]:
    """读取切片涉及各子仓当前的完整 40 位 HEAD Commit SHA。"""
    return {
        st["repo"]: subprocess.check_output(["git", "-C", str(workspace / st["repo"]), "rev-parse", "HEAD"], text=True).strip()
        for st in subtasks
    }


def _run_docker_qa(workspace: Path, spec: dict, commits: Dict[str, str], out_dir: Path) -> dict:
    """调用 `qa_runner.py` 执行隔离容器干净构建测试并核验 `server_qa.json` 证据。"""
    qa_dir = out_dir / "docker_qa"
    qa_dir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(workspace / "project-control/tools/qa_runner/qa_runner.py"), "--task-id", spec["slice_id"], "--task-revision", "1", "--output-dir", str(qa_dir)]
    for repo_rel, sha in commits.items():
        branch = next(s["branch"] for s in spec["subtasks"] if s["repo"] == repo_rel)
        cmd.extend(["--repo", f"{repo_rel}={sha}:refs/heads/{branch}"])
    for qc in spec.get("qa_commands", []):
        cmd.extend(["--cmd", f"{qc['subpath']}:{qc['kind']}:{qc['command']}"])
    proc = subprocess.run(cmd, cwd=str(workspace), text=True, capture_output=True, timeout=600)
    proof_path = qa_dir / "evidence/server_qa.json"
    if proc.returncode != 0 or not proof_path.is_file():
        raise RuntimeError(f"Docker QA 沙箱未通过 (rc={proc.returncode}): {proc.stderr or proc.stdout}")
    proof = json.loads(proof_path.read_text(encoding="utf-8"))
    if proof.get("passed") is not True:
        raise RuntimeError("server_qa.json 记录沙箱结果为未通过")
    return proof


def _build_review_prompt(spec: dict, commits: Dict[str, str], qa_proof: dict) -> str:
    """构造仅含精确元数据、验收条款与客观沙箱摘要的双轴冷审提示词。"""
    criteria = "\n".join(f"- {item}" for item in spec.get("acceptance_criteria", []))
    return (
        f"独立只读双轴冷审切片: {spec['slice_id']}\n契约: {spec.get('contract_ref')}\n方案: {spec.get('plan_ref')}\n"
        f"锁定提交: {json.dumps(commits, ensure_ascii=False)}\n容器: {qa_proof.get('sandbox', {}).get('container_id', 'ok')}\n"
        f"验收判据:\n{criteria}\n请严格按 BLOCKER / MINOR / NIT 分级。"
    )


def append_ledger_entry(ledger_path: Path, entry: dict) -> None:
    """将通过四阶漏斗的切片记录与 `MINOR` 技术债幂等追加写入 `slices/ledger.md`。"""
    text = ledger_path.read_text(encoding="utf-8") if ledger_path.is_file() else ""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = f"| {now} | {entry['batch_id']} | {entry['slice_id']} | {entry['status']} | `{entry['commits_short']}` | `{entry['container_id']}` | `{entry['codex_session']}` | `{entry['verdict_sha256'][:16]}` |\n"
    marker = "## 2. 非阻断技术债登记表"
    if f"| {entry['slice_id']} | {entry['status']} |" not in text:
        text = text.replace(marker, row + "\n" + marker, 1) if marker in text else text + "\n" + row
    for item in entry.get("minors", []):
        debt = f"| {now} | {entry['slice_id']} | `{item['axis']}` | `{item['location']}` | {item['message']} |\n"
        if debt not in text:
            text += debt
    ledger_path.write_text(text, encoding="utf-8")


def execute_slice_funnel(workspace: Path, slice_path: Path, out_dir: Path, fast_only: bool = False) -> dict:
    """顺序执行垂直切片四阶门禁漏斗并生成带 SHA256 的 `verdict.json`。"""
    spec = load_slice_spec(slice_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    ok_fast, fast_errs = fast_gate.run_fast_gate(workspace, slice_path=slice_path)
    if not ok_fast:
        return {"stage": "fast_gate", "passed": False, "errors": fast_errs}
    rc_int, int_log = _run_shell_step(spec["integration_cmd"], workspace)
    if rc_int != 0 or fast_only:
        return {"stage": "integration", "passed": rc_int == 0, "errors": [] if rc_int == 0 else [int_log]}
    commits = _collect_locked_commits(workspace, spec["subtasks"])
    qa_proof = _run_docker_qa(workspace, spec, commits, out_dir)
    verdict = codex_review.run_codex_audit(_build_review_prompt(spec, commits, qa_proof), spec["slice_id"], workspace, out_dir / "codex")
    doc = {"slice_id": spec["slice_id"], "batch_id": spec["batch_id"], "commits": commits, "decision": verdict.decision, "codex_session": verdict.session_id, "blocker_count": verdict.blocker_count, "findings": verdict.payload["findings"]}
    raw = json.dumps(doc, indent=2, ensure_ascii=False).encode("utf-8")
    v_sha = hashlib.sha256(raw).hexdigest()
    (out_dir / "verdict.json").write_bytes(raw)
    if verdict.decision == "APPROVED":
        append_ledger_entry(workspace / "project-control/slices/ledger.md", {"batch_id": spec["batch_id"], "slice_id": spec["slice_id"], "status": "SW-Verified", "commits_short": ",".join(f"{k}:{v[:7]}" for k, v in commits.items()), "container_id": qa_proof.get("sandbox", {}).get("container_id", "n/a")[:12], "codex_session": verdict.session_id, "verdict_sha256": v_sha, "minors": verdict.minor_findings})
    return {"stage": "codex", "passed": verdict.decision == "APPROVED", "verdict_sha256": v_sha, "verdict": doc}


def main(argv: Optional[List[str]] = None) -> int:
    """命令行入口：执行指定 `SLICE-XX.yaml` 的四阶门禁或前置快检合龙。"""
    parser = argparse.ArgumentParser(description="AI SoC V2 垂直切片四阶无状态门禁")
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--slice", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--fast-only", action="store_true")
    ns = parser.parse_args(argv)
    res = execute_slice_funnel(ns.workspace, ns.slice, ns.out_dir, ns.fast_only)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res.get("passed") else 1


if __name__ == "__main__":
    sys.exit(main())
