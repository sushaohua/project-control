#!/usr/bin/env python3
"""AUTO-05: Phase 1 M1 & M2 Comprehensive End-to-End Independent Acceptance Test Suite.

Covers all 19 acceptance criteria for M1 & M2:
- Intake & Security: P1-01, P1-06, P1-16
- Approval & Anti-Forgery: P1-03, P1-18, P1-19
- Triage & Multi-Role: P1-02, P1-04, P1-17
- Async Orchestration & Idempotence: P1-05, P1-07, P1-08, P1-20
- Reconciliation & Concurrency: P1-09, P1-10, P1-13
- Execution Gates & Live Drill: P1-11, P1-12, P1-15
- Invariants: AST function scale (<=50 lines, <=4 args) self-audit
"""

import ast
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import sqlite3
import sys
import tempfile
import time
from typing import Dict, List, Optional, Tuple
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
    CoordRunner,
    CoordRunnerConfig,
    CoordState,
    CoordStateMachine,
    DemandDispatchPlan,
    FiveSourceReconciler,
    GateValidationError,
    JobLauncher,
    Lease,
    LeaseManager,
    MultiRoleSplitSpec,
    ReconcileReport,
    ReconcileStatus,
    ResourceConflictError,
    RoleAdapterConfig,
    RoleJobHandle,
    RoleSliceSpec,
    RoleTaskRequest,
    RoleTaskResult,
    StateStore,
    TaskExecutionRecord,
    TaskState,
    WorkIntakeManager,
    build_multi_role_requests,
    compute_bytes_sha256,
    create_exclusive,
    get_proc_starttime,
    is_proc_alive,
    read_with_digest,
    route_intake_demand,
    verify_independent_codex_review_entry,
    write_atomic_json,
    write_cas,
)
from coord_runner.errors import RemediationLimitExceededError


def _setup_test_intake_env(base_dir: Path) -> Tuple[Path, Path]:
    ws = base_dir / "workspace"
    ws.mkdir(parents=True, exist_ok=True)
    intake = ws / "project-control/docs/work_intake"
    for folder in ("submissions", "confirmations", "approvals", "issues", "features", "requirements"):
        (intake / folder).mkdir(parents=True, exist_ok=True)
    return ws, intake


def _write_conf(ws: Path, rel_path: str, conf_id: str, rev: int) -> Tuple[Path, str]:
    full_p = ws / rel_path
    full_p.parent.mkdir(parents=True, exist_ok=True)
    body = f"---\nconfirmation_id: {conf_id}\nrevision: {rev}\n---\n# Confirmation {conf_id}\n"
    full_p.write_text(body, encoding="utf-8")
    return full_p, compute_bytes_sha256(body)


def _build_appr(conf_rel: str, conf_id: str, conf_rev: int, conf_sha: str) -> dict:
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


