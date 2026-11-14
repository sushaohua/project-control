#!/usr/bin/env python3
"""COORD M2 断点恢复、外部 SQLite 状态存储与五源对账综合测试套件。"""

import ast
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import sqlite3
import subprocess
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
    CasConflictError,
    CoordRunner,
    CoordRunnerConfig,
    CoordRunnerError,
    CoordState,
    FiveSourceReconciler,
    JobLauncher,
    Lease,
    LeaseManager,
    ReconcileReport,
    ReconcileStatus,
    ResourceConflictError,
    RoleJobHandle,
    RoleTaskRequest,
    RoleTaskResult,
    StateStore,
    TaskExecutionRecord,
    TaskState,
    get_proc_starttime,
    is_proc_alive,
    write_atomic_json,
)


class StateStoreAuthoritativeRecoveryTest(unittest.TestCase):
    """P1-05, P1-09, P1-10: Test external SQLite WAL authoritative store and single-instance flock."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="coord_recovery_test_")
        self.base = Path(self.temp_dir.name)
        self.db_path = self.base / "state.sqlite3"
        self.lock_path = self.base / "coord_runner.lock"
        self.store = StateStore(self.db_path, self.lock_path)

    def tearDown(self):
        self.store.close()
        self.temp_dir.cleanup()

    def test_sqlite_wal_mode_and_tables_initialized(self):
        conn = sqlite3.connect(str(self.db_path))
        try:
            journal_mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
            self.assertEqual(journal_mode.lower(), "wal")
            cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = {r[0] for r in cur.fetchall()}
            for expected in {"coord_meta", "in_flight_tasks", "completed_tasks", "leases", "role_jobs"}:
                self.assertIn(expected, tables)
        finally:
            conn.close()

    def test_save_and_restore_coord_state(self):
        tasks = {
            "TASK-01": TaskExecutionRecord("TASK-01", state=TaskState.IN_PROGRESS.value, task_revision=1),
            "TASK-02": TaskExecutionRecord("TASK-02", state=TaskState.READY.value, task_revision=2),
        }
        leases = [
            Lease("lease_01", "TASK-01", "implementation", "owner_1", time.time(), time.time() + 1800, True),
        ]
        state = CoordState(
            schema_version=1,
            cursor="TASK-01",
            in_flight_tasks=tasks,
            completed_tasks=["DONE-01", "DONE-02"],
            leases=leases,
        )
        self.store.save_coord_state(state)
        restored = self.store.load_coord_state()
        self.assertIsNotNone(restored)
        self.assertEqual(restored.cursor, "TASK-01")
        self.assertEqual(restored.completed_tasks, ["DONE-01", "DONE-02"])
        self.assertEqual(len(restored.in_flight_tasks), 2)
        self.assertEqual(restored.in_flight_tasks["TASK-01"].state, TaskState.IN_PROGRESS.value)
        self.assertEqual(len(restored.leases), 1)
        self.assertEqual(restored.leases[0].lease_id, "lease_01")

    def test_single_instance_flock_mutual_exclusion(self):
        self.assertTrue(self.store.acquire_process_lock())
        second_store = StateStore(self.db_path, self.lock_path)
        try:
            with self.assertRaises(ResourceConflictError):
                second_store.acquire_process_lock()
        finally:
            second_store.close()
        self.store.release_process_lock()
        self.assertTrue(second_store.acquire_process_lock())
        second_store.close()

    def test_metadata_and_role_job_persistence(self):
        self.store.set_meta("active_coord_thread_id", "thread_12345")
        self.assertEqual(self.store.get_meta("active_coord_thread_id"), "thread_12345")
        job = {
            "job_id": "job_001", "dispatch_key": "TASK-01:rev1:INTEGRATOR:implement:1",
            "task_id": "TASK-01", "task_revision": 1, "role": "INTEGRATOR",
            "phase": "implement", "status": "RUNNING", "job_dir": str(self.base / "job_001"),
        }
        self.store.save_role_job(job)
        fetched = self.store.get_role_job("job_001")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["dispatch_key"], "TASK-01:rev1:INTEGRATOR:implement:1")
        self.store.update_role_job("job_001", {"status": "COMPLETED", "returncode": 0})
        fetched2 = self.store.get_role_job("job_001")
        self.assertEqual(fetched2["status"], "COMPLETED")
        self.assertEqual(fetched2["returncode"], 0)


class JobLauncherAndPidStarttimeTest(unittest.TestCase):
    """Test non-blocking asynchronous job launcher, PID starttime, and atomic exit_status."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="coord_launcher_test_")
        self.base = Path(self.temp_dir.name)
        self.launcher = JobLauncher(workspace_root=self.base)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_proc_starttime_matches_proc_stat(self):
        pid = os.getpid()
        st = get_proc_starttime(pid)
        self.assertIsNotNone(st)
        self.assertTrue(is_proc_alive(pid, st))
        self.assertFalse(is_proc_alive(pid, "non_matching_starttime_999999"))
        self.assertFalse(is_proc_alive(99999999, st))

    def test_write_atomic_json_guarantees_file_integrity(self):
        target = self.base / "atomic.json"
        payload = {"success": True, "count": 42}
        write_atomic_json(target, payload)
        self.assertTrue(target.is_file())
        data = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(data["count"], 42)

    def test_async_job_launch_creates_pid_and_exit_status(self):
        job_dir = self.base / "job_async_01"
        fast_cmd = [sys.executable, "-c", "import sys, time; sys.stdout.write('hello\\n'); sys.exit(0)"]
        worker_pid = self.launcher.launch_async(job_dir, fast_cmd, "dummy prompt")
        self.assertGreater(worker_pid, 0)
        # Wait up to 5 seconds for background worker to write pid.json and exit_status.json
        for _ in range(50):
            if (job_dir / "exit_status.json").is_file():
                break
            time.sleep(0.1)
        self.launcher.poll_proc(worker_pid)
        self.assertTrue((job_dir / "pid.json").is_file())
        self.assertTrue((job_dir / "exit_status.json").is_file())
        exit_info = json.loads((job_dir / "exit_status.json").read_text(encoding="utf-8"))
        self.assertEqual(exit_info["returncode"], 0)


