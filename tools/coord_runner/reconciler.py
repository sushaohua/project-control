#!/usr/bin/env python3
"""五源防重对账器与孤儿进程清理模块（对齐 SQLite、`exit_status.json`、`/proc`、JSONL 事件流与宿主机 Codex DB）。"""

from dataclasses import dataclass, field
from enum import Enum
import json
import os
from pathlib import Path
import sqlite3
import time
from typing import Dict, List, Optional, Tuple

from .cas_writer import compute_bytes_sha256
from .errors import CasConflictError, CoordRunnerError
from .job_launcher import is_proc_alive
from .lease_manager import LeaseManager
from .models import Lease, TaskState
from .state_store import StateStore

DEFAULT_CODEX_HOME = Path.home() / ".codex"
DEFAULT_MAX_JOB_TIMEOUT = 1800.0


class ReconcileStatus(str, Enum):
    """五源对账归一化后的作业状态枚举。"""
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    RECONCILE_REQUIRED = "RECONCILE_REQUIRED"
    NOT_FOUND = "NOT_FOUND"


@dataclass(frozen=True)
class ReconcileReport:
    """跨五类状态源汇总得到的单个角色作业对账报告。"""
    job_id: str
    dispatch_key: str
    status: str
    thread_id: Optional[str] = None
    returncode: Optional[int] = None
    reconcile_required: bool = False
    alive: bool = False
    detail: str = ""


