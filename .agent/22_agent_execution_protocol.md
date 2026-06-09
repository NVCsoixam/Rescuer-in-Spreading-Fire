# 22_agent_execution_protocol.md

# PURPOSE

Tài liệu này định nghĩa giao thức chính thức cho AI Coding Agent.

Mục tiêu:

* Cho phép AI triển khai dự án theo từng bước
* Ngăn AI viết sai kiến trúc
* Giữ code đồng nhất
* Đảm bảo build được từ đầu đến cuối

Tài liệu này là luật vận hành của Coding Agent.

---

# 1. AGENT ROLE

---

AI Agent phải hoạt động như:

```text id="ag001"
Senior Software Engineer
```

---

Không phải:

```text id="ag002"
Code Generator
```

---

Nhiệm vụ:

```text id="ag003"
Đọc task

Phân tích dependency

Implement

Test

Validate

Commit
```

---

# 2. CONTEXT LOADING ORDER

---

Mỗi session mới phải đọc:

```text id="ag004"
00_project_spec.md

01_tasks.md

02_microtasks.md
```

---

Sau đó:

```text id="ag005"
File liên quan tới task hiện tại
```

---

Ví dụ

```text id="ag006"
Implement Fire System
```

---

Agent phải load:

```text id="ag007"
fire_architecture.md

fire_rules.md

risk_system.md
```

---

# 3. EXECUTION HIERARCHY

---

Highest Priority

```text id="ag008"
Project Spec
```

---

Second

```text id="ag009"
Architecture Documents
```

---

Third

```text id="ag010"
Task Registry
```

---

Fourth

```text id="ag011"
Microtasks
```

---

Rule

```text id="ag012"
Never violate higher level document
```

---

# 4. IMPLEMENTATION UNIT

---

Agent không được implement:

```text id="ag013"
Entire project
```

---

Agent chỉ implement:

```text id="ag014"
One microtask
```

at a time.

---

Example

```text id="ag015"
P00-T04-M03
```

---

# 5. MICROTASK WORKFLOW

---

Step 1

```text id="ag016"
Read microtask
```

---

Step 2

```text id="ag017"
Identify dependencies
```

---

Step 3

```text id="ag018"
Implement code
```

---

Step 4

```text id="ag019"
Run tests
```

---

Step 5

```text id="ag020"
Verify acceptance criteria
```

---

Step 6

```text id="ag021"
Mark completed
```

---

# 6. FILE OWNERSHIP RULES

---

Each task must declare:

```text id="ag022"
Files allowed to modify
```

---

Agent must not touch:

```text id="ag023"
Unrelated modules
```

---

Reason

```text id="ag024"
Reduce regression risk
```

---

# 7. TASK EXECUTION FORMAT

---

Agent response format:

```text id="ag025"
TASK

FILES

IMPLEMENTATION

TESTS

RESULT
```

---

Example

```text id="ag026"
TASK:
P00-T08-M02

FILES:
movement.py

RESULT:
PASS
```

---

# 8. DEVELOPMENT CHECKLIST

---

Before coding

```text id="ag027"
Dependencies available

Interfaces defined

Tests identified
```

---

After coding

```text id="ag028"
Lint pass

Tests pass

Types pass
```

---

# 9. FORBIDDEN ACTIONS

---

Forbidden

```text id="ag029"
Rewrite architecture
```

without approval.

---

Forbidden

```text id="ag030"
Change public interfaces
```

without dependency review.

---

Forbidden

```text id="ag031"
Skip tests
```

---

Forbidden

```text id="ag032"
Implement multiple phases simultaneously
```

---

# 10. INTERFACE CONTRACTS

---

Rule

```text id="ag033"
Public APIs are contracts
```

---

Changing contract requires:

```text id="ag034"
Impact analysis
```

---

Required

```text id="ag035"
Backward compatibility
```

---

# 11. TEST-FIRST VALIDATION

---

For every microtask:

```text id="ag036"
Acceptance criteria defined
```

---

Before completion

```text id="ag037"
Acceptance criteria validated
```

---

# 12. DEPENDENCY VALIDATION

---

Before implementation

Agent checks:

```text id="ag038"
Dependency complete?
```

---

If No

```text id="ag039"
Block task execution
```

---

Example

```text id="ag040"
Cannot implement FireEngine
```

if

```text id="ag041"
Grid System missing
```

---

# 13. DOCUMENTATION UPDATE RULE

---

If public API changes:

```text id="ag042"
Update documentation
```

---

Required Files

```text id="ag043"
README

API docs

Task status
```

---

# 14. ERROR RESPONSE PROTOCOL

---

If task impossible:

Agent returns

```text id="ag044"
BLOCKED
```

---

With

```text id="ag045"
Missing dependency

Reason

Required action
```

---

Never

```text id="ag046"
Guess implementation
```

---

# 15. CODE QUALITY GATE

---

Before DONE:

```text id="ag047"
ruff pass

black pass

pytest pass

mypy pass
```

---

Required

```text id="ag048"
100%
```

for critical modules.

---

# 16. AGENT MEMORY RULE

---

Agent must remember:

```text id="ag049"
Current phase

Current task

Completed tasks

Blocked tasks
```

---

Must not:

```text id="ag050"
Reimplement completed work
```

---

# 17. PROJECT EXECUTION ORDER

---

Mandatory

```text id="ag051"
Foundation

↓

Core

↓

Map

↓

Fire

↓

Rescue

↓

AI

↓

Engine

↓

UI

↓

Benchmark

↓

Testing
```

---

Rule

```text id="ag052"
No phase skipping
```

---

# 18. MULTI-AGENT SUPPORT

---

Future Support

```text id="ag053"
Planner Agent

Coding Agent

Review Agent

Testing Agent
```

---

Communication

```text id="ag054"
Task IDs only
```

---

# 19. COMPLETION REPORT

---

Every finished task outputs:

```text id="ag055"
Task ID

Files Changed

Tests Run

Coverage

Status
```

---

Example

```text id="ag056"
P00-T10-M04

Files:
fire_sim.py

Tests:
PASS

Coverage:
100%

Status:
DONE
```

---

# 20. DEFINITION OF TASK DONE

---

Task is DONE only when:

```text id="ag057"
Code complete

Tests pass

Types pass

Lint pass

Acceptance criteria pass

Documentation updated
```

---

# 21. AGENT SUCCESS CRITERIA

Protocol passes review when:

```text id="ag058"
Deterministic execution

No skipped dependencies

No architecture violations

Traceable implementation

Reliable task completion
```

---

# END OF FILE

File Number

```text id="ag059"
22_agent_execution_protocol.md
```

Next File

```text id="ag060"
23_developer_handoff_package.md
```

Purpose

```text id="ag061"
Complete Project Bootstrap Package

Developer Onboarding

Context Transfer

Project Handoff Documentation

Implementation Startup Guide
```
