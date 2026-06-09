"""
app/map/grid.py

Grid abstraction for the 2D Rescue Simulation System.
Manages grid dimensions, cells, walkability validation, and deterministic neighbor expansion.
"""

from app.config import CellType, GRID_MIN_SIZE, DIRECTIONS
from app.core.state import Cell, Position


class Grid:
    """Manages the 2D cell grid map and pathfinding constraints."""

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize the Grid container.

        Args:
            width: Number of columns.
            height: Number of rows.

        Raises:
            ValueError: If dimensions are smaller than GRID_MIN_SIZE.
        """
        if width < GRID_MIN_SIZE or height < GRID_MIN_SIZE:
            raise ValueError(
                f"Grid dimensions must be at least {GRID_MIN_SIZE}x{GRID_MIN_SIZE}, "
                f"got {width}x{height}"
            )

        self.width: int = width
        self.height: int = height

        # Initialize the 2D cell array cells[y][x] with EMPTY cells
        self.cells: list[list[Cell]] = []
        for y in range(height):
            row = []
            for x in range(width):
                pos = Position(x, y)
                row.append(Cell(position=pos, cell_type=CellType.EMPTY))
            self.cells.append(row)

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Verify if coordinates are within the grid bounds.

        Args:
            x: Column coordinate.
            y: Row coordinate.

        Returns:
            bool: True if in bounds, False otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Cell | None:
        """
        Retrieve cell at given coordinate safely.

        Args:
            x: Column coordinate.
            y: Row coordinate.

        Returns:
            Cell | None: The Cell object if in bounds, None otherwise.
        """
        if not self.in_bounds(x, y):
            return None
        return self.cells[y][x]

    def set_cell(self, x: int, y: int, cell_type: CellType) -> None:
        """
        Update the type of a cell at given coordinate.

        Args:
            x: Column coordinate.
            y: Row coordinate.
            cell_type: The new CellType to assign.

        Returns:
            None

        Raises:
            ValueError: If coordinates are out of bounds.
        """
        if not self.in_bounds(x, y):
            raise ValueError(f"Coordinate ({x}, {y}) is out of bounds.")
        self.cells[y][x].cell_type = cell_type

    def get_neighbors(self, x: int, y: int) -> list[Position]:
        """
        Get in-bounds neighbors of a cell in 4 directions.
        Deterministic order: UP, RIGHT, DOWN, LEFT.

        Args:
            x: Column coordinate.
            y: Row coordinate.

        Returns:
            list[Position]: In-bound neighbor positions.
        """
        neighbors: list[Position] = []
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                neighbors.append(Position(nx, ny))
        return neighbors

    def is_walkable(self, x: int, y: int) -> bool:
        """
        Check if a cell coordinate is navigable (not WALL or FIRE).

        Args:
            x: Column coordinate.
            y: Row coordinate.

        Returns:
            bool: True if navigable, False otherwise.
        """
        if not self.in_bounds(x, y):
            return False
        cell = self.cells[y][x]
        return cell.cell_type not in (CellType.WALL, CellType.FIRE)
