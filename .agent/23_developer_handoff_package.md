# 23_developer_handoff_package.md

# PURPOSE

Đây là tài liệu handoff chính thức.

Mục tiêu:

* Cho phép developer mới tham gia dự án trong vài phút
* Cho phép Coding Agent tiếp tục implementation không mất context
* Là điểm bắt đầu duy nhất của dự án

---

# 1. PROJECT SUMMARY

---

Project Name

```text id="dh001"
2D Rescue Simulation System
```

---

Type

```text id="dh002"
AI Simulation

Pathfinding Research

Dynamic Environment
```

---

Goal

```text id="dh003"
Compare AI algorithms
inside a rescue environment
with dynamic fire propagation.
```

---

# 2. CORE CONCEPT

---

System is NOT

```text id="dh004"
Maze Solver
```

---

System IS

```text id="dh005"
Dynamic Rescue Simulation
```

---

Features

```text id="dh006"
Robot

Victims

Fire

Rescue Station

Risk Map

Pathfinding AI
```

---

# 3. PRIMARY OBJECTIVES

---

Objective 1

```text id="dh007"
Save victims
```

---

Objective 2

```text id="dh008"
Avoid fire
```

---

Objective 3

```text id="dh009"
Minimize risk
```

---

Objective 4

```text id="dh010"
Benchmark algorithms
```

---

# 4. SYSTEM CAPABILITIES

---

Current Scope

```text id="dh011"
Single Robot

Multiple Victims

Dynamic Fire

Multiple Algorithms

Benchmark Framework
```

---

Out Of Scope v1

```text id="dh012"
Multi-agent rescue

Networking

Cloud deployment

Machine learning
```

---

# 5. PROJECT DOCUMENT INDEX

---

Mandatory Reading Order

```text id="dh013"
00_project_spec.md

01_tasks.md

02_microtasks.md

03_architecture.md

04_domain_model.md

05_state_machine.md

06_map_generation.md

07_fire_system.md

08_rescue_system.md

09_ai_framework.md

10_pathfinding_algorithms.md

11_engine_design.md

12_benchmark_design.md

13_testing_strategy.md

14_performance_requirements.md

15_ui_system_design.md

16_logging_monitoring.md

17_error_handling.md

18_test_cases_catalog.md

19_benchmark_framework.md

20_project_structure_final.md

21_implementation_guidelines.md

22_agent_execution_protocol.md
```

---

# 6. IMPLEMENTATION STATUS TRACKING

---

Status Types

```text id="dh014"
NOT_STARTED

IN_PROGRESS

BLOCKED

DONE
```

---

Tracking File

```text id="dh015"
project_status.md
```

---

Example

```text id="dh016"
P00-T01 DONE

P00-T02 DONE

P00-T03 IN_PROGRESS
```

---

# 7. DEVELOPMENT ENTRY POINT

---

Start Here

```text id="dh017"
main.py
```

---

Boot Sequence

```text id="dh018"
main.py

↓

Engine

↓

GameState

↓

Renderer
```

---

# 8. REQUIRED ENVIRONMENT

---

Language

```text id="dh019"
Python 3.12+
```

---

Libraries

```text id="dh020"
pygame

pytest

mypy

ruff

black
```

---

Install

```bash id="dh021"
pip install -r requirements.txt
```

---

# 9. PHASE EXECUTION PLAN

---

Phase 0

```text id="dh022"
Foundation
```

---

Phase 1

```text id="dh023"
State Models
```

---

Phase 2

```text id="dh024"
Grid + Map
```

---

Phase 3

```text id="dh025"
Fire System
```

---

Phase 4

```text id="dh026"
Rescue Logic
```

---

Phase 5

```text id="dh027"
AI Algorithms
```

---

Phase 6

```text id="dh028"
Engine
```

---

Phase 7

```text id="dh029"
UI
```

---

Phase 8

```text id="dh030"
Benchmark
```

---

Phase 9

```text id="dh031"
Testing
```

---

# 10. DEPENDENCY MAP

---

```text id="dh032"
State

↓

Grid

↓

Map Generator

↓

Fire

↓

Rescue

↓

AI

↓

Engine

↓

UI

↓

Benchmark
```

---

Rule

```text id="dh033"
Bottom dependency must exist first
```

---

# 11. QUALITY REQUIREMENTS

---

Coverage

```python id="dh034"
>= 90%
```

---

Critical Modules

```python id="dh035"
100%
```

---

Lint

```text id="dh036"
Required
```

---

Typing

```text id="dh037"
Required
```

---

# 12. PERFORMANCE TARGETS

---

Simulation

```python id="dh038"
30 FPS minimum
```

---

Pathfinding

```python id="dh039"
< 100 ms
```

---

Fire Tick

```python id="dh040"
< 10 ms
```

---

Grid Size

```python id="dh041"
35x35
```

---

# 13. FAILURE POLICY

---

System Must Never

```text id="dh042"
Crash
```

---

Instead

```text id="dh043"
Log

Recover

Continue
```

---

Reference

```text id="dh044"
17_error_handling.md
```

---

# 14. CODING RULES SUMMARY

---

Required

```text id="dh045"
Type hints

Tests

Dataclasses

Structured logging
```

---

Forbidden

```text id="dh046"
Wildcard imports

Magic numbers

Silent failures
```

---

# 15. BENCHMARK OBJECTIVES

---

Algorithms

```text id="dh047"
BFS

DFS

UCS

Dijkstra

Greedy

A*
```

---

Metrics

```text id="dh048"
Success Rate

Execution Time

Expanded Nodes

Victims Saved

Risk
```

---

# 16. RELEASE CHECKLIST

---

Before Release

```text id="dh049"
All tests pass

Coverage achieved

Benchmark completed

Documentation complete

Performance targets met
```

---

# 17. PROJECT RISKS

---

Risk 1

```text id="dh050"
Fire recomputation overhead
```

---

Mitigation

```text id="dh051"
Incremental updates
```

---

Risk 2

```text id="dh052"
AI replanning cost
```

---

Mitigation

```text id="dh053"
Cached path segments
```

---

Risk 3

```text id="dh054"
State corruption
```

---

Mitigation

```text id="dh055"
Snapshot system
```

---

# 18. FUTURE ROADMAP

---

Version 2

```text id="dh056"
Multi-agent rescue
```

---

Version 3

```text id="dh057"
Reinforcement Learning
```

---

Version 4

```text id="dh058"
Distributed Simulation
```

---

Version 5

```text id="dh059"
Research Platform
```

---

# 19. HANDOFF CHECKLIST

---

New Developer Must Understand

```text id="dh060"
Architecture

State Model

Fire System

AI Framework

Engine Lifecycle

Benchmark Process
```

---

Before Coding

```text id="dh061"
Read documents

Review task registry

Check status file
```

---

# 20. FINAL SUCCESS DEFINITION

Project is successful when:

```text id="dh062"
Simulation stable

Algorithms comparable

Benchmark reproducible

Documentation complete

Codebase maintainable
```

---

# END OF FILE

File Number

```text id="dh063"
23_developer_handoff_package.md
```

Next File

```text id="dh064"
24_project_status_template.md
```

Purpose

```text id="dh065"
Task Tracking

Progress Dashboard

Blocked Items

Milestone Status

Developer Reporting Format
```
