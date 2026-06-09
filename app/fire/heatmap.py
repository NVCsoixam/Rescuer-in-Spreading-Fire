"""
app/fire/heatmap.py

Heatmap system for calculating fire threat and risk scoring.
Propagates risk outward from active fire sources using a depth-limited BFS.
"""

from collections import deque
from app.config import CellType
from app.core.state import FireCell
from app.map.grid import Grid


def generate_heatmap(grid: Grid, fire_cells: list[FireCell]) -> list[list[float]]:
    """
    Generate a 2D matrix of risk values and update cells in the grid.
    Risk is calculated based on shortest path distance to the nearest fire cell,
    respecting WALL boundaries. Max propagation depth is 4.

    Risk values by distance from nearest fire:
    - Distance 0 (burning): 1.0
    - Distance 1: 0.9
    - Distance 2: 0.7
    - Distance 3: 0.5
    - Distance 4: 0.3
    - Distance >= 5 or unreachable: 0.0

    Args:
        grid: The simulation grid.
        fire_cells: The list of currently active FireCell objects.

    Returns:
        list[list[float]]: A 2D grid matrix of computed risk values.
    """
    # Initialize risk matrix with 0.0 values
    risk_matrix = [[0.0 for _ in range(grid.width)] for _ in range(grid.height)]

    if not fire_cells:
        # If there is no fire, reset all grid cell risks to 0.0 and return
        for y in range(grid.height):
            for x in range(grid.width):
                grid.cells[y][x].risk = 0.0
        return risk_matrix

    # BFS lookup table: maps distance to risk penalty
    risk_levels = {
        0: 1.0,
        1: 0.9,
        2: 0.7,
        3: 0.5,
        4: 0.3
    }

    # Queue stores (x, y, distance)
    queue: deque[tuple[int, int, int]] = deque()
    visited: set[tuple[int, int]] = set()

    # Initialize BFS with all fire cell positions at distance 0
    for fc in fire_cells:
        pos = (fc.position.x, fc.position.y)
        queue.append((fc.position.x, fc.position.y, 0))
        visited.add(pos)

    # Perform multi-source BFS up to max depth of 4
    while queue:
        cx, cy, dist = queue.popleft()
        risk_matrix[cy][cx] = risk_levels[dist]

        if dist < 4:
            neighbors = grid.get_neighbors(cx, cy)
            for n in neighbors:
                if (n.x, n.y) not in visited:
                    cell = grid.get_cell(n.x, n.y)
                    # Risk does not propagate through WALL cells
                    if cell is not None and cell.cell_type != CellType.WALL:
                        visited.add((n.x, n.y))
                        queue.append((n.x, n.y, dist + 1))

    # Synchronize calculated risk values back to grid cell objects
    for y in range(grid.height):
        for x in range(grid.width):
            grid.cells[y][x].risk = risk_matrix[y][x]

    return risk_matrix
