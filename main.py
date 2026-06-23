import flet as ft
from settings import Config
from ui.app_view import CasinoApp # главный класс приложения который собирает всю программу вместе


def main(page: ft.Page) -> None: # окно создаётся
    app = CasinoApp(page) # объект казино + окно флета. тут прям вся логика. бд, данные, сервисы интерфейс
    app.run() # запуск приложение и главное меню


if __name__ == "__main__":
    ft.run(main, assets_dir=Config.ASSETS_DIR)