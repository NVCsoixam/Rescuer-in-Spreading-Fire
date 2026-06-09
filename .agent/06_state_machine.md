# 06_state_machine.md

# PURPOSE

Tài liệu này định nghĩa chính xác vòng đời của Simulation Engine.

Đây là nguồn sự thật duy nhất (Single Source of Truth) cho:

* State Transition
* Event Processing
* Runtime Flow
* Failure Handling
* Recovery Logic

Mọi implementation phải tuân thủ tài liệu này.

---

# 1. STATE MACHINE OVERVIEW

```text id="s01"
          ┌─────────┐
          │  IDLE   │
          └────┬────┘
               │
               ▼
          ┌─────────┐
          │  EDIT   │
          └────┬────┘
               │
               ▼
          ┌─────────┐
          │ RUNNING │
          └──┬───┬──┘
             │   │
             │   ▼
             │ PAUSED
             │   │
             └───┘

               ▼

          ┌─────────┐
          │FINISHED │
          └────┬────┘
               │
               ▼
          ┌─────────┐
          │  IDLE   │
          └─────────┘
```

---

# 2. STATE DEFINITIONS

---

## STATE-001

### IDLE

Purpose

```text id="s02"
System initialized

No active simulation

Waiting for user action
```

---

Allowed Actions

```text id="s03"
Load map

Generate map

Enter edit mode
```

---

Forbidden Actions

```text id="s04"
Pause

Resume

Simulation Step
```

---

## STATE-002

### EDIT

Purpose

```text id="s05"
User modifies map
```

---

Allowed Actions

```text id="s06"
Place wall

Place robot

Place victim

Place fire

Place rescue station

Generate map

Save snapshot
```

---

Forbidden Actions

```text id="s07"
Run fire

Run AI

Advance simulation
```

---

## STATE-003

### RUNNING

Purpose

```text id="s08"
Simulation active
```

---

Allowed Actions

```text id="s09"
AI planning

Movement

Fire spread

Rescue

Statistics update
```

---

Forbidden Actions

```text id="s10"
Map editing
```

---

## STATE-004

### PAUSED

Purpose

```text id="s11"
Freeze runtime
```

---

Allowed Actions

```text id="s12"
Resume

Reset

Inspect state
```

---

Forbidden Actions

```text id="s13"
Movement

Fire

AI planning
```

---

## STATE-005

### FINISHED

Purpose

```text id="s14"
Mission ended
```

---

Possible Causes

```text id="s15"
All victims rescued

Robot dead

No reachable victims

No reachable rescue route
```

---

Allowed Actions

```text id="s16"
View report

Reset

Return to idle
```

---

# 3. TRANSITION RULES

---

## TRANSITION-001

```text id="s17"
IDLE -> EDIT
```

Trigger

```text id="s18"
User enters editor
```

---

## TRANSITION-002

```text id="s19"
EDIT -> RUNNING
```

Requirements

```text id="s20"
Map valid

Robot exists

Victim exists

Rescue station exists

Snapshot exists
```

---

Failure

```python id="s21"
ValidationError
```

---

## TRANSITION-003

```text id="s22"
RUNNING -> PAUSED
```

Trigger

```text id="s23"
Pause command
```

---

## TRANSITION-004

```text id="s24"
PAUSED -> RUNNING
```

Trigger

```text id="s25"
Resume command
```

---

## TRANSITION-005

```text id="s26"
RUNNING -> FINISHED
```

Triggers

```text id="s27"
Mission success

Mission failure
```

---

## TRANSITION-006

```text id="s28"
FINISHED -> IDLE
```

Trigger

```text id="s29"
Reset complete
```

---

# 4. ILLEGAL TRANSITIONS

---

Forbidden

```text id="s30"
IDLE -> FINISHED

IDLE -> PAUSED

FINISHED -> RUNNING

PAUSED -> EDIT

RUNNING -> IDLE
```

---

Result

```python id="s31"
raise InvalidStateTransition
```

---

# 5. ENGINE EXECUTION LOOP

---

## LOOP-001

Main Loop

```python id="s32"
while RUNNING:
    simulation_step()
```

---

## LOOP-002

Execution Order

```text id="s33"
1 Path Planning

2 Movement

3 Rescue Check

4 Fire Tick

5 Risk Recalculate

6 Statistics Update

7 Terminal Check
```

---

Rule

```text id="s34"
Execution order is immutable
```

---

# 6. AI DECISION FLOW

---

## FLOW-001

Victim Selection

```text id="s35"
Find nearest reachable victim
```

---

## FLOW-002

Path Planning

```text id="s36"
Current Algorithm

↓

Generate Path

↓

PathResult
```

---

## FLOW-003

Movement

```text id="s37"
Follow first step

Remove consumed step
```

---

## FLOW-004

Replanning Trigger

```text id="s38"
Path blocked

Fire spread

Victim dead

Target changed
```

---

# 7. RESCUE STATE MACHINE

---

Victim State

```text id="s39"
WAITING
   ↓

CARRIED
   ↓

RESCUED
```

---

Failure Path

```text id="s40"
WAITING
   ↓

DEAD
```

---

Terminal States

```text id="s41"
RESCUED

DEAD
```

---

# 8. ROBOT STATE MACHINE

---

Robot State

```text id="s42"
IDLE

MOVING

CARRYING

DEAD
```

---

Transitions

```text id="s43"
IDLE -> MOVING

MOVING -> CARRYING

CARRYING -> MOVING

MOVING -> DEAD

CARRYING -> DEAD
```

---

# 9. FIRE STATE MACHINE

---

Cell State

```text id="s44"
SAFE
   ↓

BURNING
```

---

Rule

```text id="s45"
No extinguish mechanic in v1
```

---

Once burning

```text id="s46"
Always burning
```

---

# 10. FAILURE STATES

---

## FAIL-001

Robot Burned

Condition

```text id="s47"
Robot cell becomes FIRE
```

---

Result

```text id="s48"
Mission failure
```

---

## FAIL-002

No Reachable Victim

Condition

```text id="s49"
All remaining victims unreachable
```

---

Result

```text id="s50"
Mission failure
```

---

## FAIL-003

No Reachable Rescue

Condition

```text id="s51"
Victim reachable

Rescue unreachable
```

---

Result

```text id="s52"
Mission failure
```

---

# 11. RECOVERY STATES

---

## RECOVERY-001

Reset

Source

```text id="s53"
PAUSED

FINISHED
```

---

Action

```text id="s54"
Restore Snapshot
```

---

Destination

```text id="s55"
IDLE
```

---

## RECOVERY-002

Map Regeneration

Source

```text id="s56"
EDIT
```

---

Destination

```text id="s57"
EDIT
```

---

Purpose

```text id="s58"
Generate valid map
```

---

# 12. SUCCESS CRITERIA

Mission Success

```text id="s59"
All victims rescued
```

---

Mission Failure

```text id="s60"
Robot dead

No reachable victim

No reachable rescue route
```

---

Simulation Completion

```text id="s61"
Mode = FINISHED
```

---

# 13. IMPLEMENTATION REQUIREMENTS

Engine must guarantee

```text id="s62"
Deterministic transitions

No invalid states

No skipped states

No hidden transitions

No state corruption
```

---

# END OF FILE

File Number

```text id="s63"
06_state_machine.md
```

Next File

```text id="s64"
07_algorithm_benchmarks.md
```

Purpose

```text id="s65"
Formal comparison framework

Benchmark scenarios

Performance metrics

AI evaluation methodology

Fairness rules
```
