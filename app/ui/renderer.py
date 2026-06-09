"""
app/ui/renderer.py

Grid Renderer for the 2D Rescue Simulation System.
Renders cells, entities, risk overlays, and planned path dots onto the Pygame screen.
"""

import pygame
from app.config import CellType, RobotState, VictimState
from app.core.state import GameState, Position


# Color palette definitions (harmoneous and premium aesthetics)
COLOR_WALL = (45, 45, 48)          # Dark gray/charcoal
COLOR_EMPTY = (245, 245, 245)      # Light gray/off-white background
COLOR_RESCUE = (46, 139, 87)       # Sea green
COLOR_ROBOT = (30, 144, 255)       # Dodger blue
COLOR_ROBOT_DEAD = (128, 128, 128) # Neutral gray
COLOR_VICTIM = (255, 193, 7)       # Amber gold
COLOR_VICTIM_DEAD = (40, 40, 40)   # Dark gray
COLOR_FIRE = (231, 76, 60)         # Crimson red
COLOR_PATH = (0, 206, 209)         # Dark turquoise
COLOR_GRID_LINE = (220, 220, 220)  # Subtle grid line divisor

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

    def draw(
        self,
        surface: pygame.Surface,
        state: GameState,
        planned_path: list[Position],
        show_path: bool = True,
        show_risk: bool = True
    ) -> None:
        """
        Render the grid, entities, and overlays onto the surface.

        Args:
            surface: The Pygame screen surface.
            state: The current GameState.
            planned_path: The list of positions in the robot's current route.
            show_path: Whether to draw planned path dots.
            show_risk: Whether to overlay heatmap risk colors.
        """
        grid_w = state.width
        grid_h = state.height

        if grid_w == 0 or grid_h == 0:
            return

        # Calculate centered responsive cell sizes
        cell_size = min(self.width_px / grid_w, self.height_px / grid_h)
        offset_x = (self.width_px - (grid_w * cell_size)) / 2
        offset_y = (self.height_px - (grid_h * cell_size)) / 2

        # 1. Draw Cell Backgrounds (Walls, empty space, rescue stations)
        for y in range(grid_h):
            for x in range(grid_w):
                cell = state.grid[y][x]
                rect = pygame.Rect(
                    offset_x + x * cell_size,
                    offset_y + y * cell_size,
                    cell_size,
                    cell_size
                )

                # Determine base cell color
                if cell.cell_type == CellType.WALL:
                    color = COLOR_WALL
                elif cell.cell_type == CellType.RESCUE:
                    color = COLOR_RESCUE
                else:
                    color = COLOR_EMPTY

                pygame.draw.rect(surface, color, rect)
                # Thin divider grid lines
                pygame.draw.rect(surface, COLOR_GRID_LINE, rect, 1)

        # 2. Draw Heatmap Risk Overlay
        if show_risk:
            for y in range(grid_h):
                for x in range(grid_w):
                    cell = state.grid[y][x]
                    # If cell is wall, skip risk overlay
                    if cell.cell_type == CellType.WALL:
                        continue

                    # Risk Alpha transparent overlay
                    if cell.risk > 0.0:
                        rect = pygame.Rect(
                            offset_x + x * cell_size,
                            offset_y + y * cell_size,
                            cell_size,
                            cell_size
                        )
                        # Determine overlay color based on threat level
                        if cell.risk >= 1.0:
                            overlay_color = (COLOR_FIRE[0], COLOR_FIRE[1], COLOR_FIRE[2], 180)
                        elif cell.risk >= 0.9:
                            overlay_color = (255, 69, 0, 140)    # Red-orange
                        elif cell.risk >= 0.7:
                            overlay_color = (255, 140, 0, 100)   # Dark orange
                        elif cell.risk >= 0.5:
                            overlay_color = (255, 165, 0, 75)    # Orange
                        else:  # >= 0.3 warning
                            overlay_color = (255, 200, 0, 50)    # Light yellow-orange

                        # Create temporary surface for transparent alpha overlays
                        temp_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                        temp_surface.fill(overlay_color)
                        surface.blit(temp_surface, (rect.x, rect.y))

        # 3. Draw Path Overlay (Cyan dots)
        if show_path and planned_path:
            for pos in planned_path:
                cx = offset_x + pos.x * cell_size + cell_size / 2
                cy = offset_y + pos.y * cell_size + cell_size / 2
                pygame.draw.circle(surface, COLOR_PATH, (int(cx), int(cy)), max(2, int(cell_size * 0.15)))

        # 4. Draw Fire Cell indicators
        for fc in state.fire_cells:
            fx, fy = fc.position.x, fc.position.y
            rect = pygame.Rect(
                offset_x + fx * cell_size + 2,
                offset_y + fy * cell_size + 2,
                cell_size - 4,
                cell_size - 4
            )
            # Draw fire as a glowing concentric circle/box
            pygame.draw.rect(surface, COLOR_FIRE, rect, border_radius=4)
            # Innermost core
            pygame.draw.circle(surface, (255, 235, 59), rect.center, max(2, int(cell_size * 0.18)))

        # 5. Draw Victims
        for v in state.victims:
            # Only render victims who are not currently carried or rescued off grid
            if v.state in (VictimState.WAITING, VictimState.DEAD):
                vx, vy = v.x, v.y
                cx = offset_x + vx * cell_size + cell_size / 2
                cy = offset_y + vy * cell_size + cell_size / 2
                radius = int(cell_size * 0.35)

                color = COLOR_VICTIM if v.alive else COLOR_VICTIM_DEAD
                pygame.draw.circle(surface, color, (int(cx), int(cy)), radius)
                # Draw black borders
                pygame.draw.circle(surface, (0, 0, 0), (int(cx), int(cy)), radius, 2)

                # If dead, draw cross indicator
                if not v.alive:
                    pygame.draw.line(surface, (255, 0, 0), (cx - 5, cy - 5), (cx + 5, cy + 5), 2)
                    pygame.draw.line(surface, (255, 0, 0), (cx + 5, cy - 5), (cx - 5, cy + 5), 2)
                else:
                    # Render ID text inside circle
                    id_txt = FONT_ENTITY.render(f"V{v.victim_id}", True, (0, 0, 0))
                    surface.blit(id_txt, (cx - id_txt.get_width() / 2, cy - id_txt.get_height() / 2))

        # 6. Draw Robot
        robot = state.robot
        rx, ry = robot.x, robot.y
        cx = offset_x + rx * cell_size + cell_size / 2
        cy = offset_y + ry * cell_size + cell_size / 2
        radius = int(cell_size * 0.4)

        color = COLOR_ROBOT if robot.alive else COLOR_ROBOT_DEAD
        pygame.draw.circle(surface, color, (int(cx), int(cy)), radius)
        pygame.draw.circle(surface, (0, 0, 0), (int(cx), int(cy)), radius, 2)

        # Draw inner detail or status text
        if not robot.alive:
            pygame.draw.line(surface, (255, 0, 0), (cx - 6, cy - 6), (cx + 6, cy + 6), 3)
            pygame.draw.line(surface, (255, 0, 0), (cx + 6, cy - 6), (cx - 6, cy + 6), 3)
        else:
            # Show carrying victim indicator
            if robot.carrying_victim:
                pygame.draw.circle(surface, COLOR_VICTIM, (int(cx), int(cy)), int(radius * 0.5))
                pygame.draw.circle(surface, (0, 0, 0), (int(cx), int(cy)), int(radius * 0.5), 1)
                hud_txt = FONT_HUD.render(f"V{robot.carried_victim_id}", True, (0, 0, 0))
                surface.blit(hud_txt, (cx - hud_txt.get_width() / 2, cy - hud_txt.get_height() / 2))
            else:
                # Standard R text (Robot)
                r_txt = FONT_ENTITY.render("R", True, (255, 255, 255))
                surface.blit(r_txt, (cx - r_txt.get_width() / 2, cy - r_txt.get_height() / 2))
