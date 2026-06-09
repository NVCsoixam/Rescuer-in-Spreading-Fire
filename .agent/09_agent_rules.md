# 09_agent_rules.md

# PURPOSE

Tài liệu này định nghĩa quy tắc bắt buộc cho mọi AI Coding Agent tham gia phát triển dự án.

Mục tiêu:

* Ngăn architecture drift
* Ngăn code duplication
* Ngăn hidden dependency
* Đảm bảo deterministic development

Đây là tài liệu governance cao nhất cho code generation.

---

# 1. AGENT ROLE

Agent được xem là:

```text
Software Engineer
```

Không phải:

```text
Architect

Product Owner

System Designer
```

---

Agent chỉ được:

```text
Implement
```

Không được:

```text
Redesign architecture
```

---

# 2. GOLDEN RULES

---

## RULE-001

Luôn đọc:

```text
01_tasks.md

02_microtasks.md

03_execution_specs.md

04_project_structure.md

05_api_contracts.md

06_state_machine.md
```

trước khi code.

---

## RULE-002

Không được tự ý:

```text
Tạo module mới

Đổi tên module

Đổi cấu trúc thư mục
```

---

## RULE-003

Nếu contract conflict:

```text
API Contract thắng
```

---

## RULE-004

Nếu task conflict:

```text
Execution Spec thắng
```

---

# 3. FILE OWNERSHIP RULES

---

Agent chỉ được sửa:

```text
File hiện tại đang implement
```

---

Không được sửa:

```text
Unrelated modules
```

---

Ví dụ:

Nếu implement

```text
app/fire/fire_sim.py
```

Không được sửa:

```text
app/ui/*
```

---

# 4. IMPORT RULES

---

Allowed

```text
config

core

logic

fire

ai

ui
```

theo dependency graph.

---

Forbidden

```text
ui -> ai

ui -> fire

ai -> ui

ai -> engine
```

---

Violation

```text
Architecture Error
```

---

# 5. FUNCTION RULES

---

## RULE-005

Một function chỉ có:

```text
Một responsibility
```

---

## RULE-006

Maximum function size

```python
50 lines
```

---

Nếu lớn hơn:

```text
Refactor
```

---

## RULE-007

Maximum nesting

```python
3 levels
```

---

Nếu vượt:

```text
Extract method
```

---

# 6. CLASS RULES

---

Maximum class size

```python
300 lines
```

---

Maximum public methods

```python
15
```

---

If exceeded

```text
Split class
```

---

# 7. STATE MANAGEMENT RULES

---

Only

```text
Engine
```

được mutate:

```python
GameState
```

---

Forbidden

```text
Renderer

Sidebar

AI

Validator
```

---

Violation

```text
Critical Architecture Error
```

---

# 8. AI MODULE RULES

---

AI modules phải:

```text
Pure Function
```

---

Input

```python
Grid

Start

Goal
```

---

Output

```python
PathResult
```

---

Forbidden

```text
Read UI

Write state

Modify map
```

---

# 9. UI RULES

---

UI được phép:

```text
Render

Receive input

Send command
```

---

UI không được:

```text
Run AI

Mutate state

Spread fire

Calculate rescue logic
```

---

# 10. LOGGING RULES

---

Every subsystem must log:

```text
Start

Success

Failure
```

---

Log Levels

```python
INFO

DEBUG

WARNING

ERROR
```

---

Forbidden

```python
print()
```

---

Use

```python
logging
```

---

# 11. ERROR HANDLING RULES

---

Never

```python
except:
    pass
```

---

Forbidden

```python
Bare Exception
```

---

Required

```python
except SpecificError:
```

---

# 12. TEST RULES

---

Every new module

Must include

```text
Unit Test
```

---

Every subsystem

Must include

```text
Integration Test
```

---

Coverage Target

```python
90%
```

---

# 13. CODE STYLE RULES

---

Formatting

```bash
black
```

---

Linting

```bash
ruff
```

---

Typing

```python
mypy
```

---

Required

```python
Type Hints
```

---

Forbidden

```python
Untyped public functions
```

---

# 14. DOCUMENTATION RULES

---

Every public function

Must contain

```python
Docstring
```

---

Format

```python
"""
Purpose

Args

Returns

Raises
"""
```

---

# 15. REFACTOR RULES

---

Agent được phép:

```text
Extract Function

Rename Local Variable

Improve Readability
```

---

Agent không được:

```text
Change Contract

Change DTO

Change State Machine
```

---

Nếu cần:

```text
Raise Architecture Review
```

---

# 16. IMPLEMENTATION WORKFLOW

---

Step 1

```text
Read Task
```

---

Step 2

```text
Read Contract
```

---

Step 3

```text
Read Spec
```

---

Step 4

```text
Implement
```

---

Step 5

```text
Run Unit Tests
```

---

Step 6

```text
Run Integration Tests
```

---

Step 7

```text
Commit
```

---

# 17. DEFINITION OF DONE

Task hoàn thành khi:

```text
Code Compiles

Tests Pass

Coverage Maintained

Contract Satisfied

No Architecture Violation
```

---

Task chưa hoàn thành nếu:

```text
TODO còn tồn tại

Contract thiếu

Test thiếu

Lint lỗi

Typing lỗi
```

---

# 18. FORBIDDEN ACTIONS

---

Agent tuyệt đối không được:

```text
Hardcode pathfinding result

Hardcode benchmark result

Bypass validation

Disable tests

Skip state transitions

Modify snapshot directly

Use global mutable state
```

---

# 19. REVIEW CHECKLIST

Trước khi merge:

```text
Contract OK

Tests OK

Coverage OK

Architecture OK

Performance OK

Logging OK
```

---

Nếu bất kỳ mục nào fail:

```text
Reject Merge
```

---

# 20. SUCCESS CRITERIA

Agent tuân thủ khi:

```text
Code deterministic

Code testable

Code maintainable

Code contract-compliant

Code architecture-compliant
```

---

# END OF FILE

File Number

```text
09_agent_rules.md
```

Next File

```text
10_coding_standards.md
```

Purpose

```text
Naming conventions

Folder conventions

Python standards

Dataclass standards

Error standards

Logging standards

Documentation standards
```
