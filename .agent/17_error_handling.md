# 17_error_handling.md

# PURPOSE

Tài liệu này định nghĩa chiến lược Error Handling chính thức của hệ thống.

Mục tiêu:

* Fault Tolerance
* Graceful Degradation
* Deterministic Recovery
* No System Crash

Nguyên tắc:

```text id="er001"
Simulation must never crash
```

---

# 1. ERROR HANDLING PHILOSOPHY

---

## RULE-001

Error phải:

```text id="er002"
Detected

Logged

Handled

Recovered
```

---

## RULE-002

Không được:

```text id="er003"
Ignore exception
```

---

Forbidden

```python id="er004"
except:
    pass
```

---

## RULE-003

Mọi lỗi phải có:

```text id="er005"
Error Type

Error Message

Recovery Action
```

---

# 2. ERROR CATEGORIES

---

## CATEGORY-001

Validation Errors

Purpose

```text id="er006"
Invalid user input
```

---

Examples

```text id="er007"
Invalid map

Duplicate robot

Missing victim

Missing rescue station
```

---

## CATEGORY-002

Runtime Errors

Purpose

```text id="er008"
Execution problems
```

---

Examples

```text id="er009"
Path not found

Fire spread issue

Snapshot restore issue
```

---

## CATEGORY-003

State Errors

Purpose

```text id="er010"
State machine violation
```

---

Examples

```text id="er011"
Illegal transition

Corrupted state
```

---

## CATEGORY-004

System Errors

Purpose

```text id="er012"
Unexpected failures
```

---

Examples

```text id="er013"
File IO failure

Memory issue
```

---

# 3. EXCEPTION HIERARCHY

---

Base Exception

```python id="er014"
class SimulationError(Exception):
    pass
```

---

Validation

```python id="er015"
class ValidationError(SimulationError):
    pass
```

---

State

```python id="er016"
class StateError(SimulationError):
    pass
```

---

Transition

```python id="er017"
class InvalidStateTransition(StateError):
    pass
```

---

Snapshot

```python id="er018"
class SnapshotError(SimulationError):
    pass
```

---

Pathfinding

```python id="er019"
class PathfindingError(SimulationError):
    pass
```

---

Map

```python id="er020"
class MapGenerationError(SimulationError):
    pass
```

---

# 4. VALIDATION FAILURE POLICY

---

Invalid Grid Size

Action

```text id="er021"
Reject request
```

---

Recovery

```text id="er022"
Keep previous value
```

---

Invalid Entity Placement

Action

```text id="er023"
Reject placement
```

---

Recovery

```text id="er024"
Display warning
```

---

# 5. STATE TRANSITION FAILURES

---

Example

```text id="er025"
IDLE -> FINISHED
```

---

Action

```python id="er026"
raise InvalidStateTransition
```

---

Recovery

```text id="er027"
Remain in current state
```

---

Log Level

```text id="er028"
ERROR
```

---

# 6. PATHFINDING FAILURES

---

Scenario

```text id="er029"
Goal unreachable
```

---

Result

```python id="er030"
PathResult(
    found=False
)
```

---

Forbidden

```python id="er031"
raise Exception
```

---

Reason

```text id="er032"
Expected condition
```

---

# 7. FIRE SYSTEM FAILURES

---

Invalid Cell

Action

```text id="er033"
Ignore
```

---

Out Of Bounds

Action

```text id="er034"
Ignore
```

---

Duplicate Fire

Action

```text id="er035"
Ignore
```

---

Rule

```text id="er036"
Continue simulation
```

---

# 8. SNAPSHOT FAILURES

---

Scenario

```text id="er037"
Snapshot missing
```

---

Action

```python id="er038"
raise SnapshotError
```

---

Recovery

```text id="er039"
Block reset operation
```

---

Scenario

```text id="er040"
Snapshot corrupted
```

---

Action

```python id="er041"
raise SnapshotError
```

---

Recovery

```text id="er042"
Return to IDLE
```

---

# 9. MAP GENERATION FAILURES

---

Scenario

```text id="er043"
Disconnected map
```

---

Action

```text id="er044"
Regenerate map
```

---

Scenario

```text id="er045"
No valid placement
```

---

Action

```text id="er046"
Retry generation
```

---

Maximum Attempts

```python id="er047"
100
```

---

# 10. UI FAILURES

---

Invalid Input

```text id="er048"
Ignore input
```

---

Invalid Tool

```text id="er049"
Show warning
```

---

Rendering Error

```text id="er050"
Render fallback frame
```

---

Rule

```text id="er051"
UI must remain responsive
```

---

# 11. LOGGING REQUIREMENTS

---

Every Error Must Log

```python id="er052"
timestamp

error_type

message

module
```

---

Example

```json id="er053"
{
  "level":"ERROR",
  "module":"engine",
  "error":"InvalidStateTransition"
}
```

---

# 12. RECOVERY STRATEGIES

---

Strategy 1

```text id="er054"
Retry
```

---

Used For

```text id="er055"
Map generation
```

---

Strategy 2

```text id="er056"
Fallback
```

---

Used For

```text id="er057"
Rendering
```

---

Strategy 3

```text id="er058"
Reject Action
```

---

Used For

```text id="er059"
Invalid input
```

---

Strategy 4

```text id="er060"
Safe State
```

---

Used For

```text id="er061"
Critical engine failures
```

---

# 13. SAFE STATE POLICY

---

Safe State

```text id="er062"
PAUSED
```

---

Reason

```text id="er063"
Preserve state
```

---

Critical Failure

```text id="er064"
Move to PAUSED
```

---

User Decision

```text id="er065"
Resume

Reset

Exit
```

---

# 14. FAILURE SEVERITY

---

LOW

```text id="er066"
Input issue
```

---

MEDIUM

```text id="er067"
Path failure
```

---

HIGH

```text id="er068"
Snapshot failure
```

---

CRITICAL

```text id="er069"
State corruption
```

---

# 15. TEST REQUIREMENTS

---

Must Test

```text id="er070"
Validation errors

Path failures

State failures

Snapshot failures

Map failures
```

---

Coverage

```python id="er071"
100% exception paths
```

---

# 16. FORBIDDEN PRACTICES

---

Forbidden

```python id="er072"
except:
```

---

Forbidden

```python id="er073"
return None
```

when exception expected.

---

Forbidden

```python id="er074"
Silent Failure
```

---

Forbidden

```python id="er075"
Swallowed Exception
```

---

# 17. SUCCESS CRITERIA

Error Handling passes review when:

```text id="er076"
All exceptions typed

All failures logged

Recovery strategies defined

No silent failures

No crash scenarios

Safe state reachable
```

---

# END OF FILE

File Number

```text id="er077"
17_error_handling.md
```

Next File

```text id="er078"
18_test_cases_catalog.md
```

Purpose

```text id="er079"
Complete Test Case Registry

QA Matrix

Acceptance Cases

Regression Cases

Edge Cases

Stress Cases
```
