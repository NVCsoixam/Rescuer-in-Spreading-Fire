# 10_coding_standards.md

# PURPOSE

Tài liệu này định nghĩa coding standards bắt buộc cho toàn bộ source code.

Mục tiêu:

* Consistency
* Readability
* Maintainability
* Testability
* Scalability

---

# 1. GENERAL PRINCIPLES

---

## STANDARD-001

Code phải ưu tiên:

```text
Correctness
```

trước

```text
Performance
```

---

## STANDARD-002

Code phải ưu tiên:

```text
Readability
```

trước

```text
Micro Optimization
```

---

## STANDARD-003

Code phải:

```text
Deterministic
```

---

Không được phụ thuộc:

```text
Runtime randomness
```

trừ khi được inject seed.

---

# 2. FILE NAMING

---

## Python Files

Required

```text
snake_case.py
```

---

Good

```text
grid.py

fire_sim.py

heatmap.py

test_fire.py
```

---

Bad

```text
Grid.py

FireSimulation.py

TEST_FIRE.py
```

---

# 3. CLASS NAMING

---

Required

```python
PascalCase
```

---

Good

```python
GameState

FireSimulator

PathResult

GridGenerator
```

---

Bad

```python
game_state

fire_simulator

PATHRESULT
```

---

# 4. FUNCTION NAMING

---

Required

```python
snake_case
```

---

Good

```python
generate_map()

calculate_risk()

restore_snapshot()
```

---

Bad

```python
GenerateMap()

RiskCalculation()
```

---

# 5. CONSTANT NAMING

---

Required

```python
UPPER_CASE
```

---

Example

```python
GRID_WIDTH

GRID_HEIGHT

MAX_VICTIMS

FIRE_INTERVAL
```

---

# 6. ENUM STANDARDS

---

Example

```python
class CellType(Enum):

    EMPTY = 0

    WALL = 1

    FIRE = 2

    VICTIM = 3

    ROBOT = 4

    RESCUE = 5
```

---

Rule

```text
Never use magic numbers
```

---

# 7. DATACLASS STANDARDS

---

Required

```python
@dataclass
```

---

Used For

```text
DTO

State

Result Objects
```

---

Example

```python
@dataclass
class Position:

    x: int

    y: int
```

---

# 8. TYPE HINTS

---

Required

```python
100%
```

---

Good

```python
def get_neighbors(
    x: int,
    y: int
) -> list[Position]:
```

---

Bad

```python
def get_neighbors(x, y):
```

---

# 9. DOCSTRING STANDARD

---

Every public function:

```python
"""
Purpose

Args

Returns

Raises
"""
```

---

Example

```python
def restore_snapshot() -> None:
    """
    Restore simulation state.

    Args:
        None

    Returns:
        None

    Raises:
        SnapshotError
    """
```

---

# 10. COMPLEXITY LIMITS

---

Function

```python
Max 50 lines
```

---

Class

```python
Max 300 lines
```

---

Nesting

```python
Max 3 levels
```

---

Parameters

```python
Max 5
```

---

If exceeded

```text
Refactor required
```

---

# 11. ERROR HANDLING

---

Allowed

```python
raise ValidationError()

raise SnapshotError()

raise PathNotFoundError()
```

---

Forbidden

```python
raise Exception()
```

---

# 12. LOGGING STANDARD

---

Use

```python
logging
```

---

Never

```python
print()
```

---

Levels

```python
DEBUG

INFO

WARNING

ERROR
```

---

# 13. TEST STANDARD

---

Naming

```python
test_<feature>.py
```

---

Example

```python
test_grid.py

test_fire.py

test_engine.py
```

---

# 14. IMPORT STANDARD

---

Order

```python
Standard Library

Third Party

Local Imports
```

---

Example

```python
import logging
from dataclasses import dataclass

import pytest

from app.core.state import GameState
```

---

# 15. SUCCESS CRITERIA

Code đạt chuẩn khi:

```text
Lint Pass

Type Check Pass

Tests Pass

No Magic Numbers

No Circular Imports

100% Type Hints
```

---

# END OF FILE

File Number

```text
10_coding_standards.md
```

Next File

```text
11_data_model_spec.md
```
