#!/usr/bin/env python3
"""Acceptance and unit test suite for M3 systemd user service deployment and P1-14 verification."""

import ast
import configparser
import json
import multiprocessing
import os
from pathlib import Path
import shutil
import signal
import tempfile
import time
import unittest
from typing import Dict, List, Optional, Tuple

from tools.coord_runner.errors import ResourceConflictError
from tools.coord_runner.models import CoordRunnerConfig, CoordState, TaskExecutionRecord, TaskState
from tools.coord_runner.runner import CoordRunner
from tools.coord_runner.service_ctl import (
    DEFAULT_SOURCE_PATH,
    SERVICE_NAME,
    check_user_linger,
    control_service,
    get_service_status,
    install_service,
    uninstall_service,
    verify_crontab_isolation,
)
from tools.coord_runner.state_store import StateStore


def _run_daemon_worker(ws_dir: str, ready_file: str) -> None:
    """Helper worker executing daemon service in a separate OS process for lifecycle testing."""
    ws = Path(ws_dir)
    cfg = CoordRunnerConfig(
        workspace_root=ws,
        intake_root=ws / "intake",
        queue_file=ws / "queue.yaml",
        state_db_file=ws / "state.sqlite3",
        lock_file=ws / "coord_runner.lock",
        checkpoint_file=ws / "checkpoint.json",
        jobs_dir=ws / "jobs",
    )
    runner = CoordRunner(cfg)
    rec = TaskExecutionRecord(
        "TASK-INFLIGHT",
        state=TaskState.IN_PROGRESS.value,
        task_revision=2,
        runtime_context={"async_job_id": "job_daemon_async"},
    )
    runner.in_flight_tasks["TASK-INFLIGHT"] = rec
    runner.completed_tasks.add("TASK-PREV")
    runner.save_checkpoint()
    runner.state_store.save_coord_state(CoordState(
        schema_version=1,
        in_flight_tasks={"TASK-INFLIGHT": rec},
        completed_tasks=["TASK-PREV"],
    ))
    runner.state_store.acquire_process_lock()
    Path(ready_file).write_text("READY", encoding="utf-8")
    runner.run_daemon(poll_interval=0.05)


class MockCommandRunner:
    """Deterministic mock for subprocess systemctl and crontab commands."""

    def __init__(self, crontab_output: Optional[str] = None):
        self.recorded_commands: List[List[str]] = []
        self.default_rc = 0
        self.default_output = "active"
        self.crontab_output = crontab_output or "0,30 * * * * /bin/bash /home/sushaohua/scripts/sync_md.sh\n"

    def __call__(self, cmd: List[str]) -> Tuple[int, str]:
        self.recorded_commands.append(list(cmd))
        if cmd[0] == "crontab":
            return 0, self.crontab_output
        if "is-active" in cmd:
            return 0, "active"
        if "status" in cmd:
            return 0, "Active: active (running)"
        return self.default_rc, self.default_output


class SystemdUnitFileStructureTest(unittest.TestCase):
    """Validate format, sections, and directives of ai-soc-coord-runner.service."""

    def setUp(self):
        self.unit_path = DEFAULT_SOURCE_PATH
        self.assertTrue(self.unit_path.is_file(), f"Service file missing: {self.unit_path}")
        self.content = self.unit_path.read_text(encoding="utf-8")

    def test_required_sections_present(self):
        for sec in ["[Unit]", "[Service]", "[Install]"]:
            self.assertIn(sec, self.content)

    def test_service_exec_and_restart_directives(self):
        self.assertIn("ExecStart=", self.content)
        self.assertIn("python3 -m tools.coord_runner --daemon", self.content)
        self.assertIn("Restart=on-failure", self.content)
        self.assertIn("RestartSec=5s", self.content)

    def test_working_directory_and_environment(self):
        self.assertIn("WorkingDirectory=/home/sushaohua/workspace/ai_soc_project", self.content)
        self.assertIn("PYTHONPATH=/home/sushaohua/workspace/ai_soc_project/project-control", self.content)
        self.assertIn("WantedBy=default.target", self.content)


