import flet as ft

def primary_button(text: str, icon, on_click) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        content=text,
        icon=icon,
        height=48,
        bgcolor="#16a34a",
        color="#ffffff",
        elevation=6,
        on_click=on_click,
    )

def secondary_button(text: str, icon, on_click) -> ft.OutlinedButton:
    return ft.OutlinedButton(
        content=text,
        icon=icon,
        height=48,
        style=ft.ButtonStyle(
            color="#d1d5db",
            side=ft.BorderSide(1, "#334155"),
        ),
        on_click=on_click,
    )

