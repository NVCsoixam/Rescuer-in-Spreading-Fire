# 20_project_structure_final.md

# PURPOSE

Tài liệu này định nghĩa cấu trúc source code cuối cùng của toàn bộ dự án.

Đây là blueprint chính thức cho implementation.

Mọi module phải tuân thủ structure này.

---

# 1. ARCHITECTURE OVERVIEW

---

Architecture Style

```text
Layered Architecture
```

---

Core Principle

```text
UI

↓

Engine

↓

Domain Logic

↓

Infrastructure
```

---

Rule

```text
Upper layer may depend on lower layer

Lower layer must not depend on upper layer
```

---

# 2. FINAL PROJECT STRUCTURE

```text
rescue_simulation/

│
├── main.py
│
├── requirements.txt
├── README.md
├── pyproject.toml
│
├── app/
│
│   ├── config.py
│
│   ├── core/
│   │   ├── state.py
│   │   ├── snapshot.py
│   │   ├── engine.py
│   │   ├── lifecycle.py
│   │   ├── validation.py
│   │   └── events.py
│
│   ├── map/
│   │   ├── grid.py
│   │   ├── generator.py
│   │   ├── connectivity.py
│   │   └── editor.py
│
│   ├── fire/
│   │   ├── fire_sim.py
│   │   ├── heatmap.py
│   │   ├── risk.py
│   │   └── fire_rules.py
│
│   ├── rescue/
│   │   ├── pickup.py
│   │   ├── delivery.py
│   │   └── mission.py
│
│   ├── ai/
│   │   ├── _shared.py
│   │   ├── bfs.py
│   │   ├── dfs.py
│   │   ├── ucs.py
│   │   ├── dijkstra.py
│   │   ├── greedy.py
│   │   ├── astar.py
│   │   ├── target_selector.py
│   │   └── replanner.py
│
│   ├── ui/
│   │   ├── renderer.py
│   │   ├── sidebar.py
│   │   ├── controls.py
│   │   ├── overlays.py
│   │   └── benchmark_view.py
│
│   ├── benchmark/
│   │   ├── runner.py
│   │   ├── scorer.py
│   │   ├── metrics.py
│   │   └── reports.py
│
│   └── utils/
│       ├── logger.py
│       ├── timer.py
│       ├── profiler.py
│       └── serialization.py
│
├── tests/
│
│   ├── unit/
│   ├── integration/
│   ├── acceptance/
│   ├── regression/
│   └── performance/
│
├── docs/
│
├── logs/
│
├── benchmark/
│   └── results/
│
└── assets/
    ├── icons/
    └── maps/
```

---

# 3. MODULE RESPONSIBILITIES

---

## app/core

Purpose

```text
State ownership
```

---

Contains

```text
GameState

Engine

Lifecycle

Snapshot
```

---

Rule

```text
Single source of truth
```

---

## app/map

Purpose

```text
World generation
```

---

Contains

```text
Grid

Map Generator

Connectivity Validation
```

---

## app/fire

Purpose

```text
Hazard system
```

---

Contains

```text
Fire propagation

Heatmap

Risk calculations
```

---

## app/rescue

Purpose

```text
Mission mechanics
```

---

Contains

```text
Pickup

Delivery

Mission completion
```

---

## app/ai

Purpose

```text
Decision making
```

---

Contains

```text
Algorithms

Target selection

Replanning
```

---

## app/ui

Purpose

```text
Visualization only
```

---

Contains

```text
Renderer

Sidebar

Controls
```

---

## app/benchmark

Purpose

```text
Research framework
```

---

Contains

```text
Metrics

Scoring

Reports
```

---

# 4. DEPENDENCY RULES

---

Allowed

```text
UI -> Engine

Engine -> AI

Engine -> Fire

Engine -> Rescue

Engine -> Map
```

---

Forbidden

```text
AI -> UI

Fire -> UI

Rescue -> UI

Map -> UI
```

---

Forbidden

```text
AI -> Engine
```

---

Reason

```text
Prevent circular dependencies
```

---

# 5. IMPORT RULES

---

Good

```python
from app.ai.astar import find_path
```

---

Bad

```python
from ..ai.astar import *
```

---

Rule

```text
Explicit imports only
```

---

# 6. CONFIGURATION MANAGEMENT

---

Single File

```text
app/config.py
```

---

Contains

```python
GRID_SIZE

FPS

FIRE_INTERVAL

MAX_VICTIMS

MAX_GRID_SIZE
```

---

Rule

```text
No hardcoded constants
```

---

# 7. STATE OWNERSHIP

---

Owner

```text
Engine
```

---

Read Access

```text
UI

AI

Fire

Benchmark
```

---

Write Access

```text
Engine only
```

---

# 8. EVENT FLOW

---

Standard Flow

```text
User

↓

UI

↓

Engine

↓

Domain Logic

↓

GameState

↓

UI Refresh
```

---

Rule

```text
Unidirectional data flow
```

---

# 9. TEST STRUCTURE

---

Unit

```text
tests/unit
```

---

Integration

```text
tests/integration
```

---

Acceptance

```text
tests/acceptance
```

---

Regression

```text
tests/regression
```

---

Performance

```text
tests/performance
```

---

# 10. DOCUMENTATION STRUCTURE

---

docs/

```text
00_project_spec.md

01_tasks.md

02_microtasks.md

03_architecture.md

...

20_project_structure_final.md
```

---

Rule

```text
Documentation version controlled
```

---

# 11. FUTURE EXPANSION POINTS

---

Reserved Modules

```text
multi_agent/

rl/

network/

cloud/

analytics/
```

---

Requirement

```text
Backward compatible
```

---

# 12. CODE QUALITY REQUIREMENTS

---

Lint

```bash
ruff
```

---

Formatting

```bash
black
```

---

Typing

```python
mypy
```

---

Coverage

```text
>= 90%
```

---

# 13. RELEASE CRITERIA

---

Version 1.0 Ready When

```text
All core features implemented

All tests passing

Benchmark operational

Documentation complete

Performance targets met
```

---

# 14. IMPLEMENTATION ORDER

---

Phase 1

```text
Core State
```

---

Phase 2

```text
Map System
```

---

Phase 3

```text
Fire System
```

---

Phase 4

```text
Rescue System
```

---

Phase 5

```text
AI Algorithms
```

---

Phase 6

```text
Engine
```

---

Phase 7

```text
UI
```

---

Phase 8

```text
Benchmark
```

---

Phase 9

```text
Testing
```

---

# 15. SUCCESS CRITERIA

Project Structure passes review when:

```text
No circular dependencies

Clear ownership

Scalable architecture

Testable modules

Maintainable codebase

Future extensions possible
```

---

# END OF FILE

File Number

```text
20_project_structure_final.md
```

Next File

```text
21_implementation_guidelines.md
```

Purpose

```text
Coding Standards

Naming Conventions

Dataclass Rules

Typing Rules

Development Workflow

Code Review Checklist
```
