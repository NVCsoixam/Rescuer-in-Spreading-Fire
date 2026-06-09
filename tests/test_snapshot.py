"""
tests/test_snapshot.py

Unit tests for the Snapshot system.
"""

from app.config import CellType, SimulationState, RobotState
from app.core.state import (
    Position, Cell, Robot, Victim, RescueStation, FireCell,
    SimulationStats, GameState
)
from app.core.snapshot import create_snapshot, restore_snapshot
from app.map.grid import Grid


def test_snapshot_deep_copy_isolation() -> None:
    """Test that creating and restoring snapshots clones state without shared references."""
    grid = Grid(10, 10)
    grid.set_cell(1, 1, CellType.WALL)

    robot = Robot(position=Position(2, 2), state=RobotState.IDLE)
    victims = [Victim(victim_id=1, position=Position(3, 3))]
    rescue_stations = [RescueStation(station_id=1, position=Position(4, 4))]
    fire_cells = [FireCell(position=Position(5, 5), ignition_step=0)]
    stats = SimulationStats(total_steps=10, simulation_time=5.0)

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

    # Create snapshot
    snapshot = create_snapshot(state)

    # Modify original state
    state.robot.position = Position(9, 9)
    state.stats.total_steps = 99
    state.victims[0].position = Position(0, 0)
    state.grid[1][1].cell_type = CellType.EMPTY

    # Restore state from snapshot
    restored = restore_snapshot(snapshot)

    # Assert original modifications did NOT leak into restored state
    assert restored.robot.position == Position(2, 2)
    assert restored.stats.total_steps == 10
    assert restored.victims[0].position == Position(3, 3)
    assert restored.grid[1][1].cell_type == CellType.WALL

    # Verify restored object is independent from the snapshot itself
    restored.robot.position = Position(8, 8)
    assert snapshot.robot.position == Position(2, 2)
