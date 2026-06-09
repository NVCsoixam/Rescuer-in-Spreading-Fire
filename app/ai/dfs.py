"""
app/ai/dfs.py

Depth-First Search (DFS) pathfinding algorithm.
Returns a path using stack-based depth-first traversal with search depth limits.
"""

import time
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
    Search for a path from start to goal using Depth-First Search (DFS).
    Uses an iterative stack implementation to prevent recursion overflows.

    Args:
        grid: The grid map.
        start: Starting Position.
        goal: Target Position.
        heatmap: Ignored in DFS (uniform cost).

    Returns:
        PathResult: Search outcome containing paths, cost, and diagnostics.
    """
    start_time = time.perf_counter()
    expanded_nodes = 0
    max_depth = grid.width * grid.height

    # Quick check for invalid inputs
    if not grid.in_bounds(start.x, start.y) or not grid.in_bounds(goal.x, goal.y):
        execution_time = (time.perf_counter() - start_time) * 1000.0
        return PathResult(found=False, path=[], cost=0.0, expanded_nodes=0, execution_time_ms=execution_time)

    if start == goal:
        execution_time = (time.perf_counter() - start_time) * 1000.0
        return PathResult(found=True, path=[], cost=0.0, expanded_nodes=0, execution_time_ms=execution_time)

    # Stack stores (PathNode, current_depth)
    stack: list[tuple[PathNode, int]] = [(PathNode(position=start), 0)]
    visited: set[tuple[int, int]] = set()

    found = False
    goal_node = None

    while stack:
        curr_node, depth = stack.pop()
        curr_pos = curr_node.position

        if curr_pos == goal:
            found = True
            goal_node = curr_node
            break

        if (curr_pos.x, curr_pos.y) in visited:
            continue

        visited.add((curr_pos.x, curr_pos.y))
        expanded_nodes += 1

        if depth >= max_depth:
            continue

        # Get neighbors (UP, RIGHT, DOWN, LEFT)
        neighbors = grid.get_neighbors(curr_pos.x, curr_pos.y)
        # Reverse neighbor push order to maintain deterministic pop priority (UP first, then RIGHT, DOWN, LEFT)
        for n in reversed(neighbors):
            if (n.x, n.y) not in visited and grid.is_walkable(n.x, n.y):
                # Uniform cost = 1.0 per step
                stack.append((PathNode(position=n, cost=curr_node.cost + 1.0, parent=curr_node), depth + 1))

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
