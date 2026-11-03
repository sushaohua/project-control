---
task_id: AUTO-05
task_revision: 1
reviewer_role: ARCH
actual_session: "01a1a0dd-26f2-72e0-8298-6536a2fd1f43"
reviewed_artifact_version: bc7c766cf390ee844c92f66fc22f92faf28e1b8d
decision: REJECTED
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-05/runs/run_02/server_qa.json
  sha256: 5013c6530b5fbfe29add99e33dc10986d69f10d21975cb5400406bf33c579783
reviewed_artifacts:
  - path: "project-control/tools/test_phase1_intake_acceptance.py"
    sha256: "a2f844c59dddcc915503bf5b36b23844b2f8a7bda3a80792d59bbc7cf71f0aa5"
  - path: "project-control/docs/evidence/coord_automation/AUTO-05/runs/run_01/result.md"
    sha256: "a52fb1191917af9c8e6e8b355c31a1d3a918c93bee364f570cdeaac7c6f9c423"
content_audit:
  fact_sources:
    result: passed
    basis: "Recomputed both required deliverable SHA256 values and the planning confirmation SHA256 from the read-only checkout. Verified HEAD equals the pinned candidate and checked server_qa.json against the supplied SHA256; server_lock.json and checkout.log bind the fresh sandbox checkout to candidate bc7c766cf390ee844c92f66fc22f92faf28e1b8d."
  protocol_compatibility:
    result: not-applicable
    basis: "This review covers an acceptance suite and its results record; no protocol implementation is under review."
  claim_scope:
    result: passed
    basis: "The report's overall acceptance claims were compared with the test assertions and server test record. Run 02 passes in the sandbox, but three requested behaviors remain unproven by the designated acceptance tests; details follow."
  architecture_completeness:
    result: passed
    basis: "Reviewed all eight Run 01 findings, the task card, confirmation rev 2, design rev 2, approval record, pinned sandbox evidence, and protected business-code paths. Architectural acceptance remains blocked by unresolved coverage gaps in P1-07, P1-08, and P1-15."

# ARCH Review — AUTO-05 run_02

## Decision

**REJECTED.** The candidate and sandbox evidence are bound to the requested commit, and the acceptance suite passes in the recorded server sandbox. However, the delivered test bodies do not fully satisfy three of the eight required Run 01 corrections. The passing run establishes that the tests executed successfully; it does not close these coverage gaps.

## Evidence and boundary checks

- The checkout HEAD is `bc7c766cf390ee844c92f66fc22f92faf28e1b8d`, matching the requested candidate. The server lock and checkout log record fetching and checking out that commit. The sandbox record identifies a fresh read-only bind mount and container image digest `sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f`.
- The supplied hashes match the checked-out test suite, Run 01 result record, confirmation rev 2, and server QA record.
- `server_qa.json` records the acceptance suite and other sandbox commands passing. The AST gate reports no violations in the acceptance suite.
- The protected `soc-ap`, `mcu-p3`, `test_harness`, and `boot/*` business-code paths have no changes in the candidate checkout.
- The Run 01 result accurately lists the prior findings and claimed corrections, but its overall “all corrected” assertion exceeds the tests for P1-07, P1-08, and P1-15 below.

## Run 01 finding audit

1. **P1-09 — crash reconciliation via dispatch key: covered.** The named test launches a real child process, kills it with `os.kill(pid, signal.SIGKILL)`, reconciles against a dispatch-key record in SQLite, checks `RECONCILE_REQUIRED`, and then checks completion after an exit status is written. This establishes the requested crash simulation and reconciliation behavior within the test fixture.

2. **P1-08 — asynchronous advancement and concurrency limit: incomplete.** The test dispatches three task records directly through `dispatch_task`, verifies two are in flight and the third is blocked, then releases a lease and dispatches the third. It does not execute the requested `step()` loop or launch and monitor a long-running asynchronous job while a second ready task advances. The direct dispatch calls do not demonstrate nonblocking scheduler advancement around an async job.

3. **P1-07 — in-flight revision conflict referral: incomplete.** The test detects a revision conflict and confirms the stored task remains at revision 1 and `InProgress`. It does not assert a `COORDINATOR_REFERRAL`, create audit referral records, or prove that both old and new revision bindings are preserved in those records.

4. **P1-11 — exit 0 and QA rejection block Done: covered.** The test checks that a missing deliverable is rejected, a QA `REJECTED` decision blocks Done, and missing non-author report review blocks Done.

5. **P1-12 — forged QA rejection and unpushed candidate: covered.** The test checks rejection of an unpushed candidate, a report SHA mismatch, and `platform: subagent`, as well as same-author review rejection.

6. **P1-15 — bounded software drill evidence: incomplete.** The test verifies M1 and M2 summary files exist and checks the M1 manifest digest, candidate binding, approval decision, and selected M2 flags. It does not verify exact SHA256 digests for both live drill summaries and the deliverable manifest as required. The M2 report check is conditional on the file existing, so absence of that report does not fail the test. The requested complete evidence binding is therefore not established.

7. **P1-20 — substantive revision requires fresh approval: covered.** The test checks that reordered input generates no duplicate records and that an approval bound to revision 1 is rejected when revision 2 is targeted.

8. **P1-16 — deletion protection: covered.** The test separately checks preservation of `InProgress` work after setting `enabled: false` and after physically deleting the entry.

## Required correction

Close the P1-07, P1-08, and P1-15 gaps with assertions for the referral and audit bindings, actual scheduler-step async advancement with a third-task concurrency rejection, and exact presence/hash verification of all required live-drill summaries and manifest. Produce a new candidate and run for independent review.