import math # математика нужна чтобы считать движение шарика по кругу
import flet as ft

from games.roulette_game import RouletteGame 
from models.app_state import AppState 
from settings import Config as cfg 
from ui.helpers import UI 


EUROPEAN_ORDER = cfg.ROULETTE_WHEEL_ORDER # порядок чисел на европейской рулетке
ROULETTE_WHEEL_SIZE = 360 # размер колеса рулетки
ROULETTE_WHEEL_CENTER = ROULETTE_WHEEL_SIZE / 2 # центр колеса тут будет 180
ROULETTE_BALL_SIZE = 14 # размер шарика
ROULETTE_BALL_RADIUS = ROULETTE_BALL_SIZE / 2 # радиус шарика
ROULETTE_BALL_START_RADIUS = 136.0 # радиус где шарик начинает крутиться
ROULETTE_BALL_END_RADIUS = 126.0 # радиус где шарик останавливается ближе к центру


def _build_roulette_view(
    state: AppState,
    bet_field: ft.TextField, # поле ввода ставки
    selected_bet_text: ft.Text, # текст выбранной ставки, например выбрано красное
    selected_number_text: ft.Text, # текст выпавшего числа
    wheel: ft.Stack, # готовое колесо рулетки
    result_banner: ft.Container, # баннер результата победа проигрыш ошибка
    on_spin,
    on_back,
    on_select_number, # функция выбора числа
    on_select_color, # функция выбора цвета
    on_select_even_odd, # функция выбора чет нечет
) -> ft.Container:
    return ft.Container(
        expand=True,
        bgcolor="#080d13", # ФОН ЭКРАНА РУЛЕТКИ
        alignment=ft.Alignment(0, 0), # всё содержимое по центру
        content=ft.Column( # Column ставит элементы сверху вниз
            width=1120, # ширина центральной части экрана рулетки
            controls=[
                UI.title_text("Рулетка"), # заголовок экрана
                UI.status_row(state), # строка с балансом, играми и победами
                ft.Row( # Row ставит элементы слева направо
                    controls=[
                        UI.panel(480, [wheel, result_banner]), # слева панель с колесом и баннером результата
                        _bet_panel( # справа панель выбора ставки
                            bet_field,
                            selected_bet_text,
                            selected_number_text,
                            on_spin,
                            on_back,
                            on_select_number,
                            on_select_color,
                            on_select_even_odd,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER, # колесо и панель ставки по центру
                    vertical_alignment=ft.CrossAxisAlignment.START, # оба блока начинаются сверху
                    spacing=20, # расстояние между колесом и панелью ставки
                    wrap=True, # если места мало то блоки переносятся вниз
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER, # выравнивание внутри Column по вертикали
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # выравнивание внутри Column по горизонтали
            spacing=18, # расстояние между заголовком, статусом и основным блоком
        ),
    )


def _build_roulette_wheel(number_text: ft.Text, ball: ft.Container) -> ft.Stack: # функция создаёт колесо рулетки
    return ft.Stack( # Stack позволяет класть элементы друг на друга
        width=ROULETTE_WHEEL_SIZE, # ширина колеса
        height=ROULETTE_WHEEL_SIZE, # высота колеса
        controls=[
            _circle(ROULETTE_WHEEL_SIZE, "#3b1111", "#7f1d1d"), # большой внешний круг рулетки
            ft.Container(left=30, top=30, content=_circle(300, "#10251d", "#f59e0b")), # внутренний круг
            *_wheel_pockets(), # звёздочка распаковывает список чисел на колесе
            ft.Container( # центральный круг где показывается выпавшее число
                left=120,
                top=120,
                width=120,
                height=120,
                border_radius=60,
                bgcolor="#111827",
                border=ft.border.all(3, "#f59e0b"),
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    controls=[
                        ft.Text("Выпало", size=cfg.BODY_TEXT_SIZE, color="#d1d5db"), # подпись
                        number_text, # само число которое меняется во время вращения
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
            ),
            ball, # шарик рулетки
        ],
    )


def _bet_panel(
    bet_field: ft.TextField, # поле ставки
    selected_bet_text: ft.Text, # выбранная ставка
    selected_number_text: ft.Text, # выпавшее число
    on_spin,
    on_back,
    on_select_number,
    on_select_color,
    on_select_even_odd,
) -> ft.Container:
    spin_button = UI.primary_button("Крутить", ft.Icons.PLAY_ARROW, on_spin)
    home_button = UI.secondary_button("Домой", ft.Icons.HOME, on_back)
    spin_button.expand = True # кнопка крутить растягивается в строке
    home_button.expand = True # кнопка домой тоже растягивается в строке

    return UI.panel(
        460, # ширина панели ставки
        [
            UI.title_text("Ставка", cfg.TITLE_TEXT_SIZE), # заголовок панели
            bet_field, # поле куда вводится ставка
            ft.Container( # блок с выбранной ставкой и выпавшим числом
                padding=10,
                border_radius=8,
                bgcolor="#0b1117",
                content=ft.Column(
                    controls=[selected_bet_text, selected_number_text],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                ),
            ),
            _bet_row( # строка выбора цвета
                [
                    ("Красное", "#dc2626", RouletteGame.RED), # кнопка красное
                    ("Черное", "#020617", RouletteGame.BLACK), # кнопка черное
                ],
                on_select_color,
            ),
            _bet_row( # строка выбора чет нечет
                [
                    ("Чет", "#2563eb", RouletteGame.EVEN),
                    ("Нечет", "#7c3aed", RouletteGame.ODD),
                ],
                on_select_even_odd,
            ),
            _number_board(on_select_number), # поле со всеми числами рулетки
            ft.Row(controls=[spin_button, home_button], spacing=12), # строка с кнопками крутить и домой
        ],
    )


def _number_board(on_select_number) -> ft.Container: # функция создаёт доску с числами рулетки
    rows = [_number_row([cfg.ROULETTE_MIN_NUMBER], on_select_number)] # первая строка только с 0
    rows += [
        _number_row(
            range(start, min(start + 12, cfg.ROULETTE_MAX_NUMBER + 1)), on_select_number
        )
        for start in range(1, cfg.ROULETTE_MAX_NUMBER + 1, 12)
    ] # дальше числа идут строками по 12 штук

    return ft.Container(
        padding=10,
        border_radius=8,
        bgcolor="#0b1117",
        content=ft.Column(controls=rows, spacing=5), # строки чисел идут сверху вниз
    )


def _number_row(numbers, on_select_number) -> ft.Row: # функция создаёт одну строку чисел
    return ft.Row(
        controls=[_number_chip(number, on_select_number) for number in numbers], # для каждого числа создаётся кнопка
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=6, # расстояние между числами
    )


def _number_chip(number: int, on_select_number) -> ft.Container: # одна кнопка числа
    return UI.click_box(
        str(number), # текст на кнопке это число
        _pocket_color(number), # цвет кнопки зависит от числа
        lambda e: on_select_number(number), # при нажатии выбирается это число
        width=100 if number == cfg.ROULETTE_MIN_NUMBER else 30, # 0 шире остальных чисел
        height=32,
    )


def _bet_row(items: list[tuple[str, str, str]], on_select) -> ft.Row: # функция создаёт строку кнопок ставки
    return ft.Row(
        controls=[
            UI.click_box(
                title, color, lambda e, value=value: on_select(value), expand=True
            ) # создаёт кликабельную кнопку типа красное черное чет нечет
            for title, color, value in items
        ],
        spacing=12,
    )


def _build_roulette_ball() -> ft.Container: # создаётся шарик рулетки
    return ft.Container(
        left=ROULETTE_WHEEL_CENTER - ROULETTE_BALL_RADIUS, # стартовая позиция шарика по X
        top=ROULETTE_WHEEL_CENTER - ROULETTE_BALL_RADIUS, # стартовая позиция шарика по Y
        width=ROULETTE_BALL_SIZE,
        height=ROULETTE_BALL_SIZE,
        border_radius=ROULETTE_BALL_RADIUS, # делает шарик круглым
        bgcolor="#f9fafb", # белый цвет шарика
    )


def _move_ball(
    ball: ft.Container, angle: float, radius: float = ROULETTE_BALL_START_RADIUS
) -> None: # двигает шарик по кругу
    x = ROULETTE_WHEEL_CENTER + math.cos(angle) * radius # позиция шарика по X
    y = ROULETTE_WHEEL_CENTER + math.sin(angle) * radius # позиция шарика по Y
    ball.left = x - ROULETTE_BALL_RADIUS # задаём шарик левее на его радиус
    ball.top = y - ROULETTE_BALL_RADIUS # задаём шарик выше на его радиус


def _roulette_angle_for_number(number: int) -> float: # функция считает угол для конкретного числа
    return -math.pi / 2 + (math.pi * 2 / len(EUROPEAN_ORDER)) * EUROPEAN_ORDER.index(
        number
    ) # нужно чтобы понять где на колесе находится число


def _roulette_number_for_angle(angle: float) -> int: # функция по углу понимает какое число сейчас под шариком
    pocket_size = math.pi * 2 / len(EUROPEAN_ORDER) # размер одного сектора рулетки
    index = round(((angle + math.pi / 2) % (math.pi * 2)) / pocket_size) % len(
        EUROPEAN_ORDER
    ) # число в порядке рулетки
    return EUROPEAN_ORDER[index] # возвращаем число по индексу


def _wheel_pockets() -> list[ft.Container]: # функция создаёт маленькие числа вокруг колеса
    pockets = [] # сюда складываются все числа на колесе
    for number in EUROPEAN_ORDER: # проходим по всем числам рулетки в правильном порядке
        angle = _roulette_angle_for_number(number) # считаем угол где должно стоять число
        x = ROULETTE_WHEEL_CENTER + math.cos(angle) * 150 # позиция числа по X
        y = ROULETTE_WHEEL_CENTER + math.sin(angle) * 150 # позиция числа по Y
        pockets.append(
            ft.Container(
                left=x - 13,
                top=y - 13,
                content=UI.click_box(
                    str(number), _pocket_color(number), None, width=26, height=26
                ), # число на колесе. тут None потому что эти числа не нажимаются
            )
        )
    return pockets


def _circle(size: int, color: str, border_color: str) -> ft.Container: # функция создаёт круг
    return ft.Container(
        width=size,
        height=size,
        border_radius=size / 2, # если радиус половина размера, получится круг
        bgcolor=color, # цвет круга
        border=ft.border.all(4, border_color), # рамка круга
    )


def _pocket_color(number: int) -> str: # функция выбирает цвет числа
    if number == cfg.ROULETTE_MIN_NUMBER:
        return "#16a34a" # 0 зелёный
    return "#dc2626" if number in RouletteGame.RED_NUMBERS else "#020617" # красные числа красные а остальные черные


class RouletteView: # класс-обёртка для экрана рулетки
    build = staticmethod(_build_roulette_view)
    build_wheel = staticmethod(_build_roulette_wheel)
    build_ball = staticmethod(_build_roulette_ball)
    move_ball = staticmethod(_move_ball)
    angle_for_number = staticmethod(_roulette_angle_for_number)
    number_for_angle = staticmethod(_roulette_number_for_angle)