class ServiceControllerLifecycleTest(unittest.TestCase):
    """Validate service_ctl.py installation, uninstall, actions, and linger status."""

    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.user_systemd_dir = self.tmp_dir / ".config" / "systemd" / "user"

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_install_and_uninstall_lifecycle(self):
        mock_runner = MockCommandRunner()
        inst_res = install_service(dest_dir=self.user_systemd_dir, runner=mock_runner)
        self.assertTrue(inst_res["success"])
        target_file = self.user_systemd_dir / SERVICE_NAME
        self.assertTrue(target_file.is_file())
        self.assertIn(["systemctl", "--user", "daemon-reload"], mock_runner.recorded_commands)

        uninst_res = uninstall_service(dest_dir=self.user_systemd_dir, runner=mock_runner)
        self.assertTrue(uninst_res["success"])
        self.assertFalse(target_file.is_file())
        self.assertIn(["systemctl", "--user", "stop", SERVICE_NAME], mock_runner.recorded_commands)
        self.assertIn(["systemctl", "--user", "disable", SERVICE_NAME], mock_runner.recorded_commands)

    def test_control_service_actions(self):
        mock_runner = MockCommandRunner()
        for act in ["start", "stop", "restart"]:
            res = control_service(act, runner=mock_runner)
            self.assertTrue(res["success"])
            self.assertIn(["systemctl", "--user", act, SERVICE_NAME], mock_runner.recorded_commands)
        res_invalid = control_service("unsupported", runner=mock_runner)
        self.assertFalse(res_invalid["success"])

    def test_get_service_status_installed_and_missing(self):
        mock_runner = MockCommandRunner()
        st_missing = get_service_status(dest_dir=self.user_systemd_dir, runner=mock_runner)
        self.assertFalse(st_missing["installed"])
        install_service(dest_dir=self.user_systemd_dir, runner=mock_runner)
        st_installed = get_service_status(dest_dir=self.user_systemd_dir, runner=mock_runner)
        self.assertTrue(st_installed["installed"])
        self.assertTrue(st_installed["active"])

    def test_check_user_linger_detection(self):
        res = check_user_linger("sushaohua")
        self.assertEqual(res["user"], "sushaohua")
        self.assertTrue(isinstance(res["linger_enabled"], bool))


class CrontabIsolationGateTest(unittest.TestCase):
    """Hard gate: ensure user crontab is never modified and coord_runner does not contaminate cron."""

    def test_real_crontab_isolation(self):
        res = verify_crontab_isolation()
        self.assertTrue(res["crontab_clean"])
        self.assertEqual(len(res.get("forbidden_entries", [])), 0)

    def test_forbidden_crontab_entry_detected(self):
        poisoned = (
            "0,30 * * * * /bin/bash /home/sushaohua/scripts/sync_md.sh\n"
            "* * * * * python3 -m tools.coord_runner\n"
        )
        mock_runner = MockCommandRunner(crontab_output=poisoned)
        res = verify_crontab_isolation(runner=mock_runner)
        self.assertFalse(res["crontab_clean"])
        self.assertEqual(len(res["forbidden_entries"]), 1)
        self.assertIn("coord_runner", res["forbidden_entries"][0])

    def test_crontab_command_failure_reports_not_clean(self):
        def failing_runner(cmd: List[str]) -> Tuple[int, str]:
            return 1, "crontab: must be privileged to use -u / permission denied"
        res = verify_crontab_isolation(runner=failing_runner)
        self.assertFalse(res["crontab_clean"])
        self.assertIn("failed", res.get("error", ""))

    def test_absent_crontab_reports_clean(self):
        def no_crontab_runner(cmd: List[str]) -> Tuple[int, str]:
            return 1, "no crontab for sushaohua"
        res = verify_crontab_isolation(runner=no_crontab_runner)
        self.assertTrue(res["crontab_clean"])
        self.assertEqual(res["active_entries_count"], 0)

    def test_missing_crontab_executable_reports_clean(self):
        def not_found_runner(cmd: List[str]) -> Tuple[int, str]:
            return 1, "[Errno 2] No such file or directory: 'crontab'"
        res = verify_crontab_isolation(runner=not_found_runner)
        self.assertTrue(res["crontab_clean"])
        self.assertEqual(res["active_entries_count"], 0)


