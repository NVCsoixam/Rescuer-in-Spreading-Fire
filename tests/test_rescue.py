"""
tests/test_rescue.py

Unit tests for rescue mechanics (pickup & delivery).
"""

from app.config import RobotState, VictimState
from app.core.state import Position, Robot, Victim, RescueStation, SimulationStats
from app.logic.rescue import check_and_pickup, check_and_deliver


def test_pickup_success() -> None:
    """Test picking up a victim successfully."""
    robot = Robot(position=Position(3, 3), state=RobotState.IDLE)
    victims = [
        Victim(victim_id=1, position=Position(3, 3), state=VictimState.WAITING),
        Victim(victim_id=2, position=Position(5, 5), state=VictimState.WAITING)
    ]

    picked = check_and_pickup(robot, victims)
    assert picked is not None
    assert picked.victim_id == 1
    assert picked.state == VictimState.CARRIED

    assert robot.carrying_victim is True
    assert robot.carried_victim_id == 1
    assert robot.state == RobotState.CARRYING


def test_pickup_already_carrying() -> None:
    """Test pickup is blocked if robot is already carrying a victim."""
    robot = Robot(position=Position(3, 3), state=RobotState.CARRYING, carrying_victim=True, carried_victim_id=2)
    victims = [
        Victim(victim_id=1, position=Position(3, 3), state=VictimState.WAITING)
    ]

    picked = check_and_pickup(robot, victims)
    assert picked is None


def test_delivery_success() -> None:
    """Test delivering a carried victim to a rescue station."""
    robot = Robot(position=Position(4, 4), state=RobotState.CARRYING, carrying_victim=True, carried_victim_id=1)
    victims = [
        Victim(victim_id=1, position=Position(4, 4), state=VictimState.CARRIED)
    ]
    rescue_stations = [
        RescueStation(station_id=1, position=Position(4, 4))
    ]
    stats = SimulationStats()

    delivered = check_and_deliver(robot, victims, rescue_stations, stats)
    assert delivered is not None
    assert delivered.victim_id == 1
    assert delivered.state == VictimState.RESCUED
    assert delivered.rescued is True

    assert robot.carrying_victim is False
    assert robot.carried_victim_id is None
    assert robot.state == RobotState.MOVING
    assert stats.victims_saved == 1


def test_delivery_wrong_position() -> None:
    """Test delivery does not occur if robot is not on a rescue station."""
    robot = Robot(position=Position(3, 3), state=RobotState.CARRYING, carrying_victim=True, carried_victim_id=1)
    victims = [
        Victim(victim_id=1, position=Position(3, 3), state=VictimState.CARRIED)
    ]
    rescue_stations = [
        RescueStation(station_id=1, position=Position(4, 4))
    ]
    stats = SimulationStats()

    delivered = check_and_deliver(robot, victims, rescue_stations, stats)
    assert delivered is None
    assert stats.victims_saved == 0
