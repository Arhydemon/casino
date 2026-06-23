import flet as ft

from models.app_state import AppState # AppState хранит игрока, баланс, статистику и настройки
from models.game_result import GameResult # GameResult хранит результат сыгранного раунда
from settings import Config as cfg

# кнопка по типу крутить
def primary_button(text: str , # надпись на кнопке
                    icon, # иконка кнопки
                    on_click) -> ft.ElevatedButton: # при нажатии
    return ft.ElevatedButton( # создаёт и возвращает главную зелёную кнопку
        # ElevatedButton обычная кнопка с заливкой
        content=_button_text(text, "#ffffff"),
        icon=icon,
        height=42,
        bgcolor="#16a34a",
        color="#ffffff",
        on_click=on_click, # функция возврата в меню
    ) # функция только создаёт объект кнопки, на экран НЕ ДОБАВЛЯЕТ

# кнопка домой
def secondary_button(text: str, icon, on_click) -> ft.OutlinedButton: # КНОПКА С РАМКОЙ, НО БЕЗ ЗАЛИВКИ
    return ft.OutlinedButton(
        content=_button_text(text, "#d1d5db"),
        icon=icon,
        height=42,
        style=ft.ButtonStyle(color="#d1d5db", side=ft.BorderSide(1, "#334155")),
        on_click=on_click, 
    ) # функция только создаёт объект кнопки, на экран НЕ ДОБАВЛЯЕТ


def title_text(text: str, size: int | None = None) -> ft.Text: # СОЗДАЁТ ЗАГОЛОВКИ по типу казик слоты ставка рулетка
    return ft.Text( 
        text, # текст, который будет показан на экране
        size=size or cfg.TITLE_TEXT_SIZE + 8,
        weight=ft.FontWeight.BOLD, # жирный шрифт
        color="#f9fafb",
        text_align=ft.TextAlign.CENTER, # выравниваем сам текст по центру, впринципе ниче не поменяется даже если влево вправо прописать
    )


def panel(width: int, controls: list[ft.Control]) -> ft.Container: # СОЗДАЁТ ОБЩУЮ ТЁМНУЮ ПАНЕЛЬ!
    return ft.Container( # Container - прямоугольный блок-обёртка
    # в слотах это правая панель: Ставка, поле ввода, Крутить, Домой
    # в рулетке это: левая панель с колесом и результатом ну и правая панель с выбором ставки
        width=width,
        padding=16, # внутренний отступ от краёв панели
        border_radius=8, # закругление углов
        bgcolor="#111827",
        border=ft.border.all(1, "#263244"), # рамка со всех сторон. толщина + цвет
        content=ft.Column( # Container принимает один content, а Column содержит уже много элементов
            controls=controls, # список элементов, переданный в panel()
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # элементы по центру панели горизонтально
            spacing=12, # расстояние между элементами по вертикали
        ),
    )


def click_box( # СОЗДАЁТ ЦВЕТНОЙ НАЖИМАЕМЫЙ ПРЯМОУГОЛЬНИК! используется только на экране рулетки: все кнопки там чисел и тд, + рисует числа на колесе
    text: str,
    color: str,
    on_click,
    width: int | None = None,
    height: int = 40,
    expand: bool = True, # растягивать по свободной ширине или нет
) -> ft.Container:
    return ft.Container(
        width=width,
        height=height,
        expand=expand,
        border_radius=8,
        bgcolor=color,
        alignment=ft.Alignment(0, 0),
        # текст находится по центру блока: первое центр по горизонтали, второе центр по вертикали
        ink=on_click is not None, # включает визуальный эффект нажатия
        on_click=on_click,
        content=ft.Text(
            text,
            size=cfg.BODY_TEXT_SIZE,
            color="#f9fafb",
            weight=ft.FontWeight.BOLD,
        ),
    )


