#!/usr/bin/env python3
"""Check canonical task structure and readiness without changing task state."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    sys.exit("Task checks require PyYAML (python3-yaml); no packages were installed.")


STATES = {"Backlog", "Ready", "InProgress", "Review", "Verify", "Done"}
REPOSITORIES = {"project-control", "soc-ap", "mcu-p3", "test_harness"}


def read_header(path):
    sections = path.read_text(encoding="utf-8").split("---", 2)
    if len(sections) != 3 or sections[0].strip():
        raise ValueError("missing YAML frontmatter")
    header = yaml.safe_load(sections[1])
    if not isinstance(header, dict) or not header.get("id"):
        raise ValueError("missing task id")
    return header


def card_paths(control):
    patterns = [
        ".agents/kanban/milestones/*.md",
        ".agents/kanban/microtasks/minimc_v2/V2-*.md",
        "docs/planning/work_packages/TASK-*.md",
        "docs/planning/product/product_pl*.md",
    ]
    return sorted(path for pattern in patterns for path in control.glob(pattern))


def find_cycles(cards):
    complete, stack, cycles = set(), [], []

    def visit(task_id):
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

    for task_id in cards:
        visit(task_id)
    return cycles


def has_ancestor(cards, task_id, target, visited=None):
    visited = set() if visited is None else visited
    if task_id in visited:
        return False
    visited.add(task_id)
    predecessors = cards[task_id].get("depends_on", [])
    return target in predecessors or any(
        has_ancestor(cards, predecessor, target, visited)
        for predecessor in predecessors if predecessor in cards
    )


def structural_errors(task_id, card, cards, workspace):
    problems = []
    required = [
        "title", "revision", "primary_work_package", "scope_status", "write_scope",
        "protocol_input", "source_baseline", "dispatch_binding", "dependency_conditions",
        "verification", "deliverables", "rollback", "budget", "resources", "checkpoint",
        "review_assignments", "handoff", "execution_contract", "readiness_pending",
    ]
    problems.extend(
        "missing " + field for field in required
        if not card.get(field) and field != "dependency_conditions"
    )
    if "dependency_conditions" not in card:
        problems.append("missing dependency_conditions")
    if card.get("status") not in STATES:
        problems.append("invalid status")
    if card.get("scope_status") != "mapped":
        problems.append("new task scope is not mapped")
    if card.get("dispatchable") is not True:
        problems.append("microtask must be dispatchable type (this does not mean Ready)")
    parent_id = card.get("primary_work_package")
    parent = cards.get(parent_id, {})
    if parent.get("task_kind") != "work_package" or task_id not in parent.get("child_tasks", []):
        problems.append("primary work package is missing or does not list this child")
    conditions = card.get("dependency_conditions", [])
    if {item.get("task") for item in conditions} != set(card.get("depends_on", [])):
        problems.append("dependency conditions do not match direct predecessors")
    flat_paths = set()
    for repository, paths in card.get("write_scope", {}).items():
        if repository not in REPOSITORIES or not (workspace / repository).is_dir():
            problems.append("unknown/missing repository: " + repository)
        if repository == "mcu-p3":
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
    protocol = card.get("protocol_input", {})
    protocol_path = workspace / protocol.get("path", "__missing__")
    if not protocol_path.is_file():
        problems.append("local protocol input does not exist")
    elif hashlib.sha256(protocol_path.read_bytes()).hexdigest() != protocol.get("sha256"):
        problems.append("protocol hash mismatch")
    for source in card.get("read_sources", []) + [card.get("execution_contract", "")]:
        if not source or not (workspace / source).is_file():
            problems.append("missing shared input: " + source)
    verification = card.get("verification", {})
    for field in ["commands", "positive_cases", "negative_cases"]:
        if not verification.get(field):
            problems.append("missing verification " + field)
    for command in verification.get("commands", []):
        if not all(command.get(field) for field in ["id", "cwd", "command", "expected", "availability"]):
            problems.append("incomplete verification command")
    sessions = (card.get("review_assignments") or {}).get("reviewer_sessions", [])
    if {item.get("role") for item in sessions} != set(card.get("reviewer", [])):
        problems.append("required reviewer roles differ from assignments")
    root = "docs/evidence/minimc_v2/" + task_id
    if card.get("handoff", {}).get("evidence_location") != root:
        problems.append("handoff evidence root must be unique to this task")
    if not card.get("deliverables", {}).get("record", "").startswith(root + "/runs/"):
        problems.append("missing per-run output location")
    if card.get("budget", {}).get("max_evidence_based_corrections") != 2:
        problems.append("missing two-correction stop rule")
    return [task_id + ": " + message for message in problems]


def readiness_blockers(card, cards):
    blockers = []
    executor = card.get("executor") or {}
    author = executor.get("agent_id")
    if not author or card.get("owner") != author:
        blockers.append("actual owner/executor is not assigned consistently")
    assignments = (card.get("review_assignments") or {}).get("reviewer_sessions", [])
    if not assignments or any(not item.get("session") for item in assignments):
        blockers.append("required independent reviewer session is not assigned")
    if author and any(item.get("session") == author for item in assignments):
        blockers.append("author cannot be own independent reviewer")
    if not card.get("worktree"):
        blockers.append("actual worktree/working directory is not bound")
    binding = card.get("dispatch_binding") or {}
    if not card.get("base_commit") or not binding.get("source_commit") or not binding.get("workspace_diff_sha256"):
        blockers.append("dispatch input commit/diff is not bound")
    lease = card.get("lease") or {}
    if not all(lease.get(field) for field in ["owner", "task_revision", "lease_id", "expires_at"]):
        blockers.append("actual lease and checkpoint deadline are not registered")
    elif lease["owner"] != author or lease["task_revision"] != card.get("revision"):
        blockers.append("lease does not match author/task revision")
    handoff = card.get("handoff") or {}
    if not handoff.get("receiver_session") or not handoff.get("transport"):
        blockers.append("actual handoff receiver/transport is missing")
    for condition in card.get("dependency_conditions", []):
        predecessor = condition["task"]
        if cards.get(predecessor, {}).get("status") != "Done":
            blockers.append(predecessor + " is not Done")
        if not condition.get("accepted_version") or not condition.get("acceptance_evidence"):
            blockers.append(predecessor + " accepted deliverable/version is not bound")
    return blockers


def artifact_check(card, workspace):
    issues, hashes = [], {}
    for name in card.get("deliverables", {}).get("artifacts", []):
        path = workspace / name
        if not path.is_file():
            issues.append("declared deliverable missing: " + name)
        else:
            hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
            if not path.stat().st_size:
                issues.append("declared deliverable empty: " + name)
    if card["id"] == "V2-P06C" and hashes:
        path = workspace / "project-control/docs/releases/minimc_v2_offline_candidate.yaml"
        candidate = yaml.safe_load(path.read_text())
        for field in ["candidate_id", "scope", "repositories", "protocol", "verification", "limitations", "handoff"]:
            if not isinstance(candidate, dict) or not candidate.get(field):
                issues.append("candidate missing field: " + field)
        if isinstance(candidate, dict):
            protocol = candidate.get("protocol")
            if not isinstance(protocol, dict) or protocol.get("sha256") != card["protocol_input"]["sha256"]:
                issues.append("candidate protocol hash differs from accepted input")
    return {"errors": issues, "artifact_hashes": hashes, "scope": "presence/hash only; independent content review is still required"}


def check(workspace):
    control = workspace / "project-control"
    cards, paths, errors = {}, {}, []
    for path in card_paths(control):
        try:
            card = read_header(path)
        except (ValueError, yaml.YAMLError) as error:
            errors.append(str(path.relative_to(control)) + ": " + str(error))
            continue
        task_id = card["id"]
        if task_id in cards:
            errors.append("duplicate task id: " + task_id)
        cards[task_id], paths[task_id] = card, str(path.relative_to(control))
    for task_id, card in cards.items():
        for predecessor in card.get("depends_on", []):
            if predecessor not in cards:
                errors.append(task_id + ": missing predecessor " + predecessor)
        for child in card.get("child_tasks", []):
            if child not in cards:
                errors.append(task_id + ": missing child task " + child)
    cycles = find_cycles(cards)
    errors.extend("dependency cycle: " + " -> ".join(cycle) for cycle in cycles)
    new = {task_id: card for task_id, card in cards.items() if task_id.startswith("V2-")}
    for task_id, card in new.items():
        errors.extend(structural_errors(task_id, card, cards, workspace))
        parents = [
            parent_id for parent_id, parent in cards.items()
            if task_id in parent.get("child_tasks", [])
        ]
        if parents != [card.get("primary_work_package")]:
            errors.append(task_id + ": must have exactly one primary work-package parent")
        if card.get("status") in {"Ready", "InProgress"}:
            errors.extend(
                task_id + ": state cannot advance: " + blocker
                for blocker in readiness_blockers(card, cards)
            )
    overlaps = []
    for left, left_card in new.items():
        for right, right_card in new.items():
            if left >= right:
                continue
            shared = set(left_card.get("allowed_paths", [])) & set(right_card.get("allowed_paths", []))
            if shared:
                ordered = has_ancestor(cards, left, right) or has_ancestor(cards, right, left)
                overlaps.append({"tasks": [left, right], "paths": sorted(shared), "dependency_ordered": ordered})
                if not ordered:
                    errors.append(left + "/" + right + ": shared writes lack dependency ordering")
    return cards, {
        "scope": "static planning validation, not execution/approval/QA acceptance",
        "canonical_task_count": len(cards), "v2_microtask_count": len(new),
        "errors": errors, "dependency_cycles": cycles, "shared_write_pairs": overlaps,
        "readiness_blockers": {task_id: readiness_blockers(card, cards) for task_id, card in new.items()},
        "card_paths": paths,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--report", type=Path)
    parser.add_argument("--check-ready", metavar="TASK_ID")
    parser.add_argument("--check-artifact", metavar="TASK_ID")
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    try:
        cards, report = check(workspace)
        code = 1 if report["errors"] else 0
        if args.check_ready:
            if args.check_ready not in report["readiness_blockers"]:
                report["errors"].append("unknown v2 microtask: " + args.check_ready)
                code = 1
            else:
                blockers = report["readiness_blockers"][args.check_ready]
                report["selected_readiness"] = {"task": args.check_ready, "blockers": blockers}
                if blockers and not code:
                    code = 2
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
