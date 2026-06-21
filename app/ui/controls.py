"""
app/ui/controls.py

Controls Handler for the 2D Rescue Simulation System.
Translates mouse clicks, dragging, and keyboard events into simulation state updates.
"""

from __future__ import annotations
import random
import pygame
from app.config import (
    CellType, SimulationState, EditTool,
    UP, DOWN, LEFT, RIGHT, GRID_MIN_SIZE, GRID_MAX_SIZE,
    VictimState, RobotState,
)
from app.core.state import Position, Victim, RescueStation, FireCell, GameState
from app.map.generator import MapGenerator
from app.core.engine import Engine
from app.ui.sidebar import Sidebar


class UIState:
    """Stores local presentation states for the graphical panel inputs."""

    def __init__(self) -> None:
        self.active_tool: EditTool = EditTool.WALL
        self.selected_size: int = 20
        self.size_dropdown_open: bool = False
        self.fire_interval_focused: bool = False
        self.fire_interval_text: str = "1000"
        self.show_path: bool = True  # Always show path (can't toggle via UI anymore)
        self.history_open: bool = False


def _apply_fire_interval(engine: Engine, ui_state: UIState) -> None:
    """Validate and apply typed fire interval to the simulation engine."""
    try:
        val = float(ui_state.fire_interval_text)
    except ValueError:
        val = 1000.0
    val = max(0.0, min(val, 10000.0))
    engine.fire_interval = val
    ui_state.fire_interval_text = str(int(val))


def _get_cell_from_mouse(
    mx: int, my: int, grid_w: int, grid_h: int,
    grid_width_px: int = 960, grid_height_px: int = 800,
) -> tuple[int, int] | None:
    """Convert mouse pixel coordinates to grid cell coordinates with correct padding offsets."""
    padding = 35  # Match the padding in GridRenderer
    usable_w = grid_width_px - 2 * padding
    usable_h = grid_height_px - 2 * padding

    if grid_w > 0 and grid_h > 0:
        cs = min(usable_w / grid_w, usable_h / grid_h)
        ox = padding + (usable_w - (grid_w * cs)) / 2
        oy = padding + (usable_h - (grid_h * cs)) / 2
        gx = int((mx - ox) / cs)
        gy = int((my - oy) / cs)
        if 0 <= gx < grid_w and 0 <= gy < grid_h:
            return gx, gy
    return None