class FiveSourceReconciler:
    """统筹 SQLite、`/proc`、JSONL 事件流、宿主机 Codex 数据库与 `exit_status.json` 的五源状态对齐器。"""

    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        state_store: Optional[StateStore] = None,
        codex_home: Optional[Path] = None,
    ):
        """初始化五源对账器，绑定工作区根路径、状态存储与宿主机 `.codex` 目录。"""
        self.workspace_root = Path(workspace_root or ".").resolve()
        self.state_store = state_store or StateStore()
        self.codex_home = Path(codex_home or DEFAULT_CODEX_HOME).resolve()
        self.max_timeout = DEFAULT_MAX_JOB_TIMEOUT

    def _lookup_host_thread(self, dispatch_key: str) -> Optional[str]:
        """以只读模式查询宿主机 `~/.codex/state_5.sqlite`，按派发键前缀检索已启动的会话 thread_id。"""
        db_path = self.codex_home / "state_5.sqlite"
        if not db_path.is_file():
            return None
        prefix = f"[COORD_DISPATCH_KEY:{dispatch_key}]%"
        try:
            uri = f"file:{db_path}?mode=ro"
            conn = sqlite3.connect(uri, uri=True, timeout=2.0)
            try:
                cur = conn.execute(
                    "SELECT id FROM threads WHERE first_user_message LIKE ? ORDER BY created_at DESC LIMIT 1;",
                    (prefix,),
                )
                row = cur.fetchone()
                return str(row[0]) if row and row[0] else None
            finally:
                conn.close()
        except sqlite3.Error:
            return None

    def _extract_events_thread(self, job_dir: Path) -> Optional[str]:
        """从作业目录的 `codex_events.jsonl` 中提取 `session_started` 事件记录的 `thread_id`。"""
        events_file = job_dir / "codex_events.jsonl"
        if not events_file.is_file():
            return None
        try:
            for line in events_file.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                evt = json.loads(line)
                if evt.get("type") == "session_started" and evt.get("thread_id"):
                    return str(evt["thread_id"])
        except (OSError, json.JSONDecodeError):
            pass
        return None

    def _check_exit_status(self, job_dir: Path) -> Optional[Tuple[str, int]]:
        """检查 `exit_status.json` 是否已落盘，解析返回 (归一化状态, 进程退出码)。"""
        status_file = job_dir / "exit_status.json"
        if not status_file.is_file():
            return None
        try:
            info = json.loads(status_file.read_text(encoding="utf-8"))
            rc = int(info["returncode"])
            st = ReconcileStatus.COMPLETED.value if rc == 0 else ReconcileStatus.FAILED.value
            return st, rc
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            return ReconcileStatus.RECONCILE_REQUIRED.value, 1

    def _inspect_process(self, job_dir: Path) -> Tuple[bool, Optional[int], Optional[str]]:
        """读取 `pid.json` 并结合 `/proc/<pid>/stat` 启动时间戳核验 Worker 进程是否真实存活。"""
        pid_file = job_dir / "pid.json"
        if not pid_file.is_file():
            return False, None, None
        try:
            p_data = json.loads(pid_file.read_text(encoding="utf-8"))
            pid = int(p_data["pid"])
            st = str(p_data.get("starttime", ""))
            return is_proc_alive(pid, st), pid, st
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            return False, None, None

    def reconcile_job(self, job_dir: Path, dispatch_key: str) -> ReconcileReport:
        """按 `exit_status.json` -> `/proc` -> 事件流 -> 宿主机 DB -> SQLite 的优先级对单个作业执行五源对账。"""
        j_dir = Path(job_dir).resolve()
        exit_info = self._check_exit_status(j_dir)
        thread_id = self._extract_events_thread(j_dir) or self._lookup_host_thread(dispatch_key)
        if exit_info is not None:
            st, rc = exit_info
            return self._finalize_completed_job(j_dir, dispatch_key, (st, rc, thread_id))
        alive, pid, st_time = self._inspect_process(j_dir)
        if alive and pid is not None:
            return self._handle_alive_job(j_dir, dispatch_key, (pid, st_time or "", thread_id))
        return self._handle_orphan_job(j_dir, dispatch_key, thread_id)

    def _finalize_completed_job(
        self,
        job_dir: Path,
        dispatch_key: str,
        outcome: Tuple[str, int, Optional[str]],
    ) -> ReconcileReport:
        """将已正常或异常退出的作业状态同步更新至 SQLite 并返回对账报告。"""
        status, returncode, thread_id = outcome
        job_id = job_dir.name
        self.state_store.update_role_job(job_id, {
            "status": status, "returncode": returncode, "thread_id": thread_id,
        })
        return ReconcileReport(
            job_id=job_id, dispatch_key=dispatch_key, status=status,
            thread_id=thread_id, returncode=returncode, reconcile_required=False, alive=False,
        )

    def _handle_alive_job(
        self,
        job_dir: Path,
        dispatch_key: str,
        proc_info: Tuple[int, str, Optional[str]],
    ) -> ReconcileReport:
        """处理仍在运行的作业进程：若超出最大超时阈值则发送 SIGTERM 并标记为 TIMEOUT。"""
        pid, starttime, thread_id = proc_info
        job_id = job_dir.name
        pid_file = job_dir / "pid.json"
        elapsed = time.time() - pid_file.stat().st_mtime if pid_file.is_file() else 0.0
        if elapsed > self.max_timeout:
            try:
                os.kill(pid, 15)
            except OSError:
                pass
            self.state_store.update_role_job(job_id, {
                "status": ReconcileStatus.TIMEOUT.value, "thread_id": thread_id,
            })
            return ReconcileReport(
                job_id=job_id, dispatch_key=dispatch_key, status=ReconcileStatus.TIMEOUT.value,
                thread_id=thread_id, reconcile_required=True, alive=False, detail="Process timed out",
            )
        self.state_store.update_role_job(job_id, {
            "status": ReconcileStatus.RUNNING.value, "pid": pid, "starttime": starttime, "thread_id": thread_id,
        })
        return ReconcileReport(
            job_id=job_id, dispatch_key=dispatch_key, status=ReconcileStatus.RUNNING.value,
            thread_id=thread_id, reconcile_required=False, alive=True, detail="Actively running",
        )

    def _handle_orphan_job(
        self,
        job_dir: Path,
        dispatch_key: str,
        thread_id: Optional[str],
    ) -> ReconcileReport:
        """处理进程已消失但缺少 exit_status.json 的孤儿作业，标记为 RECONCILE_REQUIRED 严禁盲目重派。"""
        job_id = job_dir.name
        detail = "Process terminated without exit_status; host thread observed" if thread_id else "Orphan process died"
        self.state_store.update_role_job(job_id, {
            "status": ReconcileStatus.RECONCILE_REQUIRED.value, "thread_id": thread_id,
        })
        return ReconcileReport(
            job_id=job_id, dispatch_key=dispatch_key, status=ReconcileStatus.RECONCILE_REQUIRED.value,
            thread_id=thread_id, reconcile_required=True, alive=False, detail=detail,
        )

    def reconcile_active_jobs(self, jobs_dir: Path) -> List[ReconcileReport]:
        """扫描 SQLite 中所有处于 RUNNING 状态的角色作业并逐一与宿主机五源状态对齐。"""
        active_jobs = self.state_store.list_role_jobs(status=ReconcileStatus.RUNNING.value)
        reports = []
        for job_row in active_jobs:
            j_dir = Path(job_row["job_dir"])
            rep = self.reconcile_job(j_dir, job_row["dispatch_key"])
            reports.append(rep)
        return reports

    def protect_active_leases(self, lease_mgr: LeaseManager, jobs_dir: Optional[Path] = None) -> int:
        """若租约账面时间已到期但其绑定的作业进程在 `/proc` 中仍然存活，则自动续期保护该租约（P1-10）。"""
        now = time.time()
        protected_count = 0
        for lease in lease_mgr._leases.values():
            if not lease.active or now < lease.expires_at:
                continue
            job_record = self.state_store.get_role_job(lease.task_id)
            if not job_record or not job_record.get("job_dir"):
                continue
            j_dir = Path(job_record["job_dir"])
            alive, _, _ = self._inspect_process(j_dir)
            if alive:
                lease.expires_at = now + lease_mgr.default_duration
                protected_count += 1
        return protected_count

    def record_intake_digest(
        self,
        demand_id: str,
        rev: int,
        content_sha: str,
    ) -> None:
        """在状态库中持久化记录收件单需求的权威 SHA256 摘要，用于幂等性门禁（P1-05）。"""
        meta_key = f"intake_digest:{demand_id}:rev{rev}"
        self.state_store.set_meta(meta_key, content_sha)

    def check_intake_idempotence(
        self,
        demand_id: str,
        rev: int,
        content_sha: str,
    ) -> bool:
        """检查相同 demand_id、revision 与内容摘要是否已在状态库中登记（已存在则返回 True，P1-05）。"""
        meta_key = f"intake_digest:{demand_id}:rev{rev}"
        stored_sha = self.state_store.get_meta(meta_key)
        if stored_sha is None:
            self.state_store.set_meta(meta_key, content_sha)
            return False
        return stored_sha == content_sha

    def check_in_flight_revision(self, task_id: str, new_revision: int) -> bool:
        """检查目标任务当前是否正在以不同的旧 revision 处于在途执行状态（P1-07）。"""
        state = self.state_store.load_coord_state()
        if not state or task_id not in state.in_flight_tasks:
            return False
        rec = state.in_flight_tasks[task_id]
        return rec.state in {TaskState.IN_PROGRESS.value, TaskState.CANDIDATE_PUSHED.value} and rec.task_revision != new_revision

    def record_revision_conflict_referral(
        self,
        task_id: str,
        incoming_revision: int,
        reason: str = "IN_FLIGHT_REVISION_CONFLICT",
    ) -> Optional[Dict[str, object]]:
        """当在途任务发生版本升级冲突时，记录 COORDINATOR_REFERRAL 审计转交记录而不强杀在途任务（P1-07）。"""
        state = self.state_store.load_coord_state()
        if not state or task_id not in state.in_flight_tasks:
            return None
        rec = state.in_flight_tasks[task_id]
        if rec.task_revision == incoming_revision:
            return None
        referral = {
            "action": "COORDINATOR_REFERRAL",
            "task_id": task_id,
            "active_revision": rec.task_revision,
            "incoming_revision": incoming_revision,
            "active_state": rec.state,
            "reason": reason,
        }
        meta_key = f"referral:{task_id}:rev{incoming_revision}"
        self.state_store.set_meta(meta_key, json.dumps(referral, sort_keys=True))
        return referral

    def verify_cas_write(self, target_path: Path, expected_sha: str) -> None:
        """写前校验目标文件当前磁盘 SHA256 与预期摘要是否一致，不一致则抛出 CasConflictError（P1-13）。"""
        target = Path(target_path).resolve()
        if not target.is_file():
            return
        actual_sha = compute_bytes_sha256(target.read_bytes())
        if actual_sha != expected_sha:
            raise CasConflictError(
                f"Concurrent edit detected on {target.name}: expected {expected_sha}, found {actual_sha}",
                {"path": str(target), "expected": expected_sha, "actual": actual_sha},
            )
