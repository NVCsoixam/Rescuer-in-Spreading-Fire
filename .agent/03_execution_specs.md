# 03_execution_specs.md (PART 1)

# PURPOSE

Tài liệu này chuyển đổi Micro Tasks thành các đặc tả triển khai có thể thực thi trực tiếp bởi AI Coding Agent.

Mọi implementation phải tuân thủ:

```text
UI contains no business logic

Engine is the single source of truth

AI modules are pure functions

Fire simulation is deterministic

State mutation only through Engine
```

---

# P00-T03 — GLOBAL CONFIGURATION SYSTEM

---

## SPEC-001

### Component

Config Module

### File

```text
app/config.py
```

### Responsibilities

Store all global constants.

No runtime logic allowed.

---

### Required Constants

```python
GRID_MIN_SIZE = 10
GRID_MAX_SIZE = 35
GRID_DEFAULT_SIZE = 20

DEFAULT_VICTIM_COUNT = 5
DEFAULT_RESCUE_COUNT = 3
DEFAULT_FIRE_SOURCE_COUNT = 1

FIRE_INTERVAL_DEFAULT = 1000

FPS = 30
```

---

### Cell Types

```python
EMPTY = 0
WALL = 1
FIRE = 2
VICTIM = 3
ROBOT = 4
RESCUE = 5
```

---

### Lifecycle States

```python
IDLE
EDIT
RUNNING
PAUSED
FINISHED
```

---

### Movement

```python
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
```

---

### Validation

```text
No imports from engine
No imports from UI
No imports from AI
```

---

# P00-T04 — GAME STATE MODELS

---

## SPEC-002

### Component

Cell

### File

```text
app/core/state.py
```

### Type

```python
@dataclass
```

---

### Fields

```python
x: int
y: int

cell_type: int

risk: float = 0.0

fire_level: float = 0.0
```

---

### Validation

```text
risk >= 0

fire_level >= 0
```

---

### Methods

None

Cell is a pure data structure.

---

## SPEC-003

### Component

Robot

### Type

```python
@dataclass
```

---

### Fields

```python
x: int
y: int

alive: bool = True

carrying_victim: bool = False

steps: int = 0
```

---

### Invariants

```text
Only one robot exists

Robot occupies exactly one cell
```

---

## SPEC-004

### Component

Victim

### Type

```python
@dataclass
```

---

### Fields

```python
x: int
y: int

alive: bool = True

rescued: bool = False
```

---

### State Rules

```text
rescued=True => alive=True

alive=False => rescued=False
```

---

## SPEC-005

### Component

RescueStation

### Type

```python
@dataclass
```

---

### Fields

```python
x: int
y: int
```

---

## SPEC-006

### Component

GameState

### Type

```python
@dataclass
```

---

### Fields

```python
grid

robot

victims

rescue_stations

fire_cells

saved_count

dead_count

simulation_time

current_mode
```

---

### Ownership Rules

```text
GameState owns all runtime data.

No subsystem may duplicate state.
```

---

### Mutation Rules

```text
Direct mutation forbidden outside Engine.
```

---

# P00-T05 — SNAPSHOT SYSTEM

---

## SPEC-007

### Component

Snapshot Module

### File

```text
app/core/snapshot.py
```

---

### Function

```python
create_snapshot(
    state: GameState
) -> GameState
```

---

### Purpose

Create deep copy of entire simulation state.

---

### Algorithm

```text
1. Receive GameState

2. Deep copy all fields

3. Return cloned object
```

---

### Complexity

```text
Time: O(N)

Space: O(N)
```

Where:

```text
N = number of cells + entities
```

---

## SPEC-008

### Function

```python
restore_snapshot(
    snapshot: GameState
) -> GameState
```

---

### Purpose

Restore original simulation state.

---

### Algorithm

```text
1. Deep copy snapshot

2. Return restored state
```

---

### Constraints

```text
No reference sharing

No shallow copy
```

---

### Validation Tests

```text
Modify current state

Restore snapshot

Verify:

robot position restored

victims restored

fire restored

counters restored
```

---

# P00-T06 — GRID SYSTEM

---

## SPEC-009

### Component

Grid

### File

```text
app/map/grid.py
```

### Class

```python
class Grid
```

---

### Constructor

```python
Grid(
    width: int,
    height: int
)
```

---

### Fields

```python
width

height

cells
```

---