def status_row(state: AppState) -> ft.Row: # СОЗДАЁТ СТРОКУ СО СТАТИСТИКОЙ!
    # показывается: в главном меню, на экране слотов, на экране рулетки. выглядит как [баланс] [игр] [побед] [выигрыш]
    return ft.Row( # Row располагает элементы горизонтально
        controls=[
            _metric("баланс", state.player.balance, ft.Icons.PAID),
            _metric("игр", state.statistics.games_played, ft.Icons.SPORTS_ESPORTS),
            _metric("побед", state.statistics.wins, ft.Icons.EMOJI_EVENTS),
            _metric("выигрыш", state.statistics.total_win, ft.Icons.TRENDING_UP),
        ],
        alignment=ft.MainAxisAlignment.CENTER, # все блоки располагаются по центру строки
        spacing=12, # расстояние между блоками
        wrap=True, # если блоки не помещаются по ширине то они переходят на следующую строку
    )


def result_banner(result: GameResult | None) -> ft.Container: # СОЗДАЁТ БАННЕР С РЕЗУЛЬТАТОМ ИГРЫ! показывается под рулеткой и слотами
    if result is None: # до первой игры показывается синий текст
        text = "Сделай ставку"
        color = "#60a5fa" 
    elif result.is_win: # при победе показываем зелёный текст
        text = f"Победа: +{result.win_amount} | баланс: {result.balance}" 
        color = "#22c55e"
    else:
        text = f"Минус ставка: {result.bet} | баланс: {result.balance}"
        color = "#f97316" # при проигрыше показываем оранжевый текст

    return message_banner(text, color) # сам прямоугольник создаёт message_banner()
    # сюда передаём ТОЛЬКО готовый текст и цвет


def message_banner(text: str, color: str = "#f97316") -> ft.Container: # СОЗДАЁТ ПРЯМОУГОЛЬНИК С СООБЩЕНИЕМ!
    return ft.Container(
        # result_banner() использует его для результатов,
        # app_view.py использует его для ошибок: денег не хватает, ставка должна быть положительной, ошибка раунда
        height=46,
        padding=12,
        border_radius=8,
        bgcolor="#111827",
        border=ft.border.all(1, color), # рамка принимает цвет сообщения
        alignment=ft.Alignment(0, 0), # текст по центру блока
        content=ft.Text(
            text,
            size=cfg.BODY_TEXT_SIZE,
            color=color,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        ),
    )


def _metric(label: str, value: int, icon) -> ft.Container: # СОЗДАЁТ ОДИН МАЛЕНЬКИЙ БЛОК СТАТИСТИКИ! под названием
    # название, баланс, игр, побед или выигрыш
    return ft.Container(
        width=140,
        height=38,
        border_radius=8,
        bgcolor="#111827",
        border=ft.border.all(1, "#263244"),
        alignment=ft.Alignment(0, 0),
        content=ft.Row(
            controls=[
                ft.Icon(icon, size=16, color="#fa60e3"),
                ft.Text(f"{label}: {value}", size=cfg.BODY_TEXT_SIZE, color="#f9fafb"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
    )


def _button_text(text: str, color: str) -> ft.Text: # СОЗДАЁТ ТЕКСТ ВНУТРИ КНОПОК!
    return ft.Text(
    # используется в primary_button() и secondary_button() чтобы не повторять одни настройки текста
        text,
        size=cfg.BODY_TEXT_SIZE,
        color=color,
        weight=ft.FontWeight.BOLD,
    )


class UI: # СОБИРАЕТ ВСЕ ЗАГОТОВКИ ИНТЕРФЕЙСА!
    # позволяет писать UI.primary_button() вместо импорта каждой функции
    # staticmethod означает, что объект UI создавать не нужно. по типу
    # UI.primary_button(...) а не ui = UI() ui.primary_button(...)
    # по типу button = UI.primary_button("Крутить", ft.Icons.PLAY_ARROW, on_play)
    primary_button = staticmethod(primary_button) # зелёная кнопка крутить
    secondary_button = staticmethod(secondary_button) # кнопка домой с рамкой
    title_text = staticmethod(title_text) # заголовки экранов и панелей
    panel = staticmethod(panel) # тёмные панели рулетки и слотов
    click_box = staticmethod(click_box) # кнопки выбора ставки в рулетке
    status_row = staticmethod(status_row) # строка баланса и статистики
    result_banner = staticmethod(result_banner) # результат победы или проигрыша
    message_banner = staticmethod(message_banner) # сообщения об ошибках