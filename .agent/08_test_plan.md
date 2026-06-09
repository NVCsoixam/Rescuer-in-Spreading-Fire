# 08_test_plan.md

# PURPOSE

Tài liệu này định nghĩa chiến lược kiểm thử chính thức cho dự án.

Mục tiêu:

* Ngăn regression
* Đảm bảo correctness
* Đảm bảo deterministic behavior
* Đảm bảo architecture compliance
* Đảm bảo production quality

---

# 1. TESTING PHILOSOPHY

---

## RULE-001

Every feature must have:

```text id="t001"
Unit Test
```

---

## RULE-002

Every subsystem must have:

```text id="t002"
Integration Test
```

---

## RULE-003

Every release must pass:

```text id="t003"
Regression Test Suite
```

---

## RULE-004

Simulation behavior must be:

```text id="t004"
Deterministic
```

---

# 2. TEST PYRAMID

---

```text id="t005"
          Acceptance

        Integration

          Unit
```

---

Target Distribution

```text id="t006"
70% Unit

20% Integration

10% Acceptance
```

---

# 3. UNIT TEST PLAN

---

# GRID TESTS

---

## TEST-001

Grid Creation

Verify

```python id="t007"
Grid(10,10)
```

Creates:

```text id="t008"
Correct dimensions

Correct cell count
```

---

## TEST-002

Bounds Check

Verify

```python id="t009"
in_bounds()
```

Returns

```text id="t010"
True for valid cells

False for invalid cells
```

---

## TEST-003

Neighbor Expansion

Verify order

```text id="t011"
UP

RIGHT

DOWN

LEFT
```

---

Reason

```text id="t012"
Deterministic pathfinding
```

---

# MOVEMENT TESTS

---

## TEST-004

Valid Movement

Expected

```text id="t013"
Robot position updated
```

---

## TEST-005

Wall Collision

Expected

```text id="t014"
Movement rejected
```

---

## TEST-006

Fire Collision

Expected

```text id="t015"
Movement rejected
```

---

## TEST-007

Step Counter

Expected

```text id="t016"
Increment only on success
```

---

# RESCUE TESTS

---

## TEST-008

Pickup Victim

Expected

```text id="t017"
Robot carrying=True
```

---

## TEST-009

Drop Victim

Expected

```text id="t018"
Victim rescued
```

---

## TEST-010

Carry Limit

Expected

```text id="t019"
Only one victim allowed
```

---

# FIRE TESTS

---

## TEST-011

Fire Spread

Expected

```text id="t020"
Neighbor cells burn
```

---

## TEST-012

Wall Blocking

Expected

```text id="t021"
Wall prevents spread
```

---

## TEST-013

Victim Burn

Expected

```text id="t022"
alive=False
```

---

## TEST-014

Robot Burn

Expected

```text id="t023"
Mission failure
```

---

# AI TESTS

---

## TEST-015

BFS Valid Path

Expected

```text id="t024"
Shortest path
```

---

## TEST-016

DFS Valid Path

Expected

```text id="t025"
Path exists
```

---

## TEST-017

UCS Optimal Cost

Expected

```text id="t026"
Lowest cost path
```

---

## TEST-018

Dijkstra Optimal Cost

Expected

```text id="t027"
Lowest cost path
```

---

## TEST-019

Greedy Path

Expected

```text id="t028"
Path exists
```

---

## TEST-020

A* Path

Expected

```text id="t029"
Optimal path
```

---

# SNAPSHOT TESTS

---

## TEST-021

Create Snapshot

Expected

```text id="t030"
Deep copy
```

---

## TEST-022

Restore Snapshot

Expected

```text id="t031"
Exact restoration
```

---

## TEST-023

Isolation

Expected

```text id="t032"
No shared references
```

---

# 4. INTEGRATION TEST PLAN

---

## TEST-024

Full Rescue Flow

Scenario

```text id="t033"
Move

Pickup

Deliver
```

