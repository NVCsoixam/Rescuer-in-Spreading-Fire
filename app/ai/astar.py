"""
app/ai/astar.py

A* Search pathfinding algorithm.
Implements risk-aware optimal pathfinding using f(n) = g(n) + h(n) + risk_penalty(n).
"""

from __future__ import annotations
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
    heatmap: list[list[float]] | None = None,
) -> PathResult:
    """
    Search for a path from start to goal using A* Search.
    Evaluation function: f(n) = g(n) + h(n) + risk_penalty(n).

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

    # Priority queue: (f_score, counter, PathNode)
    heap: list[tuple[float, int, PathNode]] = []
    counter = 0

    start_node = PathNode(position=start, cost=0.0)
    start_f = float(manhattan_distance(start, goal))
    heapq.heappush(heap, (start_f, counter, start_node))
    counter += 1

    # Track best g(n) for each visited position
    g_score: dict[tuple[int, int], float] = {(start.x, start.y): 0.0}
    visited: set[tuple[int, int]] = set()

    found = False
    goal_node: PathNode | None = None

    while heap:
        curr_f, _, curr_node = heapq.heappop(heap)
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
            # g(n): base cost is 1.0 per step
            new_g = g_score[pos_key] + 1.0

            if n_key not in g_score or new_g < g_score[n_key]:
                g_score[n_key] = new_g

                # f(n) = g(n) + h(n) + risk_penalty(n)
                h_val = manhattan_distance(n, goal)
                risk_val = 0.0
                if heatmap is not None and 0 <= n.y < len(heatmap) and 0 <= n.x < len(heatmap[0]):
                    risk_val = heatmap[n.y][n.x]

                risk_penalty = risk_val * RISK_WEIGHT
                f_val = new_g + float(h_val) + risk_penalty

                next_node = PathNode(position=n, cost=new_g, parent=curr_node)
                heapq.heappush(heap, (f_val, counter, next_node))
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