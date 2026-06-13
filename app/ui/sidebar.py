"""
app/ui/sidebar.py

Sidebar Controller and UI Panel for the 2D Rescue Simulation System.
Renders control buttons, settings, and live status dashboard.
"""

from __future__ import annotations
import time
import pygame
from app.config import SimulationState, EditTool
from app.core.state import GameState

# Colors matching premium design standards
COLOR_SIDEBAR_BG = (21, 21, 26)  # Dark metallic gray
COLOR_SECTION_HEADER = (170, 180, 195)  # Soft light blue-gray
COLOR_LABEL = (195, 205, 215)  # Muted gray text
COLOR_BTN_BG = (43, 50, 68)  # Slate blue-gray
COLOR_BTN_HOVER = (60, 72, 98)  # Bright hover gray-blue
COLOR_BTN_ACTIVE = (0, 150, 255)  # Electric Dodger Blue active
COLOR_BTN_TEXT = (255, 255, 255)
COLOR_BORDER = (55, 65, 82)  # Dark border line
COLOR_DANGER = (231, 76, 60)  # Modern coral red
COLOR_WARNING = (241, 196, 15)  # Bright amber gold

# Result Banner Colors
COLOR_COMPLETE = (46, 204, 113)  # Emerald green
COLOR_FAILED = (231, 76, 60)  # Crimson red

