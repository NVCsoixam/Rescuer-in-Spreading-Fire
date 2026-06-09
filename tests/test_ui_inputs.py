"""
tests/test_ui_inputs.py

Unit tests for UIState, dropdown logic, numeric text parsing, and engine auto-resets.
"""

import pygame
from app.config import CellType, SimulationState, RobotState, VictimState
from app.core.state import (
    Position, Cell, Robot, Victim, RescueStation, FireCell,
    SimulationStats, GameState
)
from app.core.engine import Engine
from app.ui.controls import UIState, handle_events, _apply_fire_interval
from app.ui.sidebar import Sidebar
from app.map.grid import Grid
from app.map.generator import MapGenerator


def test_uistate_initial_fields() -> None:
    """Verify default initialization fields of UIState."""
    ui = UIState()
    assert ui.selected_size == 20
    assert ui.size_dropdown_open is False
    assert ui.fire_interval_focused is False
    assert ui.fire_interval_text == "1000"


def test_apply_fire_interval_validation() -> None:
    """Verify custom numeric text inputs validation and clamping logic."""
    grid = Grid(10, 10)
    state = GameState(
        grid=grid.cells,
        robot=Robot(position=Position(1, 1)),
        victims=[],
        rescue_stations=[],
        fire_cells=[],
        stats=SimulationStats(),
        current_mode=SimulationState.READY,
        selected_algorithm="ASTAR"
    )
    engine = Engine(state)
    ui = UIState()

    # Normal value
    ui.fire_interval_text = "1500"
    _apply_fire_interval(engine, ui)
    assert engine.fire_interval == 1500.0
    assert ui.fire_interval_text == "1500"

    # Excess clamp
    ui.fire_interval_text = "25000"
    _apply_fire_interval(engine, ui)
    assert engine.fire_interval == 10000.0
    assert ui.fire_interval_text == "10000"

    # Negative clamp
    ui.fire_interval_text = "-500"
    _apply_fire_interval(engine, ui)
    assert engine.fire_interval == 0.0
    assert ui.fire_interval_text == "0"

    # Empty/garbage string fallback to 1000
    ui.fire_interval_text = "abc"
    _apply_fire_interval(engine, ui)
    assert engine.fire_interval == 1000.0
    assert ui.fire_interval_text == "1000"


def test_engine_auto_reset_on_algorithm_start() -> None:
    """Verify start() resets the engine first if current_mode is not READY."""
    grid = Grid(10, 10)
    grid.set_cell(2, 2, CellType.ROBOT)
    grid.set_cell(3, 3, CellType.VICTIM)
    grid.set_cell(4, 4, CellType.RESCUE)

    robot = Robot(position=Position(2, 2))
    victims = [Victim(victim_id=1, position=Position(3, 3))]
    rescue_stations = [RescueStation(station_id=1, position=Position(4, 4))]
    stats = SimulationStats()

    state = GameState(
        grid=grid.cells,
        robot=robot,
        victims=victims,
        rescue_stations=rescue_stations,
        fire_cells=[],
        stats=stats,
        current_mode=SimulationState.READY,
        selected_algorithm="ASTAR"
    )

    engine = Engine(state)
    engine.step_interval = 0.0

    # Start A*
    engine.start(SimulationState.ASTAR)
    assert engine.state.current_mode == SimulationState.ASTAR

    # Step robot along
    engine.simulation_step()
    # Robot should have moved from starting position (2,2)
    assert engine.state.robot.position != Position(2, 2)

    # Start BFS directly without manually clicking reset
    engine.start(SimulationState.BFS)
    # The start call should trigger auto-reset back to (2,2) and start BFS!
    assert engine.state.current_mode == SimulationState.BFS
    assert engine.state.robot.position == Position(2, 2)
