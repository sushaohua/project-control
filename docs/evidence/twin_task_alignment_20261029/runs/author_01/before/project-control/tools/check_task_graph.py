#!/usr/bin/env python3
"""Check canonical task structure, schema, readiness, and acceptance without mutating state."""

import argparse
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Task checks require PyYAML (python3-yaml); no packages were installed.")

STATES = {"Backlog", "Ready", "InProgress", "Review", "Verify", "Done"}
REPOSITORIES = {"project-control", "soc-ap", "mcu-p3", "test_harness"}
HEX40_RE = re.compile(r"^[0-9a-fA-F]{40}$")
HEX64_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def read_header(path: Path) -> dict:
    sections = path.read_text(encoding="utf-8").split("---", 2)
    if len(sections) != 3 or sections[0].strip():
        raise ValueError("missing YAML frontmatter")
    header = yaml.safe_load(sections[1])
    if not isinstance(header, dict) or not header.get("id"):
        raise ValueError("missing task id")
    return header


def card_paths(control: Path) -> list:
    patterns = [
        ".agents/kanban/milestones/*.md",
        ".agents/kanban/microtasks/*/*.md",
        "docs/planning/work_packages/TASK-*.md",
        "docs/planning/product/product_pl*.md",
    ]
    paths = []
    for pattern in patterns:
        for path in control.glob(pattern):
            if "superseded" in path.parts or path.name.startswith("README"):
                continue
            paths.append(path)
    return sorted(set(paths))


def find_cycles(cards: dict) -> list:
    complete, stack, cycles = set(), [], []

    def visit(task_id: str):
        if task_id in stack:
            cycles.append(stack[stack.index(task_id):] + [task_id])
            return
        if task_id in complete:
            return
        stack.append(task_id)
        for predecessor in cards[task_id].get("depends_on", []):
            if predecessor in cards:
                visit(predecessor)
        stack.pop()
        complete.add(task_id)

    for tid in cards:
        visit(tid)
    return cycles


def has_ancestor(cards: dict, task_id: str, target: str, visited=None) -> bool:
    visited = set() if visited is None else visited
    if task_id in visited:
        return False
    visited.add(task_id)
    predecessors = cards.get(task_id, {}).get("depends_on", [])
    if target in predecessors:
        return True
    return any(has_ancestor(cards, p, target, visited) for p in predecessors if p in cards)


def is_microtask(task_id: str, card: dict) -> bool:
    return task_id.startswith(("V2-", "MCQ-", "THQ-", "CR-", "TEMP-"))


def _check_task_fields(task_id: str, card: dict) -> list:
    problems = []
    required = [
        "title", "revision", "primary_work_package", "scope_status", "write_scope",
        "protocol_input", "source_baseline", "dispatch_binding", "dependency_conditions",
        "verification", "deliverables", "rollback", "budget", "resources", "checkpoint",
        "review_assignments", "handoff", "execution_contract", "readiness_pending",
    ]
    for field in required:
        if field in {"dependency_conditions", "readiness_pending"}:
            if field not in card:
                problems.append("missing " + field)
        elif not card.get(field):
            problems.append("missing " + field)
    if card.get("status") not in STATES:
        problems.append("invalid status")
    if card.get("scope_status") != "mapped":
        problems.append("new task scope is not mapped")
    if card.get("dispatchable") is not True:
        problems.append("microtask must be dispatchable type (this does not mean Ready)")
    return problems


def _check_parent_and_deps(task_id: str, card: dict, cards: dict) -> list:
    problems = []
    parent_id = card.get("primary_work_package")
    parent = cards.get(parent_id, {})
    if parent.get("task_kind") != "work_package" or task_id not in parent.get("child_tasks", []):
        problems.append("primary work package is missing or does not list this child")
    conditions = card.get("dependency_conditions", [])
    if {item.get("task") for item in conditions} != set(card.get("depends_on", [])):
        problems.append("dependency conditions do not match direct predecessors")
    return problems


