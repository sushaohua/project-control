#!/usr/bin/env python3
"""Dependency-aware task scheduling with legacy queue isolation and Done acceptance checks."""

from dataclasses import dataclass, field
from pathlib import Path
import sys
from typing import Dict, List, Optional, Set
import yaml

from .errors import ConfigError
from .lease_manager import LeaseManager

LEGACY_QUEUE_NAME = "coord_autorun_queue_20261029.yaml"
LEGACY_TASK_PREFIXES = ("TWIN-", "MS-")


@dataclass
class ScheduleContext:
    """Context bundle for task scheduling decisions."""
    queue: dict
    cards: dict
    completed_tasks: Set[str] = field(default_factory=set)
    in_flight_tasks: Set[str] = field(default_factory=set)
    lease_mgr: Optional[LeaseManager] = None
    done_reconcile_errors: Dict[str, List[str]] = field(default_factory=dict)


def _load_graph_module() -> object:
    tools_dir = Path(__file__).resolve().parent.parent
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    import check_task_graph as graph
    return graph


class CoordScheduler:
    """Schedules tasks based on dependency graph, verified Done gates, and resource locks."""

    def __init__(self, workspace_root: Optional[Path] = None, isolate_legacy_queue: bool = False):
        self.workspace_root = (workspace_root or Path(".")).resolve()
        self.isolate_legacy_queue = isolate_legacy_queue

    def load_queue(self, queue_path: Path) -> dict:
        target = Path(queue_path).resolve()
        if self.isolate_legacy_queue and target.name == LEGACY_QUEUE_NAME:
            raise ConfigError(
                f"Legacy queue {LEGACY_QUEUE_NAME} is isolated from Phase 1 work_intake runner"
            )
        if not target.is_file():
            raise FileNotFoundError(f"Queue file not found: {target}")
        data = yaml.safe_load(target.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"Invalid queue format in {target}")
        return data

    def get_ordered_tasks(self, queue: dict) -> List[str]:
        bootstrap = queue.get("bootstrap", [])
        order = queue.get("order", [])
        combined = list(bootstrap) + [t for t in order if t not in bootstrap]
        isolated = (
            self.isolate_legacy_queue
            or queue.get("isolate_legacy_queue") is True
            or queue.get("queue_domain") == "work_intake"
        )
        if isolated:
            legacy = [tid for tid in combined if str(tid).startswith(LEGACY_TASK_PREFIXES)]
            if legacy:
                raise ConfigError(
                    f"Isolated work_intake queue forbids auto-rerunning legacy tasks: {legacy}"
                )
        return combined

    def _done_acceptance_errors(self, task_id: str, card: dict, cards: dict) -> List[str]:
        graph = _load_graph_module()
        return list(graph.done_acceptance_errors(task_id, card, cards, self.workspace_root))

    def is_dependencies_satisfied(
        self,
        task_id: str,
        cards: dict,
        completed_tasks: Set[str],
    ) -> bool:
        card = cards.get(task_id, {})
        if card.get("blocked", False):
            return False
        deps = card.get("depends_on", [])
        for dep in deps:
            if dep in completed_tasks:
                continue
            dep_card = cards.get(dep, {})
            if dep_card.get("status") != "Done":
                return False
            if self._done_acceptance_errors(dep, dep_card, cards):
                return False
        return True

    def check_resource_available(self, card: dict, lease_mgr: Optional[LeaseManager]) -> bool:
        if lease_mgr is None:
            return True
        task_kind = card.get("task_kind", "implementation")
        if task_kind == "implementation":
            active_impl = lease_mgr.count_active_implementation()
            if active_impl >= lease_mgr.max_parallel_impl:
                return False
        for res_item in card.get("resources", []):
            if isinstance(res_item, dict) and res_item.get("exclusive", False):
                res_name = res_item.get("resource", "")
                if res_name and lease_mgr.is_resource_locked(res_name):
                    return False
        return True

    def select_next_tasks(self, ctx: ScheduleContext) -> List[str]:
        ordered = self.get_ordered_tasks(ctx.queue)
        schedulable = []
        for task_id in ordered:
            if task_id in ctx.completed_tasks or task_id in ctx.in_flight_tasks:
                continue
            card = ctx.cards.get(task_id, {})
            if card.get("status") == "Done":
                errs = self._done_acceptance_errors(task_id, card, ctx.cards)
                if not errs:
                    ctx.completed_tasks.add(task_id)
                else:
                    ctx.done_reconcile_errors[task_id] = errs
                continue
            if not self.is_dependencies_satisfied(task_id, ctx.cards, ctx.completed_tasks):
                continue
            if not self.check_resource_available(card, ctx.lease_mgr):
                continue
            schedulable.append(task_id)
        return schedulable
