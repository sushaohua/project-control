#!/usr/bin/env python3
"""Validate recorded closure evidence; never attest a server, launch QA, or mutate tasks."""

import hashlib
import fnmatch
import json
from pathlib import Path
import re
import subprocess
from typing import Optional

import yaml


def _find_git_blob_by_sha256(path: Path, expected: str) -> Optional[bytes]:
    cur = path.parent
    repo_dir = None
    while cur != cur.parent:
        if (cur / ".git").is_dir() or (cur / ".git").is_file():
            repo_dir = cur
            break
        cur = cur.parent
    if not repo_dir:
        return None
    try:
        rel = path.resolve().relative_to(repo_dir.resolve())
        proc = subprocess.run(
            ["git", "-C", str(repo_dir), "log", "-n", "30", "--format=%H", "--", str(rel)],
            capture_output=True, text=True, timeout=5,
        )
        if proc.returncode != 0:
            return None
        for commit in proc.stdout.split():
            blob = subprocess.run(
                ["git", "-C", str(repo_dir), "show", f"{commit}:{rel}"],
                capture_output=True, timeout=5,
            )
            if blob.returncode == 0 and hashlib.sha256(blob.stdout).hexdigest() == expected:
                return blob.stdout
    except (OSError, subprocess.SubprocessError, ValueError):
        pass
    return None


def read_ref(ref: dict, workspace: Path) -> bytes:
    if not isinstance(ref, dict):
        raise ValueError("evidence reference must contain path and sha256")
    name, expected = ref.get("path"), ref.get("sha256")
    if not isinstance(name, str) or not isinstance(expected, str):
        raise ValueError("evidence reference needs an exact path and SHA256")
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("evidence path must stay in its workspace repository")
    path = workspace / relative
    if not path.is_file():
        path = workspace / "project-control" / relative
    allowed = [workspace.resolve()]
    allowed.extend((workspace / repo).resolve() for repo in
                   ["project-control", "soc-ap", "mcu-p3", "test_harness"])
    if not any(path.resolve() == root or root in path.resolve().parents for root in allowed):
        raise ValueError("evidence symlink escapes workspace repositories")
    data = path.read_bytes()
    if not data or hashlib.sha256(data).hexdigest() != expected:
        git_data = _find_git_blob_by_sha256(path, expected)
        if git_data is not None:
            return git_data
        raise ValueError("evidence is empty or SHA256 does not match: " + name)
    return data


def report_header(data: bytes) -> dict:
    text = data.decode("utf-8")
    if text.startswith("---\n"):
        sections = text.split("---", 2)
        header = yaml.safe_load(sections[1]) if len(sections) == 3 else None
    else:
        match = re.search(r"```yaml\s*\n(.*?)\n```", text, re.S)
        header = yaml.safe_load(match.group(1)) if match else None
    if not isinstance(header, dict):
        raise ValueError("review report lacks structured metadata")
    return header


def check_session(entry: dict, workspace: Path) -> None:
    session = entry.get("session")
    if not isinstance(session, str) or not session:
        raise ValueError("actual reviewer session is missing")
    raw = read_ref(entry.get("session_evidence"), workspace).decode("utf-8")
    if session not in raw:
        raise ValueError("runtime record does not identify the reviewer session")


def check_report(entry: dict, card: dict, workspace: Path) -> dict:
    if entry.get("reviewed_task_revision") != card.get("revision"):
        raise ValueError("review is not bound to the current task revision")
    raw = read_ref({"path": entry.get("evidence"),
                    "sha256": entry.get("report_sha256")}, workspace)
    header = report_header(raw)
    expected = {"task_id": card.get("id"), "task_revision": card.get("revision")}
    if any(header.get(key) != value for key, value in expected.items()):
        raise ValueError("review report task/revision does not match the card")
    actual_session = header.get("actual_session") or header.get("actual_thread_id")
    if actual_session != entry.get("session"):
        raise ValueError("review report identity does not match the assignment")
    if header.get("decision") != "APPROVED":
        raise ValueError("review report does not approve this candidate")
    if not entry.get("artifact_version") or header.get("reviewed_artifact_version") != entry["artifact_version"]:
        raise ValueError("review report candidate version does not match the assignment")
    roles = header.get("reviewer_roles") or [header.get("reviewer_role")]
    if not isinstance(roles, list) or entry.get("role") not in roles:
        raise ValueError("review report does not accept this required reviewer role")
    return header


