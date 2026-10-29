#!/usr/bin/env python3
"""Main COORD runner orchestrating queue scheduling, leases, and state machine."""

import argparse
import json
from pathlib import Path
import signal
import subprocess
import sys
import time
from typing import Callable, Dict, List, Optional, Set

if __package__:
    from .checkpoint import CheckpointManager
    from .codex_adapter import CodexReviewAdapter
    from .errors import CoordRunnerError, GateValidationError, ResourceConflictError
    from .lease_manager import LeaseManager
    from .models import CoordRunnerConfig, CoordState, TaskExecutionRecord, TaskState
    from .scheduler import CoordScheduler, ScheduleContext
    from .state_machine import CoordStateMachine
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from coord_runner.checkpoint import CheckpointManager
    from coord_runner.codex_adapter import CodexReviewAdapter
    from coord_runner.errors import CoordRunnerError, GateValidationError, ResourceConflictError
    from coord_runner.lease_manager import LeaseManager
    from coord_runner.models import CoordRunnerConfig, CoordState, TaskExecutionRecord, TaskState
    from coord_runner.scheduler import CoordScheduler, ScheduleContext
    from coord_runner.state_machine import CoordStateMachine


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
        if self.agent_executor is None:
            raise CoordRunnerError(f"Missing agent_executor for {record.task_id}: fail-closed enforced")
        commit = self.agent_executor(record.task_id, record)
        self.state_machine.validate_commit_sha(commit)
        record.candidate_commit = commit
        self.state_machine.transition(record, TaskState.CANDIDATE_PUSHED)

    def _execute_qa_phase(self, record: TaskExecutionRecord, card: dict) -> bool:
        if record.state != TaskState.SANDBOX_QA.value:
            self.state_machine.transition(record, TaskState.SANDBOX_QA)
        if self.qa_executor is None:
            raise CoordRunnerError(f"Missing qa_executor for {record.task_id}: fail-closed enforced")
        try:
            verdict = self.qa_executor(record.task_id, record.candidate_commit, record.task_revision)
        except TypeError:
            verdict = self.qa_executor(record.task_id, record.candidate_commit)
        ok = self.state_machine.validate_qa_verdict(record, verdict)
        if ok:
            self.state_machine.transition(record, TaskState.REVIEW)
        return ok

    def _invoke_reviewer(self, role: str, record: TaskExecutionRecord) -> dict:
        try:
            return self.review_executor(record.task_id, record.candidate_commit, role)
        except TypeError:
            try:
                return self.review_executor(record.task_id, record.candidate_commit, record)
            except TypeError:
                return self.review_executor(record.task_id, record.candidate_commit)

    def _ensure_qa_report_review(
        self,
        record: TaskExecutionRecord,
        sessions: list,
        author: str,
    ) -> bool:
        qa_entry = next((e for e in sessions if e.get("role") == "QA"), None)
        if not qa_entry or qa_entry.get("report_review"):
            return True
        non_author = next(
            (e for e in sessions if e.get("role") != "QA" and e.get("decision") == "APPROVED"),
            None,
        )
        if not non_author:
            arch_entry = self._invoke_reviewer("ARCH", record)
            arch_entry.setdefault("role", "ARCH")
            if not self.state_machine.validate_review_verdict(record, arch_entry, author):
                return False
            sessions.append(arch_entry)
            non_author = arch_entry
        qa_entry["report_review"] = {
            "reviewer": non_author.get("reviewer") or non_author.get("session"),
            "session": non_author.get("session"),
            "role": non_author.get("role", "ARCH"),
            "decision": "APPROVED",
        }
        return True

    def _execute_review_phase(self, record: TaskExecutionRecord, card: dict) -> bool:
        if self.review_executor is None:
            raise CoordRunnerError(f"Missing review_executor for {record.task_id}: fail-closed enforced")
        req_raw = card.get("reviewer") or ["QA"]
        required_roles = [req_raw] if isinstance(req_raw, str) else list(req_raw)
        if "review_assignments" not in card or not isinstance(card["review_assignments"], dict):
            card["review_assignments"] = {"reviewer_sessions": []}
        sessions = card["review_assignments"].setdefault("reviewer_sessions", [])
        approved_roles = {e.get("role") for e in sessions if e.get("decision") == "APPROVED"}
        author_session = record.session_id or ""
        for role in required_roles:
            if role in approved_roles:
                continue
            entry = self._invoke_reviewer(role, record)
            entry.setdefault("role", role)
            ok = self.state_machine.validate_review_verdict(record, entry, author_session)
            if not ok:
                return False
            sessions.append(entry)
            approved_roles.add(role)
        if "QA" in required_roles:
            if not self._ensure_qa_report_review(record, sessions, author_session):
                return False
        self.state_machine.transition(record, TaskState.DONE)
        return True

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

    def default_agent_executor(self, task_id: str, record: TaskExecutionRecord) -> str:
        repo_name = self._resolve_task_repo(task_id)
        repo_dir = self.config.workspace_root / repo_name
        if not repo_dir.is_dir():
            repo_dir = self.config.workspace_root
        cmd = ["git", "-c", "safe.directory=*", "-C", str(repo_dir), "rev-parse", "HEAD"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if proc.returncode != 0:
            raise CoordRunnerError(f"Failed to resolve git HEAD in {repo_dir}: {proc.stderr.strip()}")
        commit = proc.stdout.strip()
        self.state_machine.validate_commit_sha(commit)
        self._verify_server_commit(repo_dir, commit)
        return commit

    def default_qa_executor(
        self,
        task_id: str,
        candidate_commit: str,
        revision: int = 1,
    ) -> dict:
        qa_script = self.config.workspace_root / "project-control" / "tools" / "qa_runner" / "qa_runner.py"
        repo = self._resolve_task_repo(task_id)
        cmd = [
            sys.executable, str(qa_script),
            "--task", task_id,
            "--revision", str(revision),
            "--repo-commit", f"{repo}={candidate_commit}",
        ]
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(self.config.workspace_root),
            timeout=300,
        )
        server_qa = self._parse_qa_runner_output(proc.stdout, proc.stderr)
        return {
            "passed": proc.returncode == 0,
            "candidate_commit": candidate_commit,
            "task_id": task_id,
            "server_qa": server_qa,
        }

    def default_review_executor(
        self,
        task_id: str,
        candidate_commit: str,
        role_or_record: object = "QA",
    ) -> dict:
        role = role_or_record if isinstance(role_or_record, str) else "QA"
        adapter = CodexReviewAdapter()
        prompt = (
            f"Review task {task_id} as role {role} with candidate commit {candidate_commit}. "
            "Verify implementation against task contract and state APPROVED or REJECTED."
        )
        res = adapter.execute_review(prompt, self.config.workspace_root)
        return {
            "reviewer_session": res.session_id,
            "session": res.session_id,
            "role": role,
            "decision": res.decision,
            "model": adapter.default_model,
            "commit_sha": candidate_commit,
            "task_id": task_id,
            "tokens_used": res.tokens_used,
            "summary": res.output_text[:200] if res.output_text else "",
        }

    def wire_production_executors(self) -> None:
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


def create_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="COORD task runner and scheduler")
    parser.add_argument("--config", default="project-control/config/coord_runner/coord_config.yaml",
                        help="Path to coord_runner YAML config")
    parser.add_argument("--once", action="store_true", help="Execute single step and exit")
    parser.add_argument("--max-tasks", type=int, default=0, help="Execute up to N tasks and exit")
    parser.add_argument("--daemon", action="store_true", help="Run polling daemon mode")
    parser.add_argument("--poll-interval", type=float, default=None, help="Polling interval in seconds")
    return parser


def main() -> int:
    parser = create_cli_parser()
    args = parser.parse_args()
    cfg_path = Path(args.config)
    import yaml
    raw_cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) if cfg_path.is_file() else {}
    base_dir = cfg_path.parent.parent.parent
    config = CoordRunnerConfig.from_dict(raw_cfg, base_dir)
    runner = CoordRunner(config)
    runner.wire_production_executors()
    if args.once:
        runner.run_once()
        return 0
    if args.max_tasks > 0:
        runner.run_tasks(args.max_tasks)
        return 0
    if args.daemon:
        runner.run_daemon(args.poll_interval)
        return 0
    runner.run_once()
    return 0


if __name__ == "__main__":
    sys.exit(main())
