#!/usr/bin/env python3
"""Exception definitions for COORD runner and scheduling."""


class CoordRunnerError(Exception):
    """Base exception for COORD runner errors."""
    pass


class DependencyUnmetError(CoordRunnerError):
    """Raised when a task dependency is missing or not Done."""
    pass


class ResourceConflictError(CoordRunnerError):
    """Raised when a resource lease cannot be acquired due to conflict."""
    pass


class LeaseExpiredError(CoordRunnerError):
    """Raised when operating on an expired lease."""
    pass


class StateTransitionError(CoordRunnerError):
    """Raised when an invalid task state transition is attempted."""
    pass


class RemediationLimitExceededError(CoordRunnerError):
    """Raised when task corrections exceed the configured limit (max 2)."""
    pass


class GateValidationError(CoordRunnerError):
    """Raised when delivery gate checks fail (e.g. fake Done, self-review)."""
    pass


class CheckpointCorruptError(CoordRunnerError):
    """Raised when a checkpoint file is corrupt or unreadable."""
    pass


class ConfigError(CoordRunnerError):
    """Raised when runner configuration is invalid or missing."""
    pass


class CasConflictError(CoordRunnerError):
    """Raised when SHA256 optimistic concurrency check detects a conflicting edit."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.details = dict(details or {})


class IntakeValidationError(CoordRunnerError):
    """Raised when a work_intake submission or category record violates schema/invariants."""

    def __init__(self, message: str, code: str = "INTAKE_INVALID"):
        super().__init__(message)
        self.code = code


class ApprovalValidationError(GateValidationError):
    """Raised when human approval binding is missing, forged, stale, or out of scope."""

    def __init__(self, message: str, code: str = "APPROVAL_REJECTED"):
        super().__init__(message)
        self.code = code


class BoundaryViolationError(GateValidationError):
    """Raised when an execution touches paths outside allowed_paths or inside forbidden_paths."""

    def __init__(self, message: str, paths: list = None):
        super().__init__(message)
        self.violating_paths = list(paths or [])

