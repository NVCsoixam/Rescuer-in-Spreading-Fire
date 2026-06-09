"""
app/core/engine.py

Core Simulation Engine for the 2D Rescue Simulation System.
Coordinates lifecycle states, ticks, movement, rescue mechanics, fire spread, and AI pathfinding.
"""

import logging
from app.config import CellType, SimulationState, RobotState, VictimState, FIRE_INTERVAL_DEFAULT
from app.core.state import Position, GameState, PathResult
from app.core.snapshot import create_snapshot, restore_snapshot
from app.logic.movement import validate_and_move
from app.logic.rescue import check_and_pickup, check_and_deliver
from app.fire.fire_sim import spread_fire, check_burn_entities
from app.fire.heatmap import generate_heatmap

# Import pathfinding algorithms
from app.ai.bfs import find_path as bfs_find_path
from app.ai.dfs import find_path as dfs_find_path
from app.ai.ucs import find_path as ucs_find_path
from app.ai.dijkstra import find_path as dijkstra_find_path
from app.ai.greedy import find_path as greedy_find_path
from app.ai.astar import find_path as astar_find_path

# Logger setup
logger = logging.getLogger("SimulationEngine")

# Map SimulationState algorithms to their implementation functions
PATHFINDERS = {
    SimulationState.BFS: bfs_find_path,
    SimulationState.DFS: dfs_find_path,
    SimulationState.UCS: ucs_find_path,
    SimulationState.DIJKSTRA: dijkstra_find_path,
    SimulationState.GREEDY: greedy_find_path,
    SimulationState.ASTAR: astar_find_path
}


class Engine:
    """Controls the simulation execution loop and maintains the single source of truth state."""

    def __init__(self, state: GameState) -> None:
        """
        Initialize the simulation Engine.

        Args:
            state: The GameState object.
        """
        self.state: GameState = state
        self.snapshot: GameState | None = create_snapshot(state)
        self.planned_path: list[Position] = []

        # Ticking controls (in milliseconds)
        self.fire_interval: float = float(FIRE_INTERVAL_DEFAULT)
        self.step_interval: float = 200.0  # Robot moves every 200ms

        self.accumulated_fire_time: float = 0.0
        self.accumulated_sim_time: float = 0.0
        self.prev_mode: SimulationState = SimulationState.READY

    def set_state(self, new_state: GameState) -> None:
        """
        Set a new GameState and update the initial snapshot.

        Args:
            new_state: The new GameState object.
        """
        self.state = new_state
        self.snapshot = create_snapshot(new_state)
        self.planned_path = []
        self.accumulated_fire_time = 0.0
        self.accumulated_sim_time = 0.0

    def start(self, mode: SimulationState) -> bool:
        """
        Start the simulation in the specified execution mode.

        Args:
            mode: The selected running mode (e.g. BFS, ASTAR, USER_MODE).

        Returns:
            bool: True if started successfully, False otherwise.
        """
        # Snapshot the current state before we begin mutating it
        self.snapshot = create_snapshot(self.state)
        self.state.current_mode = mode

        # Clear path cache and accumulators
        self.planned_path = []
        self.accumulated_fire_time = 0.0
        self.accumulated_sim_time = 0.0

        # Initialize heatmap and risk overlays based on start positions of fire
        from app.map.grid import Grid
        grid_obj = Grid(self.state.width, self.state.height)
        grid_obj.cells = self.state.grid
        generate_heatmap(grid_obj, self.state.fire_cells)

        logger.info(f"Simulation started in mode: {mode.value}")
        return True

    def pause(self) -> None:
        """Pause the running simulation."""
        if self.state.current_mode not in (SimulationState.READY, SimulationState.PAUSED,
                                           SimulationState.MISSION_COMPLETE, SimulationState.MISSION_FAILED):
            self.prev_mode = self.state.current_mode
            self.state.current_mode = SimulationState.PAUSED
            logger.info("Simulation paused.")

    def resume(self) -> None:
        """Resume the paused simulation."""
        if self.state.current_mode == SimulationState.PAUSED:
            self.state.current_mode = self.prev_mode
            logger.info(f"Simulation resumed in mode: {self.prev_mode.value}")

    def reset(self) -> None:
        """Reset the simulation back to its initial snapshot state."""
        if self.snapshot is not None:
            restored = restore_snapshot(self.snapshot)

            # In-place copy to preserve references
            self.state.grid = restored.grid
            self.state.robot = restored.robot
            self.state.victims = restored.victims
            self.state.rescue_stations = restored.rescue_stations
            self.state.fire_cells = restored.fire_cells
            self.state.stats = restored.stats
            self.state.current_mode = restored.current_mode
            self.state.selected_algorithm = restored.selected_algorithm

            self.planned_path = []
            self.accumulated_fire_time = 0.0
            self.accumulated_sim_time = 0.0

            # Recalculate heatmap on reset to make sure UI risk levels are correct
            from app.map.grid import Grid
            grid_obj = Grid(self.state.width, self.state.height)
            grid_obj.cells = self.state.grid
            generate_heatmap(grid_obj, self.state.fire_cells)

            logger.info("Simulation state reset to initial snapshot.")

    def update(self, dt_ms: float) -> None:
        """
        Advance the simulation timer and trigger ticks.

        Args:
            dt_ms: Time step delta in milliseconds.
        """
        if self.state.current_mode in (SimulationState.READY, SimulationState.PAUSED,
                                       SimulationState.MISSION_COMPLETE, SimulationState.MISSION_FAILED):
            return

        # Track total simulation elapsed time
        self.state.stats.simulation_time += dt_ms / 1000.0

        # Initialize grid helpers
        from app.map.grid import Grid
        grid_obj = Grid(self.state.width, self.state.height)
        grid_obj.cells = self.state.grid

        # 1. Fire tick accumulator check (fire intervals are time-based)
        self.accumulated_fire_time += dt_ms
        if self.accumulated_fire_time >= self.fire_interval:
            self.accumulated_fire_time -= self.fire_interval

            # Run deterministic fire propagation
            new_fire = spread_fire(grid_obj, self.state.fire_cells, self.state.stats.total_steps, self.state.stats)
            if new_fire:
                # Update risk map
                generate_heatmap(grid_obj, self.state.fire_cells)

                # Mandated Replanning check: if any coordinate in planned path is now on fire
                # or is blocked, clear current path cache to trigger path recalculation
                path_blocked = False
                for p in self.planned_path:
                    if grid_obj.cells[p.y][p.x].cell_type == CellType.FIRE:
                        path_blocked = True
                        break
                if path_blocked:
                    self.planned_path = []
                    self.state.stats.replans += 1
                    logger.info("Path blocked by spreading fire. Cleared path for replanning.")

            # Perform burn checks
            check_burn_entities(self.state.robot, self.state.victims, self.state.fire_cells, self.state.stats)
            self._check_mission_completion()

        # 2. Robot movement tick accumulator check
        self.accumulated_sim_time += dt_ms
        if self.accumulated_sim_time >= self.step_interval:
            self.accumulated_sim_time -= self.step_interval
            self.simulation_step()

    def simulation_step(self) -> None:
        """Execute a single simulation step (planning -> movement -> rescue checks)."""
        if self.state.current_mode in (SimulationState.READY, SimulationState.PAUSED,
                                       SimulationState.MISSION_COMPLETE, SimulationState.MISSION_FAILED):
            return

        # 1. Path Planning (Skip if manual USER_MODE)
        if self.state.current_mode != SimulationState.USER_MODE:
            # Check if path cache is empty or invalid
            path_is_valid = True
            if not self.planned_path:
                path_is_valid = False
            else:
                for p in self.planned_path:
                    # WALL or FIRE blocks movement
                    if self.state.grid[p.y][p.x].cell_type in (CellType.WALL, CellType.FIRE):
                        path_is_valid = False
                        break

            if not path_is_valid:
                target = self.select_target()
                if target is None:
                    # Remaining victims exist but none are reachable -> Fail
                    self.state.current_mode = SimulationState.MISSION_FAILED
                    logger.info("Failure: No reachable target remains.")
                    return

                path_res = self._find_path_to(target)
                if path_res.found:
                    self.planned_path = path_res.path
                    self.state.stats.replans += 1
                else:
                    self.state.current_mode = SimulationState.MISSION_FAILED
                    logger.info("Failure: Pathfinding failed to reach target.")
                    return

            # Move one step along the path
            if self.planned_path:
                next_pos = self.planned_path.pop(0)
                self._move_robot_entity(next_pos)

        # 2. Rescue checks
        # Pickup check
        picked_up = check_and_pickup(self.state.robot, self.state.victims)
        if picked_up:
            self.state.grid[picked_up.y][picked_up.x].cell_type = CellType.ROBOT
            self.planned_path = []  # Discard path to re-orient target to Rescue Station
            logger.info(f"Robot picked up Victim #{picked_up.victim_id} at ({picked_up.x}, {picked_up.y})")

        # Delivery check
        delivered = check_and_deliver(self.state.robot, self.state.victims, self.state.rescue_stations, self.state.stats)
        if delivered:
            self.state.grid[delivered.y][delivered.x].cell_type = CellType.ROBOT
            self.planned_path = []  # Discard path to search for next victim
            logger.info(f"Robot delivered Victim #{delivered.victim_id} to Rescue Station")

        # Double check burn checks (in case robot stepped into fire)
        check_burn_entities(self.state.robot, self.state.victims, self.state.fire_cells, self.state.stats)
        self._check_mission_completion()

    def move_robot_user(self, direction: tuple[int, int]) -> bool:
        """
        Manually step the robot in USER_MODE.

        Args:
            direction: The direction vector (dx, dy) to step.

        Returns:
            bool: True if move was completed successfully, False otherwise.
        """
        if self.state.current_mode != SimulationState.USER_MODE:
            return False

        from app.map.grid import Grid
        grid_obj = Grid(self.state.width, self.state.height)
        grid_obj.cells = self.state.grid

        next_pos = validate_and_move(grid_obj, self.state.robot.position, direction)
        if next_pos is not None:
            self._move_robot_entity(next_pos)

            # Pickup check
            picked_up = check_and_pickup(self.state.robot, self.state.victims)
            if picked_up:
                self.state.grid[picked_up.y][picked_up.x].cell_type = CellType.ROBOT

            # Delivery check
            delivered = check_and_deliver(self.state.robot, self.state.victims, self.state.rescue_stations, self.state.stats)
            if delivered:
                self.state.grid[delivered.y][delivered.x].cell_type = CellType.ROBOT

            check_burn_entities(self.state.robot, self.state.victims, self.state.fire_cells, self.state.stats)
            self._check_mission_completion()
            return True

        return False

    def select_target(self) -> Position | None:
        """
        Determine the next target position based on robot state (carrying vs seeking).

        Returns:
            Position | None: Target position or None if no valid target remains.
        """
        if self.state.robot.carrying_victim:
            # 1. Target is the closest rescue station
            candidates = []
            for station in self.state.rescue_stations:
                path_res = self._find_path_to(station.position)
                if path_res.found:
                    candidates.append((path_res.cost, station.station_id, station.position))

            if candidates:
                # Sort: cost ascending, station_id ascending
                candidates.sort(key=lambda item: (item[0], item[1]))
                return candidates[0][2]
            return None
        else:
            # 2. Target is the next best victim (waiting and alive)
            candidates = []
            for victim in self.state.victims:
                if victim.state == VictimState.WAITING and victim.alive:
                    path_res = self._find_path_to(victim.position)
                    if path_res.found:
                        # Tie break metrics
                        risk_sum = sum(self.state.grid[p.y][p.x].risk for p in path_res.path)
                        candidates.append((path_res.cost, risk_sum, victim.victim_id, victim.position))

            if candidates:
                # Sort: cost ascending, risk_sum ascending, victim_id ascending
                candidates.sort(key=lambda item: (item[0], item[1], item[2]))
                return candidates[0][3]
            return None

    def _find_path_to(self, goal: Position) -> PathResult:
        """Retrieve path from robot position to target using selected pathfinding algorithm."""
        from app.map.grid import Grid
        grid_obj = Grid(self.state.width, self.state.height)
        grid_obj.cells = self.state.grid

        algo = self.state.current_mode
        # Fallback to selected_algorithm string during READY or PAUSED state checks
        if algo not in PATHFINDERS:
            try:
                algo = SimulationState[self.state.selected_algorithm]
            except KeyError:
                algo = SimulationState.ASTAR

        pathfinder = PATHFINDERS.get(algo, astar_find_path)
        heatmap = [[cell.risk for cell in row] for row in self.state.grid]

        return pathfinder(grid_obj, self.state.robot.position, goal, heatmap)

    def _move_robot_entity(self, next_pos: Position) -> None:
        """Update coordinates and grid visual cells after robot steps."""
        robot = self.state.robot
        old_pos = robot.position

        # Determine cell type to restore old coordinate
        is_rescue = any(rs.position == old_pos for rs in self.state.rescue_stations)
        if is_rescue:
            self.state.grid[old_pos.y][old_pos.x].cell_type = CellType.RESCUE
        else:
            self.state.grid[old_pos.y][old_pos.x].cell_type = CellType.EMPTY

        # Update next position visual cell type
        self.state.grid[next_pos.y][next_pos.x].cell_type = CellType.ROBOT

        # Mutate robot model coordinates and step count
        robot.position = next_pos
        robot.steps += 1
        self.state.stats.total_steps += 1

    def _check_mission_completion(self) -> None:
        """Evaluate if the mission has reached a terminal success or failure state."""
        # 1. Failure: Robot dies
        if not self.state.robot.alive:
            self.state.current_mode = SimulationState.MISSION_FAILED
            logger.info("Mission Terminated: Robot burned.")
            return

        # 2. Success check
        waiting_count = sum(1 for v in self.state.victims if v.state == VictimState.WAITING)
        if waiting_count == 0 and not self.state.robot.carrying_victim:
            # If robot is alive and all victims were processed
            if self.state.stats.victims_saved > 0:
                self.state.current_mode = SimulationState.MISSION_COMPLETE
                logger.info("Mission Terminated: Success! All victims processed.")
            else:
                self.state.current_mode = SimulationState.MISSION_FAILED
                logger.info("Mission Terminated: Failure! No victims saved.")
            return

        # 3. Unreachable target checks (during AI execution)
        if self.state.current_mode != SimulationState.USER_MODE:
            target = self.select_target()
            if target is None:
                # Active targets exist, but none can be reached
                self.state.current_mode = SimulationState.MISSION_FAILED
                logger.info("Mission Terminated: Failure! Targets are unreachable.")