### Storage

```python
cells[y][x]
```

---

### Validation

```text
width >= GRID_MIN_SIZE

height >= GRID_MIN_SIZE
```

---

## SPEC-010

### Function

```python
get_cell(
    x: int,
    y: int
)
```

---

### Returns

```python
Cell
```

---

### Failure

```text
Out of bounds

-> return None
```

---

## SPEC-011

### Function

```python
set_cell(
    x: int,
    y: int,
    value
)
```

---

### Validation

```text
Coordinate must exist
```

---

### Failure

```text
Raise ValueError
```

---

## SPEC-012

### Function

```python
in_bounds(
    x: int,
    y: int
)
```

---

### Returns

```python
bool
```

---

## SPEC-013

### Function

```python
get_neighbors(
    x: int,
    y: int
)
```

---

### Movement Rules

```text
4-direction only

No diagonal
```

---

### Neighbor Order

```python
UP
RIGHT
DOWN
LEFT
```

Deterministic ordering required.

---

### Returns

```python
List[(x,y)]
```

---

## SPEC-014

### Function

```python
is_walkable(
    x: int,
    y: int
)
```

---

### Blocked Types

```text
WALL

FIRE
```

---

### Returns

```python
bool
```

---

# END OF PART 1

Covered:

```text
P00-T03 Configuration

P00-T04 State Models

P00-T05 Snapshot System

P00-T06 Grid System
```

Next:

```text
P00-T07 Map Generator

P00-T08 Movement Logic

P00-T09 Rescue Logic

P00-T10 Fire Simulation

P00-T11 Heat Map
```
# 03_execution_specs.md (PART 2)

# P00-T07 — MAP GENERATOR

---

## SPEC-015

### Component

MapGenerator

### File

```text
app/map/generator.py
```

### Class

```python
class MapGenerator
```

---

### Responsibilities

```text
Generate playable maps

Generate rooms

Generate corridors

Place entities

Validate reachability
```

---

### Constraints

```text
No random noise maps

Must resemble building layout

Must be fully playable
```

---

## SPEC-016

### Function

```python
generate_empty_map(
    width: int,
    height: int
)
```

---

### Algorithm

```text
Create Grid

Fill all cells as WALL
```

---

### Complexity

```text
O(width * height)
```

---

## SPEC-017

### Function

```python
generate_rooms()
```

---

### Parameters

```python
MIN_ROOM_SIZE = 3

MAX_ROOM_SIZE = 8

ROOM_COUNT = random(...)
```

---

### Algorithm

```text
1 Create candidate room

2 Check overlap

3 If valid:
    carve room

4 Store room metadata
```

---

### Output

```text
List[Room]
```

---

## SPEC-018

### Function

```python
connect_rooms()
```

---

### Goal

Guarantee global connectivity.

---

### Algorithm

```text
Sort rooms

For i in range(room_count-1):

    connect center(i)

    to

    center(i+1)
```

---

### Corridor Type

```text
L-shaped corridor
```

---

### Determinism

```text
Given same seed

Generate same map
```

---

## SPEC-019

### Function

```python
validate_connectivity()
```

---

### Algorithm

```text
BFS from robot spawn

Count reachable walkable cells

Compare against total walkable cells
```

---

### Success

```text
All walkable cells reachable
```

---

### Failure

```text
Regenerate map
```

---

## SPEC-020

### Function

```python
place_entities()
```

---

### Placement Order

```text
Robot

Rescue Stations

Victims

Fire Sources
```

---

### Rules

```text
No overlap

Walkable only

Unique positions
```

---

## SPEC-021

### Function

```python
validate_playability()
```

---

### Required Checks

```text
Robot exists

Victims exist

Rescue stations exist

Fire source exists
```

---

### Reachability Checks

```text
Robot -> Victim

Victim -> Rescue
```

---

### Failure

```text
Regenerate map
```

---

# P00-T08 — MOVEMENT LOGIC

---

## SPEC-022

### Component

MovementService

### File

```text
app/logic/movement.py
```

---

### Responsibility

```text
Robot movement only

No AI decisions
```

---

## SPEC-023

### Function

```python
move(
    state,
    direction
)
```

---

### Input

```python
direction = (
    dx,
    dy
)
```

---

### Algorithm

```text
1 Compute target cell

2 Validate bounds

3 Validate walkable

4 Update robot position

5 Increment step counter
```

