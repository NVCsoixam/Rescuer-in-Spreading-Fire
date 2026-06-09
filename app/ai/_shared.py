"""
app/ai/_shared.py

Shared search utilities and node definitions for AI pathfinding algorithms.
"""

from dataclasses import dataclass
from app.core.state import Position


@dataclass
class PathNode:
    """Search tree node representation used during pathfinding traversal."""
    position: Position
    cost: float = 0.0
    parent: "PathNode | None" = None

    def __lt__(self, other: "PathNode") -> bool:
        """Comparison operator based on path cost for priority queues."""
        return self.cost < other.cost


def manhattan_distance(p1: Position, p2: Position) -> int:
    """
    Calculate the Manhattan distance between two coordinates.

    Args:
        p1: First Position.
        p2: Second Position.

    Returns:
        int: The L1 Manhattan distance.
    """
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def reconstruct_path(node: PathNode) -> list[Position]:
    """
    Reconstruct the path of positions from the goal node back to start.

    Args:
        node: The final search node.

    Returns:
        list[Position]: The reconstructed path from start to goal (excluding start).
    """
    path = []
    curr = node
    while curr is not None:
        path.append(curr.position)
        curr = curr.parent
    path.reverse()
    # Exclude start position from the path segment
    if path:
        path.pop(0)
    return path