def _check_write_scope(task_id: str, card: dict, workspace: Path) -> tuple:
    problems, flat_paths = [], set()
    allowed_repos = set(card.get("allowed_repositories", []))
    for repository, paths in card.get("write_scope", {}).items():
        if repository not in REPOSITORIES or not (workspace / repository).is_dir():
            problems.append("unknown/missing repository: " + repository)
        if repository == "mcu-p3" and "mcu-p3" not in allowed_repos and task_id.startswith("V2-"):
            problems.append("MCU writes are outside this offline increment")
        if not paths:
            problems.append("empty write scope for " + repository)
        for path in paths:
            relative = Path(path)
            if relative.is_absolute() or ".." in relative.parts or path == "**":
                problems.append("unbounded/escaping write path: " + path)
            flat_paths.add(repository + "/" + path)
    if flat_paths != set(card.get("allowed_paths", [])):
        problems.append("allowed_paths differs from write_scope")
    return problems, flat_paths


def _check_verification_commands(task_id: str, card: dict, flat_paths: set) -> list:
    problems = []
    verification = card.get("verification", {})
    for field in ["commands", "positive_cases", "negative_cases"]:
        if not verification.get(field):
            problems.append("missing verification " + field)
    for command in verification.get("commands", []):
        if not all(command.get(field) for field in ["id", "cwd", "command", "expected", "availability"]):
            problems.append("incomplete verification command")
    cpp_writes = [p for p in flat_paths if p.endswith(".cpp")]
    cmd_ids = {c.get("id") for c in verification.get("commands", [])}
    if card.get("task_kind") == "implementation" and cpp_writes:
        if "header" in cmd_ids or not any("build" in cid or "compile" in cid for cid in cmd_ids):
            problems.append("cpp implementation task must compile/build cpp target, not header-only check")
    return problems


def _check_shared_inputs(task_id: str, card: dict, workspace: Path) -> list:
    problems = []
    protocol = card.get("protocol_input", {})
    protocol_path = workspace / protocol.get("path", "__missing__")
    if not protocol_path.is_file():
        problems.append("local protocol input does not exist")
    elif hashlib.sha256(protocol_path.read_bytes()).hexdigest() != protocol.get("sha256"):
        problems.append("protocol hash mismatch")
    for source in card.get("read_sources", []) + [card.get("execution_contract", "")]:
        if source and not (workspace / source).is_file():
            problems.append("missing shared input: " + source)
    sessions = (card.get("review_assignments") or {}).get("reviewer_sessions") or []
    if {item.get("role") for item in sessions} != set(card.get("reviewer") or []):
        problems.append("required reviewer roles differ from assignments")
    root = str((card.get("handoff") or {}).get("evidence_location") or "")
    if not root.startswith("docs/evidence/"):
        problems.append("handoff evidence root must start with docs/evidence/")
    deliv_record = str((card.get("deliverables") or {}).get("record") or "")
    if not deliv_record.startswith(root.rstrip("/") + "/"):
        problems.append("deliverables record must be within task handoff evidence root")
    if (card.get("budget") or {}).get("max_evidence_based_corrections") != 2:
        problems.append("missing two-correction stop rule")
    return problems


def structural_errors(task_id: str, card: dict, cards: dict, workspace: Path) -> list:
    problems = _check_task_fields(task_id, card)
    problems.extend(_check_parent_and_deps(task_id, card, cards))
    scope_problems, flat_paths = _check_write_scope(task_id, card, workspace)
    problems.extend(scope_problems)
    problems.extend(_check_verification_commands(task_id, card, flat_paths))
    problems.extend(_check_shared_inputs(task_id, card, workspace))
    return [task_id + ": " + msg for msg in problems]


def paths_overlap(p1: str, p2: str) -> bool:
    if p1 == p2:
        return True
    if p1.endswith("/**"):
        prefix = p1[:-3]
        if p2 == prefix or p2.startswith(prefix + "/"):
            return True
    if p2.endswith("/**"):
        prefix = p2[:-3]
        if p1 == prefix or p1.startswith(prefix + "/"):
            return True
    return bool(fnmatch.fnmatch(p1, p2) or fnmatch.fnmatch(p2, p1))


