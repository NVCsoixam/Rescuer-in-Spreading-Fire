"""
app/ui/controls.py

Controls Handler for the 2D Rescue Simulation System.
Translates mouse clicks, dragging, and keyboard events into simulation state updates.
"""

import random
import pygame
from app.config import (
    CellType, SimulationState, EditTool, EnvironmentType, Complexity,
    UP, DOWN, LEFT, RIGHT, FIRE_SPEED_PRESETS, GRID_MIN_SIZE, GRID_MAX_SIZE
)
from app.core.state import Position, Robot, Victim, RescueStation, FireCell, GameState
from app.map.generator import MapGenerator
from app.core.engine import Engine
from app.ui.sidebar import Sidebar


class UIState:
    """Stores local presentation states for the graphical panel inputs."""

    def __init__(self) -> None:
        self.active_tool: EditTool = EditTool.WALL
        self.selected_size: int = 20
        self.selected_speed_name: str = "Normal"
        self.selected_env_type: EnvironmentType = EnvironmentType.HOSPITAL
        self.selected_complexity: Complexity = Complexity.MEDIUM
        self.show_path: bool = True
        self.show_risk: bool = True


def handle_events(
    events: list[pygame.event.Event],
    engine: Engine,
    sidebar: Sidebar,
    ui_state: UIState,
    map_generator: MapGenerator
) -> bool:
    """
    Process Pygame events and coordinate engine/state mutations.

    Args:
        events: List of captured window events.
        engine: The central simulation engine.
        sidebar: The sidebar renderer instance.
        ui_state: Local UI settings state wrapper.
        map_generator: Map generator instance for map regeneration commands.

    Returns:
        bool: True to continue running, False if a quit event is processed.
    """
    state = engine.state
    grid_w = state.width
    grid_h = state.height

    # Calculate grid viewport offsets
    cell_size = min(960 / grid_w, 800 / grid_h) if grid_w > 0 else 1
    offset_x = (960 - (grid_w * cell_size)) / 2
    offset_y = (800 - (grid_h * cell_size)) / 2

    # Map speed preset labels to values
    speed_presets_keys = list(FIRE_SPEED_PRESETS.keys())

    for event in events:
        if event.type == pygame.QUIT:
            return False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

            # In USER_MODE, arrow keys step the robot manually
            if state.current_mode == SimulationState.USER_MODE:
                direction = None
                if event.key == pygame.K_UP:
                    direction = UP
                elif event.key == pygame.K_DOWN:
                    direction = DOWN
                elif event.key == pygame.K_LEFT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    direction = RIGHT

                if direction is not None:
                    engine.move_robot_user(direction)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # 1. Click inside Grid Area -> Edit Map
            if mx < 960:
                if state.current_mode == SimulationState.READY:
                    # Translate mouse pixels to grid coordinates
                    gx = int((mx - offset_x) / cell_size)
                    gy = int((my - offset_y) / cell_size)

                    if 0 <= gx < grid_w and 0 <= gy < grid_h:
                        if event.button == 1:  # Left Click
                            _apply_tool(state, gx, gy, ui_state.active_tool)
                        elif event.button == 3:  # Right Click
                            _apply_tool(state, gx, gy, EditTool.ERASE)

            # 2. Click inside Sidebar Area -> Adjust Configs
            else:
                for name, rect in sidebar.buttons.items():
                    if rect.collidepoint(event.pos):
                        # Fire Interval speed adjustment
                        if name == "speed_prev":
                            idx = speed_presets_keys.index(ui_state.selected_speed_name)
                            ui_state.selected_speed_name = speed_presets_keys[(idx - 1) % len(speed_presets_keys)]
                            engine.fire_interval = float(FIRE_SPEED_PRESETS[ui_state.selected_speed_name])
                        elif name == "speed_next":
                            idx = speed_presets_keys.index(ui_state.selected_speed_name)
                            ui_state.selected_speed_name = speed_presets_keys[(idx + 1) % len(speed_presets_keys)]
                            engine.fire_interval = float(FIRE_SPEED_PRESETS[ui_state.selected_speed_name])

                        # Environment style selector
                        elif name == "env_prev":
                            envs = list(EnvironmentType)
                            idx = envs.index(ui_state.selected_env_type)
                            ui_state.selected_env_type = envs[(idx - 1) % len(envs)]
                        elif name == "env_next":
                            envs = list(EnvironmentType)
                            idx = envs.index(ui_state.selected_env_type)
                            ui_state.selected_env_type = envs[(idx + 1) % len(envs)]

                        # Generator complexity
                        elif name == "comp_prev":
                            comps = list(Complexity)
                            idx = comps.index(ui_state.selected_complexity)
                            ui_state.selected_complexity = comps[(idx - 1) % len(comps)]
                        elif name == "comp_next":
                            comps = list(Complexity)
                            idx = comps.index(ui_state.selected_complexity)
                            ui_state.selected_complexity = comps[(idx + 1) % len(comps)]

                        # Random Map Generation trigger
                        elif name == "generate_map":
                            if state.current_mode == SimulationState.READY:
                                seed = random.randint(1, 100000)
                                new_state = map_generator.generate(
                                    width=30,
                                    height=25,
                                    env_type=ui_state.selected_env_type,
                                    complexity=ui_state.selected_complexity,
                                    seed=seed
                                )
                                # Re-inject into engine and update initial snapshot
                                engine.set_state(new_state)

                        # Tool Selection toggles
                        elif name.startswith("tool_"):
                            tool_val = name.replace("tool_", "")
                            ui_state.active_tool = EditTool(tool_val)

                        # Execution Mode triggers
                        elif name.startswith("run_"):
                            mode_val = name.replace("run_", "")
                            run_mode = SimulationState(mode_val)
                            engine.state.selected_algorithm = run_mode.name
                            engine.start(run_mode)

                        # Pause / Resume and Reset
                        elif name == "control_pause":
                            if state.current_mode == SimulationState.PAUSED:
                                engine.resume()
                            else:
                                engine.pause()
                        elif name == "control_reset":
                            engine.reset()

        # Handle mouse drags for quick wall carving and erasing
        elif event.type == pygame.MOUSEMOTION:
            # Only allow edits in READY mode
            if state.current_mode == SimulationState.READY:
                mx, my = event.pos
                if mx < 960:
                    gx = int((mx - offset_x) / cell_size)
                    gy = int((my - offset_y) / cell_size)

                    if 0 <= gx < grid_w and 0 <= gy < grid_h:
                        buttons_pressed = pygame.mouse.get_pressed()
                        if buttons_pressed[0]:  # Left drag
                            if ui_state.active_tool == EditTool.WALL:
                                _apply_tool(state, gx, gy, EditTool.WALL)
                            elif ui_state.active_tool == EditTool.ERASE:
                                _apply_tool(state, gx, gy, EditTool.ERASE)
                        elif buttons_pressed[2]:  # Right drag
                            _apply_tool(state, gx, gy, EditTool.ERASE)

    return True