---

### Success

```text
Return True
```

---

### Failure

```text
Return False
```

---

## SPEC-024

### Collision Rules

Blocked:

```text
Wall

Fire
```

---

Allowed:

```text
Victim

Rescue Station
```

---

## SPEC-025

### Step Counter

Rule

```text
Increment only on successful movement
```

---

### Failure Case

```text
Blocked move

No increment
```

---

# P00-T09 — RESCUE SYSTEM

---

## SPEC-026

### Component

RescueService

### File

```text
app/logic/rescue.py
```

---

### Responsibilities

```text
Pickup victim

Drop victim

Update statistics
```

---

## SPEC-027

### Function

```python
pickup_victim()
```

---

### Preconditions

```text
Robot alive

Robot not carrying

Victim alive

Same position
```

---

### Algorithm

```text
Find victim

Set carrying=True

Remove victim from grid
```

---

### Success

```text
Victim attached to robot
```

---

## SPEC-028

### Function

```python
drop_victim()
```

---

### Preconditions

```text
Robot carrying victim

Standing on rescue station
```

---

### Algorithm

```text
Set carrying=False

Victim.rescued=True

saved_count += 1
```

---

### Output

```text
Victim rescued
```

---

## SPEC-029

### Function

```python
check_mission_complete()
```

---

### Success

```text
All victims rescued
```

---

### Returns

```python
bool
```

---

# P00-T10 — FIRE SIMULATION

---

## SPEC-030

### Component

FireManager

### File

```text
app/fire/fire_sim.py
```

---

### Responsibilities

```text
Track fire cells

Spread fire

Handle burning events
```

---

## SPEC-031

### Data Model

Store:

```python
active_fire_cells
```

---

### Type

```python
Set[(x,y)]
```

---

## SPEC-032

### Function

```python
tick()
```

---

### Purpose

Advance fire by one simulation step.

---

### Algorithm

```text
For every fire cell

Expand to neighbors

Collect new cells

Apply spread simultaneously
```

---

### Important

```text
Never modify source set during iteration
```

---

## SPEC-033

### Spread Rules

Can spread to:

```text
Empty

Victim

Robot

Rescue
```

---

Cannot spread to:

```text
Wall
```

---

## SPEC-034

### Victim Burn Logic

Condition

```text
Victim position enters fire
```

---

### Result

```text
alive=False

dead_count += 1
```

---

## SPEC-035

### Robot Burn Logic

Condition

```text
Robot position enters fire
```

---

### Result

```text
alive=False

Mission failure
```

---

## SPEC-036

### Deterministic Spread

Rule

```text
Same map

Same fire interval

Same seed

=> Same fire behavior
```

---

# P00-T11 — HEAT MAP SYSTEM

---

## SPEC-037

### Component

RiskMap

### File

```text
app/fire/heatmap.py
```

---

### Purpose

Convert fire information into navigation risk.

---

## SPEC-038

### Risk Scale

```text
0.0 Safe

0.3 Warning

0.6 Danger

0.9 Critical

1.0 Fire
```

---

## SPEC-039

### Function

```python
recalculate()
```

---

### Trigger

```text
Every fire tick
```

---

### Algorithm

```text
For each cell

Compute nearest fire distance

Convert distance -> risk
```

---

### Example

```text
Distance 0 => 1.0

Distance 1 => 0.9

Distance 2 => 0.7

Distance 3 => 0.5

Distance 4+ => 0.2
```

---

## SPEC-040

### Function

```python
get_risk(
    x,
    y
)
```

---

### Returns

```python
float
```

---

### Range

```text
0.0 <= risk <= 1.0
```

---

## SPEC-041

### Function

```python
get_overlay()
```

---

### Purpose

Provide renderer data.

---

### Output

```python
List[List[float]]
```

---

### Consumers

```text
Renderer

AI algorithms
```

---

# END OF PART 2

Covered:

```text
P00-T07 Map Generator

P00-T08 Movement Logic

P00-T09 Rescue System

P00-T10 Fire Simulation

P00-T11 Heat Map
```

Next:

```text
P00-T12 Core Engine

P00-T13 BFS

P00-T14 DFS

P00-T15 UCS

P00-T16 Dijkstra

P00-T17 Greedy

P00-T18 A*

P00-T19 Shared AI Utilities
```
# 03_execution_specs.md (PART 3)

# P00-T12 — CORE ENGINE

