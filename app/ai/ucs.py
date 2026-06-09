"""
app/ai/ucs.py

Uniform Cost Search (UCS) pathfinding algorithm.
Finds the optimal path based on step cost, taking cell risk penalty weights into account.
"""

import heapq
import time
from app.config import RISK_WEIGHT
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
    Search for a path from start to goal using Uniform Cost Search (UCS).
    Step cost is determined by: 1.0 + risk * RISK_WEIGHT.

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

    # Priority queue stores (cost, counter, PathNode)
    # Counter resolves tie breaks when costs are identical
    heap: list[tuple[float, int, PathNode]] = []
    counter = 0

    start_node = PathNode(position=start, cost=0.0)
    heapq.heappush(heap, (0.0, counter, start_node))
    counter += 1

    # Keep track of the minimum cost to arrive at each node
    min_cost: dict[tuple[int, int], float] = { (start.x, start.y): 0.0 }
    visited: set[tuple[int, int]] = set()

    found = False
    goal_node = None

    while heap:
        curr_cost, _, curr_node = heapq.heappop(heap)
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
                # Calculate movement cost to neighbor cell n
                risk = 0.0
                if heatmap is not None and len(heatmap) > n.y and len(heatmap[0]) > n.x:
                    risk = heatmap[n.y][n.x]

                # Step cost: base cost of 1.0 + risk * weight
                step_cost = 1.0 + risk * RISK_WEIGHT
                next_cost = curr_cost + step_cost

                # If we found a cheaper route to the neighbor, push it
                if (n.x, n.y) not in min_cost or next_cost < min_cost[(n.x, n.y)]:
                    min_cost[(n.x, n.y)] = next_cost
                    next_node = PathNode(position=n, cost=next_cost, parent=curr_node)
                    heapq.heappush(heap, (next_cost, counter, next_node))
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
