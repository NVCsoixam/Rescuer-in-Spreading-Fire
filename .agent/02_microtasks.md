# 02_microtasks.md

# Rescue Simulation 2D

## PURPOSE

Tài liệu này phân rã các Task (P00-Txx) thành các Micro Tasks có kích thước đủ nhỏ để AI Coding Agent thực hiện trực tiếp.

Mỗi Micro Task phải:

* Có mục tiêu duy nhất
* Có đầu ra rõ ràng
* Có thể kiểm chứng
* Không chứa nhiều trách nhiệm cùng lúc

---

# PHASE 1 — FOUNDATION LAYER

---

# P00-T01 — Project Bootstrap

## MT-01

Create package structure

Files:

```text
app/
app/core/
app/map/
app/fire/
app/ai/
app/logic/
app/ui/
tests/
docs/
```

Output:

```text
Project directories created
```

---

## MT-02

Create package initialization files

Files:

```text
app/__init__.py

app/core/__init__.py
app/map/__init__.py
app/fire/__init__.py
app/ai/__init__.py
app/logic/__init__.py
app/ui/__init__.py
```

Output:

```text
Python package imports work
```

---

## MT-03

Create application entry point

File:

```text
main.py
```

Requirements:

* define main()
* define bootstrap stub

Output:

```text
Application starts without error
```

---

## MT-04

Add startup guard

```python
if __name__ == "__main__":
    main()
```

Output:

```text
Executable application entry point
```

---

# P00-T02 — Dependency And Tooling Setup

## MT-05

Create requirements.txt

Dependencies:

```text
pygame
pytest
```

Output:

```text
Installable dependency list
```

---

## MT-06

Create pyproject.toml

Configure:

```text
pytest
black
```

Output:

```text
Toolchain configuration
```

---

## MT-07

Create .gitignore

Ignore:

```text
venv
__pycache__
.pytest_cache
.idea
.vscode
```

Output:

```text
Clean repository
```

---

# P00-T03 — Global Configuration System

## MT-08

Create config.py

File:

```text
app/config.py
```

Output:

```text
Central configuration module
```

---

## MT-09

Define grid size limits

Constants:

```python
GRID_MIN_SIZE = 10
GRID_MAX_SIZE = 35
GRID_DEFAULT_SIZE = 20
```

Output:

```text
Grid constraints centralized
```

---

## MT-10

Define fire interval limits

Constants:

```python
FIRE_INTERVAL_MIN = 0
FIRE_INTERVAL_MAX = 10000
FIRE_INTERVAL_DEFAULT = 1000
```

Output:

```text
Fire timing centralized
```

---

## MT-11

Define cell types

Constants:

```python
EMPTY
WALL
FIRE
VICTIM
ROBOT
RESCUE
```

Output:

```text
Shared world model identifiers
```

---

## MT-12

Define simulation states

Constants:

```python
IDLE
EDIT
RUNNING
PAUSED
FINISHED
```

Output:

```text
Lifecycle state identifiers
```

---

## MT-13

Define movement vectors

Constants:

```python
UP
DOWN
LEFT
RIGHT
```

Output:

```text
Movement system constants
```

---

# PHASE 2 — CORE DATA LAYER

---

# P00-T04 — Game State Models

## MT-14

Create state.py

File:

```text
app/core/state.py
```

Output:

```text
State module exists
```

---

## MT-15

Create Cell dataclass

Fields:

```python
x
y
cell_type
risk
fire_level
```

Output:

```text
Grid cell representation
```

---

## MT-16

Create Robot dataclass

Fields:

```python
x
y
alive
carrying
steps
```

Output:

```text
Robot entity model
```

---

## MT-17

Create Victim dataclass

Fields:

```python
x
y
alive
rescued
```

Output:

```text
Victim entity model
```

---

## MT-18

Create RescueStation dataclass

Fields:

```python
x
y
```

Output:

```text
Rescue station model
```

---

## MT-19

Create GameState dataclass

Fields:

```python
grid
robot
victims
rescue_stations
fire_cells

saved_count
dead_count

simulation_time

current_mode
```

Output:

```text
Single source of truth state
```

---

## MT-20

Add state validation helpers

Checks:

```text
Single robot
Valid positions
No overlaps
```

Output:

```text
State consistency validation
```

---

# P00-T05 — Snapshot System

## MT-21

Create snapshot.py

File:

```text
app/core/snapshot.py
```

Output:

```text
Snapshot module exists
```

---

## MT-22

Implement create_snapshot()

Responsibilities:

```text
Deep copy GameState
```

Output:

```text
State backup available
```

---

## MT-23

Implement restore_snapshot()

Responsibilities:

```text
Restore previous state
```

Output:

```text
Deterministic reset support
```

---

## MT-24

Verify snapshot isolation

Requirements:

```text
No shared references
```

Output:

```text
Safe rollback behavior
```

---

# P00-T06 — Grid System

## MT-25

Create grid.py

File:

```text
app/map/grid.py
```

Output:

```text
Grid abstraction module
```

---

## MT-26

Implement Grid class

Responsibilities:

```text
Store cells
Manage dimensions
```

Output:

```text
Reusable grid container
```

---

## MT-27

Implement get_cell()

Output:

```text
Safe cell access
```

---

## MT-28

Implement set_cell()

Output:

```text
Controlled cell mutation
```

---

## MT-29

Implement in_bounds()

Output:

```text
Coordinate validation
```

---

## MT-30

Implement get_neighbors()

Rules:

```text
4-direction only
No diagonal movement
```

Output:

```text
Neighbor expansion utility
```

---

## MT-31

Implement walkable check

Rules:

```text
Wall blocked
Fire blocked
```

Output:

```text
Navigation validation
```

---

# END OF PART 1

Covered:

* P00-T01
* P00-T02
* P00-T03
* P00-T04
* P00-T05
* P00-T06

Next file section will continue from:

P00-T07 — Map Generator

# 02_microtasks.md (PART 2)

# PHASE 2 — CORE DATA LAYER (CONTINUED)

---

# P00-T07 — Map Generator

## MT-32

Create generator.py

File:

```text
app/map/generator.py
```

Output:

```text
Map generation module exists
```

---

## MT-33

Create MapGenerator class

Responsibilities:

```text
Generate structured maps
Validate generated maps
Place entities
```

Output:

```text
Reusable generator component
```

---

## MT-34

Implement generate_empty_map()

Inputs:

```text
width
height
```

Output:

```text
Empty grid initialized
```

---

## MT-35

Implement room generation

Rules:

```text
Generate rectangular rooms
Random size within limits
No room overlap
```

Output:

```text
Building-like structure
```

---

## MT-36

Implement corridor generation

Rules:

```text
Connect generated rooms
Horizontal corridors
Vertical corridors
```

Output:

```text
Reachable room network
```

---

## MT-37

Implement wall placement

Rules:

```text
Walls define room boundaries
Walls block movement
Walls block fire spread
```

Output:

```text
Structured environment
```

---

## MT-38

Implement connectivity validation

Checks:

```text
All major regions connected
```

Output:

```text
No isolated playable areas
```

---

## MT-39

Implement robot placement

Rules:

```text
Exactly one robot
Spawn on walkable cell
```

Output:

```text
Valid robot spawn
```

---

## MT-40

Implement rescue station placement

Rules:

```text
Default = 3
At least 1
Walkable cells only
```

Output:

```text
Valid rescue stations
```

---

## MT-41

Implement victim placement

Rules:

```text
Default = 5
Walkable cells only
No overlap
```

Output:

```text
Victim distribution complete
```

---

## MT-42

Implement fire source placement

Rules:

```text
Default = 1
Walkable cell only
```

Output:

```text
Fire source initialized
```

---

## MT-43

Validate reachability

Checks:

```text
Robot -> Victim reachable
Victim -> Rescue reachable
```

Output:

```text
Playable map guaranteed
```

---

## MT-44

Implement regenerate-on-failure

Rules:

```text
Invalid map => regenerate
```

Output:

```text
Reliable map creation
```

---

# PHASE 3 — SIMULATION ENGINE

---

# P00-T08 — Movement Logic

## MT-45

Create movement.py

File:

```text
app/logic/movement.py
```

Output:

```text
Movement module exists
```

---

## MT-46

Implement move_up()

Output:

```text
Robot can move upward
```

---

## MT-47

Implement move_down()

Output:

```text
Robot can move downward
```

---

## MT-48

Implement move_left()

Output:

```text
Robot can move left
```

---

## MT-49

Implement move_right()

Output:

```text
Robot can move right
```

---

## MT-50

Implement generic move()

Inputs:

```text
current_position
direction
```

Output:

```text
Reusable movement API
```

---

## MT-51

Validate boundaries

Rules:

```text
Cannot leave grid
```

Output:

```text
Safe movement
```

---

## MT-52

Validate wall collision

Rules:

```text
Cannot move through walls
```

Output:

```text
Wall blocking enforced
```

---

## MT-53

Validate fire collision

Rules:

```text
Cannot move into active fire
```

Output:

```text
Fire avoidance support
```

---

## MT-54

Track step counter

Rules:

```text
Increment every valid move
```

Output:

```text
Movement statistics available
```

---

# P00-T09 — Rescue System

