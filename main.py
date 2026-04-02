import flet as ft
from app.app_state import *
from app.core.services import AppStateService


class CasinoApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.state_service = AppStateService()
        self.test_stats_button = ft.Button("Тест статистики", on_click=self.test_stats)
        self.page.title = "Дым дым казино и бляди"
        self.page.window.width = 800 # ширина
        self.page.window.height = 400 # высота
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.state_service.initialize_database()
        self.state: AppState = self.state_service.load_state() # без этой хуйни импорты из других файлов не будут работать

        self.title_text: ft.Text = ft.Text('Казино и бляди', size=32)
        self.balance_text: ft.Text = ft.Text(f'Балик: {self.state.player.balance}')
        self.menu_text: ft.Text = ft.Text('Выбери игру, йоу')

        self.r_button: ft.Button = ft.Button("Рулеточка", on_click=self.open_roulette)
        self.b_button: ft.Button = ft.Button('Блекджек', on_click=self.open_blackjack)
        self.s_button: ft.Button = ft.Button('Слоты', on_click=self.open_slots)

        self.main_menu_column: ft.Column = ft.Column(
            controls=[
                self.title_text,
                self.balance_text,
                self.menu_text,
                self.r_button,
                self.b_button,
                self.s_button,
                self.test_stats_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

    def open_roulette(self, event: ft.ControlEvent) -> None: # event это параметр, его ожидает питон, можно даже хуй или _ написать, но без этой хуйни не получится
        self.page.show_dialog(ft.SnackBar(ft.Text('Рулетки еще нет, лудик ты ебаный')))

    def open_blackjack(self, event: ft.ControlEvent) -> None:
        self.page.show_dialog(ft.SnackBar(ft.Text('Блекджека тоже пока что нихуя нет азазааз))')))

    def open_slots(self, event: ft.ControlEvent) -> None:
        self.page.show_dialog(ft.SnackBar(ft.Text("Слоты пока не готовы")))

    def build(self) -> None:
        self.page.controls.clear()
        self.page.add(self.main_menu_column)
        self.page.update()

    def test_stats(self, event):
        self.state.games_played += 1
        self.state.games_won += 1
        self.state.total_win += 50
        self.state_service.save_state(self.state)
        self.page.show_dialog(ft.SnackBar(ft.Text("Стата обновлена")))

def main(page: ft.Page) -> None:
    app = CasinoApp(page)
    app.build()

ft.run(main)