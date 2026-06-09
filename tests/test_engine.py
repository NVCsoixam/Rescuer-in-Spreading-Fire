"""
tests/test_engine.py

Integration tests for the core Engine, simulation loop, and replanning triggers.
"""

from app.config import CellType, SimulationState, RobotState, VictimState
from app.core.state import (
    Position, Cell, Robot, Victim, RescueStation, FireCell,
    SimulationStats, GameState
)
from app.core.engine import Engine
from app.map.grid import Grid


def test_engine_lifecycle_success() -> None:
    """Test start, pause, resume, reset, and successful mission completion."""
    grid = Grid(10, 10)
    grid.set_cell(2, 2, CellType.ROBOT)
    grid.set_cell(3, 3, CellType.VICTIM)
    grid.set_cell(4, 4, CellType.RESCUE)
    grid.set_cell(9, 9, CellType.FIRE)  # Safe distant fire

    robot = Robot(position=Position(2, 2))
    victims = [Victim(victim_id=1, position=Position(3, 3))]
    rescue_stations = [RescueStation(station_id=1, position=Position(4, 4))]
    fire_cells = [FireCell(position=Position(9, 9), ignition_step=0)]
    stats = SimulationStats()

    state = GameState(
        grid=grid.cells,
        robot=robot,
        victims=victims,
        rescue_stations=rescue_stations,
        fire_cells=fire_cells,
        stats=stats,
        current_mode=SimulationState.READY,
        selected_algorithm="ASTAR"
    )

    engine = Engine(state)
    engine.step_interval = 0.0  # Instant moves for testing
    engine.fire_interval = 10000.0  # Slow fire

    # 1. Start simulation
    assert engine.start(SimulationState.ASTAR) is True
    assert engine.state.current_mode == SimulationState.ASTAR
    assert engine.snapshot is not None

    # 2. Pause and Resume
    engine.pause()
    assert engine.state.current_mode == SimulationState.PAUSED
    engine.resume()
    assert engine.state.current_mode == SimulationState.ASTAR

    # 3. Step simulation (Robot moves to (3,3) and picks up victim - requires 2 steps)
    engine.simulation_step()  # Step 1: Moves to intermediate cell (3,2) or (2,3)
    assert engine.state.robot.carrying_victim is False
    engine.simulation_step()  # Step 2: Moves to (3,3) and picks up victim
    assert engine.state.robot.position == Position(3, 3)
    assert engine.state.robot.carrying_victim is True

    # 4. Step simulation (Robot moves to (4,4) and drops off victim - requires 2 steps)
    engine.simulation_step()  # Step 3: Moves to intermediate cell
    assert engine.state.robot.carrying_victim is True
    engine.simulation_step()  # Step 4: Moves to (4,4) and drops off
    assert engine.state.robot.position == Position(4, 4)
    assert engine.state.robot.carrying_victim is False
    assert engine.state.stats.victims_saved == 1
    assert engine.state.current_mode == SimulationState.MISSION_COMPLETE

    # 5. Reset simulation
    engine.reset()
    assert engine.state.current_mode == SimulationState.READY
    assert engine.state.robot.position == Position(2, 2)
    assert engine.state.stats.victims_saved == 0


def test_engine_replanning_on_fire_block() -> None:
    """Test that spreading fire blocking the path triggers replanning."""
    grid = Grid(10, 10)
    grid.set_cell(2, 2, CellType.ROBOT)
    grid.set_cell(2, 4, CellType.VICTIM)
    # Rescue station
    grid.set_cell(2, 5, CellType.RESCUE)

    # Initial Fire source adjacent to goal (so spreading will block the goal cell)
    grid.set_cell(3, 4, CellType.FIRE)

    robot = Robot(position=Position(2, 2))
    victims = [Victim(victim_id=1, position=Position(2, 4))]
    rescue_stations = [RescueStation(station_id=1, position=Position(2, 5))]
    fire_cells = [FireCell(position=Position(3, 4), ignition_step=0)]
    stats = SimulationStats()

    state = GameState(
        grid=grid.cells,
        robot=robot,
        victims=victims,
        rescue_stations=rescue_stations,
        fire_cells=fire_cells,
        stats=stats,
        current_mode=SimulationState.READY,
        selected_algorithm="ASTAR"
    )

    engine = Engine(state)
    engine.step_interval = 10000.0  # Slow step
    engine.fire_interval = 0.0  # Instant fire spread on update

    engine.start(SimulationState.ASTAR)

    # Trigger planning path (BFS/A* plans from (2,2) to (2,4) via (2,3) -> (2,4))
    engine.simulation_step()
    assert len(engine.planned_path) > 0  # Path should contain (2,4) remaining

    # Run update with dt to trigger fire tick
    # Fire spreads from (3,4) to (2,4) - which is on the robot's remaining planned path!
    engine.update(100.0)

    # Verify fire spread occurred
    assert any(fc.position == Position(2, 4) for fc in engine.state.fire_cells)
    # Check that path was cleared for replanning
    assert len(engine.planned_path) == 0
    # Steps stats should register a replan increment
    assert engine.state.stats.replans > 0
