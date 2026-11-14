#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MiniMCProto v2.0 机器单一契约真源生成与跨五端对齐校验器。

读取 `project-control/contracts/minimc_v2_contract.yaml`，对五端 C/C++ 头文件常量、
正反向命令码唯一性、`>=520B` 升级载荷容量及黄金帧 CRC-16/CCITT-FALSE 进行毫秒级校验，
并支持一键渲染标准 C/C++ 参考头文件。
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Dict, List, Optional, Tuple

import yaml

DEFINE_RE = re.compile(r"^\s*#define\s+(?P<name>[A-Z0-9_]+)\s+\(*\s*(?P<val>0x[0-9A-Fa-f]+|\d+)[UuLl]*\s*\)*", re.MULTILINE)
CONSTEXPR_RE = re.compile(r"constexpr\s+[A-Za-z0-9_:]+\s+(?P<name>[A-Z0-9_]+)\s*=\s*(?P<val>0x[0-9A-Fa-f]+|\d+)", re.MULTILINE)


def load_contract(contract_path: Path) -> dict:
    """加载 YAML 格式的跨仓单一协议契约真源（文件缺失时抛 FileNotFoundError）。"""
    if not contract_path.is_file():
        raise FileNotFoundError(f"契约真源文件不存在: {contract_path}")
    return yaml.safe_load(contract_path.read_text(encoding="utf-8"))


def crc16_ccitt_false(payload: bytes) -> int:
    """计算完整帧头+载荷字节序列的 CRC-16/CCITT-FALSE (poly=0x1021, init=0xFFFF)。"""
    crc = 0xFFFF
    for byte_val in payload:
        crc ^= byte_val << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if (crc & 0x8000) else (crc << 1) & 0xFFFF
    return crc


def parse_header_constants(text: str) -> Dict[str, int]:
    """从 C/C++ 头文件提取 `#define` 与 `constexpr` 整型常量并补全组合帧长。"""
    consts: Dict[str, int] = {}
    for pattern in (DEFINE_RE, CONSTEXPR_RE):
        for match in pattern.finditer(text or ""):
            raw = match.group("val")
            consts[match.group("name")] = int(raw, 16 if raw.lower().startswith("0x") else 10)
    if "MINIMC_MAX_FRAME_SIZE" not in consts and "MINIMC_MAX_PAYLOAD_SIZE" in consts:
        hdr = consts.get("MINIMC_HEADER_SIZE", 12)
        crc_sz = consts.get("MINIMC_CRC_SIZE", consts.get("MINIMC_CRC16_SIZE", 2))
        consts["MINIMC_MAX_FRAME_SIZE"] = hdr + consts["MINIMC_MAX_PAYLOAD_SIZE"] + crc_sz
    return consts


def _build_macro_map(contract: dict) -> Dict[str, Tuple[str, int]]:
    """根据契约定义构建允许的命令宏到 `(规范语义名, 规范数值)` 的反查表。"""
    mapping: Dict[str, Tuple[str, int]] = {}
    for macro_name, spec in contract.get("allowed_extra_macros", {}).items():
        mapping[macro_name] = (spec["group"], int(spec["code"]))
    for group_name, spec in contract.get("canonical_commands", {}).items():
        for alias in spec.get("aliases", []):
            mapping[alias] = (group_name, int(spec["code"]))
    return mapping


def _check_capacity_and_required(
    ep_name: str, consts: Dict[str, int], contract: dict, full_app: bool
) -> List[str]:
    """校验单端点必需命令覆盖率以及 OTA `>=520B` 载荷 / `>=534B` 帧容量红线。"""
    errors: List[str] = []
    for key, spec in contract.get("canonical_commands", {}).items():
        if not full_app and not spec.get("boot_required", False):
            continue
        code = int(spec["code"])
        if not any(consts.get(alias) == code for alias in spec.get("aliases", [])):
            errors.append(f"[{ep_name}] 缺失必需命令 {key}(0x{code:02X})")
    framing = contract["framing"]
    max_pay = max(consts.get("MINIMC_MAX_PAYLOAD_SIZE", 0), consts.get("MAX_PAYLOAD_SIZE", 0))
    max_frm = max(consts.get("MINIMC_MAX_FRAME_SIZE", 0), consts.get("MAX_FRAME_SIZE", 0))
    if max_pay < int(framing["min_max_payload_bytes"]):
        errors.append(f"[{ep_name}] 最大载荷 {max_pay}B 小于红线 {framing['min_max_payload_bytes']}B")
    if max_frm < int(framing["min_max_frame_bytes"]):
        errors.append(f"[{ep_name}] 最大帧长 {max_frm}B 小于红线 {framing['min_max_frame_bytes']}B")
    return errors