def handle_events(
    events: list[pygame.event.Event],
    engine: Engine,
    sidebar: Sidebar,
    ui_state: UIState,
    map_generator: MapGenerator,
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

    for event in events:
        if event.type == pygame.QUIT:
            return False

        elif event.type == pygame.KEYDOWN:
            if ui_state.fire_interval_focused:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    ui_state.fire_interval_focused = False
                    _apply_fire_interval(engine, ui_state)
                elif event.key == pygame.K_BACKSPACE:
                    ui_state.fire_interval_text = ui_state.fire_interval_text[:-1]
                elif event.unicode.isdigit():
                    new_text = ui_state.fire_interval_text + event.unicode
                    try:
                        if int(new_text) <= 10000:
                            ui_state.fire_interval_text = new_text
                    except ValueError:
                        pass
                continue

            if event.key == pygame.K_ESCAPE:
                return False

            # USER_MODE arrow keys
            if state.current_mode == SimulationState.USER_MODE:
                direction_map = {
                    pygame.K_UP: UP,
                    pygame.K_DOWN: DOWN,
                    pygame.K_LEFT: LEFT,
                    pygame.K_RIGHT: RIGHT,
                }
                direction = direction_map.get(event.key)
                if direction is not None:
                    engine.move_robot_user(direction)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if ui_state.history_open:
                btn = sidebar.buttons.get("control_history")
                if not (btn and btn.collidepoint(event.pos)):
                    ui_state.history_open = False
                    continue # Consume click

            # Click in Grid Area
            if mx < 960:
                ui_state.size_dropdown_open = False
                if ui_state.fire_interval_focused:
                    ui_state.fire_interval_focused = False
                    _apply_fire_interval(engine, ui_state)

                if state.current_mode == SimulationState.READY:
                    cell = _get_cell_from_mouse(mx, my, grid_w, grid_h)
                    if cell is not None:
                        gx, gy = cell
                        if event.button == 1:  # Left click
                            _apply_tool(state, gx, gy, ui_state.active_tool)
                        elif event.button == 3:  # Right click = erase
                            _apply_tool(state, gx, gy, EditTool.ERASE)

            # Click in Sidebar Area
            else:
                _handle_sidebar_click(event, sidebar, engine, ui_state, map_generator, state)

        # Mouse drag handling for quick wall/erase
        elif event.type == pygame.MOUSEMOTION:
            if state.current_mode == SimulationState.READY:
                mx, my = event.pos
                if mx < 960:
                    cell = _get_cell_from_mouse(mx, my, grid_w, grid_h)
                    if cell is not None:
                        gx, gy = cell
                        buttons = pygame.mouse.get_pressed()
                        if buttons[0]:  # Left drag
                            if ui_state.active_tool in (EditTool.WALL, EditTool.ERASE):
                                _apply_tool(state, gx, gy, ui_state.active_tool)
                        elif buttons[2]:  # Right drag = erase
                            _apply_tool(state, gx, gy, EditTool.ERASE)

    return True


def _handle_sidebar_click(
    event, sidebar, engine, ui_state, map_generator, state
) -> None:
    """Process sidebar button clicks."""
    clicked_dropdown = False

    # Check dropdown options first
    if ui_state.size_dropdown_open:
        for size_opt in [10, 15, 20, 25, 30, 35]:
            opt_rect = sidebar.buttons.get(f"size_option_{size_opt}")
            if opt_rect and opt_rect.collidepoint(event.pos):
                ui_state.selected_size = size_opt
                ui_state.size_dropdown_open = False
                clicked_dropdown = True
                break

    if ui_state.size_dropdown_open and not clicked_dropdown:
        trigger = sidebar.buttons.get("size_dropdown_trigger")
        if not (trigger and trigger.collidepoint(event.pos)):
            ui_state.size_dropdown_open = False

    clicked_input = False
    input_rect = sidebar.buttons.get("fire_interval_input")
    if input_rect and input_rect.collidepoint(event.pos):
        clicked_input = True

    for name, rect in sidebar.buttons.items():
        if not rect.collidepoint(event.pos):
            continue

        # Dropdown
        if name == "size_dropdown_trigger":
            ui_state.size_dropdown_open = not ui_state.size_dropdown_open
            if ui_state.fire_interval_focused:
                ui_state.fire_interval_focused = False
                _apply_fire_interval(engine, ui_state)

        elif name == "fire_interval_input":
            ui_state.fire_interval_focused = True
            ui_state.size_dropdown_open = False
            ui_state.fire_interval_text = str(int(engine.fire_interval))

        elif name == "generate_map":
            if state.current_mode == SimulationState.READY:
                seed = random.randint(1, 100000)
                new_state = map_generator.generate(
                    width=ui_state.selected_size,
                    height=ui_state.selected_size,
                    seed=seed,
                )
                engine.set_state(new_state)
                ui_state.size_dropdown_open = False
                ui_state.fire_interval_focused = False
                _apply_fire_interval(engine, ui_state)

        elif name.startswith("tool_"):
            if state.current_mode == SimulationState.READY:
                tool_val = name.replace("tool_", "")
                ui_state.active_tool = EditTool(tool_val)
                ui_state.size_dropdown_open = False
                ui_state.fire_interval_focused = False
                _apply_fire_interval(engine, ui_state)

        elif name.startswith("run_"):
            ui_state.size_dropdown_open = False
            ui_state.fire_interval_focused = False
            _apply_fire_interval(engine, ui_state)
            mode_val = name.replace("run_", "")
            run_mode = SimulationState(mode_val)
            engine.state.selected_algorithm = run_mode.name
            engine.start(run_mode)

        elif name == "control_pause":
            ui_state.size_dropdown_open = False
            ui_state.fire_interval_focused = False
            _apply_fire_interval(engine, ui_state)
            if state.current_mode == SimulationState.PAUSED:
                engine.resume()
            else:
                engine.pause()

        elif name == "control_reset":
            ui_state.size_dropdown_open = False
            ui_state.fire_interval_focused = False
            _apply_fire_interval(engine, ui_state)
            engine.reset()
            
        elif name == "control_history":
            ui_state.size_dropdown_open = False
            ui_state.fire_interval_focused = False
            _apply_fire_interval(engine, ui_state)
            ui_state.history_open = not ui_state.history_open

    # Unfocus input if clicked outside
    if ui_state.fire_interval_focused and not clicked_input:
        ui_state.fire_interval_focused = False
        _apply_fire_interval(engine, ui_state)


def _apply_tool(state: GameState, x: int, y: int, tool: EditTool) -> None:
    """Modify coordinates and lists depending on selected Editor Mode tools."""
    target_pos = Position(x, y)
    # Mark map as manually edited so History can flag it
    state.map_edited = True

    # 1. Erase
    if tool == EditTool.ERASE:
        if state.robot.position == target_pos:
            return
        state.grid[y][x].cell_type = CellType.EMPTY
        state.victims = [v for v in state.victims if v.position != target_pos]
        state.fire_cells = [fc for fc in state.fire_cells if fc.position != target_pos]
        state.rescue_stations = [rs for rs in state.rescue_stations if rs.position != target_pos]

    # 2. Wall
    elif tool == EditTool.WALL:
        if state.robot.position == target_pos:
            return
        if any(v.position == target_pos for v in state.victims):
            return
        if any(rs.position == target_pos for rs in state.rescue_stations):
            return
        state.grid[y][x].cell_type = CellType.WALL
        state.fire_cells = [fc for fc in state.fire_cells if fc.position != target_pos]

    # 3. Robot
    elif tool == EditTool.ROBOT:
        if state.grid[y][x].cell_type not in (CellType.EMPTY, CellType.ROBOT):
            return
        ox, oy = state.robot.x, state.robot.y
        state.grid[oy][ox].cell_type = CellType.EMPTY
        state.robot.position = target_pos
        state.grid[y][x].cell_type = CellType.ROBOT

    # 4. Victim
    elif tool == EditTool.VICTIM:
        if state.grid[y][x].cell_type != CellType.EMPTY:
            return
        next_id = max((v.victim_id for v in state.victims), default=0) + 1
        new_victim = Victim(victim_id=next_id, position=target_pos, state=VictimState.WAITING)
        state.victims.append(new_victim)
        state.grid[y][x].cell_type = CellType.VICTIM

    # 5. Fire
    elif tool == EditTool.FIRE:
        if state.grid[y][x].cell_type in (CellType.WALL, CellType.ROBOT):
            return
        if any(fc.position == target_pos for fc in state.fire_cells):
            return
        # Remove entities that can't share cell with fire
        state.victims = [v for v in state.victims if v.position != target_pos]
        state.rescue_stations = [rs for rs in state.rescue_stations if rs.position != target_pos]
        new_fire = FireCell(position=target_pos, ignition_step=0)
        state.fire_cells.append(new_fire)
        state.grid[y][x].cell_type = CellType.FIRE

    # 6. Rescue Station
    elif tool == EditTool.RESCUE:
        if state.grid[y][x].cell_type != CellType.EMPTY:
            return
        next_id = max((rs.station_id for rs in state.rescue_stations), default=0) + 1
        new_station = RescueStation(station_id=next_id, position=target_pos)
        state.rescue_stations.append(new_station)
        state.grid[y][x].cell_type = CellType.RESCUE