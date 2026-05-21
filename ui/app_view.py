import asyncio
import math
import random
import flet as ft

from config import APP_TITLE
from config import (
    ROULETTE_BALL_END_RADIUS,
    ROULETTE_BALL_START_RADIUS,
    ROULETTE_SPIN_DURATION_SECONDS,
    ROULETTE_SPIN_EXTRA_TURNS,
)
from database.database_manager import DatabaseManager
from games.base_game import BaseGame
from games.roulette_game import RouletteGame
from games.slots_game import SlotsGame
from services.app_state_service import AppStateService
from services.log_service import LogService
from services.sound_service import SoundService
from ui.components.balance_panel import build_result_banner
from ui.main_menu_view import build_main_menu_view
from ui.roulette_view import ( build_roulette_ball, build_roulette_view, build_roulette_wheel, move_ball, roulette_angle_for_number, roulette_number_for_angle,)
from ui.settings_view import build_settings_view
from ui.slots_view import build_reel, build_slots_view
from ui.statistics_view import build_statistics_view


class CasinoApp:
    SLOT_SYMBOLS = {
        "cherry": "🍒",
        "lemon": "🍋",
        "bell": "🔔",
        "star": "⭐",
        "seven": "7️⃣",
    }

    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.db = DatabaseManager()
        self.db.create_tables()
        self.state_service = AppStateService(self.db)
        self.state = self.state_service.load_state()
        self.log_service = LogService(self.state.player.login)
        self.sound_service = SoundService(page, self.state.settings)
        self.is_animating = False
        self.is_closing = False
        self.is_closed = False
        self.balance_refs: dict[str, ft.Text] = {}
        self.roulette_balance_refs: dict[str, ft.Text] = {}
        self.slots_balance_refs: dict[str, ft.Text] = {}
        self.roulette_bet_type = "number"
        self.roulette_bet_value: int | str = 0
        self.roulette_number_text = ft.Text("0", size=56, weight=ft.FontWeight.BOLD, color="#22c55e")
        self.roulette_selected_bet_text = ft.Text("Текущая ставка: число 0", size=14, color="#d1d5db")
        self.roulette_selected_number_text = ft.Text("Шарик на числе: 0", size=14, color="#9ca3af")
        self.roulette_ball = build_roulette_ball()
        move_ball(self.roulette_ball, roulette_angle_for_number(0), ROULETTE_BALL_START_RADIUS)
        self.roulette_wheel = build_roulette_wheel(self.roulette_number_text, self.roulette_ball)
        self.roulette_result_banner = build_result_banner(None)
        self.slots_result_banner = build_result_banner(None)
        self.roulette_bet_field = self._bet_field("Ставка для рулетки")
        self.roulette_value_field = ft.TextField(
            label="Число 0-36",
            value="0",
            bgcolor="#0b1117",
            color="#f9fafb",
            border_color="#334155",
            focused_border_color="#22c55e",
        )
        self.slots_bet_field = self._bet_field("Ставка для слотов")
        self.slots_text_controls = [
            ft.Text("🍒", size=70, text_align=ft.TextAlign.CENTER),
            ft.Text("🍋", size=70, text_align=ft.TextAlign.CENTER),
            ft.Text("⭐", size=70, text_align=ft.TextAlign.CENTER),
        ]
        self.slots_reels = [build_reel(control) for control in self.slots_text_controls]
        self.sound_switch = ft.Switch(
            value=self.state.settings.is_sound_enabled(),
            label="Включить звук",
            active_color="#22c55e",
            on_change=self.change_sound,
        )

    def run(self) -> None:
        self._configure_page()
        self.show_main_menu()

    def show_main_menu(self, e=None) -> None:
        self._set_view(
            build_main_menu_view(
                self.state,
                self.show_roulette,
                self.show_slots,
                self.show_statistics,
                self.show_settings,
            )
        )

    def show_roulette(self, e=None) -> None:
        self._refresh_balance_refs(self.roulette_balance_refs)
        self._update_roulette_controls()
        self._set_view(
            build_roulette_view(
                self.state,
                self.roulette_balance_refs,
                self.roulette_bet_field,
                self.roulette_value_field,
                self.roulette_selected_bet_text,
                self.roulette_selected_number_text,
                self.roulette_wheel,
                self.roulette_result_banner,
                self.play_roulette,
                self.show_main_menu,
                self.select_roulette_number,
                self.select_roulette_color,
                self.select_roulette_even_odd,
            )
        )

    def show_slots(self, e=None) -> None:
        self._refresh_balance_refs(self.slots_balance_refs)
        self._set_view(
            build_slots_view(
                self.state,
                self.slots_balance_refs,
                self.slots_bet_field,
                self.slots_reels,
                self.slots_result_banner,
                self.play_slots,
                self.show_main_menu,
            )
        )

    def show_statistics(self, e=None) -> None:
        self._set_view(build_statistics_view(self.state, self.reset_statistics, self.show_main_menu))

    def show_settings(self, e=None) -> None:
        self.sound_switch.value = self.state.settings.is_sound_enabled()
        self._set_view(build_settings_view(self.state, self.sound_switch, self.test_sound, self.show_main_menu))

    def play_roulette(self, e=None) -> None:
        if self.is_animating:
            return
        bet = self._read_bet(self.roulette_bet_field)
        if bet is None:
            self._replace_banner("roulette", self._error_result("Ставка должна быть положительным числом"))
            return
        if not BaseGame.can_make_bet(bet, self.state.player.balance):
            self._replace_banner("roulette", self._error_result("Недостаточно средств для ставки"))
            return
        try:
            bet_value = self._read_roulette_value()
            game = RouletteGame(bet, self.roulette_bet_type, bet_value)
        except ValueError as error:
            self._replace_banner("roulette", self._error_result(str(error)))
            return
        self.page.run_task(self._animate_roulette_round, game)

    def play_slots(self, e=None) -> None:
        if self.is_animating:
            return
        bet = self._read_bet(self.slots_bet_field)
        if bet is None:
            self._replace_banner("slots", self._error_result("Ставка должна быть положительным числом"))
            return
        if not BaseGame.can_make_bet(bet, self.state.player.balance):
            self._replace_banner("slots", self._error_result("Недостаточно средств для ставки"))
            return
        game = SlotsGame(bet)
        self.page.run_task(self._animate_slots_round, game)

    def select_roulette_number(self, value: int) -> None:
        self.roulette_bet_type = "number"
        self.roulette_bet_value = value
        self.roulette_value_field.value = str(value)
        self._update_roulette_controls()
        self.page.update()

    def select_roulette_color(self, value: str) -> None:
        self.roulette_bet_type = "color"
        self.roulette_bet_value = value
        self.roulette_value_field.value = value
        self._update_roulette_controls()
        self.page.update()

    def select_roulette_even_odd(self, value: str) -> None:
        self.roulette_bet_type = "even_odd"
        self.roulette_bet_value = value
        self.roulette_value_field.value = value
        self._update_roulette_controls()
        self.page.update()

    async def _animate_roulette_round(self, game: RouletteGame) -> None:
        self.is_animating = True
        self.sound_service.start_roulette_spin()
        try:
            result = game.play_round()
            target_angle = roulette_angle_for_number(result["number"])
            start_angle = self._current_ball_angle()
            finish_angle = self._build_finish_angle(start_angle, target_angle)
            duration = self._roulette_spin_duration_seconds()
            steps = max(24, int(duration * 60))

            for step in range(steps + 1):
                progress = step / steps
                eased = 1 - pow(1 - progress, 3)
                angle = start_angle + (finish_angle - start_angle) * eased
                radius = ROULETTE_BALL_START_RADIUS + (ROULETTE_BALL_END_RADIUS - ROULETTE_BALL_START_RADIUS) * eased
                move_ball(self.roulette_ball, angle, radius)

                live_number = roulette_number_for_angle(angle)
                live_color = RouletteGame.get_number_color(live_number)
                self.roulette_number_text.value = str(live_number)
                self.roulette_number_text.color = self._roulette_color_hex(live_color)
                self.roulette_selected_number_text.value = f"Шарик на числе: {live_number}"
                self.page.update()
                await asyncio.sleep(duration / steps)

            move_ball(self.roulette_ball, target_angle, ROULETTE_BALL_END_RADIUS)
            self.roulette_number_text.value = str(result["number"])
            self.roulette_number_text.color = self._roulette_color_hex(result["color"])
            self.roulette_selected_number_text.value = (
                f"Шарик на числе: {result['number']} ({self._translate_color(result['color'])})"
            )
            self._save_game_result(result)
            self._replace_banner("roulette", build_result_banner(result))
            self.sound_service.play_result(result["is_win"])
            self.page.update()
        except Exception as error:
            self._replace_banner("roulette", self._error_result(f"Ошибка раунда: {error}"))
            self.page.update()
        finally:
            self.sound_service.stop_roulette_spin()
            self.is_animating = False

    async def _animate_slots_round(self, game: SlotsGame) -> None:
        self.is_animating = True
        self.sound_service.start_slots_spin()
        try:
            steps = 22
            delay = 0.055
            symbol_keys = list(self.SLOT_SYMBOLS.keys())

            for step in range(steps):
                for index, text_control in enumerate(self.slots_text_controls):
                    symbol_key = random.choice(symbol_keys)
                    text_control.value = self.SLOT_SYMBOLS[symbol_key]
                    self.slots_reels[index].scale = 1.02 if step % 2 == 0 else 0.98
                    self.slots_reels[index].rotate = 0.01 if step % 2 == 0 else -0.01
                self.page.update()
                await asyncio.sleep(delay)

            result = game.play_round()
            for index, symbol_key in enumerate(result["reels"]):
                self.slots_text_controls[index].value = self.SLOT_SYMBOLS.get(symbol_key, symbol_key)
                self.slots_reels[index].scale = 1
                self.slots_reels[index].rotate = 0

            self._save_game_result(result)
            self._replace_banner("slots", build_result_banner(result))
            self.sound_service.play_result(result["is_win"])
            self.page.update()
        except Exception as error:
            self._replace_banner("slots", self._error_result(f"Ошибка раунда: {error}"))
            self.page.update()
        finally:
            self.sound_service.stop_slots_spin()
            self.is_animating = False

    def reset_statistics(self, e=None) -> None:
        self.state.statistics.reset()
        self.state_service.save_state(self.state)
        self.show_statistics()

    def change_sound(self, e) -> None:
        if e.control.value:
            self.state.settings.enable_sound()
            self.sound_service.play_click(force=True)
        else:
            self.state.settings.disable_sound()
        self.state_service.save_state(self.state)
        self.show_settings()

    def test_sound(self, e=None) -> None:
        self.sound_service.play_click(force=True)

    def _configure_page(self) -> None:
        self.page.title = APP_TITLE
        self.page.bgcolor = "#080d13"
        self.page.padding = 0
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window.maximized = True
        self.page.window.prevent_close = True
        self.page.window.on_event = self._on_window_event

    def _on_window_event(self, e) -> None:
        if getattr(e, "data", None) != "close":
            return
        self.close(e)

    def _set_view(self, control: ft.Control) -> None:
        self.page.clean()
        self.page.add(control)
        self.page.update()

    def _bet_field(self, label: str) -> ft.TextField:
        return ft.TextField(
            label=label,
            value="100",
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor="#0b1117",
            color="#f9fafb",
            border_color="#334155",
            focused_border_color="#22c55e",
        )

    def _read_bet(self, field: ft.TextField) -> int | None:
        try:
            value = int(field.value)
        except (TypeError, ValueError):
            return None
        return value if value > 0 else None

    def _read_roulette_value(self) -> int | str:
        raw_value = (self.roulette_value_field.value or "").strip().lower()
        if self.roulette_bet_type == "number":
            return int(raw_value)
        return raw_value

    def _update_roulette_controls(self) -> None:
        if self.roulette_bet_type == "number":
            text = f"Текущая ставка: число {self.roulette_bet_value}"
        elif self.roulette_bet_type == "color":
            text = f"Текущая ставка: цвет {self._translate_color(str(self.roulette_bet_value))}"
        else:
            text = f"Текущая ставка: {'четное' if self.roulette_bet_value == 'even' else 'нечетное'}"
        self.roulette_selected_bet_text.value = text

    def _save_game_result(self, result: dict) -> None:
        balance_change = int(result.get("balance_change", 0))
        self.state.update_balance(balance_change)
        self.state.record_game(result["is_win"], result["win_amount"])
        result["balance"] = self.state.player.balance
        self.state_service.save_state(self.state)
        self._refresh_balance_refs(self.roulette_balance_refs)
        self._refresh_balance_refs(self.slots_balance_refs)

    def _refresh_balance_refs(self, refs: dict[str, ft.Text]) -> None:
        if not refs:
            return
        refs["player"].value = self.state.player.login
        refs["balance"].value = str(self.state.player.balance)
        refs["games"].value = str(self.state.statistics.games_played)
        refs["wins"].value = str(self.state.statistics.wins)
        refs["total_win"].value = str(self.state.statistics.total_win)

    def _replace_banner(self, game_name: str, banner: ft.Container) -> None:
        target = self.roulette_result_banner if game_name == "roulette" else self.slots_result_banner
        target.bgcolor = banner.bgcolor
        target.border = banner.border
        target.content = banner.content
        target.padding = banner.padding
        target.border_radius = banner.border_radius
        target.animate = banner.animate

    def _error_result(self, message: str) -> ft.Container:
        return build_result_banner(
            {
                "is_win": False,
                "bet": 0,
                "win_amount": 0,
                "balance": self.state.player.balance,
            }
        ) if False else ft.Container(
            padding=18,
            border_radius=8,
            bgcolor="#321308",
            border=ft.border.all(1, "#ea580c"),
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ERROR_OUTLINE, size=32, color="#fb923c"),
                    ft.Text(message, size=14, color="#f9fafb", expand=True),
                ],
                spacing=14,
            ),
        )

    def _roulette_color_hex(self, color: str) -> str:
        if color == "red":
            return "#ef4444"
        if color == "black":
            return "#f9fafb"
        return "#22c55e"

    def _translate_color(self, color: str) -> str:
        mapping = {
            "red": "красный",
            "black": "черный",
            "green": "зеленый",
        }
        return mapping.get(color, color)

    def _current_ball_angle(self) -> float:
        center_x = (self.roulette_ball.left or 0) + 9 - 210
        center_y = (self.roulette_ball.top or 0) + 9 - 210
        return math.atan2(center_y, center_x)

    def _build_finish_angle(self, start_angle: float, target_angle: float) -> float:
        full_turn = math.pi * 2
        delta = (target_angle - start_angle) % full_turn
        extra_turns = max(1, int(ROULETTE_SPIN_EXTRA_TURNS))
        return start_angle + delta + full_turn * extra_turns

    def _roulette_spin_duration_seconds(self) -> float:
        try:
            value = float(ROULETTE_SPIN_DURATION_SECONDS)
        except (TypeError, ValueError):
            value = 1.16
        if value <= 0:
            return 1.16
        return value

    def close(self, e=None) -> None:
        if self.is_closing or self.is_closed:
            return
        self.is_closing = True
        try:
            if self.db is not None:
                self.state_service.save_state(self.state)
            self.log_service.save_session()
            self.sound_service.close()
            if self.db is not None:
                self.db.close()
                self.db = None
            self.is_closed = True
        finally:
            self.page.run_task(self._destroy_window)

    async def _destroy_window(self) -> None:
        try:
            await self.page.window.destroy()
        finally:
            self.is_closing = False
