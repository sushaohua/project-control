# AUTO-06 run_01 QA Findings & Rework Note 01

- **Task**: AUTO-06 (M3定时调度：单实例systemd用户服务部署与P1-14零空耗及重启恢复独立验收)
- **Review Run**: run_01
- **Reviewed Candidate**: `62075f28bfad48248d7c87a91af3b52ae4519000`
- **Reviewer**: Independent Host Codex QA (`role: QA`, model `gpt-6-luna`, session `01a1a109-204e-7b50-aa71-c911d22c3aa5`)
- **Decision**: `REJECTED`
- **Report**: `docs/evidence/coord_automation/AUTO-06/runs/run_01/qa_review_report.md`

---

## 1. QA Findings Summary

### Finding 1: P1-14 stop/restart recovery is not exercised with an actual service process
- **Issue**: In `test_coord_systemd_service.py`, `test_service_stop_and_restart_recovery_preserves_state_and_locks` saved state, manually called `runner_1.state_store.release_process_lock()`, created `runner_2`, and restored checkpoint. It did not exercise an actual running service daemon process receiving SIGTERM (simulating `systemctl stop/restart`), gracefully flushing checkpoint, releasing flock, and terminating, followed by a new process instance resuming under the released lock.
- **Rework Required**:
  1. Test actual process-level service shutdown/restart: run the daemon service loop in a background process/thread.
  2. Send `SIGTERM` (the exact signal sent by `systemctl stop` and `systemctl restart`).
  3. Verify the daemon's SIGTERM signal handler sets `_running = False`, flushes checkpoint, releases the flock, and cleanly terminates.
  4. Launch the second instance (simulating restart), verify it successfully acquires the lock, restores state from SQLite WAL / checkpoint, and confirms in-flight tasks and state are completely preserved.
  5. Also test `service_ctl.py` stop/restart actions against a mock or simulated service.

### Finding 2: Crontab verification can pass when inspection fails
- **Issue**: In `service_ctl.py:133-134`, `verify_crontab_isolation()` returned `crontab_clean: True` on any non-zero exit code of `crontab -l`, noting "No crontab installed or inaccessible". If crontab is inaccessible or encounters a permissions/system error, it must NOT report clean.
- **Rework Required**:
  1. In `service_ctl.py`: when `crontab -l` exits non-zero, check whether stdout/stderr indicates absent crontab (e.g. "no crontab for"). If absent, report clean. If any other error (inaccessible, permission denied, etc.), report `crontab_clean: False` with error details.
  2. In `test_coord_systemd_service.py`: add explicit test cases asserting that an unexpected failure or inaccessible crontab reports `crontab_clean: False`.

---

## 2. Constraints for Rework 01
- **AST Limits**: All newly added or edited Python functions must strictly obey $\le 50$ lines and $\le 4$ parameters.
- **Code Scope**: Zero changes to `soc-ap/`, `mcu-p3/`, `test_harness/`, or `boot/*`. Only touch allowed paths in `project-control`.
- **Existing Crontab**: Keep user's existing `sync_md.sh` crontab completely untouched.
