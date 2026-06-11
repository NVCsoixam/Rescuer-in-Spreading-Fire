"""
app/fire/fire_sim.py

Fire propagation simulation and entity burn rules.
Manages deterministic fire expansion across the grid and handles health updates.
"""

from __future__ import annotations
from app.config import CellType, RobotState, VictimState
from app.core.state import Position, Robot, Victim, FireCell, SimulationStats
from app.map.grid import Grid


def spread_fire(
    grid: Grid,
    fire_cells: list[FireCell],
    current_step: int,
    stats: SimulationStats,
) -> list[FireCell]:
    """
    Deterministically expand fire to adjacent empty/navigable cells.
    WALL cells block fire propagation.

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

    # Fast set of currently burning positions
    burning_positions = {(fc.position.x, fc.position.y) for fc in fire_cells}
    new_positions: set[tuple[int, int]] = set()

    # Collect all candidate cells for fire expansion
    for fc in fire_cells:
        neighbors = grid.get_neighbors(fc.position.x, fc.position.y)
        for n in neighbors:
            pos_key = (n.x, n.y)
            if pos_key in burning_positions or pos_key in new_positions:
                continue
            cell = grid.get_cell(n.x, n.y)
            if cell is None or cell.cell_type == CellType.WALL:
                continue
            new_positions.add(pos_key)

    if not new_positions:
        return []

    # Sort for determinism
    sorted_positions = sorted(new_positions, key=lambda coord: (coord[1], coord[0]))
    new_fire_cells: list[FireCell] = []

    for x, y in sorted_positions:
        pos = Position(x, y)
        new_fc = FireCell(position=pos, ignition_step=current_step)
        new_fire_cells.append(new_fc)

        cell = grid.get_cell(x, y)
        if cell is not None:
            grid.set_cell(x, y, CellType.FIRE)
            cell.fire_level = 1.0
        burning_positions.add((x, y))

    # Ensure existing fire cells maintain burn level
    for fc in fire_cells:
        cell = grid.get_cell(fc.position.x, fc.position.y)
        if cell is not None and cell.cell_type == CellType.FIRE:
            cell.fire_level = max(cell.fire_level, 1.0)

    fire_cells.extend(new_fire_cells)
    stats.fire_spread_events += 1

    return new_fire_cells


def check_burn_entities(
    robot: Robot,
    victims: list[Victim],
    fire_cells: list[FireCell],
    stats: SimulationStats,
) -> None:
    """
    Check if any entities are caught in fire and update their states.
    If robot is carrying a victim and burns, the carried victim dies too.

    Args:
        robot: The robot entity.
        victims: The list of victims.
        fire_cells: The list of active fire cells.
        stats: The statistics object to update victims_dead count.
    """
    if robot is None or victims is None or fire_cells is None or stats is None:
        return

    # Fast set of burning positions
    burning_positions = {(fc.position.x, fc.position.y) for fc in fire_cells}
    if not burning_positions:
        return

    # 1. Check if Robot is caught in fire
    if robot.alive and (robot.x, robot.y) in burning_positions:
        robot.die()

        # Carried victim also dies
        if robot.carrying_victim and robot.carried_victim_id is not None:
            for victim in victims:
                if victim.victim_id == robot.carried_victim_id and victim.alive:
                    victim.killed()
                    stats.victims_dead += 1
                    break

    # 2. Check if any WAITING victims are caught in fire
    for victim in victims:
        if victim.is_active() and (victim.x, victim.y) in burning_positions:
            victim.killed()
            stats.victims_dead += 1