#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HIL Physical Joint Test & Evidence Collector for ISSUE-20261102-05
Executes:
1. Normal baseline links:
   - MC GET_VERSION (Single-hop)
   - TH GET_VERSION (Dual-hop cascade)
   - MC PING/PONG (Single-hop)
   - TH PING/PONG (Dual-hop cascade)
2. Negative acknowledge contract alignment links:
   - MC UNIMPLEMENTED_CMD (cmd_id=0x7E) -> 17B CMD_NACK (0x06, len=3, err=0x04)
   - TH UNIMPLEMENTED_CMD (cmd_id=0x7E, cascaded) -> 17B CMD_NACK (0x06, len=3, err=0x04)
3. AP host program (soc-ap) validation:
   - Normal version / ping queries
   - NACK handling and structured error reporting
"""

import datetime
import json
import os
import pty
import select
import struct
import subprocess
import sys
import time
from typing import Dict, Any, Tuple, Optional
import serial

def calc_crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= (byte & 0xFF) << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc & 0xFFFF

def now_ts():
    return datetime.datetime.now(datetime.timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def build_frame(src: int, dst: int, flags: int, cmd: int, hop: int, route: int, seq: int, payload: bytes = b"") -> bytes:
    plen = len(payload)
    hdr = bytearray([
        0x55, 0xAA,
        src, dst,
        flags, cmd,
        hop, route,
        seq & 0xFF, (seq >> 8) & 0xFF,
        plen & 0xFF, (plen >> 8) & 0xFF,
    ])
    body = hdr + payload
    crc = calc_crc16(body)
    return bytes(body + bytearray([crc & 0xFF, (crc >> 8) & 0xFF]))

def parse_frame(raw: bytes) -> Dict[str, Any]:
    if len(raw) < 14:
        return {"valid": False, "error": "frame too short"}
    sof1, sof2 = raw[0], raw[1]
    if sof1 != 0x55 or sof2 != 0xAA:
        return {"valid": False, "error": "invalid SOF"}
    src = raw[2]
    dst = raw[3]
    flags = raw[4]
    cmd = raw[5]
    hop = raw[6]
    route = raw[7]
    seq = raw[8] | (raw[9] << 8)
    plen = raw[10] | (raw[11] << 8)
    total_len = 12 + plen + 2
    if len(raw) < total_len:
        return {"valid": False, "error": f"incomplete frame (expected {total_len}, got {len(raw)})"}
    payload = raw[12:12+plen]
    recv_crc = raw[12+plen] | (raw[13+plen] << 8)
    calc_c = calc_crc16(raw[:12+plen])
    return {
        "valid": True,
        "raw_hex": raw[:total_len].hex().upper(),
        "total_len": total_len,
        "src": src,
        "dst": dst,
        "flags": flags,
        "cmd": cmd,
        "hop": hop,
        "route": route,
        "seq": seq,
        "payload_len": plen,
        "payload": payload,
        "payload_hex": payload.hex().upper(),
        "crc_recv": f"0x{recv_crc:04X}",
        "crc_calc": f"0x{calc_c:04X}",
        "crc_valid": (recv_crc == calc_c),
    }

def run_physical_hil_suite(port: str = "/dev/ttyUSB0", baud: int = 115200) -> Dict[str, Any]:
    ser = serial.Serial(port, baud, timeout=0.5)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    time.sleep(0.05)

    results = {
        "timestamp": now_ts(),
        "port": port,
        "baud": baud,
        "test_cases": []
    }

    # Case 1: MC GET_VERSION (Single-hop)
    t0 = time.monotonic()
    req_mc_ver = build_frame(1, 2, 0x05, 0x01, 4, 0, 0x0001)
    t_tx = now_ts()
    ser.write(req_mc_ver)
    rx_bytes = ser.read(30)
    rtt_us = int((time.monotonic() - t0) * 1e6)
    t_rx = now_ts()
    p_rx = parse_frame(rx_bytes)
    c1 = {
        "id": "HIL-POS-01",
        "name": "MC Single-Hop GET_VERSION",
        "target": "MC",
        "tx_time": t_tx,
        "rx_time": t_rx,
        "rtt_us": rtt_us,
        "tx_hex": req_mc_ver.hex().upper(),
        "rx_hex": rx_bytes.hex().upper(),
        "parsed": p_rx,
        "pass": p_rx.get("valid") and p_rx.get("cmd") == 0x02 and p_rx.get("crc_valid")
    }
    if p_rx.get("valid") and p_rx.get("payload_len") >= 16:
        pl = p_rx["payload"]
        c1["version_info"] = {
            "proto_ver": f"{pl[0]}.{pl[1]}",
            "firmware_ver": f"{pl[2]}.{pl[3]}",
            "boot_id": f"0x{struct.unpack('<I', pl[4:8])[0]:08X}",
            "git_commit": f"0x{struct.unpack('<I', pl[8:12])[0]:08X}",
            "capabilities": f"0x{struct.unpack('<I', pl[12:16])[0]:08X}",
        }
    results["test_cases"].append(c1)
    time.sleep(0.05)

    # Case 2: TH GET_VERSION (Dual-hop cascade)
    t0 = time.monotonic()
    req_th_ver = build_frame(1, 3, 0x05, 0x01, 4, 0, 0x0002)
    t_tx = now_ts()
    ser.write(req_th_ver)
    rx_bytes = ser.read(30)
    rtt_us = int((time.monotonic() - t0) * 1e6)
    t_rx = now_ts()
    p_rx = parse_frame(rx_bytes)
    c2 = {
        "id": "HIL-POS-02",
        "name": "TH Dual-Hop Cascaded GET_VERSION",
        "target": "TH",
        "tx_time": t_tx,
        "rx_time": t_rx,
        "rtt_us": rtt_us,
        "tx_hex": req_th_ver.hex().upper(),
        "rx_hex": rx_bytes.hex().upper(),
        "parsed": p_rx,
        "pass": p_rx.get("valid") and p_rx.get("cmd") == 0x02 and p_rx.get("crc_valid")
    }
    if p_rx.get("valid") and p_rx.get("payload_len") >= 16:
        pl = p_rx["payload"]
        c2["version_info"] = {
            "proto_ver": f"{pl[0]}.{pl[1]}",
            "firmware_ver": f"{pl[2]}.{pl[3]}",
            "boot_id": f"0x{struct.unpack('<I', pl[4:8])[0]:08X}",
            "git_commit": f"0x{struct.unpack('<I', pl[8:12])[0]:08X}",
            "capabilities": f"0x{struct.unpack('<I', pl[12:16])[0]:08X}",
        }
    results["test_cases"].append(c2)
    time.sleep(0.05)

    # Case 3: MC PING (Single-hop)
    t0 = time.monotonic()
    cookie_mc = struct.pack("<I", 1000)
    req_mc_ping = build_frame(1, 2, 0x05, 0x03, 4, 0, 0x0003, payload=cookie_mc)
    t_tx = now_ts()
    ser.write(req_mc_ping)
    rx_bytes = ser.read(26)
    rtt_us = int((time.monotonic() - t0) * 1e6)
    t_rx = now_ts()
    p_rx = parse_frame(rx_bytes)
    c3 = {
        "id": "HIL-POS-03",
        "name": "MC Single-Hop PING",
        "target": "MC",
        "tx_time": t_tx,
        "rx_time": t_rx,
        "rtt_us": rtt_us,
        "tx_hex": req_mc_ping.hex().upper(),
        "rx_hex": rx_bytes.hex().upper(),
        "parsed": p_rx,
        "pass": p_rx.get("valid") and p_rx.get("cmd") == 0x04 and p_rx.get("crc_valid")
    }
    if p_rx.get("valid") and p_rx.get("payload_len") >= 12:
        pl = p_rx["payload"]
        c3["ping_info"] = {
            "t_originate_ms": struct.unpack("<I", pl[0:4])[0],
            "t_receive_ms": struct.unpack("<I", pl[4:8])[0],
            "planner_buf_free": struct.unpack("<H", pl[8:10])[0],
            "rx_fifo_free_units": pl[10],
        }
    results["test_cases"].append(c3)
    time.sleep(0.05)

    # Case 4: TH PING (Dual-hop cascade)
    t0 = time.monotonic()
    cookie_th = struct.pack("<I", 0x12345678)
    req_th_ping = build_frame(1, 3, 0x05, 0x03, 4, 0, 0x0004, payload=cookie_th)
    t_tx = now_ts()
    ser.write(req_th_ping)
    rx_bytes = ser.read(26)
    rtt_us = int((time.monotonic() - t0) * 1e6)
    t_rx = now_ts()
    p_rx = parse_frame(rx_bytes)
    c4 = {
        "id": "HIL-POS-04",
        "name": "TH Dual-Hop Cascaded PING",
        "target": "TH",
        "tx_time": t_tx,
        "rx_time": t_rx,
        "rtt_us": rtt_us,
        "tx_hex": req_th_ping.hex().upper(),
        "rx_hex": rx_bytes.hex().upper(),
        "parsed": p_rx,
        "pass": p_rx.get("valid") and p_rx.get("cmd") == 0x04 and p_rx.get("crc_valid")
    }
    if p_rx.get("valid") and p_rx.get("payload_len") >= 12:
        pl = p_rx["payload"]
        c4["ping_info"] = {
            "t_originate_ms": struct.unpack("<I", pl[0:4])[0],
            "t_receive_ms": struct.unpack("<I", pl[4:8])[0],
            "planner_buf_free": struct.unpack("<H", pl[8:10])[0],
            "rx_fifo_free_units": pl[10],
        }
    results["test_cases"].append(c4)
    time.sleep(0.05)

    # Case 5: MC UNIMPLEMENTED_CMD (cmd_id=0x7E) -> Standard 17-byte CMD_NACK (0x06)
    t0 = time.monotonic()
    seq_mc_nack = 0x002A  # 42
    req_mc_nack = build_frame(1, 2, 0x05, 0x7E, 4, 0, seq_mc_nack)
    t_tx = now_ts()
    ser.write(req_mc_nack)
    rx_bytes = ser.read(17)
    rtt_us = int((time.monotonic() - t0) * 1e6)
    t_rx = now_ts()
    p_rx = parse_frame(rx_bytes)
    pass_mc_nack = (
        p_rx.get("valid") and
        p_rx.get("total_len") == 17 and
        p_rx.get("cmd") == 0x06 and
        p_rx.get("payload_len") == 3 and
        p_rx.get("crc_valid") and
        len(p_rx.get("payload", b"")) == 3 and
        p_rx["payload"][0] == 0x04 and
        (p_rx["payload"][1] | (p_rx["payload"][2] << 8)) == seq_mc_nack
    )
    c5 = {
        "id": "HIL-NEG-01",
        "name": "MC Physical CMD_NACK Contract Alignment (cmd_id=0x7E)",
        "target": "MC",
        "tx_time": t_tx,
        "rx_time": t_rx,
        "rtt_us": rtt_us,
        "tx_hex": req_mc_nack.hex().upper(),
        "rx_hex": rx_bytes.hex().upper(),
        "parsed": p_rx,
        "pass": pass_mc_nack,
    }
    if p_rx.get("valid") and len(p_rx.get("payload", b"")) == 3:
        pl = p_rx["payload"]
        c5["nack_info"] = {
            "error_code": f"0x{pl[0]:02X}",
            "expected_seq": pl[1] | (pl[2] << 8),
            "seq_matched": (pl[1] | (pl[2] << 8)) == seq_mc_nack,
        }
    results["test_cases"].append(c5)
    time.sleep(0.05)

    # Case 6: TH UNIMPLEMENTED_CMD (cmd_id=0x7E, cascaded) -> Standard 17-byte CMD_NACK (0x06)
    t0 = time.monotonic()
    seq_th_nack = 0x003B  # 59
    req_th_nack = build_frame(1, 3, 0x05, 0x7E, 4, 0, seq_th_nack)
    t_tx = now_ts()
    ser.write(req_th_nack)
    rx_bytes = ser.read(17)
    rtt_us = int((time.monotonic() - t0) * 1e6)
    t_rx = now_ts()
    p_rx = parse_frame(rx_bytes)
    pass_th_nack = (
        p_rx.get("valid") and
        p_rx.get("total_len") == 17 and
        p_rx.get("cmd") == 0x06 and
        p_rx.get("payload_len") == 3 and
        p_rx.get("crc_valid") and
        len(p_rx.get("payload", b"")) == 3 and
        p_rx["payload"][0] == 0x04 and
        (p_rx["payload"][1] | (p_rx["payload"][2] << 8)) == seq_th_nack
    )
    c6 = {
        "id": "HIL-NEG-02",
        "name": "TH Dual-Hop Cascaded Physical CMD_NACK (cmd_id=0x7E)",
        "target": "TH",
        "tx_time": t_tx,
        "rx_time": t_rx,
        "rtt_us": rtt_us,
        "tx_hex": req_th_nack.hex().upper(),
        "rx_hex": rx_bytes.hex().upper(),
        "parsed": p_rx,
        "pass": pass_th_nack,
    }
    if p_rx.get("valid") and len(p_rx.get("payload", b"")) == 3:
        pl = p_rx["payload"]
        c6["nack_info"] = {
            "error_code": f"0x{pl[0]:02X}",
            "expected_seq": pl[1] | (pl[2] << 8),
            "seq_matched": (pl[1] | (pl[2] << 8)) == seq_th_nack,
        }
    results["test_cases"].append(c6)

    ser.close()
    return results

def run_soc_ap_e2e_tests(soc_ap_bin: str = "/home/sushaohua/soc-ap", port: str = "/dev/ttyUSB0") -> Dict[str, Any]:
    suite = {
        "soc_ap_bin": soc_ap_bin,
        "port": port,
        "cases": []
    }

    # 1. Normal soc-ap MC version query
    res = subprocess.run([soc_ap_bin, "--port", port, "--target", "mc", "--cmd", "version", "--json"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    suite["cases"].append({
        "id": "AP-E2E-POS-01",
        "cmd": f"{soc_ap_bin} --port {port} --target mc --cmd version --json",
        "exit_code": res.returncode,
        "pass": res.returncode == 0 and "SUCCESS" in res.stdout,
        "stdout": res.stdout.strip(),
        "stderr": res.stderr.strip()
    })

    # 2. Normal soc-ap TH version query
    res = subprocess.run([soc_ap_bin, "--port", port, "--target", "th", "--cmd", "version", "--json"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    suite["cases"].append({
        "id": "AP-E2E-POS-02",
        "cmd": f"{soc_ap_bin} --port {port} --target th --cmd version --json",
        "exit_code": res.returncode,
        "pass": res.returncode == 0 and "SUCCESS" in res.stdout,
        "stdout": res.stdout.strip(),
        "stderr": res.stderr.strip()
    })

    # 3. Normal soc-ap MC ping query
    res = subprocess.run([soc_ap_bin, "--port", port, "--target", "mc", "--cmd", "ping", "--json"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    suite["cases"].append({
        "id": "AP-E2E-POS-03",
        "cmd": f"{soc_ap_bin} --port {port} --target mc --cmd ping --json",
        "exit_code": res.returncode,
        "pass": res.returncode == 0 and "SUCCESS" in res.stdout,
        "stdout": res.stdout.strip(),
        "stderr": res.stderr.strip()
    })

    # 4. Normal soc-ap TH ping query
    res = subprocess.run([soc_ap_bin, "--port", port, "--target", "th", "--cmd", "ping", "--json"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    suite["cases"].append({
        "id": "AP-E2E-POS-04",
        "cmd": f"{soc_ap_bin} --port {port} --target th --cmd ping --json",
        "exit_code": res.returncode,
        "pass": res.returncode == 0 and "SUCCESS" in res.stdout,
        "stdout": res.stdout.strip(),
        "stderr": res.stderr.strip()
    })

    # Helper for transparent hardware proxy NACK injection
    def run_hardware_tamper_case(cid: str, target: str, is_json: bool = False):
        phys = serial.Serial(port, 115200, timeout=0.01)
        phys.reset_input_buffer()
        master_fd, slave_fd = pty.openpty()
        slave_name = os.ttyname(slave_fd)
        args = [soc_ap_bin, "--port", slave_name, "--target", target, "--cmd", "version", "--timeout-ms", "1000"]
        if is_json:
            args.append("--json")
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pfd = phys.fileno()
        deadline = time.monotonic() + 2.0
        while time.monotonic() < deadline:
            if proc.poll() is not None:
                break
            r, _, _ = select.select([master_fd, pfd], [], [], 0.05)
            if master_fd in r:
                data = os.read(master_fd, 1024)
                if len(data) >= 14 and data[0] == 0x55 and data[1] == 0xAA:
                    tampered = bytearray(data)
                    tampered[5] = 0x7E # Tamper cmd_id to unimplemented 0x7E
                    c = calc_crc16(tampered[:12])
                    tampered[12] = c & 0xFF
                    tampered[13] = (c >> 8) & 0xFF
                    phys.write(tampered)
            if pfd in r:
                resp = phys.read(phys.in_waiting or 1)
                if resp:
                    os.write(master_fd, resp)
        os.close(slave_fd)
        stdout, stderr = proc.communicate(timeout=1.0)
        os.close(master_fd)
        phys.close()
        expected_msg = "Received CMD_NACK from target"
        passed = (proc.returncode == 2) and (expected_msg in stdout or expected_msg in stderr)
        suite["cases"].append({
            "id": cid,
            "cmd": " ".join(args),
            "exit_code": proc.returncode,
            "pass": passed,
            "stdout": stdout.strip(),
            "stderr": stderr.strip()
        })

    # 5. MC NACK text mode
    run_hardware_tamper_case("AP-E2E-NEG-01", "mc", is_json=False)
    # 6. MC NACK json mode
    run_hardware_tamper_case("AP-E2E-NEG-02", "mc", is_json=True)
    # 7. TH NACK text mode
    run_hardware_tamper_case("AP-E2E-NEG-03", "th", is_json=False)
    # 8. TH NACK json mode
    run_hardware_tamper_case("AP-E2E-NEG-04", "th", is_json=True)

    return suite

if __name__ == "__main__":
    hil_data = run_physical_hil_suite()
    ap_data = run_soc_ap_e2e_tests()
    combined = {
        "hil_tests": hil_data,
        "ap_e2e_tests": ap_data
    }
    print(json.dumps(combined, indent=2, ensure_ascii=False, default=lambda o: o.hex().upper() if isinstance(o, (bytes, bytearray)) else str(o)))
