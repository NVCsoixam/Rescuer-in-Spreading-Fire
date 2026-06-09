"""
app/fire/fire_sim.py

Fire propagation simulation and entity burn rules.
Manages deterministic fire expansion across the grid and handles health updates.
"""

from app.config import CellType, RobotState, VictimState
from app.core.state import Position, Robot, Victim, FireCell, SimulationStats
from app.map.grid import Grid


def spread_fire(
    grid: Grid,
    fire_cells: list[FireCell],
    current_step: int,
    stats: SimulationStats
) -> list[FireCell]:
    """
    Deterministically expand fire to adjacent empty/navigable cells.
    WALL cells block fire.

    Args:
        grid: The simulation grid.
        fire_cells: The list of active FireCell objects.
        current_step: The current step index of the simulation.
        stats: SimulationStats to update (e.g. fire spread count).

    Returns:
        list[FireCell]: The list of newly created FireCell objects in this step.
    """
    if not fire_cells:
        return []

    # Get set of all currently burning positions for O(1) checks
    burning_positions = { (fc.position.x, fc.position.y) for fc in fire_cells }
    new_positions: set[tuple[int, int]] = set()

    for fc in fire_cells:
        neighbors = grid.get_neighbors(fc.position.x, fc.position.y)
        for n in neighbors:
            # Check if neighbor is not already burning and is not a WALL
            if (n.x, n.y) not in burning_positions:
                cell = grid.get_cell(n.x, n.y)
                if cell is not None and cell.cell_type != CellType.WALL:
                    new_positions.add((n.x, n.y))

    if not new_positions:
        return []

    # Sort new positions to ensure deterministic ordering (y primary, x secondary)
    sorted_new_positions = sorted(list(new_positions), key=lambda coord: (coord[1], coord[0]))

    new_fire_cells: list[FireCell] = []
    for x, y in sorted_new_positions:
        pos = Position(x, y)
        new_fc = FireCell(position=pos, ignition_step=current_step)
        new_fire_cells.append(new_fc)

        # Update Grid cells
        grid.set_cell(x, y, CellType.FIRE)
        # Add to local burning positions list to avoid duplicate insertions
        burning_positions.add((x, y))

    # Update state lists and statistics
    fire_cells.extend(new_fire_cells)
    stats.fire_spread_events += 1

    return new_fire_cells


def check_burn_entities(
    robot: Robot,
    victims: list[Victim],
    fire_cells: list[FireCell],
    stats: SimulationStats
) -> None:
    """
    Check if any entities are caught in fire and update their states.
    If robot is carrying a victim and burns, the victim dies too.

    Args:
        robot: The robot entity.
        victims: The list of victims.
        fire_cells: The list of active fire cells.
        stats: The statistics object to update victims_dead count.

    Returns:
        None
    """
    # Create set of burning positions for fast check
    burning_positions = { (fc.position.x, fc.position.y) for fc in fire_cells }

    # 1. Check if Robot is caught in fire
    if robot.alive and (robot.position.x, robot.position.y) in burning_positions:
        robot.alive = False
        robot.state = RobotState.DEAD

        # If carrying a victim, that victim dies as well
        if robot.carrying_victim and robot.carried_victim_id is not None:
            for victim in victims:
                if victim.victim_id == robot.carried_victim_id and victim.alive:
                    victim.alive = False
                    victim.state = VictimState.DEAD
                    stats.victims_dead += 1
                    break

    # 2. Check if any WAITING victims are caught in fire
    for victim in victims:
        if (victim.state == VictimState.WAITING and
                victim.alive and
                (victim.position.x, victim.position.y) in burning_positions):
            victim.alive = False
            victim.state = VictimState.DEAD
            stats.victims_dead += 1
