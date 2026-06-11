"""
app/logic/movement.py

Movement mechanics and validation logic for entities in the simulation.
Checks walkability constraints before allowing step completion.
Supports both single-step and multi-step movement operations.
"""

from __future__ import annotations
from app.core.state import Position
from app.map.grid import Grid


def validate_and_move(
    grid: Grid, current: Position, direction: tuple[int, int]
) -> Position | None:
    """
    Validate and compute the next position if moving in the specified direction.

    Args:
        grid: The simulation grid map.
        current: The current Position of the entity.
        direction: A direction vector (dx, dy).

    Returns:
        Position | None: The new Position if walkable, or None if the move is invalid or blocked.
    """
    dx, dy = direction
    nx, ny = current.x + dx, current.y + dy

    if grid.is_walkable(nx, ny):
        return Position(nx, ny)

    return None


def is_adjacent(pos1: Position, pos2: Position) -> bool:
    """
    Check if two positions are adjacent (Manhattan distance == 1).

    Args:
        pos1: First Position.
        pos2: Second Position.

    Returns:
        bool: True if adjacent, False otherwise.
    """
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y) == 1