class FiveSourceReconciliationTest(unittest.TestCase):
    """P1-05, P1-07, P1-09, P1-10, P1-13, P1-20: Five-source anti-duplication and recovery."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="coord_reconcile_test_")
        self.base = Path(self.temp_dir.name)
        self.store = StateStore(self.base / "state.sqlite3", self.base / "coord_runner.lock")
        self.reconciler = FiveSourceReconciler(
            workspace_root=self.base,
            state_store=self.store,
            codex_home=self.base / ".codex",
        )

    def tearDown(self):
        self.store.close()
        self.temp_dir.cleanup()

    def test_reconcile_completed_job_from_exit_status(self):
        job_dir = self.base / "job_comp"
        job_dir.mkdir(parents=True)
        (job_dir / "exit_status.json").write_text(json.dumps({"returncode": 0}), encoding="utf-8")
        events = json.dumps({"type": "session_started", "thread_id": "thread_abc"}) + "\n"
        (job_dir / "codex_events.jsonl").write_text(events, encoding="utf-8")
        rep = self.reconciler.reconcile_job(job_dir, "KEY_01")
        self.assertEqual(rep.status, ReconcileStatus.COMPLETED.value)
        self.assertEqual(rep.returncode, 0)
        self.assertEqual(rep.thread_id, "thread_abc")
        self.assertFalse(rep.reconcile_required)

    def test_reconcile_alive_running_job(self):
        job_dir = self.base / "job_running"
        job_dir.mkdir(parents=True)
        pid = os.getpid()
        st = get_proc_starttime(pid)
        (job_dir / "pid.json").write_text(json.dumps({"pid": pid, "starttime": st}), encoding="utf-8")
        rep = self.reconciler.reconcile_job(job_dir, "KEY_02")
        self.assertEqual(rep.status, ReconcileStatus.RUNNING.value)
        self.assertTrue(rep.alive)

    def test_reconcile_orphan_killed_process_flags_reconcile_required_p1_09(self):
        job_dir = self.base / "job_orphan"
        job_dir.mkdir(parents=True)
        (job_dir / "pid.json").write_text(json.dumps({"pid": 99999999, "starttime": "0"}), encoding="utf-8")
        rep = self.reconciler.reconcile_job(job_dir, "KEY_ORPHAN")
        self.assertEqual(rep.status, ReconcileStatus.RECONCILE_REQUIRED.value)
        self.assertTrue(rep.reconcile_required)
        self.assertFalse(rep.alive)

    def test_protect_active_leases_for_running_processes_p1_10(self):
        lm = LeaseManager(default_duration=1800.0)
        lease = lm.acquire_lease("TASK-ACTIVE", "implementation", "owner_x")
        # Artificially expire lease on paper
        lease.expires_at = time.time() - 10.0
        job_dir = self.base / "job_active_task"
        job_dir.mkdir(parents=True)
        pid = os.getpid()
        st = get_proc_starttime(pid)
        (job_dir / "pid.json").write_text(json.dumps({"pid": pid, "starttime": st}), encoding="utf-8")
        self.store.save_role_job({
            "job_id": "job_active_task", "dispatch_key": "k_active", "task_id": "TASK-ACTIVE",
            "task_revision": 1, "role": "INTEGRATOR", "phase": "implement",
            "status": "RUNNING", "job_dir": str(job_dir),
        })
        protected = self.reconciler.protect_active_leases(lm, self.base)
        self.assertEqual(protected, 1)
        self.assertGreater(lease.expires_at, time.time())

    def test_rescan_idempotence_p1_05(self):
        self.store.set_meta("intake_digest:DEM-001:rev1", "sha_abc123")
        self.assertTrue(self.reconciler.check_intake_idempotence("DEM-001", 1, "sha_abc123"))
        self.assertFalse(self.reconciler.check_intake_idempotence("DEM-001", 1, "sha_different"))
        self.assertFalse(self.reconciler.check_intake_idempotence("DEM-002", 1, "sha_abc123"))

    def test_in_flight_revision_conflict_p1_07(self):
        state = CoordState(schema_version=1, in_flight_tasks={
            "TASK-REVISION": TaskExecutionRecord("TASK-REVISION", state=TaskState.IN_PROGRESS.value, task_revision=1),
        })
        self.store.save_coord_state(state)
        self.assertTrue(self.reconciler.check_in_flight_revision("TASK-REVISION", 2))
        self.assertFalse(self.reconciler.check_in_flight_revision("TASK-REVISION", 1))

    def test_record_revision_conflict_referral_p1_07(self):
        state = CoordState(schema_version=1, in_flight_tasks={
            "TASK-REVISION": TaskExecutionRecord("TASK-REVISION", state=TaskState.IN_PROGRESS.value, task_revision=1),
        })
        self.store.save_coord_state(state)
        self.assertIsNone(self.reconciler.record_revision_conflict_referral("TASK-REVISION", 1))
        self.assertIsNone(self.reconciler.record_revision_conflict_referral("TASK-OTHER", 2))
        ref = self.reconciler.record_revision_conflict_referral("TASK-REVISION", 2)
        self.assertIsNotNone(ref)
        self.assertEqual(ref["action"], "COORDINATOR_REFERRAL")
        self.assertEqual(ref["active_revision"], 1)
        self.assertEqual(ref["incoming_revision"], 2)
        meta_val = self.store.get_meta("referral:TASK-REVISION:rev2")
        self.assertIsNotNone(meta_val)
        self.assertIn('"action": "COORDINATOR_REFERRAL"', meta_val)

    def test_cas_conflict_detection_p1_13(self):
        f = self.base / "card.md"
        f.write_text("original content", encoding="utf-8")
        sha = hashlib.sha256(b"original content").hexdigest()
        self.reconciler.verify_cas_write(f, sha)
        f.write_text("manually edited content", encoding="utf-8")
        with self.assertRaises(CasConflictError):
            self.reconciler.verify_cas_write(f, sha)


class DualTaskParallelConcurrencyTest(unittest.TestCase):
    """P1-08: Test dual-task parallel concurrent advancement without blocking."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="coord_parallel_test_")
        self.base = Path(self.temp_dir.name)
        self.qfile = self.base / "queue.yaml"
        self.qfile.write_text("order: [TASK-A, TASK-B, TASK-C]\n", encoding="utf-8")
        self.cfile = self.base / "coord_state.json"
        self.cfg = CoordRunnerConfig(workspace_root=self.base, queue_file=self.qfile, checkpoint_file=self.cfile)
        self.runner = CoordRunner(self.cfg)

    def tearDown(self):
        self.runner.state_store.close()
        self.temp_dir.cleanup()

    def test_max_parallel_implementation_allows_two_concurrent_tasks(self):
        card_a = {"id": "TASK-A", "depends_on": [], "task_kind": "implementation", "status": "Ready"}
        card_b = {"id": "TASK-B", "depends_on": [], "task_kind": "implementation", "status": "Ready"}
        card_c = {"id": "TASK-C", "depends_on": [], "task_kind": "implementation", "status": "Ready"}
        rec_a = self.runner.dispatch_task("TASK-A", card_a)
        rec_b = self.runner.dispatch_task("TASK-B", card_b)
        self.assertEqual(len(self.runner.in_flight_tasks), 2)
        # Attempting to dispatch a 3rd implementation task hits concurrency limit (max 2)
        with self.assertRaises(ResourceConflictError):
            self.runner.dispatch_task("TASK-C", card_c)
        # Release TASK-A implementation lease, allowing TASK-C to dispatch
        self.runner.lease_mgr.release_task_leases("TASK-A")
        rec_c = self.runner.dispatch_task("TASK-C", card_c)
        self.assertEqual(rec_c.task_id, "TASK-C")


