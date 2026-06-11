"""
app/map/grid.py

Grid abstraction for the 2D Rescue Simulation System.
Manages grid dimensions, cells, walkability validation, and deterministic neighbor expansion.
Optimized for performance with caching and batch operations.
"""

from __future__ import annotations
from app.config import CellType, GRID_MIN_SIZE, DIRECTIONS
from app.core.state import Cell, Position


class Grid:
    """Manages the 2D cell grid map and pathfinding constraints."""

    __slots__ = ("width", "height", "cells", "_neighbor_cache")

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
        self.cells: list[list[Cell]] = []
        self._neighbor_cache: dict[tuple[int, int], list[Position]] = {}

        # Initialize the 2D cell array cells[y][x] with EMPTY cells
        for y in range(height):
            row: list[Cell] = []
            for x in range(width):
                pos = Position(x, y)
                row.append(Cell(position=pos, cell_type=CellType.EMPTY))
            self.cells.append(row)

    # ── Bounds Checking ───────────────────────────────────────────

    def in_bounds(self, x: int, y: int) -> bool:
        """Verify if coordinates are within the grid bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def in_bounds_pos(self, pos: Position) -> bool:
        """Verify if a Position is within the grid bounds."""
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    # ── Cell Access ───────────────────────────────────────────────

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

    def get_cell_at(self, pos: Position) -> Cell | None:
        """Get cell at a Position."""
        if not self.in_bounds(pos.x, pos.y):
            return None
        return self.cells[pos.y][pos.x]

    def set_cell(self, x: int, y: int, cell_type: CellType) -> None:
        """
        Update the type of a cell at given coordinate.

        Args:
            x: Column coordinate.
            y: Row coordinate.
            cell_type: The new CellType to assign.

        Raises:
            ValueError: If coordinates are out of bounds.
        """
        if not self.in_bounds(x, y):
            raise ValueError(f"Coordinate ({x}, {y}) is out of bounds.")
        self.cells[y][x].cell_type = cell_type

    def set_cell_type_at(self, pos: Position, cell_type: CellType) -> None:
        """Set cell type at a Position."""
        if not self.in_bounds(pos.x, pos.y):
            raise ValueError(f"Position ({pos.x}, {pos.y}) is out of bounds.")
        self.cells[pos.y][pos.x].cell_type = cell_type

    def get_cell_type(self, x: int, y: int) -> CellType | None:
        """Get cell type at coordinates, or None if out of bounds."""
        cell = self.get_cell(x, y)
        return cell.cell_type if cell is not None else None

    # ── Neighborhood ──────────────────────────────────────────────

    def get_neighbors(self, x: int, y: int) -> list[Position]:
        """
        Get in-bounds neighbors of a cell in 4 directions.
        Deterministic order: UP, RIGHT, DOWN, LEFT.

        Results are cached for performance.

        Args:
            x: Column coordinate.
            y: Row coordinate.

        Returns:
            list[Position]: In-bound neighbor positions.
        """
        key = (x, y)
        cached = self._neighbor_cache.get(key)
        if cached is not None:
            return cached

        neighbors: list[Position] = []
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                neighbors.append(Position(nx, ny))

        # Cache the result (grid is static during simulation steps)
        if len(self._neighbor_cache) < 5000:  # Prevent unbounded cache growth
            self._neighbor_cache[key] = neighbors
        return neighbors

    def get_neighbors_of(self, pos: Position) -> list[Position]:
        """Get neighbors at a Position."""
        return self.get_neighbors(pos.x, pos.y)

    def clear_neighbor_cache(self) -> None:
        """Clear the neighbor cache (call after map changes)."""
        self._neighbor_cache.clear()

    # ── Walkability ───────────────────────────────────────────────

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

    def is_walkable_pos(self, pos: Position) -> bool:
        """Check if a Position is walkable."""
        return self.is_walkable(pos.x, pos.y)

    def is_blocked(self, x: int, y: int) -> bool:
        """Inverse of is_walkable for readability."""
        return not self.is_walkable(x, y)

    # ── Batch Operations ──────────────────────────────────────────

    def fill_all(self, cell_type: CellType) -> None:
        """Fill entire grid with a single cell type."""
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x].cell_type = cell_type

    def get_empty_cells(self) -> list[Position]:
        """Get all empty (non-wall, non-fire) cell positions."""
        result: list[Position] = []
        for y in range(self.height):
            row = self.cells[y]
            for x in range(self.width):
                if row[x].cell_type == CellType.EMPTY:
                    result.append(Position(x, y))
        return result

    def is_empty(self, x: int, y: int) -> bool:
        """Check if cell is EMPTY."""
        cell = self.get_cell(x, y)
        return cell is not None and cell.cell_type == CellType.EMPTY

    def is_room_cell(self, x: int, y: int) -> bool:
        """Check if a cell has more than 2 open neighbors (indicating a room vs corridor)."""
        open_count = sum(
            1 for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]
            if 0 <= x + dx < self.width and 0 <= y + dy < self.height
            and self.cells[y + dy][x + dx].cell_type != CellType.WALL
        )
        return open_count > 2