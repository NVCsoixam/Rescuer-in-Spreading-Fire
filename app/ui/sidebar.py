"""
app/ui/sidebar.py

Sidebar Controller and UI Panel for the 2D Rescue Simulation System.
Renders control buttons, settings, and live status dashboard.
"""

import pygame
from app.config import SimulationState, EditTool, EnvironmentType, Complexity
from app.core.state import GameState


# Colors matching design standards
COLOR_SIDEBAR_BG = (30, 30, 35)        # Dark charcoal/slate
COLOR_SECTION_HEADER = (150, 150, 160) # Muted gray-blue
COLOR_LABEL = (200, 200, 210)          # Soft light gray
COLOR_BTN_BG = (50, 50, 60)            # Muted navy/gray button background
COLOR_BTN_HOVER = (70, 70, 85)         # Lighter button hover state
COLOR_BTN_ACTIVE = (30, 144, 255)      # Dodger blue highlight
COLOR_BTN_TEXT = (255, 255, 255)       # White text
COLOR_BORDER = (70, 70, 75)            # Subtle section divider borders

# Result Banner Colors
COLOR_COMPLETE = (46, 139, 87)         # Green for success
COLOR_FAILED = (190, 40, 40)           # Deep red for failure

# Safe Font Loader
pygame.font.init()
font_name = pygame.font.match_font('arial')
if font_name:
    FONT_TITLE = pygame.font.Font(font_name, 14)
    FONT_TEXT = pygame.font.Font(font_name, 12)
    FONT_BOLD = pygame.font.Font(font_name, 12)
else:
    FONT_TITLE = pygame.font.SysFont(None, 14)
    FONT_TEXT = pygame.font.SysFont(None, 12)
    FONT_BOLD = pygame.font.SysFont(None, 12)


