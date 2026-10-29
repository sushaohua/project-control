#!/usr/bin/env python3
"""Dependency-aware task scheduling and queue management."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set
import yaml

from .lease_manager import LeaseManager


@dataclass
class ScheduleContext:
    """Context bundle for task scheduling decisions."""
    queue: dict
    cards: dict
    completed_tasks: Set[str] = field(default_factory=set)
    in_flight_tasks: Set[str] = field(default_factory=set)
    lease_mgr: Optional[LeaseManager] = None


class CoordScheduler:
    """Schedules tasks based on dependency graph, readiness, and resource locks."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path(".")).resolve()

    def load_queue(self, queue_path: Path) -> dict:
        target = Path(queue_path).resolve()
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
        return combined

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
            if dep not in completed_tasks:
                dep_card = cards.get(dep, {})
                if dep_card.get("status") != "Done":
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
                ctx.completed_tasks.add(task_id)
                continue
            if not self.is_dependencies_satisfied(task_id, ctx.cards, ctx.completed_tasks):
                continue
            if not self.check_resource_available(card, ctx.lease_mgr):
                continue
            schedulable.append(task_id)
        return schedulable
