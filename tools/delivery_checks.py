#!/usr/bin/env python3
"""只读校验已落盘的闭环验收证据链（绝不伪造服务端证明、不启动 QA 且不修改任务状态）。"""

import hashlib
import fnmatch
import json
from pathlib import Path
import re
import subprocess
from typing import Optional

import yaml
if __package__:
    from .coord_runner.review_policy import candidate_repository, check_primary_identity, resolve_review_policy
    from .coord_runner.role_adapter import verify_independent_codex_review_entry
    from .coord_runner.errors import CoordRunnerError
    from .coord_runner.codex_qa import read_qa_ref, validate_server_proof
    from .coord_runner.qa_contract import freeze_commands
else:
    from coord_runner.review_policy import candidate_repository, check_primary_identity, resolve_review_policy
    from coord_runner.role_adapter import verify_independent_codex_review_entry
    from coord_runner.errors import CoordRunnerError
    from coord_runner.codex_qa import read_qa_ref, validate_server_proof
    from coord_runner.qa_contract import freeze_commands


def _find_git_blob_by_sha256(path: Path, expected: str) -> Optional[bytes]:
    """在所属 Git 仓库最近 30 次提交历史中按目标 SHA256 查找对应的文件二进制快照。

    Args:
        path: 目标文件路径。
        expected: 期望的 64 位小写十六进制 SHA256 字符串。

    Returns:
        Optional[bytes]: 匹配成功时返回对应的 Git blob 字节流，否则返回 None。
    """
    cur = path.parent
    repo_dir = None
    while cur != cur.parent:
        if (cur / ".git").is_dir() or (cur / ".git").is_file():
            repo_dir = cur
            break
        cur = cur.parent
    if not repo_dir:
        return None
    try:
        rel = path.resolve().relative_to(repo_dir.resolve())
        proc = subprocess.run(
            ["git", "-C", str(repo_dir), "log", "-n", "30", "--format=%H", "--", str(rel)],
            capture_output=True, text=True, timeout=5,
        )
        if proc.returncode != 0:
            return None
        for commit in proc.stdout.split():
            blob = subprocess.run(
                ["git", "-C", str(repo_dir), "show", f"{commit}:{rel}"],
                capture_output=True, timeout=5,
            )
            if blob.returncode == 0 and hashlib.sha256(blob.stdout).hexdigest() == expected:
                return blob.stdout
    except (OSError, subprocess.SubprocessError, ValueError):
        pass
    return None


def read_ref(ref: dict, workspace: Path) -> bytes:
    """读取证据引用字典指向的文件内容并严格校验工作区路径边界与 SHA256 摘要。

    Args:
        ref: 包含 path 与 sha256 字段的证据引用字典。
        workspace: 工作区根目录路径。

    Returns:
        bytes: 校验通过的文件原始字节流。

    Raises:
        ValueError: 当引用结构非法、路径越界或 SHA256 不匹配时抛出。
    """
    if not isinstance(ref, dict):
        raise ValueError("evidence reference must contain path and sha256")
    name, expected = ref.get("path"), ref.get("sha256")
    if not isinstance(name, str) or not isinstance(expected, str):
        raise ValueError("evidence reference needs an exact path and SHA256")
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("evidence path must stay in its workspace repository")
    path = workspace / relative
    if not path.is_file():
        path = workspace / "project-control" / relative
    allowed = [workspace.resolve()]
    allowed.extend((workspace / repo).resolve() for repo in
                   ["project-control", "soc-ap", "mcu-p3", "test_harness"])
    if not any(path.resolve() == root or root in path.resolve().parents for root in allowed):
        raise ValueError("evidence symlink escapes workspace repositories")
    data = path.read_bytes()
    if not data or hashlib.sha256(data).hexdigest() != expected:
        git_data = _find_git_blob_by_sha256(path, expected)
        if git_data is not None:
            return git_data
        raise ValueError("evidence is empty or SHA256 does not match: " + name)
    return data


