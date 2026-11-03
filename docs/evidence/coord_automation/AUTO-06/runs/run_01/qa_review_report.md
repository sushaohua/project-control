---
task_id: AUTO-06
task_revision: 1
reviewer_role: QA
actual_session: "01a1a109-204e-7b50-aa71-c911d22c3aa5"
reviewed_artifact_version: 62075f28bfad48248d7c87a91af3b52ae4519000
decision: REJECTED
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-06/runs/run_01/server_qa.json
  sha256: ad25a8a46e3302f21d1ce6c62f4b70c6c7d2ee98627f05331469a0017a45d1e6
reviewed_artifacts:
  - path: "project-control/config/coord_runner/ai-soc-coord-runner.service"
    sha256: "11412bddac62a4ca17267201719297135983a927b6dd358739363716d3877d51"
  - path: "project-control/tools/coord_runner/service_ctl.py"
    sha256: "5416311cf9c9c22974987dc693a6dae31488bca68276312d1b8825fc7c5afc9f"
  - path: "project-control/tools/test_coord_systemd_service.py"
    sha256: "021266979b5b12a5a89200a2a916b46a94943fc648105c20d77af1c36504a095"
  - path: "project-control/docs/operations/coord_runner_systemd_service_20261103.md"
    sha256: "369c741511f53580599df40d13280dc8303bf5c8e910970833afac72728619a1"
  - path: "project-control/docs/evidence/coord_automation/AUTO-06/runs/run_01/result.md"
    sha256: "d2454323096f14a6edb02a784244f428deb3a26dc0d1056c43fb3da7573b8a4a"
content_audit:
  fact_sources:
    result: passed
    basis: "Reviewed the task card, confirmation rev 2, design rev 2, candidate artifacts, and pinned server QA evidence."
  protocol_compatibility:
    result: not-applicable
    basis: "This delivery adds systemd service management and tests; it makes no protocol or firmware changes."
  claim_scope:
    result: passed
    basis: "The server evidence binds the specified candidate and reports the dedicated suite passing; unsupported recovery and crontab claims are identified below."
  architecture_completeness:
    result: passed
    basis: "The unit and operations guide cover the requested service, linger, WSL2 sleep boundary, and crontab isolation; the recovery verification gap is recorded below."
---

# Independent QA Review — AUTO-06 run_01

**Decision: REJECTED**

## Evidence reviewed

The candidate is identified as `62075f28bfad48248d7c87a91af3b52ae4519000`. The server QA evidence hash matches the required SHA256 and records the pinned candidate, isolated container, read-only snapshot mount, and a passing dedicated test run. The runtime log shows all 12 tests in `test_coord_systemd_service.py` passing. Candidate artifact hashes also match the supplied expected values.

The unit has `[Unit]`, `[Service]`, and `[Install]` sections; starts `python3 -m tools.coord_runner --daemon` with a config path; sets the workspace, `Restart=on-failure`, and `RestartSec=5s`. `service_ctl.py` provides the requested lifecycle, status, linger, and crontab commands. The operations guide documents linger enablement, WSL2 sleep boundaries, and crontab isolation.

## Findings

1. **P1-14 stop/restart recovery is not exercised.** In `test_service_stop_and_restart_recovery_preserves_state_and_locks`, the test saves state, directly releases the lock, constructs a second `CoordRunner`, and restores a checkpoint. It does not invoke `systemctl stop/start/restart`, terminate a service process, or verify shutdown persistence from an actual service lifecycle. The result report describes this as service stop/restart recovery, but the test only covers runner-level lock release and checkpoint restoration. This leaves the required service recovery behavior unverified.

2. **Crontab verification can pass when inspection fails.** `verify_crontab_isolation()` returns `crontab_clean: true` for any nonzero `crontab -l` result, describing the result as “No crontab installed or inaccessible.” An inaccessible crontab is indistinguishable from an absent one, so the gate can report clean without verifying the existing `sync_md.sh` entry or isolation. The test does not cover this failure case.

The service unit and basic controller structure meet the stated checks, and the idle-cycle test asserts zero calls across 20 cycles. The findings above prevent approval of the recovery and crontab acceptance claims.