---

Expected

```text id="t034"
Victim rescued
```

---

## TEST-025

Fire + Rescue

Scenario

```text id="t035"
Fire spreads during mission
```

---

Expected

```text id="t036"
State remains valid
```

---

## TEST-026

AI + Fire

Scenario

```text id="t037"
Path becomes blocked
```

---

Expected

```text id="t038"
Replanning occurs
```

---

## TEST-027

Engine + Snapshot

Scenario

```text id="t039"
Run

Reset
```

---

Expected

```text id="t040"
Original state restored
```

---

# 5. ACCEPTANCE TEST PLAN

---

## TEST-028

Small Scenario

Map

```python id="t041"
10x10
```

Expected

```text id="t042"
Simulation completes
```

---

## TEST-029

Medium Scenario

Map

```python id="t043"
20x20
```

Expected

```text id="t044"
Stable execution
```

---

## TEST-030

Large Scenario

Map

```python id="t045"
35x35
```

Expected

```text id="t046"
Performance target met
```

---

# 6. PERFORMANCE TEST PLAN

---

## TEST-031

FPS Test

Target

```python id="t047"
>= 30 FPS
```

---

## TEST-032

Input Latency

Target

```python id="t048"
<100 ms
```

---

## TEST-033

Pathfinding Runtime

Target

```python id="t049"
<100 ms
```

20x20 map

---

## TEST-034

Memory Usage

Target

```python id="t050"
<512 MB
```

---

# 7. STRESS TEST PLAN

---

## TEST-035

Maximum Grid

```python id="t051"
35x35
```

---

Expected

```text id="t052"
No crash
```

---

## TEST-036

Maximum Fire

Scenario

```text id="t053"
Many fire sources
```

---

Expected

```text id="t054"
Stable spread logic
```

---

## TEST-037

Maximum Victims

Scenario

```python id="t055"
50 victims
```

---

Expected

```text id="t056"
Simulation still responsive
```

---

# 8. REGRESSION TEST PLAN

---

## TEST-038

Movement Regression

Verify

```text id="t057"
Movement unchanged
```

---

## TEST-039

Fire Regression

Verify

```text id="t058"
Spread unchanged
```

---

## TEST-040

AI Regression

Verify

```text id="t059"
Path quality unchanged
```

---

## TEST-041

UI Regression

Verify

```text id="t060"
Rendering unchanged
```

---

# 9. ARCHITECTURE TESTS

---

## TEST-042

State Ownership

Verify

```text id="t061"
Only Engine mutates state
```

---

## TEST-043

UI Isolation

Verify

```text id="t062"
UI contains no logic
```

---

## TEST-044

AI Purity

Verify

```text id="t063"
No state mutation
```

---

## TEST-045

Import Rules

Verify

```text id="t064"
No forbidden imports
```

---

# 10. AUTOMATION

---

Framework

```python id="t065"
pytest
```

---

Coverage

```python id="t066"
pytest-cov
```

---

CI Command

```bash id="t067"
pytest --cov=app
```

---

Required Coverage

```python id="t068"
>= 90%
```

---

# 11. RELEASE GATE

Release blocked if:

```text id="t069"
Any critical test fails

Coverage below target

Performance target missed

Architecture violation found
```

---

Release allowed if:

```text id="t070"
All acceptance tests pass

All regression tests pass

Coverage >= 90%

Performance validated
```

---

# 12. SUCCESS CRITERIA

Testing phase complete when:

```text id="t071"
Unit tests pass

Integration tests pass

Acceptance tests pass

Stress tests pass

Regression tests pass

Architecture tests pass
```

---

# END OF FILE

File Number

```text id="t072"
08_test_plan.md
```

Next File

```text id="t073"
09_agent_rules.md
```

Purpose

```text id="t074"
Rules for Coding Agents

Code generation constraints

Architecture enforcement

Refactor policies

Implementation workflow
```
