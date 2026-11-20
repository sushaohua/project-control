#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI SoC V2 全流程 Git 服务端交接收据、LFS/OCI 核验与阶段续跑模块。"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys, urllib.parse
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Optional, Tuple
import yaml

SHA1_RE, SHA256_RE = re.compile(r"^[0-9a-f]{40}$"), re.compile(r"^[0-9a-f]{64}$")
LFS_HDR = b"version https://git-lfs.github.com/spec/v1"
STAGES = {"plan", "checkpoint", "integration", "docker_qa", "codex", "hil", "release"}
STATUSES = {"PASSED", "FAILED", "BLOCKED", "CHECKPOINT_READY"}

class HandoffError(RuntimeError):
    """服务端交接收据缺失、摘要不符、路径越界或对象阻塞异常。"""

def _git_env() -> dict:
    """构造非交互式 SSH 直连环境变量，清除父仓 Git 变量污染。"""
    env = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
    env["GIT_TERMINAL_PROMPT"] = "0"
    env.setdefault("GIT_SSH_COMMAND", "ssh -o BatchMode=yes -o ConnectTimeout=10")
    return env

def _validate_rel(rel: str) -> str:
    """校验安全 POSIX 相对路径，拒绝绝对路径、file://、越界及 .git 分量。"""
    if not isinstance(rel, str) or not rel or "\\" in rel or "file://" in rel or PurePosixPath(rel).is_absolute() or any(p in ("", ".", "..", ".git") for p in rel.split("/")):
        raise HandoffError(f"非法交接相对路径: {rel}")
    return rel

def _reject_local_refs(obj: Any) -> None:
    """递归拦截元数据中的本地绝对路径或 file:// 引用。"""
    if isinstance(obj, dict): [_reject_local_refs(v) for v in obj.values()]
    elif isinstance(obj, list): [_reject_local_refs(v) for v in obj]
    elif isinstance(obj, str) and (obj.startswith(("file://", "/")) or ("://" in obj and not obj.startswith(("ssh://", "http://", "https://")))):
        raise HandoffError(f"禁止本机私有路径或协议: {obj}")

def _validate_url(url: str) -> str:
    """校验受控远端仓库 URL，严禁 file://、本地路径及 URL 内嵌凭据。"""
    p = urllib.parse.urlsplit(url or "")
    if p.scheme not in ("ssh", "http", "https") or p.password or (p.scheme in ("http", "https") and p.username):
        raise HandoffError(f"不受信任或含凭据的远端 URL: {url}")
    return url

def _sha256_file(path: Path) -> Tuple[int, str]:
    """流式计算常规文件字节数与 SHA-256，拒绝符号链接。"""
    if not path.is_file() or path.is_symlink():
        raise HandoffError(f"交接目标缺失或为符号链接: {path}")
    h, size = hashlib.sha256(), 0
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""): h.update(chunk); size += len(chunk)
    return size, h.hexdigest()

def _parse_locator(raw: Any) -> dict:
    """解析并校验交接定位符 JSON，强制包含有效仓库、ref、40 位提交、相对路径与摘要。"""
    try: doc = json.loads(raw) if isinstance(raw, str) else raw
    except ValueError as err: raise HandoffError(f"交接定位符非合法 JSON（禁止传本地路径）: {err}") from err
    if not isinstance(doc, dict) or any(not isinstance(doc.get(k), str) or not doc.get(k) for k in ("repo", "ref", "commit", "path", "sha256")):
        raise HandoffError("交接定位符缺少必填字段")
    if not SHA1_RE.fullmatch(doc["commit"]) or len(set(doc["commit"])) <= 1 or not SHA256_RE.fullmatch(doc["sha256"]):
        raise HandoffError("交接定位符提交 SHA 或摘要格式无效")
    _validate_rel(doc["path"])
    return doc

