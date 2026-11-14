#!/usr/bin/env python3
"""支持历史队列隔离、前置 Done 验收门禁与排他资源锁检查的任务依赖感知调度器。"""

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
    """单次任务调度决策的输入上下文包（队列、任务卡、已完成集、在途集、租约管理器及 Done 对账错误）。"""
    queue: dict
    cards: dict
    completed_tasks: Set[str] = field(default_factory=set)
    in_flight_tasks: Set[str] = field(default_factory=set)
    lease_mgr: Optional[LeaseManager] = None
    done_reconcile_errors: Dict[str, List[str]] = field(default_factory=dict)


def _load_graph_module() -> object:
    """动态加载顶层 `check_task_graph` 模块以复用 `done_acceptance_errors` 校验函数。"""
    tools_dir = Path(__file__).resolve().parent.parent
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    import check_task_graph as graph
    return graph


class CoordScheduler:
    """基于依赖图、已验证 Done 门禁及资源租约可用性筛选下一批可派发任务的调度器。"""

    def __init__(self, workspace_root: Optional[Path] = None, isolate_legacy_queue: bool = False):
        """初始化调度器，绑定工作区根路径与是否强制隔离历史 autorun 队列标志。"""
        self.workspace_root = (workspace_root or Path(".")).resolve()
        self.isolate_legacy_queue = isolate_legacy_queue

    def load_queue(self, queue_path: Path) -> dict:
        """加载并解析队列 YAML 文件；在隔离模式下拒绝加载历史 autorun 队列。"""
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
        """合并 bootstrap 与 order 队列顺序，并在 work_intake 隔离模式下拦截历史前缀任务重跑。"""
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
        """调用 `check_task_graph.done_acceptance_errors` 校验指定 Done 任务的准出证据。"""
        graph = _load_graph_module()
        return list(graph.done_acceptance_errors(task_id, card, cards, self.workspace_root))

    def is_dependencies_satisfied(
        self,
        task_id: str,
        cards: dict,
        completed_tasks: Set[str],
    ) -> bool:
        """检查目标任务是否未被阻塞，且所有直接前置任务均已完成并通过 Done 证据门禁。"""
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
        """检查任务所需的并行实现槽位及排他外设锁当前是否空闲可用。"""
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
        """遍历有序队列，对已标 Done 的任务执行证据对账，并挑出所有依赖与资源均就绪的待派发任务。"""
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
