#!/usr/bin/env python3
"""Comprehensive test suite for COORD runner, state machine, leases, and recovery."""

import ast
import json
from pathlib import Path
import signal
import sys
import tempfile
import time
import unittest

TOOLS_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = TOOLS_DIR.parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from coord_runner import (
    CheckpointCorruptError,
    CheckpointManager,
    CoordRunner,
    CoordRunnerConfig,
    CoordRunnerError,
    CoordScheduler,
    CoordState,
    CoordStateMachine,
    DependencyUnmetError,
    GateValidationError,
    Lease,
    LeaseExpiredError,
    LeaseManager,
    RemediationLimitExceededError,
    ResourceConflictError,
    ScheduleContext,
    StateTransitionError,
    TaskExecutionRecord,
    TaskState,
)


class TaskSelectionAndSchedulingTest(unittest.TestCase):
    def setUp(self):
        self.scheduler = CoordScheduler()
        self.queue = {
            "bootstrap": ["AUTO-01", "AUTO-02"],
            "order": ["TWIN-01", "TWIN-02"],
        }
        self.cards = {
            "AUTO-01": {"id": "AUTO-01", "depends_on": [], "status": "Done"},
            "AUTO-02": {"id": "AUTO-02", "depends_on": ["AUTO-01"], "status": "Backlog"},
            "TWIN-01": {"id": "TWIN-01", "depends_on": ["AUTO-02"], "status": "Backlog"},
            "TWIN-02": {"id": "TWIN-02", "depends_on": ["TWIN-01"], "status": "Backlog"},
        }

    def test_bootstrap_prioritized_over_order(self):
        ctx = ScheduleContext(queue=self.queue, cards=self.cards, completed_tasks={"AUTO-01"})
        next_tasks = self.scheduler.select_next_tasks(ctx)
        self.assertEqual(next_tasks[0], "AUTO-02")

    def test_unmet_dependencies_blocked(self):
        ctx = ScheduleContext(queue=self.queue, cards=self.cards, completed_tasks=set())
        next_tasks = self.scheduler.select_next_tasks(ctx)
        self.assertNotIn("TWIN-01", next_tasks)
        self.assertNotIn("TWIN-02", next_tasks)

    def test_completed_tasks_filtered(self):
        ctx = ScheduleContext(queue=self.queue, cards=self.cards, completed_tasks={"AUTO-01", "AUTO-02"})
        next_tasks = self.scheduler.select_next_tasks(ctx)
        self.assertEqual(next_tasks[0], "TWIN-01")
        self.assertNotIn("AUTO-01", next_tasks)
        self.assertNotIn("AUTO-02", next_tasks)

    def test_blocked_task_filtered(self):
        self.cards["AUTO-02"]["blocked"] = True
        ctx = ScheduleContext(queue=self.queue, cards=self.cards, completed_tasks={"AUTO-01"})
        next_tasks = self.scheduler.select_next_tasks(ctx)
        self.assertNotIn("AUTO-02", next_tasks)

    def test_resource_unavailable_blocked(self):
        mgr = LeaseManager()
        mgr.acquire_lease("TASK-X", "uart", "owner-x")
        card = {"id": "TASK-UART", "task_kind": "impl", "resources": [{"resource": "uart", "exclusive": True}]}
        ok = self.scheduler.check_resource_available(card, mgr)
        self.assertFalse(ok)


class LeaseAndExclusivityTest(unittest.TestCase):
    def setUp(self):
        self.mgr = LeaseManager(max_parallel_impl=2, default_duration=100.0)

    def test_implementation_concurrency_limit(self):
        l1 = self.mgr.acquire_lease("TASK-1", "implementation", "agent-1")
        l2 = self.mgr.acquire_lease("TASK-2", "implementation", "agent-2")
        self.assertTrue(l1.active)
        self.assertTrue(l2.active)
        with self.assertRaises(ResourceConflictError):
            self.mgr.acquire_lease("TASK-3", "implementation", "agent-3")

    def test_exclusive_device_conflict_uart(self):
        l1 = self.mgr.acquire_lease("TASK-1", "uart", "agent-1")
        self.assertTrue(l1.active)
        with self.assertRaises(ResourceConflictError):
            self.mgr.acquire_lease("TASK-2", "uart", "agent-2")

    def test_release_lease_frees_resource(self):
        l1 = self.mgr.acquire_lease("TASK-1", "uart", "agent-1")
        self.mgr.release_lease(l1.lease_id)
        l2 = self.mgr.acquire_lease("TASK-2", "uart", "agent-2")
        self.assertTrue(l2.active)

    def test_lease_expiration_and_prune(self):
        past = time.time() - 200.0
        lease = Lease("l_old", "TASK-OLD", "uart", "agent-old", past, past + 50.0)
        self.mgr.restore_leases([lease])
        self.assertTrue(self.mgr.is_resource_locked("uart", now=past + 10.0))
        pruned = self.mgr.prune_expired_leases(now=past + 100.0)
        self.assertEqual(pruned, 1)
        self.assertFalse(self.mgr.is_resource_locked("uart", now=past + 100.0))

    def test_lease_renewal_and_expired_renewal_fails(self):
        lease = self.mgr.acquire_lease("TASK-1", "resource-a", "agent-1")
        old_expiry = lease.expires_at
        renewed = self.mgr.renew_lease(lease.lease_id, extend_seconds=500.0)
        self.assertEqual(renewed.expires_at, old_expiry + 500.0)
        self.mgr.release_lease(lease.lease_id)
        with self.assertRaises(LeaseExpiredError):
            self.mgr.renew_lease(lease.lease_id)


