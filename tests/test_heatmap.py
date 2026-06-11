"""
tests/test_heatmap.py

Unit tests for the heatmap generation and risk propagation system.
"""

from app.config import CellType
from app.core.state import Position, FireCell
from app.map.grid import Grid
from app.fire.heatmap import generate_heatmap


def test_heatmap_propagation() -> None:
    """Test risk score propagation and wall blocking behavior."""
    grid = Grid(10, 10)

    # Place wall at (5, 4)
    grid.set_cell(5, 4, CellType.WALL)

    # Place fire at (5, 5)
    fire_cells = [FireCell(position=Position(5, 5), ignition_step=0)]

    heatmap = generate_heatmap(grid, fire_cells)

    # Check risk mapping directly on grid cells
    # Risk levels: dist 0=1.0, 1=0.95, 2=0.8, 3=0.6, 4=0.4
    assert grid.cells[5][5].risk == 1.0  # Center (distance 0)
    assert grid.cells[5][6].risk == 0.95  # Distance 1 (DOWN)
    assert grid.cells[5][7].risk == 0.8  # Distance 2 (DOWN)

    # Wall at (5,4) blocks propagation - so cells behind it shouldn't get direct risk
    assert grid.cells[4][5].risk == 0.0  # Wall itself should be blocked/zero risk
    # Point (5,3) is behind the wall - path around via distance ~3 or 4
    assert grid.cells[3][5].risk == 0.4  # Distance ~4 propagated around wall
