# 18_test_cases_catalog.md

# PURPOSE

Tài liệu này định nghĩa toàn bộ Test Catalog chính thức của dự án.

Mục tiêu:

* Quality Assurance
* Regression Prevention
* Acceptance Validation
* Performance Verification

Tài liệu này là nguồn sự thật duy nhất cho QA.

---

# 1. TEST STRATEGY

---

Testing Pyramid

```text
          E2E
           ▲
           │
    Integration
           ▲
           │
       Unit Test
```

---

Target

```text
70% Unit

20% Integration

10% E2E
```

---

# 2. TEST CLASSIFICATION

---

Category A

```text
Unit Tests
```

---

Category B

```text
Integration Tests
```

---

Category C

```text
Acceptance Tests
```

---

Category D

```text
Regression Tests
```

---

Category E

```text
Stress Tests
```

---

# 3. UNIT TESTS — STATE LAYER

---

## TC-001

Position Creation

Purpose

```text
Valid coordinates accepted
```

---

Input

```python
Position(5, 10)
```

---

Expected

```python
x == 5

y == 10
```

---

## TC-002

Invalid Position

Input

```python
Position(-1, 5)
```

---

Expected

```text
ValidationError
```

---

## TC-003

GameState Initialization

Expected

```text
State created successfully
```

---

# 4. UNIT TESTS — GRID

---

## TC-004

Cell Read

Expected

```text
Correct cell returned
```

---

## TC-005

Cell Write

Expected

```text
Cell updated
```

---

## TC-006

Out Of Bounds Access

Expected

```text
Safe failure
```

---

## TC-007

Neighbor Discovery

Expected

```text
4-direction neighbors
```

---

# 5. UNIT TESTS — MAP GENERATOR

---

## TC-008

Map Creation

Expected

```text
Map generated
```

---

## TC-009

Connectivity Validation

Expected

```text
All required areas reachable
```

---

## TC-010

Robot Exists

Expected

```text
Exactly one robot
```

---

## TC-011

Victim Exists

Expected

```text
At least one victim
```

---

## TC-012

Fire Source Exists

Expected

```text
At least one fire source
```

---

# 6. UNIT TESTS — FIRE SYSTEM

---

## TC-013

Fire Expansion

Input

```text
Single fire source
```

---

Expected

```text
Fire spreads correctly
```

---

## TC-014

Wall Blocking

Expected

```text
Fire does not cross walls
```

---

## TC-015

Boundary Handling

Expected

```text
No out-of-bounds spread
```

---

## TC-016

Duplicate Fire Prevention

Expected

```text
No duplicated fire cells
```

---

## TC-017

Risk Calculation

Expected

```text
Correct risk values
```

---

# 7. UNIT TESTS — RESCUE SYSTEM

---

## TC-018

Victim Pickup

Expected

```text
Victim becomes CARRIED
```

---

## TC-019

Victim Delivery

Expected

```text
Victim becomes RESCUED
```

---

## TC-020

Multiple Carry Attempt

Expected

```text
Rejected
```

---

## TC-021

Dead Victim Delivery

Expected

```text
Rejected
```

---

# 8. UNIT TESTS — AI

---

## TC-022

BFS Path Exists

Expected

```text
Path found
```

---

## TC-023

DFS Path Exists

Expected

```text
Path found
```

---

## TC-024

UCS Optimality

Expected

```text
Lowest cost path
```

---

## TC-025

Dijkstra Optimality

Expected

```text
Lowest weighted path
```

---

## TC-026

Greedy Execution

Expected

```text
Fast valid path
```

---

## TC-027

A* Execution

Expected

```text
Optimal path
```

---

## TC-028

Unreachable Goal

Expected

```python
found=False
```

---

# 9. INTEGRATION TESTS

---

## TC-029

Engine + AI

Expected

```text
Path generated and executed
```

---

## TC-030

Engine + Fire

Expected

```text
Fire updates state correctly
```

---

## TC-031

Engine + Rescue

Expected

```text
Victim rescued end-to-end
```

---

## TC-032

Engine + Snapshot

Expected

```text
Reset restores state
```

---

# 10. ACCEPTANCE TESTS

---

## TC-033

Complete Rescue Mission

Expected

```text
Mission success
```

---

## TC-034

Robot Death

Expected

```text
Mission failure
```

---

## TC-035

All Victims Burned

Expected

```text
Mission failure
```

---

## TC-036

Mixed Outcome

Expected

```text
Partial rescue statistics correct
```

---

# 11. REGRESSION TESTS

---

Purpose

```text
Prevent previously fixed bugs
```

---

## TC-037

Repeated Reset

Expected

```text
Always deterministic
```

---

## TC-038

Repeated Fire Tick

Expected

```text
No duplication
```

---

## TC-039

Repeated Replanning

Expected

```text
Stable execution
```

---

# 12. STRESS TESTS

---

## TC-040

Maximum Grid

Input

```text
35x35
```

---

Expected

```text
System remains responsive
```

---

## TC-041

Maximum Victims

Input

```text
100 victims
```

---

Expected

```text
No crash
```

---

## TC-042

Large Fire Cluster

Expected

```text
Stable fire propagation
```

---

## TC-043

100 Consecutive Runs

Expected

```text
No memory leak
```

---

# 13. PERFORMANCE TESTS

---

## TC-044

FPS Validation

Expected

```python
fps >= 30
```

---

## TC-045

Pathfinding Budget

Expected

```python
< 100 ms
```

---

## TC-046

Fire Tick Budget

Expected

```python
< 10 ms
```

---

## TC-047

Heatmap Budget

Expected

```python
< 20 ms
```

---

# 14. ERROR HANDLING TESTS

---

## TC-048

Invalid Map

Expected

```text
Validation failure
```

---

## TC-049

Missing Robot

Expected

```text
Validation failure
```

---

## TC-050

Snapshot Missing

Expected

```text
SnapshotError
```

---

## TC-051

Illegal State Transition

Expected

```text
InvalidStateTransition
```

---

# 15. TEST COVERAGE REQUIREMENTS

---

Minimum Coverage

```python
90%
```

---

Critical Modules

```python
100%
```

for:

```text
Engine

Fire

AI

Rescue
```

---

# 16. AUTOMATION REQUIREMENTS

---

Framework

```python
pytest
```

---

Command

```bash
pytest -v
```

---

CI Requirement

```text
All tests pass before merge
```

---

# 17. RELEASE GATE

Build cannot be released if:

```text
Any critical test fails

Coverage below threshold

Performance targets missed
```

---

# 18. SUCCESS CRITERIA

Test Suite passes review when:

```text
All modules covered

Acceptance tests pass

Regression tests pass

Performance validated

Automation operational
```

---

# END OF FILE

File Number

```text
18_test_cases_catalog.md
```

Next File

```text
19_benchmark_framework.md
```

Purpose

```text
Algorithm Comparison Framework

Scoring System

Benchmark Dataset

Performance Ranking

Research Evaluation Metrics
```
