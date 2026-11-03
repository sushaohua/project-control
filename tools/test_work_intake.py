#!/usr/bin/env python3
"""Unit and integration tests for M1 work_intake, CAS, approval_guard, and role_adapter."""

import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from typing import Tuple
import unittest
import yaml

TOOLS_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = TOOLS_DIR.parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from coord_runner import (
    ApprovalGuard,
    ApprovalQuery,
    ApprovalValidationError,
    BoundaryViolationError,
    CasConflictError,
    CodexRoleAdapter,
    CoordinateRequest,
    GateValidationError,
    MultiRoleSplitSpec,
    RoleAdapterConfig,
    RoleSliceSpec,
    RoleTaskRequest,
    TaskLinkUpdate,
    WorkIntakeManager,
    WriteIntent,
    build_multi_role_requests,
    compute_bytes_sha256,
    create_exclusive,
    read_with_digest,
    route_intake_demand,
    verify_independent_codex_review_entry,
    write_cas,
)


FAKE_CODEX_SCRIPT = """#!/usr/bin/env python3
import json, os, pathlib, sqlite3, sys

args = sys.argv[1:]
prompt = sys.stdin.read()
codex_home = pathlib.Path(os.environ["FAKE_CODEX_HOME"])
log_calls = codex_home / "invocations.jsonl"
with log_calls.open("a", encoding="utf-8") as fh:
    fh.write(json.dumps({"args": args, "first_line": prompt.splitlines()[0] if prompt else ""}) + "\\n")

mode = os.environ.get("FAKE_CODEX_MODE", "normal")
tid = os.environ.get("FAKE_CODEX_TID", "01a19fcc-1111-2222-3333-444455556666")
rollout_model = os.environ.get("FAKE_CODEX_ROLLOUT_MODEL", "gpt-6-luna")

db = codex_home / "state_5.sqlite"
conn = sqlite3.connect(str(db))
conn.execute("CREATE TABLE IF NOT EXISTS threads (id TEXT PRIMARY KEY, first_user_message TEXT, created_at INTEGER)")
conn.execute("INSERT OR REPLACE INTO threads VALUES (?, ?, 1)", (tid, prompt))
conn.commit()
conn.close()

sdir = codex_home / "sessions/2026/11/03"
sdir.mkdir(parents=True, exist_ok=True)
(sdir / f"rollout-2026-11-03T13-00-00-{tid}.jsonl").write_text(
    json.dumps({"type": "turn_context", "payload": {"model": rollout_model}}) + "\\n",
    encoding="utf-8",
)

out_idx = args.index("-o") + 1 if "-o" in args else -1
out_path = pathlib.Path(args[out_idx]) if out_idx > 0 else None
cwd_idx = args.index("-C") + 1 if "-C" in args else -1
workdir = pathlib.Path(args[cwd_idx]) if cwd_idx > 0 else pathlib.Path.cwd()

if mode == "write_deliverable":
    target = workdir / os.environ["FAKE_WRITE_REL"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("deliverable_ok\\n", encoding="utf-8")
elif mode == "write_unauthorized":
    (workdir / "unauthorized_escape.txt").write_text("bad\\n", encoding="utf-8")

if out_path is not None:
    payload = json.loads(os.environ["FAKE_FINAL_JSON"])
    out_path.write_text(json.dumps(payload), encoding="utf-8")

print(json.dumps({"type": "thread.started", "thread_id": tid}))
print(json.dumps({"type": "turn.completed", "usage": {"input_tokens": 120, "output_tokens": 30}}))
sys.exit(int(os.environ.get("FAKE_EXIT_CODE", "0")))
"""


def _write_valid_confirmation(ws: Path, rel_path: str, conf_id: str, rev: int) -> Tuple[Path, str]:
    full_p = ws / rel_path
    full_p.parent.mkdir(parents=True, exist_ok=True)
    body = f"---\nconfirmation_id: {conf_id}\nrevision: {rev}\n---\n# Confirmation {conf_id} r{rev}\n"
    full_p.write_text(body, encoding="utf-8")
    return full_p, compute_bytes_sha256(body)


