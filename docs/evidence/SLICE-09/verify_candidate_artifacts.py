#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SLICE-09 跨仓合龙候选固件制品清单、ATSG 尾块与 UX-01 报告完整性校验脚本。"""

from __future__ import annotations

import hashlib
import json
import pathlib
import struct
import subprocess
import sys


def verify_artifacts(ws_root: pathlib.Path) -> int:
    """核验 `UX01_WALKTHROUGH_REPORT.md` 及 `candidate_mcu_artifacts/` 与当前子仓 HEAD 强一致。"""
    sys.path.insert(0, str(ws_root / "printer-soc/tools"))
    import sign_mcu_firmware

    ev = ws_root / "project-control/docs/evidence/SLICE-09"
    ux01 = ev / "ux01_r18b_walkthrough/UX01_WALKTHROUGH_REPORT.md"
    if not ux01.is_file() or ux01.stat().st_size <= 200:
        raise AssertionError("缺失有效的 UX01_WALKTHROUGH_REPORT.md")
    man = json.loads((ev / "candidate_mcu_artifacts/artifacts_manifest.json").read_text(encoding="utf-8"))
    mc_head = subprocess.check_output(["git", "-C", str(ws_root / "mcu-p3"), "rev-parse", "HEAD"], text=True).strip()
    bt_head = subprocess.check_output(["git", "-C", str(ws_root / "boot/bootloadermc"), "rev-parse", "HEAD"], text=True).strip()
    if man.get("mcu_p3_commit") != mc_head or man.get("boot_mc_commit") != bt_head:
        raise AssertionError("artifacts_manifest.json 记录的 40 位提交与当前子仓 HEAD 不一致")
    bt_live = (ws_root / "boot/bootloadermc/build/bootloader.bin").read_bytes()
    bt_arch = (ev / "candidate_mcu_artifacts/bootloader.bin").read_bytes()
    marker = b" | Build #"
    m_pos = bt_arch.find(marker)
    if len(bt_live) != len(bt_arch) or m_pos < 8:
        raise AssertionError("boot/bootloadermc/build/bootloader.bin 长度或构建标识异常")
    if bt_live[: m_pos - 8] != bt_arch[: m_pos - 8] or bt_live[m_pos:] != bt_arch[m_pos:]:
        raise AssertionError("boot/bootloadermc/build/bootloader.bin 机器码与归档候选不一致")
    short_le = struct.pack("<I", int(mc_head[:8], 16))
    for key, bid in (("fw_mc.bin", 0x43500001), ("fw_th.bin", 0x42300001), ("bootloader.bin", None), ("bootloader_3e01c00_rollback.bin", None)):
        raw = (ev / "candidate_mcu_artifacts" / key).read_bytes()
        meta = man["files"][key]
        if hashlib.sha256(raw).hexdigest() != meta["sha256"] or len(raw) != meta["size_bytes"]:
            raise AssertionError(f"{key} 字节数或 SHA-256 与清单不一致")
        if bid is not None:
            payload, trailer = sign_mcu_firmware.validate_atsg_base(raw, check_crc=True)
            if struct.unpack_from("<I", trailer, 8)[0] != bid or short_le not in payload:
                raise AssertionError(f"{key} 板型 ID 或内嵌短提交不匹配")
    if man["files"]["bootloader.bin"]["size_bytes"] > 131072:
        raise AssertionError("bootloader.bin 超出 128KB 分区上限")
    print("[PASS] SLICE-09 candidate_mcu_artifacts & UX-01 report verified")
    return 0


def main() -> int:
    """命令行入口：校验指定工作区下的 SLICE-09 候选制品与走查报告。"""
    ws = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(".")
    return verify_artifacts(ws.resolve())


if __name__ == "__main__":
    sys.exit(main())
