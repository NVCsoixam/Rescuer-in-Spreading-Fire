# 14_ai_system_design.md

# PURPOSE

Tài liệu này định nghĩa kiến trúc AI chính thức của hệ thống.

AI System chịu trách nhiệm:

* Target Selection
* Path Planning
* Replanning
* Risk Evaluation
* Decision Making

AI modules phải là Pure Functions.

AI không được mutate GameState.

---

# 1. AI ARCHITECTURE

---

Overview

```text id="a001"
Mission Controller
        │
        ▼
Target Selector
        │
        ▼
Path Planner
        │
        ▼
Path Result
        │
        ▼
Engine
```

---

Rule

```text id="a002"
AI only returns decisions

Engine executes decisions
```

---

# 2. DESIGN PRINCIPLES

---

## PRINCIPLE-001

Deterministic

Given:

```text id="a003"
Same map

Same state

Same seed
```

---

Must produce:

```text id="a004"
Same path
```

---

## PRINCIPLE-002

Stateless

AI must not store:

```text id="a005"
Global state

Mutable cache

Runtime memory
```

---

## PRINCIPLE-003

Pure Function

Input

```python id="a006"
State
```

---

Output

```python id="a007"
Decision
```

---

No Side Effects

```text id="a008"
Required
```

---

# 3. AI COMPONENTS

---

## COMPONENT-001

TargetSelector

Purpose

```text id="a009"
Choose next victim
```

---

Output

```python id="a010"
victim_id
```

---

## COMPONENT-002

PathPlanner

Purpose

```text id="a011"
Generate route
```

---

Output

```python id="a012"
PathResult
```

---

## COMPONENT-003

RiskEvaluator

Purpose

```text id="a013"
Analyze danger
```

---

Input

```python id="a014"
HeatMap
```

---

Output

```python id="a015"
Risk Score
```

---

## COMPONENT-004

Replanner

Purpose

```text id="a016"
Handle dynamic changes
```

---

# 4. AI CONTRACT

---

Input

```python id="a017"
Grid

Robot Position

Victim Position

HeatMap
```

---

Output

```python id="a018"
PathResult
```

---

Standard Interface

```python id="a019"
def find_path(
    grid,
    start,
    goal,
    heatmap
) -> PathResult
```

---

# 5. PATH RESULT CONTRACT

---

Definition

```python id="a020"
@dataclass
class PathResult:

    found: bool

    path: list[Position]

    cost: float

    expanded_nodes: int

    execution_time_ms: float
```

---

Rule

```text id="a021"
All algorithms must return same DTO
```

---

# 6. TARGET SELECTION

---

Priority 1

```text id="a022"
Reachable victim
```

---

Priority 2

```text id="a023"
Lowest total cost
```

---

Priority 3

```text id="a024"
Lowest risk
```

---

Priority 4

```text id="a025"
Lowest victim_id
```

---

Reason

```text id="a026"
Deterministic tie breaking
```

---

# 7. BFS DESIGN

---

Properties

```text id="a027"
Complete

Optimal on uniform cost
```

---

Data Structure

```python id="a028"
deque
```

---

Complexity

```python id="a029"
O(V + E)
```

---

# 8. DFS DESIGN

---

Properties

```text id="a030"
Not optimal

Low memory
```

---

Data Structure

```python id="a031"
stack
```

---

Complexity

```python id="a032"
O(V + E)
```

---

# 9. UCS DESIGN

---

Properties

```text id="a033"
Optimal cost path
```

---

Data Structure

```python id="a034"
priority queue
```

---

Complexity

```python id="a035"
O(E log V)
```

---

# 10. DIJKSTRA DESIGN

---

Properties

```text id="a036"
Shortest weighted path
```

---

Data Structure

```python id="a037"
priority queue
```

---

Complexity

```python id="a038"
O(E log V)
```

---

# 11. GREEDY DESIGN

---

Heuristic

```python id="a039"
Manhattan Distance
```

---

Formula

```python id="a040"
abs(dx) + abs(dy)
```

---

Properties

```text id="a041"
Fast

Non-optimal
```

---

# 12. A* DESIGN

---

Cost Function

```python id="a042"
f(n) = g(n) + h(n)
```

---

Where

```python id="a043"
g = path cost

h = heuristic
```

---

Heuristic

```python id="a044"
Manhattan Distance
```

---

Requirement

```text id="a045"
Admissible
```

---

# 13. RISK-AWARE NAVIGATION

---

Movement Cost

```python id="a046"
base_cost = 1
```

---

Risk Penalty

```python id="a047"
risk * weight
```

---

Effective Cost

```python id="a048"
base_cost + risk_penalty
```

---

Example

```python id="a049"
1 + (0.7 * 10)

= 8
```

---

Purpose

```text id="a050"
Avoid future fire zones
```

---

# 14. REPLANNING

---

Trigger 1

```text id="a051"
Path blocked
```

---

Trigger 2

```text id="a052"
Fire spread
```

---

Trigger 3

```text id="a053"
Victim dead
```

---

Trigger 4

```text id="a054"
New target selected
```

---

Action

```text id="a055"
Recompute path
```

---

# 15. FAILURE CONDITIONS

---

Path Not Found

```python id="a056"
found = False
```

---

Goal Invalid

```python id="a057"
found = False
```

---

Blocked Environment

```python id="a058"
found = False
```

---

Rule

```text id="a059"
Never throw runtime exception
```

---

# 16. BENCHMARK METRICS

---

Collected

```python id="a060"
execution_time_ms

expanded_nodes

path_cost

path_length
```

---

Purpose

```text id="a061"
Algorithm comparison
```

---

# 17. PERFORMANCE TARGETS

---

BFS

```python id="a062"
< 100 ms
```

---

DFS

```python id="a063"
< 100 ms
```

---

UCS

```python id="a064"
< 150 ms
```

---

Dijkstra

```python id="a065"
< 150 ms
```

---

Greedy

```python id="a066"
< 100 ms
```

---

A*

```python id="a067"
< 100 ms
```

---

Target Map

```python id="a068"
20x20
```

---

# 18. FUTURE AI EXTENSIONS

---

Reserved

```text id="a069"
IDA*

D* Lite

Beam Search

Genetic Search

Q-Learning

Deep RL

Multi-Agent Rescue
```

---

Requirement

```text id="a070"
Implement PathResult contract
```

---

# 19. SUCCESS CRITERIA

AI System passes review when:

```text id="a071"
All algorithms deterministic

All algorithms return PathResult

No state mutation

Risk-aware mode works

Replanning works

Benchmark targets met
```

---

# END OF FILE

File Number

```text id="a072"
14_ai_system_design.md
```

Next File

```text id="a073"
15_ui_system_design.md
```

Purpose

```text id="a074"
UI Architecture

Renderer Design

Sidebar Design

Input System

Visualization Rules

UI-Engine Integration
```