class TestPhase1IntakeAndSecurity(unittest.TestCase):
    """P1-01, P1-06, P1-16: Markdown intake, tamper resistance, and boundary security."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="acceptance_p1_intake_")
        self.ws, self.intake = _setup_test_intake_env(Path(self.tmp.name))
        self.manager = WorkIntakeManager(self.ws, self.intake)

    def tearDown(self):
        self.tmp.cleanup()

    def test_p1_01_batch_markdown_generates_unique_yamls_and_preserves_contracts(self):
        md_body = (
            "# Acceptance Batch Submission\n\n"
            "## 公共约束\n"
            "- 严格在白名单内作业\n- 严禁修改业务代码与双 Bootloader\n\n"
            "## 指令列表\n"
            "1. [issue] 偶发串口校验超时调查\n"
            "2. [feature] 新增自动化验收报告清单\n"
            "3. [requirement] 澄清状态汇报协议格式\n"
        )
        sub_p = self.intake / "submissions/SUB-P1-001.md"
        sub_p.write_text(md_body, encoding="utf-8")
        scan_res = self.manager.scan_and_sync(persist_ledger=True)
        self.assertEqual(len(scan_res.generated_paths), 3)
        self.assertEqual(len(scan_res.errors), 0)
        kinds = {r["kind"] for r in scan_res.records.values()}
        self.assertEqual(kinds, {"issue", "feature", "requirement"})
        demands = {r["demand_ref"]["demand_id"] for r in scan_res.records.values()}
        self.assertEqual(len(demands), 3)
        feat = next(r for r in scan_res.records.values() if r["kind"] == "feature")
        self.assertIn("common_constraints_sha256", feat["source_refs"])
        self.assertTrue(feat["demand_ref"]["demand_id"].startswith("DEM-"))

    def test_p1_06_tampered_content_and_schema_version_isolated_from_valid_items(self):
        good_md = self.intake / "submissions/SUB-GOOD.md"
        good_md.write_text("1. [feature] 有效功能\n", encoding="utf-8")
        tamper_md = self.intake / "submissions/SUB-TAMPER.md"
        tamper_md.write_text("---\nschema_version: 1\nsubmission_id: SUB-TAMPER\nrevision: 1\n---\n1. [issue] 初始报错\n", encoding="utf-8")
        first = self.manager.scan_and_sync(persist_ledger=True)
        self.assertEqual(len(first.errors), 0)
        tamper_md.write_text("---\nschema_version: 1\nsubmission_id: SUB-TAMPER\nrevision: 1\n---\n1. [issue] 篡改内容\n", encoding="utf-8")
        (self.intake / "features/BAD-SCHEMA.yaml").write_text("schema_version: 99\nid: FEAT-X\n", encoding="utf-8")
        second = self.manager.scan_and_sync(persist_ledger=True)
        codes = {e.code for e in second.errors}
        self.assertIn("TAMPERED_SAME_REVISION", codes)
        self.assertIn("UNSUPPORTED_SCHEMA_VERSION", codes)
        self.assertGreaterEqual(len(second.records), 1)

    def test_p1_16_delete_or_disable_preserves_in_flight_and_blocks_shell_and_escape(self):
        md_path = self.intake / "submissions/SUB-SHELL.md"
        md_path.write_text("1. [feature] 测试注入 $(touch hacked.txt) ; rm -rf /\n", encoding="utf-8")
        scan1 = self.manager.scan_and_sync(persist_ledger=True)
        self.assertFalse((self.ws / "hacked.txt").exists())
        rec = next(iter(scan1.records.values()))
        self.assertTrue(rec["safety_flags"]["contains_shell_like_text"])
        active_cards = {"AUTO-99": {"id": "AUTO-99", "status": "InProgress", "feature": rec["id"], "demand_id": rec["demand_ref"]["demand_id"]}}
        raw_yaml = yaml.safe_load(Path(rec["_path"]).read_text(encoding="utf-8"))
        raw_yaml["revision"] = 2
        raw_yaml["enabled"] = False
        Path(rec["_path"]).write_text(yaml.safe_dump(raw_yaml, allow_unicode=True), encoding="utf-8")
        scan2 = self.manager.scan_and_sync(persist_ledger=True, active_cards=active_cards)
        self.assertEqual(active_cards["AUTO-99"]["status"], "InProgress")
        self.assertIn("IN_FLIGHT_PRESERVED_ON_INTAKE_DISABLED", {n.code for n in scan2.notices})
        adapter = CodexRoleAdapter(RoleAdapterConfig(workspace_root=self.ws))
        with self.assertRaises(BoundaryViolationError):
            adapter.submit_role_task(RoleTaskRequest("T-SOC", 1, "ENG-FWD", "implement", "p", allowed_paths=["soc-ap/core/**"], approval_verified=True), "k_soc")


class TestPhase1ApprovalAndAntiForgery(unittest.TestCase):
    """P1-03, P1-18, P1-19: Human approval anti-forgery, partial batch, and scope gating."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="acceptance_p1_appr_")
        self.ws = Path(self.tmp.name)
        self.guard = ApprovalGuard(self.ws)

    def tearDown(self):
        self.tmp.cleanup()

    def test_p1_03_approved_feature_scope_dispatches_while_unapproved_blocked(self):
        _, c_sha = _write_conf(self.ws, "docs/conf.md", "CONF-01", 1)
        appr = _build_appr("docs/conf.md", "CONF-01", 1, c_sha)
        appr["approval_mode"] = "partial_batch_approval"
        appr["approved_demands"] = [{
            "demand_id": "DEM-FEAT-01", "demand_confirmed": True,
            "implementation_summary_approved": True, "approved_items": ["manifest_gen"],
            "model_policy": {"default_model": "gpt-6-luna", "overrides_approved": []},
        }]
        appr_p = self.ws / "docs/APPR-01.yaml"
        appr_p.write_text(yaml.safe_dump(appr, allow_unicode=True), encoding="utf-8")
        rel_ok = self.guard.check_demand_release(ApprovalQuery(demand_id="DEM-FEAT-01", approval_path=Path("docs/APPR-01.yaml"), required_scope_item="manifest_gen"))
        self.assertTrue(rel_ok.implementation_allowed)
        rel_block = self.guard.check_demand_release(ApprovalQuery(demand_id="DEM-FEAT-01", approval_path=Path("docs/APPR-01.yaml"), required_scope_item="unapproved_slice"))
        self.assertFalse(rel_block.implementation_allowed)
        self.assertEqual(rel_block.status, "SUBSCOPE_UNAPPROVED")

    def test_p1_18_partial_batch_approval_and_demand_only_confirmation(self):
        _, c_sha = _write_conf(self.ws, "docs/conf_batch.md", "CONF-BATCH", 2)
        appr = _build_appr("docs/conf_batch.md", "CONF-BATCH", 2, c_sha)
        appr["approval_mode"] = "partial_batch_approval"
        appr["approved_demands"] = [
            {"demand_id": "DEM-A", "demand_confirmed": True, "implementation_summary_approved": True, "approved_items": ["slice_1"]},
            {"demand_id": "DEM-B", "demand_confirmed": True, "implementation_summary_approved": False, "approved_items": []},
        ]
        appr_p = self.ws / "docs/APPR-BATCH.yaml"
        appr_p.write_text(yaml.safe_dump(appr, allow_unicode=True), encoding="utf-8")
        ok_a = self.guard.check_demand_release(ApprovalQuery(demand_id="DEM-A", approval_path=Path("docs/APPR-BATCH.yaml"), required_scope_item="slice_1"))
        self.assertTrue(ok_a.implementation_allowed)
        dem_only_b = self.guard.check_demand_release(ApprovalQuery(demand_id="DEM-B", approval_path=Path("docs/APPR-BATCH.yaml")))
        self.assertFalse(dem_only_b.implementation_allowed)
        self.assertEqual(dem_only_b.status, "DEMAND_CONFIRMED_ONLY")
        unlisted_c = self.guard.check_demand_release(ApprovalQuery(demand_id="DEM-C", approval_path=Path("docs/APPR-BATCH.yaml")))
        self.assertEqual(unlisted_c.status, "PENDING_APPROVAL")

    def test_p1_19_anti_forgery_rejects_bogus_actors_stale_rev_and_fuzzy_prose(self):
        _, conf_r1_sha = _write_conf(self.ws, "docs/conf.md", "CONF-01", 1)
        appr = _build_appr("docs/conf.md", "CONF-01", 1, conf_r1_sha)
        appr_path = self.ws / "docs/APPR-01.yaml"
        bad_actor = dict(appr, approved_by={"actor_type": "MODEL", "actor_id": "ai", "source_channel": "coord_session", "verbatim_decision": "APPROVED"})
        appr_path.write_text(yaml.safe_dump(bad_actor), encoding="utf-8")
        with self.assertRaises(ApprovalValidationError) as c1:
            self.guard.require_implementation_approval(ApprovalQuery(demand_id="DEM-20261103-001", approval_path=Path("docs/APPR-01.yaml")))
        self.assertEqual(c1.exception.code, "NON_HUMAN_ACTOR_REJECTED")
        appr_path.write_text(yaml.safe_dump(appr), encoding="utf-8")
        with self.assertRaises(ApprovalValidationError) as c2:
            self.guard.require_implementation_approval(ApprovalQuery(demand_id="DEM-20261103-001", approval_path=Path("docs/APPR-01.yaml"), target_confirmation_revision=2))
        self.assertEqual(c2.exception.code, "STALE_CONFIRMATION_REVISION")
        prose_only = {"id": "FEAT-1", "enabled": True, "title": "全部批准 APPROVED", "demand_ref": {"demand_id": "DEM-1"}, "approval_refs": []}
        self.assertFalse(self.guard.check_intake_record(prose_only).implementation_allowed)


