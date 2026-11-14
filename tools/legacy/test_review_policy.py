"""版本化 QA 审阅策略解析（legacy 与 streamlined-v1）及包导入路径单元测试。"""

import ast
from pathlib import Path
import subprocess
import sys
import unittest

from coord_runner.review_policy import resolve_review_policy
from coord_runner import CoordStateMachine, GateValidationError


class ReviewPolicyTest(unittest.TestCase):
    def test_legacy_is_retained_without_explicit_migration(self):
        policy = resolve_review_policy({"reviewer": ["QA", "ARCH"]})
        self.assertEqual(policy.roles, ("QA", "ARCH"))
        self.assertTrue(policy.report_review_required)
        self.assertFalse(policy.streamlined)

    def test_streamlined_defaults_to_one_qa_and_retains_explicit_roles(self):
        policy = resolve_review_policy({"qa_policy": "streamlined-v1"})
        self.assertEqual(policy.roles, ("QA",))
        self.assertFalse(policy.report_review_required)
        policy = resolve_review_policy({"qa_policy": "streamlined-v1", "reviewer": ["ENG-MC"]})
        self.assertEqual(policy.roles, ("QA", "ENG-MC"))

    def test_qa_authored_tool_defaults_to_one_non_author_arch_check(self):
        card = {"qa_policy": "streamlined-v1", "executor": {"role": "QA"}}
        self.assertEqual(resolve_review_policy(card).roles, ("ARCH",))
        card["reviewer"] = ["QA", "ENG-MC"]
        self.assertEqual(resolve_review_policy(card).roles, ("QA", "ENG-MC"))

    def test_invalid_policy_or_roles_fail_closed(self):
        for version in [None, "", "future-v2", {}, [], True]:
            with self.subTest(version=version), self.assertRaises(ValueError):
                resolve_review_policy({"qa_policy": version})
        for roles in [["QA", "QA"], [False], {"QA": "session"}]:
            with self.subTest(roles=roles), self.assertRaises(ValueError):
                resolve_review_policy({"qa_policy": "streamlined-v1", "reviewer": roles})

    def test_invalid_policy_is_rejected_before_dispatch(self):
        with self.assertRaises(GateValidationError):
            CoordStateMachine().validate_ready({"qa_policy": "unknown"}, set())

    def test_package_entrypoint_imports_shared_gate_without_tools_path(self):
        control = Path(__file__).resolve().parent.parent
        code = ("from tools.coord_runner.state_machine import CoordStateMachine; "
                "from tools.delivery_checks import check_streamlined_server_qa; "
                "from tools.coord_runner.review_policy import resolve_review_policy; "
                "assert resolve_review_policy({'qa_policy':'streamlined-v1'}).roles == ('QA',)")
        result = subprocess.run([sys.executable, "-c", code], cwd=control, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_new_policy_and_primary_validator_functions_meet_scale_limits(self):
        tools = Path(__file__).resolve().parent
        for name in ["coord_runner/review_policy.py", "delivery_checks.py"]:
            for node in ast.walk(ast.parse((tools / name).read_text())):
                if isinstance(node, ast.FunctionDef):
                    self.assertLessEqual(node.end_lineno - node.lineno + 1, 50, node.name)
                    self.assertLessEqual(len(node.args.args) + len(node.args.kwonlyargs), 4, node.name)