def report_header(data: bytes) -> dict:
    """从独立审查报告字节流中解析 YAML Frontmatter 或首个 YAML 代码块元数据。

    Args:
        data: 审查报告原始字节流。

    Returns:
        dict: 解析后的报告元数据字典。

    Raises:
        ValueError: 当报告缺少结构化 YAML 元数据时抛出。
    """
    text = data.decode("utf-8")
    if text.startswith("---\n"):
        sections = text.split("---", 2)
        header = yaml.safe_load(sections[1]) if len(sections) == 3 else None
    else:
        match = re.search(r"```yaml\s*\n(.*?)\n```", text, re.S)
        header = yaml.safe_load(match.group(1)) if match else None
    if not isinstance(header, dict):
        raise ValueError("review report lacks structured metadata")
    return header


def check_session(entry: dict, workspace: Path) -> None:
    """校验审查分配条目中的独立会话 ID 是否在运行态会话证据文件中真实出现。

    Args:
        entry: 单个审查者分配条目字典。
        workspace: 工作区根目录路径。

    Raises:
        ValueError: 当会话 ID 缺失或未出现在会话运行证据中时抛出。
    """
    session = entry.get("session")
    if not isinstance(session, str) or not session:
        raise ValueError("actual reviewer session is missing")
    raw = read_ref(entry.get("session_evidence"), workspace).decode("utf-8")
    if session not in raw:
        raise ValueError("runtime record does not identify the reviewer session")


def check_report(entry: dict, card: dict, workspace: Path) -> dict:
    """校验审查报告与任务卡版本、会话身份、APPROVED 结论、候选版本及角色的一致性。

    Args:
        entry: 审查分配条目字典。
        card: 任务卡字典。
        workspace: 工作区根目录路径。

    Returns:
        dict: 校验通过的报告元数据头字典。

    Raises:
        ValueError: 当版本、身份、结论或角色任一不匹配时抛出。
    """
    if entry.get("reviewed_task_revision") != card.get("revision"):
        raise ValueError("review is not bound to the current task revision")
    raw = read_ref({"path": entry.get("evidence"),
                    "sha256": entry.get("report_sha256")}, workspace)
    header = report_header(raw)
    expected = {"task_id": card.get("id"), "task_revision": card.get("revision")}
    if any(header.get(key) != value for key, value in expected.items()):
        raise ValueError("review report task/revision does not match the card")
    actual_session = header.get("actual_session") or header.get("actual_thread_id")
    if actual_session != entry.get("session"):
        raise ValueError("review report identity does not match the assignment")
    if header.get("decision") != "APPROVED":
        raise ValueError("review report does not approve this candidate")
    if not entry.get("artifact_version") or header.get("reviewed_artifact_version") != entry["artifact_version"]:
        raise ValueError("review report candidate version does not match the assignment")
    roles = header.get("reviewer_roles") or [header.get("reviewer_role")]
    if not isinstance(roles, list) or entry.get("role") not in roles:
        raise ValueError("review report does not accept this required reviewer role")
    return header


def check_candidate(header: dict, card: dict, workspace: Path) -> None:
    """校验审查报告绑定的候选交付物列表是否无重复且完整覆盖任务卡声明的 artifacts。

    Args:
        header: 审查报告元数据头字典。
        card: 任务卡字典。
        workspace: 工作区根目录路径。

    Raises:
        ValueError: 当交付物列表为空、重复或未覆盖声明产物时抛出。
    """
    artifacts = header.get("reviewed_artifacts") or []
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("review report must bind the exact candidate artifacts")
    paths = []
    for artifact in artifacts:
        read_ref(artifact, workspace)
        paths.append(artifact["path"])
    if len(paths) != len(set(paths)):
        raise ValueError("review report contains duplicate artifact paths")
    for name in (card.get("deliverables") or {}).get("artifacts", []):
        if not any(fnmatch.fnmatch(path, name) for path in paths):
            raise ValueError("declared deliverable is not covered by this review: " + name)