---

## SPEC-042

### Component

Engine

### File

```text
app/core/engine.py
```

### Class

```python
class Engine
```

---

### Responsibilities

```text
Own GameState

Own Snapshot

Coordinate Fire

Coordinate Rescue

Coordinate AI

Coordinate UI Requests
```

---

### Architectural Rule

```text
Engine is the only component allowed
to mutate GameState.
```

---

## SPEC-043

### Constructor

```python
Engine(
    state: GameState
)
```

---

### Internal Dependencies

```python
Grid

FireManager

RiskMap

MovementService

RescueService
```

---

### State Ownership

```text
Engine owns:

current_state

snapshot

current_algorithm
```

---

## SPEC-044

### Function

```python
start()
```

---

### Preconditions

```text
State = IDLE or EDIT

Validation passed

Snapshot exists
```

---

### Actions

```text
current_mode = RUNNING
```

---

## SPEC-045

### Function

```python
pause()
```

---

### Preconditions

```text
current_mode = RUNNING
```

---

### Actions

```text
current_mode = PAUSED
```

---

## SPEC-046

### Function

```python
resume()
```

---

### Preconditions

```text
current_mode = PAUSED
```

---

### Actions

```text
current_mode = RUNNING
```

---

## SPEC-047

### Function

```python
reset()
```

---

### Algorithm

```text
Load snapshot

Replace current state

Reset timers

Reset runtime counters
```

---

### Complexity

```text
O(N)
```

---

## SPEC-048

### Function

```python
simulation_step()
```

---

### Execution Order

```text
1 AI decision

2 Robot movement

3 Rescue logic

4 Fire tick

5 Risk update

6 Statistics update

7 End-state evaluation
```

---

### Important

```text
Order must never change.
```

---

## SPEC-049

### Function

```python
evaluate_terminal_conditions()
```

---

### Success Conditions

```text
All victims rescued
```

---

### Failure Conditions

```text
Robot dead

No reachable victims

No reachable rescue station
```

---

### Result

```text
current_mode = FINISHED
```

---

# P00-T19 — SHARED AI UTILITIES

---

## SPEC-050

### File

```text
app/ai/_shared.py
```

---

## SPEC-051

### Dataclass

```python
PathResult
```

---

### Fields

```python
found: bool

path: list

cost: float

expanded_nodes: int

execution_time_ms: float
```

---

## SPEC-052

### Function

```python
reconstruct_path(
    parent_map,
    start,
    goal
)
```

---

### Algorithm

```text
Start from goal

Follow parents

Reverse path

Return path
```

---

### Complexity

```text
O(path_length)
```

---

## SPEC-053

### Function

```python
manhattan_distance(
    a,
    b
)
```

---

### Formula

```python
abs(ax-bx)+abs(ay-by)
```

---

### Usage

```text
Greedy

A*
```

---

## SPEC-054

### Function

```python
risk_cost(
    risk_value
)
```

---

### Formula

```python
cost = 1 + risk_value * K
```

---

### Default

```python
K = 10
```

---

## SPEC-055

### Function

```python
get_neighbors(
    grid,
    x,
    y
)
```

---

### Rules

```text
4-direction

No walls

No fire
```

---

# P00-T13 — BFS

---

## SPEC-056

### File

```text
app/ai/bfs.py
```

---

### Function

```python
bfs(
    grid,
    start,
    goal
)
```

---

### Data Structure

```python
collections.deque
```

---

### Expansion Order

```text
UP

RIGHT

DOWN

LEFT
```

---

### Determinism

```text
Required
```

---

## SPEC-057

### Search Logic

```text
Push start

Loop queue

Expand neighbors

Track visited

Track parent

Stop at goal
```

---

### Cost Model

```text
Uniform cost

Every move = 1
```

---

## SPEC-058

### Metrics

Collect:

```python
expanded_nodes

path_length

execution_time
```

---

# P00-T14 — DFS

---

## SPEC-059

### File

```text
app/ai/dfs.py
```

---

### Function

```python
dfs(
    grid,
    start,
    goal
)
```

---

### Data Structure

```python
stack
```

---

### Search Strategy

```text
Depth-first exploration
```

---

### Important

```text
Not guaranteed shortest path
```

---

## SPEC-060

### Metrics

Collect:

```python
expanded_nodes

path_length

execution_time
```

---

# P00-T15 — UCS

