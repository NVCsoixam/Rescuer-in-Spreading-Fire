"""
tests/test_movement.py

Unit tests for movement mechanics.
"""

from app.config import CellType
from app.core.state import Position
from app.map.grid import Grid
from app.logic.movement import validate_and_move


def test_validate_and_move_success() -> None:
    """Test valid robot moves into empty cells."""
    grid = Grid(10, 10)
    pos = Position(5, 5)

    # Move RIGHT
    new_pos = validate_and_move(grid, pos, (1, 0))
    assert new_pos == Position(6, 5)


def test_validate_and_move_blocked() -> None:
    """Test movement is blocked by walls, fire, and grid bounds."""
    grid = Grid(10, 10)
    pos = Position(5, 5)

    # 1. Blocked by Wall
    grid.set_cell(6, 5, CellType.WALL)
    assert validate_and_move(grid, pos, (1, 0)) is None

    # 2. Blocked by Fire
    grid.set_cell(5, 4, CellType.FIRE)
    assert validate_and_move(grid, pos, (0, -1)) is None

    # 3. Blocked by Out of Bounds
    edge_pos = Position(0, 0)
    assert validate_and_move(grid, edge_pos, (-1, 0)) is None
