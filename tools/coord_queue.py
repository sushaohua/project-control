#!/usr/bin/env python3
"""Project the COORD queue without launching agents or changing task state."""

import argparse
import json
from pathlib import Path

import yaml

import check_task_graph as graph


def next_action(queue: dict, cards: dict, workspace: Path) -> dict:
    order = queue.get("bootstrap", []) + queue.get("order", [])
    if not order or len(order) != len(set(order)):
        raise ValueError("queue is empty or contains duplicate task IDs")
    if any(task_id not in cards for task_id in order):
        raise ValueError("queue references an unknown task")
    for task_id in order:
        if cards[task_id].get("status") in {"InProgress", "Review", "Verify"}:
            return {"task": task_id, "action": "resume-existing-assignment"}
    for task_id in order:
        card = cards[task_id]
        if card.get("status") == "Done":
            errors = graph.done_acceptance_errors(task_id, card, cards, workspace)
            if errors:
                return {"task": task_id, "action": "reconcile-evidence", "issues": errors}
            continue
        missing = [p for p in card.get("depends_on", []) if cards[p].get("status") != "Done"]
        if missing or card.get("blocked"):
            continue
        blockers = graph.readiness_blockers(card, cards, workspace)
        return {"task": task_id, "action": "prepare-ready" if blockers else "dispatch-via-runner",
                "readiness_blockers": blockers}
    return {"task": None, "action": "wait-for-dependencies-or-confirm-queue-complete"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    try:
        path = workspace / "project-control/docs/planning/coord_autorun_queue_20261029.yaml"
        queue = yaml.safe_load(path.read_text(encoding="utf-8"))
        cards, report = graph.check(workspace)
        if report["errors"]:
            raise ValueError("task graph has structural errors: " + "; ".join(report["errors"]))
        result = {"mode": "read-only-queue-projection", "runner_status": queue["runner_status"],
                  "next": next_action(queue, cards, workspace),
                  "limits": "does not launch agents, verify a live server verdict or change status"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
