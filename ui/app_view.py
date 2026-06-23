# Я РАСПИШУ ПОМИНУТНО КТО ГДЕ ****** *****

import asyncio # нужен для пауз в анимации, чтобы рулетка и слоты крутились постепенно
from contextlib import suppress # чтобы игнорировать ошибки при закрытии приложения
import inspect # нужен чтобы проверить можно ли ждать результат через await
import math 
import random 
import flet as ft 

from database.database_manager import DatabaseManager 
from games.base_game import BaseGame 
from games.roulette_game import RouletteGame
from games.slots_game import SlotsGame 
from models.game_result import GameResult 
from services.app_state_service import AppStateService 
from services.log_service import LogService 
from services.sound_service import SoundService 
from settings import Config as cfg 
from ui.helpers import UI 
from ui.main_menu_view import MainMenuView # экран главного меню
from ui.roulette_view import (
    ROULETTE_BALL_END_RADIUS, # радиус шарика в конце анимации
    ROULETTE_BALL_RADIUS, # радиус самого шарика
    ROULETTE_BALL_START_RADIUS, # радиус шарика в начале анимации
    ROULETTE_WHEEL_CENTER, # центр колеса рулетки
    RouletteView, # экран рулетки и функции шарика
)
from ui.slots_view import SlotsView # экран слотов


TEXT_PRIMARY = "#f9fafb" # основной цвет текста
TEXT_SECONDARY = "#d1d5db" # второстепенный цвет текста
TEXT_MUTED = "#9ca3af" # серый приглушенный текст
FIELD_BACKGROUND = "#0b1117" # фон поля ввода
FIELD_BORDER = "#334155" # рамка поля ввода
ACCENT_GREEN = "#136a33" # главный зеленый цвет

