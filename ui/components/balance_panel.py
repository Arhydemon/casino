import flet as ft
from models.app_state import AppState

def build_balance_panel(state: AppState, refs: dict | None = None) -> ft.Container:
    refs = refs if refs is not None else {}
    player_value = _value_text(state.player.login)
    balance_value = _value_text(str(state.player.balance))
    games_value = _value_text(str(state.statistics.games_played))
    wins_value = _value_text(str(state.statistics.wins))
    total_win_value = _value_text(str(state.statistics.total_win))
    refs["player"] = player_value
    refs["balance"] = balance_value
    refs["games"] = games_value
    refs["wins"] = wins_value
    refs["total_win"] = total_win_value

    return ft.Container(
        padding=18,
        border_radius=8,
        bgcolor="#111827",
        border=ft.border.all(1, "#263244"),
        shadow=ft.BoxShadow(
            blur_radius=18,
            spread_radius=0,
            color="#05070a",
            offset=ft.Offset(0, 8),
        ),
        content=ft.Row(
            controls=[
                _metric("игрок", player_value, ft.Icons.PERSON),
                _metric("баланс", balance_value, ft.Icons.PAID),
                _metric("игр", games_value, ft.Icons.SPORTS_ESPORTS),
                _metric("побед", wins_value, ft.Icons.EMOJI_EVENTS),
                _metric("выигрыш", total_win_value, ft.Icons.TRENDING_UP),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            wrap=True,
            spacing=18,
        ),
    )


def build_result_banner(result: dict | None) -> ft.Container:
    if result is None:
        title = "ГАЗ СТАВОЧКУ"
        subtitle = "РЕЗУЛЬТАТ БУДЕТ ПОСЛЕ СТАВОЧКИ"
        icon = ft.Icons.AUTO_AWESOME
        color = "#60a5fa"
        background = "#111827"
        border_color = "#263244"
    elif result["is_win"]:
        title = "победа..."
        subtitle = f"повезло...)0): {result['win_amount']} | баланс: {result.get('balance', '')}"
        icon = ft.Icons.EMOJI_EVENTS
        color = "#22c55e"
        background = "#052e1a"
        border_color = "#16a34a"
    else:
        title = "ХАХА ЛОХ"
        subtitle = f"ПРОЁБАНО: {result['bet']} | баланс: {result.get('balance', '')}"
        icon = ft.Icons.WARNING
        color = "#f97316"
        background = "#321308"
        border_color = "#ea580c"

    return ft.Container(
        padding=18,
        border_radius=8,
        bgcolor=background,
        border=ft.border.all(1, border_color),
        animate=ft.Animation(260, ft.AnimationCurve.EASE_OUT),
        content=ft.Row(
            controls=[
                ft.Icon(icon, size=34, color=color),
                ft.Column(
                    controls=[
                        ft.Text(title, size=21, weight=ft.FontWeight.BOLD, color="#f9fafb"),
                        ft.Text(subtitle, size=14, color="#d1d5db"),
                    ],
                    spacing=2,
                    expand=True,
                ),
            ],
            spacing=14,
        ),
    )

def _metric(label: str, value_control: ft.Text, icon) -> ft.Container:
    return ft.Container(
        padding=12,
        border_radius=8,
        bgcolor="#0b1117",
        content=ft.Row(
            controls=[
                ft.Icon(icon, size=20, color="#60a5fa"),
                ft.Column(
                    controls=[
                        ft.Text(label, size=12, color="#9ca3af"),
                        value_control,
                    ],
                    spacing=0,
                ),
            ],
            spacing=10,
        ),
    )

def _value_text(value: str) -> ft.Text:
    return ft.Text(value, size=18, weight=ft.FontWeight.BOLD, color="#f9fafb")