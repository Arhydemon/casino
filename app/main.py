import flet as ft
from app_state import *

def main(page: ft.Page) -> None:
    page.title = "Дым дым казино и бляди"
    page.window.width = 800 # ширина
    page.window.height = 400 # высота
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    state: AppState = AppState() # без этой хуйни импорты из других файлов не будут работать

    title_text: ft.Text = ft.Text('Казино и бляди', size=32)
    balance_text: ft.Text = ft.Text(f'Балик: {state.player.balance}')
    menu_text: ft.Text = ft.Text('Выбери игру, йоу')

    def open_roulette(event: ft.ControlEvent) -> None: # event это параметр, его ожидает питон, можно даже хуй или _ написать, но без этой хуйни не получится
        page.show_dialog(ft.SnackBar(ft.Text('Рулетки еще нет, лудик ты ебаный')))

    def open_blackjack(event: ft.ControlEvent) -> None:
        page.show_dialog(ft.SnackBar(ft.Text('Блекджека тоже пока что нихуя нет азазааз))')))

    def open_slots(event: ft.ControlEvent) -> None:
        page.show_dialog(ft.SnackBar(ft.Text("Слоты пока не готовы")))


    r_button: ft.ElevatedButton = ft.ElevatedButton("Рулеточка", on_click=open_roulette)
    b_button: ft.ElevatedButton = ft.ElevatedButton('Блекджек', on_click=open_blackjack)
    s_button: ft.ElevatedButton = ft.ElevatedButton('Слоты', on_click=open_slots)

    main_menu_column: ft.Column = ft.Column(
        controls=[title_text, balance_text, menu_text, r_button, b_button, s_button], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing= 20
    )

    page.add(main_menu_column)
ft.app(target=main)