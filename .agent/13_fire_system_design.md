# 13_fire_system_design.md

# PURPOSE

Tài liệu này định nghĩa toàn bộ Fire System Architecture.

Fire System là thành phần tạo môi trường động (Dynamic Environment).

Nhiệm vụ:

* Fire propagation
* Risk generation
* Heatmap generation
* Hazard evaluation
* Dynamic path disruption

Fire System không được mutate GameState trực tiếp.

Mọi thay đổi phải thông qua Engine.

---

# 1. SYSTEM OVERVIEW

---

Fire System gồm 5 thành phần:

```text id="f001"
FireSimulator

FireRules

HeatMapGenerator

RiskCalculator

FireValidator
```

---

Architecture

```text id="f002"
FireSimulator

      │

      ▼

Fire Expansion

      │

      ▼

Risk Calculator

      │

      ▼

Heat Map

      │

      ▼

Engine Update
```

---

# 2. FIRE CONCEPT

---

Fire được xem là:

```text id="f003"
Permanent Hazard
```

---

Rule

```text id="f004"
Fire never disappears
```

---

Rule

```text id="f005"
Fire spreads over time
```

---

Rule

```text id="f006"
Fire blocks traversal
```

---

# 3. FIRE CELL STATE

---

## STATE-001

SAFE

```python id="f007"
risk = 0.0
```

---

## STATE-002

WARNING

```python id="f008"
risk >= 0.3
```

---

## STATE-003

DANGER

```python id="f009"
risk >= 0.6
```

---

## STATE-004

CRITICAL

```python id="f010"
risk >= 0.9
```

---

## STATE-005

BURNING

```python id="f011"
risk = 1.0
```

---

Rule

```text id="f012"
BURNING is terminal
```

---

# 4. FIRE SOURCE

---

Definition

```python id="f013"
FireCell
```

---

Properties

```python id="f014"
position

ignition_step
```

---

Rule

```text id="f015"
At least one fire source
```

---

# 5. FIRE SPREAD RULES

---

## RULE-001

Spread Direction

```text id="f016"
UP

RIGHT

DOWN

LEFT
```

---

Diagonal

```text id="f017"
Not allowed
```

---

## RULE-002

Wall Blocking

Fire cannot spread through:

```text id="f018"
WALL
```

---

## RULE-003

Map Boundary

Fire cannot spread outside:

```text id="f019"
Grid
```

---

## RULE-004

Already Burning

```text id="f020"
Ignore
```

---

# 6. FIRE TICK

---

Fire executes:

```python id="f021"
Every N simulation steps
```

---

Config

```python id="f022"
FIRE_INTERVAL
```

---

Example

```python id="f023"
FIRE_INTERVAL = 3
```

---

Meaning
# 13_fire_system_design.md (CONTINUED)

---

Meaning

```text id="f024"
Fire spreads once every 3 engine ticks
```

---

Execution

```python id="f025"
if current_step % FIRE_INTERVAL == 0:
    spread_fire()
```

---

Rule

```text id="f026"
Deterministic execution only
```

---

# 7. FIRE EXPANSION ALGORITHM

---

## ALGORITHM-001

Input

```python id="f027"
Current Fire Cells
```

---

Process

```text id="f028"
For each fire cell

Check neighbors

Validate spread

Create new fire cells
```

---

Output

```python id="f029"
New Fire Set
```

---

Pseudo Code

```python id="f030"
new_fire = set()

for fire in fire_cells:

    for neighbor in neighbors:

        if can_burn(neighbor):

            new_fire.add(neighbor)
```

---

Commit Phase

```python id="f031"
fire_cells.update(new_fire)
```

---

Rule

```text id="f032"
Expansion happens simultaneously
```

---

Reason

```text id="f033"
Avoid directional bias
```

---

# 8. FIRE VALIDATION

---

## VALIDATION-001

Can Burn

Condition

```python id="f034"
cell != WALL
```

---

Condition

```python id="f035"
cell != FIRE
```

---

Condition

```python id="f036"
inside_grid == True
```

---

Result

```python id="f037"
True / False
```

---

# 9. ENTITY BURN RULES

---

## ROBOT BURN

Condition