---

## SPEC-061

### File

```text
app/ai/ucs.py
```

---

### Function

```python
ucs(
    grid,
    start,
    goal
)
```

---

### Data Structure

```python
heapq
```

---

### Priority

```python
g_cost
```

---

### Expansion

```text
Lowest cumulative cost first
```

---

## SPEC-062

### Cost Model

```python
move_cost = 1
```

---

### Future Extension

```python
move_cost = risk-aware
```

---

# P00-T16 — DIJKSTRA

---

## SPEC-063

### File

```text
app/ai/dijkstra.py
```

---

### Function

```python
dijkstra(
    grid,
    start,
    goal
)
```

---

### Data Structures

```python
distance_map

priority_queue
```

---

### Formula

```python
new_cost =
current_cost +
edge_cost
```

---

## SPEC-064

### Guarantees

```text
Optimal path

Non-negative costs only
```

---

### Complexity

```text
O(E log V)
```

---

# P00-T17 — GREEDY SEARCH

---

## SPEC-065

### File

```text
app/ai/greedy.py
```

---

### Function

```python
greedy_search(
    grid,
    start,
    goal
)
```

---

### Priority

```python
h(n)
```

---

### Heuristic

```python
Manhattan Distance
```

---

### Behavior

```text
Fast

May be suboptimal
```

---

## SPEC-066

### Formula

```python
priority = heuristic
```

---

### Ignore

```text
Actual path cost
```

---

# P00-T18 — A*

---

## SPEC-067

### File

```text
app/ai/astar.py
```

---

### Function

```python
astar(
    grid,
    start,
    goal
)
```

---

### Formula

```python
f(n)=g(n)+h(n)
```

---

### Components

```python
g = path cost

h = heuristic
```

---

## SPEC-068

### Heuristic

```python
Manhattan Distance
```

---

### Requirement

```text
Admissible

Consistent
```

---

## SPEC-069

### Risk-Aware Mode

Formula

```python
edge_cost =
1 +
risk_cost
```

---

### Goal

```text
Prefer safer routes
```

---

## SPEC-070

### Dynamic Replanning

Trigger

```text
Fire spread changes map
```

---

### Actions

```text
Abort old path

Recompute path

Replace current route
```

---

## SPEC-071

### Benchmark Metrics

Collect

```python
expanded_nodes

execution_time

path_cost

path_length
```

---

### Used For

```text
Algorithm comparison panel
```

---

# END OF PART 3

Covered:

```text
P00-T12 Core Engine

P00-T13 BFS

P00-T14 DFS

P00-T15 UCS

P00-T16 Dijkstra

P00-T17 Greedy

P00-T18 A*

P00-T19 Shared AI Utilities
```

Next:

```text
P00-T20 Simulation Lifecycle

P00-T21 Validation System

P00-T22 Logging System

P00-T23 Grid Renderer

P00-T24 Sidebar UI

P00-T25 Input Controls
```
# 03_execution_specs.md (PART 3)

# P00-T12 — CORE ENGINE

---

## SPEC-042

### Component

Engine

### File

```text
app/core/engine.py
```

### Class

```python
class Engine
```

---

### Responsibilities

```text
Own GameState

Own Snapshot

Coordinate Fire

Coordinate Rescue

Coordinate AI

Coordinate UI Requests
```

---

### Architectural Rule

```text
Engine is the only component allowed
to mutate GameState.
```

---

## SPEC-043

### Constructor

```python
Engine(
    state: GameState
)
```

---

### Internal Dependencies

```python
Grid

FireManager

RiskMap

MovementService

RescueService
```

---

### State Ownership

```text
Engine owns:

current_state

snapshot

current_algorithm
```

---

## SPEC-044

### Function

```python
start()
```

---

### Preconditions

```text
State = IDLE or EDIT

Validation passed

Snapshot exists
```

---

### Actions

```text
current_mode = RUNNING
```

---

## SPEC-045

### Function

```python
pause()
```

---

### Preconditions

```text
current_mode = RUNNING
```

---

### Actions

```text
current_mode = PAUSED
```

---

## SPEC-046

### Function

```python
resume()
```

---

### Preconditions

```text
current_mode = PAUSED
```

---

### Actions

```text
current_mode = RUNNING
```

---

## SPEC-047

### Function

```python
reset()
```

---

### Algorithm

