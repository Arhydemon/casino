import flet as ft

def main(page: ft.Page) -> None:
    page.title = "Дым дым казино и бляди"
    page.window.width = 1920 # ширина
    page.window.height = 1080 # высота
    
    title_text: ft.Text = ft.Text("Казик йоу")
    
    page.add(title_text)

ft.app(target=main)