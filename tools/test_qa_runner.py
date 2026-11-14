#!/usr/bin/env python3
"""QA 运行器与容器沙箱隔离机制综合单元测试套件。"""

import ast
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

TOOLS_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = TOOLS_DIR.parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import delivery_checks as gate
from qa_runner.qa_runner import (
    CommandResult,
    GitLabClient,
    QARunner,
    QARunnerError,
    QARunRequest,
    QARunResult,
    RepositoryTarget,
    build_server_lock_data,
    build_server_qa_proof,
    build_server_verdict_data,
    check_ssh_connection,
    compute_file_sha256,
    create_isolated_sandbox,
    parse_command_spec,
    parse_repo_target,
    prepare_sandbox_rule_links,
    run_command_in_sandbox,
    sanitize_path_component,
    validate_commit_sha,
    validate_remote_url,
    validate_sandbox_path,
    validate_sandbox_subpath,
    verify_clean_worktree,
    verify_server_commit,
    write_evidence_bundle,
)
from test_harness.runner import harness_runner


class CommitAndUrlValidationTest(unittest.TestCase):
    def test_validate_commit_sha_positive(self):
        valid = "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819"
        validate_commit_sha(valid)

    def test_validate_commit_sha_negative_format(self):
        invalids = ["", "short", "not-hex-characters-here1234567890abcdef", "a" * 39, "b" * 41]
        for bad in invalids:
            with self.assertRaises(QARunnerError):
                validate_commit_sha(bad)

    def test_validate_commit_sha_placeholder_rejected(self):
        placeholders = ["0" * 40, "f" * 40, "a" * 40]
        for ph in placeholders:
            with self.assertRaises(QARunnerError):
                validate_commit_sha(ph)

    def test_validate_remote_url_positive(self):
        urls = [
            "ssh://git@192.168.77.113:2222/sushaohua/project-control.git",
            "http://192.168.77.113/sushaohua/soc-ap.git",
            "https://gitlab.example.com/team/repo.git",
        ]
        for u in urls:
            self.assertEqual(validate_remote_url(u), u)

    def test_validate_remote_url_negative(self):
        bads = [
            "file:///home/user/workspace/repo",
            "/local/path/repo",
            "https://user:pass@192.168.77.113/repo.git",
            "ftp://192.168.77.113/repo.git",
        ]
        for b in bads:
            with self.assertRaises(QARunnerError):
                validate_remote_url(b)