class Sidebar:
    """Renders the dashboard controls panel and registers button bounds for click mapping."""

    def __init__(self, start_x: int, width: int, height: int) -> None:
        """
        Initialize the Sidebar Panel.

        Args:
            start_x: The starting X pixel coordinate of the sidebar (e.g. 960).
            width: Width of the sidebar area in pixels (e.g. 240).
            height: Height of the sidebar area in pixels (e.g. 800).
        """
        self.start_x = start_x
        self.width = width
        self.height = height

        # Bounding box coordinates for buttons, updated during render pass
        self.buttons: dict[str, pygame.Rect] = {}

    def draw(
        self,
        surface: pygame.Surface,
        state: GameState,
        active_tool: EditTool,
        selected_speed_name: str,
        selected_env_type: EnvironmentType,
        selected_complexity: Complexity
    ) -> None:
        """
        Render the sidebar and its sections onto the Pygame window.

        Args:
            surface: The main window surface.
            state: The GameState object.
            active_tool: Currently selected map editor tool.
            selected_speed_name: Selected fire preset speed label.
            selected_env_type: Selected map environment generation style.
            selected_complexity: Selected map generator complexity setting.
        """
        # 1. Draw Sidebar Background
        sidebar_rect = pygame.Rect(self.start_x, 0, self.width, self.height)
        pygame.draw.rect(surface, COLOR_SIDEBAR_BG, sidebar_rect)
        pygame.draw.line(surface, COLOR_BORDER, (self.start_x, 0), (self.start_x, self.height), 2)

        # Clear active button bounding boxes
        self.buttons.clear()

        # Local offsets
        x_left = self.start_x + 15
        x_right = self.start_x + 125
        w_btn_half = 100
        w_btn_full = 210

        # y positions tracker
        y = 15

        # ==========================================
        # SECTION: LIVE STATUS
        # ==========================================
        y = self._draw_header(surface, "SIMULATION STATUS", y)

        mode_str = state.current_mode.value
        self._draw_status_item(surface, "State Mode:", mode_str, y, is_bold=True)
        y += 18
        self._draw_status_item(surface, "Saved Victims:", f"{state.saved_count} / {len(state.victims)}", y)
        y += 18
        self._draw_status_item(surface, "Deceased:", f"{state.dead_count}", y)
        y += 18
        self._draw_status_item(surface, "Steps Taken:", f"{state.stats.total_steps}", y)
        y += 18
        self._draw_status_item(surface, "Replans:", f"{state.stats.replans}", y)
        y += 18
        self._draw_status_item(surface, "Time Elapsed:", f"{state.simulation_time:.1f} s", y)
        y += 18
        carrying_str = f"Victim #{state.robot.carried_victim_id}" if state.robot.carrying_victim else "None"
        self._draw_status_item(surface, "Carrying:", carrying_str, y)
        y += 25

        # ==========================================
        # SECTION: MAP SETTINGS
        # ==========================================
        y = self._draw_header(surface, "MAP CONFIGURATION", y)

        # Grid size static label
        size_lbl = FONT_TEXT.render("Grid Size: 30x25 (Fixed)", True, COLOR_LABEL)
        surface.blit(size_lbl, (x_left, y))
        y += 25

        # Fire speed preset adjustment
        speed_lbl = FONT_TEXT.render(f"Fire speed: {selected_speed_name}", True, COLOR_LABEL)
        surface.blit(speed_lbl, (x_left, y))
        btn_sp_prev = self._draw_button(surface, "<", x_left + 150, y - 2, 22, 18, is_active=False)
        btn_sp_next = self._draw_button(surface, ">", x_left + 180, y - 2, 22, 18, is_active=False)
        self.buttons["speed_prev"] = btn_sp_prev
        self.buttons["speed_next"] = btn_sp_next
        y += 25

        # Environmental type generator settings
        env_lbl = FONT_TEXT.render(f"Env: {selected_env_type.value}", True, COLOR_LABEL)
        surface.blit(env_lbl, (x_left, y))
        btn_env_prev = self._draw_button(surface, "<", x_left + 150, y - 2, 22, 18, is_active=False)
        btn_env_next = self._draw_button(surface, ">", x_left + 180, y - 2, 22, 18, is_active=False)
        self.buttons["env_prev"] = btn_env_prev
        self.buttons["env_next"] = btn_env_next
        y += 25

        # Generator complexity options
        comp_lbl = FONT_TEXT.render(f"Complexity: {selected_complexity.value}", True, COLOR_LABEL)
        surface.blit(comp_lbl, (x_left, y))
        btn_comp_prev = self._draw_button(surface, "<", x_left + 150, y - 2, 22, 18, is_active=False)
        btn_comp_next = self._draw_button(surface, ">", x_left + 180, y - 2, 22, 18, is_active=False)
        self.buttons["comp_prev"] = btn_comp_prev
        self.buttons["comp_next"] = btn_comp_next
        y += 25

        # Generate Map Button
        btn_gen = self._draw_button(surface, "GENERATE RANDOM MAP", x_left, y, w_btn_full, 26, is_active=False)
        self.buttons["generate_map"] = btn_gen
        y += 38

        # ==========================================
        # SECTION: EDITOR TOOLS
        # ==========================================
        y = self._draw_header(surface, "EDITOR MODE TOOLS", y)

        tool_btns = [
            ("Wall", EditTool.WALL, x_left, y),
            ("Robot", EditTool.ROBOT, x_right, y),
            ("Victim", EditTool.VICTIM, x_left, y + 25),
            ("Fire", EditTool.FIRE, x_right, y + 25),
            ("Rescue", EditTool.RESCUE, x_left, y + 50),
            ("Erase", EditTool.ERASE, x_right, y + 50),
        ]

        for name, tool, bx, by in tool_btns:
            btn_rect = self._draw_button(surface, name, bx, by, w_btn_half, 20, is_active=(active_tool == tool))
            self.buttons[f"tool_{tool.value}"] = btn_rect

        y += 80

        # ==========================================
        # SECTION: RUN ALGORITHM
        # ==========================================
        y = self._draw_header(surface, "RUN ALGORITHM MODE", y)

        alg_btns = [
            ("MANUAL CONTROL", SimulationState.USER_MODE, x_left, y, w_btn_full),
            ("BFS", SimulationState.BFS, x_left, y + 28, w_btn_half),
            ("A* SEARCH", SimulationState.ASTAR, x_right, y + 28, w_btn_half),
            ("DFS", SimulationState.DFS, x_left, y + 53, w_btn_half),
            ("UCS (Risk Cost)", SimulationState.UCS, x_right, y + 53, w_btn_half),
            ("DIJKSTRA", SimulationState.DIJKSTRA, x_left, y + 78, w_btn_half),
            ("GREEDY SEARCH", SimulationState.GREEDY, x_right, y + 78, w_btn_half),
        ]

        for name, mode, bx, by, bw in alg_btns:
            # Highlight button if currently executing that search algorithm
            active = (state.current_mode == mode)
            # Or if paused and prev mode was this algorithm
            if state.current_mode == SimulationState.PAUSED:
                # Retrieve active indicator from caller's engine memory if necessary,
                # but matching current algorithm name is standard.
                active = (state.selected_algorithm == mode.name)

            btn_rect = self._draw_button(surface, name, bx, by, bw, 22, is_active=active)
            self.buttons[f"run_{mode.value}"] = btn_rect

        y += 112

        # ==========================================
        # SECTION: CONTROLS
        # ==========================================
        y = self._draw_header(surface, "EXECUTION CONTROLS", y)

        pause_lbl = "RESUME" if state.current_mode == SimulationState.PAUSED else "PAUSE"
        btn_pause = self._draw_button(
            surface,
            pause_lbl,
            x_left,
            y,
            w_btn_half,
            28,
            is_active=(state.current_mode == SimulationState.PAUSED)
        )
        btn_reset = self._draw_button(surface, "RESET", x_right, y, w_btn_half, 28, is_active=False)

        self.buttons["control_pause"] = btn_pause
        self.buttons["control_reset"] = btn_reset
        y += 40

        # ==========================================
        # RESULT BANNER
        # ==========================================
        if state.current_mode == SimulationState.MISSION_COMPLETE:
            self._draw_result_banner(surface, "MISSION COMPLETE", COLOR_COMPLETE, y)
        elif state.current_mode == SimulationState.MISSION_FAILED:
            self._draw_result_banner(surface, "MISSION FAILED", COLOR_FAILED, y)

    def _draw_header(self, surface: pygame.Surface, text: str, y: int) -> int:
        """Render a capitalized section header with a line divisor below it."""
        hdr = FONT_TITLE.render(text, True, COLOR_SECTION_HEADER)
        surface.blit(hdr, (self.start_x + 15, y))
        pygame.draw.line(
            surface,
            COLOR_BORDER,
            (self.start_x + 15, y + 18),
            (self.start_x + self.width - 15, y + 18),
            1
        )
        return y + 26

    def _draw_status_item(self, surface: pygame.Surface, label: str, val: str, y: int, is_bold: bool = False) -> None:
        """Render a single key-value live statistic item."""
        lbl_render = FONT_TEXT.render(label, True, COLOR_LABEL)
        surface.blit(lbl_render, (self.start_x + 15, y))

        font = FONT_BOLD if is_bold else FONT_TEXT
        color = COLOR_BTN_ACTIVE if is_bold else (255, 255, 255)
        val_render = font.render(val, True, color)
        surface.blit(val_render, (self.start_x + 120, y))

    def _draw_button(self, surface: pygame.Surface, text: str, x: int, y: int, w: int, h: int, is_active: bool) -> pygame.Rect:
        """Helper to draw professional highlighted button shapes with hover visual response."""
        rect = pygame.Rect(x, y, w, h)
        
        # Get mouse position and check collision for hover state
        mx, my = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint((mx, my))

        if is_active:
            bg_color = COLOR_BTN_ACTIVE
        elif is_hovered:
            bg_color = COLOR_BTN_HOVER
        else:
            bg_color = COLOR_BTN_BG

        pygame.draw.rect(surface, bg_color, rect, border_radius=3)
        # Outline border
        pygame.draw.rect(surface, COLOR_BORDER, rect, 1, border_radius=3)

        txt_render = FONT_TEXT.render(text, True, COLOR_BTN_TEXT)
        tx = x + (w - txt_render.get_width()) / 2
        ty = y + (h - txt_render.get_height()) / 2
        surface.blit(txt_render, (tx, ty))

        return rect

    def _draw_result_banner(self, surface: pygame.Surface, text: str, color: tuple[int, int, int], y: int) -> None:
        """Draw final mission outcome banner at the bottom of the sidebar."""
        rect = pygame.Rect(self.start_x + 15, y + 10, self.width - 30, 40)
        pygame.draw.rect(surface, color, rect, border_radius=4)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1, border_radius=4)

        txt_render = FONT_TITLE.render(text, True, (255, 255, 255))
        tx = rect.x + (rect.width - txt_render.get_width()) / 2
        ty = rect.y + (rect.height - txt_render.get_height()) / 2
        surface.blit(txt_render, (tx, ty))
