#!/usr/bin/env python3
"""COORD 运行器的资源租约、并发上限与排他硬件锁管理模块。"""

from dataclasses import dataclass
import time
from typing import Dict, List, Optional
import uuid

from .errors import LeaseExpiredError, ResourceConflictError
from .models import Lease


@dataclass
class LeaseRequest:
    """申请资源租约的请求参数结构体。"""
    task_id: str
    resource: str
    owner: str
    duration_seconds: Optional[float] = None


class LeaseManager:
    """管理任务资源租约、并行实现槽位上限与排他外设锁（获取、续期、过期清理与释放）。"""

    def __init__(
        self,
        max_parallel_impl: int = 2,
        default_duration: float = 1800.0,
        exclusive_devices: Optional[List[str]] = None,
    ):
        """初始化租约管理器，配置最大并行实现数、默认租期秒数与排他设备集合。"""
        self.max_parallel_impl = max_parallel_impl
        self.default_duration = default_duration
        self.exclusive_devices = set(exclusive_devices or ["uart", "hardware-serial", "hil-device", "probe"])
        self._leases: Dict[str, Lease] = {}

    def _generate_lease_id(self, task_id: str, resource: str) -> str:
        """为指定任务与资源生成带 8 位随机十六进制后缀的唯一租约 ID。"""
        safe_res = resource.replace(":", "_").replace("/", "_")
        rand = uuid.uuid4().hex[:8]
        return f"lease_{task_id}_{safe_res}_{rand}"

    def prune_expired_leases(self, now: Optional[float] = None) -> int:
        """扫描并将所有已到达或超过 expires_at 的活跃租约标记为失效，返回清理数量。"""
        cur_time = time.time() if now is None else now
        pruned_count = 0
        for lease in self._leases.values():
            if lease.active and cur_time >= lease.expires_at:
                lease.active = False
                pruned_count += 1
        return pruned_count

    def is_resource_locked(self, resource: str, now: Optional[float] = None) -> bool:
        """判断指定资源当前是否被未过期的活跃租约锁定。"""
        cur_time = time.time() if now is None else now
        for lease in self._leases.values():
            if lease.active and lease.resource == resource and cur_time < lease.expires_at:
                return True
        return False

    def count_active_implementation(self, now: Optional[float] = None) -> int:
        """统计当前未过期的 implementation 类型活跃租约总数。"""
        cur_time = time.time() if now is None else now
        count = 0
        for lease in self._leases.values():
            if lease.active and lease.resource == "implementation" and cur_time < lease.expires_at:
                count += 1
        return count

    def _check_exclusivity(self, resource: str, task_id: str) -> None:
        """检查目标资源是否满足并发槽位上限或排他硬件锁约束，冲突时抛出 ResourceConflictError。"""
        if resource == "implementation":
            active_impl = self.count_active_implementation()
            if active_impl >= self.max_parallel_impl:
                raise ResourceConflictError(
                    f"Max parallel implementation concurrency reached ({self.max_parallel_impl})"
                )
            return
        is_dev = resource in self.exclusive_devices or resource.startswith("device:")
        if is_dev and self.is_resource_locked(resource):
            active_leases = [l for l in self._leases.values() if l.active and l.resource == resource]
            holder = active_leases[0].task_id if active_leases else "unknown"
            raise ResourceConflictError(
                f"Exclusive device '{resource}' is locked by task '{holder}'"
            )

    def acquire_request(self, req: LeaseRequest) -> Lease:
        """先清理过期租约并校验排他性，通过后创建并登记新租约。"""
        self.prune_expired_leases()
        self._check_exclusivity(req.resource, req.task_id)
        now = time.time()
        duration = req.duration_seconds if req.duration_seconds is not None else self.default_duration
        lid = self._generate_lease_id(req.task_id, req.resource)
        lease = Lease(
            lease_id=lid,
            task_id=req.task_id,
            resource=req.resource,
            owner=req.owner,
            acquired_at=now,
            expires_at=now + duration,
            active=True,
        )
        self._leases[lid] = lease
        return lease

    def acquire_lease(self, task_id: str, resource: str, owner: str) -> Lease:
        """按默认租期为指定任务与所有者获取资源租约。"""
        req = LeaseRequest(task_id=task_id, resource=resource, owner=owner)
        return self.acquire_request(req)

    def renew_lease(self, lease_id: str, extend_seconds: float = 1800.0) -> Lease:
        """为尚未过期的活跃租约延长有效期；若租约不存在或已过期则抛出 LeaseExpiredError。"""
        lease = self._leases.get(lease_id)
        if not lease or not lease.active:
            raise LeaseExpiredError(f"Cannot renew non-existent or inactive lease: {lease_id}")
        if time.time() >= lease.expires_at:
            lease.active = False
            raise LeaseExpiredError(f"Lease {lease_id} has already expired")
        lease.expires_at += extend_seconds
        return lease

    def release_lease(self, lease_id: str) -> bool:
        """显式释放指定 ID 的活跃租约。"""
        lease = self._leases.get(lease_id)
        if lease and lease.active:
            lease.active = False
            return True
        return False

    def release_task_leases(self, task_id: str) -> int:
        """释放归属于指定任务的全部活跃租约并返回释放数量。"""
        count = 0
        for lease in self._leases.values():
            if lease.task_id == task_id and lease.active:
                lease.active = False
                count += 1
        return count

    def get_active_leases(self, task_id: Optional[str] = None) -> List[Lease]:
        """清理过期租约后，返回全局或指定任务名下的所有活跃租约列表。"""
        self.prune_expired_leases()
        results = []
        for lease in self._leases.values():
            if lease.active and (task_id is None or lease.task_id == task_id):
                results.append(lease)
        return results

    def restore_leases(self, leases: List[Lease]) -> None:
        """从持久化快照恢复租约映射表。"""
        self._leases.clear()
        for lease in leases:
            self._leases[lease.lease_id] = lease
