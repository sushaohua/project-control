---
task_id: AUTO-06
task_revision: 1
reviewer_role: QA
actual_session: "01a1a113-8a0d-79d0-a132-8ec5d3264898"
reviewed_artifact_version: dd562f3e6afad1f2c0e1f44fcc10ab6a78e7c855
decision: REJECTED
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-06/runs/run_02/server_qa.json
  sha256: feec9970d376d188724b7921475eb7707e3c5304851d3e892866ce509dbdf85e
reviewed_artifacts:
  - path: "project-control/config/coord_runner/ai-soc-coord-runner.service"
    sha256: "11412bddac62a4ca17267201719297135983a927b6dd358739363716d3877d51"
  - path: "project-control/tools/coord_runner/service_ctl.py"
    sha256: "b25d017186a2aa83651d8db76a38e3b069cff8452a3bb05191486bc5abf04165"
  - path: "project-control/tools/test_coord_systemd_service.py"
    sha256: "99dc0f613ef549e1342dc930040dc8f59f5c1eaa027d5468377183d81235b374"
  - path: "project-control/docs/operations/coord_runner_systemd_service_20261103.md"
    sha256: "369c741511f53580599df40d13280dc8303bf5c8e910970833afac72728619a1"
  - path: "project-control/docs/evidence/coord_automation/AUTO-06/runs/run_01/result.md"
    sha256: "d2454323096f14a6edb02a784244f428deb3a26dc0d1056c43fb3da7573b8a4a"
  - path: "project-control/docs/evidence/coord_automation/AUTO-06/runs/run_02/result.md"
    sha256: "6e8239fe9e8993f3c1bd7c3f7b0923e7ff8cba41fad979254a7092b768799b0b"
content_audit:
  fact_sources:
    result: passed
    basis: "Compared the task card, confirmation rev 2, design rev 2, prior run_01 QA report and rework note, candidate artifacts, and pinned run_02 server evidence."
  protocol_compatibility:
    result: not-applicable
    basis: "The reviewed change manages a systemd service and does not modify protocol or firmware behavior."
  claim_scope:
    result: passed
    basis: "Pinned server QA evidence matches the candidate and records the required tests passing; the stale operations guide test count is identified below."
  architecture_completeness:
    result: passed
    basis: "The unit and controller cover the requested daemon lifecycle, crontab isolation, and recovery design; the required restart behavior is now exercised at process level."
---

# Independent QA Review — AUTO-06 run_02

**Decision: REJECTED**

## Evidence and candidate binding

The host-side `server_qa.json` SHA256 matches the required value and binds candidate `dd562f3e6afad1f2c0e1f44fcc10ab6a78e7c855` to container `766372054d5d`, image digest `sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f`, and a read-only checkout mount. The checkout log records fetching and checking out that candidate. The pinned test evidence reports the dedicated service suite passing all 15 tests, the P1-14 idle test and recovery test passing, and no AST violations. The specified deliverable hashes match.

## Prior findings

- **F-01, SIGTERM stop/restart recovery: resolved.** The revised test starts a separate Python daemon process running `run_daemon`, verifies a second runner cannot acquire its flock, sends `SIGTERM`, checks exit code 0, and verifies a new instance reacquires the lock and restores the in-flight task, revision, state, and completed-task checkpoint. The daemon signal handler saves the checkpoint and its `finally` block releases the lock.
- **F-02, crontab error handling: resolved.** `verify_crontab_isolation()` accepts only recognized absent-crontab/missing-command messages as clean; other nonzero results return `crontab_clean: False`. The server run records passing absent-crontab, missing-executable, and command-failure tests.
- **P1-14 idle calls: passed.** The test checks 20 consecutive idle, blocked, and completed-task cycles and asserts zero model calls.
- **Scope and AST: passed.** The pinned checkout evidence binds the other repositories to their baseline commits. The candidate artifacts are within the task’s `project-control` scope. Server QA reports zero AST violations for the reviewed Python files.

## Finding

**F-03 — Operations guide reports an outdated test count.**  
The current suite has 15 tests, as shown in the run_02 server log and test file, but the operations guide says “12 tests” in its acceptance section. This makes the documented expected result inaccurate for the delivered candidate. Update the count and align the guide with the current suite.

The prior run_01 QA report was available on the host and was reviewed alongside its rework note. No QA auto-generated issues were found in the inspected evidence. The run_02 evidence demonstrates the software test results; this report does not establish a separate live systemd deployment.

## Required rework

Correct the operations guide’s test count and any related stale acceptance wording, then submit a new candidate for independent review.