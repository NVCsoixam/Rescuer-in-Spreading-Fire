"""
app/ai/bfs.py

Breadth-First Search (BFS) pathfinding algorithm.
Returns the shortest path in a grid under uniform edge costs.
"""

import time
from collections import deque
from app.core.state import Position, PathResult
from app.map.grid import Grid
from app.ai._shared import PathNode, reconstruct_path


def find_path(
    grid: Grid,
    start: Position,
    goal: Position,
    heatmap: list[list[float]] = None
) -> PathResult:
    """
    Search for a path from start to goal using Breadth-First Search (BFS).

    Args:
        grid: The grid map.
        start: Starting Position.
        goal: Target Position.
        heatmap: Ignored in BFS (uniform cost).

    Returns:
        PathResult: Search outcome containing paths, cost, and diagnostics.
    """
    start_time = time.perf_counter()
    expanded_nodes = 0

    # Quick check for invalid inputs
    if not grid.in_bounds(start.x, start.y) or not grid.in_bounds(goal.x, goal.y):
        execution_time = (time.perf_counter() - start_time) * 1000.0
        return PathResult(found=False, path=[], cost=0.0, expanded_nodes=0, execution_time_ms=execution_time)

    if start == goal:
        execution_time = (time.perf_counter() - start_time) * 1000.0
        return PathResult(found=True, path=[], cost=0.0, expanded_nodes=0, execution_time_ms=execution_time)

    # Queue stores PathNode
    queue: deque[PathNode] = deque([PathNode(position=start)])
    visited: set[tuple[int, int]] = { (start.x, start.y) }

    found = False
    goal_node = None

    while queue:
        curr_node = queue.popleft()
        expanded_nodes += 1

        curr_pos = curr_node.position
        if curr_pos == goal:
            found = True
            goal_node = curr_node
            break

        # Expand neighbors (UP, RIGHT, DOWN, LEFT)
        neighbors = grid.get_neighbors(curr_pos.x, curr_pos.y)
        for n in neighbors:
            if (n.x, n.y) not in visited and grid.is_walkable(n.x, n.y):
                visited.add((n.x, n.y))
                # Uniform cost = 1.0 per step
                queue.append(PathNode(position=n, cost=curr_node.cost + 1.0, parent=curr_node))

    execution_time = (time.perf_counter() - start_time) * 1000.0

    if found and goal_node is not None:
        path = reconstruct_path(goal_node)
        return PathResult(
            found=True,
            path=path,
            cost=goal_node.cost,
            expanded_nodes=expanded_nodes,
            execution_time_ms=execution_time
        )

    return PathResult(
        found=False,
        path=[],
        cost=0.0,
        expanded_nodes=expanded_nodes,
        execution_time_ms=execution_time
    )