## MT-55

Create rescue.py

File:

```text
app/logic/rescue.py
```

Output:

```text
Rescue module exists
```

---

## MT-56

Implement victim detection

Rules:

```text
Robot shares cell with victim
```

Output:

```text
Victim interaction enabled
```

---

## MT-57

Implement pickup_victim()

Rules:

```text
Only one victim at a time
```

Output:

```text
Carry state supported
```

---

## MT-58

Prevent multiple carrying

Rules:

```text
Cannot pickup second victim
```

Output:

```text
Carry limit enforced
```

---

## MT-59

Implement rescue station detection

Output:

```text
Station interaction enabled
```

---

## MT-60

Implement drop_victim()

Rules:

```text
Must stand on rescue station
```

Output:

```text
Victim delivery supported
```

---

## MT-61

Update rescued counter

Output:

```text
Statistics updated
```

---

## MT-62

Remove rescued victim from active list

Output:

```text
State cleanup complete
```

---

# P00-T10 — Fire Simulation

## MT-63

Create fire_sim.py

File:

```text
app/fire/fire_sim.py
```

Output:

```text
Fire simulation module exists
```

---

## MT-64

Create FireManager class

Responsibilities:

```text
Track active fire cells
Handle fire spread
Emit fire events
```

Output:

```text
Central fire controller
```

---

## MT-65

Implement fire timer

Inputs:

```text
fire_interval
```

Output:

```text
Timed fire spread
```

---

## MT-66

Implement fire tick()

Responsibilities:

```text
Advance fire simulation
```

Output:

```text
Fire progresses over time
```

---

## MT-67

Implement 4-direction spread

Rules:

```text
Up
Down
Left
Right
```

Output:

```text
Deterministic spread pattern
```

---

## MT-68

Prevent spread through walls

Output:

```text
Walls block fire
```

---

## MT-69

Prevent duplicate ignition

Rules:

```text
Already burning cells ignored
```

Output:

```text
Stable fire propagation
```

---

## MT-70

Implement victim burn handling

Rules:

```text
Victim touched by fire => dead
```

Output:

```text
Victim death supported
```

---

## MT-71

Update dead counter

Output:

```text
Death statistics tracked
```

---

## MT-72

Implement robot burn detection

Rules:

```text
Robot touched by fire
```

Output:

```text
Mission failure trigger
```

---

## MT-73

Emit fire spread events

Used by:

```text
Logging
Heatmap
Engine
```

Output:

```text
Event propagation available
```

---

# P00-T11 — Heat Map System

## MT-74

Create heatmap.py

File:

```text
app/fire/heatmap.py
```

Output:

```text
Heatmap module exists
```

---

## MT-75

Create RiskMap class

Output:

```text
Risk calculation component
```

---

## MT-76

Define risk scale

Levels:

```text
0.0 Safe
0.3 Warning
0.6 Danger
0.9 Critical
1.0 Fire
```

Output:

```text
Standardized risk model
```

---

## MT-77

Calculate distance-to-fire

Output:

```text
Risk propagation basis
```

---

## MT-78

Generate risk values

Rules:

```text
Closer fire => higher risk
```

Output:

```text
Continuous danger model
```

---

## MT-79

Update heatmap after fire spread

Output:

```text
Risk map stays synchronized
```

---

## MT-80

Provide get_risk()

Inputs:

```text
x
y
```

Output:

```text
Risk lookup API
```

---

## MT-81

Provide risk overlay data

Used by:

```text
Renderer
```

Output:

```text
Visualization support
```

---

# END OF PART 2

Covered:

```text
P00-T07 Map Generator
P00-T08 Movement Logic
P00-T09 Rescue System
P00-T10 Fire Simulation
P00-T11 Heat Map System
```

Next section:

```text
P00-T12 Core Engine
P00-T13 BFS
P00-T14 DFS
P00-T15 UCS
P00-T16 Dijkstra
P00-T17 Greedy
P00-T18 A*
P00-T19 Shared AI Utilities
```
# 02_microtasks.md (PART 3)

# PHASE 3 — SIMULATION ENGINE (CONTINUED)

---

# P00-T12 — Core Engine

## MT-82

Create engine.py

File:

```text
app/core/engine.py
```

Output:

```text
Central simulation engine module
```

---

## MT-83

Create Engine class

Responsibilities:

```text
Own GameState
Coordinate all subsystems
Control simulation lifecycle
```

Output:

```text
Single simulation controller
```

---

## MT-84

Inject dependencies

Dependencies:

```text
Grid
FireManager
RiskMap
Movement
Rescue
AI
```

Output:

```text
Subsystem orchestration ready
```

---

## MT-85

