"""
tests/test_ai.py

Integration tests for all 6 pathfinding algorithms.
"""

from app.config import CellType
from app.core.state import Position
from app.map.grid import Grid

from app.ai.bfs import find_path as bfs_find_path
from app.ai.dfs import find_path as dfs_find_path
from app.ai.ucs import find_path as ucs_find_path
from app.ai.dijkstra import find_path as dijkstra_find_path
from app.ai.greedy import find_path as greedy_find_path
from app.ai.astar import find_path as astar_find_path


def test_all_algorithms_find_path() -> None:
    """Test that all search algorithms find a valid path on a simple maze."""
    grid = Grid(10, 10)

    # Place a vertical wall partition with a door
    for y in range(8):
        grid.set_cell(5, y, CellType.WALL)
    # y=8,9 are empty (open corridor)

    start = Position(2, 2)
    goal = Position(8, 2)

    algorithms = [
        bfs_find_path,
        dfs_find_path,
        ucs_find_path,
        dijkstra_find_path,
        greedy_find_path,
        astar_find_path
    ]

    for algo in algorithms:
        res = algo(grid, start, goal)
        assert res.found is True
        assert len(res.path) > 0
        assert res.path[-1] == goal


def test_risk_aware_navigation() -> None:
    """
    Test that UCS, Dijkstra, and A* avoid high-risk zones,
    while BFS/DFS/Greedy ignore risk and choose the shortest path.
    """
    grid = Grid(10, 10)

    # Start: (0, 0), Goal: (0, 4)
    # Path A (Short): (0,0) -> (0,1) -> (0,2) -> (0,3) -> (0,4) [Length 4]
    # Path B (Long): (0,0) -> (1,0) -> (1,1) -> (1,2) -> (1,3) -> (1,4) -> (0,4) [Length 6]

    start = Position(0, 0)
    goal = Position(0, 4)

    # Place fire cell at (0, 2) to create risk on Path A
    heatmap = [[0.0 for _ in range(10)] for _ in range(10)]
    # Set high risk on the short path cells (0, 1), (0, 2), (0, 3)
    heatmap[1][0] = 0.9
    heatmap[2][0] = 1.0  # Fire position
    heatmap[3][0] = 0.9

    # y=2, x=0 is fire, so grid is not walkable there for any algorithm!
    # Let's place fire at (1, 2) instead, so Path A is walkable but very risky!
    # Path A: (0,0) -> (0,1) -> (0,2) -> (0,3) -> (0,4)
    # Cell (0,2) is adjacent to fire cell at (1,2), so it gets risk=0.9
    # Cell (0,1) and (0,3) get risk=0.7
    grid.set_cell(1, 2, CellType.FIRE)
    heatmap[2][1] = 1.0  # Fire
    heatmap[2][0] = 0.9  # Adjacent cell (high risk)
    heatmap[1][0] = 0.7  # Risk warning
    heatmap[3][0] = 0.7  # Risk warning

    # Test BFS (ignores risk, chooses Path A which is shorter)
    bfs_res = bfs_find_path(grid, start, goal, heatmap)
    assert bfs_res.found is True
    # Should take Path A: length 4
    assert len(bfs_res.path) == 4
    # Check that it goes through (0, 2)
    assert Position(0, 2) in bfs_res.path

    # Test A* (risk-aware, chooses Path B which is longer but has 0.0 risk)
    astar_res = astar_find_path(grid, start, goal, heatmap)
    assert astar_res.found is True
    # Should take Path B: length 8
    assert len(astar_res.path) == 8
    # Should NOT go through (0, 2)
    assert Position(0, 2) not in astar_res.path

    # Test UCS (risk-aware)
    ucs_res = ucs_find_path(grid, start, goal, heatmap)
    assert ucs_res.found is True
    assert len(ucs_res.path) == 8
    assert Position(0, 2) not in ucs_res.path

    # Test Dijkstra (risk-aware)
    dijkstra_res = dijkstra_find_path(grid, start, goal, heatmap)
    assert dijkstra_res.found is True
    assert len(dijkstra_res.path) == 8
    assert Position(0, 2) not in dijkstra_res.path
