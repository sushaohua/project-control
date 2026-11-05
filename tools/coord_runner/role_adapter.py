#!/usr/bin/env python3
"""宿主机 CLI 角色适配器：封装 `/home/sushaohua/.local/bin/codex exec -m gpt-6-luna` 异步调用与只读/写入边界校验（设计规范 §6）。"""

from dataclasses import dataclass, field
import datetime
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import uuid
from typing import Dict, List, Optional, Tuple

from .approval_guard import ApprovalCheckResult
from .cas_writer import compute_bytes_sha256
from .errors import (
    ApprovalValidationError,
    BoundaryViolationError,
    CoordRunnerError,
    GateValidationError,
)
from .job_launcher import JobLauncher

DEFAULT_CODEX_BIN = Path("/home/sushaohua/.local/bin/codex")
DEFAULT_MODEL = "gpt-6-luna"
HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
READ_ONLY_ROLES = {"COORD", "PM", "ARCH", "QA"}
WRITE_CAPABLE_ROLES = {
    "INTEGRATOR", "ENG-FWD", "ENG-MC", "ENG-TH", "ENG_BOOT_MC", "ENG_BOOT_TH",
    "ENG-BSP", "ENG-JOB", "ENG-STATE", "ENG-UI", "ENG-NET", "ENG-MEDIA",
    "ENG-DDS", "ENG-DBUS", "ENG-MQTT", "ENG-SIM", "ENG-COLOR",
}
VALID_COORD_ACTIONS = {
    "NOOP", "CLARIFY_PM_ARCH", "INVESTIGATE_ISSUE", "DISPATCH_OWNER",
    "SPLIT_MULTI_ROLE", "HOLD_PENDING_APPROVAL", "ADVANCE_QA",
}
PHASE1_LOCKED_PREFIXES = (
    "soc-ap/", "mcu-p3/", "test_harness/", "boot/bootloadermc/", "boot/bootloaderth/",
)


@dataclass
class RoleAdapterConfig:
    """Runtime configuration for host Codex CLI execution and job persistence."""
    workspace_root: Path = field(default_factory=lambda: Path("."))
    jobs_dir: Optional[Path] = None
    codex_bin: Path = DEFAULT_CODEX_BIN
    default_model: str = DEFAULT_MODEL
    codex_home: Path = field(default_factory=lambda: Path.home() / ".codex")
    timeout_seconds: int = 240
    require_remote_push: bool = True
    enforce_phase1_repo_lock: bool = True


@dataclass(frozen=True)
class CoordinateRequest:
    """Input state summary for `coordinate(request)` with dirty-check digest."""
    digest_inputs: dict
    previous_digest: Optional[str] = None
    active_coord_thread_id: Optional[str] = None
    parent_coord_session: str = "8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5"
    prompt: str = ""
    workdir: Optional[Path] = None
    force: bool = False


@dataclass(frozen=True)
class CoordinateDecision:
    """Bounded structured decision returned by `coordinate(request)`."""
    decision_id: str
    action: str
    model_invoked: bool
    digest: str
    thread_id: Optional[str] = None
    actual_model: Optional[str] = None
    tokens_used: int = 0
    payload: dict = field(default_factory=dict)
    job_dir: Optional[str] = None


@dataclass(frozen=True)
class RoleTaskRequest:
    """Bounded role execution contract passed to `submit_role_task`."""
    task_id: str
    task_revision: int
    role: str
    phase: str
    prompt: str
    demand_id: str = ""
    model: str = DEFAULT_MODEL
    workdir: Optional[Path] = None
    allowed_paths: List[str] = field(default_factory=list)
    forbidden_paths: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    approval_verified: bool = False
    require_commit: bool = True
    watch_dir: Optional[Path] = None


@dataclass(frozen=True)
class RoleJobHandle:
    """Durable handle returned immediately after `submit_role_task`."""
    job_id: str
    dispatch_key: str
    role: str
    sandbox_mode: str
    job_dir: Path
    thread_id: Optional[str] = None


@dataclass(frozen=True)
class RoleJobStatus:
    """Queryable status for `query_role_job(job_id_or_dispatch_key)`."""
    job_id: str
    dispatch_key: str
    state: str
    thread_id: Optional[str] = None
    returncode: Optional[int] = None
    reconcile_required: bool = False
    detail: str = ""


@dataclass(frozen=True)
class RoleTaskResult:
    """Verified deliverable and session proof returned by `collect_role_result`."""
    job_id: str
    dispatch_key: str
    task_id: str
    task_revision: int
    role: str
    thread_id: str
    actual_model: str
    tokens_used: int
    summary: str
    candidate_commit: Optional[str]
    artifacts: List[str]
    events_path: str
    output_payload: dict


