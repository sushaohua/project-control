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
from unittest.mock import MagicMock, patch

TOOLS_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = TOOLS_DIR.parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from coord_runner import (
    CheckpointCorruptError,
    CheckpointManager,
    CodexReviewAdapter,
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

    def test_qa_verdict_string_false_rejected(self):
        self.record.state = TaskState.SANDBOX_QA.value
        ok = self.sm.validate_qa_verdict(self.record, {"passed": "false"})
        self.assertFalse(ok)
        self.assertEqual(self.record.state, TaskState.IN_PROGRESS.value)

    def test_evidence_based_remediation_validation(self):
        self.sm.handle_remediation(self.record, "err", {"path": "e.log", "sha256": "abc12345"})
        self.assertEqual(self.record.corrections_count, 1)
        with self.assertRaises(GateValidationError):
            self.sm.handle_remediation(self.record, "err", {"path": ""})

    def test_qa_verdict_missing_server_qa_rejected(self):
        self.record.state = TaskState.SANDBOX_QA.value
        self.record.candidate_commit = "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819"
        qa_verdict = {
            "passed": True,
            "candidate_commit": "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819",
        }
        with self.assertRaises(GateValidationError) as ctx:
            self.sm.validate_qa_verdict(self.record, qa_verdict)
        self.assertIn("server_qa", str(ctx.exception))

    def test_qa_verdict_commit_mismatch_rejected(self):
        self.record.state = TaskState.SANDBOX_QA.value
        self.record.candidate_commit = "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819"
        qa_verdict = {
            "passed": True,
            "candidate_commit": "b" * 40,
            "server_qa": {"path": "p", "sha256": "s", "sandbox": {"kind": "container"}},
        }
        with self.assertRaises(GateValidationError) as ctx:
            self.sm.validate_qa_verdict(self.record, qa_verdict)
        self.assertIn("does not match", str(ctx.exception))

    def test_qa_verdict_invalid_sandbox_kind_rejected(self):
        self.record.state = TaskState.SANDBOX_QA.value
        self.record.candidate_commit = "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819"
        qa_verdict = {
            "passed": True,
            "candidate_commit": "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819",
            "server_qa": {"path": "p", "sha256": "s", "sandbox": {"kind": "directory"}},
        }
        with self.assertRaises(GateValidationError) as ctx:
            self.sm.validate_qa_verdict(self.record, qa_verdict)
        self.assertIn("Invalid sandbox kind", str(ctx.exception))


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

    def test_crash_and_restart_recovery_drill_from_disk_sandbox_qa(self):
        qfile = self.base / "queue.yaml"
        qfile.write_text("bootstrap: [T1]\norder: []\n", encoding="utf-8")
        cfile = self.base / "coord_state.json"
        cfg = CoordRunnerConfig(workspace_root=self.base, queue_file=qfile, checkpoint_file=cfile)
        commit = "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819"
        r1 = CoordRunner(cfg)
        r1.in_flight_tasks["T1"] = TaskExecutionRecord(
            task_id="T1", state=TaskState.SANDBOX_QA.value, candidate_commit=commit, session_id="author-s"
        )
        r1.cursor = "T1"
        r1.save_checkpoint()
        del r1

        r2 = CoordRunner(cfg)
        r2.restore_from_checkpoint()
        self.assertIn("T1", r2.in_flight_tasks)
        self.assertEqual(r2.in_flight_tasks["T1"].state, TaskState.SANDBOX_QA.value)
        r2.qa_executor = lambda tid, c: {
            "passed": True,
            "candidate_commit": c,
            "server_qa": {
                "path": "server_qa.json",
                "sha256": "48a0c82dda98bdfc3f008861b9ca94b4832a4b712dd9e917b33a6f24d9e40946",
                "sandbox": {"kind": "container"},
            },
        }
        r2.review_executor = lambda tid, c: {"session": "independent-codex-session", "decision": "APPROVED"}
        card = {"id": "T1", "review_assignments": {"reviewer_sessions": []}}
        state = r2.process_task("T1", card)
        self.assertEqual(state, TaskState.DONE.value)
        self.assertIn("T1", r2.completed_tasks)
        self.assertNotIn("T1", r2.in_flight_tasks)
        r2.save_checkpoint()
        saved_state = self.mgr.load_checkpoint(cfile)
        self.assertIn("T1", saved_state.completed_tasks)


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

    def _setup_mock_executors(self, runner: CoordRunner) -> None:
        commit = "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819"
        runner.agent_executor = lambda tid, r: commit
        runner.qa_executor = lambda tid, c: {
            "passed": True,
            "candidate_commit": c,
            "server_qa": {
                "path": "server_qa.json",
                "sha256": "48a0c82dda98bdfc3f008861b9ca94b4832a4b712dd9e917b33a6f24d9e40946",
                "sandbox": {"kind": "container", "id": "c1"},
            },
        }
        runner.review_executor = lambda tid, c: {"session": f"rev_{tid}", "decision": "APPROVED"}

    def test_production_executors_wiring(self):
        runner = CoordRunner(self.cfg)
        self.assertIsNone(runner.qa_executor)
        self.assertIsNone(runner.review_executor)
        runner.wire_production_executors()
        self.assertEqual(runner.qa_executor, runner.default_qa_executor)
        self.assertEqual(runner.review_executor, runner.default_review_executor)

    def test_missing_executor_fails_closed(self):
        runner = CoordRunner(self.cfg)
        rec = TaskExecutionRecord("T1", state=TaskState.IN_PROGRESS.value)
        runner.in_flight_tasks["T1"] = rec
        with self.assertRaises(CoordRunnerError) as ctx:
            runner.process_task("T1", {"id": "T1"})
        self.assertIn("fail-closed", str(ctx.exception))

    def test_run_once_mode(self):
        runner = CoordRunner(self.cfg)
        self._setup_mock_executors(runner)
        res = runner.run_once()
        self.assertIn("dispatched", res)
        self.assertIn("completed", res)
        self.assertTrue(self.cfile.is_file())

    def test_run_tasks_finite_mode(self):
        runner = CoordRunner(self.cfg)
        self._setup_mock_executors(runner)
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

    def test_uart_conflict_rolls_back_implementation_lease(self):
        runner = CoordRunner(self.cfg)
        runner.lease_mgr.acquire_lease("OTHER", "uart", "other-owner")
        card = {"id": "T1", "task_kind": "implementation", "resources": [{"resource": "uart", "exclusive": True}]}
        with self.assertRaises(ResourceConflictError):
            runner._acquire_task_leases("T1", card)
        self.assertEqual(runner.lease_mgr.count_active_implementation(), 0)

    def test_sandbox_qa_restart_recovery_progresses(self):
        runner = CoordRunner(self.cfg)
        self._setup_mock_executors(runner)
        rec = TaskExecutionRecord("T1", state=TaskState.SANDBOX_QA.value,
                                  candidate_commit="a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819")
        runner.in_flight_tasks["T1"] = rec
        card = {"id": "T1", "review_assignments": {"reviewer_sessions": []}}
        st = runner.process_task("T1", card)
        self.assertEqual(st, TaskState.DONE.value)
        self.assertIn("T1", runner.completed_tasks)


class CodexAndSandboxIsolationGateTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="codex_test_")
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_codex_unavailable_blocked(self):
        adapter = CodexReviewAdapter(codex_bin=self.root / "missing_codex")
        self.assertFalse(adapter.check_availability())
        with self.assertRaises(CoordRunnerError) as ctx:
            adapter.execute_review("prompt", self.root)
        self.assertIn("unavailable", str(ctx.exception))

    def test_codex_auth_failure_blocked(self):
        fake_codex = self.root / "codex"
        fake_codex.write_text("#!/bin/sh\nexit 1\n")
        fake_codex.chmod(0o755)
        adapter = CodexReviewAdapter(codex_bin=fake_codex)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stderr="Authentication error 401", stdout="")
            with self.assertRaises(CoordRunnerError) as ctx:
                adapter.execute_review("prompt", self.root)
            self.assertIn("Authentication error", str(ctx.exception))

    def test_plain_directory_sandbox_rejected(self):
        import delivery_checks as gate
        proof = {
            "task_id": "T1", "task_revision": 1,
            "source": "server-pinned-commits", "fresh_checkout": True,
            "sandbox": {"kind": "remote-runner", "id": "plain_dir", "developer_mounts": []},
            "server_lock": {"path": "lock.json", "sha256": "abc"},
        }
        ref = self.root / "server_qa.json"
        ref.write_text(json.dumps(proof), encoding="utf-8")
        header = {"server_qa": {"path": "server_qa.json", "sha256": "dummy"}}
        with patch("delivery_checks.read_ref", return_value=ref.read_bytes()):
            with self.assertRaises(ValueError) as ctx:
                gate.check_server_qa(header, {"id": "T1", "revision": 1}, self.root)
            self.assertIn("container/vm", str(ctx.exception))

    def test_docker_container_sandbox_passed(self):
        import delivery_checks as gate
        proof = {
            "task_id": "T1", "task_revision": 1,
            "source": "server-pinned-commits", "fresh_checkout": True,
            "sandbox": {"kind": "container", "container_id": "cid123", "image": "ubuntu:20.04", "developer_mounts": []},
            "runtime_log": {"path": "rt.log", "sha256": "a"},
            "checkout_log": {"path": "co.log", "sha256": "b"},
            "server_verdict": {"path": "vd.json", "sha256": "c"},
            "server_lock": {"path": "lk.json", "sha256": "d"},
        }
        lock = {"repositories": [{"name": "repo", "url": "ssh://git@srv/r.git", "ref": "main", "commit": "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819"}]}
        ref = self.root / "server_qa.json"
        ref.write_text(json.dumps(proof), encoding="utf-8")
        header = {"server_qa": {"path": "server_qa.json", "sha256": "dummy"}}
        def fake_read_ref(r, ws):
            if r["path"] == "lk.json": return json.dumps(lock).encode()
            if r["path"] == "server_qa.json": return json.dumps(proof).encode()
            return b"ok"
        with patch("delivery_checks.read_ref", side_effect=fake_read_ref):
            gate.check_server_qa(header, {"id": "T1", "revision": 1}, self.root)


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