def _apply_tool(state: GameState, x: int, y: int, tool: EditTool) -> None:
    """Modify coordinates and lists depending on selected Editor Mode tools."""
    target_pos = Position(x, y)

    # 1. Erase tool: clears existing cells and drops entities located at position
    if tool == EditTool.ERASE:
        # Cannot erase the robot, since exactly 1 is required at all times
        if state.robot.position == target_pos:
            return

        state.grid[y][x].cell_type = CellType.EMPTY

        # Remove matching victim
        state.victims = [v for v in state.victims if v.position != target_pos]
        # Remove matching fire cell
        state.fire_cells = [fc for fc in state.fire_cells if fc.position != target_pos]
        # Remove matching rescue station
        state.rescue_stations = [rs for rs in state.rescue_stations if rs.position != target_pos]

    # 2. Wall tool
    elif tool == EditTool.WALL:
        # Don't place wall on robot, victims, or rescue stations to avoid overlaps
        if state.robot.position == target_pos:
            return
        if any(v.position == target_pos for v in state.victims):
            return
        if any(rs.position == target_pos for rs in state.rescue_stations):
            return

        state.grid[y][x].cell_type = CellType.WALL
        # Remove any fire at position
        state.fire_cells = [fc for fc in state.fire_cells if fc.position != target_pos]

    # 3. Robot tool: moves the robot start position
    elif tool == EditTool.ROBOT:
        # Position must be EMPTY to receive robot
        if state.grid[y][x].cell_type not in (CellType.EMPTY, CellType.ROBOT):
            return
        # Restore old position cell type
        ox, oy = state.robot.x, state.robot.y
        state.grid[oy][ox].cell_type = CellType.EMPTY
        # Relocate robot
        state.robot.position = target_pos
        state.grid[y][x].cell_type = CellType.ROBOT

    # 4. Victim tool: adds a victim
    elif tool == EditTool.VICTIM:
        # Cell must be EMPTY to place a victim
        if state.grid[y][x].cell_type != CellType.EMPTY:
            return
        # Assign next valid unique ID
        next_id = max([v.victim_id for v in state.victims]) + 1 if state.victims else 1
        new_victim = Victim(victim_id=next_id, position=target_pos, state=VictimState.WAITING)
        state.victims.append(new_victim)
        state.grid[y][x].cell_type = CellType.VICTIM

    # 5. Fire tool: ignites cell
    elif tool == EditTool.FIRE:
        # Cannot ignite walls or robot
        if state.grid[y][x].cell_type in (CellType.WALL, CellType.ROBOT):
            return
        # Avoid duplicate additions
        if any(fc.position == target_pos for fc in state.fire_cells):
            return
        # Remove any victim or rescue station located at coordinate
        state.victims = [v for v in state.victims if v.position != target_pos]
        state.rescue_stations = [rs for rs in state.rescue_stations if rs.position != target_pos]

        new_fire = FireCell(position=target_pos, ignition_step=0)
        state.fire_cells.append(new_fire)
        state.grid[y][x].cell_type = CellType.FIRE

    # 6. Rescue Station tool
    elif tool == EditTool.RESCUE:
        # Position must be EMPTY
        if state.grid[y][x].cell_type != CellType.EMPTY:
            return
        next_id = max([rs.station_id for rs in state.rescue_stations]) + 1 if state.rescue_stations else 1
        new_station = RescueStation(station_id=next_id, position=target_pos)
        state.rescue_stations.append(new_station)
        state.grid[y][x].cell_type = CellType.RESCUE
