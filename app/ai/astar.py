"""
app/ai/astar.py

A* Search pathfinding algorithm.
Implements risk-aware pathfinding using f(n) = g(n) + h(n) + risk(n).
"""

import heapq
import time
from app.config import RISK_WEIGHT
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
    Search for a path from start to goal using A* Search.
    Evaluation function: f(n) = g(n) + h(n) + risk_penalty(n).
    g(n): Path travel cost (1.0 per step).
    h(n): Manhattan distance heuristic.
    risk_penalty(n): Heat map penalty (cell risk * RISK_WEIGHT).

    Args:
        grid: The grid map.
        start: Starting Position.
        goal: Target Position.
        heatmap: The 2D matrix of risk values.

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

    # Priority queue stores (f_score, counter, PathNode)
    heap: list[tuple[float, int, PathNode]] = []
    counter = 0

    start_node = PathNode(position=start, cost=0.0)
    # Start node f_score is just the heuristic to goal
    start_f = manhattan_distance(start, goal)
    heapq.heappush(heap, (start_f, counter, start_node))
    counter += 1

    # Keep track of minimum path travel cost g(n)
    min_g: dict[tuple[int, int], float] = { (start.x, start.y): 0.0 }
    visited: set[tuple[int, int]] = set()

    found = False
    goal_node = None

    while heap:
        curr_f, _, curr_node = heapq.heappop(heap)
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
            if grid.is_walkable(n.x, n.y):
                # g(n): base cost is 1.0 per step
                new_g = min_g[(curr_pos.x, curr_pos.y)] + 1.0

                if (n.x, n.y) not in min_g or new_g < min_g[(n.x, n.y)]:
                    min_g[(n.x, n.y)] = new_g

                    # Calculate f(n) = g(n) + h(n) + risk_penalty(n)
                    h_val = manhattan_distance(n, goal)
                    risk_val = 0.0
                    if heatmap is not None and len(heatmap) > n.y and len(heatmap[0]) > n.x:
                        risk_val = heatmap[n.y][n.x]

                    risk_penalty = risk_val * RISK_WEIGHT
                    f_val = new_g + h_val + risk_penalty

                    next_node = PathNode(position=n, cost=new_g, parent=curr_node)
                    heapq.heappush(heap, (f_val, counter, next_node))
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