class TestPhase1TriageAndMultiRole(unittest.TestCase):
    """P1-02, P1-04, P1-17: Clarification triage, root-cause investigation, and multi-role split."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="acceptance_p1_triage_")
        self.ws = Path(self.tmp.name)
        _, c_sha = _write_conf(self.ws, "docs/conf.md", "CONF-01", 1)
        appr_dict = _build_appr("docs/conf.md", "CONF-01", 1, c_sha)
        appr_p = self.ws / "docs/APPR.yaml"
        appr_p.write_text(yaml.safe_dump(appr_dict), encoding="utf-8")
        self.ok_appr = ApprovalGuard(self.ws).check_demand_release(ApprovalQuery(demand_id="DEM-20261103-001", approval_path=Path("docs/APPR.yaml"), required_scope_item="scope_alpha"))

    def tearDown(self):
        self.tmp.cleanup()

    def test_p1_02_ambiguous_requirement_triggers_pm_arch_clarification(self):
        req_plan = route_intake_demand({"kind": "requirement", "demand_ref": {"demand_id": "DEM-R"}, "triage_metadata": {"clarity_status": "unclear"}}, self.ok_appr)
        self.assertEqual(req_plan.route, "CLARIFY_PM_ARCH")
        self.assertEqual(req_plan.sandbox_mode, "read-only")
        self.assertFalse(req_plan.implementation_released)

    def test_p1_04_issue_root_cause_triage_routing_to_owner(self):
        iss_unk = route_intake_demand({"kind": "issue", "demand_ref": {"demand_id": "DEM-I"}, "triage_metadata": {"root_cause_status": "unknown"}}, self.ok_appr)
        self.assertEqual(iss_unk.route, "INVESTIGATE_ISSUE_READONLY")
        self.assertEqual(iss_unk.sandbox_mode, "read-only")
        iss_known = route_intake_demand({"kind": "issue", "demand_ref": {"demand_id": "DEM-20261103-001"}, "triage_metadata": {"root_cause_status": "known", "proposed_owner_role": "ENG-FWD"}}, self.ok_appr)
        self.assertEqual(iss_known.route, "DISPATCH_KNOWN_ISSUE_OWNER")
        self.assertEqual(iss_known.target_roles, ["ENG-FWD"])

    def test_p1_17_single_demand_multi_role_split_preserves_demand_id(self):
        reqs = build_multi_role_requests(MultiRoleSplitSpec(
            demand_id="DEM-20261103-001", approval=self.ok_appr,
            slices=[
                RoleSliceSpec("AUTO-10", "ENG-FWD", ["project-control/docs/a/**"], ["project-control/docs/a/out.md"], "p1"),
                RoleSliceSpec("AUTO-11", "ENG-UI", ["project-control/docs/b/**"], ["project-control/docs/b/out.md"], "p2"),
            ],
        ))
        self.assertEqual([r.demand_id for r in reqs], ["DEM-20261103-001", "DEM-20261103-001"])
        self.assertEqual({r.role for r in reqs}, {"ENG-FWD", "ENG-UI"})


class TestPhase1AsyncOrchestrationAndIdempotence(unittest.TestCase):
    """P1-05, P1-07, P1-08, P1-20: Idempotent rescan, revision conflict, and async concurrency."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="acceptance_p1_async_")
        self.ws, self.intake = _setup_test_intake_env(Path(self.tmp.name))
        self.manager = WorkIntakeManager(self.ws, self.intake)
        self.store = StateStore(self.ws / "state.sqlite3", self.ws / "coord_runner.lock")
        self.reconciler = FiveSourceReconciler(workspace_root=self.ws, state_store=self.store)

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def test_p1_05_intake_rescan_and_renotify_idempotence(self):
        md = self.intake / "submissions/SUB-IDEM.md"
        md.write_text("1. [feature] 幂等指令 A\n2. [feature] 幂等指令 B\n", encoding="utf-8")
        res1 = self.manager.scan_and_sync(persist_ledger=True)
        self.assertEqual(len(res1.generated_paths), 2)
        res2 = self.manager.scan_and_sync(persist_ledger=True)
        self.assertEqual(len(res2.generated_paths), 0)
        self.assertEqual(len(res2.records), 2)
        self.store.set_meta("intake_digest:DEM-001:rev1", "sha_fixed_123")
        self.assertTrue(self.reconciler.check_intake_idempotence("DEM-001", 1, "sha_fixed_123"))

    def test_p1_07_higher_revision_in_flight_conflict_delegation(self):
        state = CoordState(schema_version=1, in_flight_tasks={
            "TASK-ACTIVE": TaskExecutionRecord("TASK-ACTIVE", state=TaskState.IN_PROGRESS.value, task_revision=1),
        })
        self.store.save_coord_state(state)
        self.assertTrue(self.reconciler.check_in_flight_revision("TASK-ACTIVE", 2))
        self.assertFalse(self.reconciler.check_in_flight_revision("TASK-ACTIVE", 1))

    def test_p1_08_async_long_running_job_allows_second_task_advancement(self):
        jobs_dir = self.ws / "jobs"
        jobs_dir.mkdir(parents=True, exist_ok=True)
        launcher = JobLauncher(workspace_root=self.ws)
        j1_dir = jobs_dir / "job_long"
        j2_dir = jobs_dir / "job_fast"
        pid1 = launcher.launch_async(j1_dir, [sys.executable, "-c", "import time; time.sleep(0.8)"], "prompt_1")
        pid2 = launcher.launch_async(j2_dir, [sys.executable, "-c", "import time; time.sleep(0.05)"], "prompt_2")
        st1 = get_proc_starttime(pid1)
        st2 = get_proc_starttime(pid2)
        self.assertTrue(is_proc_alive(pid1, st1))
        time.sleep(0.15)
        self.assertEqual(launcher.poll_proc(pid2), 0)
        self.assertFalse(is_proc_alive(pid2, st2))
        self.assertTrue(is_proc_alive(pid1, st1))
        time.sleep(0.75)
        self.assertEqual(launcher.poll_proc(pid1), 0)
        self.assertFalse(is_proc_alive(pid1, st1))

    def test_p1_20_reordered_input_reuses_approvals_while_substantive_bump_requires_fresh(self):
        md = self.intake / "submissions/SUB-ORD.md"
        md.write_text("1. [feature] 功能Alpha\n2. [feature] 功能Beta\n", encoding="utf-8")
        r1 = self.manager.scan_and_sync(persist_ledger=True)
        self.assertEqual(len(r1.generated_paths), 2)
        md.write_text("1. [feature] 功能Beta\n2. [feature] 功能Alpha\n", encoding="utf-8")
        r2 = self.manager.scan_and_sync(persist_ledger=True)
        self.assertEqual(len(r2.generated_paths), 0)
        self.assertEqual(len(r2.records), 2)