class ServerVerificationTest(unittest.TestCase):
    def test_gitlab_client_init_requires_token(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(QARunnerError):
                GitLabClient("http://192.168.77.113")

    def test_verify_server_commit_positive(self):
        client = MagicMock()
        sha = "1246ea9cb441d074ea444f53320f5632fefcd503"
        client.get_commit.return_value = {"id": sha, "title": "Commit title"}
        res = verify_server_commit(client, "sushaohua/mcu-p3", sha)
        self.assertEqual(res["id"], sha)

    def test_verify_server_commit_unpushed_rejection(self):
        client = MagicMock()
        sha = "1246ea9cb441d074ea444f53320f5632fefcd503"
        client.get_commit.side_effect = QARunnerError("GitLab API HTTP 404")
        with self.assertRaises(QARunnerError) as ctx:
            verify_server_commit(client, "sushaohua/mcu-p3", sha)
        self.assertIn("unpushed or invalid", str(ctx.exception))

    def test_check_ssh_connection_parsing(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Welcome to GitLab, @sushaohua!", stderr="")
            ok = check_ssh_connection("192.168.77.113", 2222, "git")
            self.assertTrue(ok)


class SandboxIsolationTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="qa_sandbox_test_")
        self.base_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_sanitize_path_component(self):
        self.assertEqual(sanitize_path_component("AUTO-01"), "AUTO-01")
        self.assertEqual(sanitize_path_component("run_01"), "run_01")
        for bad in ["../escape", "a/b", "task*", ""]:
            with self.assertRaises(QARunnerError):
                sanitize_path_component(bad)

    def test_sandbox_path_forbidden_roots(self):
        forbidden = [self.base_dir]
        sub = self.base_dir / "child"
        with self.assertRaises(QARunnerError):
            validate_sandbox_path(sub, forbidden)

    def test_create_isolated_sandbox(self):
        box = create_isolated_sandbox(self.base_dir, "TASK-1", "run-1")
        self.assertTrue(box.is_dir())
        self.assertTrue(box.name.startswith("TASK-1_run-1_"))

    def test_validate_sandbox_subpath_escape(self):
        box = create_isolated_sandbox(self.base_dir, "TASK-2", "run-2")
        safe_child = validate_sandbox_subpath(box, "repo/src")
        self.assertTrue(str(safe_child).startswith(str(box)))
        with self.assertRaises(QARunnerError):
            validate_sandbox_subpath(box, "../../outside")

    def test_verify_clean_worktree_detection(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout=" M dirty_file.cpp\n", stderr="")
            with self.assertRaises(QARunnerError):
                verify_clean_worktree(self.base_dir)

    def test_stop_docker_sandbox_preserves_container_state(self):
        from qa_runner.qa_runner import stop_docker_sandbox
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            stop_docker_sandbox("dummy-cid-12345")
            mock_run.assert_called_once_with(
                ["docker", "stop", "-t", "2", "dummy-cid-12345"],
                text=True, capture_output=True, timeout=30
            )


class CommandAndEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="qa_cmd_test_")
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_run_command_in_sandbox_success(self):
        box = self.root / "sandbox"
        box.mkdir(parents=True, exist_ok=True)
        res = run_command_in_sandbox(box, "echo 'hello qa'")
        self.assertEqual(res.returncode, 0)
        self.assertEqual(res.stdout.strip(), "hello qa")

    def test_run_command_in_sandbox_escape_blocked(self):
        box = self.root / "sandbox"
        box.mkdir(parents=True, exist_ok=True)
        with self.assertRaises(QARunnerError):
            run_command_in_sandbox(box, "ls", subpath="../../")

    def test_parse_helpers(self):
        urls = {"soc-ap": "ssh://git@192.168.77.113:2222/sushaohua/soc-ap.git"}
        sha = "4445c8fedc21bafef5e6c971fcb54cec703f0e71"
        target = parse_repo_target(f"soc-ap={sha}:refs/heads/main", urls)
        self.assertEqual(target.name, "soc-ap")
        self.assertEqual(target.commit, sha)
        self.assertEqual(target.ref, "refs/heads/main")
        spec = parse_command_spec("build:soc-ap:make -j4")
        self.assertEqual(spec["kind"], "build")
        self.assertEqual(spec["subpath"], "soc-ap")
        self.assertEqual(spec["command"], "make -j4")

    def test_repo_default_branch_and_explicit_override(self):
        sha = "1246ea9cb441d074ea444f53320f5632fefcd503"
        urls = {"mcu-p3": "ssh://git@example.com/mcu-p3.git"}
        branches = {"mcu-p3": "feat/soc-debug"}
        target = parse_repo_target(f"mcu-p3={sha}", urls, branches)
        self.assertEqual(build_server_lock_data([target])["repositories"][0]["ref"], "feat/soc-debug")
        target = parse_repo_target(f"mcu-p3={sha}:refs/heads/other", urls, branches)
        self.assertEqual(target.ref, "refs/heads/other")
        with self.assertRaises(QARunnerError):
            parse_repo_target(f"mcu-p3={sha}", urls)

    def test_evidence_bundle_delivery_checks_compatibility(self):
        sha = "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819"
        target = RepositoryTarget("project-control", "ssh://git@192.168.77.113:2222/sushaohua/project-control.git", sha, "refs/heads/main")
        targets = [target]
        lock_data = build_server_lock_data(targets)
        run_res = QARunResult(
            task_id="AUTO-01", task_revision=1, run_id="run_test",
            sandbox_id="sandbox_AUTO-01_run_test", sandbox_path=str(self.root / "sandbox"),
            passed=True, tool_versions={"git": "2.34.1"},
            build_results=[], test_results=[{"command": "test", "exit_code": "0", "output": "ok"}],
            summary="All tests passed",
        )
        logs = {"checkout": "Cloned cleanly", "runtime": "All passed"}
        evidence_dir = self.root / "evidence"
        refs = write_evidence_bundle(evidence_dir, run_res, lock_data, logs)
        self.assertTrue((evidence_dir / "server_qa.json").is_file())
        self.assertTrue((evidence_dir / "server_lock.json").is_file())
        card = {"id": "AUTO-01", "revision": 1}
        qa_header = {"server_qa": {
            "path": str((evidence_dir / "server_qa.json").relative_to(self.root)),
            "sha256": compute_file_sha256(evidence_dir / "server_qa.json"),
        }}
        server_qa_dict = json.loads((evidence_dir / "server_qa.json").read_text(encoding="utf-8"))
        for key in ["server_lock", "checkout_log", "runtime_log", "server_verdict"]:
            abs_p = Path(server_qa_dict[key]["path"])
            server_qa_dict[key]["path"] = str(abs_p.relative_to(self.root))
        (evidence_dir / "server_qa.json").write_text(json.dumps(server_qa_dict), encoding="utf-8")
        qa_header["server_qa"]["sha256"] = compute_file_sha256(evidence_dir / "server_qa.json")
        gate.check_server_qa(qa_header, card, self.root)


