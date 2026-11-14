#!/usr/bin/env python3
"""ai-soc-coord-runner 用户级 systemd 服务管理与 crontab 隔离核验工具。"""

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
    """带 15s 超时保护地执行外部命令并返回 (退出码, 合并后的标准输出字符串)。"""
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
    """安全调用 `systemctl --user` 子命令并返回执行结果元组。"""
    run_fn = runner or default_exec_cmd
    cmd = ["systemctl", "--user"] + args
    return run_fn(cmd)


def check_user_linger(username: Optional[str] = None) -> Dict[str, object]:
    """通过 `/var/lib/systemd/linger/` 或 `loginctl` 检查当前用户是否已开启 systemd 驻留（linger）。"""
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
    """将 systemd 用户单元文件安装到目标目录并执行 `daemon-reload`。"""
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
    """停止、禁用并移除用户级 systemd 单元文件，随后重载 systemd 守护进程。"""
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
    """对用户级 systemd 服务执行 start、stop 或 restart 控制动作。"""
    if action not in {"start", "stop", "restart"}:
        return {"success": False, "error": f"Unsupported action: {action}"}
    rc, out = run_systemctl([action, SERVICE_NAME], runner)
    return {"success": rc == 0, "action": action, "returncode": rc, "output": out}


def get_service_status(
    dest_dir: Optional[Path] = None,
    runner: Optional[CmdRunner] = None,
) -> Dict[str, object]:
    """查询用户级 systemd 服务的安装状态、活跃状态（is-active）与详细输出。"""
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
    """核验用户 crontab 未被污染且不包含任何 coord_runner 定时任务项。"""
    run_fn = runner or default_exec_cmd
    rc, out = run_fn(["crontab", "-l"])
    if rc != 0:
        lower_out = out.lower()
        if any(pattern in lower_out for pattern in ["no crontab for", "no such file", "not found"]):
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
    """构建 systemd 服务控制器的命令行参数解析器。"""
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
    """systemd 服务管理命令行主入口。"""
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
