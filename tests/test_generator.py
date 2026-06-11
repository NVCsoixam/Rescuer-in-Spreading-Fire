"""
tests/test_generator.py

Unit tests for the MapGenerator.
"""

from app.config import CellType
from app.core.state import Position
from app.map.generator import MapGenerator


def test_map_generator_determinism() -> None:
    """Test that the same seed produces exactly the same map layout."""
    generator = MapGenerator()

    # Generate map 1
    state1 = generator.generate(
        width=20, height=20,
        seed=42
    )

    # Generate map 2 with same seed
    state2 = generator.generate(
        width=20, height=20,
        seed=42
    )

    # Assert exact match of cell layouts
    for y in range(20):
        for x in range(20):
            assert state1.grid[y][x].cell_type == state2.grid[y][x].cell_type

    # Assert identical entity placements
    assert state1.robot.position == state2.robot.position
    assert len(state1.victims) == len(state2.victims)
    for v1, v2 in zip(state1.victims, state2.victims):
        assert v1.position == v2.position
        assert v1.victim_id == v2.victim_id

    assert len(state1.rescue_stations) == len(state2.rescue_stations)
    for r1, r2 in zip(state1.rescue_stations, state2.rescue_stations):
        assert r1.position == r2.position
        assert r1.station_id == r2.station_id


def test_map_generator_different_seeds() -> None:
    """Test that different seeds produce different map layouts."""
    generator = MapGenerator()

    state1 = generator.generate(
        width=20, height=20,
        seed=42
    )

    state2 = generator.generate(
        width=20, height=20,
        seed=100
    )

    # They should differ at least in robot position or cell layouts
    differ = False
    if state1.robot.position != state2.robot.position:
        differ = True
    else:
        for y in range(20):
            for x in range(20):
                if state1.grid[y][x].cell_type != state2.grid[y][x].cell_type:
                    differ = True
                    break
            if differ:
                break

    assert differ, "Maps with different seeds must not be identical."


def test_connectivity_check() -> None:
    """Test that generated maps verify reachability of entities."""
    generator = MapGenerator()
    state = generator.generate(
        width=15, height=15,
        seed=1337
    )

    # Verify entities exist
    assert state.robot is not None
    assert len(state.victims) == 5
    assert len(state.rescue_stations) == 3
    assert len(state.fire_cells) == 1

    # Hand-rolled BFS to verify reachability from test code
    visited = {(state.robot.x, state.robot.y)}
    queue = [state.robot.position]
    head = 0

    while head < len(queue):
        curr = queue[head]
        head += 1
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = curr.x + dx, curr.y + dy
            if (0 <= nx < 15) and (0 <= ny < 15) and (nx, ny) not in visited:
                cell_type = state.grid[ny][nx].cell_type
                if cell_type != CellType.WALL and cell_type != CellType.FIRE:
                    visited.add((nx, ny))
                    queue.append(Position(nx, ny))

    # All victims must be reachable
    for v in state.victims:
        assert (v.x, v.y) in visited

    # All rescue stations must be reachable
    for r in state.rescue_stations:
        assert (r.x, r.y) in visited