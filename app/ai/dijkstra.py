"""
app/ai/dijkstra.py

Dijkstra's pathfinding algorithm.
Finds the shortest weighted path on the grid taking cell risk weights into account.
Equivalent to UCS but without heuristic optimization.
"""

from __future__ import annotations
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
    heatmap: list[list[float]] | None = None,
) -> PathResult:
    """
    Search for a path from start to goal using Dijkstra's algorithm.
    Cost is calculated per step: 1.0 + risk * RISK_WEIGHT.

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

    # Quick bounds check
    if not grid.in_bounds(start.x, start.y) or not grid.in_bounds(goal.x, goal.y):
        elapsed = (time.perf_counter() - start_time) * 1000.0
        return PathResult(found=False, path=[], cost=0.0, expanded_nodes=0, execution_time_ms=elapsed)

    if start == goal:
        elapsed = (time.perf_counter() - start_time) * 1000.0
        return PathResult(found=True, path=[], cost=0.0, expanded_nodes=0, execution_time_ms=elapsed)

    # Priority queue: (cost, counter, PathNode)
    heap: list[tuple[float, int, PathNode]] = []
    counter = 0

    start_node = PathNode(position=start, cost=0.0)
    heapq.heappush(heap, (0.0, counter, start_node))
    counter += 1

    # Track minimum cost to each node
    min_cost: dict[tuple[int, int], float] = {(start.x, start.y): 0.0}
    visited: set[tuple[int, int]] = set()

    found = False
    goal_node: PathNode | None = None

    while heap:
        curr_cost, _, curr_node = heapq.heappop(heap)
        curr_pos = curr_node.position
        pos_key = (curr_pos.x, curr_pos.y)

        if curr_pos == goal:
            found = True
            goal_node = curr_node
            break

        if pos_key in visited:
            continue
        visited.add(pos_key)
        expanded_nodes += 1

        # Expand neighbors
        for n in grid.get_neighbors(curr_pos.x, curr_pos.y):
            if not grid.is_walkable(n.x, n.y):
                continue

            n_key = (n.x, n.y)
            # Calculate risk-weighted step cost
            risk = 0.0
            if heatmap is not None and 0 <= n.y < len(heatmap) and 0 <= n.x < len(heatmap[0]):
                risk = heatmap[n.y][n.x]

            step_cost = 1.0 + risk * RISK_WEIGHT
            next_cost = curr_cost + step_cost

            if n_key not in min_cost or next_cost < min_cost[n_key]:
                min_cost[n_key] = next_cost
                next_node = PathNode(position=n, cost=next_cost, parent=curr_node)
                heapq.heappush(heap, (next_cost, counter, next_node))
                counter += 1

    elapsed = (time.perf_counter() - start_time) * 1000.0

    if found and goal_node is not None:
        path = reconstruct_path(goal_node)
        return PathResult(
            found=True,
            path=path,
            cost=goal_node.cost,
            expanded_nodes=expanded_nodes,
            execution_time_ms=elapsed,
        )

    return PathResult(
        found=False,
        path=[],
        cost=0.0,
        expanded_nodes=expanded_nodes,
        execution_time_ms=elapsed,
    )