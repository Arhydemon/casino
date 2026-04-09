import threading
import time
import winsound
import flet as ft
from app.games.roulette.constants import (
    RED_NUMBERS,
    RAMP_UP_STEPS,
    CRUISE_STEPS,
    START_DELAY,
    CRUISE_DELAY,
    END_DELAY,
)

# звук тика рулетки
def play_tick_sound() -> None:
    try:
        winsound.PlaySound(
            "assets/sounds/roulette.wav",
            winsound.SND_FILENAME | winsound.SND_ASYNC,
        )
    except Exception:
        pass

# определяем цвет числа
def get_number_color(number: int):
    if number == 0:
        return ft.Colors.GREEN
    if number in RED_NUMBERS:
        return ft.Colors.RED
    return ft.Colors.BLACK

# чтобы тик не играл слишком часто
def maybe_play_tick(last_tick_sound_time: float, min_tick_gap: float) -> float:
    now = time.perf_counter()
    if now - last_tick_sound_time >= min_tick_gap:
        threading.Thread(target=play_tick_sound, daemon=True).start()
        return now
    return last_tick_sound_time

# считаем задержку между шагами анимации
def get_step_delay(step: int, ramp_down_steps: int) -> float:
    if step < RAMP_UP_STEPS:
        t = step / max(RAMP_UP_STEPS - 1, 1)
        return START_DELAY + (CRUISE_DELAY - START_DELAY) * t

    if step < RAMP_UP_STEPS + CRUISE_STEPS:
        return CRUISE_DELAY
    slow_step = step - RAMP_UP_STEPS - CRUISE_STEPS
    t = slow_step / max(ramp_down_steps - 1, 1)
    smooth = t * t * (3 - 2 * t)
    return CRUISE_DELAY + (END_DELAY - CRUISE_DELAY) * smooth