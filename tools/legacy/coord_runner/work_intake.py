#!/usr/bin/env python3
"""人工 Markdown 批量收件解析器、三类唯一 YAML 归档生成器与故障隔离器。"""

from dataclasses import dataclass, field
import datetime
import json
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple
import yaml

from .cas_writer import WriteIntent, compute_bytes_sha256, create_exclusive, read_with_digest, write_cas
from .errors import IntakeValidationError

SUPPORTED_SCHEMA_VERSION = 1
CATEGORY_DIRS = {"issue": "issues", "feature": "features", "requirement": "requirements"}
CATEGORY_PREFIXES = {"issue": "ISS", "feature": "FEAT", "requirement": "REQ"}
VALID_ACTIONS = {"triage", "clarify", "plan", "execute"}
FORBIDDEN_PATH_PREFIXES = (
    "soc-ap/", "mcu-p3/", "test_harness/", "boot/bootloadermc/", "boot/bootloaderth/",
)
HEADING_INSTRUCTION_RE = re.compile(r"^#{2,3}\s*(?:指令|Instruction)\s*(\d+)[^\n]*$", re.MULTILINE)
NUMBERED_ITEM_RE = re.compile(r"^\s*(\d+)[\.\)]\s+(.+)$")
CONSTRAINTS_HEADING_RE = re.compile(r"^#{1,3}\s*(?:公共约束|全局约束|Common Constraints)\s*$", re.IGNORECASE)
SHELL_LIKE_RE = re.compile(
    r"(?:\brm\s+-rf\b|\$\([^)]+\)|`[^`]+`|;\s*(?:sh|bash|rm|sudo|reboot)\b|```(?:sh|bash))",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ParsedInstruction:
    """Single verbatim human instruction mapped 1:1 to a stable demand."""
    index: int
    anchor: str
    verbatim_text: str
    instruction_sha256: str
    inferred_kind: str
    title: str
    contains_shell_text: bool
    explicit_demand_id: Optional[str] = None
    explicit_category_id: Optional[str] = None
    root_cause_status: str = "unknown"
    clarity_status: str = "clear"
    owner_role: Optional[str] = None


@dataclass(frozen=True)
class ParsedSubmission:
    """Parsed human Markdown batch submission with verbatim instructions and constraints."""
    submission_id: str
    revision: int
    path: Path
    file_sha256: str
    reported_by: dict
    common_constraints: List[str]
    common_constraints_sha256: str
    instructions: List[ParsedInstruction]
    raw_archive_ref: dict
    enabled: bool = True


@dataclass(frozen=True)
class IntakeErrorRecord:
    """Structured error isolating a malformed, conflicting, or tampered intake file."""
    path: str
    code: str
    message: str


@dataclass(frozen=True)
class IntakeLifecycleNotice:
    """Non-destructive notice when disabled/deleted intake encounters active work (P1-16)."""
    code: str
    item_id: str
    task_ids: List[str]
    action: str
    message: str


@dataclass
class IntakeScanResult:
    """Aggregated result of scanning submissions and category YAML directories."""
    submissions: List[ParsedSubmission] = field(default_factory=list)
    generated_paths: List[Path] = field(default_factory=list)
    records: Dict[str, dict] = field(default_factory=dict)
    errors: List[IntakeErrorRecord] = field(default_factory=list)
    notices: List[IntakeLifecycleNotice] = field(default_factory=list)


@dataclass(frozen=True)
class TaskLinkUpdate:
    """封装分类 YAML 与正式看板任务、确认单、批准单及 ARCH 拆解文档的关联更新参数。"""

    category_yaml_path: Path
    task_ids: List[str]
    demand_ref_updates: Optional[dict] = None
    approval_refs: Optional[List[dict]] = None
    requested_action: Optional[str] = None
    arch_breakdown: Optional[dict] = None


def _split_optional_frontmatter(raw_text: str) -> Tuple[dict, str]:
    if not raw_text.startswith("---\n") and not raw_text.startswith("---\r\n"):
        return {}, raw_text
    parts = raw_text.split("---", 2)
    if len(parts) != 3:
        raise IntakeValidationError("Truncated YAML frontmatter in submission", "CORRUPT_SUBMISSION")
    try:
        meta = yaml.safe_load(parts[1])
    except yaml.YAMLError as err:
        raise IntakeValidationError(f"Invalid YAML frontmatter: {err}", "CORRUPT_SUBMISSION") from err
    if meta is None:
        meta = {}
    if not isinstance(meta, dict):
        raise IntakeValidationError("Submission frontmatter must be a mapping", "INVALID_SUBMISSION_SCHEMA")
    return meta, parts[2]


def _unwrap_verbatim_fence(block: str) -> str:
    stripped = block.strip()
    lines = stripped.splitlines()
    if len(lines) >= 2 and lines[0].strip().startswith("```") and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()
    return stripped


def _extract_constraints_and_body(body_text: str) -> Tuple[List[str], str]:
    constraints: List[str] = []
    remaining: List[str] = []
    in_constraints = False
    for line in body_text.splitlines():
        if CONSTRAINTS_HEADING_RE.match(line.strip()):
            in_constraints = True
            continue
        if in_constraints and line.lstrip().startswith("#"):
            in_constraints = False
        if in_constraints:
            cleaned = re.sub(r"^\s*[-\*\d\.\)]+\s*", "", line).strip()
            if cleaned:
                constraints.append(cleaned)
        else:
            remaining.append(line)
    return constraints, "\n".join(remaining)


def _split_raw_instructions(clean_body: str) -> List[str]:
    matches = list(HEADING_INSTRUCTION_RE.finditer(clean_body))
    if matches:
        blocks = []
        for idx, match in enumerate(matches):
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(clean_body)
            text = _unwrap_verbatim_fence(clean_body[start:end])
            if text:
                blocks.append(text)
        return blocks
    numbered: List[List[str]] = []
    for line in clean_body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        m = NUMBERED_ITEM_RE.match(line)
        if m:
            numbered.append([m.group(2).strip()])
        elif numbered and stripped:
            numbered[-1].append(stripped)
    if numbered:
        return ["\n".join(parts).strip() for parts in numbered if parts]
    whole = _unwrap_verbatim_fence("\n".join(
        ln for ln in clean_body.splitlines() if not ln.strip().startswith("# ")
    ))
    return [whole] if whole else []


def _classify_instruction_metadata(text: str, mapping: dict) -> dict:
    explicit_cat = mapping.get("primary_category")
    lower = text.lower()
    if explicit_cat in CATEGORY_DIRS:
        kind = explicit_cat
    elif any(tag in lower for tag in ("[issue]", "【问题】", "【故障】", "故障", "报错", "崩溃", "异常")):
        kind = "issue"
    elif any(tag in lower for tag in ("[requirement]", "【需求】", "【澄清】", "待澄清", "目标不清", "目标待定")):
        kind = "requirement"
    else:
        kind = "feature"
    clarity = "unclear" if any(k in lower for k in ("待澄清", "目标不清", "不明确", "待定", "unclear")) else "clear"
    rc_status = "known" if any(k in lower for k in ("根因明确", "已知根因", "root_cause=known")) else "unknown"
    owner_match = re.search(r"\b(ENG-[A-Z]+|ENG_BOOT_(?:MC|TH)|INTEGRATOR)\b", text)
    first_line = re.sub(r"^\[(?:issue|feature|requirement)\]\s*", "", text.splitlines()[0], flags=re.I)
    title = re.sub(r"^【(?:问题|故障|功能|需求|澄清)】\s*", "", first_line).strip()[:96]
    return {
        "kind": kind,
        "clarity": mapping.get("clarity_status", clarity),
        "root_cause": mapping.get("root_cause_status", rc_status),
        "owner_role": mapping.get("owner_role") or (owner_match.group(1) if owner_match else None),
        "title": title or f"{kind} instruction",
    }


def _validate_submission_meta(meta: dict, path: Path) -> Tuple[str, int, dict, bool]:
    if "schema_version" in meta:
        if type(meta["schema_version"]) is not int or meta["schema_version"] != SUPPORTED_SCHEMA_VERSION:
            raise IntakeValidationError(
                f"Unsupported submission schema_version: {meta.get('schema_version')!r}",
                "UNSUPPORTED_SCHEMA_VERSION",
            )
    sub_id = str(meta.get("submission_id") or path.stem).strip()
    rev = meta.get("revision", 1)
    if not sub_id or type(rev) is not int or rev < 1:
        raise IntakeValidationError("Invalid submission_id or revision", "INVALID_SUBMISSION_SCHEMA")
    rep = meta.get("reported_by") or {
        "actor_type": "HUMAN",
        "actor_id": "human_markdown_author",
        "source_channel": "markdown_submission",
    }
    if not isinstance(rep, dict) or rep.get("actor_type") != "HUMAN" or not str(rep.get("actor_id", "")).strip():
        raise IntakeValidationError("Phase 1 submissions must have reported_by.actor_type=='HUMAN'", "NON_HUMAN_SUBMITTER")
    enabled = meta.get("enabled", not bool(meta.get("example_only", False)))
    if type(enabled) is not bool:
        raise IntakeValidationError("submission enabled flag must be bool", "INVALID_SUBMISSION_SCHEMA")
    return sub_id, rev, rep, enabled


def parse_submission_markdown(path: Path) -> ParsedSubmission:
    """Parse a human Markdown batch file into 1:1 verbatim instructions without running shell text."""
    snap = read_with_digest(path)
    try:
        raw_text = snap.text
    except UnicodeDecodeError as err:
        raise IntakeValidationError(f"Non-UTF8 submission {path}: {err}", "CORRUPT_SUBMISSION") from err
    meta, body = _split_optional_frontmatter(raw_text)
    sub_id, rev, reported_by, enabled = _validate_submission_meta(meta, snap.path)
    fm_constraints = [str(c).strip() for c in (meta.get("common_constraints") or []) if str(c).strip()]
    md_constraints, clean_body = _extract_constraints_and_body(body)
    all_constraints = fm_constraints + [c for c in md_constraints if c not in fm_constraints]
    constraints_sha = compute_bytes_sha256("\n".join(all_constraints))
    raw_blocks = _split_raw_instructions(clean_body)
    if not raw_blocks:
        raise IntakeValidationError(f"Submission {sub_id} contains zero instructions", "EMPTY_SUBMISSION")
    mappings = {
        int(m["instruction_index"]): m
        for m in (meta.get("demand_mappings") or [])
        if isinstance(m, dict) and type(m.get("instruction_index")) is int
    }
    instructions: List[ParsedInstruction] = []
    for idx, text in enumerate(raw_blocks, start=1):
        mp = mappings.get(idx, {})
        info = _classify_instruction_metadata(text, mp)
        instructions.append(ParsedInstruction(
            index=idx,
            anchor=f"instruction_{idx}",
            verbatim_text=text,
            instruction_sha256=compute_bytes_sha256(text),
            inferred_kind=info["kind"],
            title=info["title"],
            contains_shell_text=bool(SHELL_LIKE_RE.search(text)),
            explicit_demand_id=mp.get("demand_id"),
            explicit_category_id=mp.get("category_item_id"),
            root_cause_status=info["root_cause"],
            clarity_status=info["clarity"],
            owner_role=info["owner_role"],
        ))
    archive_ref = meta.get("raw_archive_ref") if isinstance(meta.get("raw_archive_ref"), dict) else {}
    return ParsedSubmission(
        submission_id=sub_id, revision=rev, path=snap.path, file_sha256=snap.sha256,
        reported_by=reported_by, common_constraints=all_constraints,
        common_constraints_sha256=constraints_sha, instructions=instructions,
        raw_archive_ref=archive_ref, enabled=enabled,
    )


def _check_category_record_fields(data: dict, expected_kind: str) -> None:
    if type(data.get("schema_version")) is not int or data.get("schema_version") != SUPPORTED_SCHEMA_VERSION:
        raise IntakeValidationError(f"Unsupported schema_version: {data.get('schema_version')!r}", "UNSUPPORTED_SCHEMA_VERSION")
    if "approved" in data:
        raise IntakeValidationError("Self-filled 'approved' field forbidden in intake YAML", "MODEL_SELF_APPROVED_REJECTED")
    if data.get("kind") != expected_kind:
        raise IntakeValidationError(
            f"Directory-kind conflict: file in {CATEGORY_DIRS[expected_kind]}/ has kind={data.get('kind')!r}",
            "DIRECTORY_KIND_CONFLICT",
        )
    if type(data.get("revision")) is not int or data["revision"] < 1 or type(data.get("enabled")) is not bool:
        raise IntakeValidationError("Invalid revision or enabled field type", "INVALID_FIELD_TYPE")
    for req_str in ("id", "title", "objective", "priority_hint"):
        if not isinstance(data.get(req_str), str) or not data[req_str].strip():
            raise IntakeValidationError(f"Missing or empty required string field: {req_str}", "MISSING_REQUIRED_FIELD")
    if data.get("requested_action") not in VALID_ACTIONS:
        raise IntakeValidationError(f"Invalid requested_action: {data.get('requested_action')!r}", "INVALID_REQUESTED_ACTION")


def _check_category_record_refs(data: dict) -> None:
    src = data.get("source_refs")
    dem = data.get("demand_ref")
    rep = data.get("reported_by")
    if not isinstance(src, dict) or not str(src.get("submission_id", "")).strip() or not str(src.get("submission_sha256", "")).strip():
        raise IntakeValidationError("source_refs missing mandatory submission_id or submission_sha256", "INVALID_SOURCE_REFS")
    has_verbatim = bool(str(src.get("verbatim_instruction", "")).strip())
    has_archive = bool(str(src.get("raw_archive_path", "")).strip() and str(src.get("raw_archive_sha256", "")).strip())
    if not has_verbatim and not has_archive:
        raise IntakeValidationError("source_refs must preserve verbatim_instruction or raw_archive_ref", "MISSING_VERBATIM_SOURCE")
    if not isinstance(dem, dict) or not str(dem.get("demand_id", "")).strip():
        raise IntakeValidationError("demand_ref missing mandatory demand_id", "INVALID_DEMAND_REF")
    if not isinstance(rep, dict) or rep.get("actor_type") != "HUMAN" or not str(rep.get("actor_id", "")).strip():
        raise IntakeValidationError("reported_by must identify an authentic HUMAN actor", "NON_HUMAN_SUBMITTER")
    if not isinstance(data.get("authorization_refs"), list) or not isinstance(data.get("approval_refs"), list):
        raise IntakeValidationError("authorization_refs and approval_refs must be lists", "INVALID_REFS_LIST")
    if not isinstance(data.get("related_ids"), (dict, list)):
        raise IntakeValidationError("related_ids must be dict or list", "INVALID_RELATED_IDS")
    for target_path in data.get("target_paths") or []:
        norm = str(target_path).lstrip("./")
        if ".." in Path(norm).parts or norm.startswith(FORBIDDEN_PATH_PREFIXES):
            raise IntakeValidationError(f"Forbidden target path in Phase 1 intake: {target_path}", "SCOPE_BOUNDARY_REJECTED")


class WorkIntakeManager:
    """Manages `docs/work_intake/` parsing, unique YAML generation, tamper ledger, and task linkage."""

    def __init__(self, workspace_root: Path, intake_root: Optional[Path] = None, reconciler: Optional[object] = None):
        """初始化人工收件管理器，解析工作区与收件目录路径并绑定对账器。

        参数：
        - workspace_root (Path)：工作区根目录路径。
        - intake_root (Optional[Path])：可选的收件目录路径（相对路径基于 `workspace_root` 解析）。
        - reconciler (Optional[object])：可选的五源对账器实例，用于记录与核验幂等摘要。
        """
        self.workspace_root = Path(workspace_root).resolve()
        default_intake = self.workspace_root / "project-control/docs/work_intake"
        if intake_root is None:
            self.intake_root = default_intake.resolve()
        else:
            raw_in = Path(intake_root)
            self.intake_root = raw_in.resolve() if raw_in.is_absolute() else (self.workspace_root / raw_in).resolve()
        self.ledger_path = self.intake_root / ".intake_digests.json"
        self.reconciler = reconciler

    def _load_ledger(self) -> dict:
        if not self.ledger_path.is_file():
            return {"submissions": {}, "categories": {}, "ingested_instructions": {}}
        try:
            data = json.loads(self.ledger_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("submissions", {})
                data.setdefault("categories", {})
                data.setdefault("ingested_instructions", {})
                return data
        except (OSError, json.JSONDecodeError):
            pass
        return {"submissions": {}, "categories": {}, "ingested_instructions": {}}

    def _save_ledger(self, ledger: dict) -> None:
        """将收件摘要账本以 CAS 方式写回磁盘；若账本内容未变化或无收件目录且账本为空则幂等短路返回。

        参数：
        - ledger (dict)：包含 `submissions`、`categories` 与 `ingested_instructions` 的摘要账本字典。

        返回值：
        - None：无返回值。
        """
        payload = json.dumps(ledger, indent=2, ensure_ascii=False, sort_keys=True)
        if self.ledger_path.is_file():
            snap = read_with_digest(self.ledger_path)
            if snap.text == payload:
                return
            write_cas(self.ledger_path, payload, snap.sha256)
            return
        if not self.intake_root.is_dir() and not any(ledger.values()):
            return
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        create_exclusive(self.ledger_path, payload)

    def _check_and_bind_digest(self, bucket: dict, item_id: str, rev_and_sha: Tuple[int, str]) -> None:
        rev, sha = rev_and_sha
        key = f"{item_id}@r{rev}"
        recorded = bucket.get(key)
        if recorded is not None and recorded != sha:
            raise IntakeValidationError(
                f"Same (id={item_id}, revision={rev}) content tampered: recorded={recorded}, actual={sha}",
                "TAMPERED_SAME_REVISION",
            )
        bucket[key] = sha

    def _scan_category_files(self, ledger: dict, result: IntakeScanResult) -> Tuple[set, Dict[str, str]]:
        used_ids: set = set()
        demand_to_cat: Dict[str, str] = {}
        tracker = (ledger, used_ids, demand_to_cat, result)
        for expected_kind, folder_name in CATEGORY_DIRS.items():
            folder = self.intake_root / folder_name
            if not folder.is_dir():
                continue
            for path in sorted(folder.iterdir()):
                if path.name == ".gitkeep" or path.is_dir():
                    continue
                if path.name.startswith(".") or path.suffix not in {".yaml", ".yml"}:
                    result.errors.append(IntakeErrorRecord(str(path), "TEMP_OR_UNSUPPORTED_FILE", f"Ignored/isolated non-YAML file: {path.name}"))
                    continue
                self._validate_single_category_file(path, expected_kind, tracker)
        return used_ids, demand_to_cat

    def _validate_single_category_file(
        self,
        path: Path,
        expected_kind: str,
        tracker: Tuple[dict, set, Dict[str, str], IntakeScanResult],
    ) -> None:
        ledger, used_ids, demand_to_cat, result = tracker
        try:
            snap = read_with_digest(path)
            data = yaml.safe_load(snap.text)
            if not isinstance(data, dict):
                raise IntakeValidationError("Category YAML must parse to a dictionary", "CORRUPT_CATEGORY_YAML")
            _check_category_record_fields(data, expected_kind)
            _check_category_record_refs(data)
            rec_id = data["id"]
            dem_id = data["demand_ref"]["demand_id"]
            if rec_id in used_ids:
                raise IntakeValidationError(f"Duplicate category ID across intake directories: {rec_id}", "DUPLICATE_CATEGORY_ID")
            if dem_id in demand_to_cat:
                raise IntakeValidationError(
                    f"Demand {dem_id} duplicated across categories ({demand_to_cat[dem_id]} and {rec_id})",
                    "DUPLICATE_PRIMARY_CATEGORY",
                )
            self._check_and_bind_digest(ledger["categories"], rec_id, (data["revision"], snap.sha256))
            used_ids.add(rec_id)
            used_ids.add(dem_id)
            demand_to_cat[dem_id] = rec_id
            data["_path"] = str(path)
            data["_sha256"] = snap.sha256
            result.records[rec_id] = data
        except (UnicodeDecodeError, yaml.YAMLError, OSError) as err:
            result.errors.append(IntakeErrorRecord(str(path), "CORRUPT_CATEGORY_YAML", str(err)))
        except IntakeValidationError as err:
            result.errors.append(IntakeErrorRecord(str(path), err.code, str(err)))

    def _allocate_unique_id(self, prefix: str, date_tag: str, used_ids: set) -> str:
        seq = 1
        while True:
            candidate = f"{prefix}-{date_tag}-{seq:03d}"
            if candidate not in used_ids:
                used_ids.add(candidate)
                return candidate
            seq += 1

    def _find_existing_instruction_record(self, sub_id: str, inst: ParsedInstruction, records: Dict[str, dict]) -> Optional[dict]:
        for rec in records.values():
            if inst.explicit_category_id and rec.get("id") == inst.explicit_category_id:
                return rec
            if inst.explicit_demand_id and (rec.get("demand_ref") or {}).get("demand_id") == inst.explicit_demand_id:
                return rec
            src = rec.get("source_refs") or {}
            if src.get("submission_id") == sub_id:
                if src.get("instruction_sha256") and src.get("instruction_sha256") == inst.instruction_sha256:
                    return rec
                if not src.get("instruction_sha256") and src.get("instruction_anchor") == inst.anchor:
                    return rec
        return None

    def _build_category_payload(
        self,
        sub: ParsedSubmission,
        inst: ParsedInstruction,
        ids: Tuple[str, str],
    ) -> dict:
        demand_id, cat_id = ids
        rel_sub = self._rel_path(sub.path)
        src_refs = {
            "submission_id": sub.submission_id,
            "submission_revision": sub.revision,
            "instruction_anchor": inst.anchor,
            "submission_path": rel_sub,
            "submission_sha256": sub.file_sha256,
            "instruction_sha256": inst.instruction_sha256,
            "verbatim_instruction": inst.verbatim_text,
            "common_constraints": list(sub.common_constraints),
            "common_constraints_sha256": sub.common_constraints_sha256,
        }
        if sub.raw_archive_ref.get("path") and sub.raw_archive_ref.get("sha256"):
            src_refs["raw_archive_path"] = sub.raw_archive_ref["path"]
            src_refs["raw_archive_sha256"] = sub.raw_archive_ref["sha256"]
        payload = {
            "schema_version": SUPPORTED_SCHEMA_VERSION,
            "id": cat_id,
            "revision": 1,
            "kind": inst.inferred_kind,
            "enabled": sub.enabled,
            "title": inst.title,
            "objective": inst.verbatim_text,
            "source_refs": src_refs,
            "demand_ref": {"demand_id": demand_id, "confirmation_id": None, "confirmation_revision": None, "confirmation_path": None, "confirmation_sha256": None},
            "reported_by": dict(sub.reported_by),
            "authorization_refs": [{"path": rel_sub, "revision": sub.revision, "sha256": sub.file_sha256}],
            "approval_refs": [],
            "requested_action": "clarify" if inst.clarity_status == "unclear" else "triage",
            "priority_hint": "P2",
            "related_ids": {"engineering_tasks": []},
            "triage_metadata": {"root_cause_status": inst.root_cause_status, "clarity_status": inst.clarity_status, "proposed_owner_role": inst.owner_role},
            "safety_flags": {"shell_execution_disabled": True, "contains_shell_like_text": inst.contains_shell_text},
        }
        return payload

    def _rel_path(self, path: Path) -> str:
        try:
            return str(path.resolve().relative_to(self.workspace_root))
        except ValueError:
            return str(path)

    def _verify_submission_against_records(self, sub: ParsedSubmission, records: Dict[str, dict]) -> None:
        for rec in records.values():
            src = rec.get("source_refs") or {}
            if src.get("submission_id") == sub.submission_id and src.get("submission_revision") == sub.revision:
                expected_sha = src.get("submission_sha256")
                if expected_sha and expected_sha != sub.file_sha256:
                    raise IntakeValidationError(
                        f"Submission ({sub.submission_id}, rev {sub.revision}) content modified without bumping revision",
                        "TAMPERED_SAME_REVISION",
                    )

    def _ingest_single_submission(
        self,
        md_path: Path,
        state: Tuple[dict, set, Dict[str, str]],
        result: IntakeScanResult,
    ) -> None:
        ledger, used_ids, demand_to_cat = state
        try:
            sub = parse_submission_markdown(md_path)
            self._verify_submission_against_records(sub, result.records)
            self._check_and_bind_digest(ledger["submissions"], sub.submission_id, (sub.revision, sub.file_sha256))
        except (IntakeValidationError, OSError) as err:
            code = err.code if isinstance(err, IntakeValidationError) else "IO_ERROR"
            result.errors.append(IntakeErrorRecord(str(md_path), code, str(err)))
            return
        result.submissions.append(sub)
        date_tag = datetime.date.today().strftime("%Y%m%d")
        for inst in sub.instructions:
            inst_key = f"{sub.submission_id}@r{sub.revision}:{inst.instruction_sha256}"
            existing = self._find_existing_instruction_record(sub.submission_id, inst, result.records)
            if existing is not None or inst_key in ledger["ingested_instructions"]:
                if existing is not None:
                    ledger["ingested_instructions"][inst_key] = existing["id"]
                    if self.reconciler is not None:
                        dem_id = (existing.get("demand_ref") or {}).get("demand_id") or existing["id"]
                        rev = int(existing.get("revision", 1))
                        content_sha = existing.get("_sha256") or sub.file_sha256
                        self.reconciler.check_intake_idempotence(dem_id, rev, content_sha)
                continue
            dem_id = inst.explicit_demand_id or self._allocate_unique_id("DEM", date_tag, used_ids)
            used_ids.add(dem_id)
            cat_prefix = CATEGORY_PREFIXES[inst.inferred_kind]
            cat_id = inst.explicit_category_id or self._allocate_unique_id(cat_prefix, date_tag, used_ids)
            used_ids.add(cat_id)
            payload = self._build_category_payload(sub, inst, (dem_id, cat_id))
            out_path = self.intake_root / CATEGORY_DIRS[inst.inferred_kind] / f"{cat_id}.yaml"
            yaml_text = yaml.safe_dump(payload, allow_unicode=True, sort_keys=False)
            sha = create_exclusive(out_path, yaml_text)
            ledger["categories"][f"{cat_id}@r1"] = sha
            ledger["ingested_instructions"][inst_key] = cat_id
            demand_to_cat[dem_id] = cat_id
            payload["_path"] = str(out_path)
            payload["_sha256"] = sha
            if self.reconciler is not None:
                self.reconciler.record_intake_digest(dem_id, 1, sha)
            result.generated_paths.append(out_path)
            result.records[cat_id] = payload

    def scan_and_sync(self, persist_ledger: bool = True, active_cards: Optional[Dict[str, dict]] = None) -> IntakeScanResult:
        """Scan `submissions/` and 3 category dirs, auto-generate missing YAMLs, and isolate bad records."""
        result = IntakeScanResult()
        ledger = self._load_ledger()
        used_ids, demand_to_cat = self._scan_category_files(ledger, result)
        used_ids.update(k.split("@r", 1)[0] for k in ledger.get("categories", {}))
        sub_dir = self.intake_root / "submissions"
        if sub_dir.is_dir():
            for path in sorted(sub_dir.iterdir()):
                if path.name == ".gitkeep" or path.is_dir():
                    continue
                if path.name.startswith(".") or path.suffix.lower() != ".md":
                    result.errors.append(IntakeErrorRecord(str(path), "TEMP_OR_UNSUPPORTED_FILE", f"Ignored non-MD file: {path.name}"))
                    continue
                self._ingest_single_submission(path, (ledger, used_ids, demand_to_cat), result)
        if active_cards:
            self._reconcile_in_flight_notices(result, active_cards)
        if persist_ledger:
            self._save_ledger(ledger)
        return result

    def _reconcile_in_flight_notices(self, result: IntakeScanResult, active_cards: Dict[str, dict]) -> None:
        by_demand = {(r.get("demand_ref") or {}).get("demand_id"): r for r in result.records.values()}
        for task_id, card in sorted(active_cards.items()):
            if card.get("status") not in {"InProgress", "Review", "Verify"}:
                continue
            dem_id = card.get("demand_id")
            cat_id = card.get("feature") or card.get("issue") or card.get("requirement")
            rec = result.records.get(str(cat_id)) or (by_demand.get(dem_id) if dem_id else None)
            if rec is None and (dem_id or cat_id):
                result.notices.append(IntakeLifecycleNotice(
                    code="IN_FLIGHT_PRESERVED_ON_INTAKE_REMOVAL",
                    item_id=str(cat_id or dem_id),
                    task_ids=[task_id],
                    action="preserve_in_flight_notify_coord",
                    message=f"Intake file missing for active task {task_id}; in-flight work NOT auto-cancelled",
                ))
            elif rec is not None and rec.get("enabled") is False:
                result.notices.append(IntakeLifecycleNotice(
                    code="IN_FLIGHT_PRESERVED_ON_INTAKE_DISABLED",
                    item_id=rec["id"],
                    task_ids=[task_id],
                    action="preserve_in_flight_notify_coord",
                    message=f"Intake {rec['id']} set enabled=false while {task_id} active; preserving in-flight task",
                ))

    def link_tasks_to_category_yaml(self, update: TaskLinkUpdate) -> str:
        """以 CAS 方式更新分类 YAML 的关联字段、自动递增 revision 并同步写入 `.intake_digests.json` 账本。

        参数：
        - update (TaskLinkUpdate)：包含目标分类 YAML 路径、关联任务、确认/批准及 ARCH 拆解引用的更新请求。

        返回值：
        - str：更新后（或未发生实质变更时）分类 YAML 文件的完整 SHA-256 十六进制摘要。
        """
        snap = read_with_digest(update.category_yaml_path)
        data = yaml.safe_load(snap.text)
        if not isinstance(data, dict):
            raise IntakeValidationError("Target category YAML is invalid", "CORRUPT_CATEGORY_YAML")
        _apply_task_link_updates(data, update)
        if yaml.safe_dump(data, allow_unicode=True, sort_keys=False) == snap.text:
            return snap.sha256
        data["revision"] = int(data.get("revision", 1)) + 1
        new_text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
        planned_sha = compute_bytes_sha256(new_text)
        intent = WriteIntent(
            operation_id=f"link_{data.get('id', 'cat')}_{planned_sha[:8]}",
            target_path=snap.path,
            expected_sha256=snap.sha256,
            planned_sha256=planned_sha,
            summary=f"Link tasks {update.task_ids} to {data.get('id')}",
        )
        written_sha = write_cas(snap.path, new_text, snap.sha256, intent)
        ledger = self._load_ledger()
        ledger["categories"][f"{data['id']}@r{data['revision']}"] = written_sha
        self._save_ledger(ledger)
        return written_sha


def _apply_task_link_updates(data: dict, update: TaskLinkUpdate) -> None:
    """将确认单、批准引用、请求动作、看板任务 ID 及 ARCH 拆解引用合并写入分类 YAML 字典。

    参数：
    - data (dict)：待原地更新的分类 YAML 字典对象。
    - update (TaskLinkUpdate)：封装关联字段更新内容的请求对象。

    返回值：
    - None：原地修改 `data`，若 `requested_action` 非法则抛出 `IntakeValidationError`。
    """
    if update.demand_ref_updates:
        data.setdefault("demand_ref", {}).update(update.demand_ref_updates)
    if update.approval_refs is not None:
        data["approval_refs"] = list(update.approval_refs)
    if update.requested_action is not None:
        if update.requested_action not in VALID_ACTIONS:
            raise IntakeValidationError(f"Invalid action: {update.requested_action}", "INVALID_REQUESTED_ACTION")
        data["requested_action"] = update.requested_action
    rel_ids = data.get("related_ids")
    if not isinstance(rel_ids, dict):
        rel_ids = {"legacy_refs": list(rel_ids or [])}
    existing_tasks = list(rel_ids.get("engineering_tasks") or [])
    for tid in update.task_ids:
        if tid not in existing_tasks:
            existing_tasks.append(tid)
    rel_ids["engineering_tasks"] = existing_tasks
    if update.arch_breakdown is not None:
        rel_ids["arch_breakdown"] = dict(update.arch_breakdown)
    data["related_ids"] = rel_ids