def validate_endpoint(
    ep_name: str, consts: Dict[str, int], contract: dict, full_app: bool
) -> List[str]:
    """校验单端常量表的禁用宏、正反向命令码唯一性与容量要求，返回错误列表。"""
    errors = [f"[{ep_name}] 存在禁用宏 {m}" for m in contract["forbidden"]["macros"] if m in consts]
    forbidden_codes = {int(x) for x in contract["forbidden"]["opcodes"]}
    macro_map = _build_macro_map(contract)
    owners: Dict[int, str] = {}
    # 逐项检查 MINIMC_CMD_* 正向值一致性与反向数值唯一性（防同值多义碰撞）
    for name, val in sorted(consts.items()):
        if not name.startswith("MINIMC_CMD_"):
            continue
        if val in forbidden_codes:
            errors.append(f"[{ep_name}] 宏 {name} 使用了禁用保留码 0x{val:02X}")
        if name not in macro_map:
            errors.append(f"[{ep_name}] 未登记的私有命令宏 {name}=0x{val:02X}")
            continue
        group_name, exp_val = macro_map[name]
        if val != exp_val:
            errors.append(f"[{ep_name}] {name}=0x{val:02X} 偏离契约 {group_name}(0x{exp_val:02X})")
        if val in owners and owners[val] != group_name:
            errors.append(f"[{ep_name}] 命令码 0x{val:02X} 发生语义碰撞: {owners[val]} vs {group_name}")
        owners[val] = group_name
    errors.extend(_check_capacity_and_required(ep_name, consts, contract, full_app))
    return errors


def verify_golden_vectors(workspace: Path, contract: dict) -> List[str]:
    """核验黄金字节向量文件 SHA256 完整性及全部正例帧的小端全帧头 CRC-16 自洽性。"""
    gv_cfg = contract["golden_vectors"]
    gv_path = workspace / gv_cfg["path"]
    if not gv_path.is_file():
        return [f"黄金向量文件缺失: {gv_path}"]
    raw = gv_path.read_bytes()
    errors: List[str] = []
    if hashlib.sha256(raw).hexdigest() != gv_cfg["sha256"]:
        errors.append("黄金向量 SHA256 与契约锁不一致")
    vectors = json.loads(raw.decode("utf-8")).get("golden_vectors", [])
    if len(vectors) < int(gv_cfg["min_vector_count"]):
        errors.append(f"黄金向量条数不足: {len(vectors)} < {gv_cfg['min_vector_count']}")
    # 对所有 expected_valid=true 的黄金帧按含 SOF 全帧头+载荷校验小端 CRC-16
    for vec in vectors:
        if not vec.get("expected_valid"):
            continue
        buf = bytes.fromhex(vec["frame_hex"])
        exp_crc, calc_crc = int.from_bytes(buf[-2:], "little"), crc16_ccitt_false(buf[:-2])
        if calc_crc != exp_crc:
            errors.append(f"黄金向量 {vec['id']} CRC 失配: 0x{exp_crc:04X} != 0x{calc_crc:04X}")
    return errors


def render_canonical_header(contract: dict) -> str:
    """从机器契约真源生成标准无歧义的 C/C++ 协议常量参考头文件文本。"""
    fr = contract["framing"]
    lines = [
        "/* 自动生成自 project-control/contracts/minimc_v2_contract.yaml，请勿手改 */",
        "#ifndef MINIMC_V2_GENERATED_CONTRACT_H",
        "#define MINIMC_V2_GENERATED_CONTRACT_H",
        f"#define MINIMC_HEADER_SIZE {int(fr['header_bytes'])}U",
        f"#define MINIMC_CRC_SIZE {int(fr['crc_bytes'])}U",
        f"#define MINIMC_MAX_PAYLOAD_SIZE {int(fr['min_max_payload_bytes'])}U",
        f"#define MINIMC_MAX_FRAME_SIZE {int(fr['min_max_frame_bytes'])}U",
    ]
    for spec in contract["canonical_commands"].values():
        lines.append(f"#define {spec['aliases'][0]} 0x{int(spec['code']):02X}U")
    lines.append("#endif /* MINIMC_V2_GENERATED_CONTRACT_H */\n")
    return "\n".join(lines)


def verify_workspace_contracts(workspace: Path, contract_path: Optional[Path] = None) -> Tuple[bool, List[str]]:
    """对工作区全部五端头文件与黄金帧向量执行契约一致性总检查。"""
    c_path = contract_path or (workspace / "project-control/contracts/minimc_v2_contract.yaml")
    contract, errors = load_contract(c_path), []
    for ep in contract.get("endpoints", []):
        merged, found = {}, False
        for rel in ep["headers"]:
            hp = workspace / rel
            if hp.is_file():
                found = True
                for k, v in parse_header_constants(hp.read_text(encoding="utf-8")).items():
                    if k in merged and merged[k] != v and k.startswith("MINIMC_CMD_"):
                        errors.append(f"[{ep['name']}] 同端跨头文件冲突 {rel}: {k}")
                    merged[k] = v
        errors.extend([f"[{ep['name']}] 未找到头文件"] if not found else validate_endpoint(ep["name"], merged, contract, bool(ep["full_app_table"])))
    errors.extend(verify_golden_vectors(workspace, contract))
    return len(errors) == 0, errors


def main(argv: Optional[List[str]] = None) -> int:
    """命令行入口：校验五端契约一致性，可选通过 `--render-header` 生成标准头文件。"""
    parser = argparse.ArgumentParser(description="MiniMCProto v2 单一契约真源同步与门禁")
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--contract", type=Path, default=None)
    parser.add_argument("--render-header", type=Path, default=None)
    args = parser.parse_args(argv)
    if args.render_header:
        c_path = args.contract or (args.workspace / "project-control/contracts/minimc_v2_contract.yaml")
        args.render_header.parent.mkdir(parents=True, exist_ok=True)
        args.render_header.write_text(render_canonical_header(load_contract(c_path)), encoding="utf-8")
    ok, errs = verify_workspace_contracts(args.workspace, args.contract)
    for err in errs:
        print(f"[CONTRACT-FAIL] {err}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
