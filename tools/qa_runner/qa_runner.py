#!/usr/bin/env python3
"""服务端候选版本锁定与隔离沙箱 QA 运行器。

强制保证正式 QA 仅在从 GitLab 服务端全新克隆的隔离沙箱（含只读 Docker 容器）中执行，
严格拒绝本地开发工作树挂载、未提交脏文件及未推送至服务端的提交哈希。
"""

import argparse
from dataclasses import dataclass, field
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Dict, List, Optional
import urllib.error
import urllib.parse
import urllib.request

import yaml


class QARunnerError(Exception):
    """QA 运行器操作异常基类。"""
    pass


@dataclass
class RepositoryTarget:
    """单个待检出仓库的目标版本描述结构体。"""

    name: str
    url: str
    commit: str
    ref: Optional[str] = None


@dataclass
class QARunRequest:
    """一次完整沙箱 QA 执行请求的数据结构。"""

    task_id: str
    task_revision: int
    targets: List[RepositoryTarget]
    commands: List[dict]


@dataclass
class CommandResult:
    """沙箱内单条构建或测试命令的执行结果记录。"""

    command: str
    cwd: str
    returncode: int
    stdout: str
    stderr: str
    duration_seconds: float


@dataclass
class QARunResult:
    """单次沙箱 QA 运行的汇总结论、容器溯源与构建/测试明细结果。"""

    task_id: str
    task_revision: int
    run_id: str
    sandbox_id: str
    sandbox_path: str
    passed: bool
    tool_versions: Dict[str, str] = field(default_factory=dict)
    checkout_records: List[Dict[str, str]] = field(default_factory=list)
    build_results: List[Dict[str, str]] = field(default_factory=list)
    test_results: List[Dict[str, str]] = field(default_factory=list)
    evidence_files: Dict[str, Dict[str, str]] = field(default_factory=dict)
    summary: str = ""
    container_id: str = ""
    container_image: str = "ubuntu:20.04"
    container_inspect: Dict[str, object] = field(default_factory=dict)


def redact_token(text: str) -> str:
    """将文本中可能包含的环境变量 GITLAB_TOKEN 敏感令牌脱敏替换。

    Args:
        text: 原始日志或异常消息字符串。

    Returns:
        str: 脱敏后的安全字符串。
    """
    token = os.environ.get("GITLAB_TOKEN")
    if token and token in text:
        return text.replace(token, "[REDACTED_GITLAB_TOKEN]")
    return text


def compute_bytes_sha256(data: bytes) -> str:
    """计算原始字节流的 64 位小写十六进制 SHA256 摘要。"""
    return hashlib.sha256(data).hexdigest()


def compute_file_sha256(file_path: Path) -> str:
    """计算指定文件的 SHA256 十六进制摘要。"""
    if not file_path.is_file():
        raise QARunnerError(f"Target file does not exist: {file_path}")
    return compute_bytes_sha256(file_path.read_bytes())