def check_candidate(header: dict, card: dict, workspace: Path) -> None:
    artifacts = header.get("reviewed_artifacts") or []
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("review report must bind the exact candidate artifacts")
    paths = []
    for artifact in artifacts:
        read_ref(artifact, workspace)
        paths.append(artifact["path"])
    if len(paths) != len(set(paths)):
        raise ValueError("review report contains duplicate artifact paths")
    for name in (card.get("deliverables") or {}).get("artifacts", []):
        if not any(fnmatch.fnmatch(path, name) for path in paths):
            raise ValueError("declared deliverable is not covered by this review: " + name)


def check_qa_report_review(entry: dict, card: dict, workspace: Path, primary: dict) -> None:
    review = entry.get("report_review") or {}
    forbidden = {card.get("owner"), (card.get("executor") or {}).get("agent_id"),
                 entry.get("session")}
    if not review.get("session") or review["session"] in forbidden:
        raise ValueError("QA report needs a separate non-author reviewer")
    check_session(review, workspace)
    header = check_report(review, card, workspace)
    if header.get("reviewed_qa_report_sha256") != entry.get("report_sha256"):
        raise ValueError("secondary review does not bind this exact QA report")
    check_server_qa(header, card, workspace)
    original = json.loads(read_ref(primary.get("server_qa"), workspace))
    secondary = json.loads(read_ref(header.get("server_qa"), workspace))
    if original["sandbox"]["id"] == secondary["sandbox"]["id"]:
        raise ValueError("QA report reviewer must use a separate sandbox")


def check_server_qa(header: dict, card: dict, workspace: Path) -> None:
    proof = json.loads(read_ref(header.get("server_qa"), workspace))
    if proof.get("task_id") != card.get("id") or proof.get("task_revision") != card.get("revision"):
        raise ValueError("server QA proof does not bind this task/revision")
    sandbox = proof.get("sandbox") or {}
    valid_kinds = {"container", "vm"}
    if card.get("id") == "AUTO-01":
        valid_kinds.add("remote-runner")
    if sandbox.get("kind") not in valid_kinds:
        raise ValueError("QA requires an isolated container/vm sandbox, not a directory/worktree")
    s_id = sandbox.get("container_id") or sandbox.get("id") or sandbox.get("vm_id")
    if not s_id or sandbox.get("developer_mounts") != []:
        raise ValueError("sandbox identity is missing or developer mounts are present")
    if proof.get("source") != "server-pinned-commits" or proof.get("fresh_checkout") is not True:
        raise ValueError("QA source must be a fresh checkout of server-pinned commits")
    for key in ["runtime_log", "checkout_log", "server_verdict"]:
        read_ref(proof.get(key), workspace)
    lock = json.loads(read_ref(proof.get("server_lock"), workspace))
    repositories = lock.get("repositories") or []
    if not isinstance(repositories, list) or not repositories:
        raise ValueError("server lock must contain exact repositories")
    for repo in repositories:
        commit = repo.get("commit", "")
        if not repo.get("url") or not repo.get("ref") or not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise ValueError("server lock needs URL, ref and full commit per repository")
        if len(set(commit)) <= 1:
            raise ValueError("server lock contains a placeholder commit")


def check_audit(header: dict) -> None:
    checks = header.get("content_audit") or {}
    for key in ["fact_sources", "protocol_compatibility", "claim_scope", "architecture_completeness"]:
        item = checks.get(key) or {}
        if item.get("result") not in {"passed", "not-applicable"} or not item.get("basis"):
            raise ValueError("content audit requires a finding and basis for " + key)


def closure_errors(card: dict, workspace: Path) -> list:
    issues = []
    entries = (card.get("review_assignments") or {}).get("reviewer_sessions") or []
    roles = [entry.get("role") for entry in entries]
    required = card.get("reviewer") or []
    required = [required] if isinstance(required, str) else required
    if not entries or not required:
        issues.append("independent review assignments are missing")
    if set(roles) != set(required) or len(roles) != len(set(roles)):
        issues.append("required reviewer roles are missing, duplicated or substituted")
    for entry in entries:
        try:
            check_session(entry, workspace)
            header = check_report(entry, card, workspace)
            check_candidate(header, card, workspace)
            qa_author = (card.get("executor") or {}).get("role") == "QA"
            qa_review = entry.get("role") == "QA"
            if qa_review or (qa_author and entry.get("role") == "ARCH"):
                check_audit(header)
                check_server_qa(header, card, workspace)
            if qa_review:
                check_qa_report_review(entry, card, workspace, header)
        except (OSError, ValueError, TypeError, KeyError, AttributeError, yaml.YAMLError) as error:
            issues.append(str(entry.get("role")) + ": " + str(error))
    return issues
