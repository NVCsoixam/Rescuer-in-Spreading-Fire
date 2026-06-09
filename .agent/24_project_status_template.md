# 24_project_status_template.md

# PURPOSE

Tài liệu này định nghĩa hệ thống theo dõi tiến độ chính thức của dự án.

Mục tiêu:

* Theo dõi trạng thái implementation
* Quản lý milestone
* Quản lý blocker
* Hỗ trợ AI Agent và Developer đồng bộ trạng thái

Đây là tài liệu được cập nhật xuyên suốt vòng đời dự án.

---

# 1. PROJECT INFORMATION

---

Project

```text id="ps001"
2D Rescue Simulation System
```

---

Version

```text id="ps002"
v1.0
```

---

Current Phase

```text id="ps003"
NOT_STARTED
```

---

Current Task

```text id="ps004"
NONE
```

---

Last Updated

```text id="ps005"
YYYY-MM-DD
```

---

# 2. STATUS LEGEND

---

Available Status

```text id="ps006"
NOT_STARTED
```

Meaning

```text id="ps007"
Task chưa bắt đầu
```

---

```text id="ps008"
IN_PROGRESS
```

Meaning

```text id="ps009"
Đang thực hiện
```

---

```text id="ps010"
BLOCKED
```

Meaning

```text id="ps011"
Bị chặn bởi dependency
```

---

```text id="ps012"
REVIEW
```

Meaning

```text id="ps013"
Chờ review
```

---

```text id="ps014"
DONE
```

Meaning

```text id="ps015"
Hoàn thành
```

---

# 3. PHASE TRACKER

---

| Phase | Name            | Status      |
| ----- | --------------- | ----------- |
| P00   | Foundation      | NOT_STARTED |
| P01   | Core Data Layer | NOT_STARTED |
| P02   | Map System      | NOT_STARTED |
| P03   | Fire System     | NOT_STARTED |
| P04   | Rescue System   | NOT_STARTED |
| P05   | AI Layer        | NOT_STARTED |
| P06   | Engine          | NOT_STARTED |
| P07   | UI              | NOT_STARTED |
| P08   | Benchmark       | NOT_STARTED |
| P09   | Testing         | NOT_STARTED |

---

# 4. TASK TRACKER

---

## FOUNDATION

| Task ID | Description       | Status      |
| ------- | ----------------- | ----------- |
| P00-T01 | Project Bootstrap | NOT_STARTED |
| P00-T02 | Tooling Setup     | NOT_STARTED |
| P00-T03 | Global Config     | NOT_STARTED |

---

## CORE DATA

| Task ID | Description     | Status      |
| ------- | --------------- | ----------- |
| P00-T04 | State Models    | NOT_STARTED |
| P00-T05 | Snapshot System | NOT_STARTED |
| P00-T06 | Grid System     | NOT_STARTED |
| P00-T07 | Map Generator   | NOT_STARTED |

---

## SIMULATION

| Task ID | Description     | Status      |
| ------- | --------------- | ----------- |
| P00-T08 | Movement Logic  | NOT_STARTED |
| P00-T09 | Rescue System   | NOT_STARTED |
| P00-T10 | Fire Simulation | NOT_STARTED |
| P00-T11 | Heatmap System  | NOT_STARTED |
| P00-T12 | Core Engine     | NOT_STARTED |

---

## AI

| Task ID | Description      | Status      |
| ------- | ---------------- | ----------- |
| P00-T13 | BFS              | NOT_STARTED |
| P00-T14 | DFS              | NOT_STARTED |
| P00-T15 | UCS              | NOT_STARTED |
| P00-T16 | Dijkstra         | NOT_STARTED |
| P00-T17 | Greedy           | NOT_STARTED |
| P00-T18 | A*               | NOT_STARTED |
| P00-T19 | Shared Utilities | NOT_STARTED |

---

## VALIDATION

| Task ID | Description | Status      |
| ------- | ----------- | ----------- |
| P00-T20 | Lifecycle   | NOT_STARTED |
| P00-T21 | Validation  | NOT_STARTED |
| P00-T22 | Logging     | NOT_STARTED |

---

