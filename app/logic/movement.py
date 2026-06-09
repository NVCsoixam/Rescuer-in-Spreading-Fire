"""
app/logic/movement.py

Movement mechanics and validation logic for entities in the simulation.
Checks walkability constraints before allowing step completion.
"""

from app.core.state import Position
from app.map.grid import Grid


def validate_and_move(grid: Grid, current: Position, direction: tuple[int, int]) -> Position | None:
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
