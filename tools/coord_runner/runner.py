#!/usr/bin/env python3
"""Main COORD runner orchestrating queue scheduling, leases, and state machine."""

import argparse
from pathlib import Path
import signal
import sys
import time
from typing import Callable, Dict, List, Optional, Set

from .checkpoint import CheckpointManager
from .errors import CoordRunnerError, GateValidationError, ResourceConflictError
from .lease_manager import LeaseManager
from .models import CoordRunnerConfig, CoordState, TaskExecutionRecord, TaskState
from .scheduler import CoordScheduler, ScheduleContext
from .state_machine import CoordStateMachine


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
        self.scheduler = CoordScheduler(workspace_root=self.config.workspace_root)
        self.checkpoint_mgr = CheckpointManager()
        self.in_flight_tasks: Dict[str, TaskExecutionRecord] = {}
        self.completed_tasks: Set[str] = set()
        self.cursor: Optional[str] = None
        self._running = False
        self.agent_executor: Optional[Callable] = None
        self.qa_executor: Optional[Callable] = None
        self.review_executor: Optional[Callable] = None

    def restore_from_checkpoint(self) -> bool:
        state = self.checkpoint_mgr.safe_load(self.config.checkpoint_file)
        if state is None:
            return False
        self.cursor = state.cursor
        self.completed_tasks = set(state.completed_tasks)
        self.in_flight_tasks = dict(state.in_flight_tasks)
        self.lease_mgr.restore_leases(state.leases)
        return True

    def save_checkpoint(self) -> None:
        state = CoordState(
            schema_version=1,
            cursor=self.cursor,
            in_flight_tasks=self.in_flight_tasks,
            completed_tasks=sorted(self.completed_tasks),
            leases=self.lease_mgr.get_active_leases(),
        )
        self.checkpoint_mgr.save_checkpoint(self.config.checkpoint_file, state)

    def load_cards(self) -> dict:
        cards_dir = self.config.workspace_root / "project-control/.agents/kanban/microtasks"
        if not cards_dir.is_dir():
            return {}
        import check_task_graph as graph
        cards, _ = graph.check(self.config.workspace_root)
        return cards

    def _acquire_task_leases(self, task_id: str, card: dict) -> List[str]:
        owner = card.get("owner", f"session_{task_id}")
        acquired = []
        task_kind = card.get("task_kind", "implementation")
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
        )
        self.state_machine.transition(record, TaskState.IN_PROGRESS)
        self.in_flight_tasks[task_id] = record
        self.cursor = task_id
        return record

    def _execute_agent_phase(self, record: TaskExecutionRecord, card: dict) -> None:
        if self.agent_executor:
            commit = self.agent_executor(record.task_id, record)
        else:
            commit = card.get("candidate_commit", "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819")
        self.state_machine.validate_commit_sha(commit)
        record.candidate_commit = commit
        self.state_machine.transition(record, TaskState.CANDIDATE_PUSHED)

    def _execute_qa_phase(self, record: TaskExecutionRecord, card: dict) -> bool:
        self.state_machine.transition(record, TaskState.SANDBOX_QA)
        if self.qa_executor:
            verdict = self.qa_executor(record.task_id, record.candidate_commit)
        else:
            verdict = {"passed": True, "developer_mounts": []}
        ok = self.state_machine.validate_qa_verdict(record, verdict)
        if ok:
            self.state_machine.transition(record, TaskState.REVIEW)
        return ok

    def _execute_review_phase(self, record: TaskExecutionRecord, card: dict) -> bool:
        if self.review_executor:
            entry = self.review_executor(record.task_id, record.candidate_commit)
        else:
            entry = {"session": f"reviewer_{record.task_id}", "decision": "APPROVED"}
        author_session = record.session_id or ""
        ok = self.state_machine.validate_review_verdict(record, entry, author_session)
        if ok:
            if "review_assignments" not in card:
                card["review_assignments"] = {"reviewer_sessions": []}
            card["review_assignments"]["reviewer_sessions"].append(entry)
            self.state_machine.transition(record, TaskState.DONE)
        return ok

    def process_task(self, task_id: str, card: dict) -> str:
        record = self.in_flight_tasks[task_id]
        if record.state == TaskState.IN_PROGRESS.value:
            self._execute_agent_phase(record, card)
        if record.state == TaskState.CANDIDATE_PUSHED.value:
            if not self._execute_qa_phase(record, card):
                return record.state
        if record.state == TaskState.REVIEW.value:
            if not self._execute_review_phase(record, card):
                return record.state
        if record.state == TaskState.DONE.value:
            self.state_machine.validate_done_acceptance(card, self.config.workspace_root)
            self.completed_tasks.add(task_id)
            self.lease_mgr.release_task_leases(task_id)
            del self.in_flight_tasks[task_id]
        return record.state

    def step(self) -> Dict[str, object]:
        self.lease_mgr.prune_expired_leases()
        cards = self.load_cards()
        in_flight_keys = list(self.in_flight_tasks.keys())
        for task_id in in_flight_keys:
            card = cards.get(task_id, {"id": task_id})
            self.process_task(task_id, card)
        queue = self.scheduler.load_queue(self.config.queue_file)
        ctx = ScheduleContext(
            queue=queue,
            cards=cards,
            completed_tasks=self.completed_tasks,
            in_flight_tasks=set(self.in_flight_tasks.keys()),
            lease_mgr=self.lease_mgr,
        )
        ready_tasks = self.scheduler.select_next_tasks(ctx)
        dispatched = []
        for task_id in ready_tasks:
            card = cards.get(task_id, {"id": task_id})
            try:
                self.dispatch_task(task_id, card)
                dispatched.append(task_id)
            except ResourceConflictError:
                break
        self.save_checkpoint()
        return {
            "cursor": self.cursor,
            "dispatched": dispatched,
            "in_flight": list(self.in_flight_tasks.keys()),
            "completed": sorted(self.completed_tasks),
        }

    def run_once(self) -> Dict[str, object]:
        self.restore_from_checkpoint()
        result = self.step()
        self.save_checkpoint()
        return result

    def run_tasks(self, max_tasks: int) -> int:
        self.restore_from_checkpoint()
        completed_initial = len(self.completed_tasks)
        while len(self.completed_tasks) - completed_initial < max_tasks:
            info = self.step()
            if not info["dispatched"] and not info["in_flight"]:
                break
        self.save_checkpoint()
        return len(self.completed_tasks) - completed_initial

    def _signal_handler(self, signum: int, frame: object) -> None:
        self._running = False
        self.save_checkpoint()

    def run_daemon(self, poll_interval: Optional[float] = None) -> None:
        interval = poll_interval if poll_interval is not None else self.config.poll_interval_seconds
        self.restore_from_checkpoint()
        self._running = True
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        try:
            while self._running:
                self.step()
                time.sleep(interval)
        finally:
            self.save_checkpoint()
