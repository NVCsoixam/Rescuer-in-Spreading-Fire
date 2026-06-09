# 01_tasks.md
# Rescue Simulation 2D - Task Registry (Master Task List)

## 1. PURPOSE

File này định nghĩa toàn bộ hệ thống task của dự án dưới dạng danh sách chuẩn hóa để AI agent có thể:

- Hiểu toàn bộ pipeline build
- Biết thứ tự triển khai
- Biết dependency giữa các module
- Điều phối micro-task execution
- Không cần suy luận ngoài context

---

## 2. TASK SYSTEM OVERVIEW

Hệ thống được chia thành 6 phase chính:

1. Foundation Layer (setup + config)
2. Core Data Layer (state + snapshot)
3. Simulation Engine Layer
4. AI Pathfinding Layer
5. Fire + Rescue Logic Layer
6. UI + Integration Layer
7. Testing + Optimization Layer

---

## 3. TASK FORMAT STANDARD

Mỗi task tuân theo format:

- TASK_ID
- NAME
- TYPE (setup / core / logic / ui / test / integration)
- DESCRIPTION
- FILES AFFECTED
- DEPENDENCIES
- OUTPUT

---

## 4. PHASE 1 — FOUNDATION LAYER

### P00-T01 — Project Bootstrap
TYPE: setup  
FILES:
- main.py
- app/**init**.py

DESCRIPTION:
Tạo entry point và package structure để Python import được toàn bộ hệ thống.

DEPENDENCIES: none

OUTPUT:
Runnable empty project

---

### P00-T02 — Dependency & Tooling Setup
TYPE: setup  
FILES:
- requirements.txt
- pyproject.toml
- .gitignore
- README.md

DESCRIPTION:
Thiết lập môi trường chạy, lint, test.

DEPENDENCIES: P00-T01

OUTPUT:
Project installable via pip

---

### P00-T03 — Global Configuration System
TYPE: core  
FILES:
- app/config.py

DESCRIPTION:
Define toàn bộ constants: grid size, fire interval, UI layout, directions.

DEPENDENCIES: P00-T01

OUTPUT:
Single source of truth config

---

## 5. PHASE 2 — CORE DATA LAYER

### P00-T04 — Game State Models
TYPE: core  
FILES:
- app/core/state.py

DESCRIPTION:
Define dataclasses:
- Cell
- Robot
- Victim
- RescueStation
- GameState

DEPENDENCIES: P00-T03

OUTPUT:
Typed simulation state

---

### P00-T05 — Snapshot System
TYPE: core  
FILES:
- app/core/snapshot.py

DESCRIPTION:
Deep copy + restore GameState for reset mechanism.

DEPENDENCIES: P00-T04

OUTPUT:
Deterministic reset system

---

### P00-T06 — Grid System
TYPE: core  
FILES:
- app/map/grid.py

DESCRIPTION:
2D grid abstraction + neighbor utilities + safe access.

DEPENDENCIES: P00-T04

OUTPUT:
Stable grid API

---

### P00-T07 — Map Generator
TYPE: core  
FILES:
- app/map/generator.py

DESCRIPTION:
Generate structured maps (rooms + corridors + validation).

DEPENDENCIES: P00-T06

OUTPUT:
Playable map generator

---

## 6. PHASE 3 — SIMULATION ENGINE

### P00-T08 — Movement Logic
TYPE: logic  
FILES:
- app/logic/movement.py

DESCRIPTION:
4-direction movement rules + validation.

DEPENDENCIES: P00-T06

OUTPUT:
Robot movement system

---

### P00-T09 — Rescue System
TYPE: logic  
FILES:
- app/logic/rescue.py

DESCRIPTION:
Pickup + delivery logic (1 victim max).

DEPENDENCIES: P00-T08

OUTPUT:
Rescue mechanics

---

### P00-T10 — Fire Simulation
TYPE: core  
FILES:
- app/fire/fire_sim.py

DESCRIPTION:
Fire spread per tick + collision handling.

DEPENDENCIES: P00-T06

OUTPUT:
Dynamic fire system

---

### P00-T11 — Heat Map System
TYPE: logic  
FILES:
- app/fire/heatmap.py

DESCRIPTION:
Risk scoring layer for AI decision making.

DEPENDENCIES: P00-T10

OUTPUT:
Risk-aware environment

---

### P00-T12 — Core Engine
TYPE: core  
FILES:
- app/core/engine.py

DESCRIPTION:
Main simulation controller:
- step()
- run()
- pause()
- reset()

DEPENDENCIES:
P00-T05, P00-T08, P00-T09, P00-T10

OUTPUT:
Central simulation runtime

---

## 7. PHASE 4 — AI PATHFINDING

### P00-T13 — BFS
TYPE: ai  
FILES:
- app/ai/bfs.py

---

### P00-T14 — DFS
TYPE: ai  
FILES:
- app/ai/dfs.py

---

### P00-T15 — UCS
TYPE: ai  
FILES:
- app/ai/ucs.py

---

### P00-T16 — Dijkstra
TYPE: ai  
FILES:
- app/ai/dijkstra.py

---

### P00-T17 — Greedy Search
TYPE: ai  
FILES:
- app/ai/greedy.py

---

### P00-T18 — A* Algorithm
TYPE: ai  
FILES:
- app/ai/astar.py

---

### P00-T19 — Shared AI Utilities
TYPE: ai  
FILES:
- app/ai/_shared.py

DESCRIPTION:
Neighbor expansion, heuristic, path reconstruction.

DEPENDENCIES:
P00-T06, P00-T11

OUTPUT:
Reusable AI core

---

## 8. PHASE 5 — STATE MACHINE + VALIDATION

### P00-T20 — Simulation Lifecycle
TYPE: core  
FILES:
- app/core/state.py
- app/core/engine.py

DESCRIPTION:
Define states:
IDLE, EDIT, RUNNING, PAUSED, FINISHED

---

### P00-T21 — Validation System
TYPE: core  
FILES:
- app/core/engine.py
- app/map/generator.py

DESCRIPTION:
Validate:
- grid size
- fire interval
- robot existence
- overlaps

---

### P00-T22 — Logging System
TYPE: core  
FILES:
- engine + ai modules

DESCRIPTION:
Structured logging for debugging AI + fire + rescue.

---

## 9. PHASE 6 — UI SYSTEM

### P00-T23 — Grid Renderer
TYPE: ui  
FILES:
- app/ui/renderer.py

DESCRIPTION:
Render map + entities + overlays.

---

### P00-T24 — Sidebar UI
TYPE: ui  
FILES:
- app/ui/sidebar.py

DESCRIPTION:
Control panel (map settings, run mode, status).

---

### P00-T25 — Input Controls
TYPE: ui  
FILES:
- app/ui/controls.py

DESCRIPTION:
Click-to-edit system.

---

## 10. PHASE 7 — TESTING

### P00-T26 — Unit Tests
TYPE: test  
FILES:
- tests/test_*.py

---

### P00-T27 — Integration Tests
TYPE: test  
FILES:
- tests/test_integration_simulation.py

---

## 11. PHASE 8 — FINALIZATION

### P00-T28 — Documentation
TYPE: integration  
FILES:
- docs/*.md

---

### P00-T29 — Final Refactor
TYPE: optimization  
FILES:
- app/**/*.py

---

## 12. EXECUTION ORDER (CRITICAL)

1. P00-T01 → P00-T02
2. P00-T03
3. P00-T04 → P00-T06
4. P00-T07
5. P00-T08 → P00-T11
6. P00-T12
7. P00-T13 → P00-T19
8. P00-T20 → P00-T22
9. UI layer (P00-T23 → P00-T25)
10. Testing (P00-T26 → P00-T27)
11. Docs + cleanup (P00-T28 → P00-T29)

---

## 13. CRITICAL RULES

- UI NEVER contains logic
- Engine is single source of truth
- State mutation only inside engine
- AI modules are pure functions (no side effects)
- Snapshot must always exist before RUNNING state
- Fire tick is deterministic per step

---

## 14. DONE CRITERIA

Project is complete when:

- Simulation runs at ≥30 FPS
- All AI algorithms return valid path or failure
- Fire spreads correctly
- Rescue system works end-to-end
- UI reflects state correctly
- Reset restores exact snapshot