```text
Load snapshot

Replace current state

Reset timers

Reset runtime counters
```

---

### Complexity

```text
O(N)
```

---

## SPEC-048

### Function

```python
simulation_step()
```

---

### Execution Order

```text
1 AI decision

2 Robot movement

3 Rescue logic

4 Fire tick

5 Risk update

6 Statistics update

7 End-state evaluation
```

---

### Important

```text
Order must never change.
```

---

## SPEC-049

### Function

```python
evaluate_terminal_conditions()
```

---

### Success Conditions

```text
All victims rescued
```

---

### Failure Conditions

```text
Robot dead

No reachable victims

No reachable rescue station
```

---

### Result

```text
current_mode = FINISHED
```

---

# P00-T19 — SHARED AI UTILITIES

---

## SPEC-050

### File

```text
app/ai/_shared.py
```

---

## SPEC-051

### Dataclass

```python
PathResult
```

---

### Fields

```python
found: bool

path: list

cost: float

expanded_nodes: int

execution_time_ms: float
```

---

## SPEC-052

### Function

```python
reconstruct_path(
    parent_map,
    start,
    goal
)
```

---

### Algorithm

```text
Start from goal

Follow parents

Reverse path

Return path
```

---

### Complexity

```text
O(path_length)
```

---

## SPEC-053

### Function

```python
manhattan_distance(
    a,
    b
)
```

---

### Formula

```python
abs(ax-bx)+abs(ay-by)
```

---

### Usage

```text
Greedy

A*
```

---

## SPEC-054

### Function

```python
risk_cost(
    risk_value
)
```

---

### Formula

```python
cost = 1 + risk_value * K
```

---

### Default

```python
K = 10
```

---

## SPEC-055

### Function

```python
get_neighbors(
    grid,
    x,
    y
)
```

---

### Rules

```text
4-direction

No walls

No fire
```

---

# P00-T13 — BFS

---

## SPEC-056

### File

```text
app/ai/bfs.py
```

---

### Function

```python
bfs(
    grid,
    start,
    goal
)
```

---

### Data Structure

```python
collections.deque
```

---

### Expansion Order

```text
UP

RIGHT

DOWN

LEFT
```

---

### Determinism

```text
Required
```

---

## SPEC-057

### Search Logic

```text
Push start

Loop queue

Expand neighbors

Track visited

Track parent

Stop at goal
```

---

### Cost Model

```text
Uniform cost

Every move = 1
```

---

## SPEC-058

### Metrics

Collect:

```python
expanded_nodes

path_length

execution_time
```

---

# P00-T14 — DFS

---

## SPEC-059

### File

```text
app/ai/dfs.py
```

---

### Function

```python
dfs(
    grid,
    start,
    goal
)
```

---

### Data Structure

```python
stack
```

---

### Search Strategy

```text
Depth-first exploration
```

---

### Important

```text
Not guaranteed shortest path
```

---

## SPEC-060

### Metrics

Collect:

```python
expanded_nodes

path_length

execution_time
```

---

# P00-T15 — UCS

---

## SPEC-061

### File

```text
app/ai/ucs.py
```

---

### Function

```python
ucs(
    grid,
    start,
    goal
)
```

---

### Data Structure

```python
heapq
```

---

### Priority

```python
g_cost
```

---

### Expansion

```text
Lowest cumulative cost first
```

---

## SPEC-062

### Cost Model

```python
move_cost = 1
```

---

### Future Extension

```python
move_cost = risk-aware
```

---

# P00-T16 — DIJKSTRA

---

## SPEC-063

### File

```text
app/ai/dijkstra.py
```

---

### Function

```python
dijkstra(
    grid,
    start,
    goal
)
```

---

### Data Structures

```python
distance_map

priority_queue
```

---

### Formula

```python
new_cost =
current_cost +
edge_cost
```

---

## SPEC-064

### Guarantees

```text
Optimal path

Non-negative costs only
```

---

### Complexity

```text
O(E log V)
```

---

# P00-T17 — GREEDY SEARCH

---

## SPEC-065

### File

```text
app/ai/greedy.py
```

---

### Function

```python
greedy_search(
    grid,
    start,
    goal
)
```

---

### Priority

```python
h(n)
```

---

### Heuristic

```python
Manhattan Distance
```

---

### Behavior

```text
Fast

May be suboptimal
```

---

## SPEC-066

### Formula

```python
priority = heuristic
```