```text id="f038"
Robot position in fire
```

---

Action

```python id="f039"
robot.alive = False
```

---

Result

```text id="f040"
Mission Failure
```

---

## VICTIM BURN

Condition

```text id="f041"
Victim position in fire
```

---

Action

```python id="f042"
victim.state = DEAD
```

---

Statistics

```python id="f043"
victims_dead += 1
```

---

## CARRIED VICTIM

Condition

```text id="f044"
Robot carrying victim
AND
Robot burns
```

---

Result

```python id="f045"
victim.state = DEAD
```

---

# 10. RISK MODEL

---

Purpose

```text id="f046"
Predict danger before fire arrives
```

---

Risk Range

```python id="f047"
0.0 → 1.0
```

---

Interpretation

```text id="f048"
0.0 Safe

1.0 Burning
```

---

# 11. RISK CALCULATION

---

## LEVEL-0

Burning Cell

```python id="f049"
risk = 1.0
```

---

## LEVEL-1

Distance = 1

```python id="f050"
risk = 0.9
```

---

## LEVEL-2

Distance = 2

```python id="f051"
risk = 0.7
```

---

## LEVEL-3

Distance = 3

```python id="f052"
risk = 0.5
```

---

## LEVEL-4

Distance = 4

```python id="f053"
risk = 0.3
```

---

## LEVEL-5+

```python id="f054"
risk = 0.0
```

---

Rule

```text id="f055"
Use nearest fire source
```

---

# 12. HEATMAP GENERATION

---

## HEATMAP-001

Input

```python id="f056"
Grid

Fire Cells
```

---

Output

```python id="f057"
Risk Matrix
```

---

Type

```python id="f058"
list[list[float]]
```

---

Size

```python id="f059"
Same as grid
```

---

# 13. AI INTEGRATION

---

Risk-aware algorithms may use:

```python id="f060"
movement_cost

+

risk_penalty
```

---

Formula

```python id="f061"
effective_cost =

distance_cost

+

(risk * risk_weight)
```

---

Example

```python id="f062"
1 + (0.8 * 10)

= 9
```

---

Purpose

```text id="f063"
Avoid dangerous zones
```

---

# 14. FIRE EVENTS

---

## EVENT-001

FireSpreadEvent

Payload

```python id="f064"
source_cell

target_cell

step
```

---

## EVENT-002

VictimBurnedEvent

Payload

```python id="f065"
victim_id

position

step
```

---

## EVENT-003

RobotBurnedEvent

Payload

```python id="f066"
position

step
```

---

# 15. FIRE STATISTICS

---

Tracked Metrics

```python id="f067"
total_fire_cells

spread_events

victims_burned

robot_burned

largest_fire_cluster
```

---

Purpose

```text id="f068"
Benchmarking
```

---

# 16. PERFORMANCE REQUIREMENTS

---

Fire Tick Runtime

```python id="f069"
< 10 ms
```

---

Heatmap Runtime

```python id="f070"
< 20 ms
```

---

Memory Usage

```python id="f071"
< 50 MB
```

---

# 17. FAILURE HANDLING

---

Invalid Fire Cell

```text id="f072"
Ignore
```

---

Duplicate Fire Cell

```text id="f073"
Ignore
```

---

Out Of Bounds

```text id="f074"
Ignore
```

---

Rule

```text id="f075"
Never crash simulation
```

---

# 18. FUTURE EXTENSIONS

---

Reserved

```text id="f076"
Wind System

Smoke System

Water System

Firefighter Agent

Extinguishing Mechanic

Fire Intensity Levels
```

---

Requirement

```text id="f077"
Backward compatible
```

---

# 19. SUCCESS CRITERIA

Fire System passes review when:

```text id="f078"
Fire spreads correctly

Risk map valid

Heatmap deterministic

AI can consume risk

Performance targets met

No crashes
```

---

# END OF FILE

File Number

```text id="f079"
13_fire_system_design.md
```

Next File

```text id="f080"
14_ai_system_design.md
```

Purpose

```text id="f081"
AI Architecture

Search Framework

Pathfinding Contracts

Target Selection

Replanning Strategy

Risk-Aware Navigation
```
