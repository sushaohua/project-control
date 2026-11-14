"""审阅前预检、首审与差异复验提示的聚焦测试。"""

import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from coord_runner import TaskState
from coord_runner.errors import CoordRunnerError
from coord_runner.review_bundle import (
    _prior_review, _validate_declared_run_id, build_reverification_context,
    review_prompt, validate_audit, validate_current_review_inputs,
)
import test_qa_pipeline


class QAReviewEfficiencyTest(unittest.TestCase):
    def test_approved_may_include_nonblocking_recommendation(self):
        result = SimpleNamespace(output_text=json.dumps({
            "task_id": "TASK-1", "task_revision": 2, "candidate_commit": "a" * 40,
            "role": "QA", "decision": "APPROVED", "summary": "通过",
            "findings": ["非阻断建议：补充说明"], "accepted_scope": "全部接受项",
            "unexecuted": [],
        }))
        expected = {"task_id": "TASK-1", "task_revision": 2,
                    "candidate_commit": "a" * 40, "role": "QA"}
        self.assertEqual(validate_audit(result, expected)["decision"], "APPROVED")

    def test_current_card_revision_is_checked_before_freeze(self):
        record = SimpleNamespace(task_id="TASK-1", task_revision=2, candidate_commit="a" * 40)
        card = {"id": "TASK-1", "revision": 1}
        with patch("coord_runner.review_bundle.freeze_review_bundle") as freeze:
            with self.assertRaises(CoordRunnerError):
                validate_current_review_inputs(record, card, {"request": {}})
        freeze.assert_not_called()

    def test_frozen_manifest_and_declared_run_id_are_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory)
            request = {"task_id": "TASK-1", "task_revision": 2,
                       "candidate_commit": "a" * 40, "run_dir": str(run),
                       "contract": {"executor": {"run_id": "author_02"}}}
            manifest = run / "request.json"
            manifest.write_text(json.dumps(request), encoding="utf-8")
            request["request_ref"] = {"path": str(manifest),
                                      "sha256": hashlib.sha256(manifest.read_bytes()).hexdigest()}
            qa_result = {**{key: request[key] for key in
                            ("task_id", "task_revision", "candidate_commit")}, "request": request}
            card = {"id": "TASK-1", "revision": 2,
                    "executor": {"run_id": "author_02"}}
            record = SimpleNamespace(task_id="TASK-1", task_revision=2,
                                     candidate_commit="a" * 40)
            with patch("coord_runner.review_bundle.freeze_review_bundle", return_value={}), \
                    patch("coord_runner.review_bundle.candidate_artifact_refs", return_value=[]):
                self.assertEqual(validate_current_review_inputs(record, card, qa_result), {})
            with self.assertRaises(CoordRunnerError):
                _validate_declared_run_id({"executor": {"run_id": "other"}}, request)

    def test_prompt_separates_first_review_and_recheck(self):
        first = review_prompt({"path": "bundle"}, {}, {})
        self.assertIn("非阻断建议", first)
        self.assertIn("BLOCKED", first)
        self.assertIn("REJECTED", first)
        self.assertIn("source_report 非空", first)
        recheck = review_prompt({"path": "bundle"}, {}, {},
                                {"previous_candidate_commit": "a" * 40,
                                 "this_round_changes": {"diff": {"path": "delta"}}})
        self.assertIn("必要回归证据", recheck)
        self.assertIn("不得把上一候选的通过结论自动带入本轮", recheck)

    def test_prior_report_must_match_current_reviewer_role(self):
        prior = {"reviews": [
            {"role": "ARCH", "report_path": "arch.md", "report_sha256": "a" * 64},
            {"role": "QA", "report_path": "qa.md", "report_sha256": "b" * 64},
        ]}
        self.assertEqual(_prior_review(prior, "ARCH")["report_path"], "arch.md")
        self.assertEqual(_prior_review(prior, "QA")["report_path"], "qa.md")
        self.assertEqual(_prior_review(prior, "ENG"), {})

    def test_no_same_role_history_uses_full_first_review(self):
        result = build_reverification_context(
            {"candidate_commit": "b" * 40},
            [{"candidate_commit": "a" * 40, "reviews": [{"role": "QA"}]}],
            {"request": {"candidate_commit": "b" * 40, "run_dir": "/unused"}}, "ARCH")
        self.assertEqual(result, {})

    def test_same_role_history_without_report_reference_blocks(self):
        with self.assertRaises(CoordRunnerError):
            build_reverification_context(
                {"candidate_commit": "b" * 40},
                [{"candidate_commit": "a" * 40, "reviews": [{"role": "ARCH"}]}],
                {"request": {"candidate_commit": "b" * 40, "run_dir": "/unused"}}, "ARCH")

    def test_real_pipeline_blocks_bad_artifact_and_stale_card_before_model(self):
        for change in ("missing_artifact", "stale_candidate"):
            fixture = test_qa_pipeline.DeterministicQAPipelineTest(
                "test_streamlined_runs_one_sandbox_and_one_independent_audit")
            fixture.setUp()
            try:
                fixture.card.update(qa_policy="streamlined-v1", reviewer=["QA"])
                if change == "missing_artifact":
                    fixture.card["deliverables"] = {"artifacts": ["project-control/missing.txt"]}
                else:
                    fixture.card["candidate_commit"] = "b" * 40
                _, factory = fixture._patch_execution()
                fixture.runner.step()
                self.assertEqual(fixture.record.state, TaskState.BLOCKED.value)
                self.assertEqual(fixture.record.corrections_count, 0)
                factory.return_value.execute_audit.assert_not_called()
            finally:
                fixture.doCleanups()

    def test_reverification_binds_prior_report_hash_and_candidate_delta(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            repo.mkdir()
            self._git(repo, ["init", "-q"])
            self._git(repo, ["config", "user.email", "fixture@example.invalid"])
            self._git(repo, ["config", "user.name", "QA Fixture"])
            source = repo / "module.txt"
            source.write_text("before\n", encoding="utf-8")
            self._git(repo, ["add", "."])
            self._git(repo, ["commit", "-qm", "previous"])
            previous_commit = self._git(repo, ["rev-parse", "HEAD"]).strip()
            source.write_text("after\n", encoding="utf-8")
            self._git(repo, ["commit", "-qam", "candidate"])
            current_commit = self._git(repo, ["rev-parse", "HEAD"]).strip()
            prior_dir = root / "prior"
            prior_dir.mkdir()
            prior_report = prior_dir / "review.md"
            prior_report.write_text("previous review", encoding="utf-8")
            digest = hashlib.sha256(prior_report.read_bytes()).hexdigest()
            run_dir = root / "current"
            run_dir.mkdir()
            previous = {"candidate_commit": previous_commit, "run_dir": str(prior_dir),
                        "reviews": [{"role": "ARCH", "report_path": str(prior_report),
                                     "report_sha256": digest}]}
            qa_result = {"candidate_commit": current_commit}
            bundle = {"request": {"candidate_commit": current_commit, "repository": "repo",
                                   "run_dir": str(run_dir)},
                      "diffs": [{"repository": "repo", "source": str(repo),
                                 "candidate_commit": current_commit}]}
            context = build_reverification_context(qa_result, [previous], bundle, "ARCH")
            self.assertIn("+after", Path(context["this_round_changes"]["diff"]["path"]).read_text())
            self.assertEqual(context["previous_report"]["sha256"], digest)
            self.assertTrue(Path(context["previous_report"]["snapshot"]["path"]).is_file())
            prior_report.write_text("tampered", encoding="utf-8")
            with self.assertRaises(CoordRunnerError):
                build_reverification_context(qa_result, [previous], bundle, "ARCH")

    def _git(self, repo: Path, arguments: list) -> str:
        result = subprocess.run(["git", "-C", str(repo)] + arguments,
                                text=True, capture_output=True, check=True)
        return result.stdout


if __name__ == "__main__":
    unittest.main()