---

### Ignore

```text
Actual path cost
```

---

# P00-T18 — A*

---

## SPEC-067

### File

```text
app/ai/astar.py
```

---

### Function

```python
astar(
    grid,
    start,
    goal
)
```

---

### Formula

```python
f(n)=g(n)+h(n)
```

---

### Components

```python
g = path cost

h = heuristic
```

---

## SPEC-068

### Heuristic

```python
Manhattan Distance
```

---

### Requirement

```text
Admissible

Consistent
```

---

## SPEC-069

### Risk-Aware Mode

Formula

```python
edge_cost =
1 +
risk_cost
```

---

### Goal

```text
Prefer safer routes
```

---

## SPEC-070

### Dynamic Replanning

Trigger

```text
Fire spread changes map
```

---

### Actions

```text
Abort old path

Recompute path

Replace current route
```

---

## SPEC-071

### Benchmark Metrics

Collect

```python
expanded_nodes

execution_time

path_cost

path_length
```

---

### Used For

```text
Algorithm comparison panel
```

---

# END OF PART 3

Covered:

```text
P00-T12 Core Engine

P00-T13 BFS

P00-T14 DFS

P00-T15 UCS

P00-T16 Dijkstra

P00-T17 Greedy

P00-T18 A*

P00-T19 Shared AI Utilities
```

Next:

```text
P00-T20 Simulation Lifecycle

P00-T21 Validation System

P00-T22 Logging System

P00-T23 Grid Renderer

P00-T24 Sidebar UI

P00-T25 Input Controls
```
# 03_execution_specs.md (PART 5)

# P00-T24 — SIDEBAR UI

---

## SPEC-100

### Component

Sidebar

### File

```text
app/ui/sidebar.py
```

---

### Responsibilities

```text
Display controls

Display status

Forward commands to Engine

No simulation logic
```

---

## SPEC-101

### Layout

Width

```python
SIDEBAR_WIDTH = 20%
```

Grid Area

```python
GRID_AREA = 80%
```

---

### Sections

```text
Map Settings

Edit Tools

Algorithm Selection

Simulation Controls

Status Panel
```

---

## SPEC-102

### Map Settings Panel

Fields

```python
grid_width

grid_height

victim_count

rescue_station_count

fire_source_count
```

---

### Validation

```text
Apply Validator before generation
```

---

## SPEC-103

### Algorithm Selector

Supported

```python
BFS

DFS

UCS

Dijkstra

Greedy

AStar
```

---

### Output

```python
selected_algorithm
```

---

## SPEC-104

### Simulation Controls

Buttons

```python
Generate

Start

Pause

Resume

Reset
```

---

### Action Flow

```text
UI Event

↓

Engine Command

↓

Engine Mutation
```

---

### Rule

```text
Sidebar never mutates state
```

---

## SPEC-105

### Status Panel

Display

```python
current_mode

simulation_time

steps

saved_count

dead_count

remaining_victims
```

---

### Refresh

```python
Every Frame
```

---

## SPEC-106

### Carrying Indicator

Display

```python
Carrying Victim

Not Carrying
```

---

### Source

```python
Robot.carrying_victim
```

---

## SPEC-107

### Mission Result Panel

Displayed When

```python
Mode == FINISHED
```

---

### Show

```python
Success / Failure

Saved

Dead

Steps

Time

Algorithm
```

---

# P00-T25 — INPUT CONTROLS

---

## SPEC-108

### Component

InputController

### File

```text
app/ui/controls.py
```

---

### Responsibilities

```text
Handle mouse

Handle keyboard

Forward requests to Engine
```

---

## SPEC-109

### Function

```python
screen_to_grid(
    mouse_x,
    mouse_y
)
```

---

### Purpose

Convert pixel coordinates.

---

### Output

```python
(grid_x, grid_y)
```

---

## SPEC-110

### Edit Modes

Supported

```python
PLACE_WALL

PLACE_ROBOT

PLACE_VICTIM

PLACE_FIRE

PLACE_RESCUE

ERASE
```

---

### Rule

```text
Exactly one active tool
```

---

## SPEC-111

### Mouse Click Handling

Flow

```text
Mouse Click

↓

Grid Position

↓

Current Tool

↓

Engine Request
```

---

### No Direct Mutation

```text
Forbidden
```

---

## SPEC-112

### Robot Placement Rule

Allowed

