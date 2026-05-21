import flet as ft

def build_game_header(title: str, subtitle: str, on_back=None) -> ft.Row:
    controls = []
    if on_back is not None:
        controls.append(
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                tooltip="домой",
                icon_color="#f9fafb",
                on_click=on_back,
            )
        )
    controls.append(
        ft.Column(
            controls=[
                ft.Text(title, size=28, weight=ft.FontWeight.BOLD, color="#f9fafb"),
                ft.Text(subtitle, size=14, color="#9ca3af"),
            ],
            spacing=2,
            expand=True,
        )
    )
    return ft.Row(
        controls=controls,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

