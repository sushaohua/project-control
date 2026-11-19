#!/usr/bin/env python3
"""服务端候选版本锁定与隔离沙箱 QA 运行器。

强制保证正式 QA 仅在从 GitLab 服务端全新克隆的隔离沙箱（含只读 Docker 容器）中执行，
严格拒绝本地开发工作树挂载、未提交脏文件及未推送至服务端的提交哈希。
"""

import argparse
from dataclasses import dataclass, field, replace
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
from typing import Dict, List, Optional, Tuple, Union
import urllib.parse

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
    profile: str = "host-software"


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
    profile: str = "host-software"
    platform_inputs: Dict[str, object] = field(default_factory=dict)


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


def verify_remote_ref(target: RepositoryTarget, timeout: int = 60) -> str:
    """通过原生 `git ls-remote` 直连核验远端仓库及分支引用可达，拒绝未建库或失效分支。"""
    validate_commit_sha(target.commit)
    url = validate_remote_url(target.url)
    ref = target.ref or "HEAD"
    if ref != "HEAD" and not ref.startswith("refs/"):
        ref = f"refs/heads/{ref}"
    cmd = ["git", "ls-remote", url, ref]
    try:
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout,
                              env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    except (subprocess.TimeoutExpired, OSError) as err:
        raise QARunnerError(f"Remote ls-remote failed for {target.name}: {err}") from err
    if proc.returncode != 0 or not proc.stdout.strip():
        detail = proc.stderr.strip() or f"ref not found: {ref}"
        raise QARunnerError(f"Remote verification failed for {target.name}: {detail}")
    return proc.stdout.splitlines()[0].split()[0]


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
    repo_dir = validate_sandbox_subpath(sandbox_dir, target.name)
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


def _link_repo_rules(sandbox_dir: Path, repo_name: str, subdir: str) -> None:
    """在沙箱内为指定业务仓补全指向 `agents/<subdir>` 的相对软链接（绝不覆盖已有文件）。"""
    repo_dir = sandbox_dir / repo_name
    agents_dir = sandbox_dir / "agents" / subdir
    if not repo_dir.is_dir() or not agents_dir.is_dir():
        return
    exclude = repo_dir / ".git/info/exclude"
    lines = exclude.read_text(encoding="utf-8").splitlines() if exclude.is_file() else []
    added = []
    for entry in ("AGENTS.md", ".agents"):
        src, dst = agents_dir / entry, repo_dir / entry
        if src.exists() and not dst.exists() and not dst.is_symlink():
            dst.symlink_to(os.path.relpath(src, repo_dir), target_is_directory=src.is_dir())
            if f"/{entry}" not in lines:
                added.append(f"/{entry}")
    if added and exclude.parent.is_dir():
        exclude.write_text("\n".join(lines + added) + "\n", encoding="utf-8")


def prepare_sandbox_rule_links(sandbox_dir: Path, targets: List[RepositoryTarget],
                               config: dict) -> None:
    """当沙箱同时检出 `agents` 仓与业务仓时，衔接相对规则软链接供只读容器与审阅读取。"""
    if not (sandbox_dir / "agents").is_dir():
        return
    mapping = (config.get("rule_sources") or {}).get("repo_subdirs") or {}
    for target in targets:
        subdir = mapping.get(target.name)
        if subdir:
            _link_repo_rules(sandbox_dir, target.name, subdir)


# 单条沙箱构建或测试命令的默认超时秒数
DEFAULT_CMD_TIMEOUT = 300


@dataclass(frozen=True)
class ContainerCommand:
    """绑定容器 ID 与当前命令的有界执行时间。"""

    container_id: str
    timeout_seconds: int


