#!/usr/bin/env python3
"""模块职责：外部 SQLite WAL 状态存储与单实例 `flock` 进程锁管理器（设计方案 §7）。"""

import datetime
import fcntl
import json
import os
from pathlib import Path
import sqlite3
import time
from typing import Dict, List, Optional

from .errors import CoordRunnerError, ResourceConflictError
from .models import CoordState, Lease, TaskExecutionRecord, TaskState

DEFAULT_STATE_DB = Path("/home/sushaohua/.local/share/ai_soc_coord_runner/state.sqlite3")
DEFAULT_LOCK_FILE = Path("/home/sushaohua/.local/share/ai_soc_coord_runner/coord_runner.lock")
DEFAULT_COORD_SESSION = "8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5"


class StateStore:
    """权威外部 WAL 模式 SQLite 存储与单实例进程锁管理器。"""

    def __init__(
        self,
        db_path: Optional[Path] = None,
        lock_path: Optional[Path] = None,
        coord_session: str = DEFAULT_COORD_SESSION,
    ):
        """初始化 SQLite 状态库路径、锁文件路径并创建数据表。"""
        self.db_path = Path(db_path or DEFAULT_STATE_DB).resolve()
        self.lock_path = Path(lock_path or DEFAULT_LOCK_FILE).resolve()
        self.coord_session = coord_session
        self._lock_fd: Optional[int] = None
        self._is_locked = False
        self.init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """创建并配置启用 WAL 模式的 SQLite 数据库连接。"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path), timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        return conn

    def init_db(self) -> None:
        """初始化协调状态、在途任务、租约及角色作业所需的 SQLite 数据表。"""
        conn = self._get_connection()
        try:
            with conn:
                self._create_tables(conn)
        finally:
            conn.close()

    def _create_tables(self, conn: sqlite3.Connection) -> None:
        """创建 `coord_meta`、`in_flight_tasks` 等核心表并写入初始会话标识。"""
        conn.execute("""
            CREATE TABLE IF NOT EXISTS coord_meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at REAL NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS in_flight_tasks (
                task_id TEXT PRIMARY KEY,
                state TEXT NOT NULL,
                task_revision INTEGER NOT NULL,
                session_id TEXT,
                candidate_commit TEXT,
                corrections_count INTEGER NOT NULL,
                waiting_events TEXT NOT NULL,
                leases TEXT NOT NULL,
                runtime_context TEXT NOT NULL,
                updated_at REAL NOT NULL
            );
        """)
        self._create_job_and_lease_tables(conn)
        now = time.time()
        conn.execute(
            "INSERT OR IGNORE INTO coord_meta (key, value, updated_at) VALUES (?, ?, ?);",
            ("coord_session_id", self.coord_session, now),
        )

    def _create_job_and_lease_tables(self, conn: sqlite3.Connection) -> None:
        """创建已完成任务表、资源租约表及后台角色作业表。"""
        conn.execute("""
            CREATE TABLE IF NOT EXISTS completed_tasks (
                task_id TEXT PRIMARY KEY,
                completed_at REAL NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leases (
                lease_id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL,
                resource TEXT NOT NULL,
                owner TEXT NOT NULL,
                acquired_at REAL NOT NULL,
                expires_at REAL NOT NULL,
                active INTEGER NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS role_jobs (
                job_id TEXT PRIMARY KEY,
                dispatch_key TEXT UNIQUE NOT NULL,
                task_id TEXT NOT NULL,
                task_revision INTEGER NOT NULL,
                role TEXT NOT NULL,
                phase TEXT NOT NULL,
                pid INTEGER,
                starttime TEXT,
                thread_id TEXT,
                status TEXT NOT NULL,
                returncode INTEGER,
                job_dir TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            );
        """)

    def acquire_process_lock(self) -> bool:
        """获取 `coord_runner.lock` 上的非阻塞排他文件锁，若已被占用则抛出冲突异常。"""
        if self._is_locked:
            return True
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(str(self.lock_path), os.O_CREAT | os.O_RDWR, 0o644)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            payload = f"pid={os.getpid()}\nsession={self.coord_session}\ntime={time.time()}\n"
            os.ftruncate(fd, 0)
            os.write(fd, payload.encode("utf-8"))
            self._lock_fd = fd
            self._is_locked = True
            return True
        except (BlockingIOError, OSError) as err:
            os.close(fd)
            raise ResourceConflictError(
                f"Another coord_runner instance is holding lock at {self.lock_path}: {err}"
            ) from err

    def release_process_lock(self) -> None:
        """释放 `coord_runner.lock` 上的排他文件锁并关闭文件描述符。"""
        if self._is_locked and self._lock_fd is not None:
            try:
                fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
                os.close(self._lock_fd)
            except OSError:
                pass
            self._lock_fd = None
            self._is_locked = False

    def set_meta(self, key: str, value: str) -> None:
        """写入或更新单个协调器元数据键值对。"""
        conn = self._get_connection()
        try:
            with conn:
                conn.execute(
                    "INSERT OR REPLACE INTO coord_meta (key, value, updated_at) VALUES (?, ?, ?);",
                    (key, str(value), time.time()),
                )
        finally:
            conn.close()

    def get_meta(self, key: str) -> Optional[str]:
        """按键名查询单个协调器元数据值。"""
        conn = self._get_connection()
        try:
            cur = conn.execute("SELECT value FROM coord_meta WHERE key = ?;", (key,))
            row = cur.fetchone()
            return str(row["value"]) if row else None
        finally:
            conn.close()

    def _sync_in_flight(self, conn: sqlite3.Connection, tasks: Dict[str, TaskExecutionRecord]) -> None:
        """将内存中的在途任务字典全量同步写入 `in_flight_tasks` 表。"""
        conn.execute("DELETE FROM in_flight_tasks;")
        for rec in tasks.values():
            conn.execute("""
                INSERT INTO in_flight_tasks (
                    task_id, state, task_revision, session_id, candidate_commit,
                    corrections_count, waiting_events, leases, runtime_context, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                rec.task_id, rec.state, rec.task_revision, rec.session_id,
                rec.candidate_commit, rec.corrections_count,
                json.dumps(list(rec.waiting_events)), json.dumps(list(rec.leases)),
                json.dumps(dict(rec.runtime_context)), rec.updated_at,
            ))

    def _sync_leases(self, conn: sqlite3.Connection, leases: List[Lease]) -> None:
        """将当前活动租约列表同步写入 `leases` 表。"""
        conn.execute("DELETE FROM leases;")
        for l in leases:
            conn.execute("""
                INSERT INTO leases (
                    lease_id, task_id, resource, owner, acquired_at, expires_at, active
                ) VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (
                l.lease_id, l.task_id, l.resource, l.owner,
                l.acquired_at, l.expires_at, 1 if l.active else 0,
            ))

    def _sync_completed(self, conn: sqlite3.Connection, completed: List[str]) -> None:
        """将已完成任务 ID 列表幂等写入 `completed_tasks` 表。"""
        now = time.time()
        for t_id in completed:
            conn.execute(
                "INSERT OR IGNORE INTO completed_tasks (task_id, completed_at) VALUES (?, ?);",
                (t_id, now),
            )

    def save_coord_state(self, state: CoordState) -> None:
        """在单个事务中原子持久化完整的 `CoordState` 到 SQLite 权威表。"""
        conn = self._get_connection()
        now = time.time()
        now_str = datetime.datetime.now().astimezone().isoformat()
        state.last_updated = now_str
        try:
            with conn:
                conn.execute(
                    "INSERT OR REPLACE INTO coord_meta (key, value, updated_at) VALUES (?, ?, ?);",
                    ("cursor", str(state.cursor or ""), now),
                )
                conn.execute(
                    "INSERT OR REPLACE INTO coord_meta (key, value, updated_at) VALUES (?, ?, ?);",
                    ("last_updated", now_str, now),
                )
                self._sync_in_flight(conn, state.in_flight_tasks)
                self._sync_completed(conn, state.completed_tasks)
                self._sync_leases(conn, state.leases)
        finally:
            conn.close()

    def _load_in_flight(self, conn: sqlite3.Connection) -> Dict[str, TaskExecutionRecord]:
        """从 `in_flight_tasks` 表加载全部在途任务记录。"""
        tasks: Dict[str, TaskExecutionRecord] = {}
        cur = conn.execute("SELECT * FROM in_flight_tasks;")
        for row in cur.fetchall():
            rec = TaskExecutionRecord(
                task_id=row["task_id"],
                state=row["state"],
                task_revision=int(row["task_revision"]),
                session_id=row["session_id"],
                candidate_commit=row["candidate_commit"],
                corrections_count=int(row["corrections_count"]),
                waiting_events=list(json.loads(row["waiting_events"])),
                leases=list(json.loads(row["leases"])),
                runtime_context=dict(json.loads(row["runtime_context"])),
                updated_at=float(row["updated_at"]),
            )
            tasks[rec.task_id] = rec
        return tasks

    def _load_leases(self, conn: sqlite3.Connection) -> List[Lease]:
        """从 `leases` 表加载所有处于激活状态的租约记录。"""
        leases: List[Lease] = []
        cur = conn.execute("SELECT * FROM leases WHERE active = 1;")
        for row in cur.fetchall():
            l = Lease(
                lease_id=row["lease_id"],
                task_id=row["task_id"],
                resource=row["resource"],
                owner=row["owner"],
                acquired_at=float(row["acquired_at"]),
                expires_at=float(row["expires_at"]),
                active=bool(row["active"]),
            )
            leases.append(l)
        return leases

    def load_coord_state(self) -> Optional[CoordState]:
        """从 SQLite 表加载 `CoordState`；若数据库为空则返回 `None`。"""
        conn = self._get_connection()
        try:
            cursor_row = conn.execute("SELECT value FROM coord_meta WHERE key = 'cursor';").fetchone()
            updated_row = conn.execute("SELECT value FROM coord_meta WHERE key = 'last_updated';").fetchone()
            in_flight = self._load_in_flight(conn)
            cur_comp = conn.execute("SELECT task_id FROM completed_tasks ORDER BY task_id ASC;").fetchall()
            completed = [r["task_id"] for r in cur_comp]
            leases = self._load_leases(conn)
            if cursor_row is None and not in_flight and not completed and not leases:
                return None
            cursor_val = cursor_row["value"] if cursor_row and cursor_row["value"] else None
            last_updated = updated_row["value"] if updated_row else ""
            return CoordState(
                schema_version=1,
                cursor=cursor_val,
                in_flight_tasks=in_flight,
                completed_tasks=completed,
                leases=leases,
                last_updated=last_updated,
            )
        finally:
            conn.close()

    def save_role_job(self, job_meta: dict) -> None:
        """在 SQLite `role_jobs` 表中注册或替换一条角色作业记录。"""
        conn = self._get_connection()
        now = time.time()
        try:
            with conn:
                conn.execute("""
                    INSERT OR REPLACE INTO role_jobs (
                        job_id, dispatch_key, task_id, task_revision, role, phase,
                        pid, starttime, thread_id, status, returncode, job_dir,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    job_meta["job_id"], job_meta["dispatch_key"], job_meta["task_id"],
                    int(job_meta["task_revision"]), job_meta["role"], job_meta["phase"],
                    job_meta.get("pid"), job_meta.get("starttime"), job_meta.get("thread_id"),
                    job_meta.get("status", "PENDING"), job_meta.get("returncode"),
                    str(job_meta["job_dir"]), float(job_meta.get("created_at", now)), now,
                ))
        finally:
            conn.close()

    def update_role_job(self, job_id: str, updates: dict) -> None:
        """按 `job_id` 更新既有角色作业记录的指定列。"""
        conn = self._get_connection()
        now = time.time()
        clauses = ["updated_at = ?"]
        values = [now]
        for col in ("pid", "starttime", "thread_id", "status", "returncode", "job_dir"):
            if col in updates:
                clauses.append(f"{col} = ?")
                values.append(updates[col])
        values.append(job_id)
        sql = f"UPDATE role_jobs SET {', '.join(clauses)} WHERE job_id = ?;"
        try:
            with conn:
                conn.execute(sql, tuple(values))
        finally:
            conn.close()

    def get_role_job(self, job_id_or_key: str) -> Optional[dict]:
        """按 `job_id`、`dispatch_key` 或 `task_id` 查询单条角色作业记录。"""
        conn = self._get_connection()
        try:
            cur = conn.execute(
                "SELECT * FROM role_jobs WHERE job_id = ? OR dispatch_key = ? OR task_id = ? LIMIT 1;",
                (job_id_or_key, job_id_or_key, job_id_or_key),
            )
            row = cur.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def list_role_jobs(self, status: Optional[str] = None) -> List[dict]:
        """列出角色作业记录，支持按状态过滤。"""
        conn = self._get_connection()
        try:
            if status:
                cur = conn.execute("SELECT * FROM role_jobs WHERE status = ? ORDER BY created_at ASC;", (status,))
            else:
                cur = conn.execute("SELECT * FROM role_jobs ORDER BY created_at ASC;")
            return [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()

    def record_completed_task(self, task_id: str) -> None:
        """在 SQLite 权威库中记录指定任务已完成。"""
        conn = self._get_connection()
        try:
            with conn:
                conn.execute(
                    "INSERT OR IGNORE INTO completed_tasks (task_id, completed_at) VALUES (?, ?);",
                    (task_id, time.time()),
                )
        finally:
            conn.close()

    def close(self) -> None:
        """关闭状态存储并在持锁时释放进程文件锁。"""
        self.release_process_lock()
