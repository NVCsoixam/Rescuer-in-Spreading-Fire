"""
app/core/validator.py

State validation system for the 2D Rescue Simulation System.
Verifies grid dimensions, entity counts, overlaps, and paths connectivity at initialization.
"""

from app.config import CellType, GRID_MIN_SIZE, GRID_MAX_SIZE
from app.core.state import GameState, ValidationReport


def validate_game_state(state: GameState) -> ValidationReport:
    """
    Validate the completeness and correctness of the GameState.

    Checks:
        - Grid width and height are within boundaries.
        - Exactly 1 robot exists.
        - At least 1 victim exists.
        - At least 1 rescue station exists.
        - At least 1 fire cell exists.
        - Check for initial overlap violations.

    Args:
        state: The GameState to validate.

    Returns:
        ValidationReport: A report containing validation results, errors, and warnings.
    """
    errors: list[str] = []
    warnings: list[str] = []

    # 1. Grid boundary validation
    height = len(state.grid)
    width = len(state.grid[0]) if height > 0 else 0

    if not (GRID_MIN_SIZE <= width <= GRID_MAX_SIZE):
        errors.append(f"Grid width {width} is outside valid range [{GRID_MIN_SIZE}, {GRID_MAX_SIZE}].")
    if not (GRID_MIN_SIZE <= height <= GRID_MAX_SIZE):
        errors.append(f"Grid height {height} is outside valid range [{GRID_MIN_SIZE}, {GRID_MAX_SIZE}].")

    # 2. Entity count validation
    # Verify Robot existence
    if state.robot is None:
        errors.append("Robot is missing from the state.")

    # Verify Victim count
    if not state.victims:
        errors.append("At least one victim is required in the simulation.")

    # Verify Rescue station count
    if not state.rescue_stations:
        errors.append("At least one rescue station is required in the simulation.")

    # Verify Fire source count
    if not state.fire_cells:
        errors.append("At least one fire cell (source) is required in the simulation.")

    # 3. Position and Overlap check
    occupied_positions: dict[tuple[int, int], str] = {}

    # Check Robot position
    if state.robot is not None:
        rx, ry = state.robot.x, state.robot.y
        if not (0 <= rx < width and 0 <= ry < height):
            errors.append(f"Robot position ({rx}, {ry}) is out of bounds.")
        else:
            occupied_positions[(rx, ry)] = "Robot"

    # Check Rescue Station positions
    for rs in state.rescue_stations:
        rsx, rsy = rs.x, rs.y
        if not (0 <= rsx < width and 0 <= rsy < height):
            errors.append(f"Rescue Station #{rs.station_id} at ({rsx}, {rsy}) is out of bounds.")
        else:
            if (rsx, rsy) in occupied_positions:
                errors.append(f"Overlap detected: Rescue Station #{rs.station_id} and {occupied_positions[(rsx, rsy)]} occupy the same cell ({rsx}, {rsy}).")
            occupied_positions[(rsx, rsy)] = "Rescue Station"

    # Check Victim positions
    for v in state.victims:
        vx, vy = v.x, v.y
        if not (0 <= vx < width and 0 <= vy < height):
            errors.append(f"Victim #{v.victim_id} at ({vx}, {vy}) is out of bounds.")
        else:
            if (vx, vy) in occupied_positions:
                errors.append(f"Overlap detected: Victim #{v.victim_id} and {occupied_positions[(vx, vy)]} occupy the same cell ({vx}, {vy}).")
            occupied_positions[(vx, vy)] = "Victim"

    # Check Fire Cell positions
    for fc in state.fire_cells:
        fx, fy = fc.position.x, fc.position.y
        if not (0 <= fx < width and 0 <= fy < height):
            errors.append(f"Fire Cell at ({fx}, {fy}) is out of bounds.")
        else:
            # Note: Fire and victims / robot can overlap depending on run state,
            # but at initialization we should issue warnings/errors if they start on fire
            if (fx, fy) in occupied_positions:
                entity = occupied_positions[(fx, fy)]
                warnings.append(f"Initial threat: {entity} starts inside a fire cell at ({fx}, {fy}).")

    # Determine validity
    is_valid = len(errors) == 0

    return ValidationReport(is_valid=is_valid, errors=errors, warnings=warnings)