def create_evidence_ref(output_path: Path, data: bytes) -> Dict[str, str]:
    """将字节数据写入目标证据路径并返回包含 path 与 sha256 的引用字典。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(data)
    return {
        "path": str(output_path),
        "sha256": compute_bytes_sha256(data),
    }


def validate_commit_sha(commit: str) -> None:
    """校验提交哈希是否为合法的 40 位小写十六进制 SHA-1 且非全同字符占位符。"""
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise QARunnerError(f"Invalid commit SHA format: {commit}")
    if len(set(commit)) <= 1:
        raise QARunnerError(f"Placeholder commit SHA is rejected: {commit}")


def validate_remote_url(url: str) -> str:
    """校验远端仓库 URL 协议合法性，严禁本地 file 协议或内嵌明文凭据。"""
    if not isinstance(url, str):
        raise QARunnerError("Repository URL must be a string")
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme in ("file", "") or not parsed.scheme:
        raise QARunnerError(f"Local file paths or empty schemes disallowed: {url}")
    if parsed.scheme not in ("ssh", "http", "https"):
        raise QARunnerError(f"Disallowed repository URL scheme: {parsed.scheme}")
    if parsed.password or (parsed.scheme in ("http", "https") and parsed.username):
        raise QARunnerError("Repository URL must not contain embedded credentials")
    return url


class GitLabClient:
    """用于远端提交核验与鉴权检查的 GitLab REST API v4 客户端。"""

    def __init__(self, base_url: str, token: Optional[str] = None, timeout: int = 30):
        """初始化 GitLab 客户端并校验基础 URL 与访问令牌。"""
        self.base_url = base_url.rstrip("/")
        parsed = urllib.parse.urlsplit(self.base_url)
        if parsed.scheme not in ("http", "https") or parsed.username or parsed.password:
            raise QARunnerError("GITLAB_URL must be an HTTP(S) URL without credentials")
        self.token = token or os.environ.get("GITLAB_TOKEN")
        if not self.token:
            raise QARunnerError("GITLAB_TOKEN environment variable is required")
        self.timeout = timeout

    def request(self, endpoint: str, method: str = "GET", payload: Optional[dict] = None) -> dict:
        """向 GitLab API v4 端点发起带 PRIVATE-TOKEN 的 HTTP 请求并解析 JSON 响应。"""
        url = f"{self.base_url}/api/v4{endpoint}"
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(
            url,
            data=body,
            headers={"PRIVATE-TOKEN": self.token, "Content-Type": "application/json"},
            method=method,
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = resp.read()
                return json.loads(data.decode("utf-8")) if data else {}
        except urllib.error.HTTPError as err:
            msg = f"GitLab API {endpoint} failed: HTTP {err.code}"
            raise QARunnerError(msg) from err
        except (urllib.error.URLError, OSError) as err:
            msg = redact_token(f"GitLab connection failed: {err}")
            raise QARunnerError(msg) from err

    def check_auth(self) -> dict:
        """验证当前 API Token 鉴权有效性并返回当前用户信息字典。"""
        return self.request("/user")

    def get_commit(self, project_path: str, commit_sha: str) -> dict:
        """查询远端 GitLab 指定项目中的特定 Commit 元数据。"""
        validate_commit_sha(commit_sha)
        encoded = urllib.parse.quote(project_path, safe="")
        endpoint = f"/projects/{encoded}/repository/commits/{commit_sha}"
        return self.request(endpoint)


def check_ssh_connection(host: str, port: int, user: str = "git", timeout: int = 90) -> bool:
    """通过非交互式 SSH 批处理模式验证 GitLab SSH 端口连通性与公钥认证。"""
    cmd = [
        "ssh",
        "-n",
        "-o", "BatchMode=yes",
        "-o", f"ConnectTimeout={timeout}",
        "-p", str(port),
        f"{user}@{host}",
    ]
    try:
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout + 30)
        combined = f"{proc.stdout}\n{proc.stderr}"
        if "Welcome to GitLab" in combined or proc.returncode == 0:
            return True
        raise QARunnerError(f"SSH authentication failed: {proc.stderr.strip() or proc.stdout.strip()}")
    except subprocess.TimeoutExpired as err:
        raise QARunnerError(f"SSH connection to {host}:{port} timed out") from err
    except OSError as err:
        raise QARunnerError(f"SSH invocation failed: {err}") from err


def verify_server_commit(client: GitLabClient, project_path: str, commit: str) -> dict:
    """断言候选 Commit 已真实存在于远端 GitLab 服务端，拒绝未推送的本地哈希。"""
    validate_commit_sha(commit)
    try:
        data = client.get_commit(project_path, commit)
        if not data or data.get("id") != commit:
            raise QARunnerError(f"Commit {commit} mismatch in server response: {data}")
        return data
    except QARunnerError as err:
        if "HTTP 404" in str(err):
            raise QARunnerError(f"Candidate commit {commit} not found on server (unpushed or invalid)")
        raise


def sanitize_path_component(name: str) -> str:
    """清洗单个路径组件名称，拒绝包含路径穿越符（`..`）或非法特殊字符的名称。"""
    if not isinstance(name, str) or not name:
        raise QARunnerError("Path component must be a non-empty string")
    if not re.fullmatch(r"[A-Za-z0-9_\-\.]+", name) or ".." in name:
        raise QARunnerError(f"Illegal characters in path component: {name}")
    return name


def validate_sandbox_path(base_dir: Path, forbidden_roots: Optional[List[Path]] = None) -> Path:
    """校验沙箱根目录安全性，确保其不位于任何禁止挂载的开发者工作树内部。"""
    resolved_base = base_dir.resolve()
    if forbidden_roots:
        for root in forbidden_roots:
            resolved_root = root.resolve()
            if resolved_base == resolved_root or resolved_root in resolved_base.parents:
                raise QARunnerError(f"Sandbox cannot be placed inside developer worktree: {resolved_base}")
    return resolved_base


def create_isolated_sandbox(base_dir: Path, task_id: str, run_id: str) -> Path:
    """为单次 QA 运行创建带 UTC 时间戳与 0700 权限的独立沙箱目录。"""
    safe_task = sanitize_path_component(task_id)
    safe_run = sanitize_path_component(run_id)
    now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    sandbox_name = f"{safe_task}_{safe_run}_{now_str}"
    target = base_dir / sandbox_name
    target.mkdir(parents=True, mode=0o700, exist_ok=False)
    return target


def validate_sandbox_subpath(sandbox_dir: Path, relative_path: str) -> Path:
    """确保相对子路径解析后严格位于当前沙箱根目录边界之内，防止路径逃逸。"""
    if not relative_path:
        return sandbox_dir
    target = (sandbox_dir / relative_path).resolve()
    sandbox_resolved = sandbox_dir.resolve()
    if target != sandbox_resolved and sandbox_resolved not in target.parents:
        raise QARunnerError(f"Sandbox escape detected: {relative_path}")
    return target


def verify_clean_worktree(repo_dir: Path) -> None:
    """核验检出后的 Git 工作树完全干净，不存在任何未提交或未跟踪文件。"""
    cmd = ["git", "-C", str(repo_dir), "status", "--porcelain=v1"]
    res = subprocess.run(cmd, text=True, capture_output=True, timeout=30)
    if res.returncode != 0:
        raise QARunnerError(f"Failed to check git status in {repo_dir}: {res.stderr}")
    if res.stdout.strip():
        raise QARunnerError(f"Dirty files detected in freshly checked out sandbox: {res.stdout.strip()}")


def run_git_command(args: List[str], cwd: Path, timeout: int = 180) -> subprocess.CompletedProcess:
    """在剥离外部 GIT_* 环境变量污染的隔离环境中执行 git 子命令。"""
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(key, None)
    env["GIT_TERMINAL_PROMPT"] = "0"
    env.setdefault("GIT_SSH_COMMAND", "ssh -o BatchMode=yes -o ConnectTimeout=60")
    return subprocess.run(args, cwd=str(cwd), env=env, text=True, capture_output=True, timeout=timeout)


def checkout_remote_repository(sandbox_dir: Path, target: RepositoryTarget, timeout: int = 180) -> str:
    """直接从远端服务器拉取指定 Commit 并强制检出到隔离沙箱子目录，随后验证工作区洁净度。"""
    validate_commit_sha(target.commit)
    validate_remote_url(target.url)
    if not target.ref:
        raise QARunnerError(f"Missing remote ref for {target.name}")
    repo_dir = sandbox_dir / target.name
    repo_dir.mkdir(parents=True, exist_ok=True)
    logs = [f"=== Checkout repository '{target.name}' from {target.url} ==="]
    init_res = run_git_command(["git", "init"], cwd=repo_dir, timeout=timeout)
    logs.append(f"$ git init -> {init_res.returncode}")
    add_res = run_git_command(["git", "remote", "add", "origin", target.url], cwd=repo_dir, timeout=timeout)
    logs.append(f"$ git remote add origin {target.url} -> {add_res.returncode}")
    fetch_cmd = ["git", "fetch", "--depth=50", "origin", target.commit]
    fetch_res = run_git_command(fetch_cmd, cwd=repo_dir, timeout=timeout)
    logs.append(f"$ git fetch origin {target.commit} -> {fetch_res.returncode}\n{fetch_res.stderr.strip()}")
    if fetch_res.returncode != 0:
        if target.ref:
            fetch_ref_cmd = ["git", "fetch", "origin", target.ref]
            fetch_res = run_git_command(fetch_ref_cmd, cwd=repo_dir, timeout=timeout)
            logs.append(f"$ fallback git fetch origin {target.ref} -> {fetch_res.returncode}")
        if fetch_res.returncode != 0:
            raise QARunnerError(f"Fetch failed for {target.name} commit {target.commit}: {fetch_res.stderr}")
    checkout_res = run_git_command(["git", "checkout", "--force", target.commit], cwd=repo_dir, timeout=timeout)
    logs.append(f"$ git checkout {target.commit} -> {checkout_res.returncode}")
    if checkout_res.returncode != 0:
        raise QARunnerError(f"Checkout failed for {target.name}: {checkout_res.stderr}")
    rev_res = run_git_command(["git", "rev-parse", "HEAD"], cwd=repo_dir, timeout=timeout)
    if rev_res.stdout.strip() != target.commit:
        raise QARunnerError(f"Checked out commit mismatch: expected {target.commit}, got {rev_res.stdout.strip()}")
    branch_name = target.ref
    if branch_name.startswith("refs/heads/"):
        branch_name = branch_name[len("refs/heads/"):]
    run_git_command(["git", "update-ref", f"refs/remotes/origin/{branch_name}", target.commit], cwd=repo_dir, timeout=timeout)
    run_git_command(["git", "update-ref", "refs/remotes/origin/HEAD", target.commit], cwd=repo_dir, timeout=timeout)
    verify_clean_worktree(repo_dir)
    return "\n".join(logs)


# 单条沙箱构建或测试命令的默认超时秒数
DEFAULT_CMD_TIMEOUT = 300


def run_command_in_sandbox(sandbox_dir: Path, cmd: str, subpath: str = "",
                           container_id: Optional[str] = None) -> CommandResult:
    """在指定 Docker 容器内或隔离沙箱子目录中执行单条构建/测试命令并记录耗时与退出码。"""
    work_dir = validate_sandbox_subpath(sandbox_dir, subpath)
    start_time = datetime.datetime.now()
    if container_id:
        target_dir = f"/workspace/{subpath}".rstrip("/") if subpath else "/workspace"
        exec_cmd = ["docker", "exec", "-w", target_dir, container_id, "bash", "-c", cmd]
        try:
            proc = subprocess.run(exec_cmd, text=True, capture_output=True, timeout=DEFAULT_CMD_TIMEOUT)
            dur = (datetime.datetime.now() - start_time).total_seconds()
            return CommandResult(command=cmd, cwd=target_dir, returncode=proc.returncode,
                                 stdout=proc.stdout, stderr=proc.stderr, duration_seconds=dur)
        except subprocess.TimeoutExpired:
            dur = (datetime.datetime.now() - start_time).total_seconds()
            return CommandResult(command=cmd, cwd=target_dir, returncode=-1, stdout="",
                                 stderr=f"Command timed out after {DEFAULT_CMD_TIMEOUT}s", duration_seconds=dur)
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(key, None)
    try:
        proc = subprocess.run(cmd, shell=True, cwd=str(work_dir), env=env, text=True,
                              capture_output=True, timeout=DEFAULT_CMD_TIMEOUT)
        dur = (datetime.datetime.now() - start_time).total_seconds()
        return CommandResult(command=cmd, cwd=str(work_dir), returncode=proc.returncode,
                             stdout=proc.stdout, stderr=proc.stderr, duration_seconds=dur)
    except subprocess.TimeoutExpired:
        dur = (datetime.datetime.now() - start_time).total_seconds()
        return CommandResult(command=cmd, cwd=str(work_dir), returncode=-1,
                             stdout="", stderr=f"Command timed out after {DEFAULT_CMD_TIMEOUT}s", duration_seconds=dur)


def collect_tool_versions() -> Dict[str, str]:
    """采集当前运行环境的 git 与 python 工具链版本字符串以供证据溯源。"""
    versions = {}
    for tool, cmd in [("git", ["git", "--version"]), ("python", [sys.executable, "--version"])]:
        try:
            res = subprocess.run(cmd, text=True, capture_output=True, timeout=10)
            versions[tool] = res.stdout.strip() or res.stderr.strip()
        except OSError:
            versions[tool] = "unavailable"
    return versions


def build_server_lock_data(targets: List[RepositoryTarget]) -> dict:
    """根据目标仓库列表构建结构化 server_lock.json 数据字典。"""
    repos = []
    for target in targets:
        validate_commit_sha(target.commit)
        if not target.ref:
            raise QARunnerError(f"Missing remote ref for {target.name}")
        repos.append({
            "name": target.name,
            "url": target.url,
            "ref": target.ref,
            "commit": target.commit,
        })
    return {"repositories": repos}


def build_server_verdict_data(run_result: QARunResult) -> dict:
    """根据沙箱运行结果构建 server_verdict.json 判定字典。"""
    return {
        "task_id": run_result.task_id,
        "task_revision": run_result.task_revision,
        "run_id": run_result.run_id,
        "verdict": "PASSED" if run_result.passed else "FAILED",
        "exit_code": 0 if run_result.passed else 1,
        "summary": run_result.summary,
        "build_count": len(run_result.build_results),
        "test_count": len(run_result.test_results),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }


def build_server_qa_proof(run_result: QARunResult, refs: Dict[str, Dict[str, str]]) -> dict:
    """构造满足 delivery_checks 门禁要求的标准 server_qa.json 证明字典。"""
    cid = run_result.container_id or run_result.sandbox_id
    img = run_result.container_image or "ubuntu:20.04"
    return {
        "task_id": run_result.task_id,
        "task_revision": run_result.task_revision,
        "source": "server-pinned-commits",
        "fresh_checkout": True,
        "sandbox": {
            "kind": "container",
            "container_id": cid,
            "id": run_result.sandbox_id,
            "image": img,
            "path": run_result.sandbox_path,
            "developer_mounts": [],
            "container_inspect": run_result.container_inspect,
        },
        "server_lock": refs["server_lock"],
        "checkout_log": refs["checkout_log"],
        "runtime_log": refs["runtime_log"],
        "server_verdict": refs["server_verdict"],
        "tool_versions": run_result.tool_versions,
        "build_results": run_result.build_results,
        "test_results": run_result.test_results,
        "passed": run_result.passed,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }


def write_evidence_bundle(output_dir: Path, run_result: QARunResult,
                          lock_data: dict, logs: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    """将锁文件、检出日志、运行日志、判定结果及 server_qa 证明写入输出目录并返回引用映射。"""
    output_dir.mkdir(parents=True, exist_ok=True)
    lock_ref = create_evidence_ref(output_dir / "server_lock.json",
                                   json.dumps(lock_data, indent=2).encode("utf-8"))
    checkout_ref = create_evidence_ref(output_dir / "checkout.log",
                                       logs.get("checkout", "").encode("utf-8"))
    runtime_ref = create_evidence_ref(output_dir / "runtime.log",
                                      logs.get("runtime", "").encode("utf-8"))
    verdict_ref = create_evidence_ref(output_dir / "server_verdict.json",
                                      json.dumps(build_server_verdict_data(run_result), indent=2).encode("utf-8"))
    refs = {
        "server_lock": lock_ref,
        "checkout_log": checkout_ref,
        "runtime_log": runtime_ref,
        "server_verdict": verdict_ref,
    }
    proof = build_server_qa_proof(run_result, refs)
    qa_ref = create_evidence_ref(output_dir / "server_qa.json",
                                 json.dumps(proof, indent=2).encode("utf-8"))
    refs["server_qa"] = qa_ref
    return refs


def load_yaml_config(config_path: Path) -> dict:
    """加载并校验 QA Runner 的 YAML 配置文件。"""
    if not config_path.is_file():
        raise QARunnerError(f"Config file not found: {config_path}")
    try:
        content = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        if not isinstance(content, dict):
            raise QARunnerError(f"Config must be a valid mapping: {config_path}")
        return content
    except yaml.YAMLError as err:
        raise QARunnerError(f"Failed to parse config YAML: {err}") from err


def start_docker_sandbox(name: str, image: str, mount_dir: Path, read_only: bool = True) -> str:
    """启动挂载沙箱目录（默认只读 ro）的隔离 Docker 容器并返回 12 位容器 ID。"""
    mode = "ro" if read_only else "rw"
    cmd = [
        "docker", "run", "-d",
        "--name", name,
        "-v", f"{mount_dir.resolve()}:/workspace:{mode}",
        "-w", "/workspace",
        image, "sleep", "3600",
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=30)
    if proc.returncode != 0:
        raise QARunnerError(f"Failed to start Docker sandbox: {proc.stderr.strip()}")
    cid = proc.stdout.strip()[:12]
    subprocess.run(["docker", "exec", cid, "git", "config", "--global", "--add", "safe.directory", "*"],
                   text=True, capture_output=True, timeout=10)
    return cid


def stop_docker_sandbox(container_id: str) -> None:
    """停止指定 Docker 沙箱容器（保留其 exited 状态以供 docker inspect 审计）。"""
    subprocess.run(["docker", "stop", "-t", "2", container_id], text=True, capture_output=True, timeout=30)


def inspect_docker_sandbox(container_id: str) -> dict:
    """执行 docker inspect 提取容器镜像摘要、创建时间、状态与挂载卷列表作为溯源证据。"""
    cmd = ["docker", "inspect", container_id]
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=15)
    if proc.returncode == 0:
        try:
            data = json.loads(proc.stdout)
            if isinstance(data, list) and data:
                entry = data[0]
                return {
                    "id": entry.get("Id", container_id),
                    "image": entry.get("Config", {}).get("Image", ""),
                    "image_digest": entry.get("Image", ""),
                    "created": entry.get("Created", ""),
                    "state": entry.get("State", {}).get("Status", ""),
                    "mounts": entry.get("Mounts", []),
                }
        except json.JSONDecodeError:
            pass
    return {"id": container_id, "status": "inspect-failed"}


class QARunner:
    """统筹远端提交核验、隔离沙箱检出与只读容器测试执行的 QA 核心运行器。"""

    def __init__(self, config: dict, workspace_root: Optional[Path] = None):
        """初始化 QA 运行器，解析服务端地址、超时参数并校验沙箱根路径隔离性。"""
        self.config = config
        self.workspace_root = workspace_root or Path.cwd()
        server_cfg = config.get("server", {})
        self.gitlab_url = server_cfg.get("gitlab_url", "http://192.168.77.113")
        self.ssh_host = server_cfg.get("ssh_host", "192.168.77.113")
        self.ssh_port = server_cfg.get("ssh_port", 2222)
        self.ssh_user = server_cfg.get("ssh_user", "git")
        self.api_timeout = int(server_cfg.get("api_timeout_seconds", 60))
        self.ssh_timeout = int(server_cfg.get("ssh_timeout_seconds", 30))
        sandbox_cfg = config.get("sandbox", {})
        base_dir = Path(sandbox_cfg.get("base_dir", "/tmp/qa_sandboxes"))
        self.sandbox_base = validate_sandbox_path(base_dir, [self.workspace_root])
        self.gitlab = GitLabClient(self.gitlab_url, timeout=self.api_timeout)

    def verify_server_prerequisites(self) -> dict:
        """同时核验 GitLab REST API 令牌认证与 SSH 端口连通性。"""
        user_info = self.gitlab.check_auth()
        ssh_ok = check_ssh_connection(self.ssh_host, self.ssh_port, self.ssh_user, timeout=self.ssh_timeout)
        return {"api_user": user_info.get("username"), "ssh_connected": ssh_ok}

    def verify_target_commits(self, targets: List[RepositoryTarget]) -> None:
        """逐一核验请求中所有目标仓库的候选 Commit 均已存在于 GitLab 服务端。"""
        repos_cfg = self.config.get("repositories", {})
        for target in targets:
            cfg = repos_cfg.get(target.name, {})
            project_path = cfg.get("api_project_path", f"sushaohua/{target.name}")
            verify_server_commit(self.gitlab, project_path, target.commit)

    def _run_sandbox_steps(self, sandbox_dir: Path, req: QARunRequest,
                           cid: Optional[str] = None) -> tuple:
        """在沙箱或容器内顺序执行请求中的全部构建与测试命令并汇总结果。"""
        runtime_logs = []
        build_results, test_results = [], []
        overall_passed = True
        for cmd_item in req.commands:
            cmd, subpath = cmd_item.get("command", ""), cmd_item.get("subpath", "")
            is_test = cmd_item.get("kind", "test") == "test"
            c_res = run_command_in_sandbox(sandbox_dir, cmd, subpath, cid)
            res_dict = {
                "command": cmd, "exit_code": str(c_res.returncode),
                "subpath": subpath,
                "duration": f"{c_res.duration_seconds:.2f}s",
                "output": (c_res.stdout + "\n" + c_res.stderr).strip(),
            }
            if is_test:
                test_results.append(res_dict)
            else:
                build_results.append(res_dict)
            runtime_logs.append(f"$ ({subpath or '.'}) {cmd} -> {c_res.returncode}")
            runtime_logs.append(c_res.stdout + "\n" + c_res.stderr)
            if c_res.returncode != 0:
                overall_passed = False
        return runtime_logs, build_results, test_results, overall_passed

    def execute_run(self, req: QARunRequest) -> tuple:
        """在只读容器沙箱中执行完整的远端提交校验、全新检出与客观测试流程。"""
        if not req.commands or not any(item.get("kind", "test") == "test" for item in req.commands):
            raise QARunnerError("At least one accepted test command is required; zero checks cannot pass")
        self.verify_target_commits(req.targets)
        run_id = f"run_{datetime.datetime.now().strftime('%H%M%S')}"
        sandbox_dir = create_isolated_sandbox(self.sandbox_base, req.task_id, run_id)
        # 1. 在宿主机隔离沙箱目录内拉取服务端精确锁定的 Commit
        git_timeout = int(self.config.get("timeouts", {}).get("git_clone_seconds", 300))
        c_logs = []
        for target in req.targets:
            log = checkout_remote_repository(sandbox_dir, target, timeout=git_timeout)
            c_logs.append(log)
        # 2. 启动以只读模式挂载该沙箱快照的 Docker 容器执行构建与测试
        c_name = f"qa_{sanitize_path_component(req.task_id)}_{run_id}"
        img = self.config.get("sandbox", {}).get("image", "qa-sandbox:20261029")
        cid = start_docker_sandbox(c_name, img, sandbox_dir, read_only=True)
        try:
            r_logs, b_res, t_res, ok = self._run_sandbox_steps(sandbox_dir, req, cid)
        finally:
            stop_docker_sandbox(cid)
            inspect_data = inspect_docker_sandbox(cid)
        r_logs.insert(0, f"=== Docker Container Inspect: {cid} ===\n{json.dumps(inspect_data, indent=2)}")
        res = QARunResult(
            task_id=req.task_id, task_revision=req.task_revision, run_id=run_id,
            sandbox_id=sandbox_dir.name, sandbox_path=str(sandbox_dir),
            container_id=cid, container_image=img, container_inspect=inspect_data, passed=ok,
            tool_versions=collect_tool_versions(), build_results=b_res, test_results=t_res,
            summary="All sandbox tests passed" if ok else "Sandbox QA execution failed",
        )
        return res, sandbox_dir, c_logs, r_logs


def create_cli_parser() -> argparse.ArgumentParser:
    """构建 QA Runner 命令行参数解析器。"""
    parser = argparse.ArgumentParser(description="Server Candidate QA Sandbox Runner")
    parser.add_argument("--config", default="project-control/config/qa_runner/default_config.yaml",
                        help="Path to runner configuration YAML")
    parser.add_argument("--task", default="AUTO-01", help="Task ID under verification")
    parser.add_argument("--revision", type=int, default=1, help="Task revision number")
    parser.add_argument("--repo-commit", action="append", default=[],
                        help="Repository target in format 'name=commit[:ref]'")
    parser.add_argument("--cmd", action="append", default=[],
                        help="Command to run in format 'kind:subpath:command'")
    parser.add_argument("--output-dir", default="", help="Directory to save evidence output")
    parser.add_argument("--check-only", action="store_true", help="Only verify server credentials")
    return parser


def parse_repo_target(raw: str, default_urls: dict, default_branches: dict = None) -> RepositoryTarget:
    """解析形如 'name=commit[:ref]' 的单条目标仓库命令行规格字符串。"""
    name, sep, rest = raw.partition("=")
    if not sep or not rest:
        raise QARunnerError(f"Target format must be 'name=commit[:ref]', got: {raw}")
    commit, sep_ref, ref = rest.partition(":")
    validate_commit_sha(commit)
    url = default_urls.get(name, f"ssh://git@192.168.77.113:2222/sushaohua/{name}.git")
    if not sep_ref:
        ref = (default_branches or {}).get(name, "")
    if not ref:
        raise QARunnerError(f"Missing remote ref for {name}")
    return RepositoryTarget(name=name, url=url, commit=commit, ref=ref)


def parse_command_spec(raw: str) -> dict:
    """解析形如 'kind:subpath:command' 的构建/测试命令规格字符串。"""
    parts = raw.split(":", 2)
    if len(parts) == 3:
        return {"kind": parts[0], "subpath": parts[1], "command": parts[2]}
    return {"kind": "test", "subpath": "", "command": raw}


def main() -> int:
    """QA Runner 命令行主入口函数。"""
    parser = create_cli_parser()
    args = parser.parse_args()
    try:
        config = load_yaml_config(Path(args.config))
        runner = QARunner(config)
        if args.check_only:
            status = runner.verify_server_prerequisites()
            print(f"[OK] Server verification passed: {status}")
            return 0
        urls = {k: v.get("url", "") for k, v in config.get("repositories", {}).items()}
        branches = {k: v.get("default_branch", "") for k, v in config.get("repositories", {}).items()}
        targets = [parse_repo_target(r, urls, branches) for r in args.repo_commit]
        commands = [parse_command_spec(c) for c in args.cmd]
        req = QARunRequest(task_id=args.task, task_revision=args.revision, targets=targets, commands=commands)
        res, s_dir, c_logs, r_logs = runner.execute_run(req)
        out_dir = Path(args.output_dir) if args.output_dir else s_dir / "evidence"
        lock_data = build_server_lock_data(targets)
        logs = {"checkout": "\n".join(c_logs), "runtime": "\n".join(r_logs)}
        refs = write_evidence_bundle(out_dir, res, lock_data, logs)
        print(f"[QA VERDICT] {res.summary} | Evidence bundle saved to: {out_dir}")
        print(f"[SERVER QA REF] {json.dumps(refs['server_qa'], indent=2)}")
        return 0 if res.passed else 1
    except QARunnerError as err:
        print(f"[QA RUNNER ERROR] {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