```text
Only one robot exists
```

---

### Violation

```python
ValidationError
```

---

## SPEC-113

### Keyboard Shortcuts

Space

```python
Pause / Resume
```

---

R

```python
Reset
```

---

G

```python
Generate Map
```

---

ESC

```python
Exit Edit Mode
```

---

## SPEC-114

### Runtime Protection

Rule

```text
Map editing disabled while RUNNING
```

---

### Reason

```text
Prevent state corruption
```

---

# P00-T26 — UNIT TESTS

---

## SPEC-115

### Test Framework

```python
pytest
```

---

### Directory

```text
tests/
```

---

## SPEC-116

### Grid Tests

Verify

```python
get_cell()

set_cell()

in_bounds()

neighbors()

walkable()
```

---

### Coverage Target

```python
>=90%
```

---

## SPEC-117

### Movement Tests

Verify

```python
Valid movement

Wall collision

Fire collision

Boundary collision
```

---

## SPEC-118

### Rescue Tests

Verify

```python
Pickup

Drop

Carry restriction

Mission complete
```

---

## SPEC-119

### Fire Tests

Verify

```python
Spread

Wall blocking

Robot burn

Victim burn
```

---

## SPEC-120

### AI Tests

For Each Algorithm

```python
BFS

DFS

UCS

Dijkstra

Greedy

AStar
```

---

Verify

```python
Path exists

Path valid

No crash
```

---

## SPEC-121

### Snapshot Tests

Verify

```python
Create

Restore

Isolation
```

---

# P00-T27 — INTEGRATION TESTS

---

## SPEC-122

### Full Rescue Scenario

Flow

```text
Generate Map

Find Victim

Pickup

Deliver

Mission Complete
```

---

### Expected

```python
saved_count > 0
```

---

## SPEC-123

### Fire Escalation Scenario

Flow

```text
Start Simulation

Advance Time

Spread Fire
```

---

### Verify

```python
Fire Count Increased
```

---

## SPEC-124

### Dynamic Replanning Scenario

Flow

```text
Generate Path

Spread Fire

Recompute Path
```

---

### Verify

```python
New path differs
```

---

## SPEC-125

### Reset Scenario

Flow

```text
Run Simulation

Mutate State

Reset
```

---

### Verify

```python
State == Snapshot
```

---

## SPEC-126

### Algorithm Benchmark Scenario

Run

```python
BFS

DFS

UCS

Dijkstra

Greedy

AStar
```

---

Collect

```python
Path Length

Cost

Expanded Nodes

Execution Time
```

---

# P00-T28 — DOCUMENTATION

---

## SPEC-127

### Architecture Documentation

Must Include

```text
Layer Diagram

Data Flow

Dependency Graph
```

---

## SPEC-128

### Module Documentation

For Every Module

```text
Purpose

Inputs

Outputs

Dependencies
```

---

## SPEC-129

### Algorithm Documentation

Include

```text
BFS

DFS

UCS

Dijkstra

Greedy

A*
```

---

Explain

```text
Complexity

Pros

Cons

Use Cases
```

---

## SPEC-130

### User Guide

Include

```text
Installation

Controls

Map Editing

Running Simulation

Comparing Algorithms
```

---

# P00-T29 — FINAL REFACTOR

---

## SPEC-131

### Dependency Audit

Verify

```text
No circular imports
```

---

## SPEC-132

### Architecture Audit

Verify

```text
UI contains no logic

AI pure functions

Engine owns state
```

---

## SPEC-133

### Performance Audit

Target

```python
30 FPS
```

---

Maximum

```python
35x35 Grid
```

---

Input Latency

```python
<100ms
```

---

## SPEC-134

### Failure Audit

Verify Safe Handling

```python
Invalid Map

Invalid Edit

Unreachable Victim

No Rescue Route

Fire Isolation
```

---

### Result

```python
No Application Crash
```

---

## SPEC-135

### Release Checklist

Requirements

```python
All Tests Pass

Coverage >= 90%

No Critical Bugs

Documentation Complete

Performance Targets Met
```

---

### Output

```python
Release Candidate
```

---

# END OF FILE

Execution Specs Statistics

```text
135 Specifications

29 Tasks

230 Micro Tasks

Complete Execution Blueprint
```

Relationship

```text
01_tasks.md

↓

02_microtasks.md

↓

03_execution_specs.md

↓

Source Code
```
