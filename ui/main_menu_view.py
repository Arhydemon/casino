import flet as ft

from models.app_state import AppState
from settings import Config as cfg
from ui.helpers import UI


def _build_slots_view(
    state: AppState, # state нужен чтобы показать баланс и статистику игрока
    bet_field: ft.TextField, # поле куда игрок вводит ставку
    reel_controls: list[ft.Container], # это барабаны слотов, их 3 штуки, можно менять, но больше 4 не влезает, если не подключать растяжку
    result_banner: ft.Container, # баннер результата там победа проигрыш ошибка
    on_play, # крутить
    on_back, # домой
) -> ft.Container:
    return ft.Container(
        expand=True,
        bgcolor="#080d13", # ФОН ЭКРАНА СЛОТОВ
        alignment=ft.Alignment(0, 0), # местоположение всего экрана слотов
        content=ft.Column( # Column ставит элементы сверху вниз
            width=920, # ширина центральной части экрана слотов
            controls=[
                UI.title_text("Слоты"), # заголовок экрана
                UI.status_row(state), # строка баланса и статистики игрока
                ft.Row( # Row ставит элементы слева направо
                    controls=[
                        _slot_machine(reel_controls, result_banner), # слева сам автомат с барабанами
                        _slot_panel(bet_field, on_play, on_back), # справа панель со ставкой и кнопками
                    ],
                    alignment=ft.MainAxisAlignment.CENTER, # автомат и панель по центру
                    vertical_alignment=ft.CrossAxisAlignment.START, # элементы начинаются сверху на одной линии
                    spacing=20, # расстояние между автоматом и панелью ставки
                    wrap=True, # если места мало, панель перенесётся вниз
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER, # выравнивание элементов внутри Column по вертикали
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # выравнивание элементов внутри Column по горизонтали
            spacing=18, # расстояние между заголовком, статусом и блоком игры
        ),
    )


def _build_reel(symbol_text: ft.Text) -> ft.Container: # функция создаёт один барабан слотов
    return ft.Container(
        width=108, # ширина одного барабана
        height=128, # высота одного барабана
        border_radius=8, # скругление углов барабана
        bgcolor="#f8fafc", # внешний светлый фон барабана
        border=ft.border.all(3, "#f59e0b"), # оранжевая рамка барабана. 3 это толщина
        alignment=ft.Alignment(0, 0), # символ внутри барабана по центру
        animate_scale=ft.Animation(180, ft.AnimationCurve.EASE_OUT), # анимация увеличения барабана при прокрутке
        animate_rotation=ft.Animation(180, ft.AnimationCurve.EASE_OUT), # анимация наклона барабана при прокрутке
        content=ft.Container( # внутреннее тёмное окошко барабана
            width=84, # ширина внутреннего окошка
            height=100, # высота внутреннего окошка
            border_radius=8, # скругление внутреннего окошка
            bgcolor="#0b1117", # фон внутри барабана
            alignment=ft.Alignment(0, 0), # символ по центру
            content=symbol_text, # сам символ слота внутри барабана
        ),
    )


def _slot_machine(
    reel_controls: list[ft.Container], result_banner: ft.Container
) -> ft.Container: # автомат слотов
    return ft.Container(
        width=500, # ширина автомата
        padding=16, # внутренний отступ автомата
        border_radius=8, # скругление углов автомата
        bgcolor="#4a0f0f", # красный фон автомата
        border=ft.border.all(3, "#f59e0b"), # оранжевая рамка автомата
        content=ft.Column( # внутри автомата элементы идут сверху вниз
            controls=[
                ft.Text(
                    "JACKPOT 777", # надпись сверху автомата
                    size=cfg.TITLE_TEXT_SIZE,
                    color="#f59e0b",
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Row( # строка с барабанами
                    controls=reel_controls, # сюда приходят ГОТОВЫЕ БАРАБАНЫ
                    alignment=ft.MainAxisAlignment.CENTER, # барабаны по центру
                    spacing=16, # расстояние между барабанами
                ),
                ft.Row( # строка с выплатами
                    controls=[
                        _payline("2 совпало", f"x{cfg.SLOT_PAYTABLE.get(2, 0)}"), # плашка выплаты за 2 совпадения
                        _payline("3 совпало", f"x{cfg.SLOT_PAYTABLE.get(3, 0)}"), # за 3
                    ],
                    alignment=ft.MainAxisAlignment.CENTER, # плашки выплат по центру
                    spacing=12, # расстояние между плашками выплат
                ),
                result_banner, # баннер результата после прокрутки
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # всё внутри автомата по центру
            spacing=12, # расстояние между надписью барабанами выплатами и баннером
        ),
    )


def _slot_panel(bet_field: ft.TextField, on_play, on_back) -> ft.Container: # правая панель со ставкой и кнопками
    return UI.panel(
        300, # ширина панели
        [
            UI.title_text("Ставка", cfg.TITLE_TEXT_SIZE), # заголовок панели
            bet_field, # поле ввода ставки
            UI.primary_button("Крутить", ft.Icons.PLAY_ARROW, on_play),
            UI.secondary_button("Домой", ft.Icons.HOME, on_back), # ну типа кнопка домой, че еще сказать то
        ],
    )


def _payline(label: str, value: str) -> ft.Container: # маленькуая плашку выплаты
    return ft.Container(
        width=130, # ширина плашки
        padding=ft.padding.symmetric(horizontal=12, vertical=8), # отступы внутри плашки слева/справа и сверху/снизу
        border_radius=8, # скругление углов плашки
        bgcolor="#111827", # фон плашки
        alignment=ft.Alignment(0, 0), # текст по центру
        content=ft.Text(
            f"{label}: {value}", # текст типа 2 совпало: x2
            size=cfg.BODY_TEXT_SIZE,
            color="#f59e0b",
            weight=ft.FontWeight.BOLD,
        ),
    )


class SlotsView: # класс-обёртка для экрана слотов по аналогии с предыдущими
    build = staticmethod(_build_slots_view)
    build_reel = staticmethod(_build_reel)
