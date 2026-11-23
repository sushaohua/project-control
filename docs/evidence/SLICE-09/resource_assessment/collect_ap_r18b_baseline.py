#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S09-RES 实板 AP 空闲 60s @ 1Hz 资源采样与存储状态采集脚本。

连接目标板（默认 root@192.168.1.101），在采样前后核对 printer-soc status 进程身份，
以 1Hz 连续采集 61 个样本点（覆盖 60 秒窗口）的 /proc/uptime、/proc/stat、/proc/meminfo
及 controller/children 各进程的 /proc/<pid>/stat 与 /proc/<pid>/status，并核算 CPU% 与内存指标。
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys


REMOTE_SAMPLER = r"""
import json, os, pathlib, subprocess, time

def get_status():
    out = subprocess.check_output(["printer-soc", "status"], text=True)
    return json.loads(out)

def read_proc_sample(pids):
    up = pathlib.Path("/proc/uptime").read_text().split()
    stat_lines = pathlib.Path("/proc/stat").read_text().splitlines()
    cpu_fields = [int(x) for x in stat_lines[0].split()[1:9]]
    mem = {}
    for line in pathlib.Path("/proc/meminfo").read_text().splitlines():
        parts = line.split()
        if parts[0].rstrip(":") in ("MemTotal", "MemFree", "MemAvailable", "Buffers", "Cached", "Shmem"):
            mem[parts[0].rstrip(":")] = int(parts[1])
    procs = {}
    for name, pid in pids.items():
        st_raw = pathlib.Path(f"/proc/{pid}/stat").read_text()
        rparen = st_raw.rfind(")")
        after = st_raw[rparen + 2:].split()
        utime, stime, starttime = int(after[11]), int(after[12]), int(after[19])
        rss_kb, hwm_kb, vmsize_kb, threads = 0, 0, 0, 0
        for sline in pathlib.Path(f"/proc/{pid}/status").read_text().splitlines():
            if sline.startswith("VmRSS:"):
                rss_kb = int(sline.split()[1])
            elif sline.startswith("VmHWM:"):
                hwm_kb = int(sline.split()[1])
            elif sline.startswith("VmSize:"):
                vmsize_kb = int(sline.split()[1])
            elif sline.startswith("Threads:"):
                threads = int(sline.split()[1])
        procs[name] = {
            "pid": pid, "utime": utime, "stime": stime, "starttime": starttime,
            "vm_rss_kib": rss_kb, "vm_hwm_kib": hwm_kb, "vm_size_kib": vmsize_kb, "threads": threads,
        }
    return {"uptime_sec": float(up[0]), "idle_sec": float(up[1]), "cpu8": cpu_fields, "mem_kib": mem, "procs": procs}

pre_status = get_status()
pids = {"controller": pre_status["controller"]["pid"]}
for k, v in pre_status["children"].items():
    pids[k] = v["pid"]
samples = []
t0 = time.monotonic()
for idx in range(61):
    target = t0 + idx * 1.0
    now = time.monotonic()
    if target > now:
        time.sleep(target - now)
    samples.append(read_proc_sample(pids))
post_status = get_status()
df_out = subprocess.check_output(["df", "-k", "/", "/data", "/run/printer-soc/firmware"], text=True)
mountinfo = pathlib.Path("/proc/self/mountinfo").read_text()
version = json.loads(pathlib.Path("/etc/printer-soc/version.json").read_text())
services_cfg = json.loads(pathlib.Path("/etc/printer-soc/services.json").read_text())
bus_addr = pre_status["bus_address"]
env = dict(os.environ, LD_LIBRARY_PATH="/usr/lib/printer-soc", DBUS_SESSION_BUS_ADDRESS=bus_addr)
ver_rpc = subprocess.check_output([
    "/usr/lib/printer-soc/bin/dbus-send", "--session", "--print-reply",
    "--dest=org.aisoc.Device", "/org/aisoc/device", "org.aisoc.DeviceInterface.GetVersionInfo"
], text=True, env=env)
port_rpc = subprocess.check_output([
    "/usr/lib/printer-soc/bin/dbus-send", "--session", "--print-reply",
    "--dest=org.aisoc.Forward", "/org/aisoc/forward", "org.aisoc.ForwardInterface.GetPortStatus"
], text=True, env=env)
print(json.dumps({
    "clk_tck": os.sysconf("SC_CLK_TCK"), "cpu_count": os.cpu_count(),
    "version": version, "services_cfg": services_cfg,
    "pre_status": pre_status, "post_status": post_status,
    "dbus_version_info_raw": ver_rpc, "dbus_port_status_raw": port_rpc,
    "df_k": df_out, "mountinfo": mountinfo, "samples": samples,
}))
"""


def verify_no_pid_churn(pre: dict, post: dict, samples: list[dict]) -> dict:
    """核对采样前后与全部样本点的进程 PID、start_ticks、exe 及存活状态是否零换代。"""
    identities = {}
    roles = [("controller", pre["controller"], post["controller"])]
    for name in sorted(pre["children"]):
        roles.append((name, pre["children"][name], post["children"][name]))
    for name, a, b in roles:
        same = (
            a["pid"] == b["pid"]
            and str(a["start_ticks"]) == str(b["start_ticks"])
            and a["exe"] == b["exe"]
        )
        alive_pre = pre["controller_alive"] if name == "controller" else pre["children_alive"][name]
        alive_post = post["controller_alive"] if name == "controller" else post["children_alive"][name]
        ticks_ok = all(str(s["procs"][name]["starttime"]) == str(a["start_ticks"]) for s in samples)
        identities[name] = {
            "pid": a["pid"],
            "start_ticks": str(a["start_ticks"]),
            "exe": a["exe"],
            "alive_pre": bool(alive_pre),
            "alive_post": bool(alive_post),
            "no_pid_churn": bool(same and alive_pre and alive_post and ticks_ok),
        }
    return identities