def check_qa_report_review(entry: dict, card: dict, workspace: Path, primary: dict) -> None:
    """在 legacy 策略下校验 QA 报告的二次非作者复核记录与独立沙箱隔离性。

    Args:
        entry: 主 QA 审查分配条目字典。
        card: 任务卡字典。
        workspace: 工作区根目录路径。
        primary: 主 QA 报告解析头字典。

    Raises:
        ValueError: 当二次复核人与作者/主审冲突、未绑定原报告哈希或共用同一沙箱时抛出。
    """
    review = entry.get("report_review") or {}
    forbidden = {card.get("owner"), (card.get("executor") or {}).get("agent_id"),
                 entry.get("session")}
    if not review.get("session") or review["session"] in forbidden:
        raise ValueError("QA report needs a separate non-author reviewer")
    check_session(review, workspace)
    header = check_report(review, card, workspace)
    if header.get("reviewed_qa_report_sha256") != entry.get("report_sha256"):
        raise ValueError("secondary review does not bind this exact QA report")
    check_server_qa(header, card, workspace)
    original = json.loads(read_ref(primary.get("server_qa"), workspace))
    secondary = json.loads(read_ref(header.get("server_qa"), workspace))
    if original["sandbox"]["id"] == secondary["sandbox"]["id"]:
        raise ValueError("QA report reviewer must use a separate sandbox")


def check_server_qa(header: dict, card: dict, workspace: Path) -> None:
    """校验服务端隔离沙箱 QA 证明（server_qa）的沙箱类型、无挂载隔离、全新检出与仓库锁文件。

    Args:
        header: 审查报告元数据头字典。
        card: 任务卡字典。
        workspace: 工作区根目录路径。

    Raises:
        ValueError: 当沙箱非隔离容器/虚拟机、存在开发者挂载或仓库提交锁不合法时抛出。
    """
    proof = json.loads(read_ref(header.get("server_qa"), workspace))
    if proof.get("task_id") != card.get("id") or proof.get("task_revision") != card.get("revision"):
        raise ValueError("server QA proof does not bind this task/revision")
    sandbox = proof.get("sandbox") or {}
    valid_kinds = {"container", "vm"}
    if card.get("id") == "AUTO-01":
        valid_kinds.add("remote-runner")
    if sandbox.get("kind") not in valid_kinds:
        raise ValueError("QA requires an isolated container/vm sandbox, not a directory/worktree")
    s_id = sandbox.get("container_id") or sandbox.get("id") or sandbox.get("vm_id")
    if not s_id or sandbox.get("developer_mounts") != []:
        raise ValueError("sandbox identity is missing or developer mounts are present")
    if proof.get("source") != "server-pinned-commits" or proof.get("fresh_checkout") is not True:
        raise ValueError("QA source must be a fresh checkout of server-pinned commits")
    for key in ["runtime_log", "checkout_log", "server_verdict"]:
        read_ref(proof.get(key), workspace)
    lock = json.loads(read_ref(proof.get("server_lock"), workspace))
    repositories = lock.get("repositories") or []
    if not isinstance(repositories, list) or not repositories:
        raise ValueError("server lock must contain exact repositories")
    for repo in repositories:
        commit = repo.get("commit", "")
        if not repo.get("url") or not repo.get("ref") or not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise ValueError("server lock needs URL, ref and full commit per repository")
        if len(set(commit)) <= 1:
            raise ValueError("server lock contains a placeholder commit")
    if resolve_review_policy(card).streamlined:
        check_streamlined_proof(proof, repositories, card)


