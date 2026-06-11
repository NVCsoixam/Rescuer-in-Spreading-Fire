"""
app/ui/renderer.py

Grid Renderer for the 2D Rescue Simulation System.
Renders cells, entities, and planned path dots onto the Pygame screen.
"""

from __future__ import annotations
import pygame
from app.config import CellType, RobotState, VictimState
from app.core.state import GameState, Position


# Color palette definitions (premium aesthetics)
COLOR_WALL = (40, 42, 46)  # Dark graphite
COLOR_EXIT_WALL = (100, 70, 40)  # Brown/bronze brick for exit walls
COLOR_ROOM = (236, 240, 245)  # Light room tone
COLOR_CORRIDOR = (217, 223, 230)  # Subtle corridor shade
COLOR_EMPTY = (248, 249, 251)  # Soft off-white floor
COLOR_RESCUE = (46, 139, 87)  # Sea green
COLOR_RESCUE_LIGHT = (60, 179, 113)  # Medium sea green (hover)
COLOR_ROBOT = (30, 144, 255)  # Dodger blue
COLOR_ROBOT_DEAD = (128, 128, 128)  # Neutral gray
COLOR_VICTIM = (255, 193, 7)  # Amber gold
COLOR_VICTIM_DEAD = (60, 60, 60)  # Dark slate
COLOR_FIRE = (231, 76, 60)  # Crimson red
COLOR_FIRE_YELLOW = (255, 200, 50)  # Fire highlight
COLOR_PATH = (0, 206, 209)  # Dark turquoise
COLOR_GRID_LINE = (200, 205, 210)  # Subtle grid divider
COLOR_BG_DARK = (18, 22, 30)
COLOR_BG_LIGHT = (22, 26, 34)

# Safe Font Loader
pygame.font.init()
font_name = pygame.font.match_font('arial')
if font_name:
    FONT_ENTITY = pygame.font.Font(font_name, 12)
    FONT_HUD = pygame.font.Font(font_name, 10)
else:
    FONT_ENTITY = pygame.font.SysFont(None, 12)
    FONT_HUD = pygame.font.SysFont(None, 10)


