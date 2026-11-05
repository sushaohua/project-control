#!/usr/bin/env python3
"""COORD 主运行器：统筹任务队列调度、资源租约管理、QA 流水线与状态机流转。"""

import argparse
import hashlib
import inspect
import json
from pathlib import Path
import signal
import subprocess
import sys
import time
import tempfile
import traceback
from typing import Callable, Dict, List, Optional, Set

if __package__:
    from .approval_guard import ApprovalGuard, ApprovalQuery
    from .checkpoint import CheckpointManager
    from .codex_adapter import CodexReviewAdapter
    from .codex_qa import execute_sandbox, validate_server_proof
    from .m1_drill import execute_m1_live_drill
    from .m2_drill import execute_m2_live_drill
    from .qa_contract import create_qa_request, repository_from_card
    from .review_bundle import execute_candidate_audit, validate_current_review_inputs
    from .review_policy import resolve_review_policy
    from .errors import CoordRunnerError, GateValidationError, ResourceConflictError
    from .job_launcher import JobLauncher
    from .lease_manager import LeaseManager
    from .models import (
        CoordRunnerConfig, CoordState, TaskExecutionRecord, TaskState,
        resolve_lock_path, resolve_state_db_path,
    )
    from .reconciler import FiveSourceReconciler, ReconcileReport, ReconcileStatus
    from .role_adapter import CodexRoleAdapter, RoleAdapterConfig, RoleJobHandle, RoleTaskRequest
    from .scheduler import CoordScheduler, ScheduleContext
    from .state_machine import CoordStateMachine
    from .state_store import StateStore
    from .work_intake import WorkIntakeManager
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from coord_runner.approval_guard import ApprovalGuard, ApprovalQuery
    from coord_runner.checkpoint import CheckpointManager
    from coord_runner.codex_adapter import CodexReviewAdapter
    from coord_runner.codex_qa import execute_sandbox, validate_server_proof
    from coord_runner.m1_drill import execute_m1_live_drill
    from coord_runner.m2_drill import execute_m2_live_drill
    from coord_runner.qa_contract import create_qa_request, repository_from_card
    from coord_runner.review_bundle import execute_candidate_audit, validate_current_review_inputs
    from coord_runner.review_policy import resolve_review_policy
    from coord_runner.errors import CoordRunnerError, GateValidationError, ResourceConflictError
    from coord_runner.job_launcher import JobLauncher
    from coord_runner.lease_manager import LeaseManager
    from coord_runner.models import (
        CoordRunnerConfig, CoordState, TaskExecutionRecord, TaskState,
        resolve_lock_path, resolve_state_db_path,
    )
    from coord_runner.reconciler import FiveSourceReconciler, ReconcileReport, ReconcileStatus
    from coord_runner.role_adapter import CodexRoleAdapter, RoleAdapterConfig, RoleJobHandle, RoleTaskRequest
    from coord_runner.scheduler import CoordScheduler, ScheduleContext
    from coord_runner.state_machine import CoordStateMachine
    from coord_runner.state_store import StateStore
    from coord_runner.work_intake import WorkIntakeManager


