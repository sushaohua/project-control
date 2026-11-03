#!/usr/bin/env python3
"""Project the COORD queue (work_intake isolated by default) and report checkpoint status."""

import argparse
import json
from pathlib import Path

import yaml

import check_task_graph as graph

DEFAULT_INTAKE_QUEUE = "project-control/docs/work_intake/work_intake_queue.yaml"
LEGACY_AUTORUN_QUEUE = "project-control/docs/planning/coord_autorun_queue_20261029.yaml"


def _predecessors_verified_done(card: dict, cards: dict, workspace: Path) -> bool:
    for pred in card.get("depends_on", []):
        pred_card = cards.get(pred, {})
        if pred_card.get("status") != "Done":
            return False
        if graph.done_acceptance_errors(pred, pred_card, cards, workspace):
            return False
    return True


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
        if card.get("blocked") or not _predecessors_verified_done(card, cards, workspace):
            continue
        blockers = graph.readiness_blockers(card, cards, workspace)
        return {
            "task": task_id,
            "action": "prepare-ready" if blockers else "dispatch-via-runner",
            "readiness_blockers": blockers,
        }
    return {"task": None, "action": "wait-for-dependencies-or-confirm-queue-complete"}


def query_runner_state(workspace: Path) -> dict:
    state_path = workspace / "project-control/tools/coord_runner/coord_state.json"
    if not state_path.is_file():
        return {"status": "not-deployed", "in_flight": []}
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
        in_flight = list((data.get("in_flight_tasks") or {}).keys())
        return {"status": "deployed", "cursor": data.get("cursor"), "in_flight": in_flight}
    except (OSError, json.JSONDecodeError):
        return {"status": "corrupt-checkpoint", "in_flight": []}


def _resolve_queue_path(workspace: Path, queue_arg: str, use_legacy: bool) -> Path:
    if queue_arg:
        p = Path(queue_arg)
        return p.resolve() if p.is_absolute() else (workspace / p).resolve()
    rel = LEGACY_AUTORUN_QUEUE if use_legacy else DEFAULT_INTAKE_QUEUE
    candidate = workspace / rel
    if not candidate.is_file():
        candidate = workspace / LEGACY_AUTORUN_QUEUE
    return candidate.resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--queue", default="", help="Explicit queue YAML path")
    parser.add_argument("--legacy-queue", action="store_true", help="Inspect isolated legacy autorun queue")
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    try:
        q_path = _resolve_queue_path(workspace, args.queue, args.legacy_queue)
        queue = yaml.safe_load(q_path.read_text(encoding="utf-8"))
        cards, report = graph.check(workspace)
        if report["errors"]:
            raise ValueError("task graph has structural errors: " + "; ".join(report["errors"]))
        runner_info = query_runner_state(workspace)
        result = {
            "mode": "read-only-queue-projection",
            "queue_file": str(q_path.relative_to(workspace)) if workspace in q_path.parents else str(q_path),
            "queue_domain": queue.get("queue_domain", "legacy_autorun"),
            "legacy_queue_isolated": bool(queue.get("isolate_legacy_queue", False)),
            "runner_status": runner_info["status"],
            "runner_state": runner_info,
            "next": next_action(queue, cards, workspace),
            "limits": "does not launch agents, verify a live server verdict or change status",
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
