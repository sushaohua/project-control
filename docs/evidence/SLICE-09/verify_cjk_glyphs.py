#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AISoC 专属 UI XML 与 C++ 文案相对 LVGL CJK/基础字库的 100% 字形覆盖校验脚本。"""

from __future__ import annotations

import pathlib
import re
import struct
import sys
from typing import Set


def load_bin_codepoints(bin_path: pathlib.Path) -> Set[int]:
    """解析 LVGL 二进制字体 `.bin` 的 `cmap` 表并与 `.cjk_codepoints.manifest` 求交集返回精确码位集合。"""
    data = bin_path.read_bytes()
    pos, out = 0, set()
    while pos + 8 <= len(data):
        length, tag = struct.unpack_from("<I4s", data, pos)
        if length < 8 or pos + length > len(data):
            break
        if tag == b"cmap":
            chunk = data[pos : pos + length]
            nsub = struct.unpack_from("<I", chunk, 8)[0]
            for idx in range(nsub):
                d_off, r_st, r_ln, _, n_ent, fmt = struct.unpack_from("<IIHHHH", chunk, 12 + idx * 16)
                if fmt in (0, 2):
                    out.update(range(r_st, r_st + r_ln))
                elif fmt in (1, 3):
                    out.update(r_st + struct.unpack_from("<H", chunk, d_off + j * 2)[0] for j in range(n_ent))
        pos += length
    man_path = bin_path.parent / ".cjk_codepoints.manifest"
    if man_path.is_file():
        manifest = {int(ln.strip(), 16) for ln in man_path.read_text(encoding="utf-8").splitlines() if ln.strip().startswith("0x")}
        return out & manifest
    return out


def load_c_codepoints(c_path: pathlib.Path) -> Set[int]:
    """解析编译进二进制的 `noto_sans_*.c` C 字体 `cmap` 描述并返回 Unicode 码位集合。"""
    txt = c_path.read_text(encoding="utf-8", errors="ignore")
    out: Set[int] = set()
    pat = re.compile(
        r"\.range_start\s*=\s*(\d+),\s*\.range_length\s*=\s*(\d+).*?"
        r"\.unicode_list\s*=\s*(\w+),\s*\.glyph_id_ofs_list\s*=\s*\w+,\s*\.list_length\s*=\s*(\d+)",
        re.S,
    )
    for m in pat.finditer(txt):
        r_st, r_ln, u_list = int(m.group(1)), int(m.group(2)), m.group(3)
        if u_list == "NULL":
            out.update(range(r_st, r_st + r_ln))
            continue
        um = re.search(rf"{u_list}\[\]\s*=\s*\{{([^}}]+)\}}", txt)
        if um:
            out.update(r_st + int(tok, 0) for tok in re.findall(r"0x[0-9a-fA-F]+|\d+", um.group(1)))
    return out


def extract_ui_text(file_path: pathlib.Path) -> str:
    """提取 XML 标签属性文本或 C++ 字符串字面量（剔除源码注释避免误报）。"""
    raw = file_path.read_text(encoding="utf-8")
    if file_path.suffix == ".xml":
        return re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    no_cmt = re.sub(r"/\*.*?\*/|//[^\n]*", "", raw, flags=re.S)
    return "\n".join(m.group(1) for m in re.finditer(r'"((?:\\.|[^"\\])*)"', no_cmt))


def verify_glyph_coverage(ps_root: pathlib.Path) -> int:
    """校验 AISoC 涉及的 XML 与 C++ 视图文案在已打包字库中零缺字（100% 覆盖）。"""
    fonts_dir = ps_root / "services/helixscreen/assets/fonts"
    covered = load_bin_codepoints(fonts_dir / "cjk/noto_sans_cjk_16.bin") | load_c_codepoints(
        fonts_dir / "noto_sans_16.c"
    )
    targets = [
        "services/helixscreen/ui_xml/settings_panel.xml",
        "services/helixscreen/ui_xml/about_settings_overlay.xml",
        "services/helixscreen/ui_xml/ota_local_overlay.xml",
        "services/helixscreen/src/ui/ui_settings_ota.cpp",
        "services/helixscreen/src/ui/ui_settings_about.cpp",
    ]
    missing = []
    for rel in targets:
        txt = extract_ui_text(ps_root / rel)
        for ch in sorted({c for c in txt if ord(c) > 127}):
            if ord(ch) not in covered:
                missing.append(f"{rel}: '{ch}' (U+{ord(ch):04X})")
    if missing:
        for item in missing:
            print(f"[GLYPH-MISS] {item}", file=sys.stderr)
        return 1
    print(f"[PASS] CJK_GLYPH_COVERAGE_100_PERCENT (covered_pool={len(covered)})")
    return 0


def main() -> int:
    """命令行入口：接收 `printer-soc` 根目录路径并执行字形覆盖检查。"""
    ps_root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("printer-soc")
    return verify_glyph_coverage(ps_root)


if __name__ == "__main__":
    sys.exit(main())
