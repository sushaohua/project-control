#!/usr/bin/env python3
"""State machine and gate enforcement for COORD delivery tasks."""

from pathlib import Path
import hashlib
import json
import re
from typing import Dict, Optional, Set

from .errors import (
    DependencyUnmetError,
    GateValidationError,
    RemediationLimitExceededError,
    StateTransitionError,
)
from .models import TaskExecutionRecord, TaskState

HEX40_RE = re.compile(r"^[0-9a-f]{40}$")


class CoordStateMachine:
    """Manages task state transitions, remediation limits, and gate checks."""

    ALLOWED_TRANSITIONS = {
        TaskState.BACKLOG: {TaskState.READY, TaskState.BLOCKED},
        TaskState.READY: {TaskState.IN_PROGRESS, TaskState.BLOCKED},
        TaskState.IN_PROGRESS: {TaskState.CANDIDATE_PUSHED, TaskState.ESCALATED, TaskState.BLOCKED},
        TaskState.CANDIDATE_PUSHED: {TaskState.SANDBOX_QA, TaskState.IN_PROGRESS, TaskState.ESCALATED},
        TaskState.SANDBOX_QA: {TaskState.REVIEW, TaskState.IN_PROGRESS, TaskState.ESCALATED},
        TaskState.REVIEW: {TaskState.DONE, TaskState.IN_PROGRESS, TaskState.ESCALATED},
        TaskState.DONE: set(),
        TaskState.ESCALATED: set(),
        TaskState.BLOCKED: {TaskState.READY, TaskState.BACKLOG},
        TaskState.FAILED: set(),
    }

    def __init__(self, max_corrections: int = 2):
        self.max_corrections = max_corrections

    def check_transition_allowed(self, current: TaskState, target: TaskState) -> None:
        allowed = self.ALLOWED_TRANSITIONS.get(current, set())
        if target not in allowed:
            raise StateTransitionError(
                f"Illegal state transition from {current.value} to {target.value}"
            )

    def transition(self, record: TaskExecutionRecord, target: TaskState) -> None:
        cur_state = TaskState(record.state)
        self.check_transition_allowed(cur_state, target)
        record.state = target.value

    def validate_ready(self, card: dict, completed_tasks: Set[str]) -> None:
        if card.get("blocked"):
            raise GateValidationError(f"Task {card.get('id')} is marked as blocked")
        deps = card.get("depends_on", [])
        missing = [d for d in deps if d not in completed_tasks]
        if missing:
            raise DependencyUnmetError(
                f"Task {card.get('id')} has unmet dependencies: {', '.join(missing)}"
            )

    def validate_commit_sha(self, commit: Optional[str]) -> None:
        if not commit or not isinstance(commit, str) or not HEX40_RE.match(commit):
            raise GateValidationError(f"Candidate commit must be full 40-char hex SHA, got: {commit}")
        if len(set(commit)) <= 1:
            raise GateValidationError(f"Placeholder commit SHA rejected: {commit}")

    def handle_remediation(
        self,
        record: TaskExecutionRecord,
        reason: str,
        evidence: dict,
    ) -> None:
        if not evidence or not isinstance(evidence, dict) or not evidence.get("path") or not evidence.get("sha256"):
            raise GateValidationError("Remediation requires mandatory evidence dict with non-empty path and sha256")
        record.corrections_count += 1
        if record.corrections_count > self.max_corrections:
            record.state = TaskState.ESCALATED.value
            raise RemediationLimitExceededError(
                f"Task {record.task_id} exceeded max corrections ({self.max_corrections}): {reason}"
            )
        record.state = TaskState.IN_PROGRESS.value
        ev_tag = f":evidence={evidence.get('sha256')[:8]}"
        record.waiting_events.append(f"remediation:{record.corrections_count}:{reason}{ev_tag}")

    def _find_or_create_evidence(self, candidates: list, fallback_name: str, raw_bytes: bytes) -> dict:
        for c in candidates:
            if c:
                p = Path(c)
                if p.is_file():
                    try:
                        data = p.read_bytes()
                        return {"path": str(p), "sha256": hashlib.sha256(data).hexdigest()}
                    except OSError:
                        pass
        out = Path("/tmp") / fallback_name
        out.write_bytes(raw_bytes)
        return {"path": str(out), "sha256": hashlib.sha256(raw_bytes).hexdigest()}

    def _extract_qa_failure_evidence(self, qa_verdict: object) -> dict:
        candidates = ["server_qa.json", "runtime.log", "server_verdict.json"]
        if isinstance(qa_verdict, dict):
            ev = qa_verdict.get("evidence")
            if isinstance(ev, dict) and ev.get("path") and ev.get("sha256"):
                return ev
            sqa = qa_verdict.get("server_qa")
            if isinstance(sqa, dict) and sqa.get("path"):
                candidates.insert(0, sqa["path"])
            raw = json.dumps(qa_verdict, sort_keys=True).encode("utf-8")
        else:
            raw = str(qa_verdict).encode("utf-8")
        return self._find_or_create_evidence(candidates, "qa_failure_verdict.json", raw)

    def _extract_review_failure_evidence(self, review_entry: object) -> dict:
        candidates = ["review_report.md", "server_qa.json", "runtime.log"]
        if isinstance(review_entry, dict):
            ev = review_entry.get("evidence")
            if isinstance(ev, dict) and ev.get("path") and ev.get("sha256"):
                return ev
            rep = review_entry.get("report_ref")
            if isinstance(rep, dict) and rep.get("path"):
                candidates.insert(0, rep["path"])
            raw = json.dumps(review_entry, sort_keys=True).encode("utf-8")
        else:
            raw = str(review_entry).encode("utf-8")
        return self._find_or_create_evidence(candidates, "review_failure_report.md", raw)

    def _validate_server_qa_proof(self, server_qa: object, record: TaskExecutionRecord) -> None:
        if not server_qa or not isinstance(server_qa, dict):
            raise GateValidationError("Missing mandatory server_qa evidence dictionary in QA verdict")
        if not server_qa.get("path") or not server_qa.get("sha256"):
            raise GateValidationError("server_qa evidence reference requires non-empty path and sha256")
        sbox = server_qa.get("sandbox", {})
        if sbox.get("kind") not in {"container", "vm"}:
            raise GateValidationError(f"Invalid sandbox kind in server_qa: {sbox.get('kind')}")
        qa_rev = server_qa.get("task_revision")
        if qa_rev is None or qa_rev != record.task_revision:
            raise GateValidationError(
                f"Task revision mismatch in server QA evidence: expected {record.task_revision}, got {qa_rev}"
            )

    def validate_qa_verdict(self, record: TaskExecutionRecord, qa_verdict: dict) -> bool:
        if not isinstance(qa_verdict, dict):
            ev = self._extract_qa_failure_evidence(qa_verdict)
            self.handle_remediation(record, "QA verdict must be a valid dictionary", ev)
            return False
        passed = qa_verdict.get("passed")
        if passed is not True:
            err = qa_verdict.get("summary", "QA verification failed or passed not boolean True")
            ev = self._extract_qa_failure_evidence(qa_verdict)
            self.handle_remediation(record, f"Server QA failure: {err}", ev)
            return False
        if qa_verdict.get("developer_mounts"):
            ev = self._extract_qa_failure_evidence(qa_verdict)
            self.handle_remediation(record, "Sandbox security violation: developer mounts present", ev)
            return False
        v_commit = qa_verdict.get("candidate_commit") or qa_verdict.get("commit_sha")
        if not v_commit or v_commit != record.candidate_commit:
            raise GateValidationError(
                f"QA verdict commit ({v_commit}) does not match candidate commit ({record.candidate_commit})"
            )
        self._validate_server_qa_proof(qa_verdict.get("server_qa"), record)
        return True

    def validate_review_verdict(
        self,
        record: TaskExecutionRecord,
        review_entry: dict,
        author_session: str,
    ) -> bool:
        reviewer_session = review_entry.get("session") or review_entry.get("reviewer_session")
        if not reviewer_session:
            raise GateValidationError("Reviewer session ID is missing")
        if author_session and reviewer_session == author_session:
            raise GateValidationError(
                f"Self-review rejected: author session {author_session} cannot review own work"
            )
        decision = review_entry.get("decision", "").upper()
        if decision != "APPROVED":
            ev = self._extract_review_failure_evidence(review_entry)
            self.handle_remediation(record, f"Review rejected: decision was {decision}", ev)
            return False
        return True

    def _validate_qa_report_review(
        self,
        entry: dict,
        author: Optional[str],
        workspace: Path,
    ) -> None:
        rep_rev = entry.get("report_review")
        if not rep_rev or not isinstance(rep_rev, dict):
            raise GateValidationError("Fake Done rejected: QA reviewer missing mandatory non-author report_review")
        if rep_rev.get("decision") != "APPROVED":
            raise GateValidationError(
                "Fake Done rejected: QA reviewer missing mandatory non-author report_review (QA report review not approved)"
            )
        qa_rev = entry.get("reviewer") or entry.get("session") or entry.get("reviewer_session")
        rep_rev_id = rep_rev.get("reviewer") or rep_rev.get("session") or rep_rev.get("reviewer_session")
        if not rep_rev_id or rep_rev_id == qa_rev or (author and rep_rev_id == author):
            raise GateValidationError("Fake Done rejected: QA reviewer missing mandatory non-author report_review")
        r_path = rep_rev.get("report_path")
        r_sha = rep_rev.get("report_sha256")
        if not r_path or not isinstance(r_path, str) or not r_sha or not isinstance(r_sha, str):
            raise GateValidationError(
                "Fake Done rejected: QA report_review missing mandatory report_path or report_sha256 binding"
            )
        p = Path(r_path) if Path(r_path).is_absolute() else (workspace / r_path)
        if not p.is_file():
            raise GateValidationError(f"Fake Done rejected: QA report file not found on disk at {r_path}")
        real_sha = hashlib.sha256(p.read_bytes()).hexdigest()
        if r_sha != real_sha:
            raise GateValidationError("Fake Done rejected: report_review sha256 does not match physical file content")
        entry_sha = entry.get("report_sha256")
        if not entry_sha or entry_sha != real_sha:
            raise GateValidationError("Fake Done rejected: QA entry report_sha256 missing or does not match physical file content")

    def validate_done_acceptance(self, card: dict, workspace: Path) -> None:
        assignments = (card.get("review_assignments") or {}).get("reviewer_sessions") or []
        if not assignments:
            raise GateValidationError("Fake Done rejected: missing review assignments")
        req_raw = card.get("reviewer") or []
        required_roles = [req_raw] if isinstance(req_raw, str) else list(req_raw)
        approved_roles = set()
        for entry in assignments:
            if entry.get("decision") != "APPROVED":
                raise GateValidationError("Fake Done rejected: review assignments not approved")
            role = entry.get("role")
            if role:
                approved_roles.add(role)
        for r in required_roles:
            if r not in approved_roles:
                raise GateValidationError(f"Fake Done rejected: required reviewer role {r} missing or not approved")
        author = card.get("session_id") or card.get("author_session") or card.get("owner")
        for entry in assignments:
            if entry.get("role") == "QA" and "QA" in required_roles:
                self._validate_qa_report_review(entry, author, workspace)
