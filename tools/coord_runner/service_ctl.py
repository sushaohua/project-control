#!/usr/bin/env python3
"""CLI and management tool for ai-soc-coord-runner user systemd service."""

import argparse
import getpass
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Callable, Dict, List, Optional, Tuple

SERVICE_NAME = "ai-soc-coord-runner.service"
DEFAULT_SOURCE_PATH = (
    Path(__file__).resolve().parents[2] / "config" / "coord_runner" / SERVICE_NAME
)
DEFAULT_USER_SYSTEMD_DIR = Path.home() / ".config" / "systemd" / "user"
CmdRunner = Callable[[List[str]], Tuple[int, str]]


def default_exec_cmd(cmd: List[str]) -> Tuple[int, str]:
    """Execute command safely and capture returncode with combined output."""
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
            timeout=15.0,
        )
        return proc.returncode, proc.stdout.strip()
    except (subprocess.SubprocessError, OSError) as err:
        return 1, str(err)


def run_systemctl(args: List[str], runner: Optional[CmdRunner] = None) -> Tuple[int, str]:
    """Execute systemctl --user command safely."""
    run_fn = runner or default_exec_cmd
    cmd = ["systemctl", "--user"] + args
    return run_fn(cmd)


def check_user_linger(username: Optional[str] = None) -> Dict[str, object]:
    """Check whether linger is enabled for user via linger file or loginctl."""
    user = username or os.environ.get("USER") or getpass.getuser()
    linger_file = Path(f"/var/lib/systemd/linger/{user}")
    if linger_file.is_file():
        return {"user": user, "linger_enabled": True, "method": "linger_file"}
    rc, out = default_exec_cmd(["loginctl", "show-user", user, "--property=Linger"])
    if rc == 0 and "Linger=yes" in out:
        return {"user": user, "linger_enabled": True, "method": "loginctl"}
    return {"user": user, "linger_enabled": False, "method": "none", "detail": out}


def install_service(
    src_file: Optional[Path] = None,
    dest_dir: Optional[Path] = None,
    runner: Optional[CmdRunner] = None,
) -> Dict[str, object]:
    """Install systemd user unit file and reload daemon."""
    src = Path(src_file or DEFAULT_SOURCE_PATH).resolve()
    if not src.is_file():
        return {"success": False, "error": f"Source unit file not found: {src}"}
    target_dir = Path(dest_dir or DEFAULT_USER_SYSTEMD_DIR).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / SERVICE_NAME
    shutil.copyfile(src, target_file)
    rc, out = run_systemctl(["daemon-reload"], runner)
    return {
        "success": target_file.is_file(),
        "target_file": str(target_file),
        "daemon_reload_rc": rc,
        "daemon_reload_out": out,
    }


def uninstall_service(
    dest_dir: Optional[Path] = None,
    runner: Optional[CmdRunner] = None,
) -> Dict[str, object]:
    """Stop, disable, remove user unit file, and reload daemon."""
    run_systemctl(["stop", SERVICE_NAME], runner)
    run_systemctl(["disable", SERVICE_NAME], runner)
    target_dir = Path(dest_dir or DEFAULT_USER_SYSTEMD_DIR).resolve()
    target_file = target_dir / SERVICE_NAME
    removed = False
    if target_file.is_file():
        target_file.unlink()
        removed = True
    rc, out = run_systemctl(["daemon-reload"], runner)
    return {
        "success": True,
        "removed": removed,
        "daemon_reload_rc": rc,
        "daemon_reload_out": out,
    }


def control_service(action: str, runner: Optional[CmdRunner] = None) -> Dict[str, object]:
    """Execute start, stop, or restart action for the user service."""
    if action not in {"start", "stop", "restart"}:
        return {"success": False, "error": f"Unsupported action: {action}"}
    rc, out = run_systemctl([action, SERVICE_NAME], runner)
    return {"success": rc == 0, "action": action, "returncode": rc, "output": out}


def get_service_status(
    dest_dir: Optional[Path] = None,
    runner: Optional[CmdRunner] = None,
) -> Dict[str, object]:
    """Retrieve service installation and active status."""
    target_dir = Path(dest_dir or DEFAULT_USER_SYSTEMD_DIR).resolve()
    target_file = target_dir / SERVICE_NAME
    installed = target_file.is_file()
    rc_active, out_active = run_systemctl(["is-active", SERVICE_NAME], runner)
    rc_status, out_status = run_systemctl(["status", SERVICE_NAME, "--no-pager"], runner)
    return {
        "installed": installed,
        "unit_file": str(target_file) if installed else None,
        "active": rc_active == 0 and out_active == "active",
        "active_output": out_active,
        "status_code": rc_status,
        "status_output": out_status,
    }


def verify_crontab_isolation(runner: Optional[CmdRunner] = None) -> Dict[str, object]:
    """Verify crontab is untouched and does not contain any coord_runner entry."""
    run_fn = runner or default_exec_cmd
    rc, out = run_fn(["crontab", "-l"])
    if rc != 0:
        if "no crontab for" in out.lower():
            return {"crontab_clean": True, "active_entries_count": 0, "forbidden_entries": [], "detail": out}
        return {
            "crontab_clean": False,
            "error": f"Crontab command failed with exit code {rc}: {out}",
            "active_entries_count": 0,
            "forbidden_entries": [],
        }
    lines = [line.strip() for line in out.splitlines() if line.strip() and not line.strip().startswith("#")]
    forbidden = [line for line in lines if "coord_runner" in line or "ai-soc-coord" in line]
    return {
        "crontab_clean": len(forbidden) == 0,
        "active_entries_count": len(lines),
        "forbidden_entries": forbidden,
        "raw_entries": lines,
    }


def create_cli_parser() -> argparse.ArgumentParser:
    """Build CLI parser for service control actions."""
    parser = argparse.ArgumentParser(description="Systemd user service controller for COORD runner")
    parser.add_argument(
        "action",
        choices=["install", "uninstall", "start", "stop", "restart", "status", "check_linger", "verify_crontab"],
        help="Service lifecycle action",
    )
    parser.add_argument("--src-file", default=None, help="Custom unit file source path")
    parser.add_argument("--dest-dir", default=None, help="Custom systemd user directory")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI dispatch entrypoint."""
    parser = create_cli_parser()
    args = parser.parse_args(argv)
    res: Dict[str, object] = {}
    if args.action == "install":
        res = install_service(src_file=Path(args.src_file) if args.src_file else None,
                              dest_dir=Path(args.dest_dir) if args.dest_dir else None)
    elif args.action == "uninstall":
        res = uninstall_service(dest_dir=Path(args.dest_dir) if args.dest_dir else None)
    elif args.action in {"start", "stop", "restart"}:
        res = control_service(args.action)
    elif args.action == "status":
        res = get_service_status(dest_dir=Path(args.dest_dir) if args.dest_dir else None)
    elif args.action == "check_linger":
        res = check_user_linger()
    elif args.action == "verify_crontab":
        res = verify_crontab_isolation()
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res.get("success", True) and res.get("crontab_clean", True) else 1


if __name__ == "__main__":
    sys.exit(main())