def check_path_overlaps(microtasks: dict, cards: dict) -> tuple:
    overlaps, errors = [], []
    for left, left_card in microtasks.items():
        for right, right_card in microtasks.items():
            if left >= right:
                continue
            left_paths = left_card.get("allowed_paths", [])
            right_paths = right_card.get("allowed_paths", [])
            shared = [lp for lp in left_paths if any(paths_overlap(lp, rp) for rp in right_paths)]
            if shared:
                ordered = has_ancestor(cards, left, right) or has_ancestor(cards, right, left)
                overlaps.append({"tasks": [left, right], "paths": sorted(shared), "dependency_ordered": ordered})
                if not ordered:
                    errors.append(left + "/" + right + ": shared writes lack dependency ordering")
    return overlaps, errors


def _check_lease_readiness(card: dict, author: str) -> list:
    blockers = []
    lease = card.get("lease") or {}
    if not all(lease.get(f) for f in ["owner", "task_revision", "lease_id", "expires_at"]):
        blockers.append("actual lease and checkpoint deadline are not registered")
    elif lease.get("owner") != author or lease.get("task_revision") != card.get("revision"):
        blockers.append("lease does not match author/task revision")
    else:
        exp_str = str(lease.get("expires_at", ""))
        try:
            exp_dt = datetime.fromisoformat(exp_str.replace("Z", "+00:00"))
            if exp_dt.tzinfo is None:
                exp_dt = exp_dt.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) > exp_dt:
                blockers.append("lease has expired")
        except (ValueError, TypeError):
            blockers.append("invalid lease expires_at format")
    return blockers


def _check_dispatch_binding_readiness(card: dict) -> list:
    blockers = []
    binding = card.get("dispatch_binding") or {}
    base = str(card.get("base_commit", ""))
    src = str(binding.get("source_commit", ""))
    diff_sha = str(binding.get("workspace_diff_sha256", ""))
    if not base or not src or not diff_sha:
        blockers.append("dispatch input commit/diff is not bound")
    elif not HEX40_RE.match(src) or not HEX64_RE.match(diff_sha) or src.startswith("not-"):
        blockers.append("dispatch input commit/diff contains invalid/bogus hash")
    return blockers


def _check_dependency_conditions_readiness(card: dict, cards: dict, workspace: Path = None) -> list:
    blockers = []
    for cond in card.get("dependency_conditions", []):
        pred = cond.get("task")
        if cards.get(pred, {}).get("status") != "Done":
            blockers.append(pred + " is not Done")
        av = str(cond.get("accepted_version", ""))
        ae = str(cond.get("acceptance_evidence", ""))
        if not av or av.startswith("not-an-accepted"):
            blockers.append(pred + " accepted deliverable/version is not bound")
        if not ae:
            blockers.append(pred + " acceptance evidence path is missing")
        elif workspace and not (workspace / ae).is_file() and not (workspace / "project-control" / ae).is_file():
            blockers.append(pred + " acceptance evidence file does not exist: " + ae)
    return blockers


def readiness_blockers(card: dict, cards: dict, *args, **kw) -> list:
    workspace = args[0] if len(args) > 0 else kw.get("workspace")
    blockers = []
    if card.get("blocked") is True:
        blockers.append("task is marked blocked")
    author = (card.get("executor") or {}).get("agent_id")
    if not author or card.get("owner") != author:
        blockers.append("actual owner/executor is not assigned consistently")
    assignments = (card.get("review_assignments") or {}).get("reviewer_sessions", [])
    if not assignments or any(not item.get("session") for item in assignments):
        blockers.append("required independent reviewer session is not assigned")
    if author and any(item.get("session") == author for item in assignments):
        blockers.append("author cannot be own independent reviewer")
    if not card.get("worktree"):
        blockers.append("actual worktree/working directory is not bound")
    blockers.extend(_check_dispatch_binding_readiness(card))
    blockers.extend(_check_lease_readiness(card, author))
    handoff = card.get("handoff") or {}
    if not handoff.get("receiver_session") or not handoff.get("transport"):
        blockers.append("actual handoff receiver/transport is missing")
    blockers.extend(_check_dependency_conditions_readiness(card, cards, workspace))
    return blockers


