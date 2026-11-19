#!/usr/bin/env python3
"""QA 运行器与容器沙箱隔离机制综合单元测试套件。"""

import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

TOOLS_DIR = Path(__file__).resolve().parent
LEGACY_DIR = TOOLS_DIR / "legacy"
WORKSPACE_ROOT = TOOLS_DIR.parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
# 兼容引用归档至 tools/legacy/ 的旧证据对账辅助模块
if str(LEGACY_DIR) not in sys.path:
    sys.path.insert(0, str(LEGACY_DIR))

import delivery_checks as gate
from qa_runner.qa_runner import (
    _stage_profile_workspace,
    accepted_profile_image,
    CommandResult,
    ContainerCommand,
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
    create_cli_parser,
    create_isolated_sandbox,
    parse_command_spec,
    parse_repo_target,
    prepare_sandbox_rule_links,
    prepare_profile_inputs,
    run_profile_checks,
    run_command_in_sandbox,
    sanitize_path_component,
    start_docker_sandbox,
    system_profile_timeouts,
    validate_commit_sha,
    validate_remote_url,
    validate_sandbox_path,
    validate_sandbox_subpath,
    validate_profile_request,
    verify_clean_worktree,
    verify_remote_ref,
    write_evidence_bundle,
)
from test_harness.runner import harness_runner


class CommitAndUrlValidationTest(unittest.TestCase):
    """核验候选提交和远端 URL 的格式及凭据保护。"""
    def test_validate_commit_sha_positive(self):
        """接受合法的完整提交哈希。"""
        valid = "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819"
        validate_commit_sha(valid)

    def test_validate_commit_sha_negative_format(self):
        """拒绝长度或字符格式错误的提交哈希。"""
        invalids = ["", "short", "not-hex-characters-here1234567890abcdef", "a" * 39, "b" * 41]
        for bad in invalids:
            with self.assertRaises(QARunnerError):
                validate_commit_sha(bad)

    def test_validate_commit_sha_placeholder_rejected(self):
        """拒绝由单一重复字符伪造的占位提交。"""
        placeholders = ["0" * 40, "f" * 40, "a" * 40]
        for ph in placeholders:
            with self.assertRaises(QARunnerError):
                validate_commit_sha(ph)

    def test_validate_remote_url_positive(self):
        """接受受支持协议的无凭据远端 URL。"""
        urls = [
            "ssh://git@192.168.77.79:2222/sushaohua/project-control.git",
            "http://192.168.77.79/sushaohua/soc-ap.git",
            "https://gitlab.example.com/team/repo.git",
        ]
        for u in urls:
            self.assertEqual(validate_remote_url(u), u)

    def test_validate_remote_url_negative(self):
        """拒绝本地路径、明文凭据和不支持协议。"""
        bads = [
            "file:///home/user/workspace/repo",
            "/local/path/repo",
            "https://user:pass@192.168.77.79/repo.git",
            "ftp://192.168.77.79/repo.git",
        ]
        for b in bads:
            with self.assertRaises(QARunnerError):
                validate_remote_url(b)