@dataclass(frozen=True)
class RoleSliceSpec:
    """Single bounded role slice under a multi-role demand split (P1-17)."""
    task_id: str
    role: str
    allowed_paths: List[str]
    deliverables: List[str]
    prompt: str
    require_commit: bool = True


@dataclass(frozen=True)
class MultiRoleSplitSpec:
    """Specification splitting 1 approved demand into N bounded role tasks (P1-17)."""
    demand_id: str
    approval: ApprovalCheckResult
    slices: List[RoleSliceSpec]
    task_revision: int = 1


@dataclass(frozen=True)
class DemandDispatchPlan:
    """Deterministic routing outcome for an intake category record (P1-02/03/04/18)."""
    demand_id: str
    kind: str
    route: str
    sandbox_mode: str
    target_roles: List[str]
    implementation_released: bool
    held_reason: Optional[str] = None


def _coord_decision_schema() -> dict:
    props = {
        "decision_id": {"type": "string"},
        "action": {"type": "string", "enum": sorted(VALID_COORD_ACTIONS)},
        "target_role": {"type": "string"},
        "target_task_id": {"type": "string"},
        "rationale": {"type": "string"},
        "next_check_condition": {"type": "string"},
    }
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def _role_output_schema() -> dict:
    props = {
        "status": {"type": "string", "enum": ["COMPLETED", "NEEDS_CLARIFICATION", "BLOCKED"]},
        "summary": {"type": "string"},
        "candidate_commit": {"type": "string"},
        "artifacts": {"type": "array", "items": {"type": "string"}},
        "notes": {"type": "string"},
    }
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def _parse_codex_jsonl(raw_jsonl: str) -> Tuple[Optional[str], int]:
    thread_id: Optional[str] = None
    tokens_used = 0
    for line in raw_jsonl.splitlines():
        try:
            evt = json.loads(line)
        except ValueError:
            continue
        if not isinstance(evt, dict):
            continue
        if evt.get("type") == "thread.started" and evt.get("thread_id"):
            thread_id = str(evt["thread_id"])
        elif evt.get("type") == "turn.completed":
            usage = evt.get("usage") or {}
            tokens_used += int(usage.get("input_tokens", 0)) + int(usage.get("output_tokens", 0))
    return thread_id, tokens_used


def _match_any_pattern(rel_path: str, patterns: List[str]) -> bool:
    for pat in patterns:
        clean_pat = pat.strip().lstrip("./")
        if clean_pat.endswith("/**"):
            prefix = clean_pat[:-3]
            if rel_path == prefix or rel_path.startswith(prefix + "/"):
                return True
        if fnmatch.fnmatch(rel_path, clean_pat):
            return True
    return False


def _is_alias_or_invalid_session(session_id: Optional[str]) -> bool:
    if not session_id or not isinstance(session_id, str):
        return True
    lowered = session_id.strip().lower()
    return not lowered or lowered.startswith(("pending-", "planned-", "subagent-", "alias-"))


def route_intake_demand(record: dict, approval: ApprovalCheckResult) -> DemandDispatchPlan:
    """Route `requirement`/`issue`/`feature` per clarity, root-cause, and approval state."""
    kind = str(record.get("kind", "feature"))
    dem_id = str((record.get("demand_ref") or {}).get("demand_id") or approval.demand_id)
    triage = record.get("triage_metadata") or {}
    if kind == "requirement" and triage.get("clarity_status") == "unclear":
        return DemandDispatchPlan(
            demand_id=dem_id, kind=kind, route="CLARIFY_PM_ARCH", sandbox_mode="read-only",
            target_roles=["PM", "ARCH"], implementation_released=False,
            held_reason="WAITING_PM_ARCH_CLARIFICATION",
        )
    if kind == "issue":
        if triage.get("root_cause_status", "unknown") != "known":
            investigator = triage.get("proposed_owner_role") or "ARCH"
            return DemandDispatchPlan(
                demand_id=dem_id, kind=kind, route="INVESTIGATE_ISSUE_READONLY", sandbox_mode="read-only",
                target_roles=[investigator], implementation_released=False,
                held_reason="ROOT_CAUSE_UNKNOWN_INVESTIGATE_FIRST",
            )
        owner = triage.get("proposed_owner_role") or "INTEGRATOR"
        if not approval.implementation_allowed:
            return DemandDispatchPlan(
                demand_id=dem_id, kind=kind, route="HOLD_PENDING_APPROVAL", sandbox_mode="read-only",
                target_roles=[owner], implementation_released=False, held_reason=approval.status,
            )
        return DemandDispatchPlan(
            demand_id=dem_id, kind=kind, route="DISPATCH_KNOWN_ISSUE_OWNER",
            sandbox_mode="workspace-write", target_roles=[owner], implementation_released=True,
        )
    if not approval.implementation_allowed:
        return DemandDispatchPlan(
            demand_id=dem_id, kind=kind, route="HOLD_PENDING_APPROVAL", sandbox_mode="read-only",
            target_roles=["PM", "ARCH"], implementation_released=False, held_reason=approval.status,
        )
    owner = triage.get("proposed_owner_role") or "INTEGRATOR"
    return DemandDispatchPlan(
        demand_id=dem_id, kind=kind, route="DISPATCH_APPROVED_FEATURE",
        sandbox_mode="workspace-write", target_roles=[owner], implementation_released=True,
    )