class HarnessRunnerTest(unittest.TestCase):
    def test_harness_runner_execution(self):
        here = Path(__file__).resolve().parent
        harness_root = here.parent.parent / "test_harness"
        res = harness_runner.execute_test_command("echo 'unit test'", harness_root)
        self.assertTrue(res.passed)
        self.assertEqual(res.returncode, 0)
        self.assertEqual(res.output, "unit test")

    def test_prepare_sandbox_rule_links(self):
        """校验沙箱内同时存在 agents 与业务仓时正确生成相对规则软链接，且不覆盖已有文件。"""
        with tempfile.TemporaryDirectory(prefix="qa_rule_links_") as td:
            box = Path(td)
            (box / "agents/bootloadermc/.agents/rules").mkdir(parents=True)
            (box / "agents/bootloadermc/AGENTS.md").write_text("# boot mc\n", encoding="utf-8")
            (box / "boot/bootloadermc").mkdir(parents=True)
            (box / "soc-ap").mkdir(parents=True)
            (box / "soc-ap/AGENTS.md").write_text("# keep existing\n", encoding="utf-8")
            (box / "agents/soc-ap/.agents/rules").mkdir(parents=True)
            (box / "agents/soc-ap/AGENTS.md").write_text("# from agents\n", encoding="utf-8")
            cfg = {"rule_sources": {"repo_subdirs": {
                "boot/bootloadermc": "bootloadermc",
                "soc-ap": "soc-ap",
            }}}
            targets = [
                RepositoryTarget("boot/bootloadermc", "ssh://example.invalid/b.git", "a" * 40, "soc_debug"),
                RepositoryTarget("soc-ap", "ssh://example.invalid/s.git", "b" * 40, "main"),
            ]
            prepare_sandbox_rule_links(box, targets, cfg)
            self.assertEqual(os.readlink(box / "boot/bootloadermc/AGENTS.md"),
                             "../../agents/bootloadermc/AGENTS.md")
            self.assertEqual(os.readlink(box / "boot/bootloadermc/.agents"),
                             "../../agents/bootloadermc/.agents")
            self.assertFalse((box / "soc-ap/AGENTS.md").is_symlink())
            self.assertEqual(os.readlink(box / "soc-ap/.agents"), "../agents/soc-ap/.agents")


class MethodologicalInvariantsTest(unittest.TestCase):
    def test_python_functions_scale_and_parameters_limits(self):
        this_file = Path(__file__).resolve()
        files_to_check = [
            this_file.parent / "qa_runner/qa_runner.py",
            this_file,
            this_file.parents[2] / "test_harness/runner/harness_runner.py",
        ]
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
                        violations.append(f"{file_path.name}:{node.name} (lines={lines}, args={args_count})")
        self.assertEqual(violations, [], f"Found function scale or parameter violations: {violations}")


if __name__ == "__main__":
    unittest.main()
