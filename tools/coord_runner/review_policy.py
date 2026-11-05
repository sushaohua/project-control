"""面向调度运行器与闭环门禁的统一版本化审查策略（legacy 与 streamlined-v1）解析模块。"""

from dataclasses import dataclass
import re


STREAMLINED_POLICY = "streamlined-v1"


@dataclass(frozen=True)
class ReviewPolicy:
    """单个任务卡的审查策略配置结果（必需审查角色元组、是否要求二次审报告及是否为精简策略）。"""
    roles: tuple
    report_review_required: bool
    streamlined: bool


def resolve_review_policy(card: dict, legacy_default: tuple = ()) -> ReviewPolicy:
    """根据任务卡的 qa_policy 与 reviewer 字段解析出对应的 ReviewPolicy 对象。"""
    version = card.get("qa_policy", "legacy")
    if not isinstance(version, str) or version not in {"legacy", STREAMLINED_POLICY}:
        raise ValueError("Unknown or invalid qa_policy; expected legacy or streamlined-v1")
    roles = card.get("reviewer") or (list(legacy_default) if version == "legacy" else [])
    roles = [roles] if isinstance(roles, str) else roles
    if not isinstance(roles, list) or any(not isinstance(role, str) or not role.strip() for role in roles):
        raise ValueError("reviewer must contain non-empty role names")
    if len(roles) != len(set(roles)):
        raise ValueError("reviewer contains duplicate roles")
    if version == "legacy":
        return ReviewPolicy(tuple(roles), True, False)
    qa_author = (card.get("executor") or {}).get("role") == "QA"
    primary = "ARCH" if qa_author and "QA" not in roles else "QA"
    roles = list(dict.fromkeys([primary] + roles))
    return ReviewPolicy(tuple(roles), False, True)


def author_sessions(card: dict) -> set:
    """提取任务卡中记录的全部作者/执行者会话标识集合（用于防止自审）。"""
    return {card.get("owner"), card.get("author_session"), card.get("session_id"),
            (card.get("executor") or {}).get("agent_id")} - {None, ""}


def candidate_repository(card: dict) -> str:
    """解析任务卡对应的主要候选代码仓库名称。"""
    explicit = card.get("candidate_repository")
    if explicit:
        return explicit
    scope = list((card.get("write_scope") or {}).keys())
    code_scope = [name for name in scope if name != "project-control"]
    if len(code_scope) == 1:
        return code_scope[0]
    if len(scope) == 1:
        return scope[0]
    raise ValueError("Task must identify its candidate repository")


def check_primary_identity(entry: dict, header: dict, card: dict) -> None:
    """在运行期与落盘门禁两条路径上强制校验主审人的非作者隔离性、Codex 平台属性与精确候选 Commit 绑定。"""
    session = entry.get("session") or entry.get("reviewer_session")
    if not session or str(session).startswith(("pending-", "planned-", "subagent-", "alias-")):
        raise ValueError("Actual independent reviewer session is required")
    if session in author_sessions(card):
        raise ValueError("Author cannot review own artifact")
    if entry.get("platform") != "codex":
        raise ValueError("Independent review requires platform codex")
    actual = header.get("actual_session") or header.get("actual_thread_id")
    if actual != session or header.get("decision") != "APPROVED" or entry.get("decision") != "APPROVED":
        raise ValueError("Primary review identity or decision mismatch")
    if header.get("task_id") != card.get("id") or header.get("task_revision") != card.get("revision"):
        raise ValueError("Primary review task/revision mismatch")
    if entry.get("reviewed_task_revision") != card.get("revision"):
        raise ValueError("Primary review assignment revision mismatch")
    roles = header.get("reviewer_roles") or [header.get("reviewer_role")]
    if entry.get("role") not in roles:
        raise ValueError("Primary review role mismatch")
    candidate = card.get("candidate_commit")
    version = header.get("reviewed_artifact_version")
    if not isinstance(candidate, str) or not re.fullmatch(r"[0-9a-f]{40}", candidate):
        raise ValueError("Primary review requires a full candidate commit")
    if len(set(candidate)) <= 1 or not isinstance(version, str) or entry.get("artifact_version") != version:
        raise ValueError("Primary review requires an exact candidate version")
    if version != candidate:
        versions = dict(item.split("=", 1) for item in version.split("; ") if "=" in item)
        if versions.get(candidate_repository(card)) != candidate:
            raise ValueError("Primary review candidate mismatch")