Implement start()

Responsibilities:

```text
Switch IDLE -> RUNNING
```

Output:

```text
Simulation can start
```

---

## MT-86

Implement pause()

Responsibilities:

```text
RUNNING -> PAUSED
```

Output:

```text
Simulation pausable
```

---

## MT-87

Implement resume()

Responsibilities:

```text
PAUSED -> RUNNING
```

Output:

```text
Simulation resumable
```

---

## MT-88

Implement stop()

Responsibilities:

```text
Finish simulation safely
```

Output:

```text
Controlled shutdown
```

---

## MT-89

Implement reset()

Responsibilities:

```text
Restore snapshot
```

Output:

```text
Deterministic restart
```

---

## MT-90

Implement simulation_step()

Responsibilities:

```text
Advance one tick
```

Output:

```text
Core update loop
```

---

## MT-91

Update simulation clock

Output:

```text
Elapsed time tracked
```

---

## MT-92

Process fire updates

Output:

```text
Fire integrated into loop
```

---

## MT-93

Process AI updates

Output:

```text
AI integrated into loop
```

---

## MT-94

Process rescue updates

Output:

```text
Rescue logic integrated
```

---

## MT-95

Evaluate end conditions

Checks:

```text
All victims rescued
Robot dead
No reachable victims
```

Output:

```text
Simulation termination support
```

---

## MT-96

Create engine event dispatcher

Events:

```text
FireSpread
Move
Pickup
Drop
Death
Finish
```

Output:

```text
Internal event flow available
```

---

# PHASE 4 — AI PATHFINDING

---

# P00-T19 — Shared AI Utilities

## MT-97

Create _shared.py

File:

```text
app/ai/_shared.py
```

Output:

```text
Shared AI utility module
```

---

## MT-98

Create PathResult model

Fields:

```text
found
path
cost
expanded_nodes
```

Output:

```text
Unified algorithm output
```

---

## MT-99

Implement reconstruct_path()

Output:

```text
Parent map -> path conversion
```

---

## MT-100

Implement manhattan_distance()

Output:

```text
Grid heuristic available
```

---

## MT-101

Implement euclidean_distance()

Output:

```text
Alternative heuristic available
```

---

## MT-102

Implement get_valid_neighbors()

Rules:

```text
4-direction movement
Ignore walls
Ignore fire
```

Output:

```text
Reusable expansion logic
```

---

## MT-103

Implement movement_cost()

Output:

```text
Traversal cost abstraction
```

---

## MT-104

Implement risk_aware_cost()

Rules:

```text
Base cost + risk penalty
```

Output:

```text
Risk-sensitive search support
```

---

# P00-T13 — BFS

## MT-105

Create bfs.py

Output:

```text
BFS module exists
```

---

## MT-106

Implement bfs()

Inputs:

```text
grid
start
goal
```

Output:

```text
Breadth-first search implementation
```

---

## MT-107

Create queue management

Output:

```text
FIFO traversal
```

---

## MT-108

Track visited nodes

Output:

```text
No duplicate expansion
```

---

## MT-109

Track parent nodes

Output:

```text
Path reconstruction support
```

---

## MT-110

Return PathResult

Output:

```text
Standardized algorithm result
```

---

# P00-T14 — DFS

## MT-111

Create dfs.py

Output:

```text
DFS module exists
```

---

## MT-112

Implement dfs()

Output:

```text
Depth-first search implementation
```

---

## MT-113

Create stack management

Output:

```text
LIFO traversal
```

---

## MT-114

Track visited nodes

Output:

```text
Prevent infinite loops
```

---

## MT-115

Return PathResult

Output:

```text
Standardized result
```

---

# P00-T15 — UCS

## MT-116

Create ucs.py

Output:

```text
UCS module exists
```

---

## MT-117

Implement ucs()

Output:

```text
Uniform Cost Search
```

---

## MT-118

Create priority queue

Output:

```text
Lowest cost expansion
```

---

## MT-119

Track cumulative cost

Output:

```text
Cost-aware search
```

---

## MT-120

Return PathResult

Output:

```text
Unified result object
```

---

# P00-T16 — Dijkstra

## MT-121

Create dijkstra.py

Output:

```text
Dijkstra module exists
```

---

## MT-122

Implement dijkstra()

Output:

```text
Shortest path algorithm
```

---

## MT-123

Maintain distance table

Output:

```text
Optimal distance tracking
```

---

## MT-124

Update priority queue logic

Output:

```text
Efficient node ordering
```

---

## MT-125

Return PathResult

Output:

```text
Standard result format
```

---

# P00-T17 — Greedy Search

## MT-126

Create greedy.py

Output:

```text
Greedy module exists
```

