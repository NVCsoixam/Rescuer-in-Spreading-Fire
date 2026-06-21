"""
app/core/state.py

Domain models and state representations for the 2D Rescue Simulation System.
Defines Position, Cell, Robot, Victim, RescueStation, FireCell, SimulationStats, and GameState.
All coordinates are validated at construction time to prevent invalid state.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from app.config import CellType, SimulationState, RobotState, VictimState


@dataclass(frozen=True)
class Position:
    """Universal coordinate representation in the 2D grid."""
    x: int
    y: int

    def __post_init__(self) -> None:
        if self.x < 0 or self.y < 0:
            raise ValueError(f"Coordinates must be non-negative: ({self.x}, {self.y})")

    def __add__(self, other: tuple[int, int]) -> Position:
        """Support position + direction vector operations."""
        dx, dy = other
        return Position(self.x + dx, self.y + dy)

    def __sub__(self, other: Position) -> tuple[int, int]:
        """Return delta (dx, dy) between two positions."""
        return (self.x - other.x, self.y - other.y)

    def to_tuple(self) -> tuple[int, int]:
        """Fast conversion to tuple for hashing/set ops."""
        return (self.x, self.y)


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
        return self.position.x

    @property
    def y(self) -> int:
        return self.position.y

    def reset(self) -> None:
        """Reset cell to default empty state."""
        self.cell_type = CellType.EMPTY
        self.risk = 0.0
        self.fire_level = 0.0


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
        return self.position.x

    @property
    def y(self) -> int:
        return self.position.y

    def move_to(self, pos: Position) -> None:
        """Update robot position and increment step counter."""
        self.position = pos
        self.steps += 1

    def pickup(self, victim_id: int) -> None:
        """Mark robot as carrying a victim."""
        self.carrying_victim = True
        self.carried_victim_id = victim_id
        self.state = RobotState.CARRYING

    def deliver(self) -> None:
        """Reset robot after successful delivery."""
        self.carrying_victim = False
        self.carried_victim_id = None
        self.state = RobotState.MOVING

    def die(self) -> None:
        """Kill the robot."""
        self.alive = False
        self.state = RobotState.DEAD


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
        return self.position.x

    @property
    def y(self) -> int:
        return self.position.y

    def is_active(self) -> bool:
        """True if victim is waiting and alive (can be rescued)."""
        return self.state == VictimState.WAITING and self.alive

    def rescue(self) -> None:
        """Mark as successfully rescued."""
        self.state = VictimState.RESCUED
        self.rescued = True

    def killed(self) -> None:
        """Mark as dead."""
        self.alive = False
        self.state = VictimState.DEAD


@dataclass
class RescueStation:
    """Represents a rescue delivery/drop-off station."""
    station_id: int
    position: Position

    @property
    def x(self) -> int:
        return self.position.x

    @property
    def y(self) -> int:
        return self.position.y


@dataclass
class FireCell:
    """Represents a cell that is actively on fire, tracking ignition history."""
    position: Position
    ignition_step: int

    @property
    def x(self) -> int:
        return self.position.x

    @property
    def y(self) -> int:
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
    expanded_nodes: int = 0
    computation_time_ms: float = 0.0

    def reset(self) -> None:
        """Reset all statistics to zero."""
        self.total_steps = 0
        self.simulation_time = 0.0
        self.victims_saved = 0
        self.victims_dead = 0
        self.replans = 0
        self.fire_spread_events = 0
        self.expanded_nodes = 0
        self.computation_time_ms = 0.0


@dataclass
class MissionSummary:
    """Simulation final report — per 05_api_contracts.md DTO-004."""
    success: bool
    saved: int
    dead: int
    steps: int
    simulation_time: float
    algorithm: str
    expanded_nodes: int = 0
    computation_time_ms: float = 0.0
    map_seed: int = 0
    map_size: str = "?x?"
    map_edited: bool = False



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
    history: list[MissionSummary] = field(default_factory=list)
    map_seed: int = 0
    map_size: str = "20x20"
    map_edited: bool = False  # True neu user da chinh sua map bang Editor Mode

    def __post_init__(self) -> None:
        """Validate essential game state components."""
        if not self.grid or not self.grid[0]:
            raise ValueError("Grid cannot be empty")
        if self.robot is None:
            raise ValueError("Robot is required")

    @property
    def saved_count(self) -> int:
        return self.stats.victims_saved

    @property
    def dead_count(self) -> int:
        return self.stats.victims_dead

    @property
    def simulation_time(self) -> float:
        return self.stats.simulation_time

    @property
    def width(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    @property
    def height(self) -> int:
        return len(self.grid)

    @property
    def total_victims(self) -> int:
        return len(self.victims)

    @property
    def remaining_victims(self) -> int:
        """Victims still waiting to be rescued (alive and not yet carried/rescued)."""
        return sum(1 for v in self.victims if v.state == VictimState.WAITING)

    def get_cell(self, x: int, y: int) -> Cell | None:
        """Safely retrieve cell."""
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.grid[y][x]
        return None

    def set_cell_type(self, x: int, y: int, cell_type: CellType) -> None:
        """Set cell type with bounds check."""
        if 0 <= y < self.height and 0 <= x < self.width:
            self.grid[y][x].cell_type = cell_type

    def is_walkable(self, x: int, y: int) -> bool:
        """Check if a cell is navigable (not WALL or active FIRE)."""
        cell = self.get_cell(x, y)
        if cell is None:
            return False
        return cell.cell_type not in (CellType.WALL, CellType.FIRE)


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

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)
        self.is_valid = False

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)