class GridRenderer:
    """Handles rendering of the simulation viewport containing grid cells and path overlays."""

    def __init__(self, width_px: int, height_px: int) -> None:
        """
        Initialize the GridRenderer.

        Args:
            width_px: Width of the grid area in pixels (e.g. 960).
            height_px: Height of the grid area in pixels (e.g. 800).
        """
        self.width_px = width_px
        self.height_px = height_px
        self._cell_size: float = 0.0
        self._offset_x: float = 0.0
        self._offset_y: float = 0.0

    def _update_layout(self, grid_w: int, grid_h: int) -> None:
        """Recalculate cell size and offset for the current grid dimensions."""
        if grid_w > 0 and grid_h > 0:
            self._cell_size = min(self.width_px / grid_w, self.height_px / grid_h)
            self._offset_x = (self.width_px - (grid_w * self._cell_size)) / 2
            self._offset_y = (self.height_px - (grid_h * self._cell_size)) / 2

    def draw(
        self,
        surface: pygame.Surface,
        state: GameState,
        planned_path: list[Position],
    ) -> None:
        """
        Render the grid, entities, and path overlays onto the surface.

        Args:
            surface: The Pygame screen surface.
            state: The current GameState.
            planned_path: The list of positions in the robot's current route.
        """
        grid_w = state.width
        grid_h = state.height

        if grid_w == 0 or grid_h == 0:
            return

        self._update_layout(grid_w, grid_h)
        cs = self._cell_size
        ox = self._offset_x
        oy = self._offset_y

        # Background
        pygame.draw.rect(surface, COLOR_BG_DARK, (0, 0, self.width_px, self.height_px))
        pygame.draw.rect(
            surface, COLOR_BG_LIGHT,
            (0, self.height_px // 2, self.width_px, self.height_px // 2)
        )

        # 1. Draw Cell Backgrounds
        for y in range(grid_h):
            for x in range(grid_w):
                cell = state.grid[y][x]
                rect = pygame.Rect(
                    int(ox + x * cs), int(oy + y * cs),
                    int(cs), int(cs)
                )

                # Determine base cell color
                color = self._get_cell_color(cell, x, y, grid_w, grid_h, state.grid)
                pygame.draw.rect(surface, color, rect)
                # Thin grid line
                pygame.draw.rect(surface, COLOR_GRID_LINE, rect, 1)

        # 2. Draw Path Overlay (Cyan dots) - always shown
        if planned_path:
            for pos in planned_path:
                cx = ox + pos.x * cs + cs / 2
                cy = oy + pos.y * cs + cs / 2
                pygame.draw.circle(
                    surface, COLOR_PATH,
                    (int(cx), int(cy)),
                    max(2, int(cs * 0.15))
                )

        # 3. Draw Fire Cells
        for fc in state.fire_cells:
            self._draw_fire_cell(surface, fc, ox, oy, cs)

        # 4. Draw Victims
        for v in state.victims:
            if v.state in (VictimState.WAITING, VictimState.DEAD):
                self._draw_victim(surface, v, ox, oy, cs)

        # 5. Draw Robot
        self._draw_robot(surface, state.robot, ox, oy, cs)

    def _get_cell_color(
        self, cell, x: int, y: int, grid_w: int, grid_h: int,
        grid: list[list] = None
    ) -> tuple[int, int, int]:
        """Determine the base color for a cell."""
        if cell.cell_type == CellType.WALL:
            return COLOR_WALL
        if cell.cell_type == CellType.EXIT_WALL:
            return COLOR_EXIT_WALL
        if cell.cell_type == CellType.RESCUE:
            return COLOR_RESCUE
        if cell.cell_type == CellType.FIRE:
            return (190, 50, 55)

        # Differentiate rooms from corridors using neighbor info
        open_neighbors = 0
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_w and 0 <= ny < grid_h:
                if grid is not None and grid[ny][nx].cell_type not in (CellType.WALL, CellType.EXIT_WALL):
                    open_neighbors += 1
        return COLOR_CORRIDOR if open_neighbors <= 2 else COLOR_ROOM

    def _draw_fire_cell(
        self, surface: pygame.Surface, fc, ox: float, oy: float, cs: float,
    ) -> None:
        """Draw a fire cell with flame effects."""
        fx, fy = fc.position.x, fc.position.y
        rect = pygame.Rect(
            int(ox + fx * cs + 2),
            int(oy + fy * cs + 2),
            int(cs - 4),
            int(cs - 4),
        )
        pygame.draw.rect(surface, COLOR_FIRE, rect, border_radius=6)

        # Inner flame ellipse
        flame_center = rect.center
        pygame.draw.ellipse(
            surface, (255, 184, 14),
            (
                flame_center[0] - rect.width * 0.25,
                flame_center[1] - rect.height * 0.35,
                rect.width * 0.5,
                rect.height * 0.7,
            ),
        )
        # Bright core
        pygame.draw.circle(
            surface, (255, 242, 0),
            flame_center,
            max(2, int(cs * 0.18)),
        )

    def _draw_victim(
        self, surface: pygame.Surface, v, ox: float, oy: float, cs: float,
    ) -> None:
        """Draw a victim circle with status indicators."""
        vx, vy = v.x, v.y
        cx = ox + vx * cs + cs / 2
        cy = oy + vy * cs + cs / 2
        radius = int(cs * 0.35)

        color = COLOR_VICTIM if v.alive else COLOR_VICTIM_DEAD
        pygame.draw.circle(surface, color, (int(cx), int(cy)), radius)
        pygame.draw.circle(surface, (0, 0, 0), (int(cx), int(cy)), radius, 2)

        if not v.alive:
            # Dead indicator
            pygame.draw.line(surface, (255, 0, 0), (cx - 5, cy - 5), (cx + 5, cy + 5), 2)
            pygame.draw.line(surface, (255, 0, 0), (cx + 5, cy - 5), (cx - 5, cy + 5), 2)
        else:
            # ID text
            id_txt = FONT_ENTITY.render(f"V{v.victim_id}", True, (0, 0, 0))
            surface.blit(id_txt, (cx - id_txt.get_width() / 2, cy - id_txt.get_height() / 2))

    def _draw_robot(
        self, surface: pygame.Surface, robot, ox: float, oy: float, cs: float,
    ) -> None:
        """Draw the robot with carrying status indicator."""
        rx, ry = robot.x, robot.y
        cx = ox + rx * cs + cs / 2
        cy = oy + ry * cs + cs / 2
        radius = int(cs * 0.4)

        color = COLOR_ROBOT if robot.alive else COLOR_ROBOT_DEAD
        pygame.draw.circle(surface, color, (int(cx), int(cy)), radius)
        pygame.draw.circle(surface, (0, 0, 0), (int(cx), int(cy)), radius, 2)

        if not robot.alive:
            # Dead robot cross
            pygame.draw.line(surface, (255, 0, 0), (cx - 6, cy - 6), (cx + 6, cy + 6), 3)
            pygame.draw.line(surface, (255, 0, 0), (cx + 6, cy - 6), (cx - 6, cy + 6), 3)
        elif robot.carrying_victim:
            # Carrying indicator
            inner_radius = int(radius * 0.5)
            pygame.draw.circle(surface, COLOR_VICTIM, (int(cx), int(cy)), inner_radius)
            pygame.draw.circle(surface, (0, 0, 0), (int(cx), int(cy)), inner_radius, 1)
            hud_txt = FONT_HUD.render(
                f"V{robot.carried_victim_id}", True, (0, 0, 0)
            )
            surface.blit(
                hud_txt,
                (cx - hud_txt.get_width() / 2, cy - hud_txt.get_height() / 2),
            )
        else:
            # Standard R label
            r_txt = FONT_ENTITY.render("R", True, (255, 255, 255))
            surface.blit(r_txt, (cx - r_txt.get_width() / 2, cy - r_txt.get_height() / 2))