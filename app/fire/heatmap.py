"""
app/fire/heatmap.py

Heatmap system for calculating fire threat and risk scoring.
Propagates risk outward from active fire sources using depth-limited BFS.
Optimized with iterative queue and early exit patterns.
"""

from __future__ import annotations
from collections import deque
from app.config import CellType
from app.core.state import FireCell, Position
from app.map.grid import Grid

# Risk levels by distance from nearest fire source
RISK_LEVELS: dict[int, float] = {
    0: 1.0,
    1: 0.95,
    2: 0.8,
    3: 0.6,
    4: 0.4,
}

MAX_RISK_DEPTH = 4


def generate_heatmap(grid: Grid, fire_cells: list[FireCell]) -> list[list[float]]:
    """
    Generate a 2D matrix of risk values and update cells in the grid.
    Risk is calculated based on shortest path distance to the nearest fire cell,
    respecting WALL boundaries. Max propagation depth is 4.

    Args:
        grid: The simulation grid.
        fire_cells: The list of currently active FireCell objects.

    Returns:
        list[list[float]]: A 2D grid matrix of computed risk values.
    """
    if grid is None or fire_cells is None:
        return []

    width, height = grid.width, grid.height

    # Initialize risk matrix with 0.0 values
    risk_matrix = [[0.0 for _ in range(width)] for _ in range(height)]

    if not fire_cells:
        # No fire: reset all grid cell risks to 0.0
        for y in range(height):
            for x in range(width):
                grid.cells[y][x].risk = 0.0
        return risk_matrix

    # Multi-source BFS from all fire cells
    queue: deque[tuple[int, int, int]] = deque()
    visited: set[tuple[int, int]] = set()

    # Initialize BFS with all fire cell positions at distance 0
    for fc in fire_cells:
        pos = (fc.position.x, fc.position.y)
        if pos not in visited:  # Avoid duplicates at same position
            queue.append((fc.position.x, fc.position.y, 0))
            visited.add(pos)

    # Perform multi-source BFS up to max depth
    while queue:
        cx, cy, dist = queue.popleft()
        risk_matrix[cy][cx] = RISK_LEVELS[dist]

        if dist < MAX_RISK_DEPTH:
            for n in grid.get_neighbors(cx, cy):
                key = (n.x, n.y)
                if key not in visited:
                    cell = grid.get_cell(n.x, n.y)
                    # Risk does not propagate through WALL cells
                    if cell is not None and cell.cell_type != CellType.WALL:
                        visited.add(key)
                        queue.append((n.x, n.y, dist + 1))

    # Synchronize calculated risk values back to grid cell objects
    for y in range(height):
        row_grid = grid.cells[y]
        row_risk = risk_matrix[y]
        for x in range(width):
            row_grid[x].risk = row_risk[x]

    return risk_matrix