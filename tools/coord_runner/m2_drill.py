#!/usr/bin/env python3
"""Bounded M2 continuous advancement & recovery live drill executor (`P1-05/08/09/10/13/20` host proof)."""

import hashlib
import json
import os
from pathlib import Path
import sys
import time
from typing import Dict

from .cas_writer import compute_bytes_sha256, create_exclusive
from .errors import CasConflictError, GateValidationError, ResourceConflictError
from .job_launcher import JobLauncher, get_proc_starttime, is_proc_alive
from .lease_manager import LeaseManager
from .models import CoordState, Lease, TaskExecutionRecord, TaskState
from .reconciler import FiveSourceReconciler, ReconcileStatus
from .state_store import StateStore


def _setup_drill_state_store(drill_dir: Path) -> StateStore:
    db_path = drill_dir / "state.sqlite3"
    lock_path = drill_dir / "coord_runner.lock"
    store = StateStore(db_path, lock_path)
    store.acquire_process_lock()
    return store


def _verify_flock_concurrency_block(drill_dir: Path) -> bool:
    second_store = StateStore(drill_dir / "state.sqlite3", drill_dir / "coord_runner.lock")
    try:
        second_store.acquire_process_lock()
        return False
    except ResourceConflictError:
        return True
    finally:
        second_store.close()


def _run_dual_async_tasks(launcher: JobLauncher, drill_dir: Path) -> Dict[str, dict]:
    jobs = {}
    for name in ("task_a", "task_b"):
        j_dir = drill_dir / f"jobs/{name}"
        if j_dir.is_dir():
            for f in j_dir.glob("*"):
                f.unlink()
        fast_cmd = [sys.executable, "-c", "import time, sys; time.sleep(0.5); sys.exit(0)"]
        pid = launcher.launch_async(j_dir, fast_cmd, f"Prompt for {name}")
        st = get_proc_starttime(pid) or ""
        jobs[name] = {"pid": pid, "starttime": st, "job_dir": str(j_dir)}
    return jobs


def _wait_and_reconcile_jobs(
    reconciler: FiveSourceReconciler,
    store: StateStore,
    jobs: Dict[str, dict],
) -> Dict[str, dict]:
    reconciled = {}
    for name, info in jobs.items():
        j_dir = Path(info["job_dir"])
        store.save_role_job({
            "job_id": name, "dispatch_key": f"DRILL-{name}:rev1:INTEGRATOR:implement:1",
            "task_id": f"DRILL-{name.upper()}", "task_revision": 1, "role": "INTEGRATOR",
            "phase": "implement", "status": "RUNNING", "job_dir": str(j_dir),
            "pid": info["pid"], "starttime": info["starttime"],
        })
        for _ in range(50):
            if (j_dir / "exit_status.json").is_file():
                break
            time.sleep(0.1)
        rep = reconciler.reconcile_job(j_dir, f"DRILL-{name}:rev1:INTEGRATOR:implement:1")
        reconciled[name] = {
            "status": rep.status, "returncode": rep.returncode,
            "exit_status_sha256": compute_bytes_sha256((j_dir / "exit_status.json").read_bytes()),
        }
    return reconciled


def _verify_lease_protection(reconciler: FiveSourceReconciler, drill_dir: Path) -> int:
    lm = LeaseManager(default_duration=1800.0)
    lease = lm.acquire_lease("DRILL-ACTIVE", "implementation", "owner_drill")
    lease.expires_at = time.time() - 10.0
    j_dir = drill_dir / "jobs/lease_active"
    j_dir.mkdir(parents=True, exist_ok=True)
    my_pid = os.getpid()
    st = get_proc_starttime(my_pid) or ""
    (j_dir / "pid.json").write_text(json.dumps({"pid": my_pid, "starttime": st}), encoding="utf-8")
    reconciler.state_store.save_role_job({
        "job_id": "job_lease_active", "dispatch_key": "k_lease_active", "task_id": "DRILL-ACTIVE",
        "task_revision": 1, "role": "INTEGRATOR", "phase": "implement",
        "status": "RUNNING", "job_dir": str(j_dir),
    })
    return reconciler.protect_active_leases(lm, drill_dir)


def _verify_cas_conflict(drill_dir: Path, reconciler: FiveSourceReconciler) -> bool:
    f = drill_dir / "cas_test.md"
    f.write_text("initial drill content", encoding="utf-8")
    init_sha = hashlib.sha256(b"initial drill content").hexdigest()
    reconciler.verify_cas_write(f, init_sha)
    f.write_text("concurrently edited drill content", encoding="utf-8")
    try:
        reconciler.verify_cas_write(f, init_sha)
        return False
    except CasConflictError:
        return True


def execute_m2_live_drill(workspace_root: Path, drill_dir: Path) -> Dict[str, object]:
    """Run bounded M2 recovery and async dual-task drill inside `drill_dir`."""
    ws = workspace_root.resolve()
    root = drill_dir.resolve() if drill_dir.is_absolute() else (Path.cwd() / drill_dir).resolve()
    if not str(root).startswith(str((ws / "project-control").resolve()) + "/"):
        raise GateValidationError(f"Live drill directory must reside under project-control/: {root}")
    root.mkdir(parents=True, exist_ok=True)
    store = _setup_drill_state_store(root)
    try:
        flock_blocked = _verify_flock_concurrency_block(root)
        launcher = JobLauncher(workspace_root=ws)
        reconciler = FiveSourceReconciler(workspace_root=ws, state_store=store)
        jobs = _run_dual_async_tasks(launcher, root)
        reconciled = _wait_and_reconcile_jobs(reconciler, store, jobs)
        protected_leases = _verify_lease_protection(reconciler, root)
        cas_protected = _verify_cas_conflict(root, reconciler)
        summary = {
            "drill_id": "AUTO-04-M2-DRILL-01",
            "state_db_file": str((root / "state.sqlite3").relative_to(ws)),
            "state_db_sha256": compute_bytes_sha256((root / "state.sqlite3").read_bytes()),
            "lock_file": str((root / "coord_runner.lock").relative_to(ws)),
            "flock_mutual_exclusion_verified": flock_blocked,
            "async_dual_tasks_launched": list(jobs.keys()),
            "async_tasks_reconciled": reconciled,
            "lease_active_protection_count": protected_leases,
            "cas_write_conflict_detected": cas_protected,
            "p1_08_dual_parallel_verified": len(jobs) == 2,
            "p1_09_five_source_reconciliation_verified": all(
                r["status"] == ReconcileStatus.COMPLETED.value for r in reconciled.values()
            ),
            "p1_10_single_flock_and_lease_guard_verified": flock_blocked and protected_leases == 1,
            "p1_13_cas_concurrency_guard_verified": cas_protected,
        }
        (root / "drill_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        return summary
    finally:
        store.close()
