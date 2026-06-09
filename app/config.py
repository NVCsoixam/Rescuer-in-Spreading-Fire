"""
app/config.py

Global configuration system for the 2D Rescue Simulation System.
Contains enums, constants, screen layout definitions, and directions.
"""

from enum import Enum

# Grid settings
GRID_MIN_SIZE: int = 10
GRID_MAX_SIZE: int = 35
GRID_DEFAULT_SIZE: int = 20

# Pathfinding risk penalty weight
RISK_WEIGHT: float = 10.0

# Default entity counts
DEFAULT_VICTIM_COUNT: int = 5
DEFAULT_RESCUE_COUNT: int = 3
DEFAULT_FIRE_SOURCE_COUNT: int = 1

# Fire simulation timing (in milliseconds)
FIRE_INTERVAL_DEFAULT: int = 1000
FIRE_INTERVAL_MIN: int = 0
FIRE_INTERVAL_MAX: int = 10000

# App frames per second
FPS: int = 30

# UI window layout dimensions
WINDOW_WIDTH: int = 1200
WINDOW_HEIGHT: int = 800
GRID_AREA_WIDTH: int = 960
SIDEBAR_WIDTH: int = 240


class CellType(Enum):
    """Types of cells present in the 2D simulation grid."""
    EMPTY = 0
    WALL = 1
    FIRE = 2
    VICTIM = 3
    ROBOT = 4
    RESCUE = 5


class SimulationState(Enum):
    """Standard state machine representation for the simulation."""
    READY = "READY"
    USER_MODE = "USER_MODE"
    BFS = "BFS"
    DFS = "DFS"
    UCS = "UCS"
    DIJKSTRA = "DIJKSTRA"
    GREEDY = "GREEDY"
    ASTAR = "ASTAR"
    PAUSED = "PAUSED"
    MISSION_COMPLETE = "MISSION_COMPLETE"
    MISSION_FAILED = "MISSION_FAILED"


class EditTool(Enum):
    """Active tools for the Editor Mode when placing or erasing entities."""
    ROBOT = "ROBOT"
    VICTIM = "VICTIM"
    FIRE = "FIRE"
    WALL = "WALL"
    RESCUE = "RESCUE"
    ERASE = "ERASE"


class RobotState(Enum):
    """Internal lifecycle state of the rescue robot."""
    IDLE = 0
    MOVING = 1
    CARRYING = 2
    DEAD = 3


class VictimState(Enum):
    """Internal state of the victim in the simulation."""
    WAITING = 0
    CARRIED = 1
    RESCUED = 2
    DEAD = 3


class EnvironmentType(Enum):
    """Available environment generation styles for procedural building layout."""
    APARTMENT = "APARTMENT"
    OFFICE = "OFFICE"
    HOSPITAL = "HOSPITAL"
    WAREHOUSE = "WAREHOUSE"
    MIXED = "MIXED"


class Complexity(Enum):
    """Density and branching factor settings for procedural generator."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# Movement vectors (dx, dy)
UP: tuple[int, int] = (0, -1)
DOWN: tuple[int, int] = (0, 1)
LEFT: tuple[int, int] = (-1, 0)
RIGHT: tuple[int, int] = (1, 0)

# Fixed direction list for deterministic neighbor ordering (UP, RIGHT, DOWN, LEFT)
DIRECTIONS: list[tuple[int, int]] = [UP, RIGHT, DOWN, LEFT]

# Fire speed presets UI to Millisecond mapping
FIRE_SPEED_PRESETS: dict[str, int] = {
    "Very Fast": 500,
    "Fast": 750,
    "Normal": 1000,
    "Slow": 1500,
    "Very Slow": 3000
}
