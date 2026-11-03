---
task_id: AUTO-05
task_revision: 1
reviewer_role: ARCH
actual_session: "01a1a0ee-0679-76d1-9c20-066e075402e4"
reviewed_artifact_version: ac820925bf14f5d2b4864dd1f01b9784939a453e
decision: REJECTED
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-05/runs/run_03/server_qa.json
  sha256: fa1c9100a39b7e5a4403de127a9205c2802c39c0fb03d91cf467774a66fa2b5a
reviewed_artifacts:
  - path: "project-control/tools/test_phase1_intake_acceptance.py"
    sha256: "6837765d38d7d78c5a38a40cb8bb080c9084a6fc4767ac1d2d093c67be535d39"
  - path: "project-control/docs/evidence/coord_automation/AUTO-05/runs/run_01/result.md"
    sha256: "2e4854605b52f9941537912099caaf8efa61d50418e5d0ffa566b22f4893bc45"
content_audit:
  fact_sources:
    result: passed
    basis: "Recomputed the acceptance suite, run_01 result, confirmation rev2, design rev2, and server_qa.json hashes. The checkout HEAD, server_lock.json, and checkout.log bind the fresh read-only sandbox to candidate ac820925bf14f5d2b4864dd1f01b9784939a453e."
  protocol_compatibility:
    result: not-applicable
    basis: "This review covers an acceptance suite and its evidence record, not a protocol implementation."
  claim_scope:
    result: passed
    basis: "The sandbox evidence records the acceptance suite, AST check, and supporting regression commands passing. The reviewed tests now assert the run_02 gaps P1-07, P1-08, and P1-15."
  architecture_completeness:
    result: failed
    basis: "The task card still identifies candidate_commit bc7c766cf390ee844c92f66fc22f92faf28e1b8d and executor run_id run_02, while this review and server evidence bind run_03 to ac820925bf14f5d2b4864dd1f01b9784939a453e. The task record does not yet align with the reviewed candidate and run."
---

# ARCH Review — AUTO-05 run_03

## Decision

**REJECTED.** The run_02 coverage gaps are closed in the reviewed suite, and run_03 server evidence binds the tested checkout to the requested candidate. The task card remains bound to the prior candidate and run, so the delivery record is not complete for this review.

## Evidence and boundary checks

- Verified candidate `ac820925bf14f5d2b4864dd1f01b9784939a453e` against checkout HEAD, `server_lock.json`, and `checkout.log`. The container evidence identifies a fresh checkout, read-only bind mount, image `qa-sandbox:20261029`, and image digest `sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f`.
- Recomputed hashes match the requested values for the acceptance suite, run_01 result, confirmation rev2, design rev2, and run_03 `server_qa.json`.
- The server record reports the acceptance suite and supporting checks passing. The suite asserts every function is at most 50 lines and four parameters; the server AST audit reports no violations.
- The server lock records the pinned `soc-ap`, `mcu-p3`, and `test_harness` commits. The candidate changes are in `project-control`; no changes to those business repositories or the bootloader repositories were identified.
- The task card still lists `candidate_commit: bc7c766cf390ee844c92f66fc22f92faf28e1b8d` and `executor.run_id: run_02`. Those fields conflict with the server-pinned candidate and this `run_03` review.

## Rework 03 finding audit (P1-07, P1-08, P1-15, and all 8 prior findings)

- **P1-07 — covered.** `test_p1_07` calls `record_revision_conflict_referral("TASK-ACTIVE", 2)`, asserts the referral action and active/incoming revisions, checks SQLite metadata key `referral:TASK-ACTIVE:rev2`, and confirms the active task remains bound to revision 1.
- **P1-08 — covered.** `test_p1_08` enables `async_role_dispatch` and runs `CoordRunner.step()`. Its asynchronous jobs use `TASK-LONG` (0.6s) and `TASK-FAST` (0.05s); the third task is held while two are active, dispatched after FAST completes while LONG remains active, then completed alongside LONG on the following step.
- **P1-15 — covered.** The test unconditionally requires both M1/M2 summaries, the M1 manifest, and M2 report to exist, checks all four specified SHA256 digests, and verifies the report contains candidate `4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06`.

Audit of the eight run_01 findings against the current suite and run_01 evidence:

1. **P1-09 — covered:** process-kill crash simulation, dispatch-key reconciliation, unresolved-state assertion, and completion after exit status is written.
2. **P1-08 — covered:** async scheduler-step advancement and concurrency limit, as detailed above.
3. **P1-07 — covered:** coordinator referral and persisted old/new revision bindings, as detailed above.
4. **P1-11 — covered:** missing deliverable and rejected QA decision block acceptance; required non-author review is also checked.
5. **P1-12 — covered:** unpushed candidate, report hash mismatch, subagent reviewer, and author self-review are rejected.
6. **P1-15 — covered:** exact evidence presence and digest checks, as detailed above.
7. **P1-20 — covered:** reordered input reuses records; substantive revision change invalidates stale approval.
8. **P1-16 — covered:** disabling and physically deleting an intake record preserve in-flight work.

## Conclusion

The three run_02 findings and all eight prior findings are covered by the current suite. The remaining rejection is a delivery traceability issue: update the AUTO-05 task record so its candidate and run binding correspond to `ac820925bf14f5d2b4864dd1f01b9784939a453e` and `run_03`, then obtain a review against the aligned record.