---

## MT-127

Implement greedy_search()

Output:

```text
Heuristic-driven search
```

---

## MT-128

Use Manhattan heuristic

Output:

```text
Target-directed exploration
```

---

## MT-129

Track explored nodes

Output:

```text
Search statistics available
```

---

## MT-130

Return PathResult

Output:

```text
Unified output structure
```

---

# P00-T18 — A*

## MT-131

Create astar.py

Output:

```text
A* module exists
```

---

## MT-132

Implement astar()

Output:

```text
A* pathfinding algorithm
```

---

## MT-133

Implement f = g + h scoring

Output:

```text
Optimal informed search
```

---

## MT-134

Maintain open set

Output:

```text
Candidate frontier management
```

---

## MT-135

Maintain closed set

Output:

```text
Processed node tracking
```

---

## MT-136

Implement risk-aware mode

Rules:

```text
Risk contributes to movement cost
```

Output:

```text
Fire-aware navigation
```

---

## MT-137

Implement path replanning support

Trigger:

```text
Fire map changed
```

Output:

```text
Dynamic adaptation
```

---

## MT-138

Return PathResult

Output:

```text
Unified algorithm result
```

---

# END OF PART 3

Covered:

```text
P00-T12 Core Engine
P00-T13 BFS
P00-T14 DFS
P00-T15 UCS
P00-T16 Dijkstra
P00-T17 Greedy
P00-T18 A*
P00-T19 Shared AI Utilities
```

Next section:

```text
P00-T20 Simulation Lifecycle
P00-T21 Validation System
P00-T22 Logging System
P00-T23 Grid Renderer
P00-T24 Sidebar UI
P00-T25 Input Controls
```
# 02_microtasks.md (PART 4)

# PHASE 5 — STATE MACHINE + VALIDATION

---

# P00-T20 — Simulation Lifecycle

## MT-139

Define lifecycle enum

States:

```text
IDLE
EDIT
RUNNING
PAUSED
FINISHED
```

Output:

```text
Standard lifecycle model
```

---

## MT-140

Initialize engine in IDLE state

Output:

```text
Consistent startup state
```

---

## MT-141

Implement IDLE → EDIT transition

Trigger:

```text
User starts map editing
```

Output:

```text
Editable environment
```

---

## MT-142

Implement EDIT → RUNNING transition

Checks:

```text
Map validation passed
Snapshot created
```

Output:

```text
Safe simulation start
```

---

## MT-143

Prevent RUNNING without snapshot

Output:

```text
Deterministic reset guarantee
```

---

## MT-144

Implement RUNNING → PAUSED

Output:

```text
Pause support
```

---

## MT-145

Implement PAUSED → RUNNING

Output:

```text
Resume support
```

---

## MT-146

Implement RUNNING → FINISHED

Triggers:

```text
All victims rescued
Robot destroyed
No valid rescue path
```

Output:

```text
Proper completion state
```

---

## MT-147

Implement FINISHED → IDLE

Output:

```text
Ready for next simulation
```

---

## MT-148

Validate illegal transitions

Examples:

```text
IDLE -> FINISHED
FINISHED -> RUNNING
```

Output:

```text
State machine integrity
```

---

# P00-T21 — Validation System

## MT-149

Create validator component

Output:

```text
Central validation service
```

---

## MT-150

Validate grid dimensions

Checks:

```text
10 <= size <= 35
```

Output:

```text
Valid map size
```

---

## MT-151

Validate robot existence

Checks:

```text
Exactly one robot
```

Output:

```text
Valid robot state
```

---

## MT-152

Validate victim count

Checks:

```text
Victim count >= 1
```

Output:

```text
Rescue mission possible
```

---

## MT-153

Validate rescue station count

Checks:

```text
Station count >= 1
```

Output:

```text
Valid delivery target
```

---

## MT-154

Validate fire source count

Checks:

```text
Fire source count >= 1
```

Output:

```text
Dynamic environment guaranteed
```

---

## MT-155

Detect overlapping entities

Checks:

```text
Robot
Victim
Fire
Station
```

Output:

```text
World consistency maintained
```

---

## MT-156

Validate reachability

Checks:

```text
Robot -> Victim
Victim -> Rescue
```

Output:

```text
Playable map guarantee
```

---

## MT-157

Generate validation report

Output:

```text
Detailed validation feedback
```

---

# P00-T22 — Logging System

## MT-158

Configure logger

Levels:

```text
DEBUG
INFO
WARNING
ERROR
```

Output:

```text
Structured logging foundation
```

---

## MT-159

Create simulation logger

Output:

```text
Centralized event logging
```

---

## MT-160

Log movement events

Fields:

