"""
app/core/exceptions.py

Custom exception classes for the Rescue Simulation System.
As defined in 05_api_contracts.md (ERROR-001 through ERROR-004).
"""

from __future__ import annotations


class ValidationError(Exception):
    """Raised when configuration or state validation fails."""
    pass


class PathNotFoundError(Exception):
    """Raised when AI pathfinding cannot find a valid route."""
    pass


class InvalidStateTransition(Exception):
    """Raised when an illegal state machine transition is attempted."""
    pass


class SnapshotError(Exception):
    """Raised when snapshot creation or restoration fails."""
    pass