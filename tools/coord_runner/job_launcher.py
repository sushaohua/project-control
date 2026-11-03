#!/usr/bin/env python3
"""Asynchronous non-blocking job launcher with PID starttime & atomic exit status (Design §6)."""

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
            pass

DEFAULT_CODEX_BIN = Path("/home/sushaohua/.local/bin/codex")
DEFAULT_MODEL = "gpt-6-luna"


def get_proc_starttime(pid: int) -> Optional[str]:
    """Read field 22 (starttime) from /proc/<pid>/stat to guard against PID reuse."""
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
    """Check if process is alive and matches the recorded starttime."""
    if pid <= 0:
        return False
    actual_start = get_proc_starttime(pid)
    if actual_start is None:
        return False
    if expected_starttime and actual_start != str(expected_starttime):
        return False
    return True


def write_atomic_json(target_path: Path, payload: dict) -> None:
    """Write dictionary payload atomically using a PID-tagged temp file and rename."""
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
    """Spawns detached asynchronous role jobs and manages their lifecycle."""

    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        codex_bin: Optional[Path] = None,
        default_model: str = DEFAULT_MODEL,
    ):
        self.workspace_root = Path(workspace_root or ".").resolve()
        self.codex_bin = Path(codex_bin or DEFAULT_CODEX_BIN)
        self.default_model = default_model
        self._active_procs = {}

    def _prepare_job_files(self, job_dir: Path, cmd: List[str], prompt: str) -> None:
        job_dir.mkdir(parents=True, exist_ok=True)
        (job_dir / "cmd.json").write_text(json.dumps(cmd, indent=2), encoding="utf-8")
        (job_dir / "prompt.txt").write_text(prompt, encoding="utf-8")

    def launch_async(self, job_dir: Path, cmd: List[str], prompt: str) -> int:
        """Launch detached worker process with start_new_session=True; return worker PID."""
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
        """Poll tracked Popen object to collect exit code and release resources."""
        proc = self._active_procs.get(pid)
        if proc is not None:
            rc = proc.poll()
            if rc is not None:
                self._active_procs.pop(pid, None)
            return rc
        return None

    def terminate_job(self, job_dir: Path) -> bool:
        """Terminate job process recorded in pid.json if currently running."""
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
    """Worker process main entrypoint: writes pid.json, runs command, drops exit_status.json."""
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
    parser = argparse.ArgumentParser(description="Detached role job worker")
    parser.add_argument("--run-job", required=True, help="Path to job directory")
    args = parser.parse_args()
    return run_worker_job(Path(args.run_job))


if __name__ == "__main__":
    sys.exit(main())