class P1_14_ZeroIdleModelConsumptionAndRecoveryTest(unittest.TestCase):
    """P1-14 verification: Zero LLM/model calls on idle cycles and seamless stop/start recovery."""

    def setUp(self):
        self.ws = Path(tempfile.mkdtemp())
        self.intake = self.ws / "intake"
        self.intake.mkdir(parents=True)
        self.qfile = self.ws / "queue.yaml"
        self.qfile.write_text("queue_domain: work_intake\norder: []\n", encoding="utf-8")
        self.state_db = self.ws / "state.sqlite3"
        self.lock = self.ws / "coord_runner.lock"
        self.checkpoint = self.ws / "checkpoint.json"
        self.cfg = CoordRunnerConfig(
            workspace_root=self.ws,
            intake_root=self.intake,
            queue_file=self.qfile,
            state_db_file=self.state_db,
            lock_file=self.lock,
            checkpoint_file=self.checkpoint,
            jobs_dir=self.ws / "jobs",
        )
        self.model_calls = 0

    def tearDown(self):
        shutil.rmtree(self.ws, ignore_errors=True)

    def _spy_agent_executor(self, record: TaskExecutionRecord, card: dict) -> dict:
        self.model_calls += 1
        return {"candidate_commit": "mock_commit"}

    def _spy_qa_executor(self, record: TaskExecutionRecord, card: dict) -> dict:
        self.model_calls += 1
        return {"verdict": "APPROVED"}

    def _spy_reviewer_executor(self, req: dict) -> dict:
        self.model_calls += 1
        return {"decision": "APPROVED"}

    def _build_runner_with_spies(self) -> CoordRunner:
        runner = CoordRunner(self.cfg)
        runner.agent_executor = self._spy_agent_executor
        runner.qa_executor = self._spy_qa_executor
        runner.report_reviewer_executor = self._spy_reviewer_executor
        return runner

    def test_p1_14_zero_idle_model_consumption_across_consecutive_cycles(self):
        runner = self._build_runner_with_spies()
        runner.state_store.acquire_process_lock()
        try:
            for cycle in range(1, 11):
                step_res = runner.step()
                self.assertEqual(len(step_res["dispatched"]), 0, f"Cycle {cycle} dispatched unexpected task")
                self.assertEqual(self.model_calls, 0, f"P1-14 violation: model invoked on idle cycle {cycle}")

            blocked_rec = TaskExecutionRecord("TASK-BLOCKED", state=TaskState.BLOCKED.value, task_revision=1)
            runner.in_flight_tasks["TASK-BLOCKED"] = blocked_rec
            for cycle in range(11, 16):
                runner.step()
                self.assertEqual(self.model_calls, 0, f"P1-14 violation: model invoked on blocked task {cycle}")

            runner.in_flight_tasks.pop("TASK-BLOCKED")
            runner.completed_tasks.add("TASK-DONE-1")
            runner.completed_tasks.add("TASK-DONE-2")
            for cycle in range(16, 21):
                runner.step()
                self.assertEqual(self.model_calls, 0, f"P1-14 violation: model invoked with completed tasks {cycle}")
        finally:
            runner.state_store.release_process_lock()

    def test_service_process_sigterm_stop_and_restart_recovery(self):
        ready_file = self.ws / "daemon_ready.txt"
        proc = multiprocessing.Process(
            target=_run_daemon_worker,
            args=(str(self.ws), str(ready_file)),
        )
        proc.start()
        try:
            for _ in range(50):
                if ready_file.is_file():
                    break
                time.sleep(0.05)
            self.assertTrue(ready_file.is_file(), "Daemon failed to signal readiness")

            runner_probe = CoordRunner(self.cfg)
            with self.assertRaises(ResourceConflictError):
                runner_probe.state_store.acquire_process_lock()

            os.kill(proc.pid, signal.SIGTERM)
            proc.join(timeout=5.0)
            self.assertEqual(proc.exitcode, 0, "Daemon should exit with 0 on SIGTERM")

            runner_restarted = CoordRunner(self.cfg)
            self.assertTrue(runner_restarted.state_store.acquire_process_lock())
            runner_restarted.restore_from_checkpoint()
            self.assertIn("TASK-INFLIGHT", runner_restarted.in_flight_tasks)
            self.assertEqual(runner_restarted.in_flight_tasks["TASK-INFLIGHT"].task_revision, 2)
            self.assertEqual(runner_restarted.in_flight_tasks["TASK-INFLIGHT"].state, TaskState.IN_PROGRESS.value)
            self.assertIn("TASK-PREV", runner_restarted.completed_tasks)
            runner_restarted.state_store.release_process_lock()
        finally:
            if proc.is_alive():
                os.kill(proc.pid, signal.SIGKILL)
                proc.join(timeout=1.0)


class ASTScaleAndParameterGateTest(unittest.TestCase):
    """Hard AST gate: verify ALL self-developed Python functions satisfy <=50 lines and <=4 arguments."""

    def test_systemd_tools_comply_with_ast_standards(self):
        this_file = Path(__file__).resolve()
        service_ctl_file = this_file.parent / "coord_runner" / "service_ctl.py"
        files_to_check = [this_file, service_ctl_file]
        violations = []
        for file_path in files_to_check:
            tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    lines = node.end_lineno - node.lineno + 1
                    args_count = len(node.args.args) + len(node.args.kwonlyargs)
                    if lines > 50 or args_count > 4:
                        violations.append(
                            f"{file_path.name}:{node.name} line {node.lineno}: lines={lines}, args={args_count}"
                        )
        self.assertEqual(violations, [], f"AST scale/parameter violations found: {violations}")


if __name__ == "__main__":
    unittest.main()
