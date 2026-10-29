#!/usr/bin/env python3
"""State machine and gate enforcement for COORD delivery tasks."""

from pathlib import Path
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
        evidence: Optional[dict] = None,
    ) -> None:
        if evidence is not None:
            if not isinstance(evidence, dict) or not evidence.get("path") or not evidence.get("sha256"):
                raise GateValidationError("Remediation evidence requires non-empty path and sha256")
        record.corrections_count += 1
        if record.corrections_count > self.max_corrections:
            record.state = TaskState.ESCALATED.value
            raise RemediationLimitExceededError(
                f"Task {record.task_id} exceeded max corrections ({self.max_corrections}): {reason}"
            )
        record.state = TaskState.IN_PROGRESS.value
        ev_tag = f":evidence={evidence.get('sha256')[:8]}" if evidence else ""
        record.waiting_events.append(f"remediation:{record.corrections_count}:{reason}{ev_tag}")

    def validate_qa_verdict(self, record: TaskExecutionRecord, qa_verdict: dict) -> bool:
        if not isinstance(qa_verdict, dict):
            self.handle_remediation(record, "QA verdict must be a valid dictionary")
            return False
        passed = qa_verdict.get("passed")
        if passed is not True:
            err = qa_verdict.get("summary", "QA verification failed or passed not boolean True")
            self.handle_remediation(record, f"Server QA failure: {err}")
            return False
        mounts = qa_verdict.get("developer_mounts", [])
        if mounts:
            self.handle_remediation(record, "Sandbox security violation: developer mounts present")
            return False
        server_qa = qa_verdict.get("server_qa")
        if server_qa and isinstance(server_qa, dict):
            sbox = server_qa.get("sandbox", {})
            if sbox.get("kind") not in {"container", "vm"}:
                self.handle_remediation(record, f"Invalid sandbox kind: {sbox.get('kind')}")
                return False
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
            self.handle_remediation(record, f"Review rejected: decision was {decision}")
            return False
        return True

    def validate_done_acceptance(self, card: dict, workspace: Path) -> None:
        assignments = (card.get("review_assignments") or {}).get("reviewer_sessions") or []
        if not assignments:
            raise GateValidationError("Fake Done rejected: missing review assignments")
        for entry in assignments:
            if entry.get("decision") != "APPROVED":
                raise GateValidationError("Fake Done rejected: review assignments not approved")