class StateMachineAndRemediationTest(unittest.TestCase):
    def setUp(self):
        self.sm = CoordStateMachine(max_corrections=2)
        self.record = TaskExecutionRecord(task_id="TEST-01")

    def test_state_machine_positive_flow(self):
        self.sm.transition(self.record, TaskState.READY)
        self.assertEqual(self.record.state, TaskState.READY.value)
        self.sm.transition(self.record, TaskState.IN_PROGRESS)
        self.assertEqual(self.record.state, TaskState.IN_PROGRESS.value)
        self.sm.transition(self.record, TaskState.CANDIDATE_PUSHED)
        self.assertEqual(self.record.state, TaskState.CANDIDATE_PUSHED.value)
        self.sm.transition(self.record, TaskState.SANDBOX_QA)
        self.assertEqual(self.record.state, TaskState.SANDBOX_QA.value)
        self.sm.transition(self.record, TaskState.REVIEW)
        self.assertEqual(self.record.state, TaskState.REVIEW.value)
        self.sm.transition(self.record, TaskState.DONE)
        self.assertEqual(self.record.state, TaskState.DONE.value)

    def test_state_machine_invalid_transition(self):
        with self.assertRaises(StateTransitionError):
            self.sm.transition(self.record, TaskState.DONE)

    def test_candidate_commit_validation(self):
        valid = "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819"
        self.sm.validate_commit_sha(valid)
        for bad in ["not-a-hash", "0" * 40, "f" * 40, ""]:
            with self.assertRaises(GateValidationError):
                self.sm.validate_commit_sha(bad)

    def test_qa_failure_triggers_remediation(self):
        self.record.state = TaskState.SANDBOX_QA.value
        qa_fail = {"passed": False, "summary": "Compilation error"}
        ok = self.sm.validate_qa_verdict(self.record, qa_fail)
        self.assertFalse(ok)
        self.assertEqual(self.record.state, TaskState.IN_PROGRESS.value)
        self.assertEqual(self.record.corrections_count, 1)

    def test_review_rejection_triggers_remediation(self):
        self.record.state = TaskState.REVIEW.value
        review_rej = {"session": "rev-1", "decision": "REJECTED"}
        ok = self.sm.validate_review_verdict(self.record, review_rej, author_session="author-1")
        self.assertFalse(ok)
        self.assertEqual(self.record.state, TaskState.IN_PROGRESS.value)
        self.assertEqual(self.record.corrections_count, 1)

    def test_max_corrections_exceeded_escalation(self):
        self.record.state = TaskState.SANDBOX_QA.value
        qa_fail = {"passed": False, "summary": "Fail 1"}
        self.sm.validate_qa_verdict(self.record, qa_fail)
        self.assertEqual(self.record.corrections_count, 1)
        self.sm.validate_qa_verdict(self.record, {"passed": False, "summary": "Fail 2"})
        self.assertEqual(self.record.corrections_count, 2)
        with self.assertRaises(RemediationLimitExceededError):
            self.sm.validate_qa_verdict(self.record, {"passed": False, "summary": "Fail 3"})
        self.assertEqual(self.record.state, TaskState.ESCALATED.value)

    def test_author_self_review_rejected(self):
        self.record.state = TaskState.REVIEW.value
        review = {"session": "same-session-id", "decision": "APPROVED"}
        with self.assertRaises(GateValidationError):
            self.sm.validate_review_verdict(self.record, review, author_session="same-session-id")

    def test_fake_done_rejected(self):
        card = {"id": "FAKE-DONE", "review_assignments": {}}
        with self.assertRaises(GateValidationError):
            self.sm.validate_done_acceptance(card, Path("."))

    def test_qa_developer_mounts_rejected(self):
        self.record.state = TaskState.SANDBOX_QA.value
        qa_bad = {"passed": True, "developer_mounts": ["/home/user/workspace"]}
        ok = self.sm.validate_qa_verdict(self.record, qa_bad)
        self.assertFalse(ok)
        self.assertEqual(self.record.state, TaskState.IN_PROGRESS.value)


class CheckpointAndRecoveryTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="coord_checkpoint_test_")
        self.base = Path(self.temp_dir.name)
        self.mgr = CheckpointManager()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_checkpoint_roundtrip(self):
        path = self.base / "state.json"
        record = TaskExecutionRecord("AUTO-02", state="InProgress", session_id="sess-1")
        lease = Lease("l1", "AUTO-02", "uart", "sess-1", 100.0, 200.0)
        state = CoordState(
            schema_version=1,
            cursor="AUTO-02",
            in_flight_tasks={"AUTO-02": record},
            completed_tasks=["AUTO-01"],
            leases=[lease],
        )
        self.mgr.save_checkpoint(path, state)
        self.assertTrue(path.is_file())
        loaded = self.mgr.load_checkpoint(path)
        self.assertEqual(loaded.cursor, "AUTO-02")
        self.assertEqual(loaded.completed_tasks, ["AUTO-01"])
        self.assertIn("AUTO-02", loaded.in_flight_tasks)
        self.assertEqual(len(loaded.leases), 1)

    def test_checkpoint_corrupt_defense(self):
        path = self.base / "corrupt.json"
        path.write_text("{broken json here...", encoding="utf-8")
        with self.assertRaises(CheckpointCorruptError):
            self.mgr.load_checkpoint(path)
        path.write_text("{\"no_schema\": 123}", encoding="utf-8")
        with self.assertRaises(CheckpointCorruptError):
            self.mgr.load_checkpoint(path)

    def test_crash_and_restart_recovery_drill(self):
        qfile = self.base / "queue.yaml"
        qfile.write_text("bootstrap: [T1, T2]\norder: []\n", encoding="utf-8")
        cfile = self.base / "coord_state.json"
        cfg = CoordRunnerConfig(workspace_root=self.base, queue_file=qfile, checkpoint_file=cfile)
        r1 = CoordRunner(cfg)
        r1.completed_tasks.add("T1")
        rec = TaskExecutionRecord("T2", state=TaskState.IN_PROGRESS.value, session_id="orig-sess")
        r1.in_flight_tasks["T2"] = rec
        r1.cursor = "T2"
        r1.save_checkpoint()
        r2 = CoordRunner(cfg)
        ok = r2.restore_from_checkpoint()
        self.assertTrue(ok)
        self.assertIn("T1", r2.completed_tasks)
        self.assertIn("T2", r2.in_flight_tasks)
        self.assertEqual(r2.in_flight_tasks["T2"].session_id, "orig-sess")
        self.assertEqual(r2.cursor, "T2")


class ExecutionModesTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="coord_modes_test_")
        self.base = Path(self.temp_dir.name)
        self.qfile = self.base / "queue.yaml"
        self.qfile.write_text("bootstrap: [T1]\norder: []\n", encoding="utf-8")
        self.cfile = self.base / "coord_state.json"
        self.cfg = CoordRunnerConfig(workspace_root=self.base, queue_file=self.qfile, checkpoint_file=self.cfile)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_run_once_mode(self):
        runner = CoordRunner(self.cfg)
        res = runner.run_once()
        self.assertIn("dispatched", res)
        self.assertIn("completed", res)
        self.assertTrue(self.cfile.is_file())

    def test_run_tasks_finite_mode(self):
        runner = CoordRunner(self.cfg)
        cnt = runner.run_tasks(max_tasks=1)
        self.assertEqual(cnt, 1)
        self.assertIn("T1", runner.completed_tasks)
        self.assertTrue(self.cfile.is_file())

    def test_daemon_signal_handling(self):
        runner = CoordRunner(self.cfg)
        runner._running = True
        runner._signal_handler(signal.SIGINT, None)
        self.assertFalse(runner._running)
        self.assertTrue(self.cfile.is_file())


class MethodologicalInvariantsTest(unittest.TestCase):
    def test_python_functions_scale_and_parameters_limits(self):
        this_file = Path(__file__).resolve()
        coord_dir = this_file.parent / "coord_runner"
        files_to_check = [this_file, this_file.parent / "coord_queue.py"]
        files_to_check.extend(coord_dir.glob("*.py"))
        violations = []
        for file_path in files_to_check:
            if not file_path.is_file():
                continue
            tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    lines = node.end_lineno - node.lineno + 1
                    args_count = len(node.args.args) + len(node.args.kwonlyargs)
                    if lines > 50 or args_count > 4:
                        violations.append(
                            f"{file_path.name}:{node.name} (lines={lines}, args={args_count})"
                        )
        self.assertEqual(violations, [], f"Scale or parameter gate violations: {violations}")


if __name__ == "__main__":
    unittest.main()
