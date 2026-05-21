import math
import flet as ft
from games.roulette_game import RouletteGame
from models.app_state import AppState
from ui.components.action_buttons import primary_button, secondary_button
from ui.components.balance_panel import build_balance_panel
from ui.components.game_header import build_game_header

EUROPEAN_ORDER = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26,
]

def build_roulette_view(
    state: AppState,
    balance_refs: dict,
    bet_field: ft.TextField,
    roulette_value_field: ft.TextField,
    selected_bet_text: ft.Text,
    selected_number_text: ft.Text,
    wheel: ft.Stack,
    result_banner: ft.Container,
    on_spin,
    on_back,
    on_select_number,
    on_select_color,
    on_select_even_odd,
) -> ft.Container:
    return ft.Container(
        expand=True,
        padding=30,
        bgcolor="#080d13",
        content=ft.Column(
            controls=[
                build_game_header("Рулетка", "Казино стол, колесо и быстрые ставки", on_back),
                build_balance_panel(state, balance_refs),
                ft.Row(
                    controls=[
                        _roulette_stage(wheel, result_banner),
                        _bet_panel(
                            bet_field,
                            roulette_value_field,
                            selected_bet_text,
                            selected_number_text,
                            on_spin,
                            on_back,
                            on_select_color,
                            on_select_even_odd,
                        ),
                    ],
                    spacing=20,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                _number_board(on_select_number),
            ],
            spacing=22,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

def build_roulette_wheel(number_text: ft.Text, ball: ft.Container) -> ft.Stack:
    pockets = _wheel_pockets()
    return ft.Stack(
        width=420,
        height=420,
        controls=[
            ft.Container(
                width=420,
                height=420,
                border_radius=210,
                bgcolor="#3f2b1d",
                border=ft.border.all(8, "#9a6b2f"),
                shadow=ft.BoxShadow(blur_radius=28, color="#020617", offset=ft.Offset(0, 16)),
            ),
            ft.Container(
                left=18,
                top=18,
                width=384,
                height=384,
                border_radius=192,
                bgcolor="#1f2937",
                border=ft.border.all(5, "#d4af37"),
            ),
            *pockets,
            ft.Container(
                left=110,
                top=110,
                width=200,
                height=200,
                border_radius=100,
                bgcolor="#111827",
                border=ft.border.all(6, "#d4af37"),
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    controls=[
                        ft.Text("LIVE WHEEL", size=16, color="#d1d5db", text_align=ft.TextAlign.CENTER),
                        number_text,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
            ),
            ball,
        ],
    )

def _roulette_stage(wheel: ft.Stack, result_banner: ft.Container) -> ft.Container:
    return ft.Container(
        expand=True,
        padding=26,
        border_radius=8,
        bgcolor="#111827",
        border=ft.border.all(1, "#263244"),
        shadow=ft.BoxShadow(blur_radius=34, color="#020617", offset=ft.Offset(0, 16)),
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[wheel],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                result_banner,
            ],
            spacing=18,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

def _bet_panel(
    bet_field: ft.TextField,
    roulette_value_field: ft.TextField,
    selected_bet_text: ft.Text,
    selected_number_text: ft.Text,
    on_spin,
    on_back,
    on_select_color,
    on_select_even_odd,
) -> ft.Container:
    return ft.Container(
        width=380,
        padding=22,
        border_radius=8,
        bgcolor="#111827",
        border=ft.border.all(1, "#263244"),
        shadow=ft.BoxShadow(blur_radius=24, color="#020617", offset=ft.Offset(0, 12)),
        content=ft.Column(
            controls=[
                ft.Text("Поле ставок", size=20, weight=ft.FontWeight.BOLD, color="#f9fafb"),
                selected_bet_text,
                selected_number_text,
                bet_field,
                roulette_value_field,
                ft.Text("Купюры и фишки", size=15, weight=ft.FontWeight.BOLD, color="#f9fafb"),
                ft.Text(
                    "Можно выбрать ставку на поле слева или вручную через форму.",
                    size=13,
                    color="#9ca3af",
                ),
                ft.Row(
                    controls=[
                        _outside_bet("Красное", "#b91c1c", lambda e: on_select_color("red")),
                        _outside_bet("Черное", "#111827", lambda e: on_select_color("black")),
                    ],
                    spacing=12,
                ),
                ft.Row(
                    controls=[
                        _outside_bet("Четное", "#1d4ed8", lambda e: on_select_even_odd("even")),
                        _outside_bet("Нечетное", "#7c3aed", lambda e: on_select_even_odd("odd")),
                    ],
                    spacing=12,
                ),
                primary_button("Крутить рулетку", ft.Icons.PLAY_ARROW, on_spin),
                secondary_button("В меню", ft.Icons.HOME, on_back),
            ],
            spacing=14,
        ),
    )

def _number_board(on_select_number) -> ft.Container:
    rows: list[ft.Row] = [
        ft.Row(
            controls=[_zero_chip(on_select_number)],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    ]
    for start in range(1, 37, 3):
        controls = [_number_chip(number, on_select_number) for number in range(start, start + 3)]
        rows.append(
            ft.Row(
                controls=controls,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            )
        )
    return ft.Container(
        padding=18,
        border_radius=8,
        bgcolor="#111827",
        border=ft.border.all(1, "#263244"),
        content=ft.Column(
            controls=rows,
            spacing=10,
        ),
    )

def _zero_chip(on_select_number) -> ft.Container:
    return ft.Container(
        width=320,
        height=54,
        border_radius=8,
        bgcolor="#166534",
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=lambda e: on_select_number(0),
        content=ft.Text("0", size=20, weight=ft.FontWeight.BOLD, color="#f9fafb"),
    )

def _number_chip(number: int, on_select_number) -> ft.Container:
    color = "#b91c1c" if number in RouletteGame.RED_NUMBERS else "#111827"
    return ft.Container(
        width=100,
        height=56,
        border_radius=8,
        bgcolor=color,
        border=ft.border.all(1, "#334155"),
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=lambda e: on_select_number(number),
        content=ft.Text(str(number), size=18, weight=ft.FontWeight.BOLD, color="#f9fafb"),
    )

def _outside_bet(title: str, color: str, on_click) -> ft.Container:
    return ft.Container(
        expand=True,
        height=52,
        border_radius=8,
        bgcolor=color,
        border=ft.border.all(1, "#334155"),
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=on_click,
        content=ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color="#f9fafb"),
    )

def build_roulette_ball() -> ft.Container:
    return ft.Container(
        left=200,
        top=24,
        width=18,
        height=18,
        border_radius=9,
        bgcolor="#f8fafc",
        border=ft.border.all(2, "#cbd5e1"),
        shadow=ft.BoxShadow(blur_radius=12, color="#e2e8f0", offset=ft.Offset(0, 0)),
    )

def move_ball(ball: ft.Container, angle: float, radius: float = 158.0) -> None:
    center = 210
    x = center + math.cos(angle) * radius
    y = center + math.sin(angle) * radius
    ball.left = x - 9
    ball.top = y - 9

def roulette_angle_for_number(number: int) -> float:
    pocket_size = (math.pi * 2) / len(EUROPEAN_ORDER)
    index = EUROPEAN_ORDER.index(number)
    return -math.pi / 2 + pocket_size * index

def roulette_number_for_angle(angle: float) -> int:
    pocket_size = (math.pi * 2) / len(EUROPEAN_ORDER)
    normalized = (angle + math.pi / 2) % (math.pi * 2)
    index = round(normalized / pocket_size) % len(EUROPEAN_ORDER)
    return EUROPEAN_ORDER[index]

def _wheel_pockets() -> list[ft.Container]:
    controls: list[ft.Container] = []
    center = 210
    radius = 164
    pocket_size = (math.pi * 2) / len(EUROPEAN_ORDER)

    for index, number in enumerate(EUROPEAN_ORDER):
        angle = -math.pi / 2 + pocket_size * index
        x = center + math.cos(angle) * radius
        y = center + math.sin(angle) * radius
        controls.append(
            ft.Container(
                left=x - 18,
                top=y - 18,
                width=36,
                height=36,
                border_radius=18,
                bgcolor=_pocket_color(number),
                border=ft.border.all(1, "#d1d5db"),
                alignment=ft.Alignment(0, 0),
                content=ft.Text(str(number), size=12, weight=ft.FontWeight.BOLD, color="#f9fafb"),
            )
        )
    return controls

def _pocket_color(number: int) -> str:
    if number == 0:
        return "#166534"
    if number in RouletteGame.RED_NUMBERS:
        return "#b91c1c"
    return "#111827"
