import asyncio
import math
import random
import threading
import time

import flet as ft
from playsound import playsound

from app.app_state import AppState
from app.games.roulette.game import RouletteGame


def play_tick_sound() -> None:
    try:
        playsound("assets/sounds/roulette.mp3")
    except Exception:
        pass


class RouletteScreen:
    WHEEL_NUMBERS = [
        0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
        6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
        24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
        29, 7, 28, 12, 35, 3, 26,
    ]

    RED_NUMBERS = {
        1, 3, 5, 7, 9, 12, 14, 16, 18,
        19, 21, 23, 25, 27, 30, 32, 34, 36,
    }

    WHEEL_SIZE = 700
    OUTER_RADIUS = 268
    INNER_CIRCLE_SIZE = 320

    SLOT_WIDTH = 34
    SLOT_HEIGHT = 88
    SLOT_RADIUS = 7

    FULL_LOOPS = 4
    RAMP_UP_STEPS = 14
    CRUISE_STEPS = 50

    START_DELAY = 0.11
    CRUISE_DELAY = 0.028
    END_DELAY = 0.16

    MIN_TICK_GAP = 0.05
    NEAR_MISS_CHANCE = 0.3

    def __init__(self, page: ft.Page, state: AppState, state_service, go_back):
        self.page = page
        self.state = state
        self.state_service = state_service
        self.go_back = go_back
        self.game = RouletteGame(state)

        self.last_tick_sound_time = 0.0
        self.page.bgcolor = ft.Colors.BLACK

        self.selected_bet_type = "number"
        self.selected_color = "red"

        self._create_controls()
        self._build_layout()
        self.update_bet_inputs()
        self.render_wheel(0)

    def _create_controls(self) -> None:
        self.title_text = ft.Text(
            "РУЛЕТКА",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.AMBER,
        )

        self.balance_text = ft.Text(
            f"Баланс: {self.state.player.balance}",
            size=20,
            color=ft.Colors.WHITE,
        )

        self.result_text = ft.Text(
            "",
            size=18,
            color=ft.Colors.WHITE,
            text_align=ft.TextAlign.CENTER,
        )

        self.bet_amount_field = ft.TextField(
            label="Ставка",
            width=280,
            value="1",
        )

        self.bet_type_label = ft.Text(
            "Тип ставки",
            size=14,
            color=ft.Colors.WHITE70,
        )

        self.bet_type_number_btn = ft.ElevatedButton("Число", width=130)
        self.bet_type_number_btn.on_click = lambda e: self.set_bet_type("number")

        self.bet_type_color_btn = ft.ElevatedButton("Цвет", width=130)
        self.bet_type_color_btn.on_click = lambda e: self.set_bet_type("color")

        self.bet_type_even_btn = ft.ElevatedButton("Чётное", width=130)
        self.bet_type_even_btn.on_click = lambda e: self.set_bet_type("even")

        self.bet_type_odd_btn = ft.ElevatedButton("Нечётное", width=130)
        self.bet_type_odd_btn.on_click = lambda e: self.set_bet_type("odd")

        self.bet_type_block = ft.Column(
            controls=[
                self.bet_type_label,
                ft.Row(
                    controls=[
                        self.bet_type_number_btn,
                        self.bet_type_color_btn,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        self.bet_type_even_btn,
                        self.bet_type_odd_btn,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.number_dropdown = ft.Dropdown(
            label="Выберите число",
            width=280,
            value="0",
            options=[ft.dropdown.Option(str(i)) for i in range(37)],
        )

        self.number_block = ft.Column(
            controls=[self.number_dropdown],
            visible=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.color_label = ft.Text(
            "Выберите цвет",
            size=14,
            color=ft.Colors.WHITE70,
        )

        self.red_btn = ft.ElevatedButton("Красный", width=180)
        self.red_btn.on_click = lambda e: self.set_color("red")

        self.black_btn = ft.ElevatedButton("Чёрный", width=180)
        self.black_btn.on_click = lambda e: self.set_color("black")

        self.green_btn = ft.ElevatedButton("Зелёный", width=180)
        self.green_btn.on_click = lambda e: self.set_color("green")

        self.color_block = ft.Column(
            controls=[
                self.color_label,
                self.red_btn,
                self.black_btn,
                self.green_btn,
            ],
            visible=False,
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.no_extra_text = ft.Text(
            "Дополнительный выбор не нужен",
            size=14,
            color=ft.Colors.WHITE54,
            visible=False,
            text_align=ft.TextAlign.CENTER,
        )

        self.pointer_text = ft.Text(
            "▼",
            size=40,
            color=ft.Colors.AMBER,
        )

        self.center_number_text = ft.Text(
            "0",
            size=50,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.AMBER,
        )

        self.wheel_stack = ft.Stack(
            width=self.WHEEL_SIZE,
            height=self.WHEEL_SIZE,
        )

        self.wheel_container = ft.Container(
            width=self.WHEEL_SIZE,
            height=self.WHEEL_SIZE,
            content=self.wheel_stack,
            alignment=ft.alignment.Alignment(0, 0),
        )

        self.spin_btn = ft.ElevatedButton(
            "SPIN",
            width=240,
            height=50,
        )
        self.spin_btn.on_click = self.spin

        self.back_btn = ft.OutlinedButton(
            "Назад",
            width=240,
            height=44,
        )
        self.back_btn.on_click = self.back

        self.controls_card = ft.Container(
            width=340,
            padding=22,
            border_radius=14,
            bgcolor=ft.Colors.GREY_900,
            border=ft.border.all(2, ft.Colors.GREY_700),
            content=ft.Column(
                controls=[
                    self.title_text,
                    self.balance_text,
                    ft.Container(height=8),
                    self.bet_amount_field,
                    self.bet_type_block,
                    self.number_block,
                    self.color_block,
                    self.no_extra_text,
                    ft.Container(height=6),
                    self.spin_btn,
                    self.result_text,
                    self.back_btn,
                ],
                spacing=14,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def _build_layout(self) -> None:
        left_panel = ft.Container(
            expand=1,
            padding=ft.padding.only(left=10, right=10),
            alignment=ft.alignment.Alignment(0, 0),
            content=ft.Column(
                controls=[
                    self.pointer_text,
                    self.wheel_container,
                    self.center_number_text,
                ],
                spacing=14,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        right_panel = ft.Container(
            width=360,
            alignment=ft.alignment.Alignment(0, 0),
            content=self.controls_card,
        )

        self.layout = ft.Container(
            expand=True,
            padding=10,
            content=ft.Row(
                controls=[left_panel, right_panel],
                spacing=10,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def get_number_color(self, number: int):
        if number == 0:
            return ft.Colors.GREEN
        if number in self.RED_NUMBERS:
            return ft.Colors.RED
        return ft.Colors.BLACK

    def maybe_play_tick(self) -> None:
        now = time.perf_counter()
        if now - self.last_tick_sound_time >= self.MIN_TICK_GAP:
            self.last_tick_sound_time = now
            threading.Thread(target=play_tick_sound, daemon=True).start()

    def set_result(self, text: str, color) -> None:
        self.result_text.value = text
        self.result_text.color = color

    def update_balance_text(self) -> None:
        self.balance_text.value = f"Баланс: {self.state.player.balance}"

    def get_bet_amount(self) -> int:
        value = (self.bet_amount_field.value or "").strip()
        amount = int(value)
        if amount <= 0:
            raise ValueError
        return amount

    def set_bet_type(self, bet_type: str) -> None:
        self.selected_bet_type = bet_type
        self.update_bet_inputs()

    def set_color(self, color_value: str) -> None:
        self.selected_color = color_value
        self.update_color_buttons()
        self.page.update()

    def update_type_buttons(self) -> None:
        selected = self.selected_bet_type

        self.bet_type_number_btn.disabled = selected == "number"
        self.bet_type_color_btn.disabled = selected == "color"
        self.bet_type_even_btn.disabled = selected == "even"
        self.bet_type_odd_btn.disabled = selected == "odd"

    def update_color_buttons(self) -> None:
        self.red_btn.disabled = self.selected_color == "red"
        self.black_btn.disabled = self.selected_color == "black"
        self.green_btn.disabled = self.selected_color == "green"

    def get_selected_bet(self):
        if self.selected_bet_type == "number":
            return "number", int(self.number_dropdown.value)

        if self.selected_bet_type == "color":
            return "color", self.selected_color

        if self.selected_bet_type == "even":
            return "even", None

        return "odd", None

    def create_sector(
        self,
        number: int,
        x: float,
        y: float,
        angle_deg: float,
        is_active: bool = False,
    ):
        return ft.Container(
            width=self.SLOT_WIDTH,
            height=self.SLOT_HEIGHT,
            left=x,
            top=y,
            rotate=math.radians(angle_deg),
            border_radius=self.SLOT_RADIUS,
            bgcolor=self.get_number_color(number),
            border=ft.border.all(
                3 if is_active else 1,
                ft.Colors.AMBER if is_active else ft.Colors.GREY_800,
            ),
            alignment=ft.alignment.Alignment(0, 0),
            content=ft.Text(
                str(number),
                size=13,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
        )

    def build_wheel_background(self):
        return [
            ft.Container(
                width=self.WHEEL_SIZE,
                height=self.WHEEL_SIZE,
                border_radius=self.WHEEL_SIZE / 2,
                bgcolor=ft.Colors.GREY_900,
                border=ft.border.all(5, ft.Colors.GREY_700),
            ),
            ft.Container(
                width=self.WHEEL_SIZE - 40,
                height=self.WHEEL_SIZE - 40,
                left=20,
                top=20,
                border_radius=(self.WHEEL_SIZE - 40) / 2,
                bgcolor=ft.Colors.GREY_800,
                border=ft.border.all(2, ft.Colors.GREY_700),
            ),
            ft.Container(
                width=self.INNER_CIRCLE_SIZE,
                height=self.INNER_CIRCLE_SIZE,
                left=(self.WHEEL_SIZE - self.INNER_CIRCLE_SIZE) / 2,
                top=(self.WHEEL_SIZE - self.INNER_CIRCLE_SIZE) / 2,
                border_radius=self.INNER_CIRCLE_SIZE / 2,
                bgcolor=ft.Colors.BLACK,
                border=ft.border.all(3, ft.Colors.GREY_700),
            ),
        ]

    def build_wheel_controls(self, active_index: int):
        controls = self.build_wheel_background()

        center_x = self.WHEEL_SIZE / 2
        center_y = self.WHEEL_SIZE / 2
        angle_step = 360 / len(self.WHEEL_NUMBERS)

        for screen_pos in range(len(self.WHEEL_NUMBERS)):
            real_index = (active_index + screen_pos) % len(self.WHEEL_NUMBERS)
            number = self.WHEEL_NUMBERS[real_index]

            angle_deg = -90 + screen_pos * angle_step
            angle_rad = math.radians(angle_deg)

            x = center_x + self.OUTER_RADIUS * math.cos(angle_rad) - self.SLOT_WIDTH / 2
            y = center_y + self.OUTER_RADIUS * math.sin(angle_rad) - self.SLOT_HEIGHT / 2

            controls.append(
                self.create_sector(
                    number=number,
                    x=x,
                    y=y,
                    angle_deg=angle_deg + 90,
                    is_active=(screen_pos == 0),
                )
            )

        self.center_number_text.value = str(self.WHEEL_NUMBERS[active_index])
        return controls

    def render_wheel(self, active_index: int) -> None:
        self.wheel_stack.controls = self.build_wheel_controls(active_index)

    def update_bet_inputs(self, e=None) -> None:
        self.update_type_buttons()
        self.update_color_buttons()

        self.number_block.visible = self.selected_bet_type == "number"
        self.color_block.visible = self.selected_bet_type == "color"
        self.no_extra_text.visible = self.selected_bet_type in ("even", "odd")

        self.page.update()

    def _get_step_delay(self, step: int, ramp_down_steps: int) -> float:
        if step < self.RAMP_UP_STEPS:
            t = step / max(self.RAMP_UP_STEPS - 1, 1)
            return self.START_DELAY + (self.CRUISE_DELAY - self.START_DELAY) * t

        if step < self.RAMP_UP_STEPS + self.CRUISE_STEPS:
            return self.CRUISE_DELAY

        slow_step = step - self.RAMP_UP_STEPS - self.CRUISE_STEPS
        t = slow_step / max(ramp_down_steps - 1, 1)
        smooth = t * t * (3 - 2 * t)
        return self.CRUISE_DELAY + (self.END_DELAY - self.CRUISE_DELAY) * smooth

    async def animate_spin(self, final_number: int) -> None:
        total = len(self.WHEEL_NUMBERS)
        final_index = self.WHEEL_NUMBERS.index(final_number)

        total_steps = self.FULL_LOOPS * total + final_index
        ramp_down_steps = total_steps - self.RAMP_UP_STEPS - self.CRUISE_STEPS
        if ramp_down_steps < 18:
            ramp_down_steps = 18

        for step in range(total_steps):
            active_index = step % total

            self.render_wheel(active_index)
            self.page.update()
            self.maybe_play_tick()

            delay = self._get_step_delay(step, ramp_down_steps)
            await asyncio.sleep(delay)

        if random.random() < self.NEAR_MISS_CHANCE:
            miss_index = (final_index - 1) % total
            self.render_wheel(miss_index)
            self.page.update()
            self.maybe_play_tick()
            await asyncio.sleep(0.16)

        self.render_wheel(final_index)
        self.page.update()
        self.maybe_play_tick()

    def _apply_round_stats(self, round_result) -> None:
        self.state.games_played += 1

        if round_result.is_win:
            self.state.games_won += 1
            self.state.total_win += round_result.win_amount

    async def spin(self, e) -> None:
        try:
            amount = self.get_bet_amount()
        except ValueError:
            self.set_result("Нормально введи ставку", ft.Colors.RED)
            self.page.update()
            return

        bet_type, bet_value = self.get_selected_bet()

        self.spin_btn.disabled = True
        self.set_result("Крутим...", ft.Colors.WHITE)
        self.page.update()

        final_number = random.choice(self.WHEEL_NUMBERS)

        await self.animate_spin(final_number)

        round_result = self.game.play_round_with_result(
            bet_type=bet_type,
            bet_value=bet_value,
            amount=amount,
            forced_number=final_number,
        )

        self.spin_btn.disabled = False

        if round_result is None:
            self.set_result(self.state.last_result, ft.Colors.RED)
            self.page.update()
            return

        self.update_balance_text()
        self.set_result(
            round_result.message,
            ft.Colors.GREEN if round_result.is_win else ft.Colors.RED,
        )

        self._apply_round_stats(round_result)
        self.state_service.save_state(self.state)
        self.page.update()

    def back(self, e) -> None:
        self.go_back()

    def build(self) -> None:
        self.page.controls.clear()
        self.page.add(self.layout)
        self.page.update()