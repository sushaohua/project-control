#!/usr/bin/env python3
"""Data models for COORD runner, state machine, and scheduling."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import time
from typing import Dict, List, Optional


class TaskState(str, Enum):
    """Task lifecycle states in COORD delivery gate."""
    BACKLOG = "Backlog"
    READY = "Ready"
    IN_PROGRESS = "InProgress"
    CANDIDATE_PUSHED = "CandidatePushed"
    SANDBOX_QA = "SandboxQA"
    REVIEW = "Review"
    DONE = "Done"
    ESCALATED = "Escalated"
    BLOCKED = "Blocked"
    FAILED = "Failed"


@dataclass
class Lease:
    """Exclusive or shared resource lease held by an agent/task."""
    lease_id: str
    task_id: str
    resource: str
    owner: str
    acquired_at: float
    expires_at: float
    active: bool = True

    def is_expired(self, current_time: Optional[float] = None) -> bool:
        """Check if lease has expired."""
        now = time.time() if current_time is None else current_time
        return self.active and now >= self.expires_at

    def to_dict(self) -> dict:
        """Serialize lease to dictionary."""
        return {
            "lease_id": self.lease_id,
            "task_id": self.task_id,
            "resource": self.resource,
            "owner": self.owner,
            "acquired_at": self.acquired_at,
            "expires_at": self.expires_at,
            "active": self.active,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Lease":
        """Deserialize lease from dictionary."""
        return cls(
            lease_id=data["lease_id"],
            task_id=data["task_id"],
            resource=data["resource"],
            owner=data["owner"],
            acquired_at=float(data["acquired_at"]),
            expires_at=float(data["expires_at"]),
            active=bool(data.get("active", True)),
        )


@dataclass
class TaskExecutionRecord:
    """Execution context for an active or recorded task."""
    task_id: str
    state: str = TaskState.BACKLOG.value
    session_id: Optional[str] = None
    candidate_commit: Optional[str] = None
    task_revision: int = 1
    corrections_count: int = 0
    waiting_events: List[str] = field(default_factory=list)
    leases: List[str] = field(default_factory=list)
    updated_at: float = field(default_factory=time.time)
    runtime_context: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize task record to dictionary."""
        return {
            "task_id": self.task_id,
            "state": self.state,
            "session_id": self.session_id,
            "candidate_commit": self.candidate_commit,
            "task_revision": self.task_revision,
            "corrections_count": self.corrections_count,
            "waiting_events": list(self.waiting_events),
            "leases": list(self.leases),
            "updated_at": self.updated_at,
            "runtime_context": dict(self.runtime_context),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TaskExecutionRecord":
        """Deserialize task record from dictionary."""
        return cls(
            task_id=data["task_id"],
            state=data.get("state", TaskState.BACKLOG.value),
            session_id=data.get("session_id"),
            candidate_commit=data.get("candidate_commit"),
            task_revision=int(data.get("task_revision", 1)),
            corrections_count=int(data.get("corrections_count", 0)),
            waiting_events=list(data.get("waiting_events", [])),
            leases=list(data.get("leases", [])),
            updated_at=float(data.get("updated_at", time.time())),
            runtime_context=dict(data.get("runtime_context", {})),
        )


@dataclass
class CoordState:
    """Persistent snapshot of the runner execution context."""
    schema_version: int = 1
    cursor: Optional[str] = None
    in_flight_tasks: Dict[str, TaskExecutionRecord] = field(default_factory=dict)
    completed_tasks: List[str] = field(default_factory=list)
    leases: List[Lease] = field(default_factory=list)
    last_updated: str = ""

    def to_dict(self) -> dict:
        """Serialize coordinate state to dictionary."""
        return {
            "schema_version": self.schema_version,
            "cursor": self.cursor,
            "in_flight_tasks": {k: v.to_dict() for k, v in self.in_flight_tasks.items()},
            "completed_tasks": list(self.completed_tasks),
            "leases": [lease.to_dict() for lease in self.leases],
            "last_updated": self.last_updated,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CoordState":
        """Deserialize coordinate state from dictionary."""
        in_flight = {k: TaskExecutionRecord.from_dict(v) for k, v in data.get("in_flight_tasks", {}).items()}
        leases = [Lease.from_dict(item) for item in data.get("leases", [])]
        return cls(
            schema_version=int(data.get("schema_version", 1)),
            cursor=data.get("cursor"),
            in_flight_tasks=in_flight,
            completed_tasks=list(data.get("completed_tasks", [])),
            leases=leases,
            last_updated=str(data.get("last_updated", "")),
        )


def resolve_state_db_path(ws_root: Path, explicit: Optional[Path]) -> Path:
    """Resolve state DB path to shared host location or isolate in test workspace."""
    if explicit is not None:
        return Path(explicit).resolve()
    ws = Path(ws_root).resolve()
    if ws == Path(".").resolve() or ws.name in {"ai_soc_project", "project-control"}:
        return Path("/home/sushaohua/.local/share/ai_soc_coord_runner/state.sqlite3")
    return (ws / "state.sqlite3").resolve()


def resolve_lock_path(ws_root: Path, explicit: Optional[Path]) -> Path:
    """Resolve process lock path to shared host location or isolate in test workspace."""
    if explicit is not None:
        return Path(explicit).resolve()
    ws = Path(ws_root).resolve()
    if ws == Path(".").resolve() or ws.name in {"ai_soc_project", "project-control"}:
        return Path("/home/sushaohua/.local/share/ai_soc_coord_runner/coord_runner.lock")
    return (ws / "coord_runner.lock").resolve()


@dataclass
class CoordRunnerConfig:
    """Configuration settings for COORD runner."""
    workspace_root: Path = field(default_factory=lambda: Path("."))
    queue_file: Path = field(default_factory=lambda: Path("project-control/docs/work_intake/work_intake_queue.yaml"))
    checkpoint_file: Path = field(default_factory=lambda: Path("project-control/tools/coord_runner/coord_state.json"))
    poll_interval_seconds: float = 5.0
    default_lease_duration_seconds: float = 1800.0
    max_parallel_implementation: int = 2
    max_evidence_based_corrections: int = 2
    exclusive_devices: List[str] = field(default_factory=lambda: ["uart", "hardware-serial", "hil-device", "probe"])
    intake_root: Path = field(default_factory=lambda: Path("project-control/docs/work_intake"))
    legacy_queue_file: Path = field(default_factory=lambda: Path("project-control/docs/planning/coord_autorun_queue_20261029.yaml"))
    isolate_legacy_queue: bool = False
    codex_bin: Path = field(default_factory=lambda: Path("/home/sushaohua/.local/bin/codex"))
    default_model: str = "gpt-6-luna"
    jobs_dir: Path = field(default_factory=lambda: Path("project-control/tools/coord_runner/runtime_jobs"))
    state_db_file: Optional[Path] = None
    lock_file: Optional[Path] = None

    @classmethod
    def from_dict(cls, data: dict, base_dir: Optional[Path] = None) -> "CoordRunnerConfig":
        """Create config from dictionary and optional base directory."""
        base = base_dir or Path(".")
        runner_sec = data.get("runner", {})
        limits_sec = data.get("limits", {})
        res_sec = data.get("resources", {})
        intake_sec = data.get("work_intake", {})
        ws = (base / runner_sec.get("workspace_root", ".")).resolve()
        qf = (base / runner_sec.get("queue_file", "project-control/docs/work_intake/work_intake_queue.yaml")).resolve()
        cf = (base / runner_sec.get("checkpoint_file", "project-control/tools/coord_runner/coord_state.json")).resolve()
        devs = res_sec.get("exclusive_devices", ["uart", "hardware-serial", "hil-device", "probe"])
        in_root = (base / intake_sec.get("root_dir", "project-control/docs/work_intake")).resolve()
        leg_q = (base / intake_sec.get("legacy_queue_file", "project-control/docs/planning/coord_autorun_queue_20261029.yaml")).resolve()
        j_dir = (base / intake_sec.get("jobs_dir", "project-control/tools/coord_runner/runtime_jobs")).resolve()
        s_db = Path(runner_sec["state_db_file"]) if "state_db_file" in runner_sec else None
        l_file = Path(runner_sec["lock_file"]) if "lock_file" in runner_sec else None
        return cls(
            workspace_root=ws, queue_file=qf, checkpoint_file=cf,
            poll_interval_seconds=float(runner_sec.get("poll_interval_seconds", 5.0)),
            default_lease_duration_seconds=float(runner_sec.get("default_lease_duration_seconds", 1800.0)),
            max_parallel_implementation=int(limits_sec.get("max_parallel_implementation", 2)),
            max_evidence_based_corrections=int(limits_sec.get("max_evidence_based_corrections", 2)),
            exclusive_devices=list(devs), intake_root=in_root, legacy_queue_file=leg_q,
            isolate_legacy_queue=bool(intake_sec.get("isolate_legacy_queue", True)),
            codex_bin=Path(intake_sec.get("codex_bin", "/home/sushaohua/.local/bin/codex")),
            default_model=str(intake_sec.get("default_model", "gpt-6-luna")),
            jobs_dir=j_dir, state_db_file=s_db, lock_file=l_file,
        )
