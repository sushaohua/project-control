#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S09-RES 四端 MCU/Bootloader 静态容量提取、ATSG 净载核验与归档制品对账脚本。

对隔离构建产出的 7 份 ELF/map/bin 执行 arm-none-eabi-size -A、objdump -h、readelf -lW
及 map 关键摘录，核算 Flash 实际 LMA 跨度与各 RAM bank 占用，并与 SLICE-08/SLICE-09 归档包对账。
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys


def sha256_and_size(path: Path) -> dict:
    """计算指定文件的精确字节数与 SHA-256 摘要。"""
    raw = path.read_bytes()
    return {"path": str(path), "size_bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def normalize_stamps(data: bytes) -> bytes:
    """归一化固件内嵌构建日期时间戳（含跨日 __DATE__）与开发流水号以便核对纯机器码一致性。"""
    out = re.sub(rb"V(\d+\.\d+\.\d+)-[0-9A-Fa-f]{4} \d{4}", rb"V\1-XXXX 0000", data)
    out = re.sub(rb"20\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", b"2000-00-00 00:00:00", out)
    out = re.sub(
        rb"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [ \d]\d 20\d{2} \d{2}:\d{2}:\d{2}( \| Build #)",
        rb"Jan 01 2000 00:00:00\1",
        out,
    )
    return re.sub(rb"\d{2}:\d{2}:\d{2}( \| Build #)", rb"00:00:00\1", out)


def extract_map_snippet(map_path: Path) -> str:
    """提取 GNU ld map 文件的 Memory Configuration 表、主要段头及堆栈预留块。"""
    lines = map_path.read_text(encoding="utf-8", errors="replace").splitlines()
    keep = []
    for idx, line in enumerate(lines):
        if line.startswith("Memory Configuration"):
            keep.extend(lines[idx: idx + 12])
        elif line.startswith("._user_heap_stack"):
            keep.extend(lines[idx: idx + 10])
        elif re.match(r"^(\.(isr_vector|text|rodata|ARM|preinit_array|init_array|fini_array|data|bss|noinit|boot_ipc))\b", line):
            keep.extend(lines[idx: idx + 2])
        elif re.search(r"\b(_estack|_Min_Heap_Size|_Min_Stack_Size|_sdata|_edata|_sbss|_ebss)\s*=", line):
            keep.append(line)
    return "\n".join(keep)


def analyze_elf_flash(elf_path: Path, flash_origin: int, flash_limit: int) -> dict:
    """解析 readelf -lW 中归属 Flash 区的 LOAD 段，计算首址至最高有效 LMA 末址跨度。"""
    out = subprocess.check_output(["arm-none-eabi-readelf", "-lW", str(elf_path)], text=True)
    max_lma_end = flash_origin
    segments = []
    for line in out.splitlines():
        s = line.strip()
        if not s.startswith("LOAD"):
            continue
        parts = s.split()
        vaddr, paddr, filesz, memsz = (int(parts[2], 16), int(parts[3], 16), int(parts[4], 16), int(parts[5], 16))
        segments.append({"vaddr": hex(vaddr), "paddr": hex(paddr), "filesz": filesz, "memsz": memsz})
        if flash_origin <= paddr < flash_origin + flash_limit and filesz > 0:
            max_lma_end = max(max_lma_end, paddr + filesz)
    span = max_lma_end - flash_origin
    return {
        "flash_origin": hex(flash_origin),
        "flash_limit_bytes": flash_limit,
        "max_flash_lma_end": hex(max_lma_end),
        "flash_span_bytes": span,
        "flash_headroom_bytes": flash_limit - span,
        "load_segments": segments,
    }


def reconcile_atsg_or_raw(built_bin: Path, archived_bin: Path, is_atsg: bool) -> dict:
    """用 validate_atsg_base 或原始二进制比对隔离重编产物与正式归档包。"""
    import sign_mcu_firmware

    b_raw = built_bin.read_bytes()
    a_raw = archived_bin.read_bytes()
    if is_atsg:
        b_pay, b_tr = sign_mcu_firmware.validate_atsg_base(b_raw, check_crc=True)
        a_pay, a_tr = sign_mcu_firmware.validate_atsg_base(a_raw, check_crc=True)
        board_id = hex(struct.unpack_from("<I", a_tr, 8)[0])
        diff_raw = sum(1 for x, y in zip(b_pay, a_pay) if x != y) if len(b_pay) == len(a_pay) else -1
        code_equal = len(b_pay) == len(a_pay) and normalize_stamps(b_pay) == normalize_stamps(a_pay)
        return {
            "archived": sha256_and_size(archived_bin),
            "board_id": board_id,
            "payload_bytes": len(a_pay),
            "built_payload_bytes": len(b_pay),
            "raw_payload_diff_bytes": diff_raw,
            "normalized_machine_code_identical": code_equal,
        }
    diff_raw = sum(1 for x, y in zip(b_raw, a_raw) if x != y) if len(b_raw) == len(a_raw) else -1
    return {
        "archived": sha256_and_size(archived_bin),
        "payload_bytes": len(a_raw),
        "built_payload_bytes": len(b_raw),
        "raw_payload_diff_bytes": diff_raw,
        "normalized_machine_code_identical": len(b_raw) == len(a_raw) and normalize_stamps(b_raw) == normalize_stamps(a_raw),
    }


def dump_one_target(label: str, elf: Path, map_p: Path, log_chunks: list[str]) -> str:
    """运行 arm-none-eabi-size -A / objdump -h / readelf -lW 并汇总到日志缓冲。"""
    sz_a = subprocess.check_output(["arm-none-eabi-size", "-A", str(elf)], text=True)
    sz_b = subprocess.check_output(["arm-none-eabi-size", "-B", str(elf)], text=True)
    obj_h = subprocess.check_output(["arm-none-eabi-objdump", "-h", str(elf)], text=True)
    rel_l = subprocess.check_output(["arm-none-eabi-readelf", "-lW", str(elf)], text=True)
    m_snip = extract_map_snippet(map_p)
    block = (
        f"{'=' * 80}\n### TARGET: {label}\nELF: {elf}\nMAP: {map_p}\n"
        f"--- arm-none-eabi-size -B ---\n{sz_b}\n--- arm-none-eabi-size -A ---\n{sz_a}\n"
        f"--- arm-none-eabi-objdump -h ---\n{obj_h}\n--- arm-none-eabi-readelf -lW ---\n{rel_l}\n"
        f"--- .map Extract ---\n{m_snip}\n"
    )
    log_chunks.append(block)
    return sz_b.splitlines()[1]


def main() -> int:
    """汇总四端静态容量与 SLICE-08/09 制品摘要并写出证据日志与 JSON。"""
    ws = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(".").resolve()
    sys.path.insert(0, str(ws / "printer-soc/tools"))
    ev8 = ws / "project-control/docs/evidence/SLICE-08"
    ev9 = ws / "project-control/docs/evidence/SLICE-09"
    out_dir = ev9 / "resource_assessment"
    tb = out_dir / ".tmp_baseline_build"
    specs = [
        ("mc_app_r18b", tb / "mcu_r18b/motion-controller-mcu/build/Marlin_AT32.elf", tb / "mcu_r18b/motion-controller-mcu/build/template.map", tb / "mcu_r18b/motion-controller-mcu/build/fw_mc.bin", ev8 / "fw_mc_r18.bin", 0x08020000, 896 * 1024, True),
        ("mc_app_s09", tb / "mcu_s09/motion-controller-mcu/build/Marlin_AT32.elf", tb / "mcu_s09/motion-controller-mcu/build/template.map", tb / "mcu_s09/motion-controller-mcu/build/fw_mc.bin", ev9 / "candidate_mcu_artifacts/fw_mc.bin", 0x08020000, 896 * 1024, True),
        ("th_app_r18b", tb / "mcu_r18b/color-engine-mcu/io_toggle/build/fw_th.elf", tb / "mcu_r18b/color-engine-mcu/io_toggle/build/fw_th.map", tb / "mcu_r18b/color-engine-mcu/io_toggle/build/fw_th.bin", ev8 / "fw_th_r18.bin", 0x08004000, 236 * 1024, True),
        ("th_app_s09", tb / "mcu_s09/color-engine-mcu/io_toggle/build/fw_th.elf", tb / "mcu_s09/color-engine-mcu/io_toggle/build/fw_th.map", tb / "mcu_s09/color-engine-mcu/io_toggle/build/fw_th.bin", ev9 / "candidate_mcu_artifacts/fw_th.bin", 0x08004000, 236 * 1024, True),
        ("mc_boot_r18b", tb / "bootmc_r18b/build/bootloader.elf", tb / "bootmc_r18b/build/bootloader.map", tb / "bootmc_r18b/build/bootloader.bin", ev9 / "candidate_mcu_artifacts/bootloader_3e01c00_rollback.bin", 0x08000000, 128 * 1024, False),
        ("mc_boot_s09", tb / "bootmc_s09/build/bootloader.elf", tb / "bootmc_s09/build/bootloader.map", tb / "bootmc_s09/build/bootloader.bin", ev9 / "candidate_mcu_artifacts/bootloader.bin", 0x08000000, 128 * 1024, False),
        ("th_boot_shared", tb / "bootth_shared/build/bootloaderth.elf", tb / "bootth_shared/build/bootloaderth.map", tb / "bootth_shared/build/bootloaderth.bin", tb / "bootth_shared/build/bootloaderth.bin", 0x08000000, 16 * 1024, False),
    ]
    logs: list[str] = []
    targets = {}
    for name, elf, mp, bbin, abin, forig, flim, is_atsg in specs:
        berkeley = dump_one_target(name, elf, mp, logs)
        b_nums = [int(x) for x in berkeley.split()[:3]]
        targets[name] = {
            "berkeley_size": {"text": b_nums[0], "data": b_nums[1], "bss": b_nums[2]},
            "flash": analyze_elf_flash(elf, forig, flim),
            "reconcile": reconcile_atsg_or_raw(bbin, abin, is_atsg),
        }
    ap_r18b_art = ev8 / "run_20261121_155747_r18b/docker_qa/artifacts"
    ap_artifacts = {
        "r18b_rootfs_tar_gz": sha256_and_size(ap_r18b_art / "printer-soc-rootfs.tar.gz"),
        "r18b_rootfs_ubi": sha256_and_size(ap_r18b_art / "rootfs.ubi"),
        "r18b_aml_upgrade_img": sha256_and_size(ap_r18b_art / "aml_upgrade_package.img"),
    }
    (out_dir / "mcu_elf_and_map_extracts.log").write_text("\n".join(logs), encoding="utf-8")
    summary = {"toolchain": subprocess.check_output(["arm-none-eabi-gcc", "--version"], text=True).splitlines()[0], "ap_r18b_artifacts": ap_artifacts, "mcu_targets": targets}
    (out_dir / "static_and_storage_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
