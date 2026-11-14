#!/usr/bin/env python3
"""AUTO-03 M1 受控手动单步真实演练执行器（验证 P1-01/02/03/15/18 宿主机真实闭环）。"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Tuple
import yaml

from .approval_guard import ApprovalGuard
from .cas_writer import create_exclusive, read_with_digest
from .errors import GateValidationError
from .role_adapter import (
    CodexRoleAdapter,
    CoordinateRequest,
    RoleAdapterConfig,
    RoleTaskRequest,
    route_intake_demand,
)
from .work_intake import TaskLinkUpdate, WorkIntakeManager

PARENT_APPROVAL_REL = "project-control/docs/work_intake/approvals/APPR-20261103-001.yaml"


def _ensure_drill_submission(intake_root: Path) -> Path:
    """确保演练专用的 Markdown 收件单文件在演练隔离目录内已创建。"""
    sub_dir = intake_root / "submissions"
    sub_dir.mkdir(parents=True, exist_ok=True)
    for folder in ("issues", "features", "requirements", "confirmations", "approvals"):
        (intake_root / folder).mkdir(parents=True, exist_ok=True)
    sub_path = sub_dir / "SUB-DRILL-20261103-001.md"
    if sub_path.is_file():
        return sub_path
    content = (
        "# AUTO-03 M1 受控真实单步演练批次输入\n\n"
        "## 公共约束\n"
        "- 仅在 `project-control/docs/evidence/coord_automation/AUTO-03/runs/run_01/live_drill/` 白名单内写入受控演练产物\n"
        "- 严禁触碰 `soc-ap/`、`mcu-p3/`、`test_harness/` 及双 Bootloader，严禁安装后台服务\n\n"
        "## 指令列表\n"
        "1. [feature] 在受控演练目录生成 `deliverables/drill_intake_manifest.json`，记录稳定需求 ID 与公共约束 SHA256\n"
        "2. [requirement] 第二阶段告警汇总文案格式目标不清，待 PM 与 ARCH 澄清后再定是否实施\n"
    )
    create_exclusive(sub_path, content)
    return sub_path


def _ensure_drill_confirmation(intake_root: Path, dem_id: str, parent_info: Tuple[str, str]) -> Tuple[Path, str]:
    """确保绑定父级人工总批复的演练需求确认单已生成并返回 (路径, SHA256)。"""
    parent_id, parent_sha = parent_info
    conf_path = intake_root / "confirmations" / "CONFIRM-DRILL-20261103-001.md"
    if not conf_path.is_file():
        conf_body = (
            "---\n"
            "confirmation_id: CONFIRM-DRILL-20261103-001\n"
            "revision: 1\n"
            f"demand_id: {dem_id}\n"
            f"parent_approval_id: {parent_id}\n"
            f"parent_approval_sha256: {parent_sha}\n"
            "---\n\n"
            "# AUTO-03 M1 受控单步演练确认单\n\n"
            f"- 锚定人工总批复 `{parent_id}` (`item_2a_bounded_non_production_software_drill_in_project_control_for_p1_15`)\n"
            f"- 批准需求 `{dem_id}` 在 `live_drill/deliverables/` 内执行单步实测；指令 2 保持待澄清挂起。\n"
        )
        create_exclusive(conf_path, conf_body)
    return conf_path, hashlib.sha256(conf_path.read_bytes()).hexdigest()


def _ensure_drill_confirmation_and_approval(
    workspace_root: Path,
    intake_root: Path,
    feat_record: dict,
) -> Tuple[Path, str, Path, str]:
    """校验父级人工批复文件并生成演练确认单与演练批复 YAML。"""
    parent_appr = workspace_root / PARENT_APPROVAL_REL
    parent_snap = read_with_digest(parent_appr)
    parent_data = ApprovalGuard(workspace_root).load_and_verify_approval(parent_appr, parent_snap.sha256, 1)
    dem_id = feat_record["demand_ref"]["demand_id"]
    conf_path, conf_sha = _ensure_drill_confirmation(
        intake_root, dem_id, (parent_data["approval_id"], parent_snap.sha256),
    )
    rel_conf = str(conf_path.resolve().relative_to(workspace_root))
    appr_path = intake_root / "approvals" / "APPR-DRILL-20261103-001.yaml"
    if not appr_path.is_file():
        appr_obj = {
            "schema_version": 1,
            "approval_id": "APPR-DRILL-20261103-001",
            "revision": 1,
            "approved_at": parent_data["approved_at"],
            "approved_by": dict(parent_data["approved_by"]),
            "parent_human_approval_ref": {"path": PARENT_APPROVAL_REL, "sha256": parent_snap.sha256},
            "bound_confirmation": {"confirmation_id": "CONFIRM-DRILL-20261103-001", "revision": 1,
                                   "path": rel_conf, "sha256": conf_sha},
            "approval_mode": "partial_batch_approval",
            "approved_demands": [{
                "demand_id": dem_id,
                "demand_confirmed": True,
                "implementation_summary_approved": True,
                "approved_items": ["drill_manifest_generation"],
                "model_policy": {"default_model": "gpt-6-luna", "overrides_approved": []},
            }],
        }
        create_exclusive(appr_path, yaml.safe_dump(appr_obj, allow_unicode=True, sort_keys=False))
    return conf_path, conf_sha, appr_path, hashlib.sha256(appr_path.read_bytes()).hexdigest()


def _run_drill_coord_calls(adapter: CodexRoleAdapter, digest_inputs: dict, drill_root: Path) -> Tuple[object, object]:
    """执行两次连续的 COORD 裁决调用，验证首次真实唤醒模型且无变更二次调用短路返回 NOOP。"""
    coord_prompt = (
        "You are COORD in read-only mode evaluating a bounded M1 single-step drill. "
        "Do NOT modify any files. Return structured JSON with decision_id='DEC-AUTO03-DRILL-01', "
        "action='DISPATCH_OWNER', target_role='INTEGRATOR', target_task_id='AUTO-03-DRILL-01', "
        "rationale='Demand 1 approved via exact SHA256; Demand 2 held for PM/ARCH clarification', "
        "next_check_condition='Collect INTEGRATOR deliverable and await formal QA'."
    )
    first = adapter.coordinate(CoordinateRequest(
        digest_inputs=digest_inputs, previous_digest=None, prompt=coord_prompt, workdir=drill_root,
    ))
    second = adapter.coordinate(CoordinateRequest(
        digest_inputs=digest_inputs, previous_digest=first.digest,
        active_coord_thread_id=first.thread_id, prompt=coord_prompt, workdir=drill_root,
    ))
    if not first.model_invoked or second.model_invoked or second.action != "NOOP":
        raise GateValidationError("Coordinate live/NOOP invariant failed in drill")
    return first, second


def _run_drill_role_task(
    adapter: CodexRoleAdapter,
    drill_root: Path,
    workspace_root: Path,
    feat_record: dict,
) -> Tuple[object, object, Path]:
    """派发 INTEGRATOR 角色单步演练任务并收集其生成的交付清单产物。"""
    deliv_dir = drill_root / "deliverables"
    deliv_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = deliv_dir / "drill_intake_manifest.json"
    rel_deliv_glob = str(deliv_dir.resolve().relative_to(workspace_root)) + "/**"
    rel_manifest = str(manifest_path.resolve().relative_to(workspace_root))
    dem_id = feat_record["demand_ref"]["demand_id"]
    cc_sha = feat_record["source_refs"]["common_constraints_sha256"]
    role_prompt = (
        f"Role: INTEGRATOR. Bounded M1 drill task AUTO-03-DRILL-01.\n"
        f"Write valid UTF-8 JSON to exact relative path `deliverables/drill_intake_manifest.json` "
        f"with keys: `task_id` ('AUTO-03-DRILL-01'), `demand_id` ('{dem_id}'), "
        f"`category_id` ('{feat_record['id']}'), `common_constraints_sha256` ('{cc_sha}'), "
        f"and `verified` (true). Touch NO other files. "
        f"Then return JSON matching schema with status='COMPLETED', candidate_commit='', "
        f"artifacts=['{rel_manifest}'], summary='Generated bounded drill manifest', notes='M1 live drill'."
    )
    dispatch_key = "AUTO-03-DRILL-01:rev1:INTEGRATOR:implement:1"
    req = RoleTaskRequest(
        task_id="AUTO-03-DRILL-01", task_revision=1, role="INTEGRATOR", phase="implement",
        prompt=role_prompt, demand_id=dem_id, workdir=drill_root, watch_dir=drill_root,
        allowed_paths=[rel_deliv_glob], deliverables=[rel_manifest],
        approval_verified=True, require_commit=False,
    )
    handle = adapter.submit_role_task(req, dispatch_key)
    q_status = adapter.query_role_job(dispatch_key)
    collected = adapter.collect_role_result(handle.job_id)
    return q_status, collected, manifest_path


def _prepare_drill_intake(ws: Path, intake_root: Path) -> Tuple[object, dict, dict, str]:
    """初始化演练收件单、执行首次扫描、绑定审批引用并完成二次同步。"""
    _ensure_drill_submission(intake_root)
    intake_mgr = WorkIntakeManager(ws, intake_root)
    scan_res = intake_mgr.scan_and_sync(persist_ledger=True)
    feat_rec = next(r for r in scan_res.records.values() if r["kind"] == "feature")
    req_rec = next(r for r in scan_res.records.values() if r["kind"] == "requirement")
    conf_p, conf_sha, appr_p, appr_sha = _ensure_drill_confirmation_and_approval(ws, intake_root, feat_rec)
    rel_conf = str(conf_p.resolve().relative_to(ws))
    rel_appr = str(appr_p.resolve().relative_to(ws))
    intake_mgr.link_tasks_to_category_yaml(TaskLinkUpdate(
        category_yaml_path=Path(feat_rec["_path"]),
        task_ids=["AUTO-03-DRILL-01"],
        demand_ref_updates={"confirmation_id": "CONFIRM-DRILL-20261103-001", "confirmation_revision": 1,
                            "confirmation_path": rel_conf, "confirmation_sha256": conf_sha},
        approval_refs=[{"approval_id": "APPR-DRILL-20261103-001", "revision": 1, "path": rel_appr, "sha256": appr_sha}],
        requested_action="execute",
    ))
    rescan = intake_mgr.scan_and_sync(persist_ledger=True)
    return rescan, rescan.records[feat_rec["id"]], rescan.records[req_rec["id"]], appr_sha


def execute_m1_live_drill(workspace_root: Path, drill_dir: Path, codex_bin: Path) -> Dict[str, object]:
    """在指定演练目录内使用宿主机真实 Codex CLI 执行端到端 M1 手动单步演练并保存摘要。"""
    ws = workspace_root.resolve()
    root = drill_dir.resolve() if drill_dir.is_absolute() else (Path.cwd() / drill_dir).resolve()
    if not str(root).startswith(str((ws / "project-control").resolve()) + "/"):
        raise GateValidationError(f"Live drill directory must reside under project-control/: {root}")
    rescan, feat_rec, req_rec, appr_sha = _prepare_drill_intake(ws, root / "work_intake")
    eval_map = ApprovalGuard(ws).evaluate_batch_records(list(rescan.records.values()))
    feat_plan = route_intake_demand(feat_rec, eval_map[feat_rec["id"]])
    req_plan = route_intake_demand(req_rec, eval_map[req_rec["id"]])
    adapter = CodexRoleAdapter(RoleAdapterConfig(
        workspace_root=ws, jobs_dir=root / "jobs", codex_bin=codex_bin, require_remote_push=False,
    ))
    coord_live, coord_noop = _run_drill_coord_calls(adapter, {"feat": feat_rec["_sha256"], "appr": appr_sha}, root)
    q_status, role_res, manifest_p = _run_drill_role_task(adapter, root, ws, feat_rec)
    summary = {
        "drill_task_id": "AUTO-03-DRILL-01",
        "intake_generated_count": len(rescan.records),
        "intake_errors": [e.__dict__ for e in rescan.errors],
        "approved_feature_route": feat_plan.__dict__,
        "held_requirement_route": req_plan.__dict__,
        "coord_live_thread_id": coord_live.thread_id,
        "coord_live_model": coord_live.actual_model,
        "coord_live_tokens": coord_live.tokens_used,
        "coord_second_call_action": coord_noop.action,
        "coord_second_call_model_invoked": coord_noop.model_invoked,
        "role_job_id": role_res.job_id,
        "role_dispatch_key": role_res.dispatch_key,
        "role_query_state": q_status.state,
        "role_thread_id": role_res.thread_id,
        "role_actual_model": role_res.actual_model,
        "role_tokens_used": role_res.tokens_used,
        "role_events_path": str(Path(role_res.events_path).resolve().relative_to(ws)),
        "deliverable_path": str(manifest_p.resolve().relative_to(ws)),
        "deliverable_sha256": hashlib.sha256(manifest_p.read_bytes()).hexdigest(),
        "post_role_lifecycle_state": "AWAITING_SERVER_CANDIDATE_AND_INDEPENDENT_QA",
        "auto_done_written": False,
    }
    (root / "drill_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary
