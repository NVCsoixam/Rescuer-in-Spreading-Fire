"""
app/core/engine.py

Core Simulation Engine for the 2D Rescue Simulation System.
Coordinates lifecycle states, ticks, movement, rescue mechanics, fire spread, and AI pathfinding.
"""

from __future__ import annotations
import logging
from dataclasses import dataclass, field
from app.config import CellType, SimulationState, RobotState, VictimState, FIRE_INTERVAL_DEFAULT
from app.core.state import Position, GameState, PathResult
from app.map.grid import Grid
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
    SimulationState.ASTAR: astar_find_path,
}

# States that are idle (non-running)
IDLE_STATES = frozenset({
    SimulationState.READY,
    SimulationState.PAUSED,
    SimulationState.MISSION_COMPLETE,
    SimulationState.MISSION_FAILED,
})


@dataclass
class _PathCacheEntry:
    """Internal path cache entry with timestamp for invalidation."""
    goal: Position
    result: PathResult
    fire_step: int


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
        self._grid_cache: Grid | None = None
        self._path_cache: _PathCacheEntry | None = None
        self._is_running: bool = False
        self._last_fire_spread_step: int = -1

        # Ticking controls (in milliseconds)
        self.fire_interval: float = float(FIRE_INTERVAL_DEFAULT)
        self.step_interval: float = 200.0  # Robot moves every 200ms

        self.accumulated_fire_time: float = 0.0
        self.accumulated_sim_time: float = 0.0
        self.prev_mode: SimulationState = SimulationState.READY

    # ── Grid helpers ──────────────────────────────────────────────

    def _get_grid(self) -> Grid:
        """Get or create a cached Grid wrapper around current state cells."""
        if self._grid_cache is None:
            self._grid_cache = Grid(self.state.width, self.state.height)
        self._grid_cache.cells = self.state.grid
        return self._grid_cache

    def _invalidate_caches(self) -> None:
        """Invalidate all internal caches."""
        self._grid_cache = None
        self._path_cache = None
        self.planned_path = []

    # ── State Management ──────────────────────────────────────────

    def is_idle(self) -> bool:
        """Check if the simulation is in an idle (non-running) state."""
        return self.state.current_mode in IDLE_STATES

    def is_running(self) -> bool:
        """Check if the simulation is actively running."""
        return not self.is_idle() and self._is_running

    def set_state(self, new_state: GameState) -> None:
        """
        Set a new GameState and update the initial snapshot.

        Args:
            new_state: The new GameState object.
        """
        self.state = new_state
        self._invalidate_caches()
        self.snapshot = create_snapshot(new_state)
        self.accumulated_fire_time = 0.0
        self.accumulated_sim_time = 0.0
        self._is_running = False

    # ── Simulation Lifecycle ──────────────────────────────────────

    def start(self, mode: SimulationState) -> bool:
        """
        Start the simulation in the specified execution mode.

        Args:
            mode: The selected running mode (e.g. BFS, ASTAR, USER_MODE).

        Returns:
            bool: True if started successfully, False otherwise.
        """
        # If not in READY, reset to the original snapshot first
        if self.state.current_mode not in IDLE_STATES:
            self.reset()
        elif self.state.current_mode == SimulationState.PAUSED:
            self.state.current_mode = self.prev_mode
            return True

        # Take snapshot of current state before mutating
        self.snapshot = create_snapshot(self.state)
        self.state.current_mode = mode
        self.prev_mode = mode

        # Reset accumulators and caches
        self._invalidate_caches()
        self.accumulated_fire_time = 0.0
        self.accumulated_sim_time = 0.0
        self._is_running = True
        self._last_fire_spread_step = -1

        # Initialize heatmap based on start positions of fire
        grid_obj = self._get_grid()
        generate_heatmap(grid_obj, self.state.fire_cells)

        logger.info(f"Simulation started in mode: {mode.value}")
        return True

    def pause(self) -> None:
        """Pause the running simulation."""
        if self.state.current_mode not in IDLE_STATES:
            self.prev_mode = self.state.current_mode
            self.state.current_mode = SimulationState.PAUSED
            self._is_running = False
            logger.info("Simulation paused.")

    def resume(self) -> None:
        """Resume the paused simulation."""
        if self.state.current_mode == SimulationState.PAUSED:
            self.state.current_mode = self.prev_mode
            self._is_running = True
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

            # Clear all cached state
            self._invalidate_caches()
            self.accumulated_fire_time = 0.0
            self.accumulated_sim_time = 0.0
            self._is_running = False
            self._last_fire_spread_step = -1

            # Recalculate heatmap on reset to ensure UI risk levels are correct
            grid_obj = self._get_grid()
            generate_heatmap(grid_obj, self.state.fire_cells)

            logger.info("Simulation state reset to initial snapshot.")

    # ── Main Update Loop ──────────────────────────────────────────

    def update(self, dt_ms: float) -> None:
        """
        Advance the simulation timer and trigger ticks.

        Args:
            dt_ms: Time step delta in milliseconds.
        """
        if self.state.current_mode in IDLE_STATES or not self._is_running:
            return

        # Track total simulation elapsed time
        self.state.stats.simulation_time += dt_ms / 1000.0

        # 1. Fire tick accumulator
        self._fire_tick(dt_ms)

        # 2. Robot movement tick accumulator
        self.accumulated_sim_time += dt_ms
        if self.accumulated_sim_time >= self.step_interval:
            self.accumulated_sim_time -= self.step_interval
            self.simulation_step()

    def _fire_tick(self, dt_ms: float) -> None:
        """Handle fire propagation timing and execution."""
        self.accumulated_fire_time += dt_ms
        if self.accumulated_fire_time < self.fire_interval:
            return
        self.accumulated_fire_time -= self.fire_interval

        grid_obj = self._get_grid()

        # Run deterministic fire propagation
        new_fire = spread_fire(
            grid_obj,
            self.state.fire_cells,
            self.state.stats.total_steps,
            self.state.stats,
        )
        if new_fire:
            # Update risk map
            generate_heatmap(grid_obj, self.state.fire_cells)
            self._last_fire_spread_step = self.state.stats.total_steps

            # Check if planned path is blocked by new fire
            path_blocked = any(
                grid_obj.cells[p.y][p.x].cell_type == CellType.FIRE
                for p in self.planned_path
            )
            if path_blocked:
                self.planned_path = []
                self._path_cache = None
                self.state.stats.replans += 1
                logger.info("Path blocked by spreading fire. Cleared path for replanning.")

        # Perform burn checks on all entities
        check_burn_entities(self.state.robot, self.state.victims, self.state.fire_cells, self.state.stats)
        self._check_mission_completion()

    def simulation_step(self) -> None:
        """Execute a single simulation step (planning -> movement -> rescue checks)."""
        if self.state.current_mode in IDLE_STATES:
            return

        # 1. Path Planning (Skip if manual USER_MODE)
        if self.state.current_mode != SimulationState.USER_MODE:
            self._plan_and_move()

        # 2. Rescue checks (pickup/delivery)
        self._process_rescue_actions()

        # 3. Final burn check after movement
        check_burn_entities(self.state.robot, self.state.victims, self.state.fire_cells, self.state.stats)
        self._check_mission_completion()

    def _plan_and_move(self) -> None:
        """Plan path and move robot one step along it."""
        # Validate current path cache
        path_valid = self._validate_path()

        if not path_valid:
            # Select best target and find path
            target = self.select_target()
            if target is None:
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

    def _validate_path(self) -> bool:
        """Check if the current planned path is still valid."""
        if not self.planned_path:
            return False
        for p in self.planned_path:
            cell_type = self.state.grid[p.y][p.x].cell_type
            if cell_type in (CellType.WALL, CellType.FIRE):
                return False
        return True

    def _process_rescue_actions(self) -> None:
        """Handle pickup and delivery checks after movement."""
        # Pickup check
        picked_up = check_and_pickup(self.state.robot, self.state.victims)
        if picked_up is not None:
            self.state.grid[picked_up.y][picked_up.x].cell_type = CellType.ROBOT
            self.planned_path = []  # Re-route to rescue station
            self._path_cache = None
            logger.info(
                f"Robot picked up Victim #{picked_up.victim_id} "
                f"at ({picked_up.x}, {picked_up.y})"
            )

        # Delivery check
        delivered = check_and_deliver(
            self.state.robot,
            self.state.victims,
            self.state.rescue_stations,
            self.state.stats,
        )
        if delivered is not None:
            self.state.grid[delivered.y][delivered.x].cell_type = CellType.ROBOT
            self.planned_path = []  # Search for next victim
            self._path_cache = None
            logger.info(
                f"Robot delivered Victim #{delivered.victim_id} to Rescue Station"
            )

    # ── Manual User Movement ──────────────────────────────────────

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

        grid_obj = self._get_grid()
        next_pos = validate_and_move(grid_obj, self.state.robot.position, direction)

        if next_pos is None:
            return False

        self._move_robot_entity(next_pos)

        # Pickup check
        picked_up = check_and_pickup(self.state.robot, self.state.victims)
        if picked_up is not None:
            self.state.grid[picked_up.y][picked_up.x].cell_type = CellType.ROBOT

        # Delivery check
        delivered = check_and_deliver(
            self.state.robot,
            self.state.victims,
            self.state.rescue_stations,
            self.state.stats,
        )
        if delivered is not None:
            self.state.grid[delivered.y][delivered.x].cell_type = CellType.ROBOT

        check_burn_entities(self.state.robot, self.state.victims, self.state.fire_cells, self.state.stats)
        self._check_mission_completion()
        return True

    # ── Target Selection ──────────────────────────────────────────

    def _get_fire_distances(self) -> dict[tuple[int, int], int]:
        """Run a multi-source BFS from all fire cells to find the shortest distance (in steps) to each cell."""
        fire_dists: dict[tuple[int, int], int] = {}
        queue: list[Position] = []
        for fc in self.state.fire_cells:
            fire_dists[(fc.position.x, fc.position.y)] = 0
            queue.append(fc.position)

        head = 0
        grid_obj = self._get_grid()
        while head < len(queue):
            curr = queue[head]
            head += 1
            curr_dist = fire_dists[(curr.x, curr.y)]

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = curr.x + dx, curr.y + dy
                if grid_obj.in_bounds(nx, ny):
                    if grid_obj.cells[ny][nx].cell_type != CellType.WALL:
                        if (nx, ny) not in fire_dists:
                            fire_dists[(nx, ny)] = curr_dist + 1
                            queue.append(Position(nx, ny))
        return fire_dists

    def select_target(self) -> Position | None:
        """
        Determine the next target position based on robot state (carrying vs seeking).

        If seeking and no salvageable victim remains, plans a path back to a rescue station.

        Returns:
            Position | None: Target position or None if no valid target/exit remains.
        """
        if self.state.robot.carrying_victim:
            return self._select_rescue_station_target()
        
        victim_target = self._select_victim_target()
        if victim_target is not None:
            return victim_target
            
        # Exit strategy: no salvageable victims left, return to exit
        return self._select_rescue_station_target()

    def _select_rescue_station_target(self) -> Position | None:
        """Select closest rescue station when carrying a victim or returning to exit."""
        candidates: list[tuple[float, int, Position]] = []
        for station in self.state.rescue_stations:
            path_res = self._find_path_to(station.position)
            if path_res.found:
                candidates.append((path_res.cost, station.station_id, station.position))

        if not candidates:
            return None
        candidates.sort(key=lambda item: (item[0], item[1]))
        return candidates[0][2]

    def _select_victim_target(self) -> Position | None:
        """Select closest, salvageable victim prioritizing those closest to fire."""
        fire_dists = self._get_fire_distances()
        if self.step_interval == 0.0:
            speed_ratio = 999999.0
        else:
            speed_ratio = self.fire_interval / self.step_interval

        candidates: list[tuple[float, float, float, int, Position]] = []
        for victim in self.state.victims:
            if victim.is_active():
                path_res = self._find_path_to(victim.position)
                if path_res.found:
                    steps_to = len(path_res.path)
                    fire_dist = fire_dists.get((victim.x, victim.y), 999999)
                    steps_survival = fire_dist * speed_ratio

                    # Can the robot reach the victim before fire does?
                    if steps_to < steps_survival:
                        # Calculate risk sum along the path
                        risk_sum = sum(
                            self.state.grid[p.y][p.x].risk for p in path_res.path
                        )
                        # Sorting criteria:
                        # 1. steps_survival asc (closer to dying first)
                        # 2. steps_to asc (closer to robot next)
                        # 3. risk_sum asc
                        # 4. victim_id asc (tie-breaker)
                        candidates.append(
                            (steps_survival, steps_to, risk_sum, victim.victim_id, victim.position)
                        )

        if not candidates:
            return None
        # Sort by: steps_survival, steps_to, risk_sum, victim_id
        candidates.sort(key=lambda item: (item[0], item[1], item[2], item[3]))
        return candidates[0][4]

    # ── Pathfinding ───────────────────────────────────────────────

    def _find_path_to(self, goal: Position) -> PathResult:
        """
        Find path from robot position to target using selected pathfinding algorithm.

        Results are cached to avoid redundant computation unless fire has spread.
        """
        robot_pos = self.state.robot.position

        # Cache check: if goal and fire step haven't changed, reuse cached result
        if (
            self._path_cache is not None
            and self._path_cache.goal == goal
            and self._path_cache.fire_step == self._last_fire_spread_step
        ):
            return self._path_cache.result

        grid_obj = self._get_grid()

        # Determine algorithm
        algo = self.state.current_mode
        if algo not in PATHFINDERS:
            try:
                algo = SimulationState[self.state.selected_algorithm]
            except (KeyError, ValueError):
                algo = SimulationState.ASTAR

        pathfinder = PATHFINDERS.get(algo, astar_find_path)
        heatmap = [[cell.risk for cell in row] for row in self.state.grid]

        result = pathfinder(grid_obj, robot_pos, goal, heatmap)

        self.state.stats.computation_time_ms += result.execution_time_ms
        self.state.stats.expanded_nodes += result.expanded_nodes

        # Cache the result
        self._path_cache = _PathCacheEntry(
            goal=goal,
            result=result,
            fire_step=self._last_fire_spread_step,
        )

        return result

    # ── Robot Movement ────────────────────────────────────────────

    def _move_robot_entity(self, next_pos: Position) -> None:
        """Update coordinates and grid visual cells after robot steps."""
        robot = self.state.robot
        old_pos = robot.position

        # Determine cell type to restore at old position
        is_rescue = any(rs.position == old_pos for rs in self.state.rescue_stations)
        if is_rescue:
            self.state.grid[old_pos.y][old_pos.x].cell_type = CellType.RESCUE
        else:
            self.state.grid[old_pos.y][old_pos.x].cell_type = CellType.EMPTY

        # Set new position as robot
        self.state.grid[next_pos.y][next_pos.x].cell_type = CellType.ROBOT

        # Update robot position and step count
        robot.move_to(next_pos)
        self.state.stats.total_steps += 1

    # ── Mission Completion Checks ─────────────────────────────────

    def _check_mission_completion(self) -> None:
        """Evaluate if the mission has reached a terminal success or failure state."""
        state = self.state

        # 1. Failure: Robot is dead
        if not state.robot.alive:
            state.current_mode = SimulationState.MISSION_FAILED
            logger.info("Mission Terminated: Robot burned.")
            return

        # 2. Check if all victims are processed (no waiting and no carrying)
        waiting_count = state.remaining_victims
        if waiting_count == 0 and not state.robot.carrying_victim:
            if state.saved_count > 0:
                state.current_mode = SimulationState.MISSION_COMPLETE
                logger.info(
                    f"Mission Complete! Saved {state.saved_count}/{state.total_victims} victims."
                )
            else:
                state.current_mode = SimulationState.MISSION_FAILED
                logger.info("Mission Failed: No victims were saved.")
            return

        # 3. Check exit status and target accessibility during AI execution
        if state.current_mode != SimulationState.USER_MODE:
            is_at_station = any(rs.position == state.robot.position for rs in state.rescue_stations)
            no_salvageable_victims = (self._select_victim_target() is None)

            # If robot is at station, no salvageable victims exist, and not carrying
            if is_at_station and no_salvageable_victims and not state.robot.carrying_victim:
                if state.saved_count > 0:
                    state.current_mode = SimulationState.MISSION_COMPLETE
                    logger.info(
                        f"Mission Complete! Robot returned to exit. Saved {state.saved_count}/{state.total_victims} victims."
                    )
                else:
                    state.current_mode = SimulationState.MISSION_FAILED
                    logger.info("Mission Failed: Robot returned to exit but saved 0 victims.")
                return

            # If no target can be selected (neither a victim to save nor an exit to return to)
            target = self.select_target()
            if target is None:
                state.current_mode = SimulationState.MISSION_FAILED
                logger.info("Mission Failed: Robot is trapped with no reachable targets or exits.")