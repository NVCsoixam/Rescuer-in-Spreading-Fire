# 16_logging_monitoring.md

# PURPOSE

Tài liệu này định nghĩa toàn bộ hệ thống Logging, Monitoring và Observability.

Mục tiêu:

* Debug dễ dàng
* Audit simulation
* Benchmark chính xác
* Phân tích hành vi AI
* Theo dõi runtime health

Hệ thống phải hỗ trợ:

```text id="l001"
Logging

Metrics

Tracing

Audit Events
```

---

# 1. OBSERVABILITY ARCHITECTURE

---

Overview

```text id="l002"
Simulation Engine
        │
        ▼
 Event Logger
        │
        ▼
 Log Storage
        │
        ▼
 Monitoring Dashboard
```

---

Rule

```text id="l003"
Every critical action must be observable
```

---

# 2. LOG LEVELS

---

## LEVEL-001

DEBUG

Purpose

```text id="l004"
Development diagnostics
```

---

Examples

```text id="l005"
Node expansion

Path reconstruction

Heatmap updates
```

---

## LEVEL-002

INFO

Purpose

```text id="l006"
Normal operations
```

---

Examples

```text id="l007"
Simulation started

Victim rescued

Path generated
```

---

## LEVEL-003

WARNING

Purpose

```text id="l008"
Recoverable issue
```

---

Examples

```text id="l009"
Victim unreachable

Path not found

Invalid edit ignored
```

---

## LEVEL-004

ERROR

Purpose

```text id="l010"
Serious issue
```

---

Examples

```text id="l011"
Snapshot restore failure

Invalid state transition

Critical validation failure
```

---

# 3. LOG FORMAT

---

Required Fields

```python id="l012"
timestamp

level

module

event

message
```

---

Example

```json id="l013"
{
  "timestamp": "2026-06-01T10:00:00",
  "level": "INFO",
  "module": "engine",
  "event": "simulation_started",
  "message": "Simulation entered RUNNING state"
}
```

---

Rule

```text id="l014"
Structured logging only
```

---

# 4. ENGINE LOGGING

---

## EVENT-001

Simulation Started

```text id="l015"
INFO
```

---

## EVENT-002

Simulation Paused

```text id="l016"
INFO
```

---

## EVENT-003

Simulation Resumed

```text id="l017"
INFO
```

---

## EVENT-004

Simulation Finished

```text id="l018"
INFO
```

---

## EVENT-005

Invalid Transition

```text id="l019"
ERROR
```

---

# 5. AI LOGGING

---

## EVENT-006

Path Planning Started

```text id="l020"
DEBUG
```

---

Payload

```python id="l021"
algorithm

start

goal
```

---

## EVENT-007

Path Planning Completed

```text id="l022"
INFO
```

---

Payload

```python id="l023"
cost

path_length

execution_time
```

---

## EVENT-008

Path Planning Failed

```text id="l024"
WARNING
```

---

# 6. FIRE LOGGING

---

## EVENT-009

Fire Spread

```text id="l025"
INFO
```

---

Payload

```python id="l026"
source

target

step
```

---

## EVENT-010

Victim Burned

```text id="l027"
WARNING
```

---

Payload

```python id="l028"
victim_id

position
```

---

## EVENT-011

Robot Burned

```text id="l029"
ERROR
```

---

# 7. RESCUE LOGGING

---

## EVENT-012

Victim Picked Up

```text id="l030"
INFO
```

---

## EVENT-013

Victim Delivered

```text id="l031"
INFO
```

---

## EVENT-014

Mission Success

```text id="l032"
INFO
```

---

## EVENT-015

Mission Failure

```text id="l033"
WARNING
```

---

# 8. PERFORMANCE METRICS

---

Tracked Metrics

```python id="l034"
fps

tick_time_ms

pathfinding_time_ms

heatmap_time_ms

memory_usage_mb
```

---

Purpose

```text id="l035"
Performance monitoring
```

---

# 9. BENCHMARK METRICS

---

Collected

```python id="l036"
algorithm

success

execution_time

expanded_nodes

path_cost

saved

dead
```

---

Destination

```text id="l037"
Benchmark report
```

---

# 10. AUDIT EVENTS

---

Purpose

```text id="l038"
Reproduce simulation
```

---

Tracked

```python id="l039"
map_seed

algorithm

all_commands

all_state_transitions
```

---

Rule

```text id="l040"
Enough information for replay
```

---

# 11. MONITORING DASHBOARD

---

Displays

```text id="l041"
FPS

Current State

Victims Saved

Victims Dead

Current Algorithm

Fire Count
```

---

Refresh Rate

```python id="l042"
1 second
```

---

# 12. LOG STORAGE

---

File

```text id="l043"
logs/simulation.log
```

---

Rotation

```python id="l044"
10 MB
```

---

Retention

```python id="l045"
10 files
```

---

# 13. TRACE EVENTS

---

Purpose

```text id="l046"
Debug execution order
```

---

Tracked

```text id="l047"
Path Planning

Movement

Rescue

Fire

Risk Update

Terminal Check
```

---

# 14. FAILURE MONITORING

---

Track

```python id="l048"
exceptions

validation_failures

state_errors

path_failures
```

---

Rule

```text id="l049"
No silent failures
```

---

# 15. ALERT RULES

---

Warning Threshold

```python id="l050"
tick_time_ms > 33
```

---

Error Threshold

```python id="l051"
fps < 20
```

---

Critical Threshold

```python id="l052"
engine crash
```

---

# 16. IMPLEMENTATION REQUIREMENTS

---

Use

```python id="l053"
logging
```

---

Forbidden

```python id="l054"
print()
```

---

Format

```python id="l055"
JSON formatter preferred
```

---

# 17. SUCCESS CRITERIA

Logging System passes review when:

```text id="l056"
All major events logged

Performance metrics available

Benchmark metrics captured

Audit trail reproducible

No silent failures

Logs searchable
```

---

# END OF FILE

File Number

```text id="l057"
16_logging_monitoring.md
```

Next File

```text id="l058"
17_error_handling.md
```

Purpose

```text id="l059"
Exception hierarchy

Recovery strategies

Validation failures

Runtime failures

Fault tolerance policy
```
