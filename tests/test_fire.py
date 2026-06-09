"""
tests/test_fire.py

Unit tests for the fire simulation (spread and burning mechanics).
"""

from app.config import CellType, RobotState, VictimState
from app.core.state import Position, Robot, Victim, FireCell, SimulationStats
from app.map.grid import Grid
from app.fire.fire_sim import spread_fire, check_burn_entities


def test_fire_spread_logic() -> None:
    """Test fire spreads to adjacent empty cells but is blocked by walls."""
    grid = Grid(10, 10)
    stats = SimulationStats()

    # Initial fire source in center
    fire_cells = [FireCell(position=Position(5, 5), ignition_step=0)]
    grid.set_cell(5, 5, CellType.FIRE)

    # Set up wall blocking one side
    grid.set_cell(5, 4, CellType.WALL)  # Block UP

    new_fires = spread_fire(grid, fire_cells, current_step=1, stats=stats)

    # Fire should spread to RIGHT (6,5), DOWN (5,6), LEFT (4,5) but not UP (5,4)
    assert len(new_fires) == 3
    assert len(fire_cells) == 4
    assert stats.fire_spread_events == 1

    assert grid.cells[5][4].cell_type == CellType.FIRE  # LEFT
    assert grid.cells[5][6].cell_type == CellType.FIRE  # RIGHT
    assert grid.cells[6][5].cell_type == CellType.FIRE  # DOWN
    assert grid.cells[4][5].cell_type == CellType.WALL  # UP (WALL-blocked)


def test_robot_burns() -> None:
    """Test robot dies when entering a fire cell."""
    robot = Robot(position=Position(5, 5), state=RobotState.MOVING)
    victims = [Victim(victim_id=1, position=Position(5, 5), state=VictimState.CARRIED)]
    fire_cells = [FireCell(position=Position(5, 5), ignition_step=0)]
    stats = SimulationStats()

    # Set robot to be carrying victim 1
    robot.carrying_victim = True
    robot.carried_victim_id = 1

    check_burn_entities(robot, victims, fire_cells, stats)

    assert robot.alive is False
    assert robot.state == RobotState.DEAD
    # Carried victim should die too
    assert victims[0].alive is False
    assert victims[0].state == VictimState.DEAD
    assert stats.victims_dead == 1


def test_victim_burns() -> None:
    """Test waiting victim dies when caught in fire."""
    robot = Robot(position=Position(0, 0), state=RobotState.MOVING)
    victims = [
        # Waiting victim at (5,5)
        Victim(victim_id=1, position=Position(5, 5), state=VictimState.WAITING),
        # Rescued victim at (4,4) - should be safe
        Victim(victim_id=2, position=Position(4, 4), state=VictimState.RESCUED)
    ]
    fire_cells = [FireCell(position=Position(5, 5), ignition_step=0)]
    stats = SimulationStats()

    check_burn_entities(robot, victims, fire_cells, stats)

    assert victims[0].alive is False
    assert victims[0].state == VictimState.DEAD
    assert stats.victims_dead == 1

    # Rescued victim remains unaffected
    assert victims[1].alive is True
    assert victims[1].state == VictimState.RESCUED
