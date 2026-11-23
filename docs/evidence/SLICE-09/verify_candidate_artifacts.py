#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SLICE-09 跨仓合龙候选固件当轮重编对账、ATSG 尾块与 UX-01 报告完整性校验脚本。"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import struct
import subprocess
import sys
from typing import Tuple


def normalize_build_stamps(data: bytes) -> bytes:
    """将自动生成构建日期时间戳（含跨日 __DATE__）与开发流水号归一化为等长占位符，保留全部机器码与常量字节。"""
    out = re.sub(rb"V(\d+\.\d+\.\d+)-[0-9A-Fa-f]{4} \d{4}", rb"V\1-XXXX 0000", data)
    out = re.sub(rb"20\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", b"2000-00-00 00:00:00", out)
    out = re.sub(
        rb"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [ \d]\d 20\d{2} \d{2}:\d{2}:\d{2}( \| Build #)",
        rb"Jan 01 2000 00:00:00\1",
        out,
    )
    return re.sub(rb"\d{2}:\d{2}:\d{2}( \| Build #)", rb"00:00:00\1", out)


def check_live_mcu_pack(
    live_path: pathlib.Path, arch_raw: bytes, bid: int, min_mtime: float
) -> Tuple[bytes, bytearray]:
    """核验当轮 `make clean && make pack` 产出的双板固件新鲜度、ATSG 尾块及与归档包机器码一致性。"""
    import sign_mcu_firmware

    if not live_path.is_file() or live_path.stat().st_mtime + 1.0 < min_mtime:
        raise AssertionError(f"当轮未重新生成固件包或时间戳过期: {live_path}")
    live_raw = live_path.read_bytes()
    live_pay, live_tr = sign_mcu_firmware.validate_atsg_base(live_raw, check_crc=True)
    arch_pay, arch_tr = sign_mcu_firmware.validate_atsg_base(arch_raw, check_crc=True)
    if struct.unpack_from("<I", live_tr, 8)[0] != bid or struct.unpack_from("<I", arch_tr, 8)[0] != bid:
        raise AssertionError(f"{live_path.name} 板型 ID 不匹配")
    if len(live_pay) != len(arch_pay) or normalize_build_stamps(live_pay) != normalize_build_stamps(arch_pay):
        raise AssertionError(f"{live_path.name} 当轮重编净荷机器码与归档候选不一致")
    return arch_pay, arch_tr


def verify_artifacts(ws_root: pathlib.Path, min_mtime: float) -> int:
    """核验 `UX01_WALKTHROUGH_REPORT.md`、当轮双板重编包及 `candidate_mcu_artifacts/` 强一致。"""
    sys.path.insert(0, str(ws_root / "printer-soc/tools"))
    ev = ws_root / "project-control/docs/evidence/SLICE-09"
    ux01 = ev / "ux01_r18b_walkthrough/UX01_WALKTHROUGH_REPORT.md"
    res_doc = ev / "resource_assessment/RESOURCE_ASSESSMENT_REPORT.md"
    if not ux01.is_file() or ux01.stat().st_size <= 200:
        raise AssertionError("缺失有效的 UX01_WALKTHROUGH_REPORT.md")
    if not res_doc.is_file() or res_doc.stat().st_size <= 200:
        raise AssertionError("缺失有效的 S09-RES RESOURCE_ASSESSMENT_REPORT.md")
    man = json.loads((ev / "candidate_mcu_artifacts/artifacts_manifest.json").read_text(encoding="utf-8"))
    mc_head = subprocess.check_output(["git", "-C", str(ws_root / "mcu-p3"), "rev-parse", "HEAD"], text=True).strip()
    bt_head = subprocess.check_output(["git", "-C", str(ws_root / "boot/bootloadermc"), "rev-parse", "HEAD"], text=True).strip()
    if man.get("mcu_p3_commit") != mc_head or man.get("boot_mc_commit") != bt_head:
        raise AssertionError("artifacts_manifest.json 记录的 40 位提交与当前子仓 HEAD 不一致")
    bt_live_p = ws_root / "boot/bootloadermc/build/bootloader.bin"
    bt_arch = (ev / "candidate_mcu_artifacts/bootloader.bin").read_bytes()
    if not bt_live_p.is_file() or bt_live_p.stat().st_mtime + 1.0 < min_mtime:
        raise AssertionError("当轮未重新编译 boot/bootloadermc/build/bootloader.bin")
    if normalize_build_stamps(bt_live_p.read_bytes()) != normalize_build_stamps(bt_arch):
        raise AssertionError("boot/bootloadermc/build/bootloader.bin 机器码与归档候选不一致")
    short_le = struct.pack("<I", int(mc_head[:8], 16))
    live_map = {
        "fw_mc.bin": (ws_root / "mcu-p3/motion-controller-mcu/build/fw_mc.bin", 0x43500001),
        "fw_th.bin": (ws_root / "mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin", 0x42300001),
    }
    for key in ("fw_mc.bin", "fw_th.bin", "bootloader.bin", "bootloader_3e01c00_rollback.bin"):
        raw = (ev / "candidate_mcu_artifacts" / key).read_bytes()
        meta = man["files"][key]
        if hashlib.sha256(raw).hexdigest() != meta["sha256"] or len(raw) != meta["size_bytes"]:
            raise AssertionError(f"{key} 字节数或 SHA-256 与清单不一致")
        if key in live_map:
            arch_pay, _ = check_live_mcu_pack(live_map[key][0], raw, live_map[key][1], min_mtime)
            if short_le not in arch_pay:
                raise AssertionError(f"{key} 未内嵌当前 mcu-p3 短提交")
    if man["files"]["bootloader.bin"]["size_bytes"] > 131072:
        raise AssertionError("bootloader.bin 超出 128KB 分区上限")
    print("[PASS] SLICE-09 live clean-pack reconciliation & candidate_mcu_artifacts verified")
    return 0


def main() -> int:
    """命令行入口：接收工作区根路径与合龙起始秒级时间戳并执行对账。"""
    ws = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path(".").resolve()
    min_mtime = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    return verify_artifacts(ws, min_mtime)


if __name__ == "__main__":
    sys.exit(main())