def run_command_in_sandbox(sandbox_dir: Path, cmd: str, subpath: str = "",
                           container_id: Optional[Union[str, ContainerCommand]] = None) -> CommandResult:
    """在指定 Docker 容器内或隔离沙箱子目录中执行单条构建/测试命令并记录耗时与退出码。"""
    work_dir = validate_sandbox_subpath(sandbox_dir, subpath)
    start_time = datetime.datetime.now()
    if container_id:
        limit = DEFAULT_CMD_TIMEOUT
        if isinstance(container_id, ContainerCommand):
            limit, container_id = container_id.timeout_seconds, container_id.container_id
        target_dir = f"/workspace/{subpath}".rstrip("/") if subpath else "/workspace"
        exec_cmd = ["docker", "exec", "-w", target_dir, container_id, "bash", "-c", cmd]
        try:
            proc = subprocess.run(exec_cmd, text=True, capture_output=True, timeout=limit)
            dur = (datetime.datetime.now() - start_time).total_seconds()
            return CommandResult(command=cmd, cwd=target_dir, returncode=proc.returncode,
                                 stdout=proc.stdout, stderr=proc.stderr, duration_seconds=dur)
        except subprocess.TimeoutExpired as error:
            dur = (datetime.datetime.now() - start_time).total_seconds()
            stdout = (error.stdout or b"").decode(errors="replace")
            stderr = (error.stderr or b"").decode(errors="replace")
            return CommandResult(command=cmd, cwd=target_dir, returncode=-1, stdout=stdout,
                                 stderr=f"{stderr}\nCommand timed out after {limit}s", duration_seconds=dur)
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
        "profile": run_result.profile,
        "build_count": len(run_result.build_results),
        "test_count": len(run_result.test_results),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }


SYSTEM_ARTIFACT_NAMES = (
    "build-plan.json",
    "build-receipt.json",
    "package-receipt.json",
    "image-receipt.json",
    "release-manifest.json",
    "printer-soc-rootfs.tar.gz",
    "rootfs.ubi",
    "aml_upgrade_package.img",
)


def archive_system_artifacts(sandbox_dir: Path, output_dir: Path, task_id: str) -> Dict[str, dict]:
    """将系统沙箱 `/output/<task_id>` 下的清单与交付制品归档至 `output_dir/artifacts` 并流式计算 SHA256。"""
    src_root = sandbox_dir.with_name(sandbox_dir.name + "_output") / sanitize_path_component(task_id).lower()
    if not src_root.is_dir():
        return {}
    archived = {}
    dst_root = output_dir / "artifacts"
    for name in SYSTEM_ARTIFACT_NAMES:
        src = src_root / name
        if not (src.is_file() and not src.is_symlink()):
            continue
        dst_root.mkdir(parents=True, exist_ok=True)
        dst = dst_root / name
        shutil.copy2(src, dst)
        hasher = hashlib.sha256()
        with dst.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1048576), b""):
                hasher.update(chunk)
        archived[name] = {"path": str(dst), "bytes": dst.stat().st_size, "sha256": hasher.hexdigest()}
    return archived