def build_multi_role_requests(spec: MultiRoleSplitSpec) -> List[RoleTaskRequest]:
    """Split 1 approved demand into multiple bounded role task requests keeping 1 demand_id (P1-17)."""
    if not spec.demand_id or not spec.demand_id.strip():
        raise GateValidationError("Multi-role split requires a single non-empty demand_id")
    if not spec.approval.implementation_allowed or spec.approval.demand_id != spec.demand_id:
        raise ApprovalValidationError(
            f"Cannot split unapproved or mismatched demand {spec.demand_id}",
            "UNAPPROVED_MULTI_ROLE_SPLIT",
        )
    if not spec.slices:
        raise GateValidationError("Multi-role split requires at least one bounded RoleSliceSpec")
    seen_task_ids: set = set()
    requests: List[RoleTaskRequest] = []
    for item in spec.slices:
        if item.task_id in seen_task_ids:
            raise GateValidationError(f"Duplicate task_id in multi-role split: {item.task_id}")
        if not item.allowed_paths:
            raise BoundaryViolationError(f"Role slice {item.task_id} missing bounded allowed_paths")
        seen_task_ids.add(item.task_id)
        requests.append(RoleTaskRequest(
            task_id=item.task_id, task_revision=spec.task_revision, role=item.role,
            phase="implement", prompt=item.prompt, demand_id=spec.demand_id,
            allowed_paths=list(item.allowed_paths), deliverables=list(item.deliverables),
            approval_verified=True, require_commit=item.require_commit,
        ))
    return requests


def verify_independent_codex_review_entry(entry: dict, author_session: str, workspace_root: Path) -> None:
    """Reject ordinary subagent impersonation, planned aliases, or missing Codex JSONL proof (P1-12)."""
    if not isinstance(entry, dict):
        raise GateValidationError("Review entry must be a dictionary")
    platform = entry.get("platform")
    if platform != "codex":
        raise GateValidationError(
            f"Independent QA/review must use platform='codex', rejected platform={platform!r}"
        )
    session = entry.get("session") or entry.get("reviewer_session")
    if _is_alias_or_invalid_session(session):
        raise GateValidationError(f"Invalid or planned-alias reviewer session rejected: {session!r}")
    if author_session and session == author_session:
        raise GateValidationError(f"Self-review rejected for author session {author_session}")
    if entry.get("model", DEFAULT_MODEL) != DEFAULT_MODEL:
        raise GateValidationError(f"Reviewer model must be {DEFAULT_MODEL}, got {entry.get('model')!r}")
    ev_ref = entry.get("session_evidence")
    if not isinstance(ev_ref, dict) or not ev_ref.get("path") or not ev_ref.get("sha256"):
        raise GateValidationError("Independent Codex review missing mandatory session_evidence path/sha256")
    ev_path = Path(ev_ref["path"])
    if not ev_path.is_absolute():
        ev_path = (workspace_root / ev_path).resolve()
    if not ev_path.is_file():
        raise GateValidationError(f"Reviewer session_evidence file missing: {ev_path}")
    raw_bytes = ev_path.read_bytes()
    if hashlib.sha256(raw_bytes).hexdigest() != ev_ref["sha256"]:
        raise GateValidationError("Reviewer session_evidence SHA256 mismatch")
    thread_id, _ = _parse_codex_jsonl(raw_bytes.decode("utf-8", errors="replace"))
    if thread_id != session:
        raise GateValidationError(f"Codex JSONL thread.started ({thread_id}) != claimed session ({session})")


