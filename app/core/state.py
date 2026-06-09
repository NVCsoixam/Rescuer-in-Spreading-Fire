"""
app/core/state.py

Domain models and state representations for the 2D Rescue Simulation System.
Defines Position, Cell, Robot, Victim, RescueStation, FireCell, SimulationStats, and GameState.
"""

from dataclasses import dataclass
from app.config import CellType, SimulationState, RobotState, VictimState


@dataclass(frozen=True)
class Position:
    """Universal coordinate representation in the 2D grid."""
    x: int
    y: int

    def __post_init__(self) -> None:
        if self.x < 0 or self.y < 0:
            raise ValueError(f"Coordinates must be non-negative: ({self.x}, {self.y})")


@dataclass
class Cell:
    """Represents a single cell in the grid with type, risk score, and fire level."""
    position: Position
    cell_type: CellType
    risk: float = 0.0
    fire_level: float = 0.0

    def __post_init__(self) -> None:
        if not (0.0 <= self.risk <= 1.0):
            raise ValueError(f"Risk must be between 0.0 and 1.0, got {self.risk}")
        if self.fire_level < 0.0:
            raise ValueError(f"Fire level must be non-negative, got {self.fire_level}")

    @property
    def x(self) -> int:
        """Helper to get x coordinate directly."""
        return self.position.x

    @property
    def y(self) -> int:
        """Helper to get y coordinate directly."""
        return self.position.y


@dataclass
class Robot:
    """Represents the rescue robot entity."""
    position: Position
    state: RobotState = RobotState.IDLE
    carrying_victim: bool = False
    carried_victim_id: int | None = None
    alive: bool = True
    steps: int = 0

    @property
    def x(self) -> int:
        """Helper to get x coordinate directly."""
        return self.position.x

    @property
    def y(self) -> int:
        """Helper to get y coordinate directly."""
        return self.position.y


@dataclass
class Victim:
    """Represents a victim entity in the building."""
    victim_id: int
    position: Position
    state: VictimState = VictimState.WAITING
    alive: bool = True
    rescued: bool = False

    @property
    def x(self) -> int:
        """Helper to get x coordinate directly."""
        return self.position.x

    @property
    def y(self) -> int:
        """Helper to get y coordinate directly."""
        return self.position.y


@dataclass
class RescueStation:
    """Represents a rescue delivery/drop-off station."""
    station_id: int
    position: Position

    @property
    def x(self) -> int:
        """Helper to get x coordinate directly."""
        return self.position.x

    @property
    def y(self) -> int:
        """Helper to get y coordinate directly."""
        return self.position.y


@dataclass
class FireCell:
    """Represents a cell that is actively on fire, tracking ignition history."""
    position: Position
    ignition_step: int

    @property
    def x(self) -> int:
        """Helper to get x coordinate directly."""
        return self.position.x

    @property
    def y(self) -> int:
        """Helper to get y coordinate directly."""
        return self.position.y


@dataclass
class SimulationStats:
    """Collected runtime statistics for simulation run and benchmarking."""
    total_steps: int = 0
    simulation_time: float = 0.0
    victims_saved: int = 0
    victims_dead: int = 0
    replans: int = 0
    fire_spread_events: int = 0


@dataclass
class GameState:
    """Entire simulation world state (Single Source of Truth)."""
    grid: list[list[Cell]]
    robot: Robot
    victims: list[Victim]
    rescue_stations: list[RescueStation]
    fire_cells: list[FireCell]
    stats: SimulationStats
    current_mode: SimulationState
    selected_algorithm: str

    @property
    def saved_count(self) -> int:
        """Convenience property for victims saved count."""
        return self.stats.victims_saved

    @property
    def dead_count(self) -> int:
        """Convenience property for victims deceased count."""
        return self.stats.victims_dead

    @property
    def simulation_time(self) -> float:
        """Convenience property for total simulation time in seconds."""
        return self.stats.simulation_time

    @property
    def width(self) -> int:
        """Width of the simulation grid."""
        return len(self.grid[0]) if self.grid else 0

    @property
    def height(self) -> int:
        """Height of the simulation grid."""
        return len(self.grid)


@dataclass
class PathResult:
    """Standard search result format returned by all AI pathfinding algorithms."""
    found: bool
    path: list[Position]
    cost: float
    expanded_nodes: int
    execution_time_ms: float


@dataclass
class ValidationReport:
    """Structure returned by state validation check."""
    is_valid: bool
    errors: list[str]
    warnings: list[str]


