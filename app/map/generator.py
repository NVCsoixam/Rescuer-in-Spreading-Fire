"""
app/map/generator.py

Procedural building map generator for the 2D Rescue Simulation System.
Generates connected rooms and corridors based on environment type, complexity, and seed.
"""

import random
from app.config import (
    CellType, SimulationState, RobotState, VictimState,
    EnvironmentType, Complexity, DEFAULT_VICTIM_COUNT,
    DEFAULT_RESCUE_COUNT, DEFAULT_FIRE_SOURCE_COUNT
)
from app.core.state import (
    Position, Cell, Robot, Victim, RescueStation, FireCell,
    SimulationStats, GameState
)
from app.map.grid import Grid


class MapGenerator:
    """Generates building-like layouts for simulations with connectivity validation."""

    def __init__(self) -> None:
        """Initialize the map generator."""
        pass

    def generate(
        self,
        width: int,
        height: int,
        env_type: EnvironmentType = EnvironmentType.HOSPITAL,
        complexity: Complexity = Complexity.MEDIUM,
        seed: int | None = None,
        num_victims: int = DEFAULT_VICTIM_COUNT,
        num_rescue_stations: int = DEFAULT_RESCUE_COUNT,
        num_fire_sources: int = DEFAULT_FIRE_SOURCE_COUNT
    ) -> GameState:
        """
        Generate a playable connected GameState based on parameters.

        Args:
            width: Width of the grid.
            height: Height of the grid.
            env_type: Type of the building environment (e.g. HOSPITAL, OFFICE).
            complexity: Density and number of rooms (LOW, MEDIUM, HIGH).
            seed: Seed for the random generator to ensure reproducibility.
            num_victims: Number of victims to generate.
            num_rescue_stations: Number of rescue stations to place.
            num_fire_sources: Number of initial fire cells to ignite.

        Returns:
            GameState: The generated and validated game state.
        """
        # Limit retries to prevent infinite loops if settings are too tight
        for attempt in range(20):
            # Create a separate random engine for this generation seed
            rng = random.Random(seed + attempt if seed is not None else None)
            grid = Grid(width, height)

            # 1. Fill grid with walls initially
            for y in range(height):
                for x in range(width):
                    grid.cells[y][x].cell_type = CellType.WALL

            # 2. Determine room parameters based on environment and complexity
            room_params = self._get_room_params(width, height, env_type, complexity, rng)
            min_w, max_w, min_h, max_h, target_rooms = room_params

            # Try to place rooms
            rooms: list[tuple[int, int, int, int]] = []  # List of (x, y, w, h)
            for _ in range(200):  # Maximum attempts to place rooms
                if len(rooms) >= target_rooms:
                    break
                rw = rng.randint(min_w, max_w)
                rh = rng.randint(min_h, max_h)
                rx = rng.randint(1, width - rw - 1)
                ry = rng.randint(1, height - rh - 1)

                # Check overlap with 1-cell buffer padding
                overlap = False
                for ox, oy, ow, oh in rooms:
                    if not (rx + rw + 1 < ox or rx > ox + ow + 1 or
                            ry + rh + 1 < oy or ry > oy + oh + 1):
                        overlap = True
                        break

                if not overlap:
                    rooms.append((rx, ry, rw, rh))
                    # Carve room cells as EMPTY
                    for y in range(ry, ry + rh):
                        for x in range(rx, rx + rw):
                            grid.set_cell(x, y, CellType.EMPTY)

            # Fallback if no rooms were placed
            if not rooms:
                # Place at least one room in the middle
                rw, rh = 4, 4
                rx, ry = (width - rw) // 2, (height - rh) // 2
                rooms.append((rx, ry, rw, rh))
                for y in range(ry, ry + rh):
                    for x in range(rx, rx + rw):
                        grid.set_cell(x, y, CellType.EMPTY)

            # 3. Generate corridors to connect rooms
            self._connect_rooms_with_corridors(rooms, grid, rng)

            # 4. Place entities
            # We need to collect available empty cells
            empty_cells = []
            room_cells = []
            for y in range(height):
                for x in range(width):
                    if grid.cells[y][x].cell_type == CellType.EMPTY:
                        empty_cells.append(Position(x, y))
                        # Check if inside any room
                        for rx, ry, rw, rh in rooms:
                            if rx <= x < rx + rw and ry <= y < ry + rh:
                                room_cells.append(Position(x, y))
                                break

            # Place Rescue Stations (prioritize edge or border cells)
            rescue_stations: list[RescueStation] = []
            rescue_positions = self._place_rescue_stations(
                grid, num_rescue_stations, empty_cells, rng
            )
            for i, pos in enumerate(rescue_positions):
                grid.set_cell(pos.x, pos.y, CellType.RESCUE)
                rescue_stations.append(RescueStation(station_id=i + 1, position=pos))
                if pos in empty_cells:
                    empty_cells.remove(pos)
                if pos in room_cells:
                    room_cells.remove(pos)

            # Place Robot (prioritize positions near rescue stations)
            robot_pos = self._place_robot(rescue_positions, empty_cells, rng)
            grid.set_cell(robot_pos.x, robot_pos.y, CellType.ROBOT)
            robot = Robot(position=robot_pos, state=RobotState.IDLE)
            if robot_pos in empty_cells:
                empty_cells.remove(robot_pos)
            if robot_pos in room_cells:
                room_cells.remove(robot_pos)

            # Place Victims (prioritize inside rooms)
            victims: list[Victim] = []
            victim_positions = self._select_positions(
                num_victims, room_cells, empty_cells, rng
            )
            for i, pos in enumerate(victim_positions):
                grid.set_cell(pos.x, pos.y, CellType.VICTIM)
                victims.append(Victim(victim_id=i + 1, position=pos, state=VictimState.WAITING))
                if pos in empty_cells:
                    empty_cells.remove(pos)
                if pos in room_cells:
                    room_cells.remove(pos)

            # Place Fire Sources (prioritize inside rooms)
            fire_cells: list[FireCell] = []
            fire_positions = self._select_positions(
                num_fire_sources, room_cells, empty_cells, rng
            )
            for pos in fire_positions:
                grid.set_cell(pos.x, pos.y, CellType.FIRE)
                fire_cells.append(FireCell(position=pos, ignition_step=0))
                if pos in empty_cells:
                    empty_cells.remove(pos)
                if pos in room_cells:
                    room_cells.remove(pos)

            # 5. Connectivity validation using BFS
            if self._validate_connectivity(grid, robot_pos, victims, rescue_stations):
                stats = SimulationStats()
                return GameState(
                    grid=grid.cells,
                    robot=robot,
                    victims=victims,
                    rescue_stations=rescue_stations,
                    fire_cells=fire_cells,
                    stats=stats,
                    current_mode=SimulationState.READY,
                    selected_algorithm="ASTAR"
                )

        raise RuntimeError("Failed to generate a fully connected map after 20 attempts.")

    def _get_room_params(
        self, width: int, height: int, env_type: EnvironmentType,
        complexity: Complexity, rng: random.Random
    ) -> tuple[int, int, int, int, int]:
        """Get room min/max size parameters and target room count."""
        # Baseline limits (increased to reduce wall density)
        min_size, max_size = 4, 10
        if env_type == EnvironmentType.APARTMENT:
            min_size, max_size = 4, 6
            base_count = 10
        elif env_type == EnvironmentType.OFFICE:
            min_size, max_size = 6, 10
            base_count = 6
        elif env_type == EnvironmentType.HOSPITAL:
            min_size, max_size = 4, 6
            base_count = 12
        elif env_type == EnvironmentType.WAREHOUSE:
            min_size, max_size = 8, 12
            base_count = 4
        else:  # Mixed
            min_size, max_size = 4, 10
            base_count = 8

        # Scale room count based on complexity
        if complexity == Complexity.LOW:
            target_rooms = max(2, int(base_count * 0.6))
        elif complexity == Complexity.HIGH:
            target_rooms = int(base_count * 1.4)
        else:
            target_rooms = base_count

        # Adjust dimensions for small grid size limits
        max_w = min(max_size, width // 2)
        min_w = min(min_size, max_w)
        max_h = min(max_size, height // 2)
        min_h = min(min_size, max_h)

        # Scale target rooms to not saturate small grids
        max_allowed_rooms = max(2, (width * height) // 35)
        target_rooms = min(target_rooms, max_allowed_rooms)

        return min_w, max_w, min_h, max_h, target_rooms

    def _connect_rooms_with_corridors(
        self, rooms: list[tuple[int, int, int, int]], grid: Grid, rng: random.Random
    ) -> None:
        """Create connecting corridors between rooms to ensure grid graph connectivity."""
        # Calculate centers
        centers = []
        for rx, ry, rw, rh in rooms:
            cx = rx + rw // 2
            cy = ry + rh // 2
            centers.append((cx, cy))

        # Sort rooms by X coordinate to connect neighbors logically
        centers.sort(key=lambda c: c[0])

        for i in range(len(centers) - 1):
            cx1, cy1 = centers[i]
            cx2, cy2 = centers[i + 1]

            # Connect with horizontal first, then vertical
            # (or randomly choose order)
            if rng.choice([True, False]):
                # Horiz then Vert
                self._carve_h_corridor(grid, cx1, cx2, cy1)
                self._carve_v_corridor(grid, cy1, cy2, cx2)
            else:
                # Vert then Horiz
                self._carve_v_corridor(grid, cy1, cy2, cx1)
                self._carve_h_corridor(grid, cx1, cx2, cy2)

    def _carve_h_corridor(self, grid: Grid, x1: int, x2: int, y: int) -> None:
        """Carve horizontal path clearing WALL types to EMPTY."""
        start_x, end_x = min(x1, x2), max(x1, x2)
        for x in range(start_x, end_x + 1):
            if grid.in_bounds(x, y):
                # Don't overwrite existing doors/structures unless necessary
                grid.set_cell(x, y, CellType.EMPTY)

    def _carve_v_corridor(self, grid: Grid, y1: int, y2: int, x: int) -> None:
        """Carve vertical path clearing WALL types to EMPTY."""
        start_y, end_y = min(y1, y2), max(y1, y2)
        for y in range(start_y, end_y + 1):
            if grid.in_bounds(x, y):
                grid.set_cell(x, y, CellType.EMPTY)

    def _place_rescue_stations(
        self, grid: Grid, num_stations: int, empty_cells: list[Position], rng: random.Random
    ) -> list[Position]:
        """Prioritize placing rescue stations near grid borders."""
        border_cells = []
        for pos in empty_cells:
            # Check if cell is within 2 cells of the border
            if pos.x <= 1 or pos.x >= grid.width - 2 or pos.y <= 1 or pos.y >= grid.height - 2:
                border_cells.append(pos)

        # Fallback if no border cell is empty
        source_list = border_cells if len(border_cells) >= num_stations else empty_cells

        if len(source_list) < num_stations:
            # Not enough empty cells; use whatever is available
            return source_list[:]

        return rng.sample(source_list, num_stations)

    def _place_robot(
        self, rescue_positions: list[Position], empty_cells: list[Position], rng: random.Random
    ) -> Position:
        """Prioritize placing the robot near a rescue station."""
        if not rescue_positions:
            return rng.choice(empty_cells) if empty_cells else Position(0, 0)

        # Find empty cells that are close to any rescue station
        close_cells = []
        for pos in empty_cells:
            min_dist = min(abs(pos.x - r.x) + abs(pos.y - r.y) for r in rescue_positions)
            if 1 <= min_dist <= 3:
                close_cells.append(pos)

        source_list = close_cells if close_cells else empty_cells
        return rng.choice(source_list) if source_list else Position(0, 0)

    def _select_positions(
        self, count: int, primary_list: list[Position], fallback_list: list[Position],
        rng: random.Random
    ) -> list[Position]:
        """Select distinct positions prioritizing primary list then fallback list."""
        selected: list[Position] = []

        # Copy lists
        p_list = primary_list[:]
        f_list = [pos for pos in fallback_list if pos not in primary_list]

        for _ in range(count):
            if p_list:
                pos = rng.choice(p_list)
                selected.append(pos)
                p_list.remove(pos)
            elif f_list:
                pos = rng.choice(f_list)
                selected.append(pos)
                f_list.remove(pos)
            else:
                break

        return selected

    def _validate_connectivity(
        self, grid: Grid, robot_pos: Position, victims: list[Victim],
        rescue_stations: list[RescueStation]
    ) -> bool:
        """Perform BFS to check if victims and rescue stations are reachable from robot."""
        visited: set[tuple[int, int]] = { (robot_pos.x, robot_pos.y) }
        queue: list[Position] = [robot_pos]
        head = 0

        # Run standard BFS
        while head < len(queue):
            curr = queue[head]
            head += 1

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = curr.x + dx, curr.y + dy
                if grid.in_bounds(nx, ny) and (nx, ny) not in visited:
                    # During validation check, we can traverse anything that is not a WALL
                    # or active initial FIRE (since robot can't traverse fire cells initially)
                    cell_type = grid.cells[ny][nx].cell_type
                    if cell_type != CellType.WALL and cell_type != CellType.FIRE:
                        visited.add((nx, ny))
                        queue.append(Position(nx, ny))

        # Check if all victims are reachable
        for v in victims:
            if (v.x, v.y) not in visited:
                return False

        # Check if all rescue stations are reachable
        for r in rescue_stations:
            if (r.x, r.y) not in visited:
                return False

        return True
