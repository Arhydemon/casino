import flet as ft

from models.app_state import AppState
from ui.components.balance_panel import build_balance_panel


def build_main_menu_view(
    state: AppState,
    on_roulette,
    on_slots,
    on_statistics,
    on_settings,
) -> ft.Container:
    return _page_container(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            width=76,
                            height=76,
                            border_radius=8,
                            bgcolor="#06351f",
                            border=ft.border.all(1, "#22c55e"),
                            alignment=ft.Alignment(0, 0),
                            content=ft.Icon(ft.Icons.CASINO, size=44, color="#22c55e"),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Дым Дым Казино и Бляди",
                                    size=38,
                                    weight=ft.FontWeight.BOLD,
                                    color="#f9fafb",
                                ),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                    ],
                    spacing=18,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                build_balance_panel(state),
                ft.Row(
                    controls=[
                        _game_tile(
                            "Рулетка",
                            "Число, цвет или четность",
                            "0-36",
                            ft.Icons.CASINO,
                            "#22c55e",
                            on_roulette,
                        ),
                        _game_tile(
                            "Слоты",
                            "Три барабана и быстрый раунд",
                            "x5",
                            ft.Icons.STARS,
                            "#f59e0b",
                            on_slots,
                        ),
                    ],
                    spacing=18,
                    wrap=True,
                ),
                ft.Row(
                    controls=[
                        _tool_tile("Статистика", "Игры, победы, общий выигрыш", ft.Icons.BAR_CHART, on_statistics),
                        _tool_tile("Настройки", "Звук и параметры приложения", ft.Icons.SETTINGS, on_settings),
                    ],
                    spacing=18,
                    wrap=True,
                ),
            ],
            spacing=22,
            scroll=ft.ScrollMode.AUTO,
        )
    )

def _game_tile(title: str, subtitle: str, badge: str, icon, color: str, on_click) -> ft.Container:
    return ft.Container(
        width=360,
        height=190,
        padding=22,
        border_radius=8,
        bgcolor="#111827",
        border=ft.border.all(1, "#263244"),
        shadow=ft.BoxShadow(blur_radius=24, color="#05070a", offset=ft.Offset(0, 10)),
        ink=True,
        on_click=on_click,
        animate_scale=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icon, size=38, color=color),
                        ft.Container(
                            padding=ft.padding.symmetric(horizontal=12, vertical=6),
                            border_radius=8,
                            bgcolor="#0b1117",
                            content=ft.Text(badge, size=13, color=color, weight=ft.FontWeight.BOLD),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Text(title, size=26, weight=ft.FontWeight.BOLD, color="#f9fafb"),
                ft.Text(subtitle, size=14, color="#9ca3af"),
                ft.Text("Играть", size=13, color=color, weight=ft.FontWeight.BOLD),
            ],
            spacing=12,
        ),
    )

def _tool_tile(title: str, subtitle: str, icon, on_click) -> ft.Container:
    return ft.Container(
        width=360,
        padding=18,
        border_radius=8,
        bgcolor="#0f172a",
        border=ft.border.all(1, "#263244"),
        ink=True,
        on_click=on_click,
        content=ft.Row(
            controls=[
                ft.Icon(icon, size=30, color="#60a5fa"),
                ft.Column(
                    controls=[
                        ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color="#f9fafb"),
                        ft.Text(subtitle, size=12, color="#9ca3af"),
                    ],
                    spacing=2,
                    expand=True,
                ),
            ],
            spacing=14,
        ),
    )


def _page_container(content: ft.Control) -> ft.Container:
    return ft.Container(
        expand=True,
        padding=30,
        bgcolor="#080d13",
        content=content,
    )