class CodexRoleAdapter:
    """Real host adapter driving `/home/sushaohua/.local/bin/codex exec -m gpt-6-luna`."""

    def __init__(self, config: Optional[RoleAdapterConfig] = None):
        cfg = config or RoleAdapterConfig()
        self.workspace_root = Path(cfg.workspace_root).resolve()
        default_jobs = self.workspace_root / "project-control/tools/coord_runner/runtime_jobs"
        self.jobs_dir = Path(cfg.jobs_dir).resolve() if cfg.jobs_dir else default_jobs.resolve()
        self.codex_bin = Path(cfg.codex_bin)
        self.default_model = cfg.default_model
        self.codex_home = Path(cfg.codex_home).resolve()
        self.timeout_seconds = cfg.timeout_seconds
        self.require_remote_push = cfg.require_remote_push
        self.enforce_phase1_repo_lock = cfg.enforce_phase1_repo_lock

    def _ensure_codex_available(self, requested_model: str) -> None:
        if requested_model != self.default_model:
            raise GateValidationError(
                f"Model override rejected: requested {requested_model!r}, required {self.default_model!r}"
            )
        if not self.codex_bin.is_file() or not os.access(str(self.codex_bin), os.X_OK):
            raise CoordRunnerError(f"Host Codex CLI unavailable or not executable: {self.codex_bin}")

    def _build_coord_command(self, req: CoordinateRequest, job_dir: Path) -> List[str]:
        workdir = (req.workdir or self.workspace_root).resolve()
        schema_p = str(job_dir / "schema.json")
        final_p = str(job_dir / "final.json")
        if req.active_coord_thread_id:
            return [
                str(self.codex_bin), "exec", "--sandbox", "read-only",
                "resume", req.active_coord_thread_id, "--skip-git-repo-check",
                "-c", 'approval_policy="never"', "-m", self.default_model,
                "--json", "--output-schema", schema_p, "-o", final_p, "-",
            ]
        return [
            str(self.codex_bin), "exec", "--skip-git-repo-check",
            "--sandbox", "read-only", "-c", 'approval_policy="never"',
            "-m", self.default_model, "-C", str(workdir),
            "--json", "--output-schema", schema_p, "-o", final_p, "-",
        ]

    def coordinate(self, request: CoordinateRequest) -> CoordinateDecision:
        """Execute or short-circuit COORD decision; 0 model calls when digest is unchanged."""
        digest = compute_bytes_sha256(json.dumps(request.digest_inputs, sort_keys=True, ensure_ascii=False))
        if not request.force and request.previous_digest is not None and request.previous_digest == digest:
            return CoordinateDecision(
                decision_id=f"noop_{digest[:12]}", action="NOOP", model_invoked=False,
                digest=digest, thread_id=request.active_coord_thread_id,
                actual_model=None, tokens_used=0, payload={"action": "NOOP"},
            )
        self._ensure_codex_available(self.default_model)
        job_dir = self.jobs_dir / f"coord_{uuid.uuid4().hex[:12]}"
        job_dir.mkdir(parents=True, exist_ok=True)
        (job_dir / "schema.json").write_text(json.dumps(_coord_decision_schema()), encoding="utf-8")
        prompt = request.prompt or f"[COORD_DIGEST:{digest}]\nEvaluate current intake and queue delta."
        (job_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
        cmd = self._build_coord_command(request, job_dir)
        self._execute_codex_subprocess(cmd, prompt, job_dir)
        raw_events = (job_dir / "codex_events.jsonl").read_text(encoding="utf-8")
        thread_id, tokens = _parse_codex_jsonl(raw_events)
        resolved_tid = thread_id or request.active_coord_thread_id
        if _is_alias_or_invalid_session(resolved_tid):
            raise GateValidationError("COORD execution produced no valid thread_id")
        actual_model = self._verify_rollout_model(str(resolved_tid))
        payload = json.loads((job_dir / "final.json").read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or payload.get("action") not in VALID_COORD_ACTIONS:
            raise GateValidationError(f"Unsupported COORD decision action: {payload!r}")
        return CoordinateDecision(
            decision_id=str(payload["decision_id"]), action=str(payload["action"]),
            model_invoked=True, digest=digest, thread_id=str(resolved_tid),
            actual_model=actual_model, tokens_used=tokens, payload=payload, job_dir=str(job_dir),
        )

    def _validate_role_request_and_sandbox(self, request: RoleTaskRequest, dispatch_key: str) -> str:
        if not dispatch_key or not isinstance(dispatch_key, str) or not dispatch_key.strip():
            raise GateValidationError("submit_role_task requires non-empty dispatch_key")
        self._ensure_codex_available(request.model)
        if request.role in READ_ONLY_ROLES or request.phase in {"clarify", "plan", "investigate", "review"}:
            if request.role in READ_ONLY_ROLES and request.phase == "implement":
                raise BoundaryViolationError(f"Read-only role {request.role} cannot run phase='implement'")
            return "read-only"
        if request.role not in WRITE_CAPABLE_ROLES:
            raise GateValidationError(f"Unknown execution role: {request.role!r}")
        if not request.approval_verified:
            raise ApprovalValidationError(
                f"Task {request.task_id} lacks verified HUMAN approval for workspace-write",
                "APPROVAL_REQUIRED",
            )
        self._validate_write_whitelist(request.allowed_paths, request.forbidden_paths)
        return "workspace-write"

    def _validate_write_whitelist(self, allowed_paths: List[str], forbidden_paths: List[str]) -> None:
        if not allowed_paths:
            raise BoundaryViolationError("workspace-write task requires non-empty allowed_paths")
        for raw_p in allowed_paths:
            norm = raw_p.strip().lstrip("./")
            if not norm or norm == "**" or Path(norm).is_absolute() or ".." in Path(norm).parts:
                raise BoundaryViolationError(f"Unbounded or escaping allowed_path rejected: {raw_p}", [raw_p])
            if self.enforce_phase1_repo_lock and norm.startswith(PHASE1_LOCKED_PREFIXES):
                raise BoundaryViolationError(f"Phase 1 forbids business/bootloader path: {raw_p}", [raw_p])
            if forbidden_paths and _match_any_pattern(norm, forbidden_paths):
                raise BoundaryViolationError(f"allowed_path overlaps forbidden_paths: {raw_p}", [raw_p])

    def _snapshot_tree(self, root: Path) -> Dict[str, bytes]:
        snap: Dict[str, bytes] = {}
        if not root.is_dir():
            return snap
        jobs_resolved = self.jobs_dir.resolve()
        for dirpath, dirnames, filenames in os.walk(str(root)):
            dirnames[:] = [d for d in dirnames if d not in {".git", "__pycache__", ".pytest_cache"}]
            cur_dir = Path(dirpath).resolve()
            if cur_dir == jobs_resolved or jobs_resolved in cur_dir.parents:
                continue
            for fname in filenames:
                fpath = cur_dir / fname
                if fpath.is_symlink() or not fpath.is_file():
                    continue
                try:
                    rel = str(fpath.relative_to(self.workspace_root))
                    snap[rel] = fpath.read_bytes()
                except (OSError, ValueError):
                    continue
        return snap

    def _audit_and_revert_violations(
        self,
        before: Dict[str, bytes],
        after: Dict[str, bytes],
        bounds: Tuple[List[str], List[str]],
    ) -> Tuple[List[str], List[str]]:
        allowed, forbidden = bounds
        all_forbidden = list(forbidden)
        if self.enforce_phase1_repo_lock:
            all_forbidden.extend(f"{p}**" for p in PHASE1_LOCKED_PREFIXES)
        changed = [p for p in sorted(set(before) | set(after)) if before.get(p) != after.get(p)]
        violations: List[str] = []
        for rel_p in changed:
            if _match_any_pattern(rel_p, all_forbidden) or not _match_any_pattern(rel_p, allowed):
                violations.append(rel_p)
                full_p = self.workspace_root / rel_p
                if rel_p in before:
                    full_p.parent.mkdir(parents=True, exist_ok=True)
                    full_p.write_bytes(before[rel_p])
                elif full_p.is_file():
                    full_p.unlink()
        return changed, violations

    def _execute_codex_subprocess(self, cmd: List[str], prompt: str, job_dir: Path) -> int:
        events_path = job_dir / "codex_events.jsonl"
        stderr_path = job_dir / "codex.stderr"
        with events_path.open("w", encoding="utf-8") as out_f, stderr_path.open("w", encoding="utf-8") as err_f:
            try:
                proc = subprocess.run(
                    cmd, input=prompt, text=True, stdout=out_f, stderr=err_f,
                    timeout=self.timeout_seconds, check=False,
                )
            except subprocess.TimeoutExpired as err:
                (job_dir / "timeout.json").write_text(
                    json.dumps({"timed_out": True, "error": str(err)}), encoding="utf-8"
                )
                raise CoordRunnerError(f"Codex job timed out (reconcile required): {job_dir}") from err
            except OSError as err:
                (job_dir / "os_error.txt").write_text(str(err), encoding="utf-8")
                raise CoordRunnerError(f"Failed to spawn Codex CLI: {err}") from err
        exit_payload = {
            "returncode": proc.returncode,
            "finished_at": datetime.datetime.now().astimezone().isoformat(),
        }
        (job_dir / "exit_status.json").write_text(json.dumps(exit_payload, indent=2), encoding="utf-8")
        if proc.returncode != 0:
            raise CoordRunnerError(f"Codex CLI exited with code {proc.returncode}; logs: {job_dir}")
        return proc.returncode

    def _register_dispatch_index(self, dispatch_key: str, job_id: str, job_dir: Path) -> None:
        self.jobs_dir.mkdir(parents=True, exist_ok=True)
        idx_path = self.jobs_dir / "dispatch_index.json"
        index = {}
        if idx_path.is_file():
            try:
                index = json.loads(idx_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                index = {}
        index[dispatch_key] = {"job_id": job_id, "job_dir": str(job_dir)}
        index[job_id] = {"job_id": job_id, "dispatch_key": dispatch_key, "job_dir": str(job_dir)}
        idx_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

    def _build_codex_job_bundle(
        self,
        request: RoleTaskRequest,
        dispatch_key: str,
    ) -> Tuple[Path, str, List[str], str]:
        sandbox = self._validate_role_request_and_sandbox(request, dispatch_key)
        job_id = f"job_{request.task_id}_{uuid.uuid4().hex[:10]}"
        job_dir = self.jobs_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=False)
        self._register_dispatch_index(dispatch_key, job_id, job_dir)
        workdir = (request.workdir or self.workspace_root).resolve()
        full_prompt = f"[COORD_DISPATCH_KEY:{dispatch_key}]\n{request.prompt}"
        meta = {
            "job_id": job_id, "dispatch_key": dispatch_key, "task_id": request.task_id,
            "task_revision": request.task_revision, "demand_id": request.demand_id,
            "role": request.role, "phase": request.phase, "sandbox_mode": sandbox,
            "requested_model": request.model, "allowed_paths": list(request.allowed_paths),
            "forbidden_paths": list(request.forbidden_paths), "deliverables": list(request.deliverables),
            "require_commit": request.require_commit, "workdir": str(workdir),
            "started_at": datetime.datetime.now().astimezone().isoformat(),
        }
        (job_dir / "job_meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
        (job_dir / "schema.json").write_text(json.dumps(_role_output_schema()), encoding="utf-8")
        (job_dir / "prompt.txt").write_text(full_prompt, encoding="utf-8")
        cmd = [
            str(self.codex_bin), "exec", "--skip-git-repo-check",
            "--sandbox", sandbox, "-c", 'approval_policy="never"',
            "-m", request.model, "-C", str(workdir),
            "--json", "--output-schema", str(job_dir / "schema.json"),
            "-o", str(job_dir / "final.json"), "-",
        ]
        return job_dir, sandbox, cmd, full_prompt

    def submit_role_task(self, request: RoleTaskRequest, dispatch_key: str) -> RoleJobHandle:
        """Launch single-step `codex exec -m gpt-6-luna` role session with dispatch_key & path audit."""
        job_dir, sandbox, cmd, full_prompt = self._build_codex_job_bundle(request, dispatch_key)
        watch_root = (request.watch_dir or request.workdir or self.workspace_root).resolve()
        before = self._snapshot_tree(watch_root) if sandbox == "workspace-write" else {}
        self._execute_codex_subprocess(cmd, full_prompt, job_dir)
        if sandbox == "workspace-write":
            after = self._snapshot_tree(watch_root)
            changed, violations = self._audit_and_revert_violations(
                before, after, (request.allowed_paths, request.forbidden_paths),
            )
            (job_dir / "boundary_audit.json").write_text(
                json.dumps({"changed_paths": changed, "violating_paths": violations}, indent=2),
                encoding="utf-8",
            )
        raw_events = (job_dir / "codex_events.jsonl").read_text(encoding="utf-8")
        thread_id, _ = _parse_codex_jsonl(raw_events)
        return RoleJobHandle(job_id=job_dir.name, dispatch_key=dispatch_key, role=request.role,
                             sandbox_mode=sandbox, job_dir=job_dir, thread_id=thread_id)

    def submit_role_task_async(
        self,
        request: RoleTaskRequest,
        dispatch_key: str,
        launcher: Optional[JobLauncher] = None,
    ) -> RoleJobHandle:
        """Launch non-blocking asynchronous role task in background; returns durable handle immediately."""
        job_dir, sandbox, cmd, full_prompt = self._build_codex_job_bundle(request, dispatch_key)
        active_launcher = launcher or JobLauncher(self.workspace_root, self.codex_bin, self.default_model)
        active_launcher.launch_async(job_dir, cmd, full_prompt)
        return RoleJobHandle(
            job_id=job_dir.name, dispatch_key=dispatch_key, role=request.role,
            sandbox_mode=sandbox, job_dir=job_dir, thread_id=None,
        )

    def _lookup_host_sqlite_thread(self, dispatch_key: str) -> Optional[str]:
        db_path = self.codex_home / "state_5.sqlite"
        if not db_path.is_file():
            return None
        prefix = f"[COORD_DISPATCH_KEY:{dispatch_key}]%"
        try:
            uri = f"file:{db_path}?mode=ro"
            conn = sqlite3.connect(uri, uri=True, timeout=2.0)
            try:
                cur = conn.execute(
                    "SELECT id FROM threads WHERE first_user_message LIKE ? ORDER BY created_at DESC LIMIT 1",
                    (prefix,),
                )
                row = cur.fetchone()
                return str(row[0]) if row and row[0] else None
            finally:
                conn.close()
        except sqlite3.Error:
            return None

    def _check_proc_alive(self, pid_file: Path) -> bool:
        if not pid_file.is_file():
            return False
        try:
            info = json.loads(pid_file.read_text(encoding="utf-8"))
            pid = int(info["pid"])
            expected_start = str(info.get("starttime", ""))
            stat_text = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8")
            after_comm = stat_text.rsplit(")", 1)[1].split()
            actual_start = after_comm[19]
            return not expected_start or actual_start == expected_start
        except (OSError, ValueError, KeyError, IndexError):
            return False

    def query_role_job(self, job_id_or_key: str) -> RoleJobStatus:
        """Query job/session status across local job dir, `/proc`, and `~/.codex/state_5.sqlite`."""
        idx_path = self.jobs_dir / "dispatch_index.json"
        entry = {}
        if idx_path.is_file():
            index = json.loads(idx_path.read_text(encoding="utf-8"))
            entry = index.get(job_id_or_key, {})
        job_dir = Path(entry["job_dir"]) if entry.get("job_dir") else (self.jobs_dir / job_id_or_key)
        if not job_dir.is_dir():
            host_tid = self._lookup_host_sqlite_thread(job_id_or_key)
            if host_tid:
                return RoleJobStatus(job_id="", dispatch_key=job_id_or_key, state="LAUNCH_UNKNOWN",
                                     thread_id=host_tid, reconcile_required=True, detail="Found in host state_5.sqlite")
            return RoleJobStatus(job_id="", dispatch_key=job_id_or_key, state="NOT_FOUND", detail="No job record")
        meta = json.loads((job_dir / "job_meta.json").read_text(encoding="utf-8"))
        d_key = meta["dispatch_key"]
        j_id = meta["job_id"]
        thread_id = None
        if (job_dir / "codex_events.jsonl").is_file():
            thread_id, _ = _parse_codex_jsonl((job_dir / "codex_events.jsonl").read_text(encoding="utf-8"))
        if not thread_id:
            thread_id = self._lookup_host_sqlite_thread(d_key)
        if self._check_proc_alive(job_dir / "pid.json"):
            return RoleJobStatus(job_id=j_id, dispatch_key=d_key, state="RUNNING", thread_id=thread_id)
        if (job_dir / "exit_status.json").is_file():
            rc = int(json.loads((job_dir / "exit_status.json").read_text(encoding="utf-8"))["returncode"])
            st = "COMPLETED" if rc == 0 else "FAILED"
            return RoleJobStatus(job_id=j_id, dispatch_key=d_key, state=st, thread_id=thread_id, returncode=rc)
        return RoleJobStatus(
            job_id=j_id, dispatch_key=d_key, state="LAUNCH_UNKNOWN",
            thread_id=thread_id, reconcile_required=True,
            detail="Missing exit_status.json; do not blindly re-dispatch",
        )

    def _verify_rollout_model(self, thread_id: str) -> str:
        sessions_dir = self.codex_home / "sessions"
        if sessions_dir.is_dir():
            matches = list(sessions_dir.rglob(f"rollout-*-{thread_id}.jsonl"))
            for rollout in matches:
                for line in rollout.read_text(encoding="utf-8", errors="replace").splitlines():
                    try:
                        obj = json.loads(line)
                    except ValueError:
                        continue
                    if isinstance(obj, dict) and obj.get("type") == "turn_context":
                        model = (obj.get("payload") or {}).get("model")
                        if model and model != self.default_model:
                            raise GateValidationError(
                                f"Rollout model mismatch for {thread_id}: expected {self.default_model}, got {model}"
                            )
                        if model:
                            return str(model)
        return self.default_model

    def _verify_remote_commit(self, repo_dir: Path, commit: str) -> None:
        git_dir = repo_dir if (repo_dir / ".git").exists() else (self.workspace_root / "project-control")
        proc = subprocess.run(
            ["git", "-c", "safe.directory=*", "-C", str(git_dir), "branch", "-r", "--contains", commit],
            capture_output=True, text=True, timeout=10, check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return
        rem = subprocess.run(
            ["git", "-c", "safe.directory=*", "-C", str(git_dir), "ls-remote", "origin"],
            capture_output=True, text=True, timeout=10, check=False,
        )
        if rem.returncode == 0 and commit in rem.stdout:
            return
        raise GateValidationError(f"Candidate commit {commit} is not pushed to server remote origin (P1-12)")

    def _verify_implementation_outputs(self, meta: dict, output: dict) -> Optional[str]:
        for rel_art in meta.get("deliverables") or []:
            art_path = Path(rel_art)
            if not art_path.is_absolute():
                art_path = (self.workspace_root / rel_art).resolve()
                if not art_path.is_file() and (Path(meta["workdir"]) / rel_art).is_file():
                    art_path = (Path(meta["workdir"]) / rel_art).resolve()
            if not art_path.is_file() or art_path.stat().st_size == 0:
                raise GateValidationError(
                    f"Exit 0 rejected: declared deliverable missing or empty: {rel_art} (P1-11)"
                )
        raw_commit = str(output.get("candidate_commit") or "").strip()
        if not meta.get("require_commit", True):
            return raw_commit or None
        if not HEX40_RE.match(raw_commit) or len(set(raw_commit)) <= 1:
            raise GateValidationError(
                f"Exit 0 rejected: missing or placeholder 40-char candidate_commit ({raw_commit!r}) (P1-11)"
            )
        if self.require_remote_push:
            self._verify_remote_commit(Path(meta["workdir"]), raw_commit)
        return raw_commit

    def collect_role_result(self, job_id: str) -> RoleTaskResult:
        """Collect and strictly verify role output, thread_id, model=='gpt-6-luna', bounds, and commit."""
        status = self.query_role_job(job_id)
        if status.state != "COMPLETED":
            raise GateValidationError(
                f"Cannot collect incomplete/failed job {job_id}: state={status.state} ({status.detail})"
            )
        idx = json.loads((self.jobs_dir / "dispatch_index.json").read_text(encoding="utf-8"))
        job_dir = Path(idx[status.job_id]["job_dir"])
        meta = json.loads((job_dir / "job_meta.json").read_text(encoding="utf-8"))
        if (job_dir / "boundary_audit.json").is_file():
            audit = json.loads((job_dir / "boundary_audit.json").read_text(encoding="utf-8"))
            if audit.get("violating_paths"):
                raise BoundaryViolationError(
                    f"Role {meta['role']} touched unauthorized paths: {audit['violating_paths']}",
                    audit["violating_paths"],
                )
        events_path = job_dir / "codex_events.jsonl"
        thread_id, tokens = _parse_codex_jsonl(events_path.read_text(encoding="utf-8"))
        if _is_alias_or_invalid_session(thread_id):
            raise GateValidationError(f"Job {job_id} missing authentic Codex thread_id (P1-11/P1-12)")
        actual_model = self._verify_rollout_model(str(thread_id))
        if meta.get("requested_model") != self.default_model or actual_model != self.default_model:
            raise GateValidationError(f"Model mismatch: expected {self.default_model}, got {actual_model}")
        output = json.loads((job_dir / "final.json").read_text(encoding="utf-8"))
        if not isinstance(output, dict) or output.get("status") != "COMPLETED":
            raise GateValidationError(f"Role final output status is not COMPLETED: {output!r} (P1-11)")
        commit = (
            self._verify_implementation_outputs(meta, output)
            if meta.get("phase") == "implement"
            else (str(output.get("candidate_commit") or "").strip() or None)
        )
        return RoleTaskResult(
            job_id=meta["job_id"], dispatch_key=meta["dispatch_key"], task_id=meta["task_id"],
            task_revision=int(meta["task_revision"]), role=meta["role"], thread_id=str(thread_id),
            actual_model=actual_model, tokens_used=tokens, summary=str(output.get("summary", "")),
            candidate_commit=commit, artifacts=list(output.get("artifacts") or []),
            events_path=str(events_path), output_payload=output,
        )