def build_server_qa_proof(run_result: QARunResult, refs: Dict[str, Dict[str, str]]) -> dict:
    """构造满足 delivery_checks 门禁要求的标准 server_qa.json 证明字典。"""
    cid = run_result.container_id or run_result.sandbox_id
    img = run_result.container_image or "ubuntu:20.04"
    proof = {
        "task_id": run_result.task_id,
        "task_revision": run_result.task_revision,
        "source": "server-pinned-commits",
        "profile": run_result.profile,
        "platform_inputs": run_result.platform_inputs,
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
    if refs.get("artifacts"):
        proof["artifacts"] = refs["artifacts"]
    return proof


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
    if run_result.profile == "c308l-system" and run_result.sandbox_path:
        archived = archive_system_artifacts(Path(run_result.sandbox_path), output_dir, run_result.task_id)
        if archived:
            refs["artifacts"] = archived
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
    """以 name/image 启动容器；mount_dir 源码按 read_only 挂载，独立输出可写，返回容器 ID。"""
    mode = "ro" if read_only else "rw"
    return _start_docker_sandbox(name, image, mount_dir, (mode, 3600))


def _start_docker_sandbox(name: str, image: str, mount_dir: Path, options: Tuple[str, int]) -> str:
    """启动具有指定挂载模式和存活上限的隔离容器。"""
    mode, lifetime = options
    output_dir = mount_dir.with_name(mount_dir.name + "_output")
    output_dir.mkdir(mode=0o700, exist_ok=False)
    cmd = [
        "docker", "run", "-d", "--init",
        "--name", name,
        "-v", f"{mount_dir.resolve()}:/workspace:{mode}",
        "-v", f"{output_dir.resolve()}:/output:rw",
        "-e", "QA_OUTPUT_DIR=/output",
        "-e", "C308L_SDK_WORK_ROOT=/output/sdk-worktrees",
        "-w", "/workspace",
        image, "sleep", str(lifetime),
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


BUILD_PROFILES = ("host-software", "c308l-app", "c308l-system")


def validate_profile_request(req: QARunRequest) -> None:
    """核对 req 的软件验证范围与命令覆盖；缺少必需输入时抛 QARunnerError。"""
    if req.profile not in BUILD_PROFILES:
        raise QARunnerError("Unknown build profile: " + req.profile)
    if not req.commands or not any(item.get("kind", "test") == "test" for item in req.commands):
        raise QARunnerError("At least one accepted test command is required; zero checks cannot pass")
    if req.profile == "host-software":
        return
    required = {"project-control", "agents", "test_harness", "printer-soc"}
    if not required.issubset({target.name for target in req.targets}):
        raise QARunnerError("C308L QA requires pinned application, control, rules and test repositories")
    kinds = {item.get("kind", "test") for item in req.commands}
    if not kinds.intersection({"build", "image"}):
        raise QARunnerError("C308L QA requires an actual target build command")
    if req.profile == "c308l-system" and "image" not in kinds:
        raise QARunnerError("System profile requires an explicit image build and image verification test")


def _import_input_tool(path: Path, name: str):
    """以 name 加载受控 path 模块；调用方必须先确定其候选或运行器来源。"""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _stage_profile_workspace(sandbox_dir: Path, req: QARunRequest, config: dict) -> dict:
    """按 req/config 在 sandbox_dir 暂存工具和描述；摘要未获接受即拒绝，不执行候选代码。"""
    clients = config.get("repo_clients")
    if not isinstance(clients, list) or not clients:
        raise QARunnerError("C308L QA requires configured Repo clients")
    repositories = [{"path": target.name, "url": target.url, "commit": target.commit,
                     "branch": target.ref[len("refs/heads/"):] if target.ref.startswith("refs/heads/")
                     else target.ref} for target in req.targets]
    data = {"schema_version": 2, "repositories": repositories, "repo_clients": clients}
    trusted = Path(__file__).resolve().parents[3] / "tools/sdk_workspace.py"
    raw = trusted.read_bytes()
    security = config.get("security") or {}
    accepted = security.get("accepted_sdk_tool_sha256", "")
    if req.profile == "c308l-system":
        accepted = security.get("accepted_c308l_system_sdk_tool_sha256", accepted)
    digest = compute_bytes_sha256(raw)
    if not re.fullmatch(r"[0-9a-f]{64}", accepted or "") or accepted != digest:
        raise QARunnerError("SDK input tool lacks an accepted matching SHA256")
    # 先核对接受值，再写入同一字节串；不以复制后的自报摘要作为接受依据。
    with (sandbox_dir / "workspace.json").open("x", encoding="utf-8") as output:
        json.dump(data, output, ensure_ascii=False, indent=2)
    destination = sandbox_dir / "tools/sdk_workspace.py"
    destination.parent.mkdir(exist_ok=False)
    with destination.open("xb") as output:
        output.write(raw)
    return {"workspace": data, "sdk_tool_sha256": digest}


def prepare_profile_inputs(sandbox_dir: Path, req: QARunRequest, config: dict) -> dict:
    """为 req 在隔离 sandbox_dir 重建锁定 SDK；config 只提供清单配置，不接受开发者目录挂载。"""
    if req.profile == "host-software":
        return {}
    try:
        staged = _stage_profile_workspace(sandbox_dir, req, config)
        tool = _import_input_tool(sandbox_dir / "tools/sdk_workspace.py", "qa_sdk_workspace")
        clients = []
        for entry in staged["workspace"]["repo_clients"]:
            sdk = tool.load_sdk_spec(sandbox_dir, entry)
            tool.restore_sdk(sandbox_dir, sdk)
            clients.append(tool.verify_sdk(sandbox_dir, sdk))
        contract_path = sandbox_dir / "project-control/contracts/c308l_platform_contract.yaml"
        return {"source": "server-reconstructed-sdk", "clients": clients,
                "contract_sha256": compute_file_sha256(contract_path),
                "sdk_tool_sha256": staged["sdk_tool_sha256"],
                "validation": {"passed": False, "scope": "pending-container-check"}}
    except (OSError, ValueError, KeyError, TypeError, ImportError,
            subprocess.SubprocessError, yaml.YAMLError) as error:
        raise QARunnerError("Platform input reconstruction failed: " + str(error)) from error


def accepted_profile_image(req: QARunRequest, config: dict) -> str:
    """根据 req 范围读取 config 接受的镜像；目标构建要求准确 SHA256，返回 Docker 镜像参数。"""
    sandbox = config.get("sandbox") or {}
    if req.profile == "host-software":
        return sandbox.get("image", "qa-sandbox:20261029")
    digest = sandbox.get("image_digest", "")
    if req.profile == "c308l-system":
        digest = sandbox.get("c308l_system_image_digest", digest)
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest or ""):
        raise QARunnerError("C308L QA requires an accepted exact container image digest")
    return digest


def system_profile_timeouts(config: dict) -> Dict[str, int]:
    """读取有上界的系统构建时限，拒绝无效或可能关闭超时保护的配置。"""
    configured = (config.get("timeouts") or {}).get("c308l_system", {})
    if not isinstance(configured, dict):
        raise QARunnerError("C308L system timeouts must be a mapping")
    defaults = dict(build=DEFAULT_CMD_TIMEOUT, image=DEFAULT_CMD_TIMEOUT, test=DEFAULT_CMD_TIMEOUT, container=3600)
    values = {kind: configured.get(kind, seconds) for kind, seconds in defaults.items()}
    if any(type(value) is not int or not 1 <= value <= 7200 for value in values.values()):
        raise QARunnerError("C308L system timeouts must be integer seconds between 1 and 7200")
    return values


def run_profile_checks(sandbox_dir: Path, req: QARunRequest, cid: str, inputs: dict) -> CommandResult:
    """在 cid 内检查 req 的 inputs；sandbox_dir 仅定位只读输入，返回真实命令结果并记录校验身份。"""
    command = ("REPO_TRACE=0 PYTHONDONTWRITEBYTECODE=1 python3 "
               "test_harness/static_checks/platform/check_platform_inputs.py --workspace /workspace")
    result = run_command_in_sandbox(sandbox_dir, command, "", cid)
    try:
        proof = json.loads(result.stdout)
        valid = proof.get("passed") is True and proof.get("scope") == "software-inputs"
    except (json.JSONDecodeError, AttributeError):
        valid = False
    inputs["validation"] = {"passed": result.returncode == 0 and valid,
                            "container_id": cid, "command": command,
                            "stdout_sha256": compute_bytes_sha256(result.stdout.encode())}
    if result.returncode == 0 and not valid:
        result.returncode = 1
        result.stderr += "\nPlatform checker returned missing or invalid software-inputs evidence"
    if result.returncode == 0 and req.profile == "c308l-system":
        copied = copy_system_worktrees(sandbox_dir, cid, inputs)
        copied.stdout = result.stdout + "\n" + copied.stdout
        copied.stderr = result.stderr + "\n" + copied.stderr
        result = copied
    return result


def copy_system_worktrees(sandbox_dir: Path, cid: str, inputs: dict) -> CommandResult:
    """将 inputs 的受控 SDK 在 cid 内复制到独立可写输出；sandbox_dir 定位输入，返回复制结果。"""
    commands = ["mkdir -p /output/sdk-worktrees"]
    worktrees = {}
    for client in inputs["clients"]:
        source = "/workspace/" + client["path"]
        destination = "/output/sdk-worktrees/" + client["id"]
        commands.append("test ! -e " + shlex.quote(destination))
        commands.append("cp -a -- " + shlex.quote(source) + " " + shlex.quote(destination))
        worktrees[client["id"]] = destination
    result = run_command_in_sandbox(sandbox_dir, " && ".join(commands), "", cid)
    inputs["build_worktrees"] = worktrees if result.returncode == 0 else {}
    inputs["validation"]["system_copy_passed"] = result.returncode == 0
    return result


class QARunner:
    """统筹远端提交核验、隔离沙箱检出与只读容器测试执行的 QA 核心运行器。"""

    def __init__(self, config: dict, workspace_root: Optional[Path] = None):
        """初始化 QA 运行器，解析服务端 SSH 地址、超时参数并校验沙箱根路径隔离性。"""
        self.config = config
        self.workspace_root = workspace_root or Path.cwd()
        server_cfg = config.get("server", {})
        self.ssh_host = server_cfg.get("ssh_host", "192.168.77.79")
        self.ssh_port = server_cfg.get("ssh_port", 2222)
        self.ssh_user = server_cfg.get("ssh_user", "git")
        self.ssh_timeout = int(server_cfg.get("ssh_timeout_seconds", 30))
        sandbox_cfg = config.get("sandbox", {})
        base_dir = Path(sandbox_cfg.get("base_dir", "/tmp/qa_sandboxes"))
        self.sandbox_base = validate_sandbox_path(base_dir, [self.workspace_root])

    def verify_server_prerequisites(self) -> dict:
        """核验 GitLab SSH 端口公钥认证连通性（纯 Git/SSH 直连，不依赖 HTTP API）。"""
        ssh_ok = check_ssh_connection(self.ssh_host, self.ssh_port, self.ssh_user, timeout=self.ssh_timeout)
        return {"auth_mode": "ssh-git", "ssh_connected": ssh_ok}

    def verify_target_commits(self, targets: List[RepositoryTarget]) -> None:
        """逐一通过 SSH 与 `git ls-remote` 核验候选仓与引用可达性，具体提交再由克隆强校验。"""
        check_ssh_connection(self.ssh_host, self.ssh_port, self.ssh_user, timeout=self.ssh_timeout)
        for target in targets:
            verify_remote_ref(target, timeout=self.ssh_timeout)

    def _run_sandbox_steps(self, sandbox_dir: Path, req: QARunRequest,
                           cid: Optional[str] = None) -> tuple:
        """在沙箱或容器内顺序执行请求中的全部构建与测试命令并汇总结果。"""
        runtime_logs = []
        build_results, test_results = [], []
        overall_passed = True
        limits = system_profile_timeouts(self.config) if req.profile == "c308l-system" else {}
        for cmd_item in req.commands:
            cmd, subpath = cmd_item.get("command", ""), cmd_item.get("subpath", "")
            kind = cmd_item.get("kind", "test")
            scoped = ContainerCommand(cid, limits[kind]) if cid and kind in limits else cid
            c_res = run_command_in_sandbox(sandbox_dir, cmd, subpath, scoped)
            res_dict = {
                "command": cmd, "exit_code": str(c_res.returncode),
                "subpath": subpath,
                "duration": f"{c_res.duration_seconds:.2f}s",
                "output": (c_res.stdout + "\n" + c_res.stderr).strip(),
            }
            if kind == "test":
                test_results.append(res_dict)
            else:
                build_results.append(res_dict)
            runtime_logs.append(f"$ ({subpath or '.'}) {cmd} -> {c_res.returncode}")
            runtime_logs.append(c_res.stdout + "\n" + c_res.stderr)
            if c_res.returncode != 0:
                overall_passed = False
                break
        return runtime_logs, build_results, test_results, overall_passed

    def execute_run(self, req: QARunRequest) -> tuple:
        """在只读容器沙箱中执行完整的远端提交校验、全新检出与客观测试流程。"""
        validate_profile_request(req)
        img = accepted_profile_image(req, self.config)
        limits = system_profile_timeouts(self.config) if req.profile == "c308l-system" else {}
        if limits:
            budget = sum(limits.get(item.get("kind", "test"), DEFAULT_CMD_TIMEOUT) for item in req.commands)
            if limits["container"] <= budget + 2 * DEFAULT_CMD_TIMEOUT:
                raise QARunnerError("C308L system container lifetime must cover SDK checks and all commands")
        self.verify_target_commits(req.targets)
        run_id = f"run_{datetime.datetime.now().strftime('%H%M%S')}"
        sandbox_dir = create_isolated_sandbox(self.sandbox_base, req.task_id, run_id)
        # 1. 在宿主机隔离沙箱目录内拉取服务端精确锁定的 Commit
        git_timeout = int(self.config.get("timeouts", {}).get("git_clone_seconds", 300))
        c_logs = []
        for target in req.targets:
            log = checkout_remote_repository(sandbox_dir, target, timeout=git_timeout)
            c_logs.append(log)
        prepare_sandbox_rule_links(sandbox_dir, req.targets, self.config)
        platform_inputs = prepare_profile_inputs(sandbox_dir, req, self.config)
        # 2. 启动以只读模式挂载该沙箱快照的 Docker 容器执行构建与测试
        c_name = f"qa_{sanitize_path_component(req.task_id)}_{run_id}"
        if limits:
            cid = _start_docker_sandbox(c_name, img, sandbox_dir, ("ro", limits["container"]))
        else:
            cid = start_docker_sandbox(c_name, img, sandbox_dir, read_only=True)
        try:
            r_logs, b_res, t_res, ok = self._run_container_steps(
                sandbox_dir, req, {"cid": cid, "inputs": platform_inputs})
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
            profile=req.profile, platform_inputs=platform_inputs,
        )
        return res, sandbox_dir, c_logs, r_logs

    def _run_container_steps(self, sandbox_dir: Path, req: QARunRequest, context: dict) -> tuple:
        """按 req 在 context 容器内先校验平台再构建；sandbox_dir 定位输入，返回日志、构建、测试及结论。"""
        cid = context["cid"]
        if req.profile == "host-software":
            return self._run_sandbox_steps(sandbox_dir, req, cid)
        checked = run_profile_checks(sandbox_dir, req, cid, context["inputs"])
        record = {"command": checked.command, "exit_code": str(checked.returncode),
                  "subpath": "", "duration": f"{checked.duration_seconds:.2f}s",
                  "output": checked.stdout + "\n" + checked.stderr}
        logs = [f"$ {checked.command} -> {checked.returncode}", record["output"]]
        if checked.returncode != 0:
            return logs, [], [record], False
        inputs = context["inputs"]
        roots = {client["id"]: "/workspace/" + client["path"] for client in inputs["clients"]}
        if req.profile == "c308l-system":
            roots = inputs["build_worktrees"]
        if "c308l" not in roots:
            raise QARunnerError("C308L build workspace is missing")
        # 每条命令继承明确 SDK 输入；系统构建只采用独立副本，源树仍为只读挂载。
        prefix = "env REPO_TRACE=0 C308L_SDK_ROOT=" + shlex.quote(roots["c308l"]) + " bash -c "
        commands = [dict(item, command=prefix + shlex.quote(item["command"])) for item in req.commands]
        runtime, builds, tests, passed = self._run_sandbox_steps(
            sandbox_dir, replace(req, commands=commands), cid)
        return logs + runtime, builds, [record] + tests, passed


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
    parser.add_argument("--profile", choices=BUILD_PROFILES, default="host-software",
                        help="Explicit software build and verification scope")
    return parser


def parse_repo_target(raw: str, default_urls: dict, default_branches: dict = None) -> RepositoryTarget:
    """解析形如 'name=commit[:ref]' 的单条目标仓库命令行规格字符串。"""
    name, sep, rest = raw.partition("=")
    if not sep or not rest:
        raise QARunnerError(f"Target format must be 'name=commit[:ref]', got: {raw}")
    commit, sep_ref, ref = rest.partition(":")
    validate_commit_sha(commit)
    if name not in default_urls or not default_urls[name]:
        raise QARunnerError(f"Repository URL must be explicitly configured: {name}")
    url = default_urls[name]
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
        req = QARunRequest(task_id=args.task, task_revision=args.revision, targets=targets,
                           commands=commands, profile=args.profile)
        res, s_dir, c_logs, r_logs = runner.execute_run(req)
        out_dir = Path(args.output_dir) if args.output_dir else s_dir / "evidence"
        lock_data = build_server_lock_data(targets)
        lock_data.update({"profile": res.profile, "platform_inputs": res.platform_inputs})
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
