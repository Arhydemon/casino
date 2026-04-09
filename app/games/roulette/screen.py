import asyncio
import math
import random
import flet as ft
from app.app_state import AppState
from app.games.roulette.constants import (
    WHEEL_NUMBERS,
    WHEEL_SIZE,
    OUTER_RADIUS,
    INNER_CIRCLE_SIZE,
    SLOT_WIDTH,
    SLOT_HEIGHT,
    SLOT_RADIUS,
    FULL_LOOPS,
    RAMP_UP_STEPS,
    CRUISE_STEPS,
    MIN_TICK_GAP,
    NEAR_MISS_CHANCE,
)
from app.games.roulette.game import RouletteGame
from app.games.roulette.logic import (
    get_number_color,
    maybe_play_tick,
    get_step_delay,
)


class RouletteScreen:
    def __init__(self, page: ft.Page, state: AppState, state_service, go_back):
        self.page = page
        self.state = state
        self.state_service = state_service
        self.go_back = go_back
        self.game = RouletteGame(state)
        self.page.bgcolor = ft.Colors.BLACK

        # запоминаем время последнего тика
        self.last_tick_sound_time = 0.0

        # выбранные параметры ставки
        self.selected_bet_type = "number"
        self.selected_color = "red"
        self._create_controls()
        self._build_layout()
        self.update_bet_inputs()
        self.render_wheel(0)

    # создаю все UI элементы
    def _create_controls(self):
        self.title_text = ft.Text("РУЛЕТКА", size=32, weight=ft.FontWeight.BOLD)
        self.balance_text = ft.Text(f"Баланс: {self.state.player.balance}")
        self.result_text = ft.Text("")
        self.bet_amount_field = ft.TextField(label="Ставка", value="1")
        self.spin_btn = ft.ElevatedButton("SPIN", on_click=self.spin)
        self.back_btn = ft.OutlinedButton("Назад", on_click=self.back)
        self.pointer_text = ft.Text("▼", size=40)
        self.center_number_text = ft.Text("0", size=50)
        self.wheel_stack = ft.Stack(width=WHEEL_SIZE, height=WHEEL_SIZE)
        self.wheel_container = ft.Container(
            width=WHEEL_SIZE,
            height=WHEEL_SIZE,
            content=self.wheel_stack,
        )

    # собираю вывад
    def _build_layout(self):
        self.layout = ft.Column(
            controls=[
                self.pointer_text,
                self.wheel_container,
                self.center_number_text,
                self.bet_amount_field,
                self.spin_btn,
                self.result_text,
                self.back_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # создаем один сектор колеса
    def create_sector(self, number, x, y, angle_deg, is_active=False):
        return ft.Container(
            width=SLOT_WIDTH,
            height=SLOT_HEIGHT,
            left=x,
            top=y,
            rotate=math.radians(angle_deg),
            bgcolor=get_number_color(number),
            border=ft.border.all(3 if is_active else 1),
            content=ft.Text(str(number)),
        )

    # фон колеса
    def build_wheel_background(self):
        return [
            ft.Container(width=WHEEL_SIZE, height=WHEEL_SIZE),
        ]

    # строим все сектора
    def build_wheel_controls(self, active_index):
        controls = self.build_wheel_background()
        center_x = WHEEL_SIZE / 2
        center_y = WHEEL_SIZE / 2
        angle_step = 360 / len(WHEEL_NUMBERS)
        for screen_pos in range(len(WHEEL_NUMBERS)):
            real_index = (active_index + screen_pos) % len(WHEEL_NUMBERS)
            number = WHEEL_NUMBERS[real_index]
            angle_deg = -90 + screen_pos * angle_step
            angle_rad = math.radians(angle_deg)
            x = center_x + OUTER_RADIUS * math.cos(angle_rad) - SLOT_WIDTH / 2
            y = center_y + OUTER_RADIUS * math.sin(angle_rad) - SLOT_HEIGHT / 2

            controls.append(
                self.create_sector(
                    number,
                    x,
                    y,
                    angle_deg + 90,
                    screen_pos == 0,
                )
            )

        self.center_number_text.value = str(WHEEL_NUMBERS[active_index])
        return controls

    # перерисовываю колесо
    def render_wheel(self, active_index):
        self.wheel_stack.controls = self.build_wheel_controls(active_index)

    # анимация вращения
    async def animate_spin(self, final_number):
        total = len(WHEEL_NUMBERS)
        final_index = WHEEL_NUMBERS.index(final_number)
        total_steps = FULL_LOOPS * total + final_index

        ramp_down_steps = total_steps - RAMP_UP_STEPS - CRUISE_STEPS
        if ramp_down_steps < 18:
            ramp_down_steps = 18

        for step in range(total_steps):
            active_index = step % total
            self.render_wheel(active_index)
            self.page.update()

            # звук
            self.last_tick_sound_time = maybe_play_tick(
                self.last_tick_sound_time,
                MIN_TICK_GAP,
            )
            delay = get_step_delay(step, ramp_down_steps)
            await asyncio.sleep(delay)

        # эффект "почти попал"
        if random.random() < NEAR_MISS_CHANCE:
            miss_index = (final_index - 1) % total
            self.render_wheel(miss_index)
            self.page.update()
            self.last_tick_sound_time = maybe_play_tick(
                self.last_tick_sound_time,
                MIN_TICK_GAP,
            )
            await asyncio.sleep(0.16)

        # финальный результат
        self.render_wheel(final_index)
        self.page.update()
        self.last_tick_sound_time = maybe_play_tick(
            self.last_tick_sound_time,
            MIN_TICK_GAP,
        )

    # кнопка SPIN
    async def spin(self, e):
        try:
            amount = int(self.bet_amount_field.value)
        except:
            self.result_text.value = "Нормально введи ставку, долбан"
            self.page.update()
            return

        self.spin_btn.disabled = True
        self.result_text.value = "Круточка"
        self.page.update()
        final_number = random.choice(WHEEL_NUMBERS)

        # крутим анимацию
        await self.animate_spin(final_number)

        # играем раунд
        result = self.game.play_round_with_result(
            "number",
            final_number,
            amount,
            forced_number=final_number,
        )

        self.spin_btn.disabled = False

        if result:
            self.result_text.value = result.message
        else:
            self.result_text.value = self.state.last_result

        self.page.update()

    def back(self, e):
        self.go_back()

    def build(self):
        self.page.controls.clear()
        self.page.add(self.layout)
        self.page.update()