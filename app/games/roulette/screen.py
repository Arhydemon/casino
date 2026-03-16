import flet as ft
from app.app_state import AppState
from app.games.roulette.game import RouletteGame

def show_roulette_screen(page: ft.Page, state: AppState, go_back) -> None:
    page.controls.clear()
    game: RouletteGame = RouletteGame(state)

    title_text: ft.Text = ft.Text('Рулеточка', size=30)
    balance_text: ft.Text = ft.Text(f'Баланс: {state.player.balance}', size=30)
    info_text: ft.Text = ft.Text('Сделай ставку и жми СПИН', size=30)
    

    def back_to_menu(event: ft.ControlEvent) ->None:
        go_back()

    back_button: ft.ElevatedButton = ft.ElevatedButton('Домой', on_click=back_to_menu) 
    
    roulette_column: ft.Column = ft.Column(
        controls=[title_text, balance_text, info_text, back_button],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    page.add(roulette_column)
    page.update()

def test_roulette_screen(page: ft.Page,) -> None:
    page.title = 'Тест рулетки'
    page.window.width = 1920
    page.window.height = 1080
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    state: AppState = AppState()  # создаём тестовое состояние приложения

    def fake_back() -> None:
        page.controls.clear()
        page.add(ft.Text('Тут возвратик в меню будет хз'))
        page.update()

    show_roulette_screen(page, state, fake_back)

ft.app(target=test_roulette_screen)