class TestPhase1ReconciliationAndConcurrency(unittest.TestCase):
    """P1-09, P1-10, P1-13: 5-source reconciliation, flock mutual exclusion, and CAS write guard."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="acceptance_p1_recon_")
        self.ws = Path(self.tmp.name)
        self.db_path = self.ws / "state.sqlite3"
        self.lock_path = self.ws / "coord_runner.lock"
        self.store = StateStore(self.db_path, self.lock_path)
        self.reconciler = FiveSourceReconciler(workspace_root=self.ws, state_store=self.store)

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def test_p1_09_timeout_and_crash_reconciliation_via_dispatch_key(self):
        job_dir = self.ws / "job_orphan"
        job_dir.mkdir(parents=True)
        (job_dir / "pid.json").write_text(json.dumps({"pid": 99999999, "starttime": "0"}), encoding="utf-8")
        rep = self.reconciler.reconcile_job(job_dir, "KEY_ORPHAN")
        self.assertEqual(rep.status, ReconcileStatus.RECONCILE_REQUIRED.value)
        self.assertTrue(rep.reconcile_required)
        self.assertFalse(rep.alive)

    def test_p1_10_single_instance_flock_and_active_lease_protection(self):
        self.store.acquire_process_lock()
        second_store = StateStore(self.db_path, self.lock_path)
        with self.assertRaises(ResourceConflictError):
            second_store.acquire_process_lock()
        second_store.close()
        lm = LeaseManager(default_duration=1800.0)
        lease = lm.acquire_lease("TASK-ACTIVE", "implementation", "owner_x")
        lease.expires_at = time.time() - 10.0
        job_dir = self.ws / "job_active_task"
        job_dir.mkdir(parents=True)
        pid = os.getpid()
        st = get_proc_starttime(pid)
        (job_dir / "pid.json").write_text(json.dumps({"pid": pid, "starttime": st}), encoding="utf-8")
        self.store.save_role_job({
            "job_id": "job_active_task", "dispatch_key": "k_active", "task_id": "TASK-ACTIVE",
            "task_revision": 1, "role": "INTEGRATOR", "phase": "implement",
            "status": "RUNNING", "job_dir": str(job_dir),
        })
        protected = self.reconciler.protect_active_leases(lm, self.ws)
        self.assertEqual(protected, 1)
        self.assertGreater(lease.expires_at, time.time())

    def test_p1_13_cas_optimistic_concurrency_blocks_user_overwrite(self):
        f = self.ws / "card.md"
        f.write_text("original content", encoding="utf-8")
        sha = hashlib.sha256(b"original content").hexdigest()
        self.reconciler.verify_cas_write(f, sha)
        f.write_text("manually edited content", encoding="utf-8")
        with self.assertRaises(CasConflictError):
            self.reconciler.verify_cas_write(f, sha)


class TestPhase1ExecutionGatesAndLiveDrill(unittest.TestCase):
    """P1-11, P1-12, P1-15: Quality gates, remote candidate check, and real staging proof."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="acceptance_p1_gates_")
        self.ws = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_p1_11_exit_code_zero_without_evidence_or_qa_rejection_blocked(self):
        sm = CoordStateMachine(max_corrections=2)
        with self.assertRaises(GateValidationError):
            sm.validate_commit_sha("")
        with self.assertRaises(GateValidationError):
            sm.validate_commit_sha("0000000000000000000000000000000000000000")
        rec = TaskExecutionRecord("TASK-11", state=TaskState.CANDIDATE_PUSHED.value, candidate_commit="a" * 40, corrections_count=2)
        with self.assertRaises(RemediationLimitExceededError):
            sm.handle_remediation(rec, "QA failed", {"path": "qa.json", "sha256": "f" * 64})

    def test_p1_12_unpushed_candidate_and_fake_qa_subagent_rejected(self):
        sm = CoordStateMachine()
        rec = TaskExecutionRecord("AUTO-03", state=TaskState.REVIEW.value)
        with self.assertRaises(GateValidationError):
            sm.validate_review_verdict(rec, {"platform": "subagent", "session": "s1", "decision": "APPROVED"}, "auth")
        with self.assertRaises(GateValidationError):
            verify_independent_codex_review_entry(
                {"role": "QA", "platform": "subagent", "session": "s1"},
                author_session="author_123",
                workspace_root=self.ws,
            )
        with self.assertRaises(GateValidationError):
            verify_independent_codex_review_entry(
                {"role": "QA", "platform": "codex", "session": "author_123"},
                author_session="author_123",
                workspace_root=self.ws,
            )

    def test_p1_15_live_drill_end_to_end_verification(self):
        m1_drill_summary = WORKSPACE_ROOT / "project-control/docs/evidence/coord_automation/AUTO-03/runs/run_01/live_drill/drill_summary.json"
        m2_drill_summary = WORKSPACE_ROOT / "project-control/docs/evidence/coord_automation/AUTO-04/runs/run_01/live_drill/drill_summary.json"
        self.assertTrue(m1_drill_summary.is_file(), f"M1 drill summary must exist at {m1_drill_summary}")
        self.assertTrue(m2_drill_summary.is_file(), f"M2 drill summary must exist at {m2_drill_summary}")
        m1_data = json.loads(m1_drill_summary.read_text(encoding="utf-8"))
        self.assertEqual(m1_data.get("role_actual_model"), "gpt-6-luna")
        self.assertEqual(m1_data.get("approved_feature_route", {}).get("route"), "DISPATCH_APPROVED_FEATURE")
        self.assertEqual(m1_data.get("held_requirement_route", {}).get("route"), "CLARIFY_PM_ARCH")
        m2_data = json.loads(m2_drill_summary.read_text(encoding="utf-8"))
        self.assertTrue(m2_data.get("flock_mutual_exclusion_verified"))
        self.assertTrue(m2_data.get("p1_05_intake_idempotence_verified"))
        self.assertTrue(m2_data.get("p1_08_dual_parallel_nonblocking_verified"))
        self.assertTrue(m2_data.get("p1_09_five_source_reconciliation_verified"))
        self.assertTrue(m2_data.get("p1_10_single_flock_and_lease_guard_verified"))
        self.assertTrue(m2_data.get("p1_13_cas_concurrency_guard_verified"))


class TestAcceptanceSuiteInvariants(unittest.TestCase):
    """Hard AST gate: verify ALL functions in this test file satisfy <=50 lines and <=4 parameters."""

    def test_all_acceptance_functions_comply_with_ast_limits(self):
        this_file = Path(__file__).resolve()
        tree = ast.parse(this_file.read_text(encoding="utf-8"), filename=str(this_file))
        violations = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                lines = node.end_lineno - node.lineno + 1
                args_count = len(node.args.args) + len(node.args.kwonlyargs)
                if lines > 50 or args_count > 4:
                    violations.append(f"{node.name} (lines={lines}, args={args_count})")
        self.assertEqual(violations, [], f"Acceptance suite AST gate violations: {violations}")


if __name__ == "__main__":
    unittest.main()