class CoordRunner:
    """Master COORD runner executing task pipeline with gates and recovery."""

    def __init__(self, config: Optional[CoordRunnerConfig] = None):
        self.config = config or CoordRunnerConfig()
        self.lease_mgr = LeaseManager(
            max_parallel_impl=self.config.max_parallel_implementation,
            default_duration=self.config.default_lease_duration_seconds,
            exclusive_devices=self.config.exclusive_devices,
        )
        self.state_machine = CoordStateMachine(
            max_corrections=self.config.max_evidence_based_corrections,
        )
        self.scheduler = CoordScheduler(
            workspace_root=self.config.workspace_root,
            isolate_legacy_queue=self.config.isolate_legacy_queue,
        )
        self.checkpoint_mgr = CheckpointManager()
        self.approval_guard = ApprovalGuard(self.config.workspace_root)
        self.intake_mgr = WorkIntakeManager(self.config.workspace_root, self.config.intake_root)
        self.role_adapter = CodexRoleAdapter(RoleAdapterConfig(
            workspace_root=self.config.workspace_root,
            jobs_dir=self.config.jobs_dir,
            codex_bin=self.config.codex_bin,
            default_model=self.config.default_model,
        ))
        db_p = resolve_state_db_path(self.config.workspace_root, self.config.state_db_file)
        lock_p = resolve_lock_path(self.config.workspace_root, self.config.lock_file)
        self.state_store = StateStore(
            db_path=db_p,
            lock_path=lock_p,
        )
        self.job_launcher = JobLauncher(
            workspace_root=self.config.workspace_root,
            codex_bin=self.config.codex_bin,
            default_model=self.config.default_model,
        )
        self.reconciler = FiveSourceReconciler(
            workspace_root=self.config.workspace_root,
            state_store=self.state_store,
            codex_home=Path.home() / ".codex",
        )
        self.intake_mgr.reconciler = self.reconciler
        self.async_role_dispatch = False
        self.in_flight_tasks: Dict[str, TaskExecutionRecord] = {}
        self.completed_tasks: Set[str] = set()
        self.cursor: Optional[str] = None
        self._running = False
        self._checkpoint_restored: bool = True
        self.last_intake_summary: Optional[dict] = None
        self.agent_executor: Optional[Callable] = None
        self.qa_executor: Optional[Callable] = None
        self.review_executor: Optional[Callable] = None

    def restore_from_checkpoint(self) -> bool:
        """从状态库或检查点文件恢复运行器游标、在途任务与租约，并在恢复检查点执行人工收件扫描。

        返回值：
        - bool：成功恢复既有检查点状态时返回 True，无历史检查点时返回 False。
        """
        state = self.state_store.load_coord_state()
        if state is None:
            state = self.checkpoint_mgr.safe_load(self.config.checkpoint_file)
            if state is None:
                self.scan_work_intake(persist_ledger=True)
                return False
            self.state_store.save_coord_state(state)
        self.cursor = state.cursor
        self.completed_tasks = set(state.completed_tasks)
        self.in_flight_tasks = dict(state.in_flight_tasks)
        self.lease_mgr.restore_leases(state.leases)
        self.scan_work_intake(persist_ledger=True)
        return True

    def save_checkpoint(self) -> None:
        state = CoordState(
            schema_version=1,
            cursor=self.cursor,
            in_flight_tasks=self.in_flight_tasks,
            completed_tasks=sorted(self.completed_tasks),
            leases=self.lease_mgr.get_active_leases(),
        )
        self.state_store.save_coord_state(state)
        self.checkpoint_mgr.save_checkpoint(self.config.checkpoint_file, state)

    def load_cards(self) -> dict:
        cards_dir = self.config.workspace_root / "project-control/.agents/kanban/microtasks"
        if not cards_dir.is_dir():
            return {}
        tools_dir = str(Path(__file__).resolve().parent.parent)
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        import check_task_graph as graph
        cards, _ = graph.check(self.config.workspace_root)
        return cards

    def _acquire_task_leases(self, task_id: str, card: dict) -> List[str]:
        owner = card.get("owner", f"session_{task_id}")
        acquired = []
        task_kind = card.get("task_kind", "implementation")
        try:
            if task_kind == "implementation":
                lease = self.lease_mgr.acquire_lease(task_id, "implementation", owner)
                acquired.append(lease.lease_id)
            for res_item in card.get("resources", []):
                if isinstance(res_item, dict) and res_item.get("exclusive", False):
                    res_name = res_item.get("resource", "")
                    if res_name:
                        lease = self.lease_mgr.acquire_lease(task_id, res_name, owner)
                        acquired.append(lease.lease_id)
            return acquired
        except Exception:
            for lid in acquired:
                self.lease_mgr.release_lease(lid)
            raise

    def dispatch_task(self, task_id: str, card: dict) -> TaskExecutionRecord:
        if task_id in self.in_flight_tasks:
            raise CoordRunnerError(f"Task {task_id} is already in-flight")
        self.state_machine.validate_ready(card, self.completed_tasks)
        leases = self._acquire_task_leases(task_id, card)
        owner_session = card.get("owner", f"session_{task_id}")
        record = TaskExecutionRecord(
            task_id=task_id,
            state=TaskState.READY.value,
            session_id=owner_session,
            leases=leases,
            task_revision=int(card.get("revision", 1)),
        )
        self.state_machine.transition(record, TaskState.IN_PROGRESS)
        self.in_flight_tasks[task_id] = record
        self.cursor = task_id
        return record

    def _execute_agent_phase(self, record: TaskExecutionRecord, card: dict) -> None:
        if record.runtime_context.get("async_job_id"):
            return
        if self.async_role_dispatch or self.agent_executor == self.default_agent_executor:
            self.dispatch_async_role_task(record.task_id, card)
            return
        if self.agent_executor is None:
            raise CoordRunnerError(f"Missing agent_executor for {record.task_id}: fail-closed enforced")
        commit = self.agent_executor(record.task_id, record)
        self.state_machine.validate_commit_sha(commit)
        self._archive_qa_run(record)
        record.candidate_commit = commit
        self.state_machine.transition(record, TaskState.CANDIDATE_PUSHED)

    def _execute_qa_phase(self, record: TaskExecutionRecord, card: dict) -> bool:
        if record.state != TaskState.SANDBOX_QA.value:
            self.state_machine.transition(record, TaskState.SANDBOX_QA)
        if self.qa_executor is None:
            raise CoordRunnerError(f"Missing qa_executor for {record.task_id}: fail-closed enforced")
        args = (record.task_id, record.candidate_commit, record.task_revision)
        try:
            inspect.signature(self.qa_executor).bind(*args)
        except TypeError:
            args = args[:2]
        verdict = self.qa_executor(*args)
        record.runtime_context["qa_result"] = verdict
        if self.qa_executor == self.default_qa_executor:
            ok = self._validate_sandbox_execution(record, verdict)
        else:
            ok = self.state_machine.validate_qa_verdict(record, verdict)
        if ok:
            self.state_machine.transition(record, TaskState.REVIEW)
        return ok

    def _validate_sandbox_execution(self, record: TaskExecutionRecord, verdict: dict) -> bool:
        """Completed failed tests may be audited, but are never relabelled as passed."""
        if verdict.get("execution_completed") is not True:
            raise CoordRunnerError("Sandbox execution is incomplete")
        if verdict.get("candidate_commit") != record.candidate_commit or verdict.get("task_revision") != record.task_revision:
            raise CoordRunnerError("Sandbox execution does not bind the active candidate")
        proof = validate_server_proof(verdict.get("server_qa"), verdict["request"])
        if proof["passed"] != verdict.get("passed"):
            raise CoordRunnerError("Sandbox result was changed before audit")
        return True

    def _invoke_reviewer(self, role: str, record: TaskExecutionRecord) -> dict:
        args = (record.task_id, record.candidate_commit, role)
        try:
            inspect.signature(self.review_executor).bind(*args)
        except TypeError:
            args = args[:2]
        return self.review_executor(*args)

    def _resolve_qa_report_ref(self, record: TaskExecutionRecord, qa_entry: dict) -> tuple:
        rep_path = qa_entry.get("report_path")
        rep_sha = qa_entry.get("report_sha256")
        if not rep_path or not rep_sha:
            raise CoordRunnerError("QA review entry missing mandatory report_path or report_sha256")
        full_p = Path(rep_path) if Path(rep_path).is_absolute() else (self.config.workspace_root / rep_path)
        if not full_p.is_file():
            raise CoordRunnerError(f"QA report file not found on disk at {full_p}")
        real_sha = hashlib.sha256(full_p.read_bytes()).hexdigest()
        if rep_sha != real_sha:
            raise CoordRunnerError(f"QA entry report_sha256 {rep_sha} does not match physical file sha {real_sha}")
        return rep_path, real_sha

    def _invoke_report_reviewer(
        self,
        record: TaskExecutionRecord,
        rep_path: str,
        rep_sha: str,
    ) -> dict:
        req = {
            "role": "ARCH",
            "report_path": rep_path,
            "report_sha256": rep_sha,
            "review_kind": "qa_report",
        }
        try:
            return self.review_executor(record.task_id, record.candidate_commit, req)
        except TypeError as err:
            raise CoordRunnerError(
                f"Dedicated QA report reviewer failed with TypeError: {err} (fail-closed, fallback strictly prohibited)"
            ) from err

    def _ensure_qa_report_review(
        self,
        record: TaskExecutionRecord,
        sessions: list,
        author: str,
    ) -> bool:
        qa_entry = next((e for e in sessions if e.get("role") == "QA"), None)
        if not qa_entry:
            return True
        if qa_entry.get("report_review"):
            return self._validate_existing_report_review(record, qa_entry, author)
        rep_path, rep_sha = self._resolve_qa_report_ref(record, qa_entry)
        report_res = self._invoke_report_reviewer(record, rep_path, rep_sha)
        report_res.setdefault("role", "ARCH")
        rev_id = report_res.get("reviewer") or report_res.get("session") or report_res.get("reviewer_session")
        qa_rev = qa_entry.get("reviewer") or qa_entry.get("session") or qa_entry.get("reviewer_session")
        if not rev_id or rev_id == qa_rev or (author and rev_id == author):
            ev = self.state_machine._extract_review_failure_evidence(report_res)
            self.state_machine.handle_remediation(record, "QA report reviewer cannot be self or author", ev)
            return False
        if report_res.get("decision") != "APPROVED":
            ev = self.state_machine._extract_review_failure_evidence(report_res)
            self.state_machine.handle_remediation(
                record, f"QA report review rejected: {report_res.get('decision')}", ev
            )
            return False
        qa_entry["report_review"] = {
            "reviewer": rev_id,
            "session": report_res.get("session", rev_id),
            "role": report_res.get("role", "ARCH"),
            "decision": report_res.get("decision"),
            "report_path": rep_path,
            "report_sha256": rep_sha,
            "review_report_path": report_res.get("report_path"),
            "review_report_sha256": report_res.get("report_sha256"),
        }
        return True

    def _validate_existing_report_review(self, record: TaskExecutionRecord,
                                         qa_entry: dict, author: str) -> bool:
        try:
            if self.review_executor == self.default_review_executor:
                review = qa_entry["report_review"]
                self._resolve_qa_report_ref(record, {"report_path": review.get("review_report_path"),
                                                   "report_sha256": review.get("review_report_sha256")})
            self.state_machine._validate_qa_report_review(qa_entry, author, self.config.workspace_root)
            return True
        except GateValidationError as err:
            evidence = self.state_machine._extract_review_failure_evidence(qa_entry["report_review"])
            self.state_machine.handle_remediation(record, f"Pre-existing QA report review invalid: {err}", evidence)
            return False

    def _execute_review_phase(self, record: TaskExecutionRecord, card: dict) -> bool:
        """在调用默认独立审阅器前核对当前卡和冻结 QA 证据。"""
        if self.review_executor is None:
            raise CoordRunnerError(f"Missing review_executor for {record.task_id}: fail-closed enforced")
        policy = resolve_review_policy(card, ("QA",))
        required_roles = policy.roles
        if "review_assignments" not in card or not isinstance(card["review_assignments"], dict):
            card["review_assignments"] = {"reviewer_sessions": []}
        sessions = record.runtime_context.setdefault(
            "review_entries", card["review_assignments"].get("reviewer_sessions", []))
        card["review_assignments"]["reviewer_sessions"] = sessions
        if self.review_executor == self.default_review_executor:
            validate_current_review_inputs(record, card, record.runtime_context.get("qa_result"))
        approved_roles = {e.get("role") for e in sessions if self._review_entry_current(e, record)}
        author_session = record.session_id or ""
        for role in required_roles:
            if role in approved_roles:
                continue
            entry = self._invoke_reviewer(role, record)
            entry.setdefault("role", role)
            ok = self.state_machine.validate_review_verdict(record, entry, author_session)
            if not ok:
                return False
            sessions[:] = [previous for previous in sessions if previous.get("role") != role]
            sessions.append(entry)
            approved_roles.add(role)
        if policy.report_review_required and "QA" in required_roles:
            if not self._ensure_qa_report_review(record, sessions, author_session):
                return False
        acceptance_card = dict(card, candidate_commit=record.candidate_commit,
                               revision=record.task_revision, author_session=record.session_id)
        self.state_machine.validate_done_acceptance(acceptance_card, self.config.workspace_root)
        self.state_machine.transition(record, TaskState.DONE)
        return True

    def _review_entry_current(self, entry: dict, record: TaskExecutionRecord) -> bool:
        if entry.get("decision") != "APPROVED":
            return False
        if self.review_executor != self.default_review_executor:
            return True
        if entry.get("commit_sha") != record.candidate_commit or entry.get("reviewed_task_revision") != record.task_revision:
            return False
        try:
            self._resolve_qa_report_ref(record, entry)
            return True
        except (CoordRunnerError, OSError):
            return False

    def _block_task(self, record: TaskExecutionRecord, error: Exception) -> None:
        context = record.runtime_context
        evidence_dir = Path(tempfile.mkdtemp(prefix=f"coord_error_{record.task_id}_"))
        path = evidence_dir / "error.json"
        data = {"task_id": record.task_id, "task_revision": record.task_revision,
                "candidate_commit": record.candidate_commit, "phase": record.state,
                "error": str(error), "traceback": traceback.format_exc()}
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        ref = {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        context.setdefault("execution_errors", []).append(ref)
        context["blocked_reason"] = str(error)
        if record.state != TaskState.ESCALATED.value:
            context["resume_state"] = record.state
            record.state = TaskState.BLOCKED.value
        record.waiting_events.append(f"execution-blocked:{path}")

    def _process_task_safely(self, task_id: str, card: dict) -> None:
        record = self.in_flight_tasks[task_id]
        if record.state in {TaskState.BLOCKED.value, TaskState.ESCALATED.value}:
            return
        try:
            self.process_task(task_id, card)
        except Exception as error:
            self._block_task(record, error)
        finally:
            self.save_checkpoint()

    def _archive_qa_run(self, record: TaskExecutionRecord) -> None:
        result = record.runtime_context.pop("qa_result", None)
        reviews = record.runtime_context.pop("review_entries", [])
        if result:
            proof = result.get("server_qa") or {}
            history = {"candidate_commit": result.get("candidate_commit"),
                       "run_dir": (result.get("request") or {}).get("run_dir"),
                       "server_qa": {"path": proof.get("path"), "sha256": proof.get("sha256")},
                       "reviews": reviews}
            record.runtime_context.setdefault("previous_qa_runs", []).append(history)

    def resume_task(self, task_id: str, rerun_sandbox: bool = False) -> None:
        """Resume only after COORD resolves the blocker; never silently auto-retry."""
        record = self.in_flight_tasks.get(task_id)
        if not record or record.state != TaskState.BLOCKED.value:
            raise CoordRunnerError(f"Task {task_id} is not blocked")
        card = self.load_cards().get(task_id)
        if not card or card.get("revision") != record.task_revision or card.get("blocked"):
            raise CoordRunnerError("Resolve task inputs/revision before resuming")
        previous = record.runtime_context.get("resume_state")
        if previous not in {TaskState.IN_PROGRESS.value, TaskState.CANDIDATE_PUSHED.value,
                            TaskState.SANDBOX_QA.value, TaskState.REVIEW.value}:
            raise CoordRunnerError("Blocked task has no safe resume phase")
        if rerun_sandbox:
            if not record.candidate_commit:
                raise CoordRunnerError("Cannot rerun sandbox without an exact candidate")
            self._archive_qa_run(record)
            previous = TaskState.SANDBOX_QA.value
        self.lease_mgr.release_task_leases(task_id)
        record.leases = self._acquire_task_leases(task_id, card)
        record.state = previous
        record.runtime_context.pop("blocked_reason", None)
        self.save_checkpoint()

    def _parse_qa_runner_output(self, stdout: str, stderr: str) -> dict:
        prefix = "[SERVER QA REF] "
        for line in stdout.splitlines():
            if line.startswith(prefix):
                try:
                    ref = json.loads(line[len(prefix):].strip())
                    p = Path(ref.get("path", ""))
                    if p.is_file():
                        data = json.loads(p.read_text(encoding="utf-8"))
                        data["path"] = str(p)
                        data["sha256"] = ref.get("sha256", "")
                        return data
                    return ref
                except (json.JSONDecodeError, OSError):
                    pass
        return {
            "path": "server_qa.json",
            "sha256": "0" * 64,
            "sandbox": {"kind": "container"},
            "error": stderr.strip() or stdout.strip(),
        }

    def _resolve_task_repo(self, task_id: str) -> str:
        if task_id.startswith("SOC"):
            return "soc-ap"
        if task_id.startswith(("MC", "TH")):
            return "mcu-p3"
        if task_id.startswith("HARNESS"):
            return "test_harness"
        return "project-control"

    def _verify_server_commit(self, repo_dir: Path, commit: str) -> None:
        cmd = ["git", "-c", "safe.directory=*", "-C", str(repo_dir), "branch", "-r", "--contains", commit]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if proc.returncode != 0 or not proc.stdout.strip():
            rem = subprocess.run(
                ["git", "-c", "safe.directory=*", "-C", str(repo_dir), "ls-remote", "origin"],
                capture_output=True, text=True, timeout=10,
            )
            if rem.returncode == 0 and commit in rem.stdout:
                return
            raise CoordRunnerError(
                f"Candidate commit {commit} is unpushed to server remote in {repo_dir}"
            )

    def _verify_card_approval(self, task_id: str, card: dict) -> None:
        auth = card.get("authorization") or {}
        ev_path = auth.get("evidence")
        demand_id = str(card.get("demand_id") or task_id)
        exec_cfg = card.get("executor") or {}
        query = ApprovalQuery(
            demand_id=demand_id,
            approval_path=Path(ev_path) if ev_path else None,
            requested_model=str(exec_cfg.get("model") or self.config.default_model),
            record_payload=card,
        )
        self.approval_guard.require_implementation_approval(query)

    def _build_agent_role_request(
        self,
        task_id: str,
        record: TaskExecutionRecord,
        card: dict,
    ) -> RoleTaskRequest:
        repo_name = repository_from_card(card) if card.get("write_scope") else self._resolve_task_repo(task_id)
        repo_dir = self.config.workspace_root / repo_name
        workdir = repo_dir if repo_dir.is_dir() else self.config.workspace_root
        exec_cfg = card.get("executor") or {}
        role = str(exec_cfg.get("role") or card.get("proposed_owner") or "INTEGRATOR")
        model = str(exec_cfg.get("model") or self.config.default_model)
        delivs = list((card.get("deliverables") or {}).get("artifacts") or [])
        prompt = (
            f"Execute approved task {task_id} revision {record.task_revision} as role {role}.\n"
            f"Title: {card.get('title', task_id)}\n"
            f"Allowed paths: {card.get('allowed_paths', [])}\n"
            f"Deliverables: {delivs}\n"
            f"Commit and push exact candidate to origin and return structured JSON output."
        )
        return RoleTaskRequest(
            task_id=task_id,
            task_revision=record.task_revision,
            role=role,
            phase="implement",
            prompt=prompt,
            demand_id=str(card.get("demand_id") or ""),
            model=model,
            workdir=workdir,
            watch_dir=workdir,
            allowed_paths=list(card.get("allowed_paths") or []),
            forbidden_paths=list(card.get("forbidden_paths") or []),
            deliverables=delivs,
            approval_verified=True,
            require_commit=True,
        )

    def default_agent_executor(self, task_id: str, record: TaskExecutionRecord) -> str:
        """Dispatch approved role task via host `codex exec -m gpt-6-luna` (replaces passive HEAD lookup)."""
        card = record.runtime_context.get("card") or self.load_cards().get(task_id)
        if not isinstance(card, dict) or not card:
            raise CoordRunnerError(f"Missing accepted task card for {task_id}")
        self._verify_card_approval(task_id, card)
        req = self._build_agent_role_request(task_id, record, card)
        attempt = record.corrections_count + 1
        dispatch_key = f"{task_id}:rev{record.task_revision}:{req.role}:implement:{attempt}"
        handle = self.role_adapter.submit_role_task(req, dispatch_key)
        res = self.role_adapter.collect_role_result(handle.job_id)
        record.session_id = res.thread_id
        record.runtime_context["role_job_id"] = res.job_id
        record.runtime_context["dispatch_key"] = res.dispatch_key
        record.runtime_context["actual_model"] = res.actual_model
        self.state_machine.validate_commit_sha(res.candidate_commit)
        self._verify_server_commit(Path(req.workdir or self.config.workspace_root), str(res.candidate_commit))
        return str(res.candidate_commit)

    def scan_work_intake(
        self,
        persist_ledger: bool = True,
        active_cards: Optional[Dict[str, dict]] = None,
    ) -> dict:
        """扫描 `docs/work_intake/` 提交单与三类工作项，更新幂等摘要并返回收件汇总。

        参数：
        - persist_ledger (bool)：是否将更新后的收件摘要账本写回磁盘，默认 True。
        - active_cards (Optional[Dict[str, dict]])：可选的已加载看板任务字典，避免同一轮检查点重复加载。

        返回值：
        - dict：包含 `submissions_count`、`generated_files`、`valid_records`、`idempotent_records_count`、`errors` 与 `notices` 的字典。
        """
        cards = active_cards if active_cards is not None else self.load_cards()
        res = self.intake_mgr.scan_and_sync(persist_ledger=persist_ledger, active_cards=cards)
        idempotent_count = 0
        for rec_id, rec in res.records.items():
            dem_id = (rec.get("demand_ref") or {}).get("demand_id") or rec_id
            rev = int(rec.get("revision", 1))
            sha = rec.get("_sha256") or rec.get("source_refs", {}).get("submission_sha256", "")
            if sha and self.reconciler.check_intake_idempotence(dem_id, rev, sha):
                idempotent_count += 1
        summary = {
            "submissions_count": len(res.submissions),
            "generated_files": [str(p) for p in res.generated_paths],
            "valid_records": sorted(res.records.keys()),
            "idempotent_records_count": idempotent_count,
            "errors": [e.__dict__ for e in res.errors],
            "notices": [n.__dict__ for n in res.notices],
        }
        self.last_intake_summary = summary
        return summary

    def default_qa_executor(
        self,
        task_id: str,
        candidate_commit: str,
        revision: int = 1,
    ) -> dict:
        """Execute the frozen sandbox test plan directly, before model audit."""
        self.state_machine.validate_commit_sha(candidate_commit)
        card = self.load_cards().get(task_id)
        if not card:
            raise CoordRunnerError(f"Missing accepted task card for {task_id}")
        candidate = {
            "repository": repository_from_card(card),
            "candidate_commit": candidate_commit,
            "task_revision": revision,
        }
        request = create_qa_request(self.config.workspace_root, card, candidate)
        return execute_sandbox(request)

    def default_review_executor(
        self,
        task_id: str,
        candidate_commit: str,
        role_or_record: object = "QA",
    ) -> dict:
        """以当前精确候选和可核验历史上下文执行默认 QA 审阅。"""
        record = self.in_flight_tasks.get(task_id)
        if not record or record.candidate_commit != candidate_commit:
            raise CoordRunnerError("Review requires an active exact candidate")
        qa_result = record.runtime_context.get("qa_result")
        if not qa_result or qa_result.get("candidate_commit") != candidate_commit:
            raise CoordRunnerError("Review requires the completed objective sandbox evidence")
        review = role_or_record if isinstance(role_or_record, dict) else {"role": role_or_record}
        if review.get("review_kind") != "qa_report":
            review = dict(review)
            review["previous_qa_runs"] = list(record.runtime_context.get("previous_qa_runs", []))
        return execute_candidate_audit(CodexReviewAdapter(), qa_result, review)

    def wire_production_executors(self) -> None:
        self.async_role_dispatch = True
        if self.agent_executor is None:
            self.agent_executor = self.default_agent_executor
        if self.qa_executor is None:
            self.qa_executor = self.default_qa_executor
        if self.review_executor is None:
            self.review_executor = self.default_review_executor

    def process_task(self, task_id: str, card: dict) -> str:
        record = self.in_flight_tasks[task_id]
        if record.state == TaskState.IN_PROGRESS.value:
            self._execute_agent_phase(record, card)
        if record.state in {TaskState.CANDIDATE_PUSHED.value, TaskState.SANDBOX_QA.value}:
            if not self._execute_qa_phase(record, card):
                return record.state
        if record.state == TaskState.REVIEW.value:
            if record.task_id in self.in_flight_tasks:
                self.save_checkpoint()
            if not self._execute_review_phase(record, card):
                return record.state
        if record.state == TaskState.DONE.value:
            acceptance_card = dict(card, candidate_commit=record.candidate_commit,
                                   revision=record.task_revision, author_session=record.session_id)
            self.state_machine.validate_done_acceptance(acceptance_card, self.config.workspace_root)
            self.completed_tasks.add(task_id)
            self.lease_mgr.release_task_leases(task_id)
            del self.in_flight_tasks[task_id]
        return record.state

    def dispatch_async_role_task(self, task_id: str, card: dict) -> RoleJobHandle:
        """Launch background async role worker process for task; returns handle."""
        record = self.in_flight_tasks.get(task_id)
        if not record:
            raise CoordRunnerError(f"Task {task_id} not in flight")
        self._verify_card_approval(task_id, card)
        req = self._build_agent_role_request(task_id, record, card)
        attempt = record.corrections_count + 1
        dispatch_key = f"{task_id}:rev{record.task_revision}:{req.role}:implement:{attempt}"
        handle = self.role_adapter.submit_role_task_async(req, dispatch_key, self.job_launcher)
        self.state_store.save_role_job({
            "job_id": handle.job_id, "dispatch_key": dispatch_key, "task_id": task_id,
            "task_revision": record.task_revision, "role": req.role, "phase": req.phase,
            "status": ReconcileStatus.RUNNING.value, "job_dir": str(handle.job_dir),
        })
        record.runtime_context["async_job_id"] = handle.job_id
        record.runtime_context["dispatch_key"] = dispatch_key
        return handle

    def _check_async_job_completions(self) -> None:
        """Advance any background tasks that have transitioned to COMPLETED status."""
        for task_id, record in list(self.in_flight_tasks.items()):
            if record.state != TaskState.IN_PROGRESS.value:
                continue
            job_id = record.runtime_context.get("async_job_id")
            if not job_id:
                continue
            job_rec = self.state_store.get_role_job(job_id)
            if not job_rec:
                continue
            if job_rec.get("status") in {ReconcileStatus.FAILED.value, ReconcileStatus.RECONCILE_REQUIRED.value}:
                record.runtime_context.pop("async_job_id", None)
                self.state_machine.handle_remediation(
                    record,
                    f"Background job {job_id} failed with status {job_rec.get('status')}",
                    {"job_id": job_id, "detail": job_rec.get("detail", "")},
                )
                continue
            if job_rec.get("status") != ReconcileStatus.COMPLETED.value:
                continue
            res = self.role_adapter.collect_role_result(job_id)
            record.candidate_commit = str(res.candidate_commit)
            record.session_id = str(res.thread_id)
            record.runtime_context["role_job_id"] = res.job_id
            record.runtime_context["dispatch_key"] = res.dispatch_key
            record.runtime_context["actual_model"] = res.actual_model
            record.runtime_context.pop("async_job_id", None)
            if res.candidate_commit:
                self.state_machine.validate_commit_sha(res.candidate_commit)
            self.state_machine.transition(record, TaskState.CANDIDATE_PUSHED)

    def step(self) -> Dict[str, object]:
        """执行单轮调度检查点：对账租约与在途作业、自动扫描人工收件、推进在途任务并派发就绪任务。

        返回值：
        - Dict[str, object]：包含游标、派发列表、在途/完成/阻塞/升级列表及 `intake` 收件汇总的字典。
        """
        self.reconciler.protect_active_leases(self.lease_mgr, self.config.jobs_dir)
        self.lease_mgr.prune_expired_leases()
        self.reconciler.reconcile_active_jobs(self.config.jobs_dir)
        self._check_async_job_completions()
        cards = self.load_cards()
        intake_summary = self.scan_work_intake(persist_ledger=True, active_cards=cards)
        for task_id in list(self.in_flight_tasks.keys()):
            card = cards.get(task_id, {"id": task_id})
            self._process_task_safely(task_id, card)
        queue = self.scheduler.load_queue(self.config.queue_file)
        ctx = ScheduleContext(
            queue=queue, cards=cards, completed_tasks=self.completed_tasks,
            in_flight_tasks=set(self.in_flight_tasks.keys()), lease_mgr=self.lease_mgr,
        )
        ready_tasks = self.scheduler.select_next_tasks(ctx)
        dispatched = []
        for task_id in ready_tasks:
            card = cards.get(task_id, {"id": task_id})
            try:
                self.dispatch_task(task_id, card)
                dispatched.append(task_id)
                self._process_task_safely(task_id, card)
            except ResourceConflictError:
                break
        self.save_checkpoint()
        return {
            "cursor": self.cursor,
            "dispatched": dispatched,
            "in_flight": list(self.in_flight_tasks.keys()),
            "completed": sorted(self.completed_tasks),
            "blocked": {key: record.runtime_context.get("blocked_reason", "")
                        for key, record in self.in_flight_tasks.items()
                        if record.state == TaskState.BLOCKED.value},
            "escalated": [key for key, record in self.in_flight_tasks.items()
                          if record.state == TaskState.ESCALATED.value],
            "intake": intake_summary,
        }

    def run_once(self) -> Dict[str, object]:
        self.state_store.acquire_process_lock()
        try:
            self.restore_from_checkpoint()
            result = self.step()
            self.save_checkpoint()
            return result
        finally:
            self.state_store.release_process_lock()

    def run_tasks(self, max_tasks: int) -> int:
        self.state_store.acquire_process_lock()
        try:
            self.restore_from_checkpoint()
            completed_initial = len(self.completed_tasks)
            while len(self.completed_tasks) - completed_initial < max_tasks:
                info = self.step()
                runnable = any(record.state not in {TaskState.BLOCKED.value, TaskState.ESCALATED.value}
                               for record in self.in_flight_tasks.values())
                if not info["dispatched"] and not runnable:
                    break
            self.save_checkpoint()
            return len(self.completed_tasks) - completed_initial
        finally:
            self.state_store.release_process_lock()

    def _signal_handler(self, signum: int, frame: object) -> None:
        """处理 SIGINT/SIGTERM 停止信号，标记退出循环并在已恢复检查点且持锁状态下持久化状态。

        参数：
        - signum (int)：接收到的操作系统信号编号。
        - frame (object)：当前执行栈帧对象。
        """
        self._running = False
        if getattr(self, "_checkpoint_restored", True):
            self.save_checkpoint()

    def run_daemon(self, poll_interval: Optional[float] = None) -> None:
        """启动后台轮询守护进程模式：先获取单实例排他锁，再注册信号处理与恢复检查点。

        参数：
        - poll_interval (Optional[float])：可选的轮询间隔秒数，默认取配置中的 `poll_interval_seconds`。

        返回值：
        - None：收到停止信号退出循环后在锁保护下保存检查点并释放单实例锁。
        """
        interval = poll_interval if poll_interval is not None else self.config.poll_interval_seconds
        self.state_store.acquire_process_lock()
        self._running = True
        self._checkpoint_restored = False
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        try:
            self.restore_from_checkpoint()
            self._checkpoint_restored = True
            while self._running:
                self.step()
                time.sleep(interval)
        finally:
            if self._checkpoint_restored:
                self.save_checkpoint()
            self.state_store.release_process_lock()


def create_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="COORD task runner and scheduler")
    parser.add_argument("--config", default="project-control/config/coord_runner/coord_config.yaml",
                        help="Path to coord_runner YAML config")
    parser.add_argument("--once", action="store_true", help="Execute single step and exit")
    parser.add_argument("--intake-scan", action="store_true", help="Scan work_intake MD/YAML records and exit")
    parser.add_argument("--drill-dir", default="", help="Execute bounded M1 host live drill in directory")
    parser.add_argument("--drill-m2-dir", default="", help="Execute bounded M2 host recovery drill in directory")
    parser.add_argument("--resume-task", help="Explicitly retry a blocked task after resolving its blocker")
    parser.add_argument("--rerun-sandbox", action="store_true", help="With --resume-task, retain old evidence and rerun tests")
    parser.add_argument("--max-tasks", type=int, default=0, help="Execute up to N tasks and exit")
    parser.add_argument("--daemon", action="store_true", help="Run polling daemon mode")
    parser.add_argument("--poll-interval", type=float, default=None, help="Polling interval in seconds")
    return parser


