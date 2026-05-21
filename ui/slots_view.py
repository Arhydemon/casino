import flet as ft
from models.app_state import AppState
from ui.components.action_buttons import primary_button, secondary_button
from ui.components.balance_panel import build_balance_panel
from ui.components.game_header import build_game_header


def build_slots_view(
    state: AppState,
    balance_refs: dict,
    bet_field: ft.TextField,
    reel_controls: list[ft.Container],
    result_banner: ft.Container,
    on_play,
    on_back,
) -> ft.Container:
    return ft.Container(
        expand=True,
        padding=30,
        bgcolor="#080d13",
        content=ft.Column(
            controls=[
                build_game_header("Слоты", on_back),
                build_balance_panel(state, balance_refs),
                ft.Row(
                    controls=[
                        _slot_machine(reel_controls, result_banner),
                        _slot_panel(bet_field, on_play, on_back),
                    ],
                    spacing=20,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            spacing=22,
            scroll=ft.ScrollMode.AUTO,
        ),
    )


def build_reel(symbol_text: ft.Text) -> ft.Container:
    return ft.Container(
        width=180,
        height=230,
        border_radius=8,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(0, -1),
            end=ft.Alignment(0, 1),
            colors=["#f8fafc", "#d1d5db", "#94a3b8"],
        ),
        border=ft.border.all(5, "#facc15"),
        alignment=ft.Alignment(0, 0),
        animate_scale=ft.Animation(110, ft.AnimationCurve.EASE_OUT),
        animate_rotation=ft.Animation(110, ft.AnimationCurve.EASE_OUT),
        shadow=ft.BoxShadow(blur_radius=18, color="#020617", offset=ft.Offset(0, 8)),
        content=ft.Container(
            width=138,
            height=174,
            border_radius=8,
            bgcolor="#0f172a",
            alignment=ft.Alignment(0, 0),
            content=symbol_text,
        ),
    )


def _slot_machine(reel_controls: list[ft.Container], result_banner: ft.Container) -> ft.Container:
    return ft.Container(
        expand=True,
        padding=26,
        border_radius=8,
        bgcolor="#7f1d1d",
        border=ft.border.all(3, "#facc15"),
        shadow=ft.BoxShadow(blur_radius=34, color="#020617", offset=ft.Offset(0, 16)),
        content=ft.Column(
            controls=[
                ft.Container(
                    height=76,
                    border_radius=8,
                    bgcolor="#111827",
                    border=ft.border.all(2, "#facc15"),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text(
                        "JACKPOT 777",
                        size=34,
                        color="#facc15",
                        weight=ft.FontWeight.BOLD,
                    ),
                ),
                ft.Container(
                    padding=24,
                    border_radius=8,
                    bgcolor="#450a0a",
                    border=ft.border.all(2, "#991b1b"),
                    content=ft.Row(
                        controls=reel_controls,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                ),
                ft.Row(
                    controls=[
                        _payline("2 совпадения", "x2"),
                        _payline("3 совпадения", "x5"),
                        _payline("7 7 7", "x5"),
                    ],
                    spacing=12,
                    wrap=True,
                ),
                result_banner,
            ],
            spacing=18,
        ),
    )


def _slot_panel(bet_field: ft.TextField, on_play, on_back) -> ft.Container:
    return ft.Container(
        width=360,
        padding=22,
        border_radius=8,
        bgcolor="#111827",
        border=ft.border.all(1, "#263244"),
        shadow=ft.BoxShadow(blur_radius=24, color="#020617", offset=ft.Offset(0, 12)),
        content=ft.Column(
            controls=[
                ft.Text("Панель игрока", size=20, weight=ft.FontWeight.BOLD, color="#f9fafb"),
                bet_field,
                ft.Container(
                    padding=14,
                    border_radius=8,
                    bgcolor="#0b1117",
                    content=ft.Text(
                        "Жми кнопку чтобы крутить барабаны",
                        size=13,
                        color="#9ca3af",
                    ),
                ),
                primary_button("Крутить барабаны", ft.Icons.PLAY_ARROW, on_play),
                secondary_button("В меню", ft.Icons.HOME, on_back),
            ],
            spacing=14,
        ),
    )


def _payline(label: str, value: str) -> ft.Container:
    return ft.Container(
        padding=ft.padding.symmetric(horizontal=14, vertical=10),
        border_radius=8,
        bgcolor="#111827",
        border=ft.border.all(1, "#facc15"),
        content=ft.Row(
            controls=[
                ft.Text(label, size=13, color="#d1d5db"),
                ft.Text(value, size=13, color="#facc15", weight=ft.FontWeight.BOLD),
            ],
            spacing=8,
        ),
    )
