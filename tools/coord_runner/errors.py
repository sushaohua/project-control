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
