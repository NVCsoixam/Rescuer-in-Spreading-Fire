"""
app/logic/rescue.py

Pickup and delivery mechanics for the rescue simulation.
Defines entity state transitions when the robot interacts with victims and rescue stations.
"""

from __future__ import annotations
from app.config import RobotState, VictimState
from app.core.state import Robot, Victim, RescueStation, SimulationStats


def check_and_pickup(robot: Robot, victims: list[Victim]) -> Victim | None:
    """
    Check if the robot is on a victim and can pick them up.
    Robot can only carry 1 victim at a time.

    Args:
        robot: The robot entity.
        victims: The list of victims in the simulation.

    Returns:
        Victim | None: The Victim that was picked up, or None if no pickup occurred.
    """
    if robot is None or victims is None:
        return None

    if robot.carrying_victim or not robot.alive:
        return None

    for victim in victims:
        if victim.is_active() and victim.position == robot.position:
            # Perform pickup transitions using domain methods
            robot.pickup(victim.victim_id)
            victim.state = VictimState.CARRIED
            return victim

    return None


def check_and_deliver(
    robot: Robot,
    victims: list[Victim],
    rescue_stations: list[RescueStation],
    stats: SimulationStats,
) -> Victim | None:
    """
    Check if the robot is carrying a victim and has reached a rescue station.

    Args:
        robot: The robot entity.
        victims: The list of victims in the simulation.
        rescue_stations: The list of rescue stations.
        stats: The statistics object to update on successful delivery.

    Returns:
        Victim | None: The Victim that was successfully delivered, or None.
    """
    if robot is None or victims is None or rescue_stations is None or stats is None:
        return None

    if not robot.carrying_victim or not robot.alive or robot.carried_victim_id is None:
        return None

    # Verify if robot is standing on any rescue station
    on_station = any(station.position == robot.position for station in rescue_stations)
    if not on_station:
        return None

    # Find the carried victim and complete delivery
    for victim in victims:
        if victim.victim_id == robot.carried_victim_id and victim.state == VictimState.CARRIED:
            # Perform delivery transitions using domain methods
            victim.rescue()
            robot.deliver()
            stats.victims_saved += 1
            return victim

    return None