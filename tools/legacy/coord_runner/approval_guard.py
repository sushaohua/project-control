#!/usr/bin/env python3
"""模块职责：精确版本人工批准单校验器与防伪造守卫（P1-03、P1-18、P1-19）。"""

from dataclasses import dataclass, field
import datetime
import hashlib
from pathlib import Path
import re
from typing import Dict, List, Optional
import yaml

from .errors import ApprovalValidationError

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
AUTHENTIC_HUMAN_CHANNELS = {
    "coord_interactive_session",
    "human_review_record",
    "signed_submission",
}
VALID_APPROVAL_MODES = {
    "full_batch_approval",
    "partial_batch_approval",
    "demand_only_confirmation",
    "rejected",
}
DEFAULT_MODEL = "gpt-6-luna"


@dataclass(frozen=True)
class ApprovalQuery:
    """检查特定需求或任务范围是否获准进入实现的查询结构体。"""
    demand_id: str
    approval_path: Optional[Path] = None
    expected_approval_sha256: Optional[str] = None
    expected_approval_revision: Optional[int] = None
    target_confirmation_id: Optional[str] = None
    target_confirmation_revision: Optional[int] = None
    target_confirmation_sha256: Optional[str] = None
    required_scope_item: Optional[str] = None
    requested_model: str = DEFAULT_MODEL
    record_payload: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ApprovalCheckResult:
    """针对需求或任务的确定性批准评估结果结构体。"""
    demand_id: str
    demand_confirmed: bool
    implementation_allowed: bool
    preparation_allowed: bool
    status: str
    reason: str
    approval_id: Optional[str] = None
    approval_sha256: Optional[str] = None
    confirmation_id: Optional[str] = None
    confirmation_revision: Optional[int] = None
    confirmation_sha256: Optional[str] = None
    approved_items: List[str] = field(default_factory=list)


def _is_strict_int(value: object) -> bool:
    """判断输入值是否为大于等于 1 的严格整型（排除 bool）。"""
    return type(value) is int and value >= 1


def _is_non_empty_str(value: object) -> bool:
    """判断输入值是否为去空白后非空的字符串。"""
    return isinstance(value, str) and bool(value.strip())


def _resolve_contained_path(workspace_root: Path, raw_path: str) -> Path:
    """解析并校验相对路径位于工作区边界内且对应真实文件。"""
    if not _is_non_empty_str(raw_path):
        raise ApprovalValidationError("Path reference is empty", "INVALID_PATH")
    rel = Path(raw_path)
    if rel.is_absolute() or ".." in rel.parts:
        raise ApprovalValidationError(f"Escaping path rejected: {raw_path}", "ESCAPING_PATH")
    ws = workspace_root.resolve()
    candidate = (ws / rel).resolve()
    if not candidate.is_file() and (ws / "project-control" / rel).is_file():
        candidate = (ws / "project-control" / rel).resolve()
    if candidate != ws and ws not in candidate.parents:
        raise ApprovalValidationError(f"Path escapes workspace: {raw_path}", "ESCAPING_PATH")
    if not candidate.is_file():
        raise ApprovalValidationError(f"Referenced file missing on disk: {raw_path}", "MISSING_FILE")
    return candidate


def _read_confirmation_header(conf_path: Path) -> dict:
    """读取确认单 YAML 或 Markdown YAML 头信息并返回字典。"""
    text = conf_path.read_text(encoding="utf-8")
    if conf_path.suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(text)
    else:
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            raise ApprovalValidationError(
                f"Confirmation markdown lacks YAML frontmatter: {conf_path}",
                "INVALID_CONFIRMATION_HEADER",
            )
        data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ApprovalValidationError("Confirmation metadata must be a mapping", "INVALID_CONFIRMATION_HEADER")
    return data


