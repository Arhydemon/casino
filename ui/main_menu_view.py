import flet as ft

from models.app_state import AppState
from settings import Config as cfg
from ui.helpers import UI


def _build_main_menu_view(
    state: AppState, # state нужен чтобы показать баланс и статистику игрока
    on_roulette, # это функция, которая сработает при нажатии на карточку рулетка
    on_slots, # функция для карточки слотов
    sound_switch: ft.Switch, # это переключатель звука
) -> ft.Container:
    return ft.Container(
        expand=True,
        bgcolor="#080d13", # ФОН ГЛАВНОГО МЕНЮ
        alignment=ft.Alignment(0, 0), # местоположения всего в главном экране
        content=ft.Column(
            width=820, # ширина центральной колонки
            controls=[
                ft.Row( # это строка она ставит элементы слева направо
                    controls=[_sound_toggle(sound_switch)], # тут в строке лежит только переключатель звука
                    alignment=ft.MainAxisAlignment.END, # END значит прижать вправо поэтому звук находится справа сверху
                ),
                UI.title_text(cfg.APP_MENU_TITLE, cfg.TITLE_TEXT_SIZE + 12), # заголовок главного меню
                UI.status_row(state), # строка со статусом игрока. показывается баланс, игр сыграно, побед
                ft.Row( # строка с карточками игр. внутри лежат две карточки: рулетка и слоты
                    controls=[
                        _game_card(
                            "Рулетка",
                            f"{cfg.ROULETTE_MIN_NUMBER}-{cfg.ROULETTE_MAX_NUMBER}", # тут показывает диапазон чисел рулетки, например 0-36
                            ft.Icons.CASINO, # ВСТРОЕННЫЕ ИКОНКИ ОТ ФЛЕТА
                            "#22c55e", # цвет карточки рулетки
                            on_roulette, # при нажатии открывается рулетка
                        ),
                        _game_card(
                            "Слоты",
                            f"x{cfg.SLOT_PAYTABLE.get(cfg.SLOT_REEL_COUNT, 0)}", # маленький текст с максимальным множителем слотов
                            ft.Icons.STARS,
                            "#f59e0b", # цвет карточки слотов
                            on_slots, # при нажатии открываются слоты
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER, # карточки выравниваются по центру строки
                    spacing=18, # КАРТОЧКИ БЛИЖЕ/ДАЛЬШЕ
                    wrap=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER, # выравнивание элементов внутри Column по вертикали
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # выравнивание элементов внутри Column по горизонтали
            spacing=24, # расстояние между элементами главного меню: звук, заголовок, статус, карточки
        ),
    )


def _sound_toggle(sound_switch: ft.Switch) -> ft.Row: # эта функция собирает маленький блок звука в главном меню справа сверху
    return ft.Row(
        controls=[
            ft.Icon(ft.Icons.VOLUME_UP, size=20, color="#60a5fa"), # иконка громкости
            sound_switch,
        ],
        spacing=8, # расстояние между иконкой и переключателем
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def _game_card(title: str, badge: str, icon, color: str, on_click) -> ft.Container: # тут при нажатии на 1 из 2 вылазит нужная игра
    return ft.Container(
        width=300, # ширина карточки
        height=150, # высота карточки
        padding=20, # внутренний отступ чтобы текст и иконка не липли к краям карточки
        border_radius=8, # скругление углов карточки
        bgcolor="#111827",
        border=ft.border.all(1, "#263244"), # 1 это толщина
        ink=True, # ink=True даёт эффект клика
        on_click=on_click, # show_roulette или show_slots
        content=ft.Column( # внутри карточки элементы стоят сверху вниз: иконка название подпись
            controls=[
                ft.Icon(icon, size=36, color=color),
                ft.Text( # название карточки
                    title,
                    size=cfg.TITLE_TEXT_SIZE,
                    weight=ft.FontWeight.BOLD,
                    color="#f9fafb",
                ),
                ft.Text(
                    badge,
                    size=cfg.BODY_TEXT_SIZE,
                    color=color,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER, # элементы внутри карточки по центру вертикально
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # элементы внутри карточки по центру горизонтально
            spacing=8, # расстояние между иконкой, названием и подписью
        ),
    )


class MainMenuView: # класс-обёртка для главного меню
    build = staticmethod(_build_main_menu_view)
