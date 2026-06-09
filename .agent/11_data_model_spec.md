# 11_data_model_spec.md

# PURPOSE

Tài liệu này định nghĩa toàn bộ Domain Model của hệ thống.

Đây là nguồn sự thật duy nhất cho:

* Entity
* State Object
* DTO
* Relationships
* Ownership

Mọi implementation phải tuân thủ chính xác tài liệu này.

---

# 1. DOMAIN OVERVIEW

Hệ thống bao gồm 6 domain entity chính:

```text id="d001"
Cell

Robot

Victim

RescueStation

GameState

Snapshot
```

---

Relationship

```text id="d002"
GameState

 ├── Grid
 ├── Robot
 ├── Victims
 ├── RescueStations
 ├── FireCells
 └── Runtime Statistics
```

---

# 2. POSITION MODEL

---

## MODEL-001

### Position

File

```text id="d003"
app/core/state.py
```

---

Definition

```python
@dataclass(frozen=True)
class Position:

    x: int

    y: int
```

---

Constraints

```text id="d004"
x >= 0

y >= 0
```

---

Purpose

```text id="d005"
Universal coordinate object
```

---

# 3. CELL MODEL

---

## MODEL-002

### CellType

```python
class CellType(Enum):

    EMPTY = 0

    WALL = 1

    FIRE = 2

    VICTIM = 3

    ROBOT = 4

    RESCUE = 5
```

---

## MODEL-003

### Cell

Definition

```python
@dataclass
class Cell:

    position: Position

    cell_type: CellType

    risk: float
```

---

Risk Range

```python
0.0 <= risk <= 1.0
```

---

Purpose

```text id="d006"
World representation
```

---

# 4. ROBOT MODEL

---

## MODEL-004

### RobotState

```python
class RobotState(Enum):

    IDLE = 0

    MOVING = 1

    CARRYING = 2

    DEAD = 3
```

---

## MODEL-005

### Robot

Definition

```python
@dataclass
class Robot:

    position: Position

    state: RobotState

    carrying_victim: bool

    carried_victim_id: int | None

    alive: bool
```

---

Constraints

```text id="d007"
Only one robot exists
```

---

# 5. VICTIM MODEL

---

## MODEL-006

### VictimState

```python
class VictimState(Enum):

    WAITING = 0

    CARRIED = 1

    RESCUED = 2

    DEAD = 3
```

---

## MODEL-007

### Victim

Definition

```python
@dataclass
class Victim:

    victim_id: int

    position: Position

    state: VictimState

    alive: bool
```

---

Rule

```text id="d008"
victim_id unique
```

---

# 6. RESCUE STATION MODEL

---

## MODEL-008

### RescueStation

Definition

```python
@dataclass
class RescueStation:

    station_id: int

    position: Position
```

---

Rule

```text id="d009"
station_id unique
```

---

# 7. FIRE MODEL

---

## MODEL-009

### FireCell

Definition

```python
@dataclass
class FireCell:

    position: Position

    ignition_step: int
```

---

Purpose

```text id="d010"
Track fire history
```

---

# 8. GAME STATISTICS MODEL

---

## MODEL-010

### SimulationStats

Definition

```python
@dataclass
class SimulationStats:

    total_steps: int

    simulation_time: float

    victims_saved: int

    victims_dead: int

    replans: int

    fire_spread_events: int
```

---

Purpose

```text id="d011"
Benchmarking
```

---

# 9. GAME STATE MODEL

---

## MODEL-011

### GameState

Definition

```python
@dataclass
class GameState:

    grid: list[list[Cell]]

    robot: Robot

    victims: list[Victim]

    rescue_stations: list[RescueStation]

    fire_cells: list[FireCell]

    stats: SimulationStats

    current_mode: SimulationMode

    selected_algorithm: str
```

---

Ownership

```text id="d012"
Engine owns GameState
```

---

Rule

```text id="d013"
Single source of truth
```

---

# 10. SNAPSHOT MODEL

---

## MODEL-012

### Snapshot

Definition

```python
@dataclass
class Snapshot:

    saved_state: GameState

    created_at_step: int
```

---

Purpose

```text id="d014"
Deterministic reset
```

---

# 11. AI MODELS

---

## MODEL-013

### PathNode

Definition

```python
@dataclass
class PathNode:

    position: Position

    cost: float

    parent: "PathNode | None"
```

---

Purpose

```text id="d015"
Search tree node
```

---

## MODEL-014

### PathResult

Definition

```python
@dataclass
class PathResult:

    found: bool

    path: list[Position]

    cost: float

    expanded_nodes: int

    execution_time_ms: float
```

---

Purpose

```text id="d016"
Standard AI output
```

---

# 12. VALIDATION MODELS

---

## MODEL-015

### ValidationReport

Definition

```python
@dataclass
class ValidationReport:

    is_valid: bool

    errors: list[str]

    warnings: list[str]
```

---

Purpose

```text id="d017"
Validation result
```

---

# 13. MISSION SUMMARY MODEL

---

## MODEL-016

### MissionSummary

Definition

```python
@dataclass
class MissionSummary:

    success: bool

    saved: int

    dead: int

    steps: int

    simulation_time: float

    algorithm: str
```

---

Purpose

```text id="d018"
Final mission report
```

---

# 14. ENTITY RELATIONSHIPS

---

Relationship Diagram

```text id="d019"
GameState
   │
   ├── Robot (1)
   │
   ├── Victim (N)
   │
   ├── RescueStation (N)
   │
   ├── FireCell (N)
   │
   └── Grid (1)
```

---

Constraints

```text id="d020"
Exactly 1 Robot

At least 1 Victim

At least 1 Rescue Station

At least 1 Fire Source
```

---

# 15. SERIALIZATION RULES

---

Allowed

```python
dataclass

json
```

---

Forbidden

```python
pickle
```

---

Reason

```text id="d021"
Security

Portability

Debuggability
```

---

# 16. IMMUTABILITY RULES

---

Immutable

```text id="d022"
Position

PathResult

MissionSummary
```

---

Mutable

```text id="d023"
GameState

Robot

Victim
```

---

# 17. SUCCESS CRITERIA

Data Model passes review when:

```text id="d024"
All entities defined

Relationships explicit

No duplicate ownership

No hidden fields

Contracts satisfied

Serialization defined
```

---

# END OF FILE

File Number

```text id="d025"
11_data_model_spec.md
```

Next File

```text id="d026"
12_engine_design.md
```

Purpose

```text id="d027"
Simulation Engine Architecture

Execution Pipeline

Scheduler

State Mutation Rules

Runtime Loop Design
```