class ServerVerificationTest(unittest.TestCase):
    """核验纯 Git/SSH 直连认证与远端引用可达性（无 GitLab HTTP API 依赖）。"""
    def test_verify_remote_ref_positive(self):
        """原生 git ls-remote 成功返回远端分支与提交哈希。"""
        sha = "1246ea9cb441d074ea444f53320f5632fefcd503"
        target = RepositoryTarget("mcu-p3", "ssh://git@192.168.77.79:2222/sushaohua/mcu-p3.git",
                                  sha, "feat/soc-debug")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout=f"{sha}\trefs/heads/feat/soc-debug\n", stderr="")
            self.assertEqual(verify_remote_ref(target), sha)
            self.assertEqual(mock_run.call_args.args[0],
                             ["git", "ls-remote", target.url, "refs/heads/feat/soc-debug"])

    def test_verify_remote_ref_missing_rejection(self):
        """远端仓库缺失或引用不存在时必须拒绝并保留原始错误。"""
        sha = "1246ea9cb441d074ea444f53320f5632fefcd503"
        target = RepositoryTarget("mcu-p3", "ssh://git@192.168.77.79:2222/sushaohua/mcu-p3.git",
                                  sha, "refs/heads/missing")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            with self.assertRaisesRegex(QARunnerError, "ref not found"):
                verify_remote_ref(target)

    def test_verify_server_prerequisites_ssh_only(self):
        """服务端前置检查仅执行 SSH 认证，不再依赖 GITLAB_TOKEN 或 HTTP API。"""
        with tempfile.TemporaryDirectory(prefix="qa_ssh_only_") as directory:
            runner = QARunner({"sandbox": {"base_dir": directory},
                               "server": {"ssh_host": "192.168.77.79", "ssh_port": 2222}})
            with patch("qa_runner.qa_runner.check_ssh_connection", return_value=True) as mock_ssh:
                status = runner.verify_server_prerequisites()
            self.assertEqual(status, {"auth_mode": "ssh-git", "ssh_connected": True})
            mock_ssh.assert_called_once()

    def test_check_ssh_connection_parsing(self):
        """从受控 SSH 返回值识别 GitLab 认证结果。"""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Welcome to GitLab, @sushaohua!", stderr="")
            ok = check_ssh_connection("192.168.77.79", 2222, "git")
            self.assertTrue(ok)


class SandboxIsolationTest(unittest.TestCase):
    """核验沙箱路径、工作树与容器保留策略。"""
    def setUp(self):
        """为本测试创建独立临时目录，避免改变项目工作树。"""
        self.temp_dir = tempfile.TemporaryDirectory(prefix="qa_sandbox_test_")
        self.base_dir = Path(self.temp_dir.name)

    def tearDown(self):
        """清理本测试创建的临时目录和资源。"""
        self.temp_dir.cleanup()

    def test_sanitize_path_component(self):
        """接受合法沙箱名称并拒绝路径穿越字符。"""
        self.assertEqual(sanitize_path_component("AUTO-01"), "AUTO-01")
        self.assertEqual(sanitize_path_component("run_01"), "run_01")
        for bad in ["../escape", "a/b", "task*", ""]:
            with self.assertRaises(QARunnerError):
                sanitize_path_component(bad)

    def test_sandbox_path_forbidden_roots(self):
        """拒绝将沙箱创建在开发者工作树内。"""
        forbidden = [self.base_dir]
        sub = self.base_dir / "child"
        with self.assertRaises(QARunnerError):
            validate_sandbox_path(sub, forbidden)

    def test_create_isolated_sandbox(self):
        """隔离沙箱必须创建独立目录并绑定任务前缀。"""
        box = create_isolated_sandbox(self.base_dir, "TASK-1", "run-1")
        self.assertTrue(box.is_dir())
        self.assertTrue(box.name.startswith("TASK-1_run-1_"))

    def test_validate_sandbox_subpath_escape(self):
        """拒绝沙箱内部命令的工作目录越界。"""
        box = create_isolated_sandbox(self.base_dir, "TASK-2", "run-2")
        safe_child = validate_sandbox_subpath(box, "repo/src")
        self.assertTrue(str(safe_child).startswith(str(box)))
        with self.assertRaises(QARunnerError):
            validate_sandbox_subpath(box, "../../outside")

    def test_verify_clean_worktree_detection(self):
        """新检出工作树存在修改时必须报告错误。"""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout=" M dirty_file.cpp\n", stderr="")
            with self.assertRaises(QARunnerError):
                verify_clean_worktree(self.base_dir)

    def test_stop_docker_sandbox_preserves_container_state(self):
        """停止容器时保留退出现场供后续 inspect。"""
        from qa_runner.qa_runner import stop_docker_sandbox
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            stop_docker_sandbox("dummy-cid-12345")
            mock_run.assert_called_once_with(
                ["docker", "stop", "-t", "2", "dummy-cid-12345"],
                text=True, capture_output=True, timeout=30
            )


