#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEMP-06 物理台架 HIL 独立 40 轮双端温度遥测与故障注入自动化执行脚本
"""

import subprocess
import json
import time
import os
import sys

RAW_DIR = os.path.join(os.path.dirname(__file__), "raw_capture")
os.makedirs(RAW_DIR, exist_ok=True)

def run_ssh_cmd(cmd_str, timeout=5):
    full_cmd = ["ssh", "vmware", cmd_str]
    start = time.perf_counter()
    p = subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    return p.returncode, p.stdout.strip(), p.stderr.strip(), elapsed_ms

def test_samples(target, rounds=40):
    results = []
    print(f"=== Starting {rounds} rounds for target: {target} ===")
    for i in range(1, rounds + 1):
        cmd = f"~/soc-ap --port /dev/ttyUSB0 --target {target} --cmd temp --json"
        code, out, err, wall_ms = run_ssh_cmd(cmd)
        sample = {
            "round": i,
            "target": target,
            "exit_code": code,
            "wall_elapsed_ms": round(wall_ms, 2),
            "raw_output": out,
            "raw_error": err,
            "parsed": None
        }
        if code == 0 and out:
            try:
                data = json.loads(out)
                sample["parsed"] = data
            except Exception as e:
                sample["parse_error"] = str(e)
        results.append(sample)
        time.sleep(0.05)
    return results

def main():
    # 1. MC 40 rounds
    mc_results = test_samples("mc", 40)
    mc_path = os.path.join(RAW_DIR, "mc_40_samples.json")
    with open(mc_path, "w", encoding="utf-8") as f:
        json.dump(mc_results, f, indent=2, ensure_ascii=False)
    print(f"[OK] MC 40 samples saved to {mc_path}")

    # 2. TH 40 rounds
    th_results = test_samples("th", 40)
    th_path = os.path.join(RAW_DIR, "th_40_samples.json")
    with open(th_path, "w", encoding="utf-8") as f:
        json.dump(th_results, f, indent=2, ensure_ascii=False)
    print(f"[OK] TH 40 samples saved to {th_path}")

    # Summary
    for name, res in [("MC", mc_results), ("TH", th_results)]:
        success_count = sum(1 for r in res if r["exit_code"] == 0 and r["parsed"] and r["parsed"].get("status") == "SUCCESS")
        rtts = [r["parsed"]["monotonic_rtt_us"] for r in res if r["parsed"] and "monotonic_rtt_us" in r["parsed"]]
        duties = [r["parsed"]["temp_info"]["heater_duty_percent"] for r in res if r["parsed"] and "temp_info" in r["parsed"]]
        non_zero_duties = [d for d in duties if d != 0]
        
        avg_rtt = sum(rtts) / len(rtts) if rtts else 0
        min_rtt = min(rtts) if rtts else 0
        max_rtt = max(rtts) if rtts else 0
        
        print(f"\n--- {name} 统计指标 ---")
        print(f"成功率: {success_count}/{len(res)} ({success_count/len(res)*100:.1f}%)")
        print(f"RTT (us): min={min_rtt}, max={max_rtt}, avg={avg_rtt:.1f}")
        print(f"非零加热占空比次数: {len(non_zero_duties)} (红线校验: {'通过' if len(non_zero_duties) == 0 else '违规'})")

if __name__ == "__main__":
    main()
