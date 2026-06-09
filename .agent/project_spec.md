# 2D Rescue Simulation System - FULL PROJECT SPEC

---

# 1. PROJECT OVERVIEW

Dự án là một hệ thống mô phỏng cứu hộ 2D (2D Rescue Simulation System) chạy trên grid.

Môi trường gồm:
- Robot cứu hộ
- Nạn nhân (victim)
- Trạm cứu hộ
- Tường (wall)
- Lửa lan theo thời gian

Mục tiêu:
- Mô phỏng môi trường động có cháy lan
- So sánh thuật toán AI tìm đường
- Trực quan hóa decision making của AI
- Tạo simulation giống mini game

---

# 2. CORE IDEA (RẤT QUAN TRỌNG)

Đây KHÔNG phải maze solver.

Đây là:

👉 Dynamic multi-agent rescue simulation

Có:
- môi trường thay đổi theo thời gian (fire spread)
- AI phải thích nghi realtime
- risk-based navigation
- state machine rõ ràng

---

# 3. WORLD MODEL

## 3.1 GRID
- 2D grid
- size: 10x10 → 35x35
- mỗi cell là 1 object duy nhất

---

## 3.2 CELL TYPES

```python
EMPTY = 0
WALL = 1
FIRE = 2
VICTIM = 3
ROBOT = 4
RESCUE = 5

### 10. FIRE + RISK SYSTEM
Each cell has:
- risk value float
- updated every fire tick

Risk levels:
- 0.0 safe
- 0.3 warning
- 0.6 danger
- 0.9 critical
- 1.0 fire

### 11. MAP GENERATION RULES
DO NOT generate random noise map.

Must:
- generate rooms
- generate corridors
- ensure connectivity

Entities:
- 1 robot
- 1+ rescue station
- 5 victims default
- 1+ fire source

### 12. UI RULES
Layout:
- LEFT: GRID (80%)
- RIGHT: SIDEBAR (20%)

Sidebar:
- Map settings
- Edit tools
- Algorithm run buttons
- Controls
- Status panel

RULE:
👉 UI MUST NOT CONTAIN LOGIC

Only:
- render
- send input to engine

### 13. STATUS SYSTEM
Fields:
- mode
- saved
- dead
- remaining
- steps
- time
- carrying

### 14. PERFORMANCE REQUIREMENTS
- 30 FPS minimum
- 35x35 max grid
- <100ms input response
- no full recompute per frame

### 15. ERROR HANDLING
System must NEVER crash on:
- invalid map
- invalid edit
- unreachable target
- fire isolation

Instead:
- return safe failure state
- log warning

### 16. LOGGING RULES
Log:
- fire spread events
- movement decisions
- pathfinding start/end
- rescue events

Levels:
- INFO
- DEBUG
- WARNING
- ERROR

### 17. DESIGN GOALS
- AI explainability
- deterministic simulation
- reproducible runs
- comparison fairness between algorithms