class CommandAndEvidenceTest(unittest.TestCase):
    """核验命令解析、实际执行与证据格式兼容性。"""
    def setUp(self):
        """为本测试创建独立临时目录，避免改变项目工作树。"""
        self.temp_dir = tempfile.TemporaryDirectory(prefix="qa_cmd_test_")
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        """清理本测试创建的临时目录和资源。"""
        self.temp_dir.cleanup()

    def test_run_command_in_sandbox_success(self):
        """记录实际命令输出与零退出码。"""
        box = self.root / "sandbox"
        box.mkdir(parents=True, exist_ok=True)
        res = run_command_in_sandbox(box, "echo 'hello qa'")
        self.assertEqual(res.returncode, 0)
        self.assertEqual(res.stdout.strip(), "hello qa")

    def test_run_command_in_sandbox_escape_blocked(self):
        """命令工作路径越界时拒绝执行。"""
        box = self.root / "sandbox"
        box.mkdir(parents=True, exist_ok=True)
        with self.assertRaises(QARunnerError):
            run_command_in_sandbox(box, "ls", subpath="../../")

    def test_parse_helpers(self):
        """保持仓库候选和 kind:subpath:command 的准确解析。"""
        urls = {"soc-ap": "ssh://git@192.168.77.79:2222/sushaohua/soc-ap.git"}
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
        """候选必须有明确分支，显式 ref 优先于配置默认值。"""
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
        """生成的证据包必须兼容既有收件检查器。"""
        sha = "a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819"
        target = RepositoryTarget("project-control", "ssh://git@192.168.77.79:2222/sushaohua/project-control.git", sha, "refs/heads/main")
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
    """核验测试仓命令执行和规则链接。"""
    def test_harness_runner_execution(self):
        """测试仓运行器必须保留命令的真实输出与结果。"""
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


