"""
app/ai/greedy.py

Greedy Best-First Search pathfinding algorithm.
Prioritizes nodes based solely on the Manhattan distance heuristic to the goal.
"""

import heapq
import time
from app.core.state import Position, PathResult
from app.map.grid import Grid
from app.ai._shared import PathNode, reconstruct_path, manhattan_distance


def find_path(
    grid: Grid,
    start: Position,
    goal: Position,
    heatmap: list[list[float]] = None
) -> PathResult:
    """
    Search for a path from start to goal using Greedy Best-First Search.
    Priority is determined by Manhattan distance heuristic.

    Args:
        grid: The grid map.
        start: Starting Position.
        goal: Target Position.
        heatmap: Ignored in Greedy Search.

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

    # Priority queue stores (heuristic, counter, PathNode)
    heap: list[tuple[int, int, PathNode]] = []
    counter = 0

    start_node = PathNode(position=start, cost=0.0)
    heapq.heappush(heap, (manhattan_distance(start, goal), counter, start_node))
    counter += 1

    visited: set[tuple[int, int]] = set()
    found = False
    goal_node = None

    while heap:
        _, _, curr_node = heapq.heappop(heap)
        curr_pos = curr_node.position

        if curr_pos == goal:
            found = True
            goal_node = curr_node
            break

        if (curr_pos.x, curr_pos.y) in visited:
            continue
        visited.add((curr_pos.x, curr_pos.y))
        expanded_nodes += 1

        # Expand neighbors (UP, RIGHT, DOWN, LEFT)
        neighbors = grid.get_neighbors(curr_pos.x, curr_pos.y)
        for n in neighbors:
            if (n.x, n.y) not in visited and grid.is_walkable(n.x, n.y):
                h_cost = manhattan_distance(n, goal)
                next_node = PathNode(position=n, cost=curr_node.cost + 1.0, parent=curr_node)
                heapq.heappush(heap, (h_cost, counter, next_node))
                counter += 1

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
