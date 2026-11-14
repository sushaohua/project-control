#!/usr/bin/env python3
"""COORD 调度运行器与状态机门禁的强类型异常定义模块。"""


class CoordRunnerError(Exception):
    """COORD 运行器异常基类。"""
    pass


class DependencyUnmetError(CoordRunnerError):
    """当任务的前置依赖缺失或未处于 Done 状态时抛出。"""
    pass


class ResourceConflictError(CoordRunnerError):
    """当资源租约或进程级文件锁因并发争用无法获取时抛出。"""
    pass


class LeaseExpiredError(CoordRunnerError):
    """当在已过期的资源租约上执行续期或写操作时抛出。"""
    pass


class StateTransitionError(CoordRunnerError):
    """当尝试执行非法的任务生命周期状态转换时抛出。"""
    pass


class RemediationLimitExceededError(CoordRunnerError):
    """当任务基于证据的纠偏返工次数超过上限（最多 2 次）时抛出。"""
    pass


class GateValidationError(CoordRunnerError):
    """当交付门禁校验失败（如伪造 Done、自审或缺少服务端证明）时抛出。"""
    pass


class CheckpointCorruptError(CoordRunnerError):
    """当 Checkpoint 快照文件损坏、格式非法或无法原子写入时抛出。"""
    pass


class ConfigError(CoordRunnerError):
    """当运行器配置缺失或参数不合法时抛出。"""
    pass


class CasConflictError(CoordRunnerError):
    """当基于 SHA256 摘要的乐观并发控制（CAS）检测到文件已被外部并发修改时抛出。"""

    def __init__(self, message: str, details: dict = None):
        """初始化 CAS 冲突异常并附带冲突路径与期望/实际摘要详情。"""
        super().__init__(message)
        self.details = dict(details or {})


class IntakeValidationError(CoordRunnerError):
    """当 work_intake 收件单或分类记录违反 Schema 或安全不变量时抛出。"""

    def __init__(self, message: str, code: str = "INTAKE_INVALID"):
        """初始化收件单校验异常并绑定机器可读错误码。"""
        super().__init__(message)
        self.code = code


class ApprovalValidationError(GateValidationError):
    """当人工审批绑定缺失、伪造、过期或超出授权范围时抛出。"""

    def __init__(self, message: str, code: str = "APPROVAL_REJECTED"):
        """初始化审批门禁异常并绑定拒绝原因码。"""
        super().__init__(message)
        self.code = code


class BoundaryViolationError(GateValidationError):
    """当执行操作触碰 allowed_paths 白名单之外或 forbidden_paths 黑名单之内的路径时抛出。"""

    def __init__(self, message: str, paths: list = None):
        """初始化路径越界异常并记录违规路径列表。"""
        super().__init__(message)
        self.violating_paths = list(paths or [])