def _reject_forged_record_fields(payload: dict) -> None:
    """拦截模型或记录自填 `approved` 布尔字段及非法的 `approval_refs` 格式。"""
    if not isinstance(payload, dict):
        return
    if "approved" in payload:
        raise ApprovalValidationError(
            "Model/record self-filled 'approved' boolean is forbidden; bind APPR-*.yaml instead",
            "MODEL_SELF_APPROVED_REJECTED",
        )
    refs = payload.get("approval_refs")
    if refs is not None and not isinstance(refs, list):
        raise ApprovalValidationError("approval_refs must be a structured list", "INVALID_APPROVAL_REFS")


class ApprovalGuard:
    """执行精确版本人工（HUMAN）批准校验与防伪造核验的守卫类。"""

    def __init__(self, workspace_root: Path):
        """初始化批准守卫并绑定工作区根目录。"""
        if workspace_root is None:
            raise ValueError("workspace_root must not be None")
        self.workspace_root = Path(workspace_root).resolve()

    def _validate_approval_schema(self, data: object) -> dict:
        """校验批准单 YAML 顶层 Schema 版本、修订号、时间戳及批准模式。"""
        if not isinstance(data, dict):
            raise ApprovalValidationError("Approval YAML must be a dictionary", "INVALID_SCHEMA")
        if type(data.get("schema_version")) is not int or data.get("schema_version") != 1:
            raise ApprovalValidationError(
                f"Unsupported approval schema_version: {data.get('schema_version')!r}",
                "UNSUPPORTED_SCHEMA_VERSION",
            )
        if not _is_non_empty_str(data.get("approval_id")) or not _is_strict_int(data.get("revision")):
            raise ApprovalValidationError("Approval missing valid approval_id or revision", "INVALID_SCHEMA")
        approved_at = data.get("approved_at")
        if not _is_non_empty_str(approved_at):
            raise ApprovalValidationError("Approval missing approved_at timestamp", "INVALID_TIMESTAMP")
        try:
            datetime.datetime.fromisoformat(str(approved_at).replace("Z", "+00:00"))
        except ValueError as err:
            raise ApprovalValidationError(f"Invalid approved_at ISO timestamp: {approved_at}", "INVALID_TIMESTAMP") from err
        if data.get("approval_mode") not in VALID_APPROVAL_MODES:
            raise ApprovalValidationError(
                f"Invalid approval_mode: {data.get('approval_mode')!r}",
                "INVALID_APPROVAL_MODE",
            )
        return data

    def _validate_human_actor(self, approved_by: object) -> None:
        """校验 `approved_by` 必须来自受信任渠道的真实 HUMAN 角色且包含原文决定。"""
        if not isinstance(approved_by, dict):
            raise ApprovalValidationError("approved_by must be a mapping", "MISSING_HUMAN_SOURCE")
        if approved_by.get("actor_type") != "HUMAN":
            raise ApprovalValidationError(
                f"Approval actor_type must be exact 'HUMAN', got {approved_by.get('actor_type')!r}",
                "NON_HUMAN_ACTOR_REJECTED",
            )
        if not _is_non_empty_str(approved_by.get("actor_id")):
            raise ApprovalValidationError("approved_by.actor_id must be non-empty", "MISSING_HUMAN_SOURCE")
        channel = approved_by.get("source_channel")
        if channel not in AUTHENTIC_HUMAN_CHANNELS:
            raise ApprovalValidationError(
                f"Untrusted approval source_channel: {channel!r}",
                "UNTRUSTED_SOURCE_CHANNEL",
            )
        if not _is_non_empty_str(approved_by.get("verbatim_decision")):
            raise ApprovalValidationError("approved_by.verbatim_decision is required", "MISSING_VERBATIM_DECISION")

    def _verify_bound_confirmation(self, bound: object) -> dict:
        """核验批准单绑定的确认单磁盘 SHA-256 与 YAML 头信息一致。"""
        if not isinstance(bound, dict):
            raise ApprovalValidationError("bound_confirmation must be a mapping", "MISSING_CONFIRMATION_BINDING")
        conf_id = bound.get("confirmation_id")
        conf_rev = bound.get("revision")
        conf_sha = bound.get("sha256")
        if not _is_non_empty_str(conf_id) or not _is_strict_int(conf_rev):
            raise ApprovalValidationError("bound_confirmation missing confirmation_id or revision", "INVALID_CONFIRMATION_BINDING")
        if not isinstance(conf_sha, str) or not SHA256_RE.match(conf_sha):
            raise ApprovalValidationError("bound_confirmation.sha256 must be 64-hex", "INVALID_CONFIRMATION_SHA256")
        conf_file = _resolve_contained_path(self.workspace_root, str(bound.get("path", "")))
        real_sha = hashlib.sha256(conf_file.read_bytes()).hexdigest()
        if real_sha != conf_sha:
            raise ApprovalValidationError(
                f"Confirmation SHA256 mismatch on disk: approval={conf_sha}, actual={real_sha}",
                "CONFIRMATION_HASH_MISMATCH",
            )
        header = _read_confirmation_header(conf_file)
        if header.get("confirmation_id") != conf_id or header.get("revision") != conf_rev:
            raise ApprovalValidationError(
                f"Confirmation header ({header.get('confirmation_id')}, rev {header.get('revision')}) "
                f"does not match bound ({conf_id}, rev {conf_rev})",
                "CONFIRMATION_HEADER_MISMATCH",
            )
        return {"confirmation_id": conf_id, "revision": conf_rev, "sha256": real_sha}

    def load_and_verify_approval(
        self,
        approval_path: Path,
        expected_sha256: Optional[str] = None,
        expected_revision: Optional[int] = None,
    ) -> dict:
        """从磁盘加载批准单 YAML，核验摘要、HUMAN 来源及绑定确认单哈希。"""
        if approval_path is None:
            raise ApprovalValidationError("Missing approval_path", "MISSING_APPROVAL_REF")
        rel_or_abs = Path(approval_path)
        if rel_or_abs.is_absolute():
            target = rel_or_abs.resolve()
            if target != self.workspace_root and self.workspace_root not in target.parents:
                raise ApprovalValidationError("Approval file outside workspace", "ESCAPING_PATH")
            if not target.is_file():
                raise ApprovalValidationError(f"Approval file missing: {target}", "MISSING_FILE")
        else:
            target = _resolve_contained_path(self.workspace_root, str(rel_or_abs))
        raw_bytes = target.read_bytes()
        disk_sha = hashlib.sha256(raw_bytes).hexdigest()
        if expected_sha256 is not None and disk_sha != expected_sha256:
            raise ApprovalValidationError(
                f"Approval file SHA256 mismatch: expected {expected_sha256}, actual {disk_sha}",
                "APPROVAL_HASH_MISMATCH",
            )
        try:
            parsed = yaml.safe_load(raw_bytes.decode("utf-8"))
        except (UnicodeDecodeError, yaml.YAMLError) as err:
            raise ApprovalValidationError(f"Corrupt approval YAML {target}: {err}", "CORRUPT_APPROVAL_YAML") from err
        data = self._validate_approval_schema(parsed)
        if expected_revision is not None and data["revision"] != expected_revision:
            raise ApprovalValidationError(
                f"Approval revision mismatch: expected {expected_revision}, actual {data['revision']}",
                "APPROVAL_REVISION_MISMATCH",
            )
        self._validate_human_actor(data.get("approved_by"))
        conf_info = self._verify_bound_confirmation(data.get("bound_confirmation"))
        out = dict(data)
        out["_disk_sha256"] = disk_sha
        out["_verified_confirmation"] = conf_info
        return out

    def _check_target_confirmation_match(self, query: ApprovalQuery, verified_conf: dict) -> None:
        """核验查询请求的目标确认单 ID、修订号及哈希与已验证确认单完全一致。"""
        if query.target_confirmation_id and query.target_confirmation_id != verified_conf["confirmation_id"]:
            raise ApprovalValidationError(
                f"Confirmation ID mismatch: target={query.target_confirmation_id}, "
                f"approved={verified_conf['confirmation_id']}",
                "CONFIRMATION_ID_MISMATCH",
            )
        if query.target_confirmation_revision is not None:
            if query.target_confirmation_revision != verified_conf["revision"]:
                raise ApprovalValidationError(
                    f"Stale/mismatched confirmation revision: target rev {query.target_confirmation_revision} "
                    f"cannot reuse approval bound to rev {verified_conf['revision']}",
                    "STALE_CONFIRMATION_REVISION",
                )
        if query.target_confirmation_sha256 and query.target_confirmation_sha256 != verified_conf["sha256"]:
            raise ApprovalValidationError(
                f"Target confirmation SHA256 {query.target_confirmation_sha256} does not match "
                f"approved SHA256 {verified_conf['sha256']}",
                "STALE_CONFIRMATION_HASH",
            )

    def _validate_demand_entry_and_model(self, entry: dict, requested_model: str) -> None:
        """校验需求条目布尔标记与请求模型是否符合批准单中的模型策略。"""
        if type(entry.get("demand_confirmed")) is not bool:
            raise ApprovalValidationError("demand_confirmed must be strict bool", "INVALID_DEMAND_ENTRY")
        if type(entry.get("implementation_summary_approved")) is not bool:
            raise ApprovalValidationError(
                "implementation_summary_approved must be strict bool",
                "INVALID_DEMAND_ENTRY",
            )
        policy = entry.get("model_policy") or {}
        if not isinstance(policy, dict):
            raise ApprovalValidationError("model_policy must be a mapping", "INVALID_MODEL_POLICY")
        default_m = policy.get("default_model", DEFAULT_MODEL)
        overrides = policy.get("overrides_approved", [])
        if default_m != DEFAULT_MODEL or not isinstance(overrides, list):
            raise ApprovalValidationError("Invalid model_policy in approval", "INVALID_MODEL_POLICY")
        if requested_model != DEFAULT_MODEL and requested_model not in overrides:
            raise ApprovalValidationError(
                f"Requested model {requested_model!r} is not approved (default={DEFAULT_MODEL})",
                "UNAPPROVED_MODEL_OVERRIDE",
            )

    def _evaluate_demand_scope(
        self,
        query: ApprovalQuery,
        approval_data: dict,
        entry: Optional[dict],
    ) -> ApprovalCheckResult:
        """评估具体需求条目及其子范围在批准单中的放行状态。"""
        vconf = approval_data["_verified_confirmation"]
        base_kwargs = {
            "demand_id": query.demand_id,
            "approval_id": approval_data["approval_id"],
            "approval_sha256": approval_data["_disk_sha256"],
            "confirmation_id": vconf["confirmation_id"],
            "confirmation_revision": vconf["revision"],
            "confirmation_sha256": vconf["sha256"],
        }
        mode = approval_data["approval_mode"]
        if mode == "rejected" or entry is None or entry.get("demand_confirmed") is not True:
            return ApprovalCheckResult(
                demand_confirmed=False, implementation_allowed=False, preparation_allowed=True,
                status="PENDING_APPROVAL", reason="DEMAND_NOT_APPROVED_IN_BATCH", **base_kwargs,
            )
        self._validate_demand_entry_and_model(entry, query.requested_model)
        items = list(entry.get("approved_items") or [])
        unapproved = set(entry.get("unapproved_items") or [])
        if mode == "demand_only_confirmation" or entry.get("implementation_summary_approved") is not True:
            return ApprovalCheckResult(
                demand_confirmed=True, implementation_allowed=False, preparation_allowed=True,
                status="DEMAND_CONFIRMED_ONLY", reason="IMPLEMENTATION_SUMMARY_UNAPPROVED",
                approved_items=items, **base_kwargs,
            )
        req_item = query.required_scope_item
        if req_item and (req_item in unapproved or (items and req_item not in items)):
            return ApprovalCheckResult(
                demand_confirmed=True, implementation_allowed=False, preparation_allowed=True,
                status="SUBSCOPE_UNAPPROVED", reason=f"SUBSCOPE_NOT_APPROVED:{req_item}",
                approved_items=items, **base_kwargs,
            )
        return ApprovalCheckResult(
            demand_confirmed=True, implementation_allowed=True, preparation_allowed=True,
            status="APPROVED_FOR_IMPLEMENTATION", reason="EXACT_HUMAN_APPROVAL_VERIFIED",
            approved_items=items, **base_kwargs,
        )

    def check_demand_release(self, query: ApprovalQuery) -> ApprovalCheckResult:
        """评估查询对象是否具备有效的精确版本 HUMAN 实现批准。"""
        if not _is_non_empty_str(query.demand_id):
            raise ApprovalValidationError("ApprovalQuery requires non-empty demand_id", "MISSING_DEMAND_ID")
        _reject_forged_record_fields(query.record_payload)
        if query.approval_path is None:
            return ApprovalCheckResult(
                demand_id=query.demand_id, demand_confirmed=False, implementation_allowed=False,
                preparation_allowed=True, status="NO_APPROVAL_BOUND",
                reason="NO_AUTHENTIC_APPROVAL_REF",
            )
        approval_data = self.load_and_verify_approval(
            query.approval_path, query.expected_approval_sha256, query.expected_approval_revision,
        )
        self._check_target_confirmation_match(query, approval_data["_verified_confirmation"])
        demands = approval_data.get("approved_demands")
        if not isinstance(demands, list):
            raise ApprovalValidationError("approved_demands must be a list", "INVALID_SCHEMA")
        matched = next((d for d in demands if isinstance(d, dict) and d.get("demand_id") == query.demand_id), None)
        return self._evaluate_demand_scope(query, approval_data, matched)

    def require_implementation_approval(self, query: ApprovalQuery) -> ApprovalCheckResult:
        """断言需求已获准进入实现阶段，否则抛出 `ApprovalValidationError`。"""
        result = self.check_demand_release(query)
        if not result.implementation_allowed:
            raise ApprovalValidationError(
                f"Implementation blocked for {query.demand_id}: {result.status} ({result.reason})",
                result.status,
            )
        return result

    def check_intake_record(self, record: dict) -> ApprovalCheckResult:
        """评估收件分类 YAML 记录的批准状态，绝不盲信 `enabled=true` 或正文关键字。"""
        _reject_forged_record_fields(record)
        demand_ref = record.get("demand_ref") or {}
        demand_id = str(demand_ref.get("demand_id", "")).strip()
        refs = record.get("approval_refs") or []
        if not refs:
            return ApprovalCheckResult(
                demand_id=demand_id or "UNKNOWN", demand_confirmed=False,
                implementation_allowed=False, preparation_allowed=bool(record.get("enabled", False)),
                status="NO_APPROVAL_BOUND", reason="NO_APPROVAL_REFS_BOUND",
            )
        first_ref = refs[0]
        if not isinstance(first_ref, dict) or not _is_non_empty_str(first_ref.get("path")):
            raise ApprovalValidationError("approval_refs entry missing valid path", "INVALID_APPROVAL_REFS")
        query = ApprovalQuery(
            demand_id=demand_id,
            approval_path=Path(first_ref["path"]),
            expected_approval_sha256=first_ref.get("sha256"),
            expected_approval_revision=first_ref.get("revision"),
            target_confirmation_id=demand_ref.get("confirmation_id"),
            target_confirmation_revision=demand_ref.get("confirmation_revision"),
            target_confirmation_sha256=demand_ref.get("confirmation_sha256"),
            required_scope_item=record.get("required_scope_item"),
            record_payload=record,
        )
        return self.check_demand_release(query)

    def evaluate_batch_records(self, records: List[dict]) -> Dict[str, ApprovalCheckResult]:
        """独立评估一批收件记录，确保未批准条目不会阻塞同批已批准条目。"""
        results: Dict[str, ApprovalCheckResult] = {}
        for rec in records:
            rec_id = str(rec.get("id") or (rec.get("demand_ref") or {}).get("demand_id") or "UNKNOWN")
            try:
                results[rec_id] = self.check_intake_record(rec)
            except ApprovalValidationError as err:
                demand_id = str((rec.get("demand_ref") or {}).get("demand_id") or rec_id)
                results[rec_id] = ApprovalCheckResult(
                    demand_id=demand_id, demand_confirmed=False, implementation_allowed=False,
                    preparation_allowed=False, status=err.code, reason=str(err),
                )
        return results