## UI

| Task ID | Description   | Status      |
| ------- | ------------- | ----------- |
| P00-T23 | Grid Renderer | NOT_STARTED |
| P00-T24 | Sidebar       | NOT_STARTED |
| P00-T25 | Controls      | NOT_STARTED |

---

## TESTING

| Task ID | Description       | Status      |
| ------- | ----------------- | ----------- |
| P00-T26 | Unit Tests        | NOT_STARTED |
| P00-T27 | Integration Tests | NOT_STARTED |

---

## FINALIZATION

| Task ID | Description   | Status      |
| ------- | ------------- | ----------- |
| P00-T28 | Documentation | NOT_STARTED |
| P00-T29 | Refactor      | NOT_STARTED |

---

# 5. CURRENT SPRINT

---

Sprint Name

```text id="ps016"
Sprint-01
```

---

Sprint Goal

```text id="ps017"
Build Foundation Layer
```

---

Tasks

```text id="ps018"
P00-T01

P00-T02

P00-T03
```

---

Sprint Status

```text id="ps019"
NOT_STARTED
```

---

# 6. BLOCKERS

---

Format

```text id="ps020"
BLOCKER-ID

Task

Description

Resolution
```

---

Example

```text id="ps021"
BLK-001

P00-T10

Grid API missing

Implement P00-T06 first
```

---

Current Blockers

```text id="ps022"
NONE
```

---

# 7. COMPLETED TASKS

---

Format

```text id="ps023"
Task ID

Completion Date

Notes
```

---

Example

```text id="ps024"
P00-T01

2026-06-01

Bootstrap complete
```

---

# 8. QUALITY DASHBOARD

---

Coverage

```python id="ps025"
0%
```

---

Lint

```text id="ps026"
UNKNOWN
```

---

Typing

```text id="ps027"
UNKNOWN
```

---

Benchmark

```text id="ps028"
NOT_RUN
```

---

# 9. PERFORMANCE DASHBOARD

---

FPS

```text id="ps029"
N/A
```

---

Fire Tick

```text id="ps030"
N/A
```

---

Pathfinding

```text id="ps031"
N/A
```

---

Memory Usage

```text id="ps032"
N/A
```

---

# 10. RELEASE READINESS

---

Documentation

```text id="ps033"
0%
```

---

Implementation

```text id="ps034"
0%
```

---

Tests

```text id="ps035"
0%
```

---

Release Status

```text id="ps036"
NOT_READY
```

---

# 11. AGENT REPORT FORMAT

---

Every Agent Update Must Follow

```text id="ps037"
TASK

STATUS

FILES

TESTS

NOTES
```

---

Example

```text id="ps038"
TASK:
P00-T04

STATUS:
DONE

FILES:
state.py

TESTS:
PASS

NOTES:
State model complete
```

---

# 12. MILESTONE TRACKER

---

Milestone M1

```text id="ps039"
Foundation Complete
```

---

Milestone M2

```text id="ps040"
Simulation Running
```

---

Milestone M3

```text id="ps041"
AI Operational
```

---

Milestone M4

```text id="ps042"
UI Complete
```

---

Milestone M5

```text id="ps043"
Benchmark Ready
```

---

Milestone M6

```text id="ps044"
Release Candidate
```

---

# 13. PROJECT HEALTH SCORE

---

Formula

```python id="ps045"
health_score =

implementation_progress

+

test_progress

+

documentation_progress
```

---

Range

```python id="ps046"
0 → 100
```

---

Interpretation

```text id="ps047"
0-30   Critical

31-60  Risky

61-80  Healthy

81-100 Excellent
```

---

# 14. SUCCESS CRITERIA

Status Tracking passes review when:

```text id="ps048"
Progress visible

Dependencies tracked

Blockers tracked

Milestones visible

Release readiness measurable
```

---

# END OF FILE

File Number

```text id="ps049"
24_project_status_template.md
```

Next File

```text id="ps050"
25_release_readiness_checklist.md
```

Purpose

```text id="ps051"
Production Checklist

Pre-Release Validation

Quality Gates

Deployment Approval Criteria

Final Acceptance Checklist
```
