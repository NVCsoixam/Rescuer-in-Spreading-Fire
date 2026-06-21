"""
capture_history_modal.py

Chup anh man hinh bong History da co cot Map.
Chay 3 thuat toan tren cac map khac nhau de tao du lieu,
sau do chup anh modal History.
"""

import os
import pygame
from app import config
from app.config import SimulationState
from app.map.generator import MapGenerator
from app.core.engine import Engine
from app.ui.renderer import GridRenderer
from app.ui.sidebar import Sidebar
from app.ui.controls import UIState

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE_DIR, "screenshots", "history_with_map.png")
os.makedirs(os.path.dirname(OUT), exist_ok=True)


def run_algo(engine, mode, max_steps=300):
    engine.start(mode)
    for _ in range(max_steps):
        engine.simulation_step()
        if engine.state.current_mode in (
            SimulationState.MISSION_COMPLETE, SimulationState.MISSION_FAILED
        ):
            break


def main():
    pygame.init()
    pygame.display.set_caption("History Capture")
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    grid_renderer = GridRenderer(config.GRID_AREA_WIDTH, config.WINDOW_HEIGHT)
    sidebar = Sidebar(config.GRID_AREA_WIDTH, config.SIDEBAR_WIDTH, config.WINDOW_HEIGHT)
    ui_state = UIState()
    gen = MapGenerator()

    # --- Map 1: seed 42 ---
    state1 = gen.generate(width=20, height=20, seed=42)
    engine = Engine(state1)
    engine.fire_interval = 2000.0
    run_algo(engine, SimulationState.BFS)
    print(f"[1] BFS on {state1.map_size} #{state1.map_seed}: "
          f"{engine.state.current_mode.value}, saved={engine.state.saved_count}")

    # Reset va chay A* tren cung map
    engine.reset()
    run_algo(engine, SimulationState.ASTAR)
    print(f"[2] A* on {engine.state.map_size} #{engine.state.map_seed}: "
          f"{engine.state.current_mode.value}, saved={engine.state.saved_count}")

    # --- Map 2: seed 99 ---
    state2 = gen.generate(width=20, height=20, seed=99)
    state2.history = engine.state.history  # Giu history cu
    engine2 = Engine(state2)
    engine2.fire_interval = 2000.0
    run_algo(engine2, SimulationState.GREEDY)
    print(f"[3] GREEDY on {state2.map_size} #{state2.map_seed}: "
          f"{engine2.state.current_mode.value}, saved={engine2.state.saved_count}")

    # --- Map 3: seed 7 ---
    state3 = gen.generate(width=15, height=15, seed=7)
    state3.history = engine2.state.history  # Giu history cu
    engine3 = Engine(state3)
    engine3.fire_interval = 2000.0
    run_algo(engine3, SimulationState.DIJKSTRA)
    print(f"[4] DIJKSTRA on {state3.map_size} #{state3.map_seed}: "
          f"{engine3.state.current_mode.value}, saved={engine3.state.saved_count}")

    print(f"Total history entries: {len(engine3.state.history)}")

    # --- Hien thi modal History ---
    ui_state.history_open = True

    pygame.event.pump()
    screen.fill((20, 20, 25))
    grid_renderer.draw(screen, engine3.state, engine3.planned_path)
    sidebar.draw(screen, engine3.state, ui_state)
    sidebar.draw_history_overlay(screen, engine3.state, ui_state)
    pygame.display.flip()

    pygame.image.save(screen, OUT)
    print(f"[OK] Saved: {OUT}")
    pygame.quit()


if __name__ == "__main__":
    main()