def _resolve_remote(repo: str, expected: dict) -> str:
    """从受控工作区或 QA 配置解析仓库远端 URL，拒绝未登记仓库。"""
    if repo in (expected.get("remote_urls") or {}): return _validate_url(expected["remote_urls"][repo])
    ws = Path(expected.get("workspace") or ".")
    if (ws / "workspace.json").is_file():
        data = json.loads((ws / "workspace.json").read_text(encoding="utf-8"))
        wp = data.get("workspace_project") or {}
        if repo in (".", wp.get("path")) and wp.get("url"): return _validate_url(wp["url"])
        for r in data.get("repositories", []):
            if r.get("path") == repo and r.get("url"): return _validate_url(r["url"])
    cfg_p = ws / "project-control/config/qa_runner/default_config.yaml"
    if cfg_p.is_file():
        cfg = yaml.safe_load(cfg_p.read_text(encoding="utf-8")) or {}
        if repo == "." and (cfg.get("workspace_repository") or {}).get("url"): return _validate_url(cfg["workspace_repository"]["url"])
        if ((cfg.get("repositories") or {}).get(repo) or {}).get("url"): return _validate_url(cfg["repositories"][repo]["url"])
    raise HandoffError(f"未登记的交接仓库: {repo}")

def _collect_entries(stage_dir: Path, items: List[Any]) -> List[dict]:
    """收集阶段目录下受控文件的相对路径、字节长度、摘要与存储类型。"""
    root, entries = stage_dir.resolve(), []
    for item in items or []:
        rel = _validate_rel(item["path"] if isinstance(item, dict) else item)
        target = (root / rel).resolve()
        if root not in target.parents: raise HandoffError(f"交接文件越界逃逸: {rel}")
        size, digest = _sha256_file(target)
        with target.open("rb") as f:
            is_ptr = f.read(64).startswith(LFS_HDR)
        storage = item.get("storage") if isinstance(item, dict) and item.get("storage") else ("lfs" if is_ptr else "git")
        entries.append({"path": rel, "bytes": size, "sha256": digest, "storage": storage})
    return entries