def done_acceptance_errors(task_id: str, card: dict, cards: dict, *args, **kw) -> list:
    workspace = args[0] if len(args) > 0 else kw.get("workspace")
    errors = []
    for pred in card.get("depends_on", []):
        if cards.get(pred, {}).get("status") != "Done":
            errors.append(f"{task_id}: marked Done but predecessor {pred} is {cards.get(pred, {}).get('status')}")
    author_identities = {
        card.get("owner"),
        (card.get("executor") or {}).get("agent_id")
    } - {None, ""}
    assignments = (card.get("review_assignments") or {}).get("reviewer_sessions", [])
    if not assignments:
        errors.append(f"{task_id}: marked Done without review assignments")
    for rev in assignments:
        session = rev.get("session")
        if session and session in author_identities:
            errors.append(f"{task_id}: author ({session}) cannot be own independent reviewer")
        dec = str(rev.get("decision", "")).upper()
        if dec not in {"APPROVED", "ACCEPTED"}:
            errors.append(f"{task_id}: review decision is not accepted (found {rev.get('decision')})")
        if not rev.get("artifact_version"):
            errors.append(f"{task_id}: review artifact_version is missing")
        ev = rev.get("evidence")
        if not ev:
            errors.append(f"{task_id}: review evidence path is missing")
        elif workspace and not (workspace / ev).is_file() and not (workspace / "project-control" / ev).is_file():
            errors.append(f"{task_id}: review evidence file does not exist: {ev}")
        elif workspace and rev.get("report_sha256"):
            ev_file = workspace / ev if (workspace / ev).is_file() else workspace / "project-control" / ev
            actual_sha = hashlib.sha256(ev_file.read_bytes()).hexdigest()
            if actual_sha != rev.get("report_sha256"):
                errors.append(
                    f"{task_id}: review report SHA256 mismatch (recorded {rev.get('report_sha256')}, actual {actual_sha})"
                )
    return errors