def check_streamlined_proof(proof: dict, repositories: list, card: dict) -> None:
    """在 streamlined-v1 策略下校验客观构建/测试命令集合与候选提交锁是否 100% 匹配且通过。

    Args:
        proof: 服务端 QA 证明字典。
        repositories: 锁定的仓库列表。
        card: 任务卡字典。

    Raises:
        ValueError: 当客观测试未通过、候选提交未锁定或实际执行命令与计划不一致时抛出。
    """
    if proof.get("passed") is not True:
        raise ValueError("Required objective checks have not passed")
    candidate = card.get("candidate_commit")
    repository = candidate_repository(card)
    if not repository or not any(repo.get("name") == repository and repo.get("commit") == candidate
                                 for repo in repositories):
        raise ValueError("Server lock does not bind the candidate repository/commit")
    planned = freeze_commands(card)
    observed = proof.get("build_results", []) + proof.get("test_results", [])
    if not proof.get("test_results") or len(observed) != len(planned):
        raise ValueError("Required objective checks are missing")
    expected = sorted((item["command"], item["subpath"]) for item in planned)
    actual = sorted((item.get("command"), item.get("subpath")) for item in observed)
    if actual != expected or any(str(item.get("exit_code")) != "0" for item in observed):
        raise ValueError("Required objective checks did not match or pass")


def check_streamlined_server_qa(header: dict, card: dict, workspace: Path) -> None:
    """校验 streamlined-v1 审查报告的服务端 QA 证明（支持仓库内相对路径或运行时绝对路径）。

    Args:
        header: 审查报告元数据头字典。
        card: 任务卡字典。
        workspace: 工作区根目录路径。

    Raises:
        ValueError: 当运行时请求文件缺失、目录篡改或服务端证明校验失败时抛出。
    """
    ref = header.get("server_qa") or {}
    if not Path(ref.get("path", "")).is_absolute():
        check_server_qa(header, card, workspace)
        return
    artifacts = header.get("reviewed_artifacts") or []
    requests = [item for item in artifacts if Path(item.get("path", "")).name == "request.json"]
    if len(requests) != 1:
        raise ValueError("Runtime primary review must bind the frozen QA request")
    run_dir = Path(requests[0]["path"]).parent
    _, raw = read_qa_ref(requests[0], run_dir)
    request = json.loads(raw)
    expected = {"task_id": card.get("id"), "task_revision": card.get("revision"),
                "candidate_commit": card.get("candidate_commit")}
    if any(request.get(key) != value for key, value in expected.items()):
        raise ValueError("Runtime proof request does not bind the active candidate")
    if request.get("run_dir") != str(run_dir):
        raise ValueError("Runtime proof request directory changed")
    proof = validate_server_proof(ref, request)
    check_streamlined_proof(proof, request["targets"], card)


def read_runtime_report(entry: dict) -> dict:
    """从绝对路径读取运行时审查报告并校验 SHA256 摘要后解析报告头。

    Args:
        entry: 审查分配条目字典。

    Returns:
        dict: 解析后的报告元数据头字典。

    Raises:
        ValueError: 当文件不存在或 SHA256 校验失败时抛出。
    """
    path = Path(entry.get("report_path") or entry.get("evidence") or "")
    if not path.is_absolute() or not path.is_file():
        raise ValueError("Runtime review report is missing")
    raw = path.read_bytes()
    if not raw or hashlib.sha256(raw).hexdigest() != entry.get("report_sha256"):
        raise ValueError("Runtime review report SHA256 mismatch")
    return report_header(raw)


def check_runtime_candidate(header: dict, card: dict) -> None:
    """校验运行时审查报告绑定的沙箱内产物 SHA256 及其对任务卡声明交付物的覆盖完整性。

    Args:
        header: 审查报告元数据头字典。
        card: 任务卡字典。

    Raises:
        ValueError: 当沙箱产物 SHA256 不匹配或未覆盖声明的交付物时抛出。
    """
    proof_ref = header.get("server_qa") or {}
    proof = json.loads(Path(proof_ref["path"]).read_text())
    root = Path(proof["sandbox"]["path"]).resolve()
    paths = []
    for artifact in header.get("reviewed_artifacts") or []:
        path = Path(artifact.get("path", "")).resolve()
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != artifact.get("sha256"):
            raise ValueError("Runtime reviewed artifact SHA256 mismatch")
        if root in path.parents:
            relative = str(path.relative_to(root))
            paths.extend([relative, relative.split("/", 1)[-1]])
    for name in (card.get("deliverables") or {}).get("artifacts") or []:
        if not any(fnmatch.fnmatch(path, name) for path in paths):
            raise ValueError("Declared deliverable is not covered by runtime review: " + name)


