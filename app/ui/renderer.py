"""
app/ui/renderer.py

Grid Renderer for the 2D Rescue Simulation System.
Renders cells, entities, and planned path dots onto the Pygame screen.
"""

from __future__ import annotations
import math
import pygame
from app.config import CellType, RobotState, VictimState
from app.core.state import GameState, Position


# Color palette definitions (premium aesthetics)
COLOR_WALL = (52, 64, 82)  # Dark slate graphite
COLOR_EXIT_WALL = (160, 100, 50)  # Bronze brick for exit walls
COLOR_ROOM = (28, 33, 46)  # Sleek dark room tone
COLOR_CORRIDOR = (35, 41, 56)  # Deep corridor shade
COLOR_EMPTY = (30, 35, 45)  # Soft dark floor
COLOR_RESCUE = (46, 204, 113)  # Emerald green
COLOR_RESCUE_LIGHT = (82, 222, 151)  # Emerald highlight
COLOR_ROBOT = (0, 150, 255)  # Bright dodger blue
COLOR_ROBOT_DEAD = (120, 130, 140)  # Slate gray
COLOR_VICTIM = (241, 196, 15)  # Amber gold
COLOR_VICTIM_DEAD = (74, 85, 104)  # Muted gray-blue
COLOR_FIRE = (231, 76, 60)  # Crimson red
COLOR_FIRE_YELLOW = (254, 202, 87)  # Flame highlight
COLOR_PATH = (0, 229, 255)  # Cyan route
COLOR_GRID_LINE = (38, 45, 61)  # Dark divider
COLOR_BG_DARK = (15, 17, 22)  # Ultra dark base
COLOR_BG_LIGHT = (21, 24, 30)  # Deep carbon panel