class M2AsyncOrchestrationAndIdempotenceTest(unittest.TestCase):
    """P1-05 & P1-08: Verify intake rescan idempotence and asynchronous non-blocking task execution."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.ws = Path(self.temp_dir.name)
        self.intake = self.ws / "project-control/docs/work_intake"
        self.intake.mkdir(parents=True, exist_ok=True)
        self.qfile = self.ws / "queue.yaml"
        self.qfile.write_text("order: []\n", encoding="utf-8")
        self.cfg = CoordRunnerConfig(
            workspace_root=self.ws,
            intake_root=self.intake,
            queue_file=self.qfile,
            checkpoint_file=self.ws / "coord_state.json",
            state_db_file=self.ws / "state.sqlite3",
            lock_file=self.ws / "coord_runner.lock",
            jobs_dir=self.ws / "jobs",
        )
        self.runner = CoordRunner(self.cfg)

    def tearDown(self):
        self.runner.state_store.close()
        self.temp_dir.cleanup()

    def test_intake_rescan_idempotence_guard_p1_05(self):
        sub_dir = self.intake / "submissions"
        sub_dir.mkdir(parents=True, exist_ok=True)
        (sub_dir / "SUB-01.md").write_text(
            "---\nsubmission_id: SUB-01\nrevision: 1\nsubmitter: sushaohua\n---\n"
            "## 指令 1: 对账机制\n- explicit_demand_id: DEM-01\n- explicit_category_id: FEAT-01\n实现五源对账。\n",
            encoding="utf-8",
        )
        res1 = self.runner.scan_work_intake(persist_ledger=True)
        self.assertEqual(len(res1["generated_files"]), 1)
        self.assertEqual(len(res1["valid_records"]), 1)
        res2 = self.runner.scan_work_intake(persist_ledger=True)
        self.assertEqual(len(res2["generated_files"]), 0)
        self.assertEqual(res2["idempotent_records_count"], 1)
        self.assertEqual(res1["valid_records"], res2["valid_records"])

    def _setup_mock_role_jobs(self, jobs_dir):
        def fake_submit(req, dkey, launcher=None):
            j_dir = jobs_dir / f"job_{req.task_id}"
            j_dir.mkdir(parents=True, exist_ok=True)
            sleep_t = 0.8 if req.task_id == "TASK-LONG" else 0.05
            cmd = [sys.executable, "-c", f"import time, sys; time.sleep({sleep_t}); sys.exit(0)"]
            pid = self.runner.job_launcher.launch_async(j_dir, cmd, req.prompt)
            return RoleJobHandle(job_id=j_dir.name, dispatch_key=dkey, role=req.role,
                                 sandbox_mode="read-only", job_dir=j_dir)
        return fake_submit

    def _setup_mock_review_executors(self, commit):
        self.runner.role_adapter.submit_role_task_async = self._setup_mock_role_jobs(self.runner.config.jobs_dir)
        self.runner.role_adapter.collect_role_result = lambda jid: RoleTaskResult(
            job_id=jid, dispatch_key="k", task_id="T", task_revision=1, role="INTEGRATOR",
            thread_id="th1", actual_model="gpt-6-luna", tokens_used=10, summary="ok",
            candidate_commit=commit, artifacts=[], events_path="", output_payload={},
        )
        self.runner.qa_executor = lambda tid, c: {
            "passed": True, "candidate_commit": c,
            "server_qa": {
                "path": "server_qa.json", "sha256": "48a0c82dda98bdfc3f008861b9ca94b4832a4b712dd9e917b33a6f24d9e40946",
                "sandbox": {"kind": "container", "id": "c1"}, "task_revision": 1,
            },
        }
        rep = self.ws / "qa_review_report.md"
        rep.write_text("# QA Review Report\n", encoding="utf-8")
        r_sha = hashlib.sha256(b"# QA Review Report\n").hexdigest()
        self.runner.review_executor = lambda tid, c, role="QA": {
            "session": f"rev_{tid}_{role if isinstance(role, str) else 'ARCH_REPORT'}",
            "role": role if isinstance(role, str) else role.get("role", "ARCH"),
            "decision": "APPROVED", "report_path": "qa_review_report.md", "report_sha256": r_sha,
        }
        self.runner.state_machine.validate_done_acceptance = lambda c, ws: None

    def test_async_task_advances_while_long_job_running_p1_08(self):
        commit = "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819"
        cards = {
            "TASK-LONG": {"id": "TASK-LONG", "status": "Ready", "task_kind": "implementation", "depends_on": [], "review_assignments": {"reviewer_sessions": []}},
            "TASK-FAST": {"id": "TASK-FAST", "status": "Ready", "task_kind": "implementation", "depends_on": [], "review_assignments": {"reviewer_sessions": []}},
        }
        self.qfile.write_text("order:\n  - TASK-LONG\n  - TASK-FAST\n", encoding="utf-8")
        self.runner.load_cards = lambda: cards
        self.runner._verify_card_approval = lambda tid, c: None
        self._setup_mock_review_executors(commit)
        self.runner.async_role_dispatch = True
        s1 = self.runner.step()
        self.assertEqual(sorted(s1["dispatched"]), ["TASK-FAST", "TASK-LONG"])
        time.sleep(0.15)
        s2 = self.runner.step()
        self.assertIn("TASK-FAST", self.runner.completed_tasks)
        self.assertIn("TASK-LONG", self.runner.in_flight_tasks)
        self.assertEqual(self.runner.in_flight_tasks["TASK-LONG"].state, TaskState.IN_PROGRESS.value)
        time.sleep(0.8)
        s3 = self.runner.step()
        self.assertIn("TASK-LONG", self.runner.completed_tasks)


class ASTScaleAndParameterGateTest(unittest.TestCase):
    """Hard AST gate: verify ALL self-developed Python functions satisfy <=50 lines and <=4 arguments."""

    def test_all_coord_runner_modules_comply_with_ast_standards(self):
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
        self.assertEqual(violations, [], f"AST function gate violations (<=50 lines, <=4 args): {violations}")


if __name__ == "__main__":
    unittest.main()