def emit_summary(summary: dict) -> int:
    print(json.dumps(summary, ensure_ascii=False))
    return 2 if summary.get("blocked") or summary.get("escalated") else 0


def _load_cli_config(cfg_arg: str) -> CoordRunnerConfig:
    import yaml
    default_ws = Path(__file__).resolve().parents[3]
    candidates = [Path(cfg_arg), default_ws / cfg_arg]
    cfg_path = next((c.resolve() for c in candidates if c.is_file()), Path(cfg_arg).resolve())
    raw_cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) if cfg_path.is_file() else {}
    base_dir = cfg_path.parents[3] if cfg_path.is_file() and len(cfg_path.parents) >= 4 else default_ws
    return CoordRunnerConfig.from_dict(raw_cfg or {}, base_dir)


def main() -> int:
    parser = create_cli_parser()
    args = parser.parse_args()
    config = _load_cli_config(args.config)
    if args.drill_dir:
        drill_res = execute_m1_live_drill(config.workspace_root, Path(args.drill_dir), config.codex_bin)
        print(json.dumps(drill_res, ensure_ascii=False, indent=2))
        return 0
    if args.drill_m2_dir:
        drill_res = execute_m2_live_drill(config.workspace_root, Path(args.drill_m2_dir))
        print(json.dumps(drill_res, ensure_ascii=False, indent=2))
        return 0
    runner = CoordRunner(config)
    runner.wire_production_executors()
    if args.intake_scan:
        summary = runner.scan_work_intake(persist_ledger=False)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 1 if summary["errors"] else 0
    if args.resume_task:
        runner.restore_from_checkpoint()
        runner.resume_task(args.resume_task, rerun_sandbox=args.rerun_sandbox)
    elif args.rerun_sandbox:
        parser.error("--rerun-sandbox requires --resume-task")
    if args.once:
        return emit_summary(runner.run_once())
    if args.max_tasks > 0:
        completed = runner.run_tasks(args.max_tasks)
        return emit_summary({"completed_count": completed,
                             "blocked": {k: r.runtime_context.get("blocked_reason", "")
                                         for k, r in runner.in_flight_tasks.items()
                                         if r.state == TaskState.BLOCKED.value},
                             "escalated": [k for k, r in runner.in_flight_tasks.items()
                                           if r.state == TaskState.ESCALATED.value]})
    if args.daemon:
        runner.run_daemon(args.poll_interval)
        return 0
    return emit_summary(runner.run_once())


if __name__ == "__main__":
    sys.exit(main())