# Safe Font Loader
pygame.font.init()
font_name = pygame.font.match_font('segoeui') or pygame.font.match_font('arial')
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
        """Recalculate cell size and offset for the current grid dimensions, adding margin."""
        padding = 35  # Generous padding to prevent screen overflow
        usable_w = self.width_px - 2 * padding
        usable_h = self.height_px - 2 * padding
        if grid_w > 0 and grid_h > 0:
            self._cell_size = min(usable_w / grid_w, usable_h / grid_h)
            self._offset_x = padding + (usable_w - (grid_w * self._cell_size)) / 2
            self._offset_y = padding + (usable_h - (grid_h * self._cell_size)) / 2

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

        # Draw overall viewport background (sleek dark mode)
        pygame.draw.rect(surface, COLOR_BG_DARK, (0, 0, self.width_px, self.height_px))

        # Draw background panel for the grid area with rounded corners and double border
        panel_rect = pygame.Rect(
            int(ox - 8), int(oy - 8),
            int(grid_w * cs + 16), int(grid_h * cs + 16)
        )
        pygame.draw.rect(surface, COLOR_BG_LIGHT, panel_rect, border_radius=12)
        pygame.draw.rect(surface, (45, 52, 68), panel_rect, 2, border_radius=12)

        # 1. Draw Cell Backgrounds
        gap = 1.0  # Thin modern grid spacing
        for y in range(grid_h):
            for x in range(grid_w):
                cell = state.grid[y][x]
                rect = pygame.Rect(
                    int(ox + x * cs + gap), int(oy + y * cs + gap),
                    int(cs - 2 * gap), int(cs - 2 * gap)
                )

                # Determine base cell color
                color = self._get_cell_color(cell, x, y, grid_w, grid_h, state.grid)
                
                # Render rounded walls and rooms
                cell_radius = 4 if cell.cell_type in (CellType.WALL, CellType.EXIT_WALL, CellType.RESCUE) else 2
                pygame.draw.rect(surface, color, rect, border_radius=cell_radius)

        # 2. Draw Path Overlay as a continuous glowing cyan route line
        if planned_path and len(planned_path) > 0:
            # We construct a points list starting from robot's current position to targets
            path_points = []
            
            # Start position is robot position
            rx_px = ox + state.robot.x * cs + cs / 2
            ry_px = oy + state.robot.y * cs + cs / 2
            path_points.append((int(rx_px), int(ry_px)))
            
            for pos in planned_path:
                cx = ox + pos.x * cs + cs / 2
                cy = oy + pos.y * cs + cs / 2
                path_points.append((int(cx), int(cy)))
                
            if len(path_points) > 1:
                pygame.draw.lines(surface, COLOR_PATH, False, path_points, 3)
                
            # Also draw glowing path node circles
            for pos in planned_path:
                cx = ox + pos.x * cs + cs / 2
                cy = oy + pos.y * cs + cs / 2
                pygame.draw.circle(surface, (0, 180, 200), (int(cx), int(cy)), max(2, int(cs * 0.1)))
                pygame.draw.circle(surface, COLOR_PATH, (int(cx), int(cy)), max(1, int(cs * 0.06)))

        # 3. Draw Fire Cells
        for fc in state.fire_cells:
            self._draw_fire_cell(surface, fc, ox, oy, cs)

        # 4. Draw Victims with pulse breathing animation
        for v in state.victims:
            if v.state in (VictimState.WAITING, VictimState.DEAD):
                self._draw_victim(surface, v, ox, oy, cs, state.fire_cells)

        # 5. Draw Robot with thick white border and visual eyes
        self._draw_robot(surface, state.robot, ox, oy, cs)

    def _get_cell_color(
        self, cell, x: int, y: int, grid_w: int, grid_h: int,
        grid: list[list] = None
    ) -> tuple[int, int, int]:
        """Determine the base color for a cell with dark metal theme."""
        if cell.cell_type == CellType.WALL:
            return COLOR_WALL
        if cell.cell_type == CellType.EXIT_WALL:
            return COLOR_EXIT_WALL
        if cell.cell_type == CellType.RESCUE:
            return COLOR_RESCUE
        if cell.cell_type == CellType.FIRE:
            return (180, 40, 45)

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
        """Draw a fire cell with organic layered flame effects."""
        fx, fy = fc.position.x, fc.position.y
        rect = pygame.Rect(
            int(ox + fx * cs + 1),
            int(oy + fy * cs + 1),
            int(cs - 2),
            int(cs - 2),
        )
        pygame.draw.rect(surface, COLOR_FIRE, rect, border_radius=6)

        # Inner flame layer
        flame_center = rect.center
        pygame.draw.ellipse(
            surface, COLOR_FIRE_YELLOW,
            (
                flame_center[0] - rect.width * 0.25,
                flame_center[1] - rect.height * 0.35,
                rect.width * 0.5,
                rect.height * 0.7,
            ),
        )
        # Bright flame core
        pygame.draw.circle(
            surface, (255, 255, 200),
            flame_center,
            max(2, int(cs * 0.16)),
        )

    def _draw_victim(
        self, surface: pygame.Surface, v, ox: float, oy: float, cs: float, fire_cells: list
    ) -> None:
        """Draw a victim circle with status indicators, heartbeat pulse, and fire danger warning."""
        vx, vy = v.x, v.y
        cx = ox + vx * cs + cs / 2
        cy = oy + vy * cs + cs / 2

        # Alive victim breathing animation (heartbeat/pulse size variation)
        pulse = 0.0
        if v.alive:
            pulse = math.sin(pygame.time.get_ticks() * 0.006) * (cs * 0.05)

        radius = int(cs * 0.35 + pulse)

        # Danger indicator: Calculate Manhattan distance to nearest fire source
        min_fire_dist = 999
        for fc in fire_cells:
            dist = abs(fc.position.x - vx) + abs(fc.position.y - vy)
            if dist < min_fire_dist:
                min_fire_dist = dist

        in_danger = (min_fire_dist <= 3) and v.alive

        # If in high danger, flash a bright red outline around the victim cell
        if in_danger:
            flash = (pygame.time.get_ticks() // 250) % 2 == 0
            if flash:
                pygame.draw.circle(surface, (255, 0, 0), (int(cx), int(cy)), int(radius + 4), 2)

        color = COLOR_VICTIM if v.alive else COLOR_VICTIM_DEAD
        pygame.draw.circle(surface, color, (int(cx), int(cy)), radius)
        
        # Inner boundary border
        pygame.draw.circle(surface, (20, 20, 20), (int(cx), int(cy)), radius, 2)

        if not v.alive:
            # Draw dead visual indicator (X cross)
            pygame.draw.line(surface, (255, 50, 50), (cx - 4, cy - 4), (cx + 4, cy + 4), 2)
            pygame.draw.line(surface, (255, 50, 50), (cx + 4, cy - 4), (cx - 4, cy + 4), 2)
        else:
            # Draw tiny HP/Status bar on top of the cell
            bar_w = int(cs * 0.6)
            bar_h = 3
            bar_x = int(cx - bar_w / 2)
            bar_y = int(cy - radius - 5)
            
            # HP bar background
            pygame.draw.rect(surface, (60, 20, 20), (bar_x, bar_y, bar_w, bar_h))
            # HP bar green portion decreases if fire is closer
            hp_ratio = min(1.0, max(0.0, (min_fire_dist - 1) / 4.0)) # 0% if dist=1, 100% if dist>=5
            fill_color = (255, 50, 50) if in_danger else (46, 204, 113)
            pygame.draw.rect(surface, fill_color, (bar_x, bar_y, int(bar_w * hp_ratio), bar_h))

            # ID text
            id_txt = FONT_ENTITY.render(f"V{v.victim_id}", True, (0, 0, 0))
            surface.blit(id_txt, (cx - id_txt.get_width() / 2, cy - id_txt.get_height() / 2))

    def _draw_robot(
        self, surface: pygame.Surface, robot, ox: float, oy: float, cs: float,
    ) -> None:
        """Draw the robot with sleek modern accents, eyes, and thick border."""
        rx, ry = robot.x, robot.y
        cx = ox + rx * cs + cs / 2
        cy = oy + ry * cs + cs / 2
        radius = int(cs * 0.42)

        color = COLOR_ROBOT if robot.alive else COLOR_ROBOT_DEAD
        
        # Outer ring shadow/glow
        pygame.draw.circle(surface, (255, 255, 255), (int(cx), int(cy)), radius)
        pygame.draw.circle(surface, color, (int(cx), int(cy)), int(radius * 0.9))
        pygame.draw.circle(surface, (0, 0, 0), (int(cx), int(cy)), int(radius * 0.9), 1)

        if not robot.alive:
            # Dead robot cross indicator
            pygame.draw.line(surface, (255, 50, 50), (cx - 6, cy - 6), (cx + 6, cy + 6), 3)
            pygame.draw.line(surface, (255, 50, 50), (cx + 6, cy - 6), (cx - 6, cy + 6), 3)
        elif robot.carrying_victim:
            # Carrying indicator inside robot
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
            # Draw robot face/eyes to look professional
            eye_r = max(1, int(radius * 0.14))
            eye_offset = int(radius * 0.35)
            # White eye plates
            pygame.draw.circle(surface, (255, 255, 255), (int(cx - eye_offset), int(cy - 2)), eye_r)
            pygame.draw.circle(surface, (255, 255, 255), (int(cx + eye_offset), int(cy - 2)), eye_r)
            
            # White center line/mouth decoration
            pygame.draw.line(surface, (255, 255, 255), (int(cx - 3), int(cy + 4)), (int(cx + 3), int(cy + 4)), 1)