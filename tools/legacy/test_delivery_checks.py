#!/usr/bin/env python3
"""交付证据门禁隔离回归测试固件（仅供门禁逻辑回归验证，非真实 QA 签署凭据）。"""

import ast
import copy
import hashlib
import json
import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml

import check_task_graph as graph
import coord_queue
import delivery_checks as gate
from coord_runner import CoordStateMachine, GateValidationError


class DeliveryChecksTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="delivery-gate-test-")
        self.root = Path(self.temp.name)
        self.artifact = self.ref("candidate.md", b"fixture candidate\n")
        self.card = {"id": "AUTO-TEST", "revision": 2, "owner": "fixture-author",
                     "reviewer": ["QA", "ARCH"], "depends_on": [],
                     "deliverables": {"artifacts": ["candidate.md"]},
                     "review_assignments": {"reviewer_sessions": []}}
        self.proof = self.make_proof()
        self.qa_header = self.make_header("QA", "fixture-qa")
        self.qa_header["server_qa"] = self.json_ref("server-proof.json", self.proof)
        qa = self.entry("QA", "fixture-qa", self.qa_header)
        secondary = self.make_header("ARCH", "fixture-report-reviewer")
        secondary["reviewed_qa_report_sha256"] = qa["report_sha256"]
        secondary_proof = copy.deepcopy(self.proof)
        secondary_proof["sandbox"]["id"] = "fixture-secondary-container"
        secondary["server_qa"] = self.json_ref("secondary-proof.json", secondary_proof)
        qa["report_review"] = self.entry("ARCH", "fixture-report-reviewer", secondary)
        arch = self.entry("ARCH", "fixture-arch", self.make_header("ARCH", "fixture-arch"))
        self.card["review_assignments"]["reviewer_sessions"] = [qa, arch]

    def tearDown(self):
        self.temp.cleanup()

    def ref(self, name, data):
        (self.root / name).write_bytes(data)
        return {"path": name, "sha256": hashlib.sha256(data).hexdigest()}

    def json_ref(self, name, data):
        return self.ref(name, json.dumps(data).encode())

    def make_proof(self):
        return {"task_id": "AUTO-TEST", "task_revision": 2,
                "source": "server-pinned-commits", "fresh_checkout": True,
                "sandbox": {"kind": "container", "id": "fixture-container", "developer_mounts": []},
                "runtime_log": self.ref("runtime.log", b"fixture runtime, not a real sandbox"),
                "checkout_log": self.ref("checkout.log", b"fixture checkout"),
                "server_verdict": self.ref("job.json", b"fixture job, not a live verdict"),
                "server_lock": self.json_ref("lock.json", {"repositories": [{
                    "url": "ssh://fixture.invalid/control.git", "ref": "refs/heads/candidate",
                    "commit": "0123456789abcdef0123456789abcdef01234567"}]})}

    def make_header(self, role, session):
        checks = {key: {"result": "passed", "basis": "isolated test fixture"}
                  for key in ["fact_sources", "protocol_compatibility", "claim_scope", "architecture_completeness"]}
        return {"task_id": "AUTO-TEST", "task_revision": 2, "actual_session": session,
                "reviewer_role": role, "decision": "APPROVED", "content_audit": checks,
                "reviewed_artifact_version": self.artifact["sha256"],
                "reviewed_artifacts": [self.artifact]}

    def entry(self, role, session, header):
        report = "---\n" + yaml.safe_dump(header) + "---\nFixture report, not a real approval.\n"
        ref = self.ref(session + ".md", report.encode())
        return {"role": role, "session": session, "reviewed_task_revision": 2,
                "artifact_version": self.artifact["sha256"],
                "evidence": ref["path"], "report_sha256": ref["sha256"],
                "session_evidence": self.ref(session + ".log", session.encode())}

    def entries(self):
        return self.card["review_assignments"]["reviewer_sessions"]

    def check_proof(self):
        self.qa_header["server_qa"] = self.json_ref("server-proof.json", self.proof)
        gate.check_server_qa(self.qa_header, self.card, self.root)

    def test_complete_recorded_evidence_passes_local_structure_only(self):
        self.assertEqual(gate.closure_errors(self.card, self.root), [])

    def test_role_alias_without_runtime_record_cannot_close(self):
        self.entries()[0].pop("session_evidence")
        self.assertTrue(gate.closure_errors(self.card, self.root))

    def test_missing_required_owner_is_rejected(self):
        self.card["reviewer"].append("ENG-MC")
        self.assertIn("required reviewer roles are missing, duplicated or substituted",
                      gate.closure_errors(self.card, self.root))

    def test_coord_receipt_cannot_substitute_owner_report(self):
        ref = self.ref("coord-receipt.md", b"COORD says all owners passed\n")
        self.entries()[1].update(evidence=ref["path"], report_sha256=ref["sha256"])
        self.assertTrue(any("structured metadata" in e for e in gate.closure_errors(self.card, self.root)))

    def test_artifact_change_invalidates_old_review(self):
        (self.root / "candidate.md").write_bytes(b"different temperature unit\n")
        self.assertTrue(any("SHA256" in e for e in gate.closure_errors(self.card, self.root)))

    def test_current_task_revision_must_match(self):
        self.card["revision"] = 3
        self.assertTrue(gate.closure_errors(self.card, self.root))

    def test_report_cannot_approve_a_different_candidate_version(self):
        self.entries()[1]["artifact_version"] = "different-candidate"
        self.assertTrue(any("candidate version" in e for e in gate.closure_errors(self.card, self.root)))

    def test_report_review_cannot_reuse_qa_sandbox(self):
        self.json_ref("secondary-proof.json", self.proof)
        qa = self.entries()[0]
        header = self.make_header("ARCH", "fixture-report-reviewer")
        header["server_qa"] = self.json_ref("secondary-proof.json", self.proof)
        header["reviewed_qa_report_sha256"] = qa["report_sha256"]
        qa["report_review"] = self.entry("ARCH", "fixture-report-reviewer", header)
        self.assertTrue(any("separate sandbox" in e for e in gate.closure_errors(self.card, self.root)))

    def test_qa_authored_artifact_also_requires_server_sandbox_review(self):
        self.card["executor"] = {"role": "QA"}
        self.card["reviewer"] = ["ARCH"]
        self.card["review_assignments"]["reviewer_sessions"] = [self.entries()[1]]
        self.assertTrue(gate.closure_errors(self.card, self.root))

    def test_qa_report_cannot_self_review(self):
        self.entries()[0]["report_review"]["session"] = "fixture-qa"
        self.assertTrue(any("separate non-author" in e for e in gate.closure_errors(self.card, self.root)))

    def test_secondary_review_must_bind_exact_qa_report(self):
        other = self.make_header("ARCH", "fixture-report-reviewer")
        other["reviewed_qa_report_sha256"] = "a" * 64
        self.entries()[0]["report_review"] = self.entry("ARCH", "fixture-report-reviewer", other)
        self.assertTrue(any("exact QA report" in e for e in gate.closure_errors(self.card, self.root)))

    def test_developer_mount_or_worktree_is_not_a_sandbox(self):
        for field, value in [("kind", "worktree"), ("developer_mounts", ["/developer"] )]:
            with self.subTest(field=field):
                original = copy.deepcopy(self.proof)
                self.proof["sandbox"][field] = value
                with self.assertRaises(ValueError):
                    self.check_proof()
                self.proof = original

    def test_local_source_or_nonfresh_checkout_is_rejected(self):
        for field, value in [("source", "developer-worktree"), ("fresh_checkout", False)]:
            with self.subTest(field=field):
                original = copy.deepcopy(self.proof)
                self.proof[field] = value
                with self.assertRaises(ValueError):
                    self.check_proof()
                self.proof = original

    def test_placeholder_server_commit_is_rejected(self):
        self.proof["server_lock"] = self.json_ref("lock.json", {"repositories": [{
            "url": "ssh://fixture.invalid/repo", "ref": "main", "commit": "0" * 40}]})
        with self.assertRaises(ValueError):
            self.check_proof()

    def test_null_dependency_version_is_a_ready_blocker(self):
        card = {"dependency_conditions": [{"task": "PREV", "accepted_version": None,
                                          "acceptance_evidence": None}]}
        errors = graph._check_dependency_conditions_readiness(card, {"PREV": {"status": "Done"}})
        self.assertIn("PREV accepted deliverable/version is not bound", errors)
        self.assertIn("PREV acceptance evidence path is missing", errors)

    def test_done_label_cannot_release_unverified_twin_input(self):
        card = {"dependency_conditions": [{"task": "TWIN-PREV", "accepted_version": "v1",
                                          "acceptance_evidence": "candidate.md"}]}
        errors = graph._check_dependency_conditions_readiness(
            card, {"TWIN-PREV": {"status": "Done"}}, self.root)
        self.assertTrue(any("closure evidence" in item for item in errors))

    def test_new_functions_keep_scale_and_parameter_limits(self):
        for name in ["delivery_checks.py", "coord_queue.py", "test_delivery_checks.py"]:
            tree = ast.parse((Path(__file__).parent / name).read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.assertLessEqual(node.end_lineno - node.lineno + 1, 50, node.name)
                    self.assertLessEqual(len(node.args.args) + len(node.args.kwonlyargs), 4, node.name)

    def streamline(self, role="QA"):
        self.card.update(qa_policy="streamlined-v1", reviewer=[role],
                         candidate_commit="0123456789abcdef0123456789abcdef01234567",
                         write_scope={"project-control": ["candidate.md"]})
        self.card["verification"] = {"commands": [{"kind": "test", "cwd": ".", "command": "fixture-test",
                                                 "expected": "all pass", "availability": "executable"}]}
        self.proof.update(passed=True, test_results=[{"command": "fixture-test", "subpath": "", "exit_code": "0"}])
        lock = {"repositories": [{"name": "project-control", "url": "ssh://fixture.invalid/control.git",
                 "ref": "main", "commit": self.card["candidate_commit"]}]}
        self.proof["server_lock"] = self.json_ref("lock.json", lock)
        header = self.make_header(role, "fixture-primary")
        header.update(reviewed_artifact_version=self.card["candidate_commit"],
                      server_qa=self.json_ref("server-proof.json", self.proof))
        entry = self.entry(role, "fixture-primary", header)
        entry.update(platform="codex", decision="APPROVED", artifact_version=self.card["candidate_commit"],
                     session_evidence=self.ref("primary.jsonl", json.dumps(
                         {"type": "thread.started", "thread_id": "fixture-primary"}).encode()))
        self.card["review_assignments"]["reviewer_sessions"] = [entry]
        return header

    def test_streamlined_accepts_one_primary_review_in_both_gates(self):
        self.streamline()
        self.assertEqual(gate.closure_errors(self.card, self.root), [])
        CoordStateMachine().validate_done_acceptance(self.card, self.root)
        self.assertNotIn("report_review", self.entries()[0])

    def test_streamlined_qa_author_requires_independent_artifact_check(self):
        self.streamline("ARCH")
        self.card["executor"] = {"role": "QA", "agent_id": "fixture-author"}
        self.assertEqual(gate.closure_errors(self.card, self.root), [])
        self.card["executor"]["agent_id"] = "fixture-primary"
        self.assertTrue(any("own artifact" in error for error in gate.closure_errors(self.card, self.root)))
        with self.assertRaises(GateValidationError):
            CoordStateMachine().validate_done_acceptance(self.card, self.root)

    def test_streamlined_invalid_session_returns_errors_without_crashing(self):
        self.streamline()
        self.entries()[0]["session_evidence"] = self.ref("wrong.jsonl", b"not a Codex event")
        self.assertTrue(any("thread.started" in error for error in gate.closure_errors(self.card, self.root)))

    def test_streamlined_special_owner_remains_required(self):
        self.streamline()
        self.card["reviewer"].append("ENG-MC")
        self.assertTrue(gate.closure_errors(self.card, self.root))
        with self.assertRaises(GateValidationError):
            CoordStateMachine().validate_done_acceptance(self.card, self.root)

    def test_streamlined_wrong_candidate_and_missing_tests_fail_both_gates(self):
        self.streamline()
        self.card["candidate_commit"] = "abcdef0123456789abcdef0123456789abcdef0123"
        self.assertTrue(gate.closure_errors(self.card, self.root))
        with self.assertRaises(GateValidationError):
            CoordStateMachine().validate_done_acceptance(self.card, self.root)
        self.streamline()
        self.proof["test_results"] = []
        header = self.make_header("QA", "fixture-primary")
        header.update(reviewed_artifact_version=self.card["candidate_commit"],
                      server_qa=self.json_ref("server-proof.json", self.proof))
        entry = self.entries()[0]
        ref = self.ref("fixture-primary.md", ("---\n" + yaml.safe_dump(header) + "---\n").encode())
        entry.update(evidence=ref["path"], report_sha256=ref["sha256"])
        self.assertTrue(gate.closure_errors(self.card, self.root))
        with self.assertRaises(GateValidationError):
            CoordStateMachine().validate_done_acceptance(self.card, self.root)


class QueueTest(unittest.TestCase):
    def test_bootstrap_selected_before_business(self):
        cards = {"AUTO-01": {"status": "Backlog"}, "TWIN-01": {"status": "Backlog"}}
        result = coord_queue.next_action({"bootstrap": ["AUTO-01"], "order": ["TWIN-01"]}, cards, Path("."))
        self.assertEqual((result["task"], result["action"]), ("AUTO-01", "prepare-ready"))

    def test_existing_assignment_is_reported_before_new_dispatch(self):
        cards = {"A": {"status": "Backlog"}, "B": {"status": "InProgress"}}
        result = coord_queue.next_action({"order": ["A", "B"]}, cards, Path("."))
        self.assertEqual(result["action"], "resume-existing-assignment")
        self.assertEqual(result["task"], "B")

    def test_duplicate_or_unknown_queue_is_rejected(self):
        for queue in [{"order": ["A", "A"]}, {"order": ["MISSING"]}]:
            with self.assertRaises(ValueError):
                coord_queue.next_action(queue, {"A": {"status": "Backlog"}}, Path("."))


if __name__ == "__main__":
    unittest.main()
