#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V2 秒级机械门禁 (`Fast-Gate`, `<3s`)。

确定性拦截：协议契约漂移、自研函数 >50 行或 >4 入参、缺失中文 docstring、
残留 `[UNVERIFIED]`、改字节测试桥垫片（Shim）、`ctypes` 后门伪日志、分支违规与路径/预算越界。
"""

from __future__ import annotations

import argparse
import ast
import fnmatch
from pathlib import Path
import re
import subprocess
import sys
from typing import List, Optional, Tuple

import yaml

TOOLS_ROOT = Path(__file__).resolve().parents[1]
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

import sync_contracts

CJK_RE = re.compile(r"[\u4e00-\u9fff]")
C_FUNC_HEAD_RE = re.compile(r"^[A-Za-z_][\w\s\*]+?\s+([A-Za-z_]\w*)\s*\(([^;{}]*)\)\s*\{", re.MULTILINE)
PTR_MAGIC_RE = re.compile(r"\*\s*[A-Za-z_]\w*\s*(\+\+|--)")
SPIN_WAIT_RE = re.compile(r"\bwhile\s*\([^;{}]+\)\s*;")
SHIM_MUTATE_RE = re.compile(r"\bframe\s*\[\s*\d+\s*\]\s*=\s*0x[0-9A-Fa-f]+")


def _has_chinese(text: Optional[str]) -> bool:
    """判断文档字符串是否包含至少一个中文字符。"""
    return bool(text and CJK_RE.search(text))


def _count_code_lines(lines: List[str], start: int, end: int, c_style: bool = False) -> int:
    """统计指定 1-based 行区间内剔除空行与纯注释行后的有效代码行数。"""
    count = 0
    for raw in lines[max(0, start - 1) : end]:
        s = raw.strip()
        if not s or (not c_style and s.startswith("#")):
            continue
        if c_style and (s.startswith("//") or s.startswith("/*") or s.startswith("*")):
            continue
        count += 1
    return count


def check_python_ast(file_path: Path) -> List[str]:
    """检查 Python 文件的模块/类/函数中文 docstring、入参 `<=4` 与函数体 `<=50` 行。"""
    src = file_path.read_text(encoding="utf-8")
    lines, tree = src.splitlines(), ast.parse(src, filename=str(file_path))
    errors = [] if _has_chinese(ast.get_docstring(tree)) else [f"{file_path}: 缺失中文模块 docstring"]
    # 遍历所有类与同步/异步函数定义核验中文注释、非 self/cls 入参个数与有效行数
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and not _has_chinese(ast.get_docstring(node)):
            errors.append(f"{file_path}:{node.lineno}: 类 {node.name} 缺失中文 docstring")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not _has_chinese(ast.get_docstring(node)):
                errors.append(f"{file_path}:{node.lineno}: 函数 {node.name} 缺失中文 docstring")
            args = [a.arg for a in node.args.args + node.args.kwonlyargs]
            args = args[1:] if (args and args[0] in ("self", "cls")) else args
            if len(args) > 4:
                errors.append(f"{file_path}:{node.lineno}: 函数 {node.name} 入参 {len(args)} > 4")
            doc = node.body[0] if node.body and isinstance(node.body[0], ast.Expr) else None
            b_start = (doc.end_lineno + 1) if (doc and ast.get_docstring(node)) else node.lineno + 1
            if _count_code_lines(lines, b_start, node.end_lineno or node.lineno) > 50:
                errors.append(f"{file_path}:{node.lineno}: 函数 {node.name} 有效代码 > 50 行")
    return errors


def _scan_c_source(file_path: Path) -> List[str]:
    """检查自研 C/C++ 源码的函数入参 `<=4`、函数体 `<=50` 行、禁指针自增与禁死等轮询。"""
    src = file_path.read_text(encoding="utf-8", errors="replace")
    lines, errors = src.splitlines(), []
    if PTR_MAGIC_RE.search(src):
        errors.append(f"{file_path}: 禁用指针解引用自增/自减 (*p++)")
    if SPIN_WAIT_RE.search(src):
        errors.append(f"{file_path}: 禁用无超时空分号死循环 while(...);")
    # 基于花括号层级定位 C/C++ 函数体起止行并校验规模与入参数量
    for m in C_FUNC_HEAD_RE.finditer(src):
        fn, raw_p = m.group(1), m.group(2).strip()
        if fn in ("if", "while", "for", "switch"):
            continue
        params = [] if raw_p in ("", "void") else [p for p in raw_p.split(",") if p.strip()]
        s_line = src.count("\n", 0, m.start()) + 1
        if len(params) > 4:
            errors.append(f"{file_path}:{s_line}: C/C++ 函数 {fn} 入参 {len(params)} > 4")
        depth, idx = 0, m.end() - 1
        while idx < len(src):
            depth += (1 if src[idx] == "{" else -1 if src[idx] == "}" else 0)
            if depth == 0:
                break
            idx += 1
        e_line = src.count("\n", 0, idx) + 1
        if _count_code_lines(lines, s_line + 1, max(s_line + 1, e_line - 1), True) > 50:
            errors.append(f"{file_path}:{s_line}: C/C++ 函数 {fn} 有效代码 > 50 行")
    return errors


def check_anti_fake_markers(file_path: Path, rel_path: str) -> List[str]:
    """拦截未消解的 `[UNVERIFIED]` 标记、测试桥改字节垫片与 `ctypes` 后门伪日志。"""
    if file_path.name == "fast_gate.py" or file_path.name.startswith("test_"):
        return []
    text = file_path.read_text(encoding="utf-8", errors="replace")
    errors: List[str] = []
    if "[UNVERIFIED]" in text and file_path.suffix in (".c", ".cpp", ".h", ".hpp", ".py", ".js", ".ts"):
        errors.append(f"{rel_path}: 残留未消解的 [UNVERIFIED] 标记")
    if ("test_harness" in rel_path or "bridge" in file_path.name.lower()) and SHIM_MUTATE_RE.search(text):
        errors.append(f"{rel_path}: 严禁在联调桥/测试夹具中篡改协议帧字节 (Shim)")
    if "probe" in file_path.name.lower() and "ctypes.CDLL" in text:
        errors.append(f"{rel_path}: 严禁使用 ctypes.CDLL 后门注入伪造日志")
    return errors


def check_files_static(
    files: List[Path], workspace: Path, protected_globs: Tuple[str, ...] = ()
) -> List[str]:
    """对文件列表执行静态编码门禁与反造假扫描（受保护存量豁免全量重写门禁）。"""
    errors: List[str] = []
    ws_res = workspace.resolve()
    for fp in files:
        if not fp.is_file():
            continue
        rel = str(fp.resolve().relative_to(ws_res)) if ws_res in fp.resolve().parents else fp.name
        errors.extend(check_anti_fake_markers(fp, rel))
        if any(fnmatch.fnmatch(rel, g) for g in protected_globs):
            continue
        errors.extend(check_python_ast(fp) if fp.suffix == ".py" else _scan_c_source(fp) if fp.suffix in (".c", ".cpp", ".h", ".hpp") else [])
    return errors


def _collect_repo_changes(repo_dir: Path, protected_globs: Tuple[str, ...]) -> Tuple[str, List[str], int]:
    """读取子仓当前分支、变更文件列表（干净时取 HEAD 最近提交）及受保护存量变更行数。"""
    branch = subprocess.check_output(["git", "-C", str(repo_dir), "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", str(repo_dir), "status", "--porcelain"], text=True).splitlines()
    if dirty:
        changed = [ln[3:].split(" -> ")[-1].strip() for ln in dirty if len(ln) > 3]
        diff_cmd = ["git", "-C", str(repo_dir), "diff", "--numstat", "HEAD", "--"]
    else:
        changed = subprocess.check_output(["git", "-C", str(repo_dir), "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"], text=True).splitlines()
        diff_cmd = ["git", "-C", str(repo_dir), "diff", "--numstat", "HEAD~1", "HEAD", "--"]
    prot_lines = 0
    for rel in changed:
        if any(fnmatch.fnmatch(rel, g) for g in protected_globs):
            for row in subprocess.run(diff_cmd + [rel], text=True, capture_output=True).stdout.splitlines():
                p = row.split("\t")
                prot_lines += (int(p[0]) + int(p[1])) if (len(p) >= 2 and p[0].isdigit() and p[1].isdigit()) else 0
    return branch, [c for c in changed if c], prot_lines


def check_subtask_boundary(workspace: Path, subtask: dict) -> List[str]:
    """核验切片子任务开发分支红线、`allowed_paths`、`diff_budget` 与改动文件静态规范。"""
    repo_rel, budget = subtask["repo"], subtask.get("diff_budget") or {}
    repo_dir, prot_globs = workspace / repo_rel, tuple(budget.get("protected_globs") or ())
    branch, changed, prot_lines = _collect_repo_changes(repo_dir, prot_globs)
    errors: List[str] = []
    if repo_rel.startswith("boot/") and branch == "main":
        errors.append(f"[{repo_rel}] 触犯红线：严禁在 main 分支开发 Bootloader")
    if branch != subtask["branch"]:
        errors.append(f"[{repo_rel}] 分支不匹配: {branch} != {subtask['branch']}")
    if len(changed) > int(budget.get("max_files", 999)):
        errors.append(f"[{repo_rel}] 改动文件数 {len(changed)} 超出 Diff Budget")
    if prot_globs and prot_lines > int(budget.get("max_protected_lines", 0)):
        errors.append(f"[{repo_rel}] 受保护存量改动 {prot_lines} 行超出预算")
    patterns = subtask.get("allowed_paths") or []
    errors.extend(f"[{repo_rel}] 路径越界修改: {r}" for r in changed if patterns and not any(fnmatch.fnmatch(r, p) for p in patterns))
    errors.extend(check_files_static([repo_dir / r for r in changed if (repo_dir / r).is_file()], workspace, prot_globs))
    return errors


def run_fast_gate(
    workspace: Path, slice_path: Optional[Path] = None, target_files: Optional[List[Path]] = None
) -> Tuple[bool, List[str]]:
    """执行完整 `<3s` 机械门禁：契约对齐 + 指定文件静态门禁 + 切片边界校验。"""
    _, errors = sync_contracts.verify_workspace_contracts(workspace)
    if target_files:
        errors.extend(check_files_static(target_files, workspace))
    if slice_path:
        for st in yaml.safe_load(slice_path.read_text(encoding="utf-8")).get("subtasks", []):
            errors.extend(check_subtask_boundary(workspace, st))
    return len(errors) == 0, errors


def main(argv: Optional[List[str]] = None) -> int:
    """命令行入口：对切片 YAML 或显式文件列表执行 `<3s` Fast-Gate 检查。"""
    parser = argparse.ArgumentParser(description="AI SoC V2 秒级机械门禁 (Fast-Gate)")
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--slice", type=Path, default=None)
    parser.add_argument("--files", nargs="*", type=Path, default=None)
    ns = parser.parse_args(argv)
    ok, errs = run_fast_gate(ns.workspace, ns.slice, ns.files)
    for err in errs:
        print(f"[FAST-GATE-FAIL] {err}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
