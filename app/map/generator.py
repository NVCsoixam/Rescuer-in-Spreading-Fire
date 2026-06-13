"""
app/map/generator.py

Procedural building map generator for the 2D Rescue Simulation System.
Generates open, connected layouts with rescue stations at map corners as exits.
"""

from __future__ import annotations
import random
from app.config import (
    CellType, SimulationState, RobotState, VictimState,
    DEFAULT_VICTIM_COUNT, DEFAULT_RESCUE_COUNT, DEFAULT_FIRE_SOURCE_COUNT,
)
from app.core.state import (
    Position, Cell, Robot, Victim, RescueStation, FireCell,
    SimulationStats, GameState,
)
from app.map.grid import Grid


class MapGenerator:
    """Generates open, connected map layouts with rescue exits at corners."""

    def __init__(self) -> None:
        """Initialize the map generator."""
        pass

    def generate(
        self,
        width: int,
        height: int,
        seed: int | None = None,
        num_victims: int = DEFAULT_VICTIM_COUNT,
        num_rescue_stations: int = DEFAULT_RESCUE_COUNT,
        num_fire_sources: int = DEFAULT_FIRE_SOURCE_COUNT,
    ) -> GameState:
        """
        Generate a playable connected GameState based on parameters.

        Args:
            width: Width of the grid.
            height: Height of the grid.
            seed: Seed for reproducibility.
            num_victims: Number of victims to generate.
            num_rescue_stations: Number of rescue stations.
            num_fire_sources: Number of initial fire cells.

        Returns:
            GameState: The generated and validated game state.

        Raises:
            RuntimeError: If generation fails after max attempts.
        """
        max_attempts = 150
        for attempt in range(max_attempts):
            rng = random.Random(seed + attempt if seed is not None else None)
            grid = Grid(width, height)

            # 1. Fill grid with walls
            grid.fill_all(CellType.WALL)

            # 2. Generate sparse room layout (more open space)
            rooms = self._place_sparse_rooms(grid, width, height, rng)

            # 3. Carve open corridors to connect rooms (wide paths)
            self._carve_main_corridors(grid, rooms, width, height, rng)

            # 4. Collect available empty positions
            empty_cells = self._collect_cells(grid)

            if len(empty_cells) < 10:
                continue

            # 5. Place rescue stations at CORNERS (exit points)
            try:
                rescue_stations, rescue_positions = self._place_rescue_at_corners(
                    grid, width, height, num_rescue_stations, rng
                )
                robot_pos, robot = self._place_robot(
                    grid, rescue_positions, empty_cells, rng
                )
                victims = self._place_victims(
                    grid, num_victims, empty_cells, rng
                )
                fire_cells = self._place_fire_sources(
                    grid, num_fire_sources, empty_cells, rng
                )
            except (ValueError, IndexError):
                continue

            # 6. Validate connectivity
            if self._validate_connectivity(grid, robot_pos, victims, rescue_stations):
                stats = SimulationStats()
                candidate_state = GameState(
                    grid=grid.cells,
                    robot=robot,
                    victims=victims,
                    rescue_stations=rescue_stations,
                    fire_cells=fire_cells,
                    stats=stats,
                    current_mode=SimulationState.READY,
                    selected_algorithm="ASTAR",
                )
                if self._is_map_winnable(candidate_state):
                    return candidate_state

        raise RuntimeError(f"Failed to generate connected, winnable map after {max_attempts} attempts.")

    def _is_map_winnable(self, state: GameState) -> bool:
        """
        Simulate the game using ASTAR pathfinding algorithm without GUI.
        Return True if the simulation finishes in MISSION_COMPLETE state.
        """
        from app.core.engine import Engine
        from app.core.snapshot import create_snapshot, restore_snapshot

        # Create a deep-copy of the state to avoid mutating the original
        snap = create_snapshot(state)
        test_state = restore_snapshot(snap)

        test_engine = Engine(test_state)
        # Apply standard parameters
        test_engine.fire_interval = 1000.0
        test_engine.step_interval = 200.0

        # Run under A*
        test_engine.start(SimulationState.ASTAR)

        # Fast-forward simulation
        max_simulation_steps = test_state.width * test_state.height * 5
        steps = 0
        while test_engine.state.current_mode not in (SimulationState.MISSION_COMPLETE, SimulationState.MISSION_FAILED):
            test_engine.update(test_engine.step_interval)
            steps += 1
            if steps > max_simulation_steps:
                break

        return test_engine.state.current_mode == SimulationState.MISSION_COMPLETE

    # ── Open Layout Generation ─────────────────────────────────────

    def _place_sparse_rooms(
        self, grid: Grid, width: int, height: int,
        rng: random.Random,
    ) -> list[tuple[int, int, int, int]]:
        """Place rooms with compact spacing for better connectivity."""
        rooms: list[tuple[int, int, int, int]] = []

        # Target: 3-5 rooms depending on grid size
        max_rooms = max(3, min(5, (width * height) // 100))
        num_rooms = rng.randint(3, max_rooms)

        max_attempts = 200
        for _ in range(max_attempts):
            if len(rooms) >= num_rooms:
                break

            # Rooms are modest size (20-40% of grid dimension)
            rw = rng.randint(max(3, width // 6), max(5, width // 4))
            rh = rng.randint(max(3, height // 6), max(5, height // 4))
            # Place with 1 cell border from edge
            rx = rng.randint(1, width - rw - 1)
            ry = rng.randint(1, height - rh - 1)

            # Check overlap with 1-cell buffer
            overlap = any(
                not (rx + rw + 1 < ox or rx > ox + ow + 1 or
                     ry + rh + 1 < oy or ry > oy + oh + 1)
                for ox, oy, ow, oh in rooms
            )
            if not overlap:
                rooms.append((rx, ry, rw, rh))
                for y in range(ry, ry + rh):
                    for x in range(rx, rx + rw):
                        grid.set_cell(x, y, CellType.EMPTY)

        # Fallback: single big room at center
        if not rooms:
            rw, rh = width // 2, height // 2
            rx, ry = (width - rw) // 2, (height - rh) // 2
            rooms.append((rx, ry, rw, rh))
            for y in range(ry, ry + rh):
                for x in range(rx, rx + rw):
                    grid.set_cell(x, y, CellType.EMPTY)

        return rooms

    def _carve_main_corridors(
        self, grid: Grid,
        rooms: list[tuple[int, int, int, int]],
        width: int, height: int,
        rng: random.Random,
    ) -> None:
        """Carve wide corridors connecting rooms + main axes for openness."""
        if len(rooms) < 2:
            return

        # Connect room centers
        centers = [(rx + rw // 2, ry + rh // 2) for rx, ry, rw, rh in rooms]
        rng.shuffle(centers)

        for i in range(len(centers) - 1):
            cx1, cy1 = centers[i]
            cx2, cy2 = centers[i + 1]

            # Wide L-corridors (2 cells wide for openness)
            if rng.choice([True, False]):
                self._carve_h_wide(grid, cx1, cx2, cy1)
                self._carve_v_wide(grid, cy1, cy2, cx2)
            else:
                self._carve_v_wide(grid, cy1, cy2, cx1)
                self._carve_h_wide(grid, cx1, cx2, cy2)

        # Add 1-3 extra connections for better flow
        extra = min(3, len(centers) - 1)
        for _ in range(extra):
            a, b = rng.sample(centers, 2)
            if a == b:
                continue
            if rng.choice([True, False]):
                self._carve_h_wide(grid, a[0], b[0], a[1])
                self._carve_v_wide(grid, a[1], b[1], b[0])
            else:
                self._carve_v_wide(grid, a[1], b[1], a[0])
                self._carve_h_wide(grid, a[0], b[0], b[1])

        # Carve a central horizontal and vertical pathway for openness
        mid_x = width // 2
        mid_y = height // 2
        for y in range(1, height - 1):
            for dx in range(-1, 2):
                nx = mid_x + dx
                if 0 < nx < width - 1 and grid.cells[y][nx].cell_type == CellType.WALL:
                    grid.set_cell(nx, y, CellType.EMPTY)
        for x in range(1, width - 1):
            for dy in range(-1, 2):
                ny = mid_y + dy
                if 0 < ny < height - 1 and grid.cells[ny][x].cell_type == CellType.WALL:
                    grid.set_cell(x, ny, CellType.EMPTY)

        # Carve paths from first room center to all 4 map corners
        # to ensure rescue stations placed at corners are reachable
        if centers:
            cx, cy = centers[0]
            # Top-left corner
            self._carve_h_wide(grid, 1, cx, cy)
            self._carve_v_wide(grid, 1, cy, 1)
            # Top-right corner  
            self._carve_h_wide(grid, cx, width - 2, cy)
            self._carve_v_wide(grid, 1, cy, width - 2)
            # Bottom-left corner
            self._carve_h_wide(grid, 1, cx, cy)
            self._carve_v_wide(grid, cy, height - 2, 1)
            # Bottom-right corner
            self._carve_h_wide(grid, cx, width - 2, cy)
            self._carve_v_wide(grid, cy, height - 2, width - 2)

    @staticmethod
    def _carve_h_wide(grid: Grid, x1: int, x2: int, y: int) -> None:
        """Carve horizontal corridor 2 cells tall."""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for dy in range(-1, 2):
                ny = y + dy
                if grid.in_bounds(x, ny):
                    grid.set_cell(x, ny, CellType.EMPTY)

    @staticmethod
    def _carve_v_wide(grid: Grid, y1: int, y2: int, x: int) -> None:
        """Carve vertical corridor 2 cells wide."""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for dx in range(-1, 2):
                nx = x + dx
                if grid.in_bounds(nx, y):
                    grid.set_cell(nx, y, CellType.EMPTY)

    # ── Rescue at Corners (Exit Points) ────────────────────────────

    def _place_rescue_at_corners(
        self, grid: Grid, width: int, height: int,
        count: int, rng: random.Random,
    ) -> tuple[list[RescueStation], list[Position]]:
        """
        Place rescue stations at map corners.
        Creates an opening in the border wall and marks surrounding
        wall bricks as EXIT_WALL (a different brick style).
        """
        # Corner positions (inner cells, 1 cell from edge)
        corner_positions = [
            Position(1, 1),                          # Top-left
            Position(width - 2, 1),                  # Top-right
            Position(1, height - 2),                 # Bottom-left
            Position(width - 2, height - 2),         # Bottom-right
        ]

        # Shuffle and pick count
        rng.shuffle(corner_positions)
        selected = corner_positions[:min(count, len(corner_positions))]

        stations: list[RescueStation] = []
        for i, pos in enumerate(selected):
            # Clear the rescue station cell
            grid.set_cell(pos.x, pos.y, CellType.RESCUE)

            # Mark border wall bricks around this corner as EXIT_WALL
            # (different brick appearance to show exit)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
                nx, ny = pos.x + dx, pos.y + dy
                if grid.in_bounds(nx, ny):
                    cell = grid.cells[ny][nx]
                    if cell.cell_type == CellType.WALL:
                        cell.cell_type = CellType.EXIT_WALL

            # Also carve a path from rescue station inward if blocked
            # Check if station is surrounded by walls and clear a path
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = pos.x + dx, pos.y + dy
                if (grid.in_bounds(nx, ny) and
                        grid.cells[ny][nx].cell_type == CellType.WALL and
                        1 <= nx < width - 1 and 1 <= ny < height - 1):
                    # Only carve if it helps connectivity (not on the outer edge)
                    if not ((nx == 0 or nx == width - 1) or (ny == 0 or ny == height - 1)):
                        grid.set_cell(nx, ny, CellType.EMPTY)

            stations.append(RescueStation(station_id=i + 1, position=pos))

        return stations, selected

    def _place_robot(
        self, grid: Grid, rescue_positions: list[Position],
        empty_cells: list[Position], rng: random.Random,
    ) -> tuple[Position, Robot]:
        """Place robot near the center of the map."""
        # Prefer center areas
        center_cells = [
            pos for pos in empty_cells
            if grid.width // 4 <= pos.x <= 3 * grid.width // 4 and
               grid.height // 4 <= pos.y <= 3 * grid.height // 4
        ]
        source = center_cells if len(center_cells) >= 3 else empty_cells

        pos = rng.choice(source) if source else Position(1, 1)
        grid.set_cell(pos.x, pos.y, CellType.ROBOT)
        return pos, Robot(position=pos, state=RobotState.IDLE)

    def _place_victims(
        self, grid: Grid, count: int,
        empty_cells: list[Position], rng: random.Random,
    ) -> list[Victim]:
        """Place victims in open areas."""
        positions = self._select_distinct(count, empty_cells, rng)
        victims: list[Victim] = []
        for i, pos in enumerate(positions):
            grid.set_cell(pos.x, pos.y, CellType.VICTIM)
            victims.append(Victim(victim_id=i + 1, position=pos, state=VictimState.WAITING))
        return victims

    def _place_fire_sources(
        self, grid: Grid, count: int,
        empty_cells: list[Position], rng: random.Random,
    ) -> list[FireCell]:
        """Place fire sources away from rescue stations."""
        positions = self._select_distinct(count, empty_cells, rng)
        fire_cells: list[FireCell] = []
        for pos in positions:
            grid.set_cell(pos.x, pos.y, CellType.FIRE)
            fire_cells.append(FireCell(position=pos, ignition_step=0))
        return fire_cells

    # ── Utility ───────────────────────────────────────────────────

    def _collect_cells(
        self, grid: Grid,
    ) -> list[Position]:
        """Collect all EMPTY cells."""
        empty_cells: list[Position] = []
        for y in range(grid.height):
            for x in range(grid.width):
                if grid.cells[y][x].cell_type == CellType.EMPTY:
                    empty_cells.append(Position(x, y))
        return empty_cells

    def _select_distinct(
        self, count: int, pool: list[Position],
        rng: random.Random,
    ) -> list[Position]:
        """Select distinct positions from pool."""
        if len(pool) < count:
            return list(pool)
        return rng.sample(pool, count)

    def _validate_connectivity(
        self, grid: Grid, robot_pos: Position,
        victims: list[Victim], rescue_stations: list[RescueStation],
    ) -> bool:
        """BFS check if all key entities are reachable from robot."""
        visited: set[tuple[int, int]] = {(robot_pos.x, robot_pos.y)}
        queue: list[Position] = [robot_pos]
        head = 0

        while head < len(queue):
            curr = queue[head]
            head += 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = curr.x + dx, curr.y + dy
                if grid.in_bounds(nx, ny) and (nx, ny) not in visited:
                    ct = grid.cells[ny][nx].cell_type
                    if ct not in (CellType.WALL, CellType.FIRE):
                        visited.add((nx, ny))
                        queue.append(Position(nx, ny))

        return all(
            (v.x, v.y) in visited for v in victims
        ) and all(
            (r.x, r.y) in visited for r in rescue_stations
        )