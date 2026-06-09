# 04_project_structure.md

# PURPOSE

Tài liệu này định nghĩa cấu trúc thư mục chính thức của dự án.

Mọi AI Coding Agent phải tuân thủ tuyệt đối.

Không được tự ý tạo thêm package nếu chưa có trong tài liệu này.

---

# 1. HIGH LEVEL ARCHITECTURE

```text
UI Layer
    ↓

Engine Layer
    ↓

Domain Logic Layer
    ↓

Infrastructure Layer
```

Rule:

```text
UI never talks directly to AI

UI never modifies state

Engine owns state

AI is stateless
```

---

# 2. FINAL PROJECT TREE

```text
rescue_simulation/

│
├── main.py
│
├── requirements.txt
├── pyproject.toml
├── README.md
│
├── app/
│
│   ├── config.py
│
│   ├── core/
│   │
│   │   ├── state.py
│   │   ├── snapshot.py
│   │   ├── engine.py
│   │   ├── validator.py
│   │   └── logger.py
│
│   ├── map/
│   │
│   │   ├── grid.py
│   │   └── generator.py
│
│   ├── logic/
│   │
│   │   ├── movement.py
│   │   └── rescue.py
│
│   ├── fire/
│   │
│   │   ├── fire_sim.py
│   │   └── heatmap.py
│
│   ├── ai/
│   │
│   │   ├── _shared.py
│   │   ├── bfs.py
│   │   ├── dfs.py
│   │   ├── ucs.py
│   │   ├── dijkstra.py
│   │   ├── greedy.py
│   │   └── astar.py
│
│   └── ui/
│
│       ├── renderer.py
│       ├── sidebar.py
│       └── controls.py
│
├── assets/
│
│   ├── icons/
│   ├── sprites/
│   └── fonts/
│
├── tests/
│
│   ├── test_grid.py
│   ├── test_movement.py
│   ├── test_rescue.py
│   ├── test_fire.py
│   ├── test_heatmap.py
│   ├── test_engine.py
│   ├── test_ai.py
│   └── test_integration.py
│
└── docs/
    │
    ├── architecture.md
    ├── algorithms.md
    ├── workflow.md
    └── user_guide.md
```

---

# 3. OWNERSHIP RULES

---

## app/config.py

Owner:

```text
Global Configuration
```

Responsibilities:

```text
Constants

Enums

UI Dimensions

Directions
```

Must NOT:

```text
Contain runtime logic
```

---

## app/core/

Owner:

```text
Simulation Core
```

Contains:

```text
State

Engine

Validation

Logging

Snapshot
```

Rule:

```text
Core owns simulation truth
```

---

## app/map/

Owner:

```text
Map Infrastructure
```

Contains:

```text
Grid

Generator
```

Rule:

```text
No AI logic

No UI logic
```

---

## app/logic/

Owner:

```text
Game Mechanics
```

Contains:

```text
Movement

Rescue
```

Rule:

```text
Pure mechanics only
```

---

## app/fire/

Owner:

```text
Dynamic Environment
```

Contains:

```text
Fire spread

Risk map
```

---

## app/ai/

Owner:

```text
Pathfinding
```

Contains:

```text
BFS

DFS

UCS

Dijkstra

Greedy

A*
```

Rule:

```text
Pure functions only
```

---

## app/ui/

Owner:

```text
Presentation Layer
```

Contains:

```text
Renderer

Sidebar

Input Controller
```

Rule:

```text
No game logic

No pathfinding logic

No state mutation
```

---

# 4. IMPORT RULES

---

## Allowed

UI

```text
ui
 ↓
core
```

---

Engine

```text
core
 ↓
logic
 ↓
fire
 ↓
ai
```

---

AI

```text
ai
 ↓
_shared
```

---

Map

```text
map
 ↓
config
```

---

## Forbidden

UI -> AI

```text
Forbidden
```

---

UI -> Fire

```text
Forbidden
```

---

AI -> UI

```text
Forbidden
```

---

AI -> Engine

```text
Forbidden
```

---

Fire -> UI

```text
Forbidden
```

---

# 5. DEPENDENCY GRAPH

```text
config
   │
   ▼

map
   │
   ▼

core.state
   │
   ▼

logic
fire
ai

   ▼

engine

   ▼

ui
```

---

# 6. STATE OWNERSHIP

Single Source Of Truth

```text
GameState
```

Owner

```text
Engine
```

---

Allowed

```text
Engine mutates state
```

---

Forbidden

```text
Renderer mutates state

Sidebar mutates state

AI mutates state

Fire mutates state directly

Tests mutates state bypassing engine
```

---

# 7. ASSET STRUCTURE

---

## icons/

```text
robot.png

victim.png

fire.png

rescue.png

wall.png
```

---

## sprites/

```text
robot_dead.png

victim_dead.png

victim_rescued.png
```

---

## fonts/

```text
UI font files
```

---

# 8. TEST STRUCTURE

Unit Tests

```text
One module

One test file
```

Example

```text
grid.py

↓

test_grid.py
```

---

Integration Tests

```text
Cross-module behavior
```

Example

```text
Engine
+
Fire
+
AI
+
Rescue
```

---

# 9. DOCUMENTATION STRUCTURE

architecture.md

```text
System architecture
```

---

algorithms.md

```text
AI algorithm analysis
```

---

workflow.md

```text
Simulation lifecycle
```

---

user_guide.md

```text
End-user manual
```

---

# 10. FUTURE EXPANSION STRUCTURE

Reserved Directories

```text
app/scenarios/

app/replay/

app/statistics/

app/network/

app/ml/
```

Purpose

```text
Future versions

Must remain empty in v1
```

---

# DEFINITION OF STRUCTURAL SUCCESS

Project passes structure review if:

```text
No circular imports

No architecture violations

No UI logic

No duplicated ownership

No hidden dependencies

All imports deterministic
```

---

# END OF FILE

File Number:

```text
04_project_structure.md
```

Next File:

```text
05_api_contracts.md
```

This is where every module interface, function signature, DTO, request/response object, and cross-module contract is formally defined so Coding Agents can implement modules independently without breaking integration.
