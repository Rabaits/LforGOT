import flet as ft
import ctypes

def main(page: ft.Page):
    page.title = "XAB-LFGOT"
    page.window.resizable = False
    page.window.width = 1200
    page.window.height = 800
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    #обновление страницы
    page.update()
    
    # получаем размеры экрана
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    
    # центрируем окно
    page.window.left = (screen_width - 1200) // 2
    page.window.top = (screen_height - 800) // 2
    
    text = ft.Text("Опвищение", size=14, weight=ft.FontWeight.W_600)
    
    but_conekt = ft.TextButton(
        content="Подключиться к Mesh-сети",
        icon_color=ft.Colors.BLUE_300,
    )

    calculator_container = ft.Container(
        content=ft.Column([ text, but_conekt
        ])
    
    )

    #обновление страницы
    page.add(calculator_container)
    page.update()

if __name__ == "__main__":
    ft.run(main)