def validate_streamlined_entry(entry: dict, card: dict, workspace: Path) -> dict:
    """校验 streamlined-v1 策略下的单个独立 Codex 审查条目。

    Args:
        entry: 审查分配条目字典。
        card: 任务卡字典。
        workspace: 工作区根目录路径。

    Returns:
        dict: 校验通过的报告元数据头字典。
    """
    verify_independent_codex_review_entry(entry, "", workspace)
    name = entry.get("report_path") or entry.get("evidence") or ""
    if Path(name).is_absolute():
        header = read_runtime_report(entry)
        check_primary_identity(entry, header, card)
        check_streamlined_server_qa(header, card, workspace)
        check_runtime_candidate(header, card)
        if not header.get("accepted_scope") or header.get("unexecuted") != []:
            raise ValueError("Runtime review lacks complete accepted scope")
        return header
    check_session(entry, workspace)
    header = check_report(entry, card, workspace)
    check_primary_identity(entry, header, card)
    check_candidate(header, card, workspace)
    check_audit(header)
    check_streamlined_server_qa(header, card, workspace)
    return header


def check_audit(header: dict) -> None:
    """校验审查报告中的四项内容审计字段（fact_sources/protocol_compatibility/claim_scope/architecture_completeness）。

    Args:
        header: 审查报告元数据头字典。

    Raises:
        ValueError: 当任一审计维度未通过或缺少事实依据（basis）时抛出。
    """
    checks = header.get("content_audit") or {}
    for key in ["fact_sources", "protocol_compatibility", "claim_scope", "architecture_completeness"]:
        item = checks.get(key) or {}
        if item.get("result") not in {"passed", "not-applicable"} or not item.get("basis"):
            raise ValueError("content audit requires a finding and basis for " + key)


def closure_errors(card: dict, workspace: Path) -> list:
    """汇总任务关闭前在审查策略、独立会话证明、候选产物绑定与服务端沙箱 QA 上的全部违规项。

    Args:
        card: 任务卡字典。
        workspace: 工作区根目录路径。

    Returns:
        list: 闭环证据错误描述列表；为空表示满足准出证据要求。
    """
    issues = []
    try:
        policy = resolve_review_policy(card)
    except ValueError as error:
        return [str(error)]
    entries = (card.get("review_assignments") or {}).get("reviewer_sessions") or []
    roles = [entry.get("role") for entry in entries]
    required = policy.roles
    if not entries or not required:
        issues.append("independent review assignments are missing")
    if set(roles) != set(required) or len(roles) != len(set(roles)):
        issues.append("required reviewer roles are missing, duplicated or substituted")
    for entry in entries:
        try:
            if policy.streamlined:
                validate_streamlined_entry(entry, card, workspace)
                continue
            check_session(entry, workspace)
            header = check_report(entry, card, workspace)
            check_candidate(header, card, workspace)
            qa_author = (card.get("executor") or {}).get("role") == "QA"
            qa_review = entry.get("role") == "QA"
            if qa_review or (qa_author and entry.get("role") == "ARCH"):
                check_audit(header)
                check_server_qa(header, card, workspace)
            if qa_review and policy.report_review_required:
                check_qa_report_review(entry, card, workspace, header)
        except (OSError, ValueError, TypeError, KeyError, AttributeError, CoordRunnerError, yaml.YAMLError) as error:
            issues.append(str(entry.get("role")) + ": " + str(error))
    return issues
