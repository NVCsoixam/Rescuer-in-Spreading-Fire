"""
app/ui/sidebar.py

Sidebar Controller and UI Panel for the 2D Rescue Simulation System.
Renders control buttons, settings, and live status dashboard.
"""

import pygame
import time
from app.config import SimulationState, EditTool
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

# Safe Font Loader for Emoji Support
pygame.font.init()
font_names = ['segoeuiemojiregular', 'segoeuiemoji', 'segoeui', 'microsoftjhenghei', 'microsoftyahei', 'arial']
font_path = None
for name in font_names:
    font_path = pygame.font.match_font(name)
    if font_path:
        break

if font_path:
    FONT_TITLE = pygame.font.Font(font_path, 14)
    FONT_TEXT = pygame.font.Font(font_path, 12)
    FONT_BOLD = pygame.font.Font(font_path, 12)
else:
    FONT_TITLE = pygame.font.SysFont("segoeuiemoji", 14)
    FONT_TEXT = pygame.font.SysFont("segoeuiemoji", 12)
    FONT_BOLD = pygame.font.SysFont("segoeuiemoji", 12)


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
        ui_state
    ) -> None:
        """
        Render the sidebar and its sections onto the Pygame window.

        Args:
            surface: The main window surface.
            state: The GameState object.
            ui_state: The UIState wrapper containing settings and layout state.
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
        # SECTION 1: MAP SETTINGS (MAP CONFIGURATION)
        # ==========================================
        y = self._draw_header(surface, "MAP CONFIGURATION", y)

        # Map Size Dropdown trigger
        size_lbl = FONT_TEXT.render("Map Size:", True, COLOR_LABEL)
        surface.blit(size_lbl, (x_left, y))
        
        size_trigger_rect = self._draw_dropdown_trigger(
            surface,
            f"{ui_state.selected_size}x{ui_state.selected_size}  ▼",
            x_left + 85,
            y - 2,
            115,
            20,
            is_open=ui_state.size_dropdown_open
        )
        self.buttons["size_dropdown_trigger"] = size_trigger_rect
        y += 25

        # Fire Interval numeric textbox
        interval_lbl = FONT_TEXT.render("Fire Int (ms):", True, COLOR_LABEL)
        surface.blit(interval_lbl, (x_left, y))

        textbox_rect = pygame.Rect(x_left + 85, y - 2, 115, 20)
        bg_color = (20, 20, 25) if ui_state.fire_interval_focused else (40, 40, 45)
        border_color = COLOR_BTN_ACTIVE if ui_state.fire_interval_focused else COLOR_BORDER
        pygame.draw.rect(surface, bg_color, textbox_rect, border_radius=3)
        pygame.draw.rect(surface, border_color, textbox_rect, 1, border_radius=3)

        txt_str = ui_state.fire_interval_text
        if ui_state.fire_interval_focused:
            cursor = "|" if int(time.time() * 2) % 2 == 0 else ""
            txt_str += cursor
        txt_render = FONT_TEXT.render(txt_str, True, (255, 255, 255))
        surface.blit(txt_render, (textbox_rect.x + 8, textbox_rect.y + (textbox_rect.height - txt_render.get_height()) // 2))
        
        self.buttons["fire_interval_input"] = textbox_rect
        y += 25

        # Generate Map Button
        btn_gen = self._draw_button(surface, "GENERATE RANDOM MAP", x_left, y, w_btn_full, 26, is_active=False)
        self.buttons["generate_map"] = btn_gen
        y += 38

        # ==========================================
        # SECTION 2: EDIT MODE (EDITOR TOOLS)
        # ==========================================
        y = self._draw_header(surface, "EDITOR MODE TOOLS", y)

        tool_btns = [
            ("🧱 Wall", EditTool.WALL, x_left, y),
            ("👨‍🚒 Robot", EditTool.ROBOT, x_right, y),
            ("🐱 Victim", EditTool.VICTIM, x_left, y + 25),
            ("🔥 Fire", EditTool.FIRE, x_right, y + 25),
            ("🏥 Rescue", EditTool.RESCUE, x_left, y + 50),
            ("❌ Erase", EditTool.ERASE, x_right, y + 50),
        ]

        for name, tool, bx, by in tool_btns:
            btn_rect = self._draw_button(surface, name, bx, by, w_btn_half, 20, is_active=(ui_state.active_tool == tool))
            self.buttons[f"tool_{tool.value}"] = btn_rect

        y += 80

        # ==========================================
        # SECTION 3: RUN MODE (RUN ALGORITHM MODE)
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
            active = (state.current_mode == mode)
            if state.current_mode == SimulationState.PAUSED:
                active = (state.selected_algorithm == mode.name)

            btn_rect = self._draw_button(surface, name, bx, by, bw, 22, is_active=active)
            self.buttons[f"run_{mode.value}"] = btn_rect

        y += 112

        # ==========================================
        # SECTION 4: CONTROL (EXECUTION CONTROLS)
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
        # SECTION 5: STATUS (SIMULATION STATUS)
        # ==========================================
        y = self._draw_header(surface, "SIMULATION STATUS", y)

        mode_str = state.current_mode.value
        self._draw_status_item(surface, "Mode:", mode_str, y, is_bold=True)
        y += 18
        self._draw_status_item(surface, "Saved:", f"{state.saved_count} / {len(state.victims)}", y)
        y += 18
        self._draw_status_item(surface, "Dead:", f"{state.dead_count}", y)
        y += 18

        remaining = len(state.victims) - state.saved_count - state.dead_count
        self._draw_status_item(surface, "Remaining:", f"{remaining}", y)
        y += 18

        self._draw_status_item(surface, "Steps:", f"{state.stats.total_steps}", y)
        y += 18
        self._draw_status_item(surface, "Time:", f"{state.simulation_time:.1f} s", y)
        y += 18
        carrying_str = f"Victim #{state.robot.carried_victim_id}" if state.robot.carrying_victim else "None"
        self._draw_status_item(surface, "Carrying:", carrying_str, y)
        y += 25

        # Render Inline status results banner
        if state.current_mode == SimulationState.MISSION_COMPLETE:
            self._draw_result_banner(surface, "MISSION COMPLETE", COLOR_COMPLETE, y)
        elif state.current_mode == SimulationState.MISSION_FAILED:
            self._draw_result_banner(surface, "MISSION FAILED", COLOR_FAILED, y)

        # ==========================================
        # OVERLAY: MAP SIZE DROPDOWN CHOICES
        # ==========================================
        if ui_state.size_dropdown_open:
            options = [10, 15, 20, 25, 30, 35]
            trigger_rect = self.buttons.get("size_dropdown_trigger")
            if trigger_rect:
                tx, ty, tw, th = trigger_rect.x, trigger_rect.y, trigger_rect.width, trigger_rect.height
                container_rect = pygame.Rect(tx, ty + th, tw, len(options) * 20)
                
                # Draw container shadow and background
                pygame.draw.rect(surface, (25, 25, 30), container_rect)
                pygame.draw.rect(surface, COLOR_BTN_ACTIVE, container_rect, 1)

                for idx, opt in enumerate(options):
                    opt_y = ty + th + idx * 20
                    opt_rect = pygame.Rect(tx, opt_y, tw, 20)

                    mx, my = pygame.mouse.get_pos()
                    is_hovered = opt_rect.collidepoint((mx, my))
                    bg_color = COLOR_BTN_HOVER if is_hovered else (25, 25, 30)

                    pygame.draw.rect(surface, bg_color, opt_rect)
                    opt_txt = FONT_TEXT.render(f"{opt}x{opt}", True, COLOR_BTN_TEXT)
                    surface.blit(opt_txt, (tx + 8, opt_y + (20 - opt_txt.get_height()) // 2))

                    self.buttons[f"size_option_{opt}"] = opt_rect

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

    def _draw_dropdown_trigger(self, surface: pygame.Surface, text: str, x: int, y: int, w: int, h: int, is_open: bool) -> pygame.Rect:
        """Render a styled button representing the dropdown box trigger."""
        rect = pygame.Rect(x, y, w, h)
        bg_color = (40, 40, 48) if is_open else (50, 50, 60)
        pygame.draw.rect(surface, bg_color, rect, border_radius=3)
        pygame.draw.rect(surface, COLOR_BORDER, rect, 1, border_radius=3)

        txt_render = FONT_TEXT.render(text, True, COLOR_BTN_TEXT)
        surface.blit(txt_render, (x + 8, y + (h - txt_render.get_height()) // 2))
        return rect

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
        pygame.draw.rect(surface, COLOR_BORDER, rect, 1, border_radius=3)

        txt_render = FONT_TEXT.render(text, True, COLOR_BTN_TEXT)
        tx = x + (w - txt_render.get_width()) / 2
        ty = y + (h - txt_render.get_height()) / 2
        surface.blit(txt_render, (tx, ty))

        return rect

    def _draw_result_banner(self, surface: pygame.Surface, text: str, color: tuple[int, int, int], y: int) -> None:
        """Draw final mission outcome banner inside the status block."""
        rect = pygame.Rect(self.start_x + 15, y + 5, self.width - 30, 32)
        pygame.draw.rect(surface, color, rect, border_radius=4)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1, border_radius=4)

        txt_render = FONT_TITLE.render(text, True, (255, 255, 255))
        tx = rect.x + (rect.width - txt_render.get_width()) / 2
        ty = rect.y + (rect.height - txt_render.get_height()) / 2
        surface.blit(txt_render, (tx, ty))