# Safe Font Loader
pygame.font.init()
FONT_TITLE = pygame.font.SysFont("segoeui", 12, bold=True)
FONT_TEXT = pygame.font.SysFont("segoeui", 12)
FONT_BOLD = pygame.font.SysFont("segoeui", 12, bold=True)


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
        self.buttons: dict[str, pygame.Rect] = {}

    def draw(self, surface: pygame.Surface, state: GameState, ui_state) -> None:
        """
        Render the sidebar and its sections onto the Pygame window.

        Args:
            surface: The main window surface.
            state: The GameState object.
            ui_state: The UIState wrapper containing settings and layout state.
        """
        sidebar_rect = pygame.Rect(self.start_x, 0, self.width, self.height)
        pygame.draw.rect(surface, COLOR_SIDEBAR_BG, sidebar_rect)
        pygame.draw.line(surface, COLOR_BORDER, (self.start_x, 0), (self.start_x, self.height), 2)

        self.buttons.clear()

        x_left = self.start_x + 15
        x_right = self.start_x + 125
        w_half = 100
        w_full = 210

        y = 15

        # ==========================================
        # SECTION 1: MAP SETTINGS
        # ==========================================
        y = self._draw_header(surface, "MAP SETTINGS", y)

        # Map Size
        size_lbl = FONT_TEXT.render("Map Size:", True, COLOR_LABEL)
        surface.blit(size_lbl, (x_left, y))
        size_trigger = self._draw_dropdown_trigger(
            surface,
            f"{ui_state.selected_size}x{ui_state.selected_size}  ▼",
            x_left + 85, y - 2, 115, 20,
            is_open=ui_state.size_dropdown_open
        )
        self.buttons["size_dropdown_trigger"] = size_trigger
        y += 28

        # Fire Interval Textbox
        interval_lbl = FONT_TEXT.render("Fire Speed (ms):", True, COLOR_LABEL)
        surface.blit(interval_lbl, (x_left, y))
        textbox = pygame.Rect(x_left + 100, y - 2, 100, 20)
        bg = (15, 15, 20) if ui_state.fire_interval_focused else (30, 30, 38)
        border = COLOR_BTN_ACTIVE if ui_state.fire_interval_focused else COLOR_BORDER
        pygame.draw.rect(surface, bg, textbox, border_radius=4)
        pygame.draw.rect(surface, border, textbox, 1, border_radius=4)

        txt = ui_state.fire_interval_text
        if ui_state.fire_interval_focused:
            cursor = "|" if int(time.time() * 2) % 2 == 0 else ""
            txt += cursor
        txt_render = FONT_TEXT.render(txt, True, (255, 255, 255))
        surface.blit(txt_render, (textbox.x + 8, textbox.y + (textbox.height - txt_render.get_height()) // 2))
        self.buttons["fire_interval_input"] = textbox
        y += 28

        # Generate Button
        btn_gen = self._draw_btn(surface, "GENERATE RANDOM MAP", x_left, y, w_full, 28)
        self.buttons["generate_map"] = btn_gen
        y += 38

        # ==========================================
        # SECTION 2: EDITOR MODE TOOLS
        # ==========================================
        y = self._draw_header(surface, "EDITOR MODE TOOLS", y)

        tools = [
            ("🧱 Wall", EditTool.WALL, x_left, y),
            ("🤖 Robot", EditTool.ROBOT, x_right, y),
            ("👤 Victim", EditTool.VICTIM, x_left, y + 25),
            ("🔥 Fire", EditTool.FIRE, x_right, y + 25),
            ("🏥 Rescue", EditTool.RESCUE, x_left, y + 50),
            ("❌ Erase", EditTool.ERASE, x_right, y + 50),
        ]
        for name, tool, bx, by in tools:
            btn = self._draw_btn(surface, name, bx, by, w_half, 20, active=(ui_state.active_tool == tool))
            self.buttons[f"tool_{tool.value}"] = btn
        y += 80

        # ==========================================
        # SECTION 3: RUN ALGORITHM MODE
        # ==========================================
        y = self._draw_header(surface, "RUN ALGORITHM MODE", y)

        algorithms = [
            ("MANUAL CONTROL", SimulationState.USER_MODE, x_left, y, w_full),
            ("BFS", SimulationState.BFS, x_left, y + 28, w_half),
            ("A* SEARCH", SimulationState.ASTAR, x_right, y + 28, w_half),
            ("DFS", SimulationState.DFS, x_left, y + 53, w_half),
            ("UCS (Risk)", SimulationState.UCS, x_right, y + 53, w_half),
            ("DIJKSTRA", SimulationState.DIJKSTRA, x_left, y + 78, w_half),
            ("GREEDY S.", SimulationState.GREEDY, x_right, y + 78, w_half),
        ]
        for name, mode, bx, by, bw in algorithms:
            active = state.current_mode == mode
            if state.current_mode == SimulationState.PAUSED:
                active = state.selected_algorithm == mode.name
            btn = self._draw_btn(surface, name, bx, by, bw, 22, active=active)
            self.buttons[f"run_{mode.value}"] = btn
        y += 112

        # ==========================================
        # SECTION 4: EXECUTION CONTROLS
        # ==========================================
        y = self._draw_header(surface, "EXECUTION CONTROLS", y)

        pause_lbl = "RESUME" if state.current_mode == SimulationState.PAUSED else "PAUSE"
        btn_pause = self._draw_btn(
            surface, pause_lbl, x_left, y, w_half, 28,
            active=(state.current_mode == SimulationState.PAUSED)
        )
        btn_reset = self._draw_btn(surface, "RESET", x_right, y, w_half, 28)
        self.buttons["control_pause"] = btn_pause
        self.buttons["control_reset"] = btn_reset
        y += 40

        # ==========================================
        # SECTION 5: SIMULATION STATUS
        # ==========================================
        y = self._draw_header(surface, "SIMULATION STATUS", y)

        mode_str = state.current_mode.value
        self._draw_status(surface, "Mode:", mode_str, y, bold=True)
        y += 22
        self._draw_status(surface, "Saved:", f"{state.saved_count} / {state.total_victims}", y)
        y += 22
        self._draw_status(surface, "Dead:", f"{state.dead_count}", y,
                          color=COLOR_DANGER if state.dead_count > 0 else (255, 255, 255))
        y += 22
        remaining = state.remaining_victims
        self._draw_status(surface, "Remaining:", f"{remaining}", y,
                          color=COLOR_WARNING if remaining > 0 else (255, 255, 255))
        y += 22
        self._draw_status(surface, "Steps:", f"{state.stats.total_steps}", y)
        y += 22
        self._draw_status(surface, "Time:", f"{state.simulation_time:.1f}s", y)
        y += 22
        self._draw_status(surface, "Replans:", f"{state.stats.replans}", y)
        y += 22
        carrying = f"V#{state.robot.carried_victim_id}" if state.robot.carrying_victim else "None"
        self._draw_status(surface, "Carrying:", carrying, y,
                          color=COLOR_BTN_ACTIVE if state.robot.carrying_victim else (255, 255, 255))
        y += 32

        # Mission result banner
        if state.current_mode == SimulationState.MISSION_COMPLETE:
            self._draw_banner(surface, "MISSION COMPLETE", COLOR_COMPLETE, y)
        elif state.current_mode == SimulationState.MISSION_FAILED:
            self._draw_banner(surface, "MISSION FAILED", COLOR_FAILED, y)

        # ==========================================
        # OVERLAY: MAP SIZE DROPDOWN
        # ==========================================
        if ui_state.size_dropdown_open:
            self._draw_size_dropdown(surface, ui_state)

    def _draw_size_dropdown(self, surface: pygame.Surface, ui_state) -> None:
        """Draw the size selection dropdown overlay."""
        options = [10, 15, 20, 25, 30, 35]
        trigger = self.buttons.get("size_dropdown_trigger")
        if not trigger:
            return

        tx, ty, tw = trigger.x, trigger.y, trigger.width
        container = pygame.Rect(tx, ty + trigger.height, tw, len(options) * 20)
        pygame.draw.rect(surface, (25, 25, 30), container, border_radius=4)
        pygame.draw.rect(surface, COLOR_BTN_ACTIVE, container, 1, border_radius=4)
        mouse_pos = pygame.mouse.get_pos()

        for idx, opt in enumerate(options):
            opt_y = ty + trigger.height + idx * 20
            opt_rect = pygame.Rect(tx, opt_y, tw, 20)
            hovered = opt_rect.collidepoint(mouse_pos)
            bg = COLOR_BTN_HOVER if hovered else (25, 25, 30)
            pygame.draw.rect(surface, bg, opt_rect)
            txt = FONT_TEXT.render(f"{opt}x{opt}", True, COLOR_BTN_TEXT)
            surface.blit(txt, (tx + 8, opt_y + (20 - txt.get_height()) // 2))
            self.buttons[f"size_option_{opt}"] = opt_rect

    def _draw_header(self, surface: pygame.Surface, text: str, y: int) -> int:
        """Draw a section header with underline."""
        hdr = FONT_TITLE.render(text, True, COLOR_SECTION_HEADER)
        surface.blit(hdr, (self.start_x + 15, y))
        pygame.draw.line(surface, COLOR_BORDER,
                         (self.start_x + 15, y + 16),
                         (self.start_x + self.width - 15, y + 16), 1)
        return y + 24

    def _draw_status(self, surface: pygame.Surface, label: str, val: str, y: int,
                     bold: bool = False, color: tuple = (255, 255, 255)) -> None:
        """Draw a status label-value pair within a polished status bar card."""
        rect = pygame.Rect(self.start_x + 15, y - 2, self.width - 30, 20)
        pygame.draw.rect(surface, (28, 28, 35), rect, border_radius=4)
        pygame.draw.rect(surface, COLOR_BORDER, rect, 1, border_radius=4)
        
        lbl = FONT_TEXT.render(label, True, COLOR_LABEL)
        surface.blit(lbl, (self.start_x + 23, y))
        font = FONT_BOLD if bold else FONT_TEXT
        val_r = font.render(val, True, color)
        surface.blit(val_r, (self.start_x + 120, y))

    def _draw_dropdown_trigger(self, surface: pygame.Surface, text: str,
                                x: int, y: int, w: int, h: int,
                                is_open: bool = False) -> pygame.Rect:
        """Draw a dropdown trigger button."""
        rect = pygame.Rect(x, y, w, h)
        bg = (30, 30, 38) if is_open else COLOR_BTN_BG
        pygame.draw.rect(surface, bg, rect, border_radius=4)
        pygame.draw.rect(surface, COLOR_BORDER, rect, 1, border_radius=4)
        txt = FONT_TEXT.render(text, True, COLOR_BTN_TEXT)
        surface.blit(txt, (x + 8, y + (h - txt.get_height()) // 2))
        return rect

    def _draw_btn(self, surface: pygame.Surface, text: str, x: int, y: int,
                   w: int, h: int, active: bool = False) -> pygame.Rect:
        """Draw a button with hover/active states."""
        rect = pygame.Rect(x, y, w, h)
        mouse_pos = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_pos)

        if active:
            bg = COLOR_BTN_ACTIVE
        elif hovered:
            bg = COLOR_BTN_HOVER
        else:
            bg = COLOR_BTN_BG

        pygame.draw.rect(surface, bg, rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_BORDER, rect, 1, border_radius=6)

        txt = FONT_TEXT.render(text, True, COLOR_BTN_TEXT)
        surface.blit(txt, (x + (w - txt.get_width()) // 2, y + (h - txt.get_height()) // 2))
        return rect

    def _draw_banner(self, surface: pygame.Surface, text: str,
                      color: tuple[int, int, int], y: int) -> None:
        """Draw a mission status banner."""
        rect = pygame.Rect(self.start_x + 15, y + 5, self.width - 30, 32)
        pygame.draw.rect(surface, color, rect, border_radius=6)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1, border_radius=6)
        txt = FONT_TITLE.render(text, True, (255, 255, 255))
        surface.blit(txt, (rect.x + (rect.width - txt.get_width()) // 2,
                          rect.y + (rect.height - txt.get_height()) // 2))