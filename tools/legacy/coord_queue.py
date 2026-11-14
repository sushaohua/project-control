#!/usr/bin/env python3
"""投影 COORD 调度队列状态（默认隔离 work_intake 队列）并汇报 Checkpoint 快照状态。"""

import argparse
import json
from pathlib import Path

import yaml

import check_task_graph as graph

# 默认收件单驱动队列路径与历史遗留自动运行队列路径
DEFAULT_INTAKE_QUEUE = "project-control/docs/work_intake/work_intake_queue.yaml"
LEGACY_AUTORUN_QUEUE = "project-control/docs/planning/coord_autorun_queue_20261029.yaml"


def _predecessors_verified_done(card: dict, cards: dict, workspace: Path) -> bool:
    """校验当前任务卡的所有前置依赖任务是否均处于 Done 状态且通过完成度门禁校验。

    Args:
        card: 当前待检任务卡字典。
        cards: 全量任务卡映射表（task_id -> card）。
        workspace: 工作区根目录路径。

    Returns:
        bool: 所有前置任务均已完成且无证据缺失时返回 True，否则返回 False。
    """
    for pred in card.get("depends_on", []):
        pred_card = cards.get(pred, {})
        if pred_card.get("status") != "Done":
            return False
        if graph.done_acceptance_errors(pred, pred_card, cards, workspace):
            return False
    return True


def next_action(queue: dict, cards: dict, workspace: Path) -> dict:
    """根据队列顺序与任务图状态计算 COORD 下一步只读建议动作。

    Args:
        queue: 队列配置字典（包含 bootstrap 与 order 列表）。
        cards: 全量任务卡映射字典。
        workspace: 工作区根目录路径。

    Returns:
        dict: 包含目标任务编号（task）与建议动作（action）的投影字典。

    Raises:
        ValueError: 当队列为空、存在重复任务 ID 或引用未知任务时抛出。
    """
    order = queue.get("bootstrap", []) + queue.get("order", [])
    if not order or len(order) != len(set(order)):
        raise ValueError("queue is empty or contains duplicate task IDs")
    if any(task_id not in cards for task_id in order):
        raise ValueError("queue references an unknown task")
    # 优先恢复处于执行中、评审中或验证中的在途任务
    for task_id in order:
        if cards[task_id].get("status") in {"InProgress", "Review", "Verify"}:
            return {"task": task_id, "action": "resume-existing-assignment"}
    # 按序扫描首个未完成且前置依赖已满足的任务，或挑出存在证据不一致的 Done 任务
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
    """读取本地 coord_state.json 快照以查询 Runner 部署状态与在途任务列表。

    Args:
        workspace: 工作区根目录路径。

    Returns:
        dict: 包含 status（deployed/not-deployed/corrupt-checkpoint）、cursor 与 in_flight 列表的字典。
    """
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
    """解析队列 YAML 文件的绝对路径，支持显式指定路径或回退至历史队列。

    Args:
        workspace: 工作区根目录路径。
        queue_arg: 命令行传入的显式队列路径字符串。
        use_legacy: 是否强制使用历史 autorun 队列。

    Returns:
        Path: 解析后的队列文件绝对路径。
    """
    if queue_arg:
        p = Path(queue_arg)
        return p.resolve() if p.is_absolute() else (workspace / p).resolve()
    rel = LEGACY_AUTORUN_QUEUE if use_legacy else DEFAULT_INTAKE_QUEUE
    candidate = workspace / rel
    if not candidate.is_file():
        candidate = workspace / LEGACY_AUTORUN_QUEUE
    return candidate.resolve()


def main() -> int:
    """命令行入口：校验任务图结构并输出只读队列投影 JSON。

    Returns:
        int: 成功返回 0，发生配置或结构错误返回 1。
    """
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
