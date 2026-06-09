# 05_api_contracts.md

# PURPOSE

Tài liệu này định nghĩa toàn bộ contract giữa các module.

Mọi module phải triển khai đúng interface.

Không được thay đổi signature nếu chưa cập nhật contract.

---

# 1. CONTRACT RULES

---

## Rule 1

All modules communicate through:

```text id="4z3b0v"
DTO

Dataclass

Return Object
```

---

## Rule 2

Never return raw dictionaries.

Forbidden:

```python
return {
    "x": x,
    "y": y
}
```

---

Required:

```python
return Position(
    x=x,
    y=y
)
```

---

## Rule 3

Exceptions are explicit.

Allowed:

```python
ValidationError

PathNotFoundError

InvalidStateTransition
```

---

Forbidden:

```python
Exception
```

---

# 2. SHARED DTOs

---

## DTO-001

### Position

File

```text id="m2r8bo"
app/core/state.py
```

---

Definition

```python
@dataclass
class Position:
    x: int
    y: int
```

---

Purpose

```text id="x0vbdp"
Universal coordinate object
```

---

# DTO-002

### PathResult

File

```text id="6z63p3"
app/ai/_shared.py
```

---

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

```text id="k2z2jf"
Standard output for all AI algorithms
```

---

# DTO-003

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

```text id="bskv6r"
Validation subsystem result
```

---

# DTO-004

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

```text id="nm1wbl"
Simulation final report
```

---

# 3. GRID CONTRACTS

---

## CONTRACT-001

### get_cell()

Signature

```python
def get_cell(
    x: int,
    y: int
) -> Cell | None
```

---

Success

```text id="hcvruj"
Return Cell
```

---

Failure

```text id="txsj0x"
Return None
```

---

## CONTRACT-002

### set_cell()

Signature

```python
def set_cell(
    x: int,
    y: int,
    value: Cell
) -> None
```

---

Failure

```python
raise ValueError
```

---

## CONTRACT-003

### get_neighbors()

Signature

```python
def get_neighbors(
    x: int,
    y: int
) -> list[Position]
```

---

Ordering

```text id="07omw0"
UP

RIGHT

DOWN

LEFT
```

---

# 4. MOVEMENT CONTRACTS

---

## CONTRACT-004

### move()

Signature

```python
def move(
    state: GameState,
    direction: tuple[int, int]
) -> bool
```

---

Returns

```python
True
```

Movement success

---

```python
False
```

Movement blocked

---

Side Effects

```text id="nk1s44"
Robot position update

Step counter update
```

---

# 5. RESCUE CONTRACTS

---

## CONTRACT-005

### pickup_victim()

Signature

```python
def pickup_victim(
    state: GameState
) -> bool
```

---

Returns

```python
True
```

Victim picked

---

```python
False
```

No victim available

---

## CONTRACT-006

### drop_victim()

Signature

```python
def drop_victim(
    state: GameState
) -> bool
```

---

Returns

```python
True
```

Victim rescued

---

```python
False
```

Drop failed

---

# 6. FIRE CONTRACTS

---

## CONTRACT-007

### tick()

Signature

```python
def tick(
    state: GameState
) -> None
```

---

Effects

```text id="dxo6w2"
Spread fire

Burn victims

Burn robot

Update fire cells
```

---

## CONTRACT-008

### recalculate()

Signature

```python
def recalculate(
    state: GameState
) -> None
```

---

Effects

```text id="bj3ehm"
Update risk map
```

---

# 7. AI CONTRACTS

---

## CONTRACT-009

### BFS

Signature

```python
def bfs(
    grid,
    start: Position,
    goal: Position
) -> PathResult
```

---

## CONTRACT-010

### DFS

Signature

```python
def dfs(
    grid,
    start: Position,
    goal: Position
) -> PathResult
```

---

## CONTRACT-011

### UCS

Signature

```python
def ucs(
    grid,
    start: Position,
    goal: Position
) -> PathResult
```

---

## CONTRACT-012

### Dijkstra

Signature

```python
def dijkstra(
    grid,
    start: Position,
    goal: Position
) -> PathResult
```

---

## CONTRACT-013

### Greedy

Signature

```python
def greedy_search(
    grid,
    start: Position,
    goal: Position
) -> PathResult
```

---

## CONTRACT-014

### A*

Signature

```python
def astar(
    grid,
    start: Position,
    goal: Position
) -> PathResult
```

---

# Contract Requirement

All AI modules MUST return:

```python
PathResult
```

---

Never:

```python
list

tuple

dict
```

---

# 8. ENGINE CONTRACTS

---

## CONTRACT-015

### start()

Signature

```python
def start() -> bool
```

---

Returns

```python
True
```

Simulation started

---

```python
False
```

Validation failed

---

## CONTRACT-016

### pause()

Signature

```python
def pause() -> None
```

---

## CONTRACT-017

### resume()

Signature

```python
def resume() -> None
```

---

## CONTRACT-018

### reset()

Signature

```python
def reset() -> None
```

---

## CONTRACT-019

### simulation_step()

Signature

```python
def simulation_step() -> None
```

---

# 9. VALIDATOR CONTRACTS

---

## CONTRACT-020

### validate_grid()

```python
def validate_grid() -> ValidationReport
```

---

## CONTRACT-021

### validate_entities()

```python
def validate_entities() -> ValidationReport
```

---

## CONTRACT-022

### validate_reachability()

```python
def validate_reachability() -> ValidationReport
```

---

# 10. UI CONTRACTS

---

## CONTRACT-023

### Renderer

Signature

```python
def render(
    state: GameState
) -> None
```

---

Rule

```text id="b2b4bq"
Read-only access
```

---

## CONTRACT-024

### Sidebar

Signature

```python
def update(
    state: GameState
) -> None
```

---

Rule

```text id="6jcv1x"
Read-only access
```

---

## CONTRACT-025

### Input Controller

Signature

```python
def handle_event(
    event
) -> None
```

---

Flow

```text id="9wtv6l"
Event

↓

Engine Command

↓

Engine Mutation
```

---

# 11. ERROR CONTRACTS

---

## ERROR-001

ValidationError

Purpose

```text id="ec4vkr"
Configuration invalid
```

---

## ERROR-002

PathNotFoundError

Purpose

```text id="u1d3kx"
No valid route exists
```

---

## ERROR-003

InvalidStateTransition

Purpose

```text id="m0ldwq"
Lifecycle violation
```

---

## ERROR-004

SnapshotError

Purpose

```text id="g3rkkt"
Snapshot restore failure
```

---

# 12. CONTRACT SUCCESS CRITERIA

System passes contract review when:

```text id="7knx6i"
All modules compile

No signature mismatch

No contract violations

No implicit interfaces

No undocumented dependencies
```

---

# END OF FILE

File Number

```text id="wz7h4q"
05_api_contracts.md
```

Next File

```text id="f45o6u"
06_state_machine.md
```

Purpose of next file:

```text id="r93xw6"
Formal lifecycle specification

State transitions

Event handling

Engine execution flow

Failure states

Recovery states
```
