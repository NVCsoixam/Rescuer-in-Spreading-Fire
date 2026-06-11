# AI Rescue & Fire Simulation System

A 2D simulation system featuring dynamic fire propagation, AI pathfinding, and victim rescue operations.

## Features

- **Procedural Building Generation** — Room-based map generation with corridors and exits
- **Fire Propagation** — Dynamic fire spread with wall blocking and risk heatmaps
- **Victim Rescue** — Pickup and delivery mechanics with rescue stations
- **6 Pathfinding Algorithms** — BFS, DFS, UCS, Dijkstra, Greedy, A* (with risk-aware mode)
- **Manual Control** — Arrow-key robot movement
- **Real-Time Dashboard** — Status panel with saved/dead/stats tracking
- **Deterministic Snapshots** — Reliable simulation reset mechanism

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Project Structure

```
app/
├── config.py          # Global constants & enums
├── core/              # Engine, state, snapshot, validator, logger
├── map/               # Grid and procedural map generator
├── logic/             # Movement and rescue mechanics
├── fire/              # Fire simulation and heatmap
├── ai/                # 6 pathfinding algorithms
└── ui/                # Pygame renderer, sidebar, controls
```

## Running Tests

```bash
python -m pytest tests/ -v