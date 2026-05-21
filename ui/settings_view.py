import flet as ft

from models.app_state import AppState
from ui.components.action_buttons import primary_button, secondary_button
from ui.components.balance_panel import build_balance_panel
from ui.components.game_header import build_game_header


def build_settings_view(
    state: AppState,
    sound_switch: ft.Switch,
    on_test_sound,
    on_back,
) -> ft.Container:
    return ft.Container(
        expand=True,
        padding=28,
        bgcolor="#0b1117",
        content=ft.Column(
            controls=[
                build_game_header("Настройки", "Параметры локального приложения", on_back),
                build_balance_panel(state),
                ft.Container(
                    padding=20,
                    border_radius=8,
                    bgcolor="#17202a",
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.VOLUME_UP
                                        if state.settings.is_sound_enabled()
                                        else ft.Icons.VOLUME_OFF,
                                        color="#60a5fa",
                                    ),
                                    sound_switch,
                                ],
                                spacing=12,
                            ),
                            primary_button("Тест звука", ft.Icons.GRAPHIC_EQ, on_test_sound),
                            secondary_button("В меню", ft.Icons.HOME, on_back),
                        ],
                        spacing=16,
                    ),
                ),
            ],
            spacing=20,
        ),
    )