class CasinoApp:
    def __init__(self, page: ft.Page) -> None:
        self.page = page # page это главное окно приложения Flet
        self.db = DatabaseManager() # подключение к базе данных
        self.db.create_tables() # создаём таблицы если их ещё нет
        self.state_service = AppStateService(self.db) # сервис который соединяет AppState и БД
        self.state = self.state_service.load_state() # загружаем игрока, статистику и настройки из БД
        self.log_service = LogService(self.state.player.login) # лог входа выхода по логину игрока
        self.sound_service = SoundService(self.state.settings) # звук зависит от настроек игрока
        self.user_objects = [
            self.db,
            self.state_service,
            self.state,
            self.state.player,
            self.state.statistics,
            self.state.settings,
            self.log_service,
            self.sound_service,
            self.state_service.profile_repository,
            self.state_service.statistics_repository,
            self.state_service.settings_repository,
        ] # список основных объектов проекта в логике ниже почти не используется
        self.is_animating = False # True когда сейчас крутится рулетка или слоты
        self.is_closing = False # True когда приложение закрывается
        self.is_closed = False # True когда приложение уже закрыто
        self.roulette_bet_type = RouletteGame.NUMBER_BET # по умолчанию ставка в рулетке на число
        self.roulette_bet_value: int | str = cfg.ROULETTE_MIN_NUMBER # выбранное значение ставки, сначала 0
        self.roulette_number_text = ft.Text(
            str(cfg.ROULETTE_MIN_NUMBER),
            size=cfg.TITLE_TEXT_SIZE,
            weight=ft.FontWeight.BOLD,
            color=ACCENT_GREEN,
        ) # в центре рулетки показывает число
        self.roulette_selected_bet_text = ft.Text(
            f"выбрано: число {cfg.ROULETTE_MIN_NUMBER}",
            size=cfg.BODY_TEXT_SIZE,
            color=TEXT_SECONDARY,
        ) # что выбрал игрок
        self.roulette_selected_number_text = ft.Text(
            f"выпало: {cfg.ROULETTE_MIN_NUMBER}",
            size=cfg.BODY_TEXT_SIZE,
            color=TEXT_MUTED,
        ) # выпавшее число
        self.roulette_ball = RouletteView.build_ball() # создаём шарик рулетки
        RouletteView.move_ball(
            self.roulette_ball,
            RouletteView.angle_for_number(cfg.ROULETTE_MIN_NUMBER),
            ROULETTE_BALL_START_RADIUS,
        ) # ставим шарик на стартовую позицию
        self.roulette_wheel = RouletteView.build_wheel(
            self.roulette_number_text, self.roulette_ball
        ) # создаём колесо рулетки, внутрь передаём текст числа и шарик
        self.roulette_result_banner = UI.result_banner(None) # пустой баннер результата рулетки
        self.slots_result_banner = UI.result_banner(None) # пустой баннер результата слотов
        self.roulette_bet_field = self._bet_field("ставка") # поле ставки для рулетки
        self.slots_bet_field = self._bet_field("ставка") # поле ставки для слотов
        slot_symbol_keys = list(cfg.SLOT_SYMBOLS) # список ключей символов слотов
        initial_slot_symbols = [
            slot_symbol_keys[index % len(slot_symbol_keys)]
            for index in range(cfg.SLOT_REEL_COUNT)
        ] # начальные символы слотов чтобы барабаны не были пустые
        self.slots_text_controls = [
            ft.Text(
                cfg.SLOT_SYMBOLS[symbol_key],
                size=cfg.TITLE_TEXT_SIZE,
                text_align=ft.TextAlign.CENTER,
            )
            for symbol_key in initial_slot_symbols
        ] # тексты внутри барабанов, они меняются при прокрутке
        self.slots_reels = [
            SlotsView.build_reel(control) for control in self.slots_text_controls
        ] # создаём барабаны слотов и кладём внутрь текстовые символы
        self.sound_switch = ft.Switch(
            value=self.state.settings.sound_enabled,
            label="звук",
            label_text_style=ft.TextStyle(size=cfg.BODY_TEXT_SIZE),
            active_color=ACCENT_GREEN,
            on_change=self.change_sound,
        ) # переключатель звука в главном меню

    def run(self) -> None:
        self._configure_page() # настраиваем окно приложения
        self.show_main_menu() # сразу показываем главное меню

    def show_main_menu(self, e=None) -> None:
        self.sound_switch.value = self.state.settings.sound_enabled # обновляем переключатель звука из настроек
        self._set_view(
            MainMenuView.build(
                self.state,
                self.show_roulette,
                self.show_slots,
                self.sound_switch,
            )
        ) # ставим на экран главное меню

    def show_roulette(self, e=None) -> None:
        self._update_roulette_controls() # обновляем текст выбранной ставки
        self._set_view(
            RouletteView.build(
                self.state,
                self.roulette_bet_field,
                self.roulette_selected_bet_text,
                self.roulette_selected_number_text,
                self.roulette_wheel,
                self.roulette_result_banner,
                self.play_roulette,
                self.show_main_menu,
                lambda value: self.select_roulette_bet(RouletteGame.NUMBER_BET, value),
                lambda value: self.select_roulette_bet(RouletteGame.COLOR_BET, value),
                lambda value: self.select_roulette_bet(
                    RouletteGame.EVEN_ODD_BET, value
                ),
            )
        ) # ставим на экран рулетку

    def show_slots(self, e=None) -> None:
        self._set_view(
            SlotsView.build(
                self.state,
                self.slots_bet_field,
                self.slots_reels,
                self.slots_result_banner,
                self.play_slots,
                self.show_main_menu,
            )
        ) # ставим на экран слоты

    def play_roulette(self, e=None) -> None:
        if self.is_animating or self.is_closing:
            return # если уже идёт анимация или приложение закрывается, ничего не делаем
        bet = self._read_bet(self.roulette_bet_field) # читаем ставку из поля ввода
        if bet is None:
            self.roulette_result_banner = UI.message_banner(
                "ставка должна быть положительной"
            )
            self.show_roulette()
            return # если ставка плохая, показываем ошибку и выходим
        if not BaseGame.can_make_bet(bet, self.state.player.balance):
            self.roulette_result_banner = UI.message_banner("денег не хватает")
            self.show_roulette()
            return # если ставка больше баланса, показываем ошибку
        try:
            if self.roulette_bet_type == RouletteGame.NUMBER_BET:
                bet_value = int(self.roulette_bet_value) # для ставки на число нужно число int
            else:
                bet_value = str(self.roulette_bet_value) # для цвета/четности нужна строка
            game = RouletteGame(bet, self.roulette_bet_type, bet_value) # создаём объект игры рулетки
        except ValueError as error:
            self.roulette_result_banner = UI.message_banner(str(error))
            self.show_roulette()
            return # если RouletteGame ругнулась на ставку, показываем ошибку
        self.page.run_task(self._animate_roulette_round, game) # запускаем анимацию рулетки отдельно

    def play_slots(self, e=None) -> None:
        if self.is_animating or self.is_closing:
            return # если уже что-то крутится, второй раз не запускаем
        bet = self._read_bet(self.slots_bet_field) # читаем ставку из поля слотов
        if bet is None:
            self.slots_result_banner = UI.message_banner(
                "ставка должна быть положительной"
            )
            self.show_slots()
            return # ставка не число или меньше минимальной
        if not BaseGame.can_make_bet(bet, self.state.player.balance):
            self.slots_result_banner = UI.message_banner("денег не хватает")
            self.show_slots()
            return # денег на ставку не хватает
        game = SlotsGame(bet) # создаём объект игры слотов
        self.page.run_task(self._animate_slots_round, game) # запускаем анимацию слотов

    def select_roulette_bet(self, bet_type: str, value: int | str) -> None:
        self.roulette_bet_type = bet_type # сохраняем тип ставки, число/цвет/четность
        self.roulette_bet_value = value # сохраняем значение ставки
        self._update_roulette_controls() # обновляем текст выбранной ставки
        self.page.update() # обновляем интерфейс

    async def _animate_roulette_round(self, game: RouletteGame) -> None:
        self.is_animating = True # помечаем что анимация началась
        self.sound_service.start_spin() # запускаем звук прокрутки
        try:
            result = game.play_round() # тут рулетка реально считает результат игры
            target_angle = RouletteView.angle_for_number(result.number) # угол где находится выпавшее число
            start_angle = self._current_ball_angle() # текущий угол шарика
            finish_angle = self._build_finish_angle(start_angle, target_angle) # финальный угол с дополнительными кругами
            duration = float(cfg.ROULETTE_SPIN_DURATION_SECONDS) # сколько секунд крутится рулетка
            steps = max(
                cfg.ROULETTE_MIN_ANIMATION_STEPS,
                int(duration * cfg.ROULETTE_SPIN_FPS),
            ) # количество шагов анимации

            for step in range(steps + 1):
                if self.is_closing:
                    return # если приложение закрывают, выходим из анимации
                progress = step / steps # прогресс от 0 до 1
                eased = 1 - pow(1 - progress, cfg.ROULETTE_EASING_POWER) # плавное замедление
                angle = start_angle + (finish_angle - start_angle) * eased # новый угол шарика
                radius = (
                    ROULETTE_BALL_START_RADIUS
                    + (ROULETTE_BALL_END_RADIUS - ROULETTE_BALL_START_RADIUS) * eased
                ) # радиус шарика, он чуть сдвигается ближе к центру
                RouletteView.move_ball(self.roulette_ball, angle, radius) # двигаем шарик

                live_number = RouletteView.number_for_angle(angle) # число под шариком во время анимации
                live_color = RouletteGame.get_number_color(live_number) # цвет этого числа
                self.roulette_number_text.value = str(live_number) # меняем число в центре рулетки
                self.roulette_number_text.color = self._roulette_color_hex(live_color) # меняем цвет текста
                self.roulette_selected_number_text.value = f"выпало: {live_number}"
                self.page.update() # перерисовываем экран
                await asyncio.sleep(duration / steps) # маленькая пауза между кадрами

            RouletteView.move_ball(
                self.roulette_ball, target_angle, ROULETTE_BALL_END_RADIUS
            ) # ставим шарик точно на выпавшее число
            self.roulette_number_text.value = str(result.number) # финальное число
            self.roulette_number_text.color = self._roulette_color_hex(result.color) # финальный цвет числа
            self.roulette_selected_number_text.value = (
                f"выпало: {result.number} ({self._translate_color(result.color)})"
            ) # финальная подпись справа
            self._save_game_result(result) # сохраняем баланс, статистику и БД
            self.roulette_result_banner = UI.result_banner(result) # создаём баннер результата
            self.show_roulette() # перерисовываем экран рулетки
        except Exception as error:
            self.roulette_result_banner = UI.message_banner(f"ошибка раунда: {error}")
            self.show_roulette() # если ошибка, показываем её на экране
        finally:
            self.sound_service.stop_spin() # звук стопается всегда
            self.is_animating = False # анимация закончилась

    async def _animate_slots_round(self, game: SlotsGame) -> None:
        self.is_animating = True # помечаем что слоты крутятся
        self.sound_service.start_spin() # запускаем звук
        try:
            duration = float(cfg.SLOTS_SPIN_DURATION_SECONDS) # сколько секунд крутятся слоты
            steps = max(1, round(duration * cfg.SLOT_SPIN_STEPS_PER_SECOND)) # сколько шагов анимации
            delay = duration / steps # задержка между шагами
            symbol_keys = list(cfg.SLOT_SYMBOLS.keys()) # все возможные символы слотов

            for step in range(steps):
                if self.is_closing:
                    return # если приложение закрывается, выходим
                for index, text_control in enumerate(self.slots_text_controls):
                    symbol_key = random.choice(symbol_keys) # случайный символ для визуальной прокрутки
                    text_control.value = cfg.SLOT_SYMBOLS[symbol_key] # ставим символ в барабан
                    is_active_phase = step % cfg.SLOT_SPIN_PHASE_MODULO == 0 # чередование активного/обычного шага
                    self.slots_reels[index].scale = (
                        cfg.SLOT_REEL_SCALE_ACTIVE
                        if is_active_phase
                        else cfg.SLOT_REEL_SCALE_IDLE
                    ) # барабан то чуть увеличивается, то возвращается
                    self.slots_reels[index].rotate = (
                        cfg.SLOT_REEL_ROTATION_ACTIVE
                        if is_active_phase
                        else cfg.SLOT_REEL_ROTATION_IDLE
                    ) # барабан чуть наклоняется в разные стороны
                self.page.update() # обновляем экран
                await asyncio.sleep(delay) # пауза между кадрами

            result = game.play_round() # тут слоты реально считают результат игры
            for index, symbol_key in enumerate(result.reels):
                self.slots_text_controls[index].value = cfg.SLOT_SYMBOLS.get(
                    symbol_key, symbol_key
                ) # ставим финальные символы, которые реально выпали
                self.slots_reels[index].scale = cfg.SLOT_REEL_SCALE_IDLE # возвращаем обычный размер
                self.slots_reels[index].rotate = 0 # убираем наклон

            self._save_game_result(result) # сохраняем баланс, статистику и БД
            self.slots_result_banner = UI.result_banner(result) # создаём баннер результата
            self.show_slots() # перерисовываем экран слотов
        except Exception as error:
            self.slots_result_banner = UI.message_banner(f"ошибка раунда: {error}")
            self.show_slots() # если ошибка, показываем её
        finally:
            self.sound_service.stop_spin() # звук стопается всегда
            self.is_animating = False # анимация закончилась

    def change_sound(self, e) -> None:
        self.state.settings.sound_enabled = bool(e.control.value) # берём значение переключателя звука
        self.state_service.save_state(self.state) # сохраняем настройку звука в БД

    def _configure_page(self) -> None:
        self.page.title = cfg.APP_TITLE # заголовок окна приложения
        self.page.bgcolor = "#080d13" # фон окна
        self.page.padding = 0 # убираем стандартные отступы
        self.page.theme = ft.Theme(font_family=cfg.FONT_FAMILY) # шрифт приложения
        self.page.theme_mode = (
            ft.ThemeMode.DARK if cfg.THEME_MODE == "dark" else ft.ThemeMode.LIGHT
        ) # тёмная или светлая тема
        self.page.window.width = cfg.WINDOW_WIDTH # ширина окна
        self.page.window.height = cfg.WINDOW_HEIGHT # высота окна
        self.page.window.maximized = cfg.WINDOW_MAXIMIZED # открывать окно на весь экран или нет
        self.page.window.prevent_close = cfg.WINDOW_PREVENT_CLOSE # перехватывать закрытие окна или нет
        if cfg.WINDOW_PREVENT_CLOSE:
            self.page.window.on_event = self._on_window_event # если закрытие перехватывается, вешаем свой обработчик

    def _on_window_event(self, e) -> None:
        if getattr(e, "type", None) != ft.WindowEventType.CLOSE:
            return # если событие не закрытие окна, ничего не делаем
        self.close(e) # если это закрытие окна, запускаем своё закрытие

    def _set_view(self, control: ft.Control) -> None:
        self.page.clean() # очищаем текущий экран
        self.page.add(control) # добавляем новый экран
        self.page.update() # обновляем интерфейс

    def _bet_field(self, label: str) -> ft.TextField:
        return ft.TextField(
            label=label, # надпись внутри поля
            value=str(cfg.DEFAULT_BET), # ставка по умолчанию
            keyboard_type=ft.KeyboardType.NUMBER, # клавиатура под числа
            text_size=cfg.BODY_TEXT_SIZE, # размер текста
            label_style=ft.TextStyle(size=cfg.BODY_TEXT_SIZE), # размер label
            bgcolor=FIELD_BACKGROUND, # фон поля
            color=TEXT_PRIMARY, # цвет текста
            border_color=FIELD_BORDER, # цвет рамки
            focused_border_color=ACCENT_GREEN,
        ) # зелёная рамка когда поле выбрано

    def _read_bet(self, field: ft.TextField) -> int | None:
        try:
            value = int(field.value) # пытаемся превратить текст из поля в число
        except (TypeError, ValueError):
            return None # если там не число, возвращаем None
        return value if value >= cfg.MIN_BET else None # если ставка нормальная вернуть число, иначе None

    def _update_roulette_controls(self) -> None:
        if self.roulette_bet_type == RouletteGame.NUMBER_BET:
            text = f"выбрано: число {self.roulette_bet_value}" # если ставка на число
        elif self.roulette_bet_type == RouletteGame.COLOR_BET:
            text = f"выбрано: {self._translate_color(str(self.roulette_bet_value))}" # если ставка на цвет
        else:
            value = (
                "четное" if self.roulette_bet_value == RouletteGame.EVEN else "нечетное"
            ) # если ставка на чет/нечет
            text = f"выбрано: {value}"
        self.roulette_selected_bet_text.value = text # обновляем текст выбранной ставки

    def _save_game_result(self, result: GameResult) -> None:
        self.state.update_balance(result.balance_change) # меняем баланс игрока
        self.state.record_game(result.is_win, result.win_amount) # обновляем статистику
        result.balance = self.state.player.balance # записываем новый баланс в результат игры
        self.state_service.save_state(self.state) # сохраняем всё в БД

    def _roulette_color_hex(self, color: str) -> str:
        if color == RouletteGame.RED:
            return "#ef4444" # красный цвет для красных чисел
        if color == RouletteGame.BLACK:
            return TEXT_PRIMARY # почти белый цвет для чёрных чисел
        return ACCENT_GREEN # зелёный цвет для зеро

    def _translate_color(self, color: str) -> str:
        if color == RouletteGame.RED:
            return "красное"
        if color == RouletteGame.BLACK:
            return "черное"
        if color == RouletteGame.GREEN:
            return "зеро"
        return color # если цвет неизвестный, вернуть как есть

    def _current_ball_angle(self) -> float:
        center_x = (
            (self.roulette_ball.left or 0)
            + ROULETTE_BALL_RADIUS
            - ROULETTE_WHEEL_CENTER
        ) # X шарика относительно центра колеса
        center_y = (
            (self.roulette_ball.top or 0) + ROULETTE_BALL_RADIUS - ROULETTE_WHEEL_CENTER
        ) # Y шарика относительно центра колеса
        return math.atan2(center_y, center_x) # получаем угол шарика

    def _build_finish_angle(self, start_angle: float, target_angle: float) -> float:
        full_turn = math.pi * 2 # полный круг в радианах
        delta = (target_angle - start_angle) % full_turn # сколько надо докрутить до нужного числа
        extra_turns = max(1, int(cfg.ROULETTE_SPIN_EXTRA_TURNS)) # дополнительные круги перед остановкой
        return start_angle + delta + full_turn * extra_turns # итоговый угол остановки

    def close(self, e=None) -> None:
        if self.is_closing or self.is_closed:
            return # если уже закрываемся или закрылись, второй раз не запускаем
        self.page.run_task(self._close_async) # запускаем асинхронное закрытие

    async def _close_async(self) -> None:
        if self.is_closing or self.is_closed:
            return # защита от повторного закрытия
        self.is_closing = True # помечаем что закрытие началось
        try:
            with suppress(Exception):
                if self.db is not None:
                    self.state_service.save_state(self.state) # перед выходом сохраняем состояние в БД
            with suppress(Exception):
                self.log_service.save_session() # сохраняем лог сессии
            with suppress(Exception):
                self.sound_service.close() # закрываем звук
            with suppress(Exception):
                if self.db is not None:
                    self.db.close() # закрываем подключение к БД
                    self.db = None # убираем ссылку на БД
            self.is_closed = True # приложение закрыто
            self.page.window.prevent_close = False # разрешаем закрыть окно
            result = self.page.window.destroy() # уничтожаем окно
            if inspect.isawaitable(result):
                await result # если destroy вернул awaitable, ждём его
        finally:
            self.is_closing = False # закрытие закончилось