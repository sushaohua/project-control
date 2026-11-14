"""本地编排与确定性 QA 流水线协议回归测试（纯本地模拟，不启动真实 Docker、Codex 或 HIL）。"""

import hashlib
import json
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import yaml

from coord_runner import CoordRunner, CoordRunnerConfig, CoordRunnerError, TaskExecutionRecord, TaskState
from coord_runner.codex_adapter import CodexAuditOptions, CodexReviewAdapter, CodexReviewResult, audit_schema
from qa_runner.qa_runner import QARunResult, write_evidence_bundle


class DeterministicQAPipelineTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="qa_pipeline_test_")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / "author"
        config_dir = self.workspace / "project-control/config/qa_runner"
        config_dir.mkdir(parents=True)
        config_dir.joinpath("default_config.yaml").write_text(yaml.safe_dump({"repositories": {
            "project-control": {"url": "ssh://git@test/control.git", "default_branch": "main"}}}))
        self.sources = self.root / "server_snapshot"
        self.repo = self.sources / "project-control"
        self.repo.mkdir(parents=True)
        self._git(["init", "-q"])
        self._git(["config", "user.email", "fixture@example.invalid"])
        self._git(["config", "user.name", "QA Fixture"])
        self.repo.joinpath("module.txt").write_text("before\n")
        self._git(["add", "."])
        self._git(["commit", "-qm", "base"])
        self.base = self._git(["rev-parse", "HEAD"]).strip()
        self.repo.joinpath("module.txt").write_text("after\n")
        self._git(["commit", "-qam", "candidate"])
        self.commit = self._git(["rev-parse", "HEAD"]).strip()
        self.card = {"id": "AUTO-02", "revision": 2, "reviewer": ["QA", "ARCH"],
                     "write_scope": {"project-control": ["module.txt"]},
                     "source_baseline": {"project-control": self.base}, "base_commit": self.base,
                     "verification": {"commands": [{"id": "unit", "kind": "test", "cwd": ".",
                         "command": "python3 -m unittest", "expected": "checks pass", "availability": "local"}]}}
        self.queue = self.root / "queue.yaml"
        self.queue.write_text("bootstrap: []\norder: []\n")
        self.runner = CoordRunner(CoordRunnerConfig(workspace_root=self.workspace,
            checkpoint_file=self.root / "checkpoint.json", queue_file=self.queue))
        self.runner.wire_production_executors()
        self.record = TaskExecutionRecord("AUTO-02", state=TaskState.CANDIDATE_PUSHED.value,
                                         candidate_commit=self.commit, task_revision=2, session_id="author")
        self.runner.in_flight_tasks[self.record.task_id] = self.record
        self.cards_patch = patch.object(self.runner, "load_cards", return_value={"AUTO-02": self.card})
        self.cards_patch.start()
        self.addCleanup(self.cards_patch.stop)
        self.order = []
        self.process_exit = 0
        self.audit_failure = None
        self.audit_decision = "APPROVED"
        self.audit_missing = []
        self.audit_wrong_candidate = False
        self.created_runs = []

    def _git(self, arguments):
        result = subprocess.run(["git", "-C", str(self.repo)] + arguments,
                                text=True, capture_output=True, check=True)
        return result.stdout

    def _sandbox(self, argv, **kwargs):
        self.order.append("sandbox")
        output = Path(argv[argv.index("--output-dir") + 1])
        self.created_runs.append(output.parent)
        self.addCleanup(shutil.rmtree, output.parent, True)
        request = json.loads((output.parent / "request.json").read_text())
        checks = [{"command": item["command"], "subpath": item["subpath"],
                   "exit_code": str(self.process_exit), "output": "fixture check output"}
                  for item in request["commands"]]
        result = QARunResult(task_id=request["task_id"], task_revision=request["task_revision"],
            run_id="test-run", sandbox_id="fixture-box", sandbox_path=str(self.sources),
            passed=self.process_exit == 0, container_id="c123", test_results=checks,
            container_inspect={"id": "c123456", "image_digest": "sha256:fixture",
                               "mounts": [{"Source": str(self.sources), "RW": False}]})
        write_evidence_bundle(output, result, {"repositories": request["targets"]},
                              {"checkout": "fixture server checkout", "runtime": "fixture check log"})
        return subprocess.CompletedProcess(argv, self.process_exit,
            stdout='progress\n[SERVER QA REF] {\n  "pretty": "JSON"\n}\n', stderr="")

    def _audit(self, prompt, options):
        self.order.append("audit")
        if self.audit_failure:
            raise self.audit_failure
        identity = json.loads(prompt.split("\n", 1)[1])["expected"]
        report = dict(identity, decision=self.audit_decision, summary="fixture audit", findings=[],
                      accepted_scope="software fixture scope", unexecuted=self.audit_missing)
        if self.audit_wrong_candidate:
            report["candidate_commit"] = "0" * 40
        options.artifacts_dir.mkdir(parents=True)
        session = f"fixture-thread-{len(self.order)}"
        raw = json.dumps({"type": "thread.started", "thread_id": session}) + "\n"
        options.artifacts_dir.joinpath("codex.jsonl").write_text(raw)
        options.artifacts_dir.joinpath("final.json").write_text(json.dumps(report))
        return CodexReviewResult(session, "APPROVED", json.dumps(report), 42, raw)

    def _patch_execution(self):
        system_patch = patch("coord_runner.codex_qa.subprocess")
        system = system_patch.start()
        self.addCleanup(system_patch.stop)
        system.TimeoutExpired = subprocess.TimeoutExpired
        system.run.side_effect = self._sandbox
        adapter_patch = patch("coord_runner.runner.CodexReviewAdapter")
        factory = adapter_patch.start()
        self.addCleanup(adapter_patch.stop)
        factory.return_value.default_model = "gpt-6-luna"
        factory.return_value.execute_audit.side_effect = self._audit
        return system, factory

    def test_sandbox_then_independent_readonly_audits_and_bound_reports(self):
        system, factory = self._patch_execution()
        self.runner.step()
        self.assertEqual(self.order, ["sandbox", "audit", "audit", "audit"])
        self.assertEqual(system.run.call_count, 1)
        self.assertEqual(factory.return_value.execute_audit.call_count, 3)
        self.assertIn("AUTO-02", self.runner.completed_tasks)
        sessions = self.card["review_assignments"]["reviewer_sessions"]
        qa = next(item for item in sessions if item["role"] == "QA")
        self.assertTrue(Path(qa["report_path"]).is_file())
        self.assertNotEqual(qa["session"], qa["report_review"]["session"])
        self.assertTrue(Path(qa["report_review"]["review_report_path"]).is_file())
        self.assertIn("+after", next(self.created_runs[0].glob("diffs/*.patch")).read_text())

    def test_streamlined_runs_one_sandbox_and_one_independent_audit(self):
        self.card.update(qa_policy="streamlined-v1", reviewer=["QA"])
        self.card["deliverables"] = {"artifacts": ["project-control/module.txt"]}
        system, factory = self._patch_execution()
        self.runner.step()
        self.assertEqual(self.order, ["sandbox", "audit"])
        self.assertEqual(system.run.call_count, 1)
        self.assertEqual(factory.return_value.execute_audit.call_count, 1)
        self.assertIn("AUTO-02", self.runner.completed_tasks)
        self.assertNotIn("report_review", self.card["review_assignments"]["reviewer_sessions"][0])
        from delivery_checks import closure_errors
        import check_task_graph as graph
        self.card["candidate_commit"] = self.commit
        self.assertEqual(closure_errors(self.card, self.workspace), [])
        self.assertEqual(graph.done_acceptance_errors("AUTO-02", self.card, {}, self.workspace), [])
        self.repo.joinpath("module.txt").write_text("tampered source\n")
        self.assertTrue(closure_errors(self.card, self.workspace))
        with self.assertRaises(Exception):
            self.runner.state_machine.validate_done_acceptance(self.card, self.workspace)

    def test_streamlined_extra_arch_uses_same_completed_sandbox(self):
        self.card["qa_policy"] = "streamlined-v1"
        system, factory = self._patch_execution()
        self.runner.step()
        self.assertEqual(self.order, ["sandbox", "audit", "audit"])
        self.assertEqual(system.run.call_count, 1)
        self.assertEqual(factory.return_value.execute_audit.call_count, 2)
        self.assertIn("AUTO-02", self.runner.completed_tasks)

    def test_streamlined_qa_authored_tool_gets_one_arch_audit(self):
        self.card.update(qa_policy="streamlined-v1", executor={"role": "QA"})
        self.card.pop("reviewer")
        self._patch_execution()
        self.runner.step()
        self.assertEqual(self.order, ["sandbox", "audit"])
        self.assertIn("AUTO-02", self.runner.completed_tasks)
        self.assertEqual(self.card["review_assignments"]["reviewer_sessions"][0]["role"], "ARCH")

    def test_streamlined_resume_uses_completed_facts_and_rejects_tampering(self):
        self.card.update(qa_policy="streamlined-v1", reviewer=["QA"])
        self._patch_execution()
        self.audit_failure = CoordRunnerError("review unavailable")
        self.runner.step()
        self.assertEqual(self.record.state, TaskState.BLOCKED.value)
        self.audit_failure = None
        self.runner.resume_task("AUTO-02")
        self.runner.step()
        self.assertEqual(self.order.count("sandbox"), 1)
        self.assertIn("AUTO-02", self.runner.completed_tasks)

    def test_missing_plan_blocks_before_any_model_or_subprocess(self):
        system, factory = self._patch_execution()
        self.card["verification"]["commands"] = []
        self.runner.step()
        self.assertEqual(self.record.state, TaskState.BLOCKED.value)
        self.assertEqual(self.record.corrections_count, 0)
        system.run.assert_not_called()
        factory.assert_not_called()
        self.assertTrue(self.runner.config.checkpoint_file.is_file())

    def test_failed_objective_checks_are_audited_but_cannot_be_approved(self):
        self.process_exit = 1
        _, factory = self._patch_execution()
        self.runner.step()
        self.assertEqual(self.record.state, TaskState.BLOCKED.value)
        self.assertEqual(self.record.corrections_count, 0)
        factory.return_value.execute_audit.assert_called_once()
        self.assertTrue(self.created_runs[0].joinpath("evidence/server_qa.json").exists())
        self.assertFalse(list(self.created_runs[0].glob("reviews/*/review_report.md")))

    def test_invalid_audit_blocks_persists_and_resume_reuses_test_evidence(self):
        self._patch_execution()
        self.audit_failure = CoordRunnerError("malformed final JSON")
        self.runner.step()
        self.assertEqual(self.record.state, TaskState.BLOCKED.value)
        self.assertEqual(self.record.runtime_context["resume_state"], TaskState.REVIEW.value)
        self.assertEqual(self.record.corrections_count, 0)
        self.runner.restore_from_checkpoint()
        self.record = self.runner.in_flight_tasks["AUTO-02"]
        self.audit_failure = None
        self.runner.resume_task("AUTO-02")
        self.runner.step()
        self.assertEqual(self.order.count("sandbox"), 1)
        self.assertIn("AUTO-02", self.runner.completed_tasks)

    def test_blocked_task_does_not_retry_on_poll(self):
        self._patch_execution()
        self.audit_failure = CoordRunnerError("timeout")
        self.runner.step()
        first = list(self.order)
        self.runner.step()
        self.assertEqual(first, self.order)
        self.assertEqual(self.record.corrections_count, 0)

    def test_finite_mode_returns_when_only_blocked_tasks_remain(self):
        self._patch_execution()
        self.audit_failure = CoordRunnerError("timeout")
        self.assertEqual(self.runner.run_tasks(1), 0)
        self.assertEqual(self.record.state, TaskState.BLOCKED.value)
        self.assertEqual(self.order, ["sandbox", "audit"])

    def test_daemon_survives_task_audit_error(self):
        self._patch_execution()
        self.audit_failure = CoordRunnerError("invalid final result")
        def stop_after_poll(interval):
            self.runner._running = False
        with patch("coord_runner.runner.signal.signal"), patch("coord_runner.runner.time.sleep", side_effect=stop_after_poll):
            self.runner.run_daemon()
        self.assertEqual(self.record.state, TaskState.BLOCKED.value)
        self.assertTrue(self.runner.config.checkpoint_file.is_file())

    def test_hil_requirement_cannot_be_approved_by_software_profile(self):
        self._patch_execution()
        self.card["required_evidence_level"] = "hardware-verified"
        self.runner.step()
        self.assertEqual(self.order, ["sandbox"])
        self.assertEqual(self.record.state, TaskState.BLOCKED.value)
        self.assertIn("HIL", self.record.runtime_context["blocked_reason"])

    def test_missing_cases_and_wrong_candidate_cannot_be_approved(self):
        self._patch_execution()
        self.audit_missing = ["normal connected wizard path"]
        self.runner.step()
        self.assertEqual(self.record.state, TaskState.BLOCKED.value)
        self.audit_missing = []
        self.audit_wrong_candidate = True
        self.runner.resume_task("AUTO-02")
        self.runner.step()
        self.assertEqual(self.record.state, TaskState.BLOCKED.value)
        self.assertEqual(self.record.corrections_count, 0)
        self.assertNotIn("AUTO-02", self.runner.completed_tasks)

    def test_valid_rejection_returns_to_author_with_report_evidence(self):
        self._patch_execution()
        self.process_exit = 1
        self.audit_decision = "REJECTED"
        self.runner.step()
        self.assertEqual(self.record.state, TaskState.IN_PROGRESS.value)
        self.assertEqual(self.record.corrections_count, 1)
        self.assertEqual(len(list(self.created_runs[0].glob("reviews/*/review_report.md"))), 1)

    def test_sandbox_timeout_blocks_without_model_review(self):
        system, factory = self._patch_execution()
        system.run.side_effect = subprocess.TimeoutExpired("qa_runner.py", 1)
        self.runner.step()
        self.assertEqual(self.record.state, TaskState.BLOCKED.value)
        self.assertEqual(self.record.corrections_count, 0)
        factory.assert_not_called()

    def test_exception_does_not_prevent_other_inflight_task(self):
        other = TaskExecutionRecord("NEXT", state=TaskState.IN_PROGRESS.value)
        self.runner.in_flight_tasks["NEXT"] = other
        calls = []
        def process(task_id, card):
            calls.append(task_id)
            if task_id == "AUTO-02":
                raise subprocess.TimeoutExpired("codex", 1)
            other.waiting_events.append("processed")
        with patch.object(self.runner, "process_task", side_effect=process):
            self.runner.step()
        self.assertEqual(calls, ["AUTO-02", "NEXT"])
        self.assertEqual(self.record.state, TaskState.BLOCKED.value)
        self.assertIn("processed", other.waiting_events)

    def test_internal_typeerror_is_not_reinvoked_with_another_signature(self):
        executor = MagicMock(side_effect=TypeError("executor implementation failed"))
        self.runner.qa_executor = executor
        self.runner.step()
        self.assertEqual(executor.call_count, 1)
        self.assertEqual(self.record.state, TaskState.BLOCKED.value)

    def test_tampered_evidence_prevents_resume_from_approving(self):
        self._patch_execution()
        self.audit_failure = CoordRunnerError("timeout")
        self.runner.step()
        self.created_runs[0].joinpath("evidence/runtime.log").write_text("modified")
        self.audit_failure = None
        self.runner.resume_task("AUTO-02")
        self.runner.step()
        self.assertEqual(self.record.state, TaskState.BLOCKED.value)
        self.assertNotIn("AUTO-02", self.runner.completed_tasks)
        self.assertEqual(self.order.count("sandbox"), 1)

    def test_explicit_sandbox_rerun_preserves_previous_evidence(self):
        self._patch_execution()
        self.audit_failure = CoordRunnerError("environment issue")
        self.runner.step()
        original = self.created_runs[0]
        self.audit_failure = None
        self.runner.resume_task("AUTO-02", rerun_sandbox=True)
        self.runner.step()
        self.assertEqual(self.order.count("sandbox"), 2)
        self.assertNotEqual(*self.created_runs)
        self.assertTrue((original / "evidence/server_qa.json").is_file())
        self.assertEqual(self.record.runtime_context["previous_qa_runs"][0]["run_dir"], str(original))
        self.assertIn("AUTO-02", self.runner.completed_tasks)


class CodexAdapterProtocolTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="codex_protocol_fixture_")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.binary = self.root / "fixture-codex"
        self.binary.write_text(f'#!{sys.executable}\n' + '''
import json, sys, pathlib, time
payload = json.load(sys.stdin)
print(json.dumps({"type": "thread.started", "thread_id": "fixture-thread"}), flush=True)
print(json.dumps({"type": "test.argv", "argv": sys.argv}), flush=True)
print(json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "Hello, reviewing."}}), flush=True)
if payload.get("sleep"):
    time.sleep(2)
if payload.get("fail"):
    print("fixture authentication error", file=sys.stderr)
    sys.exit(2)
output = pathlib.Path(sys.argv[sys.argv.index("--output-last-message") + 1])
output.write_text(payload["final"])
print(json.dumps({"type": "turn.completed", "usage": {"input_tokens": 2, "output_tokens": 3}}))
''')
        self.binary.chmod(0o755)
        self.adapter = CodexReviewAdapter(self.binary, "gpt-6-luna", 1)
        self.options = CodexAuditOptions(self.root, self.root / "audit", audit_schema())

    def test_commentary_cannot_corrupt_separate_schema_result(self):
        result = self.adapter.execute_audit(json.dumps({"final": '{"decision":"APPROVED"}'}), self.options)
        self.assertEqual(result.decision, "APPROVED")
        self.assertEqual(result.tokens_used, 5)
        self.assertNotIn("Hello", result.output_text)
        arguments = json.loads(result.raw_log.splitlines()[1])["argv"]
        self.assertEqual(arguments[arguments.index("--sandbox") + 1], "read-only")
        self.assertIn("--output-schema", arguments)

    def test_non_json_final_cannot_approve_and_logs_survive(self):
        with self.assertRaises(CoordRunnerError):
            self.adapter.execute_audit(json.dumps({"final": "NOT APPROVED"}), self.options)
        self.assertTrue(self.options.artifacts_dir.joinpath("codex.jsonl").is_file())
        self.assertEqual(self.options.artifacts_dir.joinpath("final.json").read_text(), "NOT APPROVED")

    def test_fenced_json_is_validated_as_one_document(self):
        result = self.adapter.execute_audit(json.dumps({"final": '```json\n{"decision":"REJECTED"}\n```'}), self.options)
        self.assertEqual(result.decision, "REJECTED")

    def test_timeout_preserves_partial_events_and_error(self):
        self.adapter.timeout_seconds = 0.2
        with self.assertRaises(CoordRunnerError):
            self.adapter.execute_audit(json.dumps({"sleep": True}), self.options)
        self.assertIn("fixture-thread", self.options.artifacts_dir.joinpath("codex.jsonl").read_text())
        self.assertTrue(self.options.artifacts_dir.joinpath("error.txt").is_file())

    def test_failed_process_cannot_fallback_or_approve(self):
        with self.assertRaises(CoordRunnerError):
            self.adapter.execute_audit(json.dumps({"fail": True}), self.options)
        self.assertIn("authentication error", self.options.artifacts_dir.joinpath("codex.stderr").read_text())
        self.assertFalse(self.options.artifacts_dir.joinpath("final.json").exists())


if __name__ == "__main__":
    unittest.main()