def compute_metrics(samples: list[dict]) -> dict:
    """按 §2.6 口径计算整机 CPU%、各服务 CPU%（均值与单秒峰值）、VmRSS 峰值与 MemAvailable 最低值。"""
    sys_1s = []
    proc_names = sorted(samples[0]["procs"].keys())
    proc_1s: dict[str, list[float]] = {k: [] for k in proc_names}
    for i in range(1, len(samples)):
        c0, c1 = samples[i - 1]["cpu8"], samples[i]["cpu8"]
        dtot = sum(c1) - sum(c0)
        didle = (c1[3] - c0[3]) + (c1[4] - c0[4])
        sys_1s.append((dtot - didle) / dtot * 100.0 if dtot > 0 else 0.0)
        for k in proc_names:
            p0, p1 = samples[i - 1]["procs"][k], samples[i]["procs"][k]
            dp = (p1["utime"] + p1["stime"]) - (p0["utime"] + p0["stime"])
            proc_1s[k].append(dp / dtot * 100.0 if dtot > 0 else 0.0)
    c_first, c_last = samples[0]["cpu8"], samples[-1]["cpu8"]
    tot_all = sum(c_last) - sum(c_first)
    idle_all = (c_last[3] - c_first[3]) + (c_last[4] - c_first[4])
    proc_summary = {}
    for k in proc_names:
        p_first, p_last = samples[0]["procs"][k], samples[-1]["procs"][k]
        dp_all = (p_last["utime"] + p_last["stime"]) - (p_first["utime"] + p_first["stime"])
        rss_series = [s["procs"][k]["vm_rss_kib"] for s in samples]
        proc_summary[k] = {
            "cpu_pct_window_avg": round(dp_all / tot_all * 100.0, 3) if tot_all > 0 else 0.0,
            "cpu_pct_1s_max": round(max(proc_1s[k]), 3),
            "vm_rss_max_kib": max(rss_series),
            "vm_rss_min_kib": min(rss_series),
            "vm_hwm_max_kib": max(s["procs"][k]["vm_hwm_kib"] for s in samples),
        }
    avail = [s["mem_kib"]["MemAvailable"] for s in samples]
    return {
        "sample_count": len(samples),
        "interval_count": len(samples) - 1,
        "uptime_start_sec": samples[0]["uptime_sec"],
        "uptime_end_sec": samples[-1]["uptime_sec"],
        "uptime_span_sec": round(samples[-1]["uptime_sec"] - samples[0]["uptime_sec"], 3),
        "system_cpu_pct_window_avg": round((tot_all - idle_all) / tot_all * 100.0, 3),
        "system_cpu_pct_1s_max": round(max(sys_1s), 3),
        "system_cpu_pct_1s_min": round(min(sys_1s), 3),
        "mem_total_kib": samples[0]["mem_kib"]["MemTotal"],
        "mem_available_min_kib": min(avail),
        "mem_available_max_kib": max(avail),
        "processes": proc_summary,
    }


def main() -> int:
    """执行远端 60s 采样并将原始样本与汇总指标写入指定输出目录。"""
    host = sys.argv[1] if len(sys.argv) > 1 else "root@192.168.1.101"
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent
    tag = sys.argv[3] if len(sys.argv) > 3 else "ap_r18b_idle_60s"
    host_start = datetime.now(timezone.utc).astimezone().isoformat(timespec="milliseconds")
    raw_out = subprocess.check_output(
        ["ssh", "-o", "ConnectTimeout=5", host, f"python3 -B -c {subprocess.list2cmdline([REMOTE_SAMPLER])}"],
        text=True,
        timeout=95,
    )
    host_end = datetime.now(timezone.utc).astimezone().isoformat(timespec="milliseconds")
    payload = json.loads(raw_out)
    identities = verify_no_pid_churn(payload["pre_status"], payload["post_status"], payload["samples"])
    metrics = compute_metrics(payload["samples"])
    bundle = {
        "tag": tag,
        "target_host": host,
        "host_wall_start": host_start,
        "host_wall_end": host_end,
        "clk_tck": payload["clk_tck"],
        "cpu_count": payload["cpu_count"],
        "version": payload["version"],
        "services_cfg": payload["services_cfg"],
        "identities": identities,
        "metrics": metrics,
        "df_k": payload["df_k"],
        "mountinfo": payload["mountinfo"],
        "dbus_version_info_raw": payload["dbus_version_info_raw"],
        "dbus_port_status_raw": payload["dbus_port_status_raw"],
        "pre_status": payload["pre_status"],
        "post_status": payload["post_status"],
        "samples": payload["samples"],
    }
    raw_path = out_dir / f"{tag}_raw.json"
    sum_path = out_dir / f"{tag}_summary.json"
    raw_path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary_only = {k: v for k, v in bundle.items() if k not in ("samples", "mountinfo")}
    sum_path.write_text(json.dumps(summary_only, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"identities": identities, "metrics": metrics}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
