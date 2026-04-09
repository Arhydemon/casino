import threading
import time
import flet as ft
from playsound import playsound
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
        playsound("assets/sounds/roulette.mp3")
    except Exception:
        pass  # если звук не проигрался то похуй игра продолжается

# определяем цвет числа для UАЯ
def get_number_color(number: int):
    if number == 0:
        return ft.Colors.GREEN
    if number in RED_NUMBERS:
        return ft.Colors.RED
    return ft.Colors.BLACK

# чтобы звук не спамился 100 раз в секунду
def maybe_play_tick(last_tick_time: float, min_gap: float) -> float:
    now = time.perf_counter()
    if now - last_tick_time >= min_gap:
        threading.Thread(target=play_tick_sound, daemon=True).start()
        return now  # обновляем время последнего звука

    return last_tick_time

# считаем задержку между шагами анимации
# тут вся магия плавности вращения
def get_step_delay(step: int, ramp_down_steps: int) -> float:
    # разгон
    if step < RAMP_UP_STEPS:
        t = step / max(RAMP_UP_STEPS - 1, 1)
        return START_DELAY + (CRUISE_DELAY - START_DELAY) * t

    # ровное вращение
    if step < RAMP_UP_STEPS + CRUISE_STEPS:
        return CRUISE_DELAY

    # торможение
    slow_step = step - RAMP_UP_STEPS - CRUISE_STEPS
    t = slow_step / max(ramp_down_steps - 1, 1)
    smooth = t * t * (3 - 2 * t) # плавная функция (чтобы не было резкого стопа)
    return CRUISE_DELAY + (END_DELAY - CRUISE_DELAY) * smooth