#!/usr/bin/env python3
"""带 `/proc/<pid>/stat` 启动时间戳防复用校验与原子退出状态落盘的异步非阻塞作业启动器。"""

import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import List, Optional

if __package__:
    from .errors import CoordRunnerError
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    try:
        from coord_runner.errors import CoordRunnerError
    except ImportError:
        class CoordRunnerError(Exception):
            """当独立脚本运行且无法导入包内异常时的回退异常基类。"""
            pass

DEFAULT_CODEX_BIN = Path("/home/sushaohua/.local/bin/codex")
DEFAULT_MODEL = "gpt-6-luna"


def get_proc_starttime(pid: int) -> Optional[str]:
    """从 `/proc/<pid>/stat` 读取第 22 字段（starttime 时钟滴答数），用于防止操作系统 PID 复用误判。"""
    stat_file = Path(f"/proc/{pid}/stat")
    if not stat_file.is_file():
        return None
    try:
        content = stat_file.read_text(encoding="utf-8")
        rparen = content.rfind(")")
        if rparen < 0:
            return None
        fields = content[rparen + 1:].strip().split()
        return fields[19] if len(fields) > 19 else None
    except (OSError, IndexError, ValueError):
        return None


def is_proc_alive(pid: int, expected_starttime: Optional[str] = None) -> bool:
    """检查指定 PID 的进程是否存活，且其内核启动时间戳与预期 starttime 完全一致。"""
    if pid <= 0:
        return False
    actual_start = get_proc_starttime(pid)
    if actual_start is None:
        return False
    if expected_starttime and actual_start != str(expected_starttime):
        return False
    return True


def write_atomic_json(target_path: Path, payload: dict) -> None:
    """使用带 PID 与纳秒时间戳后缀的临时文件加 os.replace 原子写入 JSON 字典。"""
    target = Path(target_path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = target.with_suffix(f".tmp_{os.getpid()}_{time.time_ns()}")
    data_str = json.dumps(payload, indent=2, ensure_ascii=False)
    try:
        tmp_path.write_text(data_str, encoding="utf-8")
        os.replace(tmp_path, target)
    except OSError as err:
        if tmp_path.exists():
            tmp_path.unlink()
        raise CoordRunnerError(f"Failed to atomically write {target}: {err}") from err


class JobLauncher:
    """派生与管理脱离父会话（detached）的异步角色作业子进程及其生命周期。"""

    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        codex_bin: Optional[Path] = None,
        default_model: str = DEFAULT_MODEL,
    ):
        """初始化异步作业启动器，设置工作区根路径、Codex 二进制路径与活动进程跟踪表。"""
        self.workspace_root = Path(workspace_root or ".").resolve()
        self.codex_bin = Path(codex_bin or DEFAULT_CODEX_BIN)
        self.default_model = default_model
        self._active_procs = {}

    def _prepare_job_files(self, job_dir: Path, cmd: List[str], prompt: str) -> None:
        """在作业目录内落盘待执行命令行（cmd.json）与标准输入提示词（prompt.txt）。"""
        job_dir.mkdir(parents=True, exist_ok=True)
        (job_dir / "cmd.json").write_text(json.dumps(cmd, indent=2), encoding="utf-8")
        (job_dir / "prompt.txt").write_text(prompt, encoding="utf-8")

    def launch_async(self, job_dir: Path, cmd: List[str], prompt: str) -> int:
        """以 `start_new_session=True` 启动独立会话的后台 Worker 进程并立即返回其 PID。"""
        self._prepare_job_files(job_dir, cmd, prompt)
        launcher_script = Path(__file__).resolve()
        worker_cmd = [
            sys.executable, str(launcher_script),
            "--run-job", str(job_dir.resolve()),
        ]
        proc = subprocess.Popen(
            worker_cmd,
            cwd=str(self.workspace_root),
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
        self._active_procs[proc.pid] = proc
        return proc.pid

    def poll_proc(self, pid: int) -> Optional[int]:
        """非阻塞轮询已跟踪的 Popen 子进程以回收僵尸进程并返回退出码。"""
        proc = self._active_procs.get(pid)
        if proc is not None:
            rc = proc.poll()
            if rc is not None:
                self._active_procs.pop(pid, None)
            return rc
        return None

    def terminate_job(self, job_dir: Path) -> bool:
        """若 `pid.json` 中记录的作业进程仍存活且 starttime 匹配，则向其发送 SIGTERM 终止信号。"""
        pid_file = job_dir / "pid.json"
        if not pid_file.is_file():
            return False
        try:
            info = json.loads(pid_file.read_text(encoding="utf-8"))
            pid = int(info["pid"])
            st = info.get("starttime")
            if is_proc_alive(pid, st):
                os.kill(pid, 15)
                return True
        except (OSError, ValueError, KeyError):
            pass
        return False


def _execute_child_command(cmd: List[str], prompt: str, job_dir: Path) -> int:
    """在 Worker 进程内部执行目标命令，并将标准输出与标准错误重定向至作业日志文件。"""
    events_path = job_dir / "codex_events.jsonl"
    stderr_path = job_dir / "codex.stderr"
    with events_path.open("w", encoding="utf-8") as out_f, stderr_path.open("w", encoding="utf-8") as err_f:
        try:
            proc = subprocess.run(
                cmd, input=prompt, text=True,
                stdout=out_f, stderr=err_f, check=False,
            )
            return proc.returncode
        except Exception as err:
            err_f.write(f"Worker execution exception: {err}\n")
            return 127


def run_worker_job(job_dir: Path) -> int:
    """后台 Worker 进程入口：原子写入 pid.json、执行目标命令并在退出前原子落盘 exit_status.json。"""
    my_pid = os.getpid()
    starttime = get_proc_starttime(my_pid) or ""
    pid_payload = {
        "pid": my_pid,
        "starttime": starttime,
        "started_at": datetime.datetime.now().astimezone().isoformat(),
    }
    write_atomic_json(job_dir / "pid.json", pid_payload)
    cmd = json.loads((job_dir / "cmd.json").read_text(encoding="utf-8"))
    prompt = (job_dir / "prompt.txt").read_text(encoding="utf-8")
    rc = _execute_child_command(cmd, prompt, job_dir)
    exit_payload = {
        "returncode": rc,
        "finished_at": datetime.datetime.now().astimezone().isoformat(),
    }
    write_atomic_json(job_dir / "exit_status.json", exit_payload)
    return rc


def main() -> int:
    """独立 Worker 命令行入口函数。"""
    parser = argparse.ArgumentParser(description="Detached role job worker")
    parser.add_argument("--run-job", required=True, help="Path to job directory")
    args = parser.parse_args()
    return run_worker_job(Path(args.run_job))


if __name__ == "__main__":
    sys.exit(main())
