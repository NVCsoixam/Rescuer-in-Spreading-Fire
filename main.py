"""
main.py

Main entry point for the AI Rescue & Fire Simulation System.
Orchestrates Pygame lifecycle, Engine ticks, event parsing, and rendering updates.
"""

import sys
import pygame
from app import config
from app.config import SimulationState
from app.map.generator import MapGenerator
from app.core.engine import Engine
from app.ui.renderer import GridRenderer
from app.ui.sidebar import Sidebar
from app.ui.controls import UIState, handle_events


def main() -> None:
    """
    Bootstrap the application window and runs the interactive Pygame simulation loop.
    """
    pygame.init()
    pygame.display.set_caption("AI Rescue & Fire Simulation System")

    # Set up Pygame window surface
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # 1. Initialize UI helper states
    ui_state = UIState()
    map_generator = MapGenerator()

    # 2. Generate initial layout map (HOSPITAL, MEDIUM complexity by default)
    # Start with seed=42 for deterministic first-launch layout
    initial_state = map_generator.generate(
        width=20,
        height=20,
        env_type=ui_state.selected_env_type,
        complexity=ui_state.selected_complexity,
        seed=42
    )

    # 3. Instantiate Engine and View components
    engine = Engine(initial_state)
    grid_renderer = GridRenderer(config.GRID_AREA_WIDTH, config.WINDOW_HEIGHT)
    sidebar = Sidebar(config.GRID_AREA_WIDTH, config.SIDEBAR_WIDTH, config.WINDOW_HEIGHT)

    # Setup initial fire interval
    engine.fire_interval = float(config.FIRE_INTERVAL_DEFAULT)

    running = True
    print("AI Rescue & Fire Simulation System UI Loop Started.")

    while running:
        # Standardize frame rate ticking and retrieve delta time in milliseconds
        dt_ms = float(clock.tick(config.FPS))

        # Handle keyboard, mouse click, and drag inputs
        events = pygame.event.get()
        running = handle_events(events, engine, sidebar, ui_state, map_generator)

        if not running:
            break

        # Advance engine physics and clocks
        engine.update(dt_ms)

        # Clear background with a sleek theme color
        screen.fill((20, 20, 25))

        # Draw Grid, risk heatmap overlays, and pathfinding routes
        grid_renderer.draw(
            screen,
            engine.state,
            engine.planned_path,
            show_path=ui_state.show_path,
            show_risk=ui_state.show_risk
        )

        # Draw control panels, sliders, and statistics
        sidebar.draw(
            screen,
            engine.state,
            ui_state
        )

        # Flip Pygame buffers to update screen pixels
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