def prepare_handoff(stage_dir: Path, metadata: dict, receipt_path: Path) -> dict:
    """校验阶段输入与产物相对路径摘要，原子写出符合契约的交接收据。"""
    if not stage_dir.is_dir() or receipt_path.is_symlink(): raise HandoffError(f"阶段目录缺失或收据路径为符号链接: {stage_dir}")
    stage, status, repos = metadata.get("stage", ""), metadata.get("status", ""), (metadata.get("inputs") or {}).get("repos") or {}
    if stage not in STAGES or status not in STATUSES or not repos: raise HandoffError(f"非法阶段/状态或空仓集合: {stage}/{status}")
    for name, info in repos.items():
        if not SHA1_RE.fullmatch(info.get("commit", "")) or not info.get("ref"): raise HandoffError(f"仓 {name} 缺少合法 ref 或 40 位 commit")
    _reject_local_refs({"inputs": metadata["inputs"], "verdict_ref": metadata.get("verdict_ref"), "approval_ref": metadata.get("approval_ref")})
    prev = _parse_locator(metadata["previous_receipt"]) if metadata.get("previous_receipt") else None
    receipt = {
        "schema_version": 1, "task_id": metadata.get("task_id") or metadata.get("slice_id") or "",
        "slice_id": metadata.get("slice_id") or metadata.get("task_id") or "", "revision": int(metadata.get("revision", 1)),
        "run_id": str(metadata.get("run_id") or stage_dir.name), "stage": stage, "status": status,
        "previous_receipt": prev, "input_fingerprint": str(metadata.get("input_fingerprint", "")), "inputs": metadata["inputs"],
        "evidence": _collect_entries(stage_dir, metadata.get("evidence_paths") or []),
        "artifacts": _collect_entries(stage_dir, metadata.get("artifact_paths") or []),
        "verdict_ref": metadata.get("verdict_ref"), "approval_ref": metadata.get("approval_ref"),
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt

def _fetch_git_commit(url: str, ref: str, commit: str, repo_dir: Path) -> None:
    """以非交互 SSH 从受控远端拉取 ref 并核验 commit 真实可达。"""
    if (repo_dir / ".git").exists(): raise HandoffError(f"下载目标目录非空，禁止复用旧检出: {repo_dir}")
    env = _git_env()
    ls = subprocess.run(["git", "ls-remote", url, ref], text=True, capture_output=True, env=env, timeout=60)
    if ls.returncode != 0 or not ls.stdout.strip(): raise HandoffError(f"远端 ref 不可达: {url} {ref} ({ls.stderr.strip()})")
    repo_dir.mkdir(parents=True, exist_ok=True)
    for cmd in (["init"], ["remote", "add", "origin", url], ["fetch", "origin", ref]):
        res = subprocess.run(["git", "-C", str(repo_dir)] + cmd, text=True, capture_output=True, env=env, timeout=180)
        if res.returncode != 0: raise HandoffError(f"Git 拉取失败 ({' '.join(cmd)}): {res.stderr.strip()}")
    if subprocess.run(["git", "-C", str(repo_dir), "merge-base", "--is-ancestor", commit, "FETCH_HEAD"], capture_output=True, env=env, timeout=30).returncode != 0:
        raise HandoffError(f"提交 {commit} 不在远端分支 {ref} 可达历史内")
    co = subprocess.run(["git", "-C", str(repo_dir), "checkout", "--force", commit], text=True, capture_output=True, env=env, timeout=60)
    if co.returncode != 0: raise HandoffError(f"检出提交失败: {co.stderr.strip()}")

def _hydrate_lfs(repo_dir: Path, rel: str, fp: Path) -> None:
    """对 Git LFS 指针执行空缓存真实拉取，客户端缺失或对象拉取失败立即阻塞。"""
    with fp.open("rb") as f:
        if not f.read(64).startswith(LFS_HDR): return
    if subprocess.run(["git", "lfs", "version"], text=True, capture_output=True, timeout=10).returncode != 0:
        raise HandoffError(f"LFS 指针未展开且缺少 git-lfs 客户端: {rel}")
    pull = subprocess.run(["git", "-C", str(repo_dir), "lfs", "pull", f"--include={rel}"], text=True, capture_output=True, env=_git_env(), timeout=180)
    if pull.returncode != 0: raise HandoffError(f"GitLab LFS 对象拉取失败 ({rel}): {pull.stderr.strip()}")
    with fp.open("rb") as f:
        if f.read(64).startswith(LFS_HDR): raise HandoffError(f"GitLab LFS 拉取后仍为指针文件，服务端对象缺失: {rel}")

def _verify_entries(base_dir: Path, entries: List[dict], repo_dir: Optional[Path] = None) -> List[dict]:
    """逐项核验已拉取文件相对路径、LFS 真实字节与 SHA-256 摘要。"""
    root, guard, verified = base_dir.resolve(), (repo_dir or base_dir).resolve(), []
    for entry in entries:
        rel = _validate_rel(entry["path"])
        fp = (root / rel).resolve()
        if (root not in fp.parents and guard not in fp.parents) or not fp.is_file() or fp.is_symlink():
            raise HandoffError(f"收据文件缺失或软链接越界: {rel}")
        _hydrate_lfs(guard, rel, fp)
        size, digest = _sha256_file(fp)
        if size != entry["bytes"] or digest != entry["sha256"]: raise HandoffError(f"文件摘要或长度不匹配: {rel}")
        verified.append({"path": rel, "bytes": size, "sha256": digest})
    return verified

def _check_expected(receipt: dict, expected: dict) -> None:
    """比对远端收据与预期阶段、切片、指纹、仓提交及锁摘要配置。"""
    if receipt.get("schema_version") != 1 or receipt.get("stage") not in STAGES: raise HandoffError("收据 schema_version 或 stage 无效")
    for key in ("stage", "slice_id", "input_fingerprint"):
        if expected.get(key) and receipt.get(key) != expected[key]: raise HandoffError(f"收据 {key} 不匹配: {receipt.get(key)} != {expected[key]}")
    if expected.get("required_status") and receipt.get("status") != expected["required_status"]: raise HandoffError(f"收据状态未满足: {receipt.get('status')}")
    inputs = receipt.get("inputs") or {}
    for k in ("sdk_lock_sha256", "qa_image_digest"):
        if expected.get(k) and inputs.get(k) != expected[k]: raise HandoffError(f"收据 {k} 不匹配")
    exp_repos, act_repos = expected.get("commits") or {}, {k: v.get("commit") for k, v in (inputs.get("repos") or {}).items()}
    if exp_repos and any(act_repos.get(k) != v for k, v in exp_repos.items()): raise HandoffError("收据仓提交集合与期望候选不符")

def verify_handoff(receipt_ref: str, expected: dict, download_dir: Path) -> dict:
    """按定位符从远端拉取收据及关联证据/制品，校验完整链条后返回读回结果。"""
    loc = _parse_locator(receipt_ref)
    url, repo_dir = _resolve_remote(loc["repo"], expected or {}), download_dir.resolve() / loc["repo"].replace("/", "__")
    _fetch_git_commit(url, loc["ref"], loc["commit"], repo_dir)
    rp = (repo_dir / loc["path"]).resolve()
    if repo_dir.resolve() not in rp.parents or rp.is_symlink() or _sha256_file(rp)[1] != loc["sha256"]:
        raise HandoffError(f"收据路径越界或摘要校验失败: {loc['path']}")
    receipt = json.loads(rp.read_text(encoding="utf-8"))
    _check_expected(receipt, expected or {})
    files = _verify_entries(rp.parent, (receipt.get("evidence") or []) + (receipt.get("artifacts") or []), repo_dir)
    if (expected or {}).get("require_qa") and not any(f["path"].endswith("server_qa.json") for f in files):
        raise HandoffError("交接证据缺少 server_qa.json（禁止仅凭本地 verdict 准出）")
    if (expected or {}).get("verify_previous") and receipt.get("previous_receipt"):
        verify_handoff(json.dumps(receipt["previous_receipt"]), {"workspace": (expected or {}).get("workspace", ".")}, download_dir / "_prev")
    return {"locator": loc, "receipt": receipt, "repo_dir": str(repo_dir), "verified_files": files}

def cruise_precheck(ws: Path, cfg: dict, spec: dict, cp_ready: set) -> Optional[str]:
    """核验服务端交接收据或交付点覆盖的检查点是否就绪，异常时返回阻塞原因。"""
    receipts = cfg.get("handoff_receipts") or {}
    if cfg.get("require_remote_handoff") and not receipts: return "仅传本地裁决缺少服务端交接收据定位符，已阻塞"
    for sid_r, loc in receipts.items():
        if sid_r not in cp_ready:
            try:
                verify_handoff(loc if isinstance(loc, str) else json.dumps(loc), {"workspace": ws, "require_qa": cfg.get("require_remote_handoff")}, ws / f".handoff_tmp_{sid_r}")
                cp_ready.add(sid_r)
            except Exception as err: return f"{sid_r} 服务端交接校验失败: {err}"
    errs = check_deliverable_checkpoints(ws, spec, cp_ready) if spec and spec.get("delivery_kind", "deliverable") == "deliverable" else []
    return "; ".join(errs) if errs else None

def check_deliverable_checkpoints(ws: Path, spec: dict, cp_ready: Optional[set] = None) -> List[str]:
    """核验交付点声明的 covered_checkpoints 是否全部就绪且状态有效。"""
    errs = []
    for cp in spec.get("covered_checkpoints") or []:
        if cp_ready and cp in cp_ready: continue
        cp_file = ws / "project-control/docs/evidence" / cp / "checkpoint_receipt.json"
        if not cp_file.is_file() or json.loads(cp_file.read_text(encoding="utf-8")).get("status") != "CHECKPOINT_READY":
            errs.append(f"缺少或未就绪前序检查点交接收据: {cp}")
    return errs

def save_checkpoint_receipt(ws: Path, spec: dict, out_dir: Path, commits: Dict[str, str]) -> dict:
    """为内部检查点落盘标准 checkpoint_receipt.json（不写正式准出账本）。"""
    sid = spec["slice_id"]
    meta = {"slice_id": sid, "revision": int(spec.get("revision", 1)), "run_id": out_dir.name, "stage": "checkpoint", "status": "CHECKPOINT_READY", "inputs": {"repos": {k: {"ref": "refs/heads/main", "commit": v} for k, v in commits.items()}}, "evidence_paths": [], "artifact_paths": []}
    return prepare_handoff(out_dir, meta, ws / "project-control/docs/evidence" / sid / "checkpoint_receipt.json")

def _qa_matches(qa_dir: Path, spec: dict, commits: Dict[str, str], exp_img: str) -> Optional[dict]:
    """校验单个 docker_qa 目录是否与当前候选提交、测试命令及容器镜像完全一致。"""
    sp, vp, lp = qa_dir / "server_qa.json", qa_dir / "server_verdict.json", qa_dir / "server_lock.json"
    if not (sp.is_file() and vp.is_file() and lp.is_file()): return None
    sq, sv, sl = json.loads(sp.read_text()), json.loads(vp.read_text()), json.loads(lp.read_text())
    if _sha256_file(vp)[1] != (sq.get("server_verdict") or {}).get("sha256") or _sha256_file(lp)[1] != (sq.get("server_lock") or {}).get("sha256"): return None
    if sq.get("passed") is not True or sv.get("verdict") != "PASSED" or sq.get("profile", "host-software") != spec.get("profile", "host-software"): return None
    if {r["name"]: r["commit"] for r in sl.get("repositories", [])} != commits: return None
    img_used = sq.get("qa_image") or (sq.get("sandbox") or {}).get("image", "")
    if exp_img and img_used and img_used != exp_img: return None
    exp_cmds = [(c.get("kind", "test"), c.get("subpath", ""), c.get("command", "")) for c in spec.get("qa_commands", [])]
    if "qa_commands" in sq: return sq if [(c.get("kind", "test"), c.get("subpath", ""), c.get("command", "")) for c in sq["qa_commands"]] == exp_cmds else None
    if spec.get("profile", "host-software") == "host-software" and exp_cmds:
        return sq if [(r.get("subpath", ""), r.get("command", "")) for r in (sq.get("build_results") or []) + (sq.get("test_results") or [])] == [(c[1], c[2]) for c in exp_cmds] else None
    return sq

def try_reuse_qa(ws: Path, spec: dict, commits: Dict[str, str], qa_dir: Path) -> Optional[dict]:
    """同候选、同命令与同镜像下复用已验证的 Docker QA 证据并写入目标目录。"""
    qa_root, cfg_p = ws / "project-control/docs/evidence" / spec["slice_id"], ws / "project-control/config/qa_runner/default_config.yaml"
    prof, exp_img = spec.get("profile", "host-software"), ""
    if cfg_p.is_file():
        sb = (yaml.safe_load(cfg_p.read_text(encoding="utf-8")) or {}).get("sandbox") or {}
        exp_img = sb.get("image", "") if prof == "host-software" else (sb.get("c308l_system_image_digest") if prof == "c308l-system" else sb.get("image_digest")) or ""
    for src in sorted(qa_root.glob("run_*/docker_qa"), reverse=True) if qa_root.is_dir() else []:
        try:
            sq = _qa_matches(src, spec, commits, exp_img)
            if not sq: continue
            qa_dir.mkdir(parents=True, exist_ok=True)
            for fn in ("server_qa.json", "server_verdict.json", "server_lock.json", "checkout.log", "runtime.log"):
                if (src / fn).is_file(): shutil.copy2(src / fn, qa_dir / fn)
            (qa_dir / "qa_runner_call.log").write_text(f"REUSED_QA_FROM={src.name}\n", encoding="utf-8")
            return sq
        except (OSError, ValueError, KeyError, HandoffError): continue
    return None

def main(argv: Optional[List[str]] = None) -> int:
    """命令行入口：校验基于 Git 服务端的交接收据。"""
    p = argparse.ArgumentParser(description="AI SoC V2 Git 服务端交接验证器")
    pv = p.add_subparsers(dest="cmd", required=True).add_parser("verify")
    for k, kw in (("--receipt", {"required": True}), ("--stage", {"default": ""}), ("--out", {"type": Path, "required": True}), ("--workspace", {"type": Path, "default": Path(".")})): pv.add_argument(k, **kw)
    ns = p.parse_args(argv)
    try:
        res = verify_handoff(ns.receipt, {"stage": ns.stage, "workspace": ns.workspace}, ns.out)
        print(json.dumps({"status": "VERIFIED", "commit": res["locator"]["commit"], "files": len(res["verified_files"])}, ensure_ascii=False))
        return 0
    except (HandoffError, ValueError, OSError) as err:
        print(f"[HANDOFF BLOCKED] {err}", file=sys.stderr); return 2

if __name__ == "__main__": sys.exit(main())