def _check_candidate_descriptor(candidate_path: Path, workspace: Path) -> list:
    issues = []
    candidate = yaml.safe_load(candidate_path.read_text(encoding="utf-8"))
    if not isinstance(candidate, dict):
        return ["candidate descriptor is not a valid YAML dictionary"]
    for f in ["candidate_id", "scope", "repositories", "protocol", "verification", "limitations", "handoff"]:
        if not candidate.get(f):
            issues.append("candidate missing field: " + f)
    for repo, r_info in (candidate.get("repositories") or {}).items():
        commit = r_info.get("commit", "") if isinstance(r_info, dict) else str(r_info)
        if not HEX40_RE.match(commit) or len(set(commit)) <= 1:
            issues.append(f"candidate repository {repo} commit is invalid/bogus: {commit}")
        elif workspace and (workspace / repo / ".git").is_dir():
            res = subprocess.run(
                ["git", "-C", str(workspace / repo), "cat-file", "-e", commit],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            if res.returncode != 0:
                issues.append(f"candidate repository {repo} commit does not exist in git: {commit}")
    return issues


def artifact_check(card: dict, workspace: Path) -> dict:
    issues, hashes = [], {}
    for name in card.get("deliverables", {}).get("artifacts", []):
        path = workspace / name
        if not path.is_file():
            issues.append("declared deliverable missing: " + name)
        else:
            hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
            if not path.stat().st_size:
                issues.append("declared deliverable empty: " + name)
    if card.get("id") in {"V2-P06C", "V2-P0506"} and hashes:
        cand_path = workspace / "project-control/docs/releases/minimc_v2_offline_candidate.yaml"
        if cand_path.is_file():
            issues.extend(_check_candidate_descriptor(cand_path, workspace))
    return {
        "errors": issues,
        "artifact_hashes": hashes,
        "scope": "presence/hash only; independent content review is still required"
    }


def _collect_cards(control: Path) -> tuple:
    cards, paths, errors = {}, {}, []
    for path in card_paths(control):
        try:
            card = read_header(path)
        except (ValueError, yaml.YAMLError) as error:
            errors.append(str(path.relative_to(control)) + ": " + str(error))
            continue
        tid = card["id"]
        if tid in cards:
            errors.append("duplicate task id: " + tid)
        cards[tid], paths[tid] = card, str(path.relative_to(control))
    return cards, paths, errors


def _validate_task_links(cards: dict) -> list:
    errors = []
    for tid, card in cards.items():
        for pred in card.get("depends_on", []):
            if pred not in cards:
                errors.append(tid + ": missing predecessor " + pred)
        for child in card.get("child_tasks", []):
            if child not in cards:
                errors.append(tid + ": missing child task " + child)
    return errors


def check(workspace: Path) -> tuple:
    control = workspace / "project-control"
    cards, paths, errors = _collect_cards(control)
    errors.extend(_validate_task_links(cards))
    cycles = find_cycles(cards)
    errors.extend("dependency cycle: " + " -> ".join(c) for c in cycles)
    microtasks = {tid: c for tid, c in cards.items() if is_microtask(tid, c)}
    for tid, card in microtasks.items():
        errors.extend(structural_errors(tid, card, cards, workspace))
        parents = [pid for pid, p in cards.items() if tid in p.get("child_tasks", [])]
        if parents != [card.get("primary_work_package")]:
            errors.append(tid + ": must have exactly one primary work-package parent")
        if card.get("status") in {"Ready", "InProgress"}:
            errors.extend(tid + ": state cannot advance: " + b for b in readiness_blockers(card, cards, workspace))
    overlaps, overlap_errors = check_path_overlaps(microtasks, cards)
    errors.extend(overlap_errors)
    return cards, {
        "scope": "static planning validation, not execution/approval/QA acceptance",
        "canonical_task_count": len(cards), "microtask_count": len(microtasks),
        "errors": errors, "dependency_cycles": cycles, "shared_write_pairs": overlaps,
        "readiness_blockers": {tid: readiness_blockers(c, cards, workspace) for tid, c in microtasks.items()},
        "card_paths": paths,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--report", type=Path)
    parser.add_argument("--check-ready", metavar="TASK_ID")
    parser.add_argument("--check-done", metavar="TASK_ID")
    parser.add_argument("--check-artifact", metavar="TASK_ID")
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    try:
        cards, report = check(workspace)
        code = 1 if report["errors"] else 0
        if args.check_ready:
            if args.check_ready not in cards:
                report["errors"].append("unknown task: " + args.check_ready)
                code = 1
            else:
                blockers = readiness_blockers(cards[args.check_ready], cards, workspace)
                report["selected_readiness"] = {"task": args.check_ready, "blockers": blockers}
                if blockers and not code:
                    code = 2
        if args.check_done:
            if args.check_done not in cards:
                report["errors"].append("unknown task: " + args.check_done)
                code = 1
            else:
                done_errs = done_acceptance_errors(args.check_done, cards[args.check_done], cards, workspace)
                report["selected_done"] = {"task": args.check_done, "errors": done_errs}
                if done_errs:
                    code = 1
        if args.check_artifact:
            if args.check_artifact not in cards:
                report["errors"].append("unknown task: " + args.check_artifact)
                code = 1
            else:
                report["selected_artifacts"] = artifact_check(cards[args.check_artifact], workspace)
                if report["selected_artifacts"]["errors"]:
                    code = 1
        report["exit_code"] = code
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as error:
        report, code = {"errors": [str(error)], "exit_code": 1}, 1
    if args.report:
        target = args.report if args.report.is_absolute() else workspace / args.report
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