```text
Position
Direction
Step count
```

Output:

```text
Movement traceability
```

---

## MT-161

Log fire spread events

Fields:

```text
Source cell
Target cell
Timestamp
```

Output:

```text
Fire traceability
```

---

## MT-162

Log pathfinding start

Fields:

```text
Algorithm
Start
Goal
```

Output:

```text
Search visibility
```

---

## MT-163

Log pathfinding finish

Fields:

```text
Found
Cost
Expanded nodes
```

Output:

```text
Algorithm diagnostics
```

---

## MT-164

Log rescue events

Events:

```text
Pickup
Drop
Victim saved
Victim dead
```

Output:

```text
Mission traceability
```

---

## MT-165

Log simulation finish

Output:

```text
Final mission summary
```

---

# PHASE 6 — UI SYSTEM

---

# P00-T23 — Grid Renderer

## MT-166

Create renderer.py

Output:

```text
Renderer module exists
```

---

## MT-167

Create Renderer class

Output:

```text
Rendering subsystem initialized
```

---

## MT-168

Render grid background

Output:

```text
Visible world layout
```

---

## MT-169

Render walls

Output:

```text
Obstacle visualization
```

---

## MT-170

Render robot

Output:

```text
Robot visualization
```

---

## MT-171

Render victims

Output:

```text
Victim visualization
```

---

## MT-172

Render rescue stations

Output:

```text
Station visualization
```

---

## MT-173

Render fire cells

Output:

```text
Fire visualization
```

---

## MT-174

Render risk overlay

Output:

```text
Heatmap visualization
```

---

## MT-175

Render AI path

Output:

```text
Path visualization
```

---

## MT-176

Render simulation status

Output:

```text
Live feedback
```

---

# END OF PART 4

Covered:

```text
P00-T20 Simulation Lifecycle
P00-T21 Validation System
P00-T22 Logging System
P00-T23 Grid Renderer
```

Next part:

```text
P00-T24 Sidebar UI
P00-T25 Input Controls
P00-T26 Unit Tests
P00-T27 Integration Tests
P00-T28 Documentation
P00-T29 Final Refactor
```
# 02_microtasks.md (PART 4)

# PHASE 5 — STATE MACHINE + VALIDATION

---

# P00-T20 — Simulation Lifecycle

## MT-139

Define lifecycle enum

States:

```text
IDLE
EDIT
RUNNING
PAUSED
FINISHED
```

Output:

```text
Standard lifecycle model
```

---

## MT-140

Initialize engine in IDLE state

Output:

```text
Consistent startup state
```

---

## MT-141

Implement IDLE → EDIT transition

Trigger:

```text
User starts map editing
```

Output:

```text
Editable environment
```

---

## MT-142

Implement EDIT → RUNNING transition

Checks:

```text
Map validation passed
Snapshot created
```

Output:

```text
Safe simulation start
```

---

## MT-143

Prevent RUNNING without snapshot

Output:

```text
Deterministic reset guarantee
```

---

## MT-144

Implement RUNNING → PAUSED

Output:

```text
Pause support
```

---

## MT-145

Implement PAUSED → RUNNING

Output:

```text
Resume support
```

---

## MT-146

Implement RUNNING → FINISHED

Triggers:

```text
All victims rescued
Robot destroyed
No valid rescue path
```

Output:

```text
Proper completion state
```

---

## MT-147

Implement FINISHED → IDLE

Output:

```text
Ready for next simulation
```

---

## MT-148

Validate illegal transitions

Examples:

```text
IDLE -> FINISHED
FINISHED -> RUNNING
```

Output:

```text
State machine integrity
```

---

# P00-T21 — Validation System

## MT-149

Create validator component

Output:

```text
Central validation service
```

---

## MT-150

Validate grid dimensions

Checks:

```text
10 <= size <= 35
```

Output:

```text
Valid map size
```

---

## MT-151

Validate robot existence

Checks:

```text
Exactly one robot
```

Output:

```text
Valid robot state
```

---

## MT-152

Validate victim count

Checks:

```text
Victim count >= 1
```

Output:

```text
Rescue mission possible
```

---

## MT-153

Validate rescue station count

Checks:

```text
Station count >= 1
```

Output:

```text
Valid delivery target
```

---

## MT-154

Validate fire source count

Checks:

```text
Fire source count >= 1
```

Output:

```text
Dynamic environment guaranteed
```

---

## MT-155

Detect overlapping entities

Checks:

```text
Robot
Victim
Fire
Station
```

Output:

```text
World consistency maintained
```

---

## MT-156

Validate reachability

Checks:

```text
Robot -> Victim
Victim -> Rescue
```

Output:

