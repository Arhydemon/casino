import flet as ft
from models.app_state import AppState
from ui.components.action_buttons import secondary_button
from ui.components.balance_panel import build_balance_panel
from ui.components.game_header import build_game_header

def build_statistics_view(state: AppState, on_reset, on_back) -> ft.Container:
    win_rate = 0
    if state.statistics.games_played > 0:
        win_rate = round(state.statistics.wins / state.statistics.games_played * 100)
    return ft.Container(
        expand=True,
        padding=30,
        bgcolor="#080d13",
        content=ft.Column(
            controls=[
                build_game_header("Статистика", "Сохраненные результаты игрока", on_back),
                build_balance_panel(state),
                ft.Row(
                    controls=[
                        _stat_card("Игр сыграно", state.statistics.games_played, ft.Icons.SPORTS_ESPORTS, "#60a5fa"),
                        _stat_card("Побед", state.statistics.wins, ft.Icons.EMOJI_EVENTS, "#22c55e"),
                        _stat_card("Процент побед", f"{win_rate}%", ft.Icons.PERCENT, "#f59e0b"),
                        _stat_card("Общий выигрыш", state.statistics.total_win, ft.Icons.TRENDING_UP, "#a78bfa"),
                    ],
                    spacing=16,
                    wrap=True,
                ),
                ft.Container(
                    padding=20,
                    border_radius=8,
                    bgcolor="#111827",
                    border=ft.border.all(1, "#263244"),
                    content=ft.Row(
                        controls=[
                            ft.Text("Сброс статистики обнулит игры, победы и общий выигрыш.", color="#d1d5db", expand=True),
                            secondary_button("Сбросить", ft.Icons.RESTART_ALT, on_reset),
                        ],
                        spacing=16,
                        wrap=True,
                    ),
                ),
            ],
            spacing=22,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

def _stat_card(label: str, value, icon, color: str) -> ft.Container:
    return ft.Container(
        width=260,
        padding=20,
        border_radius=8,
        bgcolor="#111827",
        border=ft.border.all(1, "#263244"),
        content=ft.Column(
            controls=[
                ft.Icon(icon, size=30, color=color),
                ft.Text(label, size=13, color="#9ca3af"),
                ft.Text(str(value), size=30, weight=ft.FontWeight.BOLD, color="#f9fafb"),
            ],
            spacing=8,
        ),
    )