def _build_approval_dict(conf_rel: str, conf_id: str, conf_rev: int, conf_sha: str) -> dict:
    return {
        "schema_version": 1,
        "approval_id": "APPR-TEST-001",
        "revision": 1,
        "approved_at": "2026-11-03T13:20:00+08:00",
        "approved_by": {
            "actor_type": "HUMAN",
            "actor_id": "sushaohua",
            "source_channel": "coord_interactive_session",
            "verbatim_decision": "批准执行已列范围。",
        },
        "bound_confirmation": {
            "confirmation_id": conf_id,
            "revision": conf_rev,
            "path": conf_rel,
            "sha256": conf_sha,
        },
        "approval_mode": "full_batch_approval",
        "approved_demands": [{
            "demand_id": "DEM-20261103-001",
            "demand_confirmed": True,
            "implementation_summary_approved": True,
            "approved_items": ["scope_alpha"],
            "model_policy": {"default_model": "gpt-6-luna", "overrides_approved": []},
        }],
    }


class CasWriterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="cas_test_")
        self.base = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_read_with_digest_and_write_cas_positive(self) -> None:
        target = self.base / "card.yaml"
        initial_sha = create_exclusive(target, "status: Ready\n")
        raw, read_sha = read_with_digest(target)
        self.assertEqual(raw, b"status: Ready\n")
        self.assertEqual(read_sha, initial_sha)
        new_body = "status: InProgress\n"
        planned = compute_bytes_sha256(new_body)
        intent = WriteIntent(
            operation_id="op_01", target_path=target, expected_sha256=read_sha,
            planned_sha256=planned, summary="advance state", intent_dir=self.base / "intents",
        )
        updated_sha = write_cas(target, new_body, read_sha, intent)
        self.assertEqual(updated_sha, planned)
        self.assertEqual(target.read_text(encoding="utf-8"), new_body)
        self.assertTrue((self.base / "intents/op_01.intent.json").is_file())

    def test_write_cas_rejects_concurrent_edit_and_preserves_user_file(self) -> None:
        target = self.base / "queue.yaml"
        orig_sha = create_exclusive(target, "order: [AUTO-03]\n")
        target.write_text("order: [AUTO-03, MANUAL-EDIT]\n", encoding="utf-8")
        planned = compute_bytes_sha256("order: [OVERWRITE]\n")
        intent = WriteIntent(
            operation_id="op_conflict", target_path=target, expected_sha256=orig_sha,
            planned_sha256=planned, summary="runner write", intent_dir=self.base / "intents",
        )
        with self.assertRaises(CasConflictError) as ctx:
            write_cas(target, "order: [OVERWRITE]\n", orig_sha, intent)
        self.assertEqual(ctx.exception.details["expected_sha256"], orig_sha)
        self.assertEqual(target.read_text(encoding="utf-8"), "order: [AUTO-03, MANUAL-EDIT]\n")
        self.assertTrue((self.base / "intents/op_conflict.intent.json").is_file())

    def test_cas_rejects_invalid_digest_missing_file_and_duplicate_exclusive(self) -> None:
        target = self.base / "new.yaml"
        create_exclusive(target, "v: 1\n")
        with self.assertRaises(CasConflictError):
            create_exclusive(target, "v: 2\n")
        self.assertEqual(target.read_text(encoding="utf-8"), "v: 1\n")
        with self.assertRaises(CasConflictError):
            write_cas(target, "v: 2\n", "not-a-sha256")
        with self.assertRaises(CasConflictError):
            write_cas(self.base / "missing.yaml", "v: 2\n", "a" * 64)


class WorkIntakeBatchAndIsolationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="intake_test_")
        self.ws = Path(self.tmp.name)
        self.intake = self.ws / "project-control/docs/work_intake"
        for sub in ("submissions", "issues", "features", "requirements", "confirmations", "approvals"):
            (self.intake / sub).mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_p1_01_batch_md_generates_unique_three_category_yamls_and_links(self) -> None:
        md_text = (
            "# 人工批量输入\n\n## 公共约束\n- 保护既有工作区改动\n- 严禁改 MCU 与 Bootloader\n\n"
            "## 指令列表\n"
            "1. [issue] 状态对账日志缺少字段报错，需定位原因\n"
            "2. [feature] 新增收件汇总导出表格支持\n"
            "3. [requirement] 多角色审批通知粒度目标不清，待澄清\n"
        )
        (self.intake / "submissions/SUB-BATCH-01.md").write_text(md_text, encoding="utf-8")
        mgr = WorkIntakeManager(self.ws, self.intake)
        res1 = mgr.scan_and_sync(persist_ledger=True)
        self.assertEqual(res1.errors, [])
        self.assertEqual(len(res1.generated_paths), 3)
        kinds = {r["kind"] for r in res1.records.values()}
        self.assertEqual(kinds, {"issue", "feature", "requirement"})
        demands = {r["demand_ref"]["demand_id"] for r in res1.records.values()}
        self.assertEqual(len(demands), 3)
        res2 = mgr.scan_and_sync(persist_ledger=True)
        self.assertEqual(res2.generated_paths, [])
        feat = next(r for r in res1.records.values() if r["kind"] == "feature")
        mgr.link_tasks_to_category_yaml(TaskLinkUpdate(
            category_yaml_path=Path(feat["_path"]), task_ids=["AUTO-03", "AUTO-04"],
        ))
        reloaded = yaml.safe_load(Path(feat["_path"]).read_text(encoding="utf-8"))
        self.assertEqual(reloaded["related_ids"]["engineering_tasks"], ["AUTO-03", "AUTO-04"])

    def test_canonical_workspace_intake_and_disabled_examples(self) -> None:
        mgr = WorkIntakeManager(WORKSPACE_ROOT)
        res = mgr.scan_and_sync(persist_ledger=False)
        self.assertEqual(res.errors, [])
        self.assertIn("FEAT-INTAKE-20261103-001", res.records)
        ex_root = WORKSPACE_ROOT / "project-control/docs/work_intake/examples"
        self.assertTrue((ex_root / "README_template.md").is_file())
        for rel in ("issues/ISS-EXAMPLE-001.yaml", "features/FEAT-EXAMPLE-001.yaml", "requirements/REQ-EXAMPLE-001.yaml"):
            data = yaml.safe_load((ex_root / rel).read_text(encoding="utf-8"))
            self.assertIs(data["enabled"], False)
            self.assertEqual(data["approval_refs"], [])

    def test_p1_06_tampered_same_revision_and_corrupt_records_isolated(self) -> None:
        good_md = self.intake / "submissions/SUB-GOOD.md"
        good_md.write_text("1. [feature] 正常有效功能指令\n", encoding="utf-8")
        tamper_md = self.intake / "submissions/SUB-TAMPER.md"
        tamper_md.write_text("---\nschema_version: 1\nsubmission_id: SUB-TAMPER\nrevision: 1\n---\n1. [issue] 初始报错\n", encoding="utf-8")
        mgr = WorkIntakeManager(self.ws, self.intake)
        first = mgr.scan_and_sync(persist_ledger=True)
        self.assertEqual(first.errors, [])
        tamper_md.write_text("---\nschema_version: 1\nsubmission_id: SUB-TAMPER\nrevision: 1\n---\n1. [issue] 篡改同版本内容\n", encoding="utf-8")
        (self.intake / "issues/BAD-KIND.yaml").write_text(
            "schema_version: 1\nid: ISS-BAD-1\nrevision: 1\nkind: feature\nenabled: true\ntitle: t\nobjective: o\npriority_hint: P1\nrequested_action: triage\n",
            encoding="utf-8",
        )
        (self.intake / "features/BAD-SCHEMA.yaml").write_text("schema_version: 99\nid: FEAT-X\n", encoding="utf-8")
        (self.intake / "requirements/CORRUPT.yaml").write_text(":::broken_yaml: [", encoding="utf-8")
        (self.intake / "features/SELF-APPROVED.yaml").write_text(
            "schema_version: 1\nid: FEAT-SELF\nrevision: 1\nkind: feature\nenabled: true\napproved: true\ntitle: t\nobjective: o\npriority_hint: P1\nrequested_action: triage\n",
            encoding="utf-8",
        )
        second = mgr.scan_and_sync(persist_ledger=True)
        codes = {e.code for e in second.errors}
        self.assertIn("TAMPERED_SAME_REVISION", codes)
        self.assertIn("DIRECTORY_KIND_CONFLICT", codes)
        self.assertIn("UNSUPPORTED_SCHEMA_VERSION", codes)
        self.assertIn("CORRUPT_CATEGORY_YAML", codes)
        self.assertIn("MODEL_SELF_APPROVED_REJECTED", codes)
        self.assertGreaterEqual(len(second.records), 2)

    def test_p1_16_disabled_or_deleted_preserves_in_flight_and_blocks_shell_or_forbidden_scope(self) -> None:
        sentinel = self.ws / "shell_should_never_exist.txt"
        md_path = self.intake / "submissions/SUB-SHELL.md"
        md_path.write_text(f"1. [feature] 请检查 `touch {sentinel}` 与 $(rm -rf /tmp/nonexistent)\n", encoding="utf-8")
        mgr = WorkIntakeManager(self.ws, self.intake)
        scan1 = mgr.scan_and_sync(persist_ledger=True)
        self.assertFalse(sentinel.exists())
        rec = next(iter(scan1.records.values()))
        self.assertTrue(rec["safety_flags"]["contains_shell_like_text"])
        self.assertTrue(rec["safety_flags"]["shell_execution_disabled"])
        active_cards = {"AUTO-99": {"id": "AUTO-99", "status": "InProgress", "feature": rec["id"], "demand_id": rec["demand_ref"]["demand_id"]}}
        raw_yaml = yaml.safe_load(Path(rec["_path"]).read_text(encoding="utf-8"))
        raw_yaml["revision"] = 2
        raw_yaml["enabled"] = False
        Path(rec["_path"]).write_text(yaml.safe_dump(raw_yaml, allow_unicode=True, sort_keys=False), encoding="utf-8")
        scan2 = mgr.scan_and_sync(persist_ledger=True, active_cards=active_cards)
        self.assertEqual(active_cards["AUTO-99"]["status"], "InProgress")
        self.assertIn("IN_FLIGHT_PRESERVED_ON_INTAKE_DISABLED", {n.code for n in scan2.notices})
        Path(rec["_path"]).unlink()
        scan3 = mgr.scan_and_sync(persist_ledger=True, active_cards=active_cards)
        self.assertIn("IN_FLIGHT_PRESERVED_ON_INTAKE_REMOVAL", {n.code for n in scan3.notices})
        raw_yaml["revision"] = 3
        raw_yaml["target_paths"] = ["soc-ap/core/main.cpp"]
        (self.intake / "features/FORBIDDEN.yaml").write_text(yaml.safe_dump(raw_yaml, allow_unicode=True), encoding="utf-8")
        scan4 = mgr.scan_and_sync(persist_ledger=False)
        self.assertIn("SCOPE_BOUNDARY_REJECTED", {e.code for e in scan4.errors})


class ApprovalGuardAntiForgeryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="appr_test_")
        self.ws = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_canonical_workspace_approval_verified(self) -> None:
        guard = ApprovalGuard(WORKSPACE_ROOT)
        appr_rel = Path("project-control/docs/work_intake/approvals/APPR-20261103-001.yaml")
        res = guard.require_implementation_approval(ApprovalQuery(
            demand_id="DEM-INTAKE-P1-001",
            approval_path=appr_rel,
            target_confirmation_id="CONFIRM-INTAKE-P1-20261103",
            target_confirmation_revision=2,
            required_scope_item="item_1_phase1_objectives_m1_m2_m3_scope_p1_01_to_20_and_auto_03_to_06",
        ))
        self.assertTrue(res.implementation_allowed)
        self.assertEqual(res.status, "APPROVED_FOR_IMPLEMENTATION")

    def test_p1_19_rejects_forged_actor_stale_rev_tampered_hash_and_prose_keywords(self) -> None:
        _, conf_r1_sha = _write_valid_confirmation(self.ws, "docs/conf.md", "CONF-01", 1)
        appr = _build_approval_dict("docs/conf.md", "CONF-01", 1, conf_r1_sha)
        appr_path = self.ws / "docs/APPR-01.yaml"
        guard = ApprovalGuard(self.ws)
        bad_actor = dict(appr, approved_by={"actor_type": "MODEL", "actor_id": "ai", "source_channel": "coord_interactive_session", "verbatim_decision": "APPROVED"})
        appr_path.write_text(yaml.safe_dump(bad_actor), encoding="utf-8")
        with self.assertRaises(ApprovalValidationError) as c1:
            guard.require_implementation_approval(ApprovalQuery(demand_id="DEM-20261103-001", approval_path=Path("docs/APPR-01.yaml")))
        self.assertEqual(c1.exception.code, "NON_HUMAN_ACTOR_REJECTED")
        appr_path.write_text(yaml.safe_dump(appr), encoding="utf-8")
        with self.assertRaises(ApprovalValidationError) as c2:
            guard.require_implementation_approval(ApprovalQuery(
                demand_id="DEM-20261103-001", approval_path=Path("docs/APPR-01.yaml"), target_confirmation_revision=2,
            ))
        self.assertEqual(c2.exception.code, "STALE_CONFIRMATION_REVISION")
        (self.ws / "docs/conf.md").write_text("---\nconfirmation_id: CONF-01\nrevision: 1\n---\n# Tampered!\n", encoding="utf-8")
        with self.assertRaises(ApprovalValidationError) as c3:
            guard.require_implementation_approval(ApprovalQuery(demand_id="DEM-20261103-001", approval_path=Path("docs/APPR-01.yaml")))
        self.assertEqual(c3.exception.code, "CONFIRMATION_HASH_MISMATCH")
        prose_only = {"id": "FEAT-1", "enabled": True, "title": "全部批准 APPROVED", "demand_ref": {"demand_id": "DEM-1"}, "approval_refs": []}
        self.assertFalse(guard.check_intake_record(prose_only).implementation_allowed)
        with self.assertRaises(ApprovalValidationError):
            guard.check_intake_record(dict(prose_only, approved=True))

    def test_p1_03_and_p1_18_partial_batch_subscope_and_demand_only_split(self) -> None:
        _, conf_sha = _write_valid_confirmation(self.ws, "docs/conf_batch.md", "CONF-BATCH", 2)
        appr = _build_approval_dict("docs/conf_batch.md", "CONF-BATCH", 2, conf_sha)
        appr["approval_mode"] = "partial_batch_approval"
        appr["approved_demands"] = [
            {"demand_id": "DEM-A", "demand_confirmed": True, "implementation_summary_approved": True, "approved_items": ["slice_1"]},
            {"demand_id": "DEM-B", "demand_confirmed": True, "implementation_summary_approved": False, "approved_items": []},
        ]
        appr_p = self.ws / "docs/APPR-BATCH.yaml"
        appr_Text = yaml.safe_dump(appr, allow_unicode=True)
        appr_p.write_text(appr_Text, encoding="utf-8")
        appr_sha = compute_bytes_sha256(appr_Text)
        guard = ApprovalGuard(self.ws)
        ok_a = guard.check_demand_release(ApprovalQuery(demand_id="DEM-A", approval_path=Path("docs/APPR-BATCH.yaml"), required_scope_item="slice_1"))
        blocked_sub = guard.check_demand_release(ApprovalQuery(demand_id="DEM-A", approval_path=Path("docs/APPR-BATCH.yaml"), required_scope_item="slice_unapproved"))
        dem_only_b = guard.check_demand_release(ApprovalQuery(demand_id="DEM-B", approval_path=Path("docs/APPR-BATCH.yaml")))
        unlisted_c = guard.check_demand_release(ApprovalQuery(demand_id="DEM-C", approval_path=Path("docs/APPR-BATCH.yaml")))
        self.assertTrue(ok_a.implementation_allowed)
        self.assertEqual(blocked_sub.status, "SUBSCOPE_UNAPPROVED")
        self.assertFalse(blocked_sub.implementation_allowed)
        self.assertEqual(dem_only_b.status, "DEMAND_CONFIRMED_ONLY")
        self.assertTrue(dem_only_b.demand_confirmed)
        self.assertFalse(dem_only_b.implementation_allowed)
        self.assertEqual(unlisted_c.status, "PENDING_APPROVAL")
        batch_eval = guard.evaluate_batch_records([
            {"id": "F-A", "demand_ref": {"demand_id": "DEM-A"}, "approval_refs": [{"path": "docs/APPR-BATCH.yaml", "sha256": appr_sha}]},
            {"id": "F-B", "demand_ref": {"demand_id": "DEM-B"}, "approval_refs": [{"path": "docs/APPR-BATCH.yaml", "sha256": appr_sha}]},
        ])
        self.assertTrue(batch_eval["F-A"].implementation_allowed)
        self.assertFalse(batch_eval["F-B"].implementation_allowed)


class RoleAdapterAndGatesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="role_adapter_test_")
        self.ws = Path(self.tmp.name) / "ws"
        (self.ws / "project-control/docs").mkdir(parents=True, exist_ok=True)
        self.codex_home = Path(self.tmp.name) / "codex_home"
        self.codex_home.mkdir(parents=True, exist_ok=True)
        self.fake_bin = Path(self.tmp.name) / "fake_codex"
        self.fake_bin.write_text(FAKE_CODEX_SCRIPT, encoding="utf-8")
        self.fake_bin.chmod(0o755)
        self._old_env = {k: os.environ.get(k) for k in ("FAKE_CODEX_HOME", "FAKE_CODEX_MODE", "FAKE_FINAL_JSON", "FAKE_WRITE_REL", "FAKE_CODEX_ROLLOUT_MODEL", "FAKE_CODEX_TID", "FAKE_EXIT_CODE")}
        os.environ["FAKE_CODEX_HOME"] = str(self.codex_home)
        os.environ["FAKE_CODEX_ROLLOUT_MODEL"] = "gpt-6-luna"
        os.environ["FAKE_CODEX_TID"] = "01a19fcc-aaaa-bbbb-cccc-ddddeeeeffff"
        os.environ["FAKE_EXIT_CODE"] = "0"

    def tearDown(self) -> None:
        for k, val in self._old_env.items():
            if val is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = val
        self.tmp.cleanup()

    def _make_adapter(self, require_push: bool = False) -> CodexRoleAdapter:
        return CodexRoleAdapter(RoleAdapterConfig(
            workspace_root=self.ws, jobs_dir=self.ws / "jobs", codex_bin=self.fake_bin,
            codex_home=self.codex_home, require_remote_push=require_push,
        ))

    def test_coordinate_readonly_resume_and_zero_call_noop(self) -> None:
        adapter = self._make_adapter()
        os.environ["FAKE_FINAL_JSON"] = json.dumps({
            "decision_id": "D1", "action": "DISPATCH_OWNER", "target_role": "INTEGRATOR",
            "target_task_id": "AUTO-03", "rationale": "ready", "next_check_condition": "done",
        })
        d1 = adapter.coordinate(CoordinateRequest(digest_inputs={"v": 1}))
        self.assertTrue(d1.model_invoked)
        self.assertEqual(d1.actual_model, "gpt-6-luna")
        d_noop = adapter.coordinate(CoordinateRequest(digest_inputs={"v": 1}, previous_digest=d1.digest, active_coord_thread_id=d1.thread_id))
        self.assertFalse(d_noop.model_invoked)
        self.assertEqual(d_noop.action, "NOOP")
        d2 = adapter.coordinate(CoordinateRequest(digest_inputs={"v": 2}, previous_digest=d1.digest, active_coord_thread_id=d1.thread_id))
        self.assertTrue(d2.model_invoked)
        calls = [json.loads(ln) for ln in (self.codex_home / "invocations.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(calls), 2)
        resume_args = calls[1]["args"]
        self.assertLess(resume_args.index("--sandbox"), resume_args.index("resume"))
        self.assertEqual(resume_args[resume_args.index("--sandbox") + 1], "read-only")

    def test_p1_02_p1_04_p1_17_routing_and_multi_role_split(self) -> None:
        _, c_sha = _write_valid_confirmation(self.ws, "c.md", "C1", 1)
        appr = _build_approval_dict("c.md", "C1", 1, c_sha)
        (self.ws / "appr.yaml").write_text(yaml.safe_dump(appr), encoding="utf-8")
        ok_appr = ApprovalGuard(self.ws).check_demand_release(ApprovalQuery(demand_id="DEM-20261103-001", approval_path=Path("appr.yaml")))
        req_plan = route_intake_demand({"kind": "requirement", "demand_ref": {"demand_id": "DEM-R"}, "triage_metadata": {"clarity_status": "unclear"}}, ok_appr)
        self.assertEqual((req_plan.route, req_plan.sandbox_mode, req_plan.implementation_released), ("CLARIFY_PM_ARCH", "read-only", False))
        iss_unk = route_intake_demand({"kind": "issue", "demand_ref": {"demand_id": "DEM-I"}, "triage_metadata": {"root_cause_status": "unknown"}}, ok_appr)
        self.assertEqual((iss_unk.route, iss_unk.sandbox_mode), ("INVESTIGATE_ISSUE_READONLY", "read-only"))
        iss_known = route_intake_demand({"kind": "issue", "demand_ref": {"demand_id": "DEM-20261103-001"}, "triage_metadata": {"root_cause_status": "known", "proposed_owner_role": "ENG-FWD"}}, ok_appr)
        self.assertEqual((iss_known.route, iss_known.target_roles), ("DISPATCH_KNOWN_ISSUE_OWNER", ["ENG-FWD"]))
        reqs = build_multi_role_requests(MultiRoleSplitSpec(
            demand_id="DEM-20261103-001", approval=ok_appr,
            slices=[
                RoleSliceSpec("AUTO-10", "ENG-FWD", ["project-control/docs/a/**"], ["project-control/docs/a/out.md"], "p1"),
                RoleSliceSpec("AUTO-11", "ENG-UI", ["project-control/docs/b/**"], ["project-control/docs/b/out.md"], "p2"),
            ],
        ))
        self.assertEqual([r.demand_id for r in reqs], ["DEM-20261103-001", "DEM-20261103-001"])
        with self.assertRaises(BoundaryViolationError):
            self._make_adapter().submit_role_task(RoleTaskRequest("T-PM", 1, "PM", "implement", "bad"), "k_pm")

    def test_p1_16_boundary_revert_and_forbidden_repo_block(self) -> None:
        adapter = self._make_adapter()
        with self.assertRaises(BoundaryViolationError):
            adapter.submit_role_task(RoleTaskRequest(
                "T-SOC", 1, "ENG-FWD", "implement", "p", allowed_paths=["soc-ap/core/**"], approval_verified=True,
            ), "k_soc")
        os.environ["FAKE_CODEX_MODE"] = "write_unauthorized"
        os.environ["FAKE_FINAL_JSON"] = json.dumps({
            "status": "COMPLETED", "summary": "wrote", "candidate_commit": "a1b2c3d4" * 5,
            "artifacts": [], "notes": "",
        })
        handle = adapter.submit_role_task(RoleTaskRequest(
            "T-ESC", 1, "INTEGRATOR", "implement", "p", workdir=self.ws, watch_dir=self.ws,
            allowed_paths=["project-control/docs/**"], approval_verified=True, require_commit=False,
        ), "k_esc")
        self.assertFalse((self.ws / "unauthorized_escape.txt").exists())
        with self.assertRaises(BoundaryViolationError):
            adapter.collect_role_result(handle.job_id)

    def _init_git_with_remote(self) -> Tuple[Path, Path, str]:
        bare = Path(self.tmp.name) / "origin.git"
        subprocess.run(["git", "init", "--bare", str(bare)], check=True, capture_output=True)
        repo = self.ws / "project-control"
        subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@example.com"], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
        subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", str(bare)], check=True)
        (repo / "docs/out.md").write_text("init\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", "docs/out.md"], check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"], check=True, capture_output=True)
        sha = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
        return repo, bare, sha

    def test_p1_11_p1_12_p1_15_candidate_remote_reconcile_and_codex_reviewer_gates(self) -> None:
        repo, _, unpushed_sha = self._init_git_with_remote()
        adapter = self._make_adapter(require_push=True)
        os.environ["FAKE_CODEX_MODE"] = "write_deliverable"
        os.environ["FAKE_WRITE_REL"] = "docs/deliv.md"
        os.environ["FAKE_FINAL_JSON"] = json.dumps({"status": "COMPLETED", "summary": "no sha", "candidate_commit": "", "artifacts": ["project-control/docs/deliv.md"], "notes": ""})
        h_no_sha = adapter.submit_role_task(RoleTaskRequest(
            "T-11", 1, "INTEGRATOR", "implement", "p", workdir=repo, watch_dir=repo,
            allowed_paths=["project-control/docs/**"], deliverables=["project-control/docs/deliv.md"], approval_verified=True,
        ), "k_11")
        with self.assertRaises(GateValidationError):
            adapter.collect_role_result(h_no_sha.job_id)
        os.environ["FAKE_FINAL_JSON"] = json.dumps({"status": "COMPLETED", "summary": "unpushed", "candidate_commit": unpushed_sha, "artifacts": ["project-control/docs/deliv.md"], "notes": ""})
        h_unpushed = adapter.submit_role_task(RoleTaskRequest(
            "T-12", 1, "INTEGRATOR", "implement", "p", workdir=repo, watch_dir=repo,
            allowed_paths=["project-control/docs/**"], deliverables=["project-control/docs/deliv.md"], approval_verified=True,
        ), "k_12")
        with self.assertRaises(GateValidationError):
            adapter.collect_role_result(h_unpushed.job_id)
        subprocess.run(["git", "-C", str(repo), "push", "origin", "HEAD:refs/heads/main"], check=True, capture_output=True)
        ok_res = adapter.collect_role_result(h_unpushed.job_id)
        self.assertEqual(ok_res.candidate_commit, unpushed_sha)
        (h_unpushed.job_dir / "exit_status.json").unlink()
        unknown_st = adapter.query_role_job("k_12")
        self.assertEqual((unknown_st.state, unknown_st.reconcile_required), ("LAUNCH_UNKNOWN", True))
        with self.assertRaises(GateValidationError):
            verify_independent_codex_review_entry({"platform": "subagent", "session": "s1"}, "auth", self.ws)
        ev_file = self.ws / "qa_events.jsonl"
        ev_bytes = b'{"type":"thread.started","thread_id":"01a19fcc-9999"}\n'
        ev_file.write_bytes(ev_bytes)
        verify_independent_codex_review_entry({
            "platform": "codex", "session": "01a19fcc-9999", "model": "gpt-6-luna",
            "session_evidence": {"path": "qa_events.jsonl", "sha256": hashlib.sha256(ev_bytes).hexdigest()},
        }, "different_author", self.ws)

    def test_committed_m1_live_drill_evidence_verified(self) -> None:
        drill_dir = WORKSPACE_ROOT / "project-control/docs/evidence/coord_automation/AUTO-03/runs/run_01/live_drill"
        summary = json.loads((drill_dir / "drill_summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["coord_live_model"], "gpt-6-luna")
        self.assertEqual(summary["role_actual_model"], "gpt-6-luna")
        self.assertEqual(summary["coord_second_call_action"], "NOOP")
        self.assertIs(summary["coord_second_call_model_invoked"], False)
        self.assertIs(summary["auto_done_written"], False)
        self.assertEqual(summary["held_requirement_route"]["route"], "CLARIFY_PM_ARCH")
        self.assertIs(summary["held_requirement_route"]["implementation_released"], False)
        deliv_path = WORKSPACE_ROOT / summary["deliverable_path"]
        self.assertEqual(compute_bytes_sha256(deliv_path.read_bytes()), summary["deliverable_sha256"])
        manifest = json.loads(deliv_path.read_text(encoding="utf-8"))
        self.assertIs(manifest["verified"], True)
        events_path = WORKSPACE_ROOT / summary["role_events_path"]
        first_evt = json.loads(events_path.read_text(encoding="utf-8").splitlines()[0])
        self.assertEqual(first_evt.get("thread_id"), summary["role_thread_id"])


if __name__ == "__main__":
    unittest.main()
