# 15_ui_system_design.md

# PURPOSE

Tài liệu này định nghĩa kiến trúc UI chính thức của hệ thống.

UI chỉ chịu trách nhiệm:

* Rendering
* User Input
* Visualization
* Status Display

UI tuyệt đối không chứa business logic.

---

# 1. UI ARCHITECTURE

---

Overview

```text id="u001"
+-------------------------------+
|                               |
|          GRID VIEW            |
|                               |
|                               |
+-------------------+-----------+
|                   |           |
|                   | SIDEBAR   |
|                   |           |
|                   |           |
+-------------------+-----------+
```

---

Layout Ratio

```text id="u002"
Grid Area     = 80%

Sidebar Area  = 20%
```

---

# 2. UI DESIGN PRINCIPLES

---

## PRINCIPLE-001

UI is Passive

Meaning

```text id="u003"
UI displays state

UI does not own state
```

---

## PRINCIPLE-002

Engine Driven

Meaning

```text id="u004"
Engine is source of truth
```

---

UI reads:

```text id="u005"
GameState
```

---

## PRINCIPLE-003

No Business Logic

Forbidden

```text id="u006"
Pathfinding

Fire Spread

Rescue Logic

State Mutation
```

---

# 3. UI COMPONENTS

---

## COMPONENT-001

GridRenderer

File

```text id="u007"
app/ui/renderer.py
```

---

Responsibilities

```text id="u008"
Draw cells

Draw robot

Draw victims

Draw fire

Draw rescue stations
```

---

## COMPONENT-002

Sidebar

File

```text id="u009"
app/ui/sidebar.py
```

---

Responsibilities

```text id="u010"
Controls

Status

Settings
```

---

## COMPONENT-003

InputController

File

```text id="u011"
app/ui/controls.py
```

---

Responsibilities

```text id="u012"
Mouse input

Keyboard input

Command dispatch
```

---

# 4. GRID RENDERER

---

Input

```python id="u013"
GameState
```

---

Output

```text id="u014"
Visual representation
```

---

Rule

```text id="u015"
Renderer must be stateless
```

---

# 5. CELL VISUALIZATION

---

EMPTY

```text id="u016"
White
```

---

WALL

```text id="u017"
Dark Gray
```

---

FIRE

```text id="u018"
Red
```

---

VICTIM

```text id="u019"
Yellow
```

---

ROBOT

```text id="u020"
Blue
```

---

RESCUE

```text id="u021"
Green
```

---

# 6. RISK OVERLAY

---

Purpose

```text id="u022"
Visualize danger zones
```

---

Optional Layer

```text id="u023"
Heatmap Overlay
```

---

Risk Colors

```text id="u024"
0.0 -> Transparent

0.3 -> Light Orange

0.6 -> Orange

0.9 -> Dark Orange

1.0 -> Red
```

---

# 7. PATH VISUALIZATION

---

Purpose

```text id="u025"
Explain AI decisions
```

---

Display

```text id="u026"
Current planned path
```

---

Requirements

```text id="u027"
Non-destructive overlay
```

---

# 8. SIDEBAR LAYOUT

---

Section 1

```text id="u028"
Map Settings
```

---

Controls

```text id="u029"
Grid Size

Victim Count

Fire Count

Seed
```

---

Section
# 15_ui_system_design.md (CONTINUED)

---

Section 2

```text id="u030"
Simulation Controls
```

---

Buttons

```text id="u031"
Generate Map

Start

Pause

Resume

Reset
```

---

Section 3

```text id="u032"
Algorithm Selection
```

---

Options

```text id="u033"
BFS

DFS

UCS

Dijkstra

Greedy

A*
```

---

Section 4

```text id="u034"
Visualization
```

---

Options

```text id="u035"
Show Path

Show Risk

Show Statistics
```

---

Section 5

```text id="u036"
Status Panel
```

---

# 9. STATUS PANEL

---

Displayed Fields

```text id="u037"
Current Mode

Current Algorithm

Victims Saved

Victims Dead

Remaining Victims

Total Steps

Simulation Time

Robot State
```

---

Update Frequency

```python id="u038"
Every frame
```

---

# 10. INPUT SYSTEM

---

Mouse Left Click

```text id="u039"
Place selected entity
```

---

Mouse Right Click

```text id="u040"
Delete entity
```

---

Mouse Drag

```text id="u041"
Continuous placement
```

---

# 11. EDITOR MODE

---

Available Only In

```text id="u042"
EDIT
```

---

Supported Tools

```text id="u043"
Wall Tool

Robot Tool

Victim Tool

Fire Tool

Rescue Tool

Erase Tool
```

---

Validation

```text id="u044"
No overlapping entities
```

---

# 12. COMMAND DISPATCH

---

UI does not call logic directly.

---

Required Flow

```text id="u045"
User Action

↓

UI Event

↓

Engine Command

↓

Engine Update

↓

Render New State
```

---

Forbidden Flow

```text id="u046"
UI

↓

Modify GameState
```

---

# 13. FRAME RENDER LOOP

---

Pseudo Code

```python id="u047"
while running:

    process_input()

    draw_grid()

    draw_entities()

    draw_overlays()

    draw_sidebar()

    refresh_screen()
```

---

Rule

```text id="u048"
Render only
```

---

# 14. PERFORMANCE REQUIREMENTS

---

Target FPS

```python id="u049"
30 FPS minimum
```

---

Preferred FPS

```python id="u050"
60 FPS
```

---

Input Latency

```python id="u051"
< 100 ms
```

---

Renderer Budget

```python id="u052"
< 10 ms/frame
```

---

# 15. RESPONSIVE GRID

---

Supported Sizes

```python id="u053"
10x10

15x15

20x20

25x25

30x30

35x35
```

---

Requirement

```text id="u054"
Auto scale cell size
```

---

Formula

```python id="u055"
cell_size =

available_grid_area

/

grid_dimension
```

---

# 16. ANIMATION RULES

---

Robot Movement

```text id="u056"
Instant in v1
```

---

Fire Spread

```text id="u057"
Instant in v1
```

---

Future

```text id="u058"
Smooth interpolation
```

---

# 17. BENCHMARK UI

---

Purpose

```text id="u059"
Compare algorithms
```

---

Table Columns

```text id="u060"
Algorithm

Success

Execution Time

Expanded Nodes

Path Cost

Victims Saved

Victims Dead

Score
```

---

Sorting

```text id="u061"
Highest Score First
```

---

# 18. ERROR DISPLAY

---

Validation Error

```text id="u062"
Non-blocking popup
```

---

Runtime Error

```text id="u063"
Status panel warning
```

---

Rule

```text id="u064"
Never crash UI
```

---

# 19. ACCESSIBILITY

---

Requirements

```text id="u065"
Readable fonts

Clear colors

Consistent layout
```

---

Minimum Font Size

```python id="u066"
12 px
```

---

# 20. SUCCESS CRITERIA

UI passes review when:

```text id="u067"
No business logic

Engine-driven updates

Stable rendering

30 FPS achieved

Responsive controls

Benchmark view functional
```

---

# END OF FILE

File Number

```text id="u068"
15_ui_system_design.md
```

Next File

```text id="u069"
16_logging_monitoring.md
```

Purpose

```text id="u070"
Structured Logging

Monitoring

Debug Events

Performance Metrics

Runtime Observability

Audit Trail
```
