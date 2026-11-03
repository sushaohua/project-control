---
task_id: AUTO-05
task_revision: 1
reviewer_role: ARCH
actual_session: "01a1a0b2-f27e-7072-b150-2c008217c3f6"
reviewed_artifact_version: a49b986dbe98df3bb2dcd19da01c34777f8e19ae
decision: REJECTED
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-05/runs/run_01/server_qa.json
  sha256: b10278e908de6444eea22c7b50e5e7f53a6f6d66b7a6e63c009e2e6aa350f261
reviewed_artifacts:
  - path: "project-control/tools/test_phase1_intake_acceptance.py"
    sha256: "daa6c01dfdeffda968d3b8b296021ea2e1516a2169a3b4cde6b26f4f57a212b9"
  - path: "project-control/docs/evidence/coord_automation/AUTO-05/runs/run_01/result.md"
    sha256: "dea22b94aa1440c9b13d8e91c0d0d79a555b8f3ac7ad23a29da28386193273a5"
content_audit:
  fact_sources:
    result: passed
    basis: "Candidate, pinned server QA record, Docker inspect evidence, and both deliverable hashes were checked. The server evidence identifies candidate a49b986dbe98df3bb2dcd19da01c34777f8e19ae, fresh checkout, container c6d7624e911f, and image digest sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f."
  protocol_compatibility:
    result: not-applicable
    basis: "This review covers an acceptance suite and evidence report; the candidate changes no protocol implementation."
  claim_scope:
    result: passed
    basis: "The report’s acceptance claims were compared with the test bodies and server output. Several claims exceed their demonstrated coverage; details are listed below."
  architecture_completeness:
    result: passed
    basis: "Architectural review completed. The required M1/M2 clause evidence is incomplete for multiple criteria, so the candidate is rejected pending corrected tests and claims."
---

# ARCH Review — AUTO-05 run_01

## Decision

**REJECTED.** The sandbox and artifact bindings are verifiable, and the candidate respects the file boundary. However, the acceptance suite and `result.md` claim complete, faithful verification of all 19 M1/M2 clauses that the tests do not demonstrate.

## Evidence and boundary checks

- The candidate diff from `4c58c46be12af0e4dcfc4ef6f40dd162c5b18c06` to `a49b986dbe98df3bb2dcd19da01c34777f8e19ae` adds only `tools/test_phase1_intake_acceptance.py` and `docs/evidence/coord_automation/AUTO-05/runs/run_01/result.md`, both within `allowed_paths`.
- No changes appear in `tools/coord_runner/**`, `soc-ap`, `mcu-p3`, `test_harness`, or bootloader paths. The diff contains no systemd service files.
- The requested SHA256 values match the checked-out bytes for both deliverables and `server_qa.json`.
- Server evidence records a fresh, read-only bind mount, the expected candidate commit, and a passed test run. The container’s exit code 137 is explained in `host_runner_provenance.json` as its expected shutdown after tests completed; it does not contradict the recorded test exits.
- `result.md` reports 20 tests, all passing. That establishes execution success, but does not establish that each test covers the clause described.
- The suite’s function-size and parameter check passed in the recorded sandbox run. The diff boundary is also satisfied.

## Material coverage defects

1. **P1-09 — five-source crash/timeout reconciliation:** The named test writes one `pid.json` containing a made-up nonexistent PID and checks `RECONCILE_REQUIRED`. It does not exercise a timeout or crash, reconcile five sources, or establish dispatch-key lookup against the external host. The result’s “five-source” claim is unsupported by this test.

2. **P1-08 — external async execution and concurrency limit:** The test starts two local Python sleep processes via `JobLauncher`. It does not exercise an external role/QA executor, actual ready-task advancement, or the stated maximum of two concurrently advancing tasks. Process liveness alone does not prove the clause.

3. **P1-07 — in-flight revision conflict referral:** The test checks a boolean from `check_in_flight_revision`; it does not assert a referral to COORD, preserve the old/new revision bindings in a result, or verify the required audit trail.

4. **P1-11 — exit 0 and QA rejection must block Done:** The test validates empty/zero commit hashes and a remediation-limit exception. It does not test that a successful role exit with missing evidence, or a QA rejection, prevents a transition to `Done`.

5. **P1-12 — forged QA rejection:** The test rejects `subagent` and same-author session entries. It does not verify the report’s claimed unpushed-candidate and report-hash-mismatch cases in this acceptance test.

6. **P1-15 — real bounded software drill:** The test reads prior AUTO-03/AUTO-04 drill summaries and checks selected fields. It does not verify their hashes or bind the asserted summaries to the exact candidate, server QA evidence, and independent review record. The report’s statement that this test verifies the full real drill is too broad.

7. **P1-20 — substantive revision behavior:** The test verifies input reordering produces no new generated paths. It does not test a substantive change requiring a new revision or prove that an old approval is rejected for the changed scope.

8. **P1-16 — deletion protection:** The test checks that setting `enabled: false` preserves an active card, but does not delete the intake entry and verify that deletion also leaves in-flight work intact.

These are coverage gaps in the delivered acceptance artifact and overstatements in its results record. A passing test run cannot close them. Other clauses have corresponding tests, but their report summaries should remain limited to what the assertions actually establish.

## Required correction

Add assertions for the missing behaviors and bind the P1-15 evidence to the precise candidate and referenced artifact hashes, or narrow the report’s coverage claims where the task permits. Then produce a new candidate and run for independent review. The current read-only checkout prevents me from writing this report into the requested evidence path; this response contains the report contents.