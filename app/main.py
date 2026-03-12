import flet as ft

def main(page: ft.Page):
    page.title = "Дым дым казино и бляди"
    page.window.width = 1920
    page.window.height = 1080
    
    page.add(
        ft.Text("Казик йоу"))
    
ft.app(target=main) 