```text
Playable map guarantee
```

---

## MT-157

Generate validation report

Output:

```text
Detailed validation feedback
```

---

# P00-T22 — Logging System

## MT-158

Configure logger

Levels:

```text
DEBUG
INFO
WARNING
ERROR
```

Output:

```text
Structured logging foundation
```

---

## MT-159

Create simulation logger

Output:

```text
Centralized event logging
```

---

## MT-160

Log movement events

Fields:

```text
Position
Direction
Step count
```

Output:

```text
Movement traceability
```

---

## MT-161

Log fire spread events

Fields:

```text
Source cell
Target cell
Timestamp
```

Output:

```text
Fire traceability
```

---

## MT-162

Log pathfinding start

Fields:

```text
Algorithm
Start
Goal
```

Output:

```text
Search visibility
```

---

## MT-163

Log pathfinding finish

Fields:

```text
Found
Cost
Expanded nodes
```

Output:

```text
Algorithm diagnostics
```

---

## MT-164

Log rescue events

Events:

```text
Pickup
Drop
Victim saved
Victim dead
```

Output:

```text
Mission traceability
```

---

## MT-165

Log simulation finish

Output:

```text
Final mission summary
```

---

# PHASE 6 — UI SYSTEM

---

# P00-T23 — Grid Renderer

## MT-166

Create renderer.py

Output:

```text
Renderer module exists
```

---

## MT-167

Create Renderer class

Output:

```text
Rendering subsystem initialized
```

---

## MT-168

Render grid background

Output:

```text
Visible world layout
```

---

## MT-169

Render walls

Output:

```text
Obstacle visualization
```

---

## MT-170

Render robot

Output:

```text
Robot visualization
```

---

## MT-171

Render victims

Output:

```text
Victim visualization
```

---

## MT-172

Render rescue stations

Output:

```text
Station visualization
```

---

## MT-173

Render fire cells

Output:

```text
Fire visualization
```

---

## MT-174

Render risk overlay

Output:

```text
Heatmap visualization
```

---

## MT-175

Render AI path

Output:

```text
Path visualization
```

---

## MT-176

Render simulation status

Output:

```text
Live feedback
```

---

# END OF PART 4

Covered:

```text
P00-T20 Simulation Lifecycle
P00-T21 Validation System
P00-T22 Logging System
P00-T23 Grid Renderer
```

Next part:

```text
P00-T24 Sidebar UI
P00-T25 Input Controls
P00-T26 Unit Tests
P00-T27 Integration Tests
P00-T28 Documentation
P00-T29 Final Refactor
```
# 02_microtasks.md (PART 5)

# PHASE 6 — UI SYSTEM (CONTINUED)

---

# P00-T24 — Sidebar UI

## MT-177

Create sidebar.py

Output:

```text
Sidebar module exists
```

---

## MT-178

Create Sidebar class

Responsibilities:

```text
Render controls
Render status
Handle UI widgets
```

Output:

```text
Sidebar subsystem initialized
```

---

## MT-179

Create map settings panel

Controls:

```text
Grid size
Victim count
Fire count
Rescue station count
```

Output:

```text
Map configuration UI
```

---

## MT-180

Create fire settings panel

Controls:

```text
Fire interval
Fire enable
```

Output:

```text
Fire configuration UI
```

---

## MT-181

Create algorithm selector

Algorithms:

```text
BFS
DFS
UCS
Dijkstra
Greedy
A*
```

Output:

```text
Algorithm selection UI
```

---

## MT-182

Create run controls

Buttons:

```text
Generate
Start
Pause
Resume
Reset
```

Output:

```text
Simulation controls available
```

---

## MT-183

Create edit tools panel

Tools:

```text
Wall
Robot
Victim
Fire
Rescue Station
Erase
```

Output:

```text
Map editing controls
```

---

## MT-184

Create status panel

Fields:

```text
Mode
Time
Steps
Saved
Dead
Remaining
```

Output:

```text
Live simulation status
```

---

## MT-185

Display selected algorithm

Output:

```text
Current AI visible
```

---

## MT-186

Display carrying status

Output:

```text
Robot load status visible
```

---

## MT-187

Display validation warnings

Output:

```text
User feedback available
```

---

## MT-188

Display simulation result summary

Output:

```text
Mission outcome visible
```

---

# P00-T25 — Input Controls

## MT-189

Create controls.py

Output:

```text
Input control module exists
```

---

## MT-190

Create InputController class

Output:

```text
Input system initialized
```

---

## MT-191

Handle mouse position mapping

Output:

```text
Screen -> Grid conversion
```

---

## MT-192

Handle wall placement

Output:

```text
Wall editing supported
```

---

## MT-193

Handle wall removal

Output:

```text
Wall erase supported
```

---

## MT-194

Handle robot placement

Rules:

```text
Only one robot
```

Output:

```text
Robot editing supported
```

---

## MT-195

Handle victim placement

Output:

```text
Victim editing supported
```

---

## MT-196

Handle fire placement

Output:

```text
Fire source editing supported
```

---

## MT-197

Handle rescue station placement

Output:

```text
Station editing supported
```

---

## MT-198

Prevent illegal edits while running

Output:

```text
Simulation consistency protected
```

---

## MT-199

Forward edit requests to engine

Rules:

```text
UI contains no logic
```

Output:

```text
Architecture compliance
```

---

## MT-200

Handle keyboard shortcuts

Keys:

```text
Space
R
G
Esc
```

Output:

```text
Fast user interaction
```

---

# PHASE 7 — TESTING

---

# P00-T26 — Unit Tests

## MT-201

Create tests package

Output:

```text
Testing structure exists
```

---

## MT-202

Create grid tests

Coverage:

```text
Bounds
Neighbors
Walkability
```

Output:

```text
Grid correctness verified
```

---

## MT-203

Create movement tests

Coverage:

```text
Valid move
Wall collision
Boundary collision
```

Output:

```text
Movement correctness verified
```

---

## MT-204

Create rescue tests

Coverage:

```text
Pickup
Drop
Carry limit
```

Output:

```text
Rescue correctness verified
```

---

## MT-205

Create fire tests

Coverage:

```text
Spread
Wall blocking
Burn logic
```

Output:

```text
Fire correctness verified
```

---

## MT-206

Create heatmap tests

Coverage:

```text
Risk generation
Risk update
```

Output:

```text
Risk model verified
```

---

## MT-207

Create BFS tests

Output:

```text
BFS verified
```

---

## MT-208

Create DFS tests

Output:

```text
DFS verified
```

---

## MT-209

Create UCS tests

Output:

```text
UCS verified
```

---

## MT-210

Create Dijkstra tests

Output:

```text
Dijkstra verified
```

---

## MT-211

Create Greedy tests

Output:

```text
Greedy verified
```

---

## MT-212

Create A* tests

Output:

```text
A* verified
```

---

## MT-213

Create engine tests

Coverage:

```text
Start
Pause
Resume
Reset
Finish
```

Output:

```text
Engine correctness verified
```

---

# P00-T27 — Integration Tests

## MT-214

Create simulation integration test

Output:

```text
End-to-end validation
```

---

## MT-215

Test full rescue mission

Flow:

```text
Robot
Victim
Rescue
```

Output:

```text
Mission success verified
```

---

## MT-216

Test fire progression

Output:

```text
Dynamic environment verified
```

---

## MT-217

Test AI replanning

Output:

```text
Adaptive navigation verified
```

---

## MT-218

Test snapshot reset

Output:

```text
Deterministic restart verified
```

---

## MT-219

Test all algorithms on same map

Output:

```text
Fair comparison verified
```

---

# PHASE 8 — FINALIZATION

---

# P00-T28 — Documentation

## MT-220

Create architecture documentation

Output:

```text
System architecture documented
```

---

## MT-221

Create module documentation

Output:

```text
All modules documented
```

---

## MT-222

Create algorithm documentation

Output:

```text
Pathfinding algorithms explained
```

---

## MT-223

Create simulation workflow documentation

Output:

```text
Execution flow documented
```

---

## MT-224

Create user guide

Output:

```text
User instructions available
```

---

# P00-T29 — Final Refactor

## MT-225

Remove duplicated logic

Output:

```text
Cleaner codebase
```

---

## MT-226

Review dependency graph

Output:

```text
No circular imports
```

---

## MT-227

Review architecture rules

Checks:

```text
UI no logic
Engine owns state
Pure AI modules
```

Output:

```text
Architecture compliance verified
```

---

## MT-228

Review performance requirements

Checks:

```text
30 FPS
35x35 map
Input latency
```

Output:

```text
Performance validated
```

---

## MT-229

Review error handling

Checks:

```text
Invalid map
Invalid edit
Unreachable victim
Fire isolation
```

Output:

```text
Safe failure behavior verified
```

---

## MT-230

Run final project checklist

Output:

```text
Release candidate ready
```

---

# END OF FILE

Statistics

```text
29 Tasks
230 Micro Tasks

Foundation Layer
Core Layer
Engine Layer
AI Layer
Fire Layer
UI Layer
Testing Layer
Finalization Layer
```

This file acts as the bridge between:

Project Specification
→ Task Registry
→ Micro Tasks
→ Execution Specifications
→ Source Code

```
```

