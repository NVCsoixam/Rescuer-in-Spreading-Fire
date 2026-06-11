"""
app/core/snapshot.py

Snapshot system for deep copying and restoring GameState.
Provides functions to capture and revert simulation state deterministically.
"""

from __future__ import annotations
import copy
from app.core.state import GameState


class SnapshotError(Exception):
    """Custom exception raised when snapshot creation or restoration fails."""
    pass


def create_snapshot(state: GameState) -> GameState:
    """
    Create a deep copy of the entire simulation state.

    Args:
        state: The current GameState to clone.

    Returns:
        GameState: A deep-copied GameState object.

    Raises:
        SnapshotError: If deep copying fails.
    """
    try:
        return copy.deepcopy(state)
    except Exception as e:
        raise SnapshotError(f"Failed to create state snapshot: {e}") from e


def restore_snapshot(snapshot: GameState) -> GameState:
    """
    Restore the original simulation state by returning a deep copy.

    Args:
        snapshot: The saved GameState snapshot.

    Returns:
        GameState: A deep-copied GameState object restored from the snapshot.

    Raises:
        SnapshotError: If deep copying fails.
    """
    try:
        return copy.deepcopy(snapshot)
    except Exception as e:
        raise SnapshotError(f"Failed to restore state snapshot: {e}") from e