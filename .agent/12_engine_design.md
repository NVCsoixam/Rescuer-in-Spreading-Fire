# 12_engine_design.md

# PURPOSE

Tài liệu này định nghĩa kiến trúc chính thức của Simulation Engine.

Engine là thành phần quan trọng nhất của toàn bộ hệ thống.

Engine chịu trách nhiệm:

* State ownership
* Scheduling
* Event processing
* AI orchestration
* Fire orchestration
* Mission lifecycle

Engine là nơi duy nhất được phép mutate GameState.

---

# 1. ENGINE RESPONSIBILITIES

---

## RESPONSIBILITY-001

State Owner

```text id="e001"
GameState Owner
```

---

Engine là nơi duy nhất được phép:

```text id="e002"
Create state

Mutate state

Replace state

Restore state
```

---

Forbidden

```text id="e003"
UI mutate state

AI mutate state

Fire module mutate state
```

---

## RESPONSIBILITY-002

Simulation Scheduler

Engine quyết định:

```text id="e004"
Khi nào AI chạy

Khi nào Fire chạy

Khi nào Rescue chạy

Khi nào UI cập nhật
```

---

## RESPONSIBILITY-003

Lifecycle Manager

Engine quản lý:

```text id="e005"
IDLE

EDIT

RUNNING

PAUSED

FINISHED
```

---

# 2. ENGINE ARCHITECTURE

---

```text id="e006"
             Engine
                │
 ┌──────────────┼──────────────┐
 │              │              │
 ▼              ▼              ▼

 AI         Rescue        Fire

 │              │              │

 └──────┬───────┴───────┬──────┘
        │               │
        ▼               ▼

          GameState
```

---

Rule

```text id="e007"
All state mutations pass through Engine
```

---

# 3. ENGINE COMPONENTS

---

## COMPONENT-001

StateManager

Purpose

```text id="e008"
Own GameState
```

---

Responsibilities

```text id="e009"
Load state

Replace state

Snapshot restore

Validation
```

---

## COMPONENT-002

SimulationScheduler

Purpose

```text id="e010"
Runtime execution order
```

---

Responsibilities

```text id="e011"
Step timing

Fire timing

AI timing
```

---

## COMPONENT-003

MissionController

Purpose

```text id="e012"
Mission progress
```

---

Responsibilities

```text id="e013"
Target selection

Completion checks

Failure checks
```

---

# 4. ENGINE PUBLIC API

---

## API-001

start()

```python id="e014"
def start() -> bool
```

---

Behavior

```text id="e015"
Validate state

Create snapshot

Switch RUNNING
```

---

## API-002

pause()

```python id="e016"
def pause() -> None
```

---

Behavior

```text id="e017"
RUNNING -> PAUSED
```

---

## API-003

resume()

```python id="e018"
def resume() -> None
```

---

Behavior

```text id="e019"
PAUSED -> RUNNING
```

---

## API-004

reset()

```python id="e020"
def reset() -> None
```

---

Behavior

```text id="e021"
Restore snapshot

Go IDLE
```

---

## API-005

simulation_step()

```python id="e022"
def simulation_step() -> None
```

---

Behavior

```text id="e023"
Single deterministic tick
```

---

# 5. EXECUTION PIPELINE

---

## PIPELINE-001

Per Tick

```text id="e024"
Path Planning

↓

Movement

↓

Rescue

↓

Fire

↓

Risk Update

↓

Statistics

↓

Terminal Check
```

---

Rule

```text id="e025"
Never change order
```

---

# 6. PATH PLANNING STAGE

---

## STAGE-001

Select Target

Priority

```text id="e026"
Reachable victim

Lowest path cost

Lowest risk
```

---

Output

```python id="e027"
Victim ID
```

---

## STAGE-002

Run Algorithm

Input

```python id="e028"
Grid

Start

Goal
```

---

Output

```python id="e029"
PathResult
```

---

# 7. MOVEMENT STAGE

---

## STAGE-003

Consume Path

```python id="e030"
path.pop(0)
```

---

Update

```text id="e031"
Robot position
```

---

Statistics

```python id="e032"
steps += 1
```

---

# 8. RESCUE STAGE

---

## STAGE-004

Pickup Check

Condition

```text id="e033"
Robot on victim
```

---

Action

```text id="e034"
Pickup
```

---

## STAGE-005

Drop Check

Condition

```text id="e035"
Robot on rescue station
```

---

Action

```text id="e036"
Deliver victim
```

---

# 9. FIRE STAGE

---

## STAGE-006

Spread Fire

Action

```text id="e037"
Fire tick
```

---

Update

```text id="e038"
Fire cells
```

---

## STAGE-007

Burn Entities

Checks

```text id="e039"
Robot

Victims
```

---

# 10. HEATMAP STAGE

---

## STAGE-008

Recalculate Risk

Output

```text id="e040"
Updated cell risks
```

---

Consumers

```text id="e041"
AI
```

---

# 11. TERMINAL CHECK STAGE

---

## SUCCESS CONDITION

```text id="e042"
All victims rescued
```

---

## FAILURE CONDITION

```text id="e043"
Robot dead

No reachable victim

No rescue route
```

---

Result

```text id="e044"
FINISHED
```

---

# 12. STATE MUTATION RULES

---

Allowed

```text id="e045"
Engine modifies GameState
```

---

Forbidden

```text id="e046"
AI modifies GameState

Renderer modifies GameState

Fire module modifies GameState
```

---

Rule

```text id="e047"
All mutations centralized
```

---

# 13. EVENT SYSTEM

---

## EVENT-001

StartEvent

```text id="e048"
Begin simulation
```

---

## EVENT-002

PauseEvent

```text id="e049"
Pause simulation
```

---

## EVENT-003

ResumeEvent

```text id="e050"
Resume simulation
```

---

## EVENT-004

ResetEvent

```text id="e051"
Restore snapshot
```

---

## EVENT-005

MissionCompletedEvent

```text id="e052"
All victims rescued
```

---

## EVENT-006

MissionFailedEvent

```text id="e053"
Mission failure
```

---

# 14. SNAPSHOT INTEGRATION

---

Create Snapshot

```text id="e054"
Before RUNNING
```

---

Restore Snapshot

```text id="e055"
Reset
```

---

Requirement

```text id="e056"
Deep copy only
```

---

# 15. PERFORMANCE REQUIREMENTS

---

Tick Budget

```python id="e057"
< 33 ms
```

---

Target FPS

```python id="e058"
30 FPS
```

---

Pathfinding Budget

```python id="e059"
< 100 ms
```

---

Memory Budget

```python id="e060"
< 512 MB
```

---

# 16. FAILURE HANDLING

---

Failure must never:

```text id="e061"
Crash application
```

---

Required

```text id="e062"
Log error

Recover state

Continue safely
```

---

# 17. OBSERVABILITY

---

Engine logs:

```text id="e063"
State transitions

AI decisions

Fire events

Rescue events

Failures
```

---

Levels

```text id="e064"
INFO

DEBUG

WARNING

ERROR
```

---

# 18. SUCCESS CRITERIA

Engine passes review when:

```text id="e065"
State ownership enforced

Pipeline deterministic

No illegal transitions

Snapshot works

Performance targets met

All tests pass
```

---

# END OF FILE

File Number

```text id="e066"
12_engine_design.md
```

Next File

```text id="e067"
13_fire_system_design.md
```

Purpose

```text id="e068"
Fire propagation architecture

Risk calculation

Heatmap generation

Fire scheduling

Burn mechanics

Dynamic environment modeling
```
