import flet as ft
import ctypes

import asyncio
from bleak import BleakScanner

def main(page: ft.Page):
    page.title = "LFGOT AI CHAT"
    page.window.resizable = False
    page.window.width = 360
    page.window.height = 720
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER 
    page.update()

    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    page.window.left = (screen_width - 360) // 2
    page.window.top = (screen_height - 720) // 2
    

    #обновление страницы
    page.update()

if __name__ == "__main__":
    ft.run(main)