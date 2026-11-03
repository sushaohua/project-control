---
task_id: AUTO-04
task_revision: 1
reviewer_role: QA
actual_session: "01a1a07e-749c-7721-810a-9b3675cdc769"
reviewed_artifact_version: 7a2338a4ecd2bd5d6d73d7db5ab66961e4cb7d62
decision: REJECTED
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-04/runs/run_01/server_qa.json
  sha256: 2dafab575af795b70e0c7f789c67ef706ab635cf26a04fa3b4a2f1be976148c3
reviewed_artifacts:
  - path: "project-control/tools/coord_runner/state_store.py"
    sha256: "d8858738f06a94c77c131ec3c497e5b600954785ee1689866e4485cc962fc637"
  - path: "project-control/tools/coord_runner/job_launcher.py"
    sha256: "9463a4daa5f25dbfdef4316294b77638170e3b3e961ab95919d9bd3bbb07e429"
  - path: "project-control/tools/coord_runner/reconciler.py"
    sha256: "90289fed609ea8b5bc6b45c9a77bc2b7f3e2063976771feb7aa3afa7775d8602"
  - path: "project-control/tools/coord_runner/runner.py"
    sha256: "7081e498370601acd05817c5570cdb7a5f13d030415378d7ac5a1f063f150e61"
  - path: "project-control/tools/test_coord_recovery.py"
    sha256: "641d49979e8917c10e2da7ff403916f2e2979e01a70d2e2546ed25898848ab4f"
  - path: "project-control/docs/evidence/coord_automation/AUTO-04/runs/run_01/result.md"
    sha256: "1c8bcff7abd49c0c091e76c34f6a0792959a45bb40ca9b42930dc8cb2eff21e0"
content_audit:
  fact_sources:
    result: passed
    basis: "Task card, confirmation revision 2, design revision 2, pinned candidate snapshot, and server QA evidence were inspected."
  protocol_compatibility:
    result: not-applicable
    basis: "This change is scoped to coordinator persistence, job execution, and recovery; it does not alter an external device or wire protocol."
  claim_scope:
    result: passed
    basis: "The report limits its findings to M2 software behavior and does not claim hardware validation or M3 service deployment."
  architecture_completeness:
    result: passed
    basis: "M2 requirements were compared against runner integration and drill evidence; the missing async orchestration path is recorded as finding F-01 below."
---

# Independent QA Review — AUTO-04 run_01

## Decision

**REJECTED** for candidate `7a2338a4ecd2bd5d6d73d7db5ab66961e4cb7d62`.

The pinned snapshot and server evidence are bound to the requested candidate. The required artifact hashes match. The blocking defect is that asynchronous task dispatch is implemented as an isolated method but is not connected to the runner’s normal scheduling path.

## Findings

### F-01 — P1-08 async dispatch is not integrated

`CoordRunner.step()` processes in-flight work through `_process_task_safely()` → `process_task()` → `_execute_agent_phase()`, which invokes the synchronous `agent_executor`. No production call site invokes `dispatch_async_role_task()`; the only match in `tools/coord_runner` is its definition in `runner.py`. As a result, long-running role execution still blocks the scheduler and prevents another ready task from advancing during that call.

The live drill does not cover this path: `m2_drill.py` starts two short Python sleep subprocesses directly through `JobLauncher`, then reconciles them. It does not run two coordinator tasks with one long-running role job while another task advances. The server-reported unit tests pass, but this does not establish the required P1-08 orchestration behavior.

**Required correction:** connect async job launch and completion collection to the normal runner lifecycle, then provide evidence that a long-running role task does not block a second non-conflicting ready task from actually advancing, within the two-task limit.

### F-02 — P1-05 idempotency guard is not wired into intake rescanning

`FiveSourceReconciler.check_intake_idempotence()` checks the stored digest, but a repository search found no caller. The guard therefore does not establish that rescanning a matching `(id, revision, content_sha256)` submission avoids creating another task or job. The result record cites the method as coverage, while the test evidence exercises the helper rather than an integrated rescan path.

**Required correction:** wire the digest guard into the intake/rescan flow and verify repeated scans return the existing association without adding tasks or jobs.

## Scope and evidence audit

- The reviewed checkout is at the pinned candidate commit. The server checkout log records fetching and checking out that same full commit; `server_qa.json` records a fresh container checkout, read-only workspace mount, container ID `b8de2e683a94`, and image digest `sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f`.
- The SHA256 of host-side `server_qa.json` matches the required digest. Server verdict is `PASSED`; recorded recovery, M1 regression, QA runner, delivery checks, and AST checks report success. These results do not resolve F-01 or F-02.
- The candidate diff contains 28 paths, all within the task’s declared `allowed_paths`. No changes touch `soc-ap`, `mcu-p3`, `test_harness`, or bootloaders. The diff contains no systemd service/timer files; a read-only check of the expected systemd unit directories found no `coord` or `ai_soc` service/timer files.
- The AST size/parameter scan found no violations among `tools/coord_runner/*.py` and `tools/test_coord_recovery.py`.
- The live drill’s CAS case verifies the reconciler’s digest check rejects changed file content. It does not demonstrate the actual write path’s behavior under a concurrent edit in the normal coordinator flow.
- No hardware validation is applicable to this software-only M2 scope. No M3 service deployment is claimed.