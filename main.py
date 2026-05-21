import flet as ft
from config import ASSETS_DIR
from ui.app_view import CasinoApp

def main(page: ft.Page) -> None:
    app = CasinoApp(page)
    app.run()

if __name__ == "__main__":
    ft.run(main, assets_dir=ASSETS_DIR)