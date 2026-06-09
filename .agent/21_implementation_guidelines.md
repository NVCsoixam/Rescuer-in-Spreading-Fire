# 21_implementation_guidelines.md

# PURPOSE

Tài liệu này định nghĩa Coding Standards chính thức của dự án.

Mục tiêu:

* Consistent Codebase
* Maintainability
* Readability
* Testability
* Scalability

Mọi contributor phải tuân thủ tài liệu này.

---

# 1. GENERAL PRINCIPLES

---

## PRINCIPLE-001

Readable > Clever

Ưu tiên:

```text
Code dễ đọc
```

---

Không ưu tiên:

```text
Code ngắn nhưng khó hiểu
```

---

## PRINCIPLE-002

Explicit > Implicit

Good

```python
target_victim_id
```

---

Bad

```python
t
```

---

## PRINCIPLE-003

Single Responsibility

Một class chỉ có:

```text
1 lý do để thay đổi
```

---

# 2. NAMING CONVENTIONS

---

## Variables

Format

```python
snake_case
```

---

Good

```python
robot_position

fire_cells

victim_count
```

---

Bad

```python
RobotPosition

FireCells

vc
```

---

## Functions

Format

```python
snake_case
```

---

Good

```python
generate_map()

spread_fire()

calculate_risk()
```

---

## Classes

Format

```python
PascalCase
```

---

Good

```python
GameState

FireSimulator

PathResult
```

---

## Constants

Format

```python
UPPER_CASE
```

---

Good

```python
GRID_SIZE

FIRE_INTERVAL

MAX_VICTIMS
```

---

# 3. FILE NAMING

---

Rule

```text
snake_case.py
```

---

Good

```text
fire_sim.py

target_selector.py

benchmark_runner.py
```

---

Bad

```text
FireSim.py

TargetSelector.py
```

---

# 4. TYPE HINTING

---

Requirement

```text
Mandatory
```

---

Good

```python
def spread_fire(
    cells: list[Position]
) -> list[Position]:
```

---

Bad

```python
def spread_fire(cells):
```

---

Rule

```text
Every public function typed
```

---

# 5. DATACLASS RULES

---

Preferred

```python
@dataclass
class Victim:
```

---

Instead Of

```python
class Victim:
```

for simple models.

---

Use Frozen

```python
@dataclass(frozen=True)
class Position:
```

---

When

```text
Object immutable
```

---

# 6. ENUM RULES

---

Use Enum For

```text
States

Modes

Types
```

---

Example

```python
class CellType(Enum):
```

---

Forbidden

```python
FIRE = 2
```

spread across codebase.

---

# 7. FUNCTION DESIGN

---

Maximum Size

```python
50 lines
```

---

Preferred

```python
20-30 lines
```

---

Rule

```text
One responsibility
```

---

# 8. CLASS DESIGN

---

Maximum Size

```python
300 lines
```

---

Preferred

```python
100-200 lines
```

---

Rule

```text
High cohesion
```

---

# 9. COMMENTS

---

Comment Only

```text
Why
```

---

Avoid

```text
What
```

when code already obvious.

---

Good

```python
# Use deterministic ordering
# to guarantee benchmark fairness
```

---

Bad

```python
# Increment i
i += 1
```

---

# 10. DOCSTRINGS

---

Public Functions

```python
Required
```

---

Template

```python
def find_path(...):
    """
    Compute path between start and goal.

    Args:
        ...

    Returns:
        PathResult
    """
```

---

# 11. ERROR HANDLING

---

Allowed

```python
except ValidationError:
```

---

Forbidden

```python
except:
```

---

Rule

```text
Catch specific exceptions
```

---

# 12. LOGGING

---

Use

```python
logger.info()

logger.warning()

logger.error()
```

---

Forbidden

```python
print()
```

---

Reason

```text
Production readiness
```

---

# 13. IMPORT RULES

---

Good

```python
from app.fire.risk import calculate_risk
```

---

Bad

```python
from risk import *
```

---

Forbidden

```python
*
```

imports.

---

# 14. CONFIGURATION RULES

---

All constants belong in:

```text
app/config.py
```

---

Forbidden

```python
if grid_size > 35:
```

hardcoded everywhere.

---

Use

```python
MAX_GRID_SIZE
```

---

# 15. TESTING RULES

---

Every Public Function

```text
Must have tests
```

---

Coverage Target

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

AI

Fire

Rescue
```

---

# 16. STATE MANAGEMENT RULES

---

Only Engine Can Mutate

```text
GameState
```

---

Forbidden

```python
ai_module.state = ...
```

---

Forbidden

```python
renderer.state = ...
```

---

# 17. PERFORMANCE RULES

---

Avoid

```python
Deep copy every frame
```

---

Avoid

```python
Recompute full heatmap
```

when unnecessary.

---

Prefer

```python
Incremental updates
```

---

# 18. CODE REVIEW CHECKLIST

---

Reviewer Must Verify

```text
Type hints present

Tests present

No duplicated logic

No magic numbers

No wildcard imports

No circular dependencies
```

---

# 19. GIT WORKFLOW

---

Branch Format

```text
feature/fire-system

feature/astar

fix/heatmap-bug
```

---

Commit Format

```text
feat:

fix:

refactor:

test:

docs:
```

---

Examples

```text
feat: implement fire propagation

fix: correct risk calculation

test: add astar benchmark cases
```

---

# 20. DEFINITION OF DONE

Task considered DONE when:

```text
Code implemented

Tests passing

Lint passing

Type checking passing

Documentation updated

Code reviewed
```

---

# 21. SUCCESS CRITERIA

Implementation Guidelines pass review when:

```text
Consistent naming

Typed codebase

Maintainable modules

Reviewable changes

Production-ready quality
```

---

# END OF FILE

File Number

```text
21_implementation_guidelines.md
```

Next File

```text
22_agent_execution_protocol.md
```

Purpose

```text
Coding Agent Instructions

Task Execution Protocol

Microtask Workflow

Context Loading Rules

Implementation Order Constraints

AI Coding Governance
```
