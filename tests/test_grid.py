"""
tests/test_grid.py

Unit tests for the Grid system.
"""

import pytest
from app.config import CellType
from app.core.state import Position
from app.map.grid import Grid


def test_grid_initialization() -> None:
    """Test standard grid initialization and cell setup."""
    grid = Grid(20, 25)
    assert grid.width == 20
    assert grid.height == 25
    assert len(grid.cells) == 25
    assert len(grid.cells[0]) == 20

    # Ensure all cells are empty by default
    for y in range(25):
        for x in range(20):
            cell = grid.get_cell(x, y)
            assert cell is not None
            assert cell.cell_type == CellType.EMPTY
            assert cell.risk == 0.0
            assert cell.fire_level == 0.0


def test_grid_invalid_initialization() -> None:
    """Test initialization failure for dimensions below min size."""
    with pytest.raises(ValueError):
        Grid(9, 20)
    with pytest.raises(ValueError):
        Grid(20, 5)


def test_grid_bounds_checking() -> None:
    """Test in_bounds utility for valid and invalid coordinates."""
    grid = Grid(15, 15)
    assert grid.in_bounds(0, 0) is True
    assert grid.in_bounds(14, 14) is True
    assert grid.in_bounds(-1, 0) is False
    assert grid.in_bounds(0, -1) is False
    assert grid.in_bounds(15, 0) is False
    assert grid.in_bounds(0, 15) is False


def test_get_set_cell() -> None:
    """Test modifying grid cell types and retrieving cells safely."""
    grid = Grid(10, 10)
    cell = grid.get_cell(5, 5)
    assert cell is not None
    assert cell.cell_type == CellType.EMPTY

    # Test out of bounds returns None
    assert grid.get_cell(-1, 0) is None
    assert grid.get_cell(10, 10) is None

    # Test set cell
    grid.set_cell(5, 5, CellType.WALL)
    updated_cell = grid.get_cell(5, 5)
    assert updated_cell is not None
    assert updated_cell.cell_type == CellType.WALL

    # Test set cell out of bounds raises ValueError
    with pytest.raises(ValueError):
        grid.set_cell(-1, 0, CellType.WALL)


def test_neighbor_expansion_ordering() -> None:
    """Test neighbor lookup and the strict UP, RIGHT, DOWN, LEFT order."""
    grid = Grid(10, 10)
    neighbors = grid.get_neighbors(5, 5)
    assert len(neighbors) == 4

    # Order must be: UP (5, 4), RIGHT (6, 5), DOWN (5, 6), LEFT (4, 5)
    assert neighbors[0] == Position(5, 4)
    assert neighbors[1] == Position(6, 5)
    assert neighbors[2] == Position(5, 6)
    assert neighbors[3] == Position(4, 5)

    # Corner case: (0, 0) should only have RIGHT and DOWN
    corner_neighbors = grid.get_neighbors(0, 0)
    assert len(corner_neighbors) == 2
    assert corner_neighbors[0] == Position(1, 0)  # RIGHT
    assert corner_neighbors[1] == Position(0, 1)  # DOWN


def test_grid_walkability() -> None:
    """Test if walkability checks block WALL and FIRE types properly."""
    grid = Grid(10, 10)
    assert grid.is_walkable(5, 5) is True

    grid.set_cell(5, 5, CellType.WALL)
    assert grid.is_walkable(5, 5) is False

    grid.set_cell(5, 5, CellType.FIRE)
    assert grid.is_walkable(5, 5) is False

    # Out of bounds is not walkable
    assert grid.is_walkable(-1, 0) is False