class PlatformProfileTest(unittest.TestCase):
    """核对 profile 准入、失败停止与输入来源证据；隔离调用不代表正式 SDK QA。"""

    def _request(self, profile):
        """按 profile 构造明确的四仓候选和构建/测试范围，仅用于准入单测。"""
        sha = "1246ea9cb441d074ea444f53320f5632fefcd503"
        targets = [RepositoryTarget(name, "ssh://example.invalid/" + name + ".git", sha, "main")
                   for name in ("printer-soc", "project-control", "agents", "test_harness")]
        commands = [{"kind": "build", "command": "build-target"},
                    {"kind": "test", "command": "verify-target"}]
        return QARunRequest("PROFILE-01", 1, targets, commands, profile)

    def test_cli_profile_is_explicit(self):
        """命令行默认宿主检查，并能显式选择 ARM 应用范围。"""
        self.assertEqual(create_cli_parser().parse_args([]).profile, "host-software")
        self.assertEqual(create_cli_parser().parse_args(["--profile", "c308l-app"]).profile,
                         "c308l-app")

    def test_host_profile_never_downloads_sdk(self):
        """宿主 profile 不建立平台输入，也不触发 SDK 下载。"""
        request = self._request("host-software")
        with patch("qa_runner.qa_runner._stage_profile_workspace") as stage:
            self.assertEqual(prepare_profile_inputs(Path("unused"), request, {}), {})
        stage.assert_not_called()

    def test_application_requires_all_provenance_repositories(self):
        """缺少规则或测试候选不能进入平台 QA。"""
        request = self._request("c308l-app")
        validate_profile_request(request)
        request.targets = request.targets[:1]
        with self.assertRaises(QARunnerError):
            validate_profile_request(request)

    def test_system_profile_requires_image_command(self):
        """普通应用构建不能冒充完整系统制镜。"""
        request = self._request("c308l-system")
        with self.assertRaisesRegex(QARunnerError, "image"):
            validate_profile_request(request)
        request.commands[0]["kind"] = "image"
        validate_profile_request(request)

    def test_platform_failure_prevents_container_start(self):
        """平台来源核验失败时保留错误，不启动容器或继续测试。"""
        with tempfile.TemporaryDirectory(prefix="qa_profile_") as directory:
            runner = QARunner({"sandbox": {"base_dir": directory,
                                          "image_digest": "sha256:" + "a" * 64}})
            request = self._request("c308l-app")
            with patch.object(runner, "verify_target_commits"), \
                    patch("qa_runner.qa_runner.checkout_remote_repository", return_value="checked"), \
                    patch("qa_runner.qa_runner.prepare_profile_inputs",
                          side_effect=QARunnerError("locked SDK missing")), \
                    patch("qa_runner.qa_runner.start_docker_sandbox") as start:
                with self.assertRaisesRegex(QARunnerError, "locked SDK missing"):
                    runner.execute_run(request)
            start.assert_not_called()

    def test_platform_evidence_preserves_scope_and_lock(self):
        """QA 证据保留构建范围和 SDK 锁来源，不把 profile 名当成 HIL 结论。"""
        result = QARunResult("PROFILE-01", 1, "run", "sandbox", "isolated", True,
                             profile="c308l-app", platform_inputs={"source": "server-reconstructed-sdk"})
        refs = {name: {"path": name, "sha256": "fixture"}
                for name in ("server_lock", "checkout_log", "runtime_log", "server_verdict")}
        proof = build_server_qa_proof(result, refs)
        self.assertEqual(proof["profile"], "c308l-app")
        self.assertEqual(proof["platform_inputs"]["source"], "server-reconstructed-sdk")
        self.assertNotIn("HIL-Verified", json.dumps(proof))

    def test_unknown_repository_has_no_guessed_url(self):
        """SDK 和新应用仓必须显式映射 URL，不从逻辑名猜服务器路径。"""
        sha = "1246ea9cb441d074ea444f53320f5632fefcd503"
        with self.assertRaisesRegex(QARunnerError, "explicitly configured"):
            parse_repo_target("unknown=" + sha + ":refs/heads/main", {})

    def test_target_profile_requires_accepted_image_digest(self):
        """目标验证拒绝浮动镜像标签，宿主 profile 保留既有镜像选择。"""
        request = self._request("c308l-app")
        for value in (None, "qa-sandbox:latest", "sha256:short"):
            with self.assertRaisesRegex(QARunnerError, "image digest"):
                accepted_profile_image(request, {"sandbox": {"image_digest": value}})
        config = {"sandbox": {"image_digest": "sha256:" + "b" * 64}}
        self.assertEqual(accepted_profile_image(request, config), "sha256:" + "b" * 64)

    def test_system_profile_keeps_separate_image_and_sdk_tool_acceptance(self):
        """系统镜像及工具的接受值仅用于系统范围，显式空值拦截加载。"""
        digest = "sha256:" + "c" * 64
        config = {"sandbox": {"image": "legacy", "image_digest": None,
                              "c308l_system_image_digest": digest}}
        self.assertEqual(accepted_profile_image(self._request("c308l-system"), config), digest)
        self.assertEqual(accepted_profile_image(self._request("host-software"), config), "legacy")
        with self.assertRaisesRegex(QARunnerError, "image digest"):
            accepted_profile_image(self._request("c308l-app"), config)
        with tempfile.TemporaryDirectory(prefix="qa_system_tool_acceptance_") as directory:
            sandbox = Path(directory)
            tool_digest = compute_file_sha256(WORKSPACE_ROOT / "tools/sdk_workspace.py")
            config["repo_clients"] = [{"id": "c308l"}]
            config["security"] = {"accepted_sdk_tool_sha256": None,
                                  "accepted_c308l_system_sdk_tool_sha256": tool_digest}
            system = self._request("c308l-system")
            self.assertEqual(_stage_profile_workspace(sandbox, system, config)["sdk_tool_sha256"], tool_digest)
            config["security"]["accepted_c308l_system_sdk_tool_sha256"] = None
            with self.assertRaisesRegex(QARunnerError, "accepted matching SHA256"):
                _stage_profile_workspace(sandbox, system, config)

    def test_system_profile_time_bounds_preserve_partial_output(self):
        """系统允许不同的构建和制镜时限，超时保留原始输出并返回失败。"""
        config = {"timeouts": {"c308l_system": {"build": 1800, "image": 3600, "container": 6900}}}
        self.assertEqual(system_profile_timeouts(config),
                         {"build": 1800, "image": 3600, "test": 300, "container": 6900})
        with tempfile.TemporaryDirectory(prefix="qa_system_timeout_") as directory:
            expired = subprocess.TimeoutExpired(["docker"], 3600, output=b"first output", stderr=b"raw stderr")
            with patch("qa_runner.qa_runner.subprocess.run", side_effect=expired) as run:
                result = run_command_in_sandbox(Path(directory), "make image", "", ContainerCommand("cid", 3600))
            self.assertEqual(run.call_args.kwargs["timeout"], 3600)
            self.assertEqual((result.returncode, result.stdout), (-1, "first output"))
            self.assertIn("raw stderr", result.stderr)
            self.assertIn("3600s", result.stderr)
        for invalid in (0, -1, 7201, True, "unbounded"):
            config["timeouts"]["c308l_system"]["image"] = invalid
            with self.assertRaisesRegex(QARunnerError, "integer seconds"):
                system_profile_timeouts(config)

    def test_sdk_tool_hash_must_be_accepted_before_import(self):
        """缺失或错误的事先接受摘要均阻止写工作区与宿主导入，不能自报当前摘要通过。"""
        with tempfile.TemporaryDirectory(prefix="qa_tool_acceptance_") as directory:
            box = Path(directory)
            config = {"repo_clients": [{"id": "c308l"}]}
            with patch("qa_runner.qa_runner._import_input_tool") as imported:
                for value in (None, "0" * 64):
                    config["security"] = {"accepted_sdk_tool_sha256": value}
                    with self.assertRaisesRegex(QARunnerError, "accepted matching SHA256"):
                        prepare_profile_inputs(box, self._request("c308l-app"), config)
                    self.assertFalse((box / "workspace.json").exists())
                imported.assert_not_called()

    def test_accepted_sdk_tool_bytes_are_copied_without_candidate_execution(self):
        """单测显式接受已知工具字节后，暂存副本必须与事先接受摘要完全一致。"""
        with tempfile.TemporaryDirectory(prefix="qa_accepted_tool_") as directory:
            box = Path(directory)
            trusted = WORKSPACE_ROOT / "tools/sdk_workspace.py"
            expected = compute_file_sha256(trusted)
            config = {"repo_clients": [{"id": "c308l"}],
                      "security": {"accepted_sdk_tool_sha256": expected}}
            result = _stage_profile_workspace(box, self._request("c308l-app"), config)
            self.assertEqual(result["sdk_tool_sha256"], expected)
            self.assertEqual((box / "tools/sdk_workspace.py").read_bytes(), trusted.read_bytes())

    def test_candidate_checker_is_not_imported_during_host_preparation(self):
        """真实候选模块含可见副作用时，宿主准备仍只导入已暂存工具，候选保持未执行。"""
        with tempfile.TemporaryDirectory(prefix="qa_host_candidate_") as directory:
            box = Path(directory)
            (box / "tools").mkdir()
            (box / "tools/sdk_workspace.py").write_text('"""受控输入工具测试夹具。"""\n')
            contract = box / "project-control/contracts/c308l_platform_contract.yaml"
            contract.parent.mkdir(parents=True)
            contract.write_text("schema_version: 1\n")
            checker = box / "test_harness/static_checks/platform/check_platform_inputs.py"
            checker.parent.mkdir(parents=True)
            marker = box / "candidate_executed"
            checker.write_text("from pathlib import Path\nPath(" + repr(str(marker)) + ").touch()\n")
            staged = {"workspace": {"repo_clients": []}, "sdk_tool_sha256": "fixture"}
            with patch("qa_runner.qa_runner._stage_profile_workspace", return_value=staged):
                result = prepare_profile_inputs(box, self._request("c308l-app"), {})
            self.assertFalse(marker.exists())
            self.assertFalse(result["validation"]["passed"])

    def test_platform_check_executes_in_container_and_records_failure(self):
        """容器内检查失败或伪造零退出且无有效证据时，保留输出并阻止后续构建。"""
        with tempfile.TemporaryDirectory(prefix="qa_container_check_") as directory:
            box = Path(directory)
            inputs = {}
            request = self._request("c308l-app")
            for code, stdout in ((1, "raw failure"), (0, "{}")):
                command = CommandResult("checker", "/workspace", code, stdout, "stderr", 0.1)
                with patch("qa_runner.qa_runner.run_command_in_sandbox", return_value=command) as run:
                    result = run_profile_checks(box, request, "real-container-id", inputs)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, stdout)
                self.assertFalse(inputs["validation"]["passed"])
                self.assertEqual(run.call_args.args[-1], "real-container-id")

    def test_container_platform_failure_prevents_build(self):
        """平台校验失败时即使业务命令存在，也不得执行下一条构建。"""
        with tempfile.TemporaryDirectory(prefix="qa_preflight_stop_") as directory:
            box = Path(directory)
            runner = QARunner({"sandbox": {"base_dir": directory}})
            failed = CommandResult("checker", "/workspace", 2, "raw stdout", "raw stderr", 0.1)
            with patch("qa_runner.qa_runner.run_profile_checks", return_value=failed), \
                    patch.object(runner, "_run_sandbox_steps") as build:
                result = runner._run_container_steps(box, self._request("c308l-app"),
                                                     {"cid": "container", "inputs": {}})
            self.assertFalse(result[-1])
            self.assertIn("raw stderr", "\n".join(result[0]))
            build.assert_not_called()

    def test_container_output_mount_is_separate_and_writable(self):
        """构建输出只能写独立目录，受测来源仍按只读挂载；不启动真实 Docker。"""
        with tempfile.TemporaryDirectory(prefix="qa_output_mount_") as directory:
            box = Path(directory) / "source"
            box.mkdir()
            with patch("qa_runner.qa_runner.subprocess.run") as run:
                run.return_value = MagicMock(returncode=0, stdout="container-id", stderr="")
                start_docker_sandbox("check", "accepted-image", box)
            command = run.call_args_list[0].args[0]
            self.assertIn("--init", command)
            self.assertIn(str(box.resolve()) + ":/workspace:ro", command)
            self.assertIn(str(box.with_name("source_output").resolve()) + ":/output:rw", command)

    def test_system_profile_copies_only_its_reconstructed_sdk(self):
        """系统范围先校验再复制 SDK，副本路径和成功状态绑定输入；应用范围不复制。"""
        with tempfile.TemporaryDirectory(prefix="qa_system_copy_") as directory:
            box = Path(directory)
            inputs = {"clients": [{"id": "c308l", "path": "sdk/c308l"}]}
            proof = json.dumps({"passed": True, "scope": "software-inputs", "errors": []})
            checked = CommandResult("checker", "/workspace", 0, proof, "", 0.1)
            copied = CommandResult("copy", "/workspace", 0, "copy stdout", "", 0.1)
            with patch("qa_runner.qa_runner.run_command_in_sandbox",
                       side_effect=[checked, copied]) as run:
                result = run_profile_checks(box, self._request("c308l-system"), "cid", inputs)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(inputs["build_worktrees"], {"c308l": "/output/sdk-worktrees/c308l"})
            self.assertIn("cp -a -- /workspace/sdk/c308l /output/sdk-worktrees/c308l",
                          run.call_args_list[1].args[1])
            self.assertTrue(inputs["validation"]["system_copy_passed"])

    def test_system_build_environment_selects_separate_sdk(self):
        """候选构建只在容器执行，系统命令继承可写 SDK 副本路径，应用命令使用只读 SDK。"""
        with tempfile.TemporaryDirectory(prefix="qa_build_environment_") as directory:
            box = Path(directory)
            runner = QARunner({"sandbox": {"base_dir": directory}})
            inputs = {"clients": [{"id": "c308l", "path": "sdk/c308l"}],
                      "build_worktrees": {"c308l": "/output/sdk-worktrees/c308l"}}
            checked = CommandResult("checker", "/workspace", 0, "{}", "", 0.1)
            for profile, root in (("c308l-system", "/output/sdk-worktrees/c308l"),
                                  ("c308l-app", "/workspace/sdk/c308l")):
                with patch("qa_runner.qa_runner.run_profile_checks", return_value=checked), \
                        patch.object(runner, "_run_sandbox_steps", return_value=([], [], [], True)) as run:
                    runner._run_container_steps(box, self._request(profile), {"cid": "cid", "inputs": inputs})
                self.assertIn("C308L_SDK_ROOT=" + root, run.call_args.args[1].commands[0]["command"])
                self.assertEqual(run.call_args.args[-1], "cid")


class MethodologicalInvariantsTest(unittest.TestCase):
    """通过 AST 核验自研函数规模和参数数目。"""
    def test_python_functions_scale_and_parameters_limits(self):
        """对运行器和测试入口核验函数行数与入参数量。"""
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
