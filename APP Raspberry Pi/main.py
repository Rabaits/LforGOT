import flet as ft
import ctypes

import asyncio
from bleak import BleakScanner

DEVICE_ADDRESS = "Meshtastic_7bb8"  

async def check_bluetooth():
    try:
        devices = await BleakScanner.discover(timeout=2)
        if devices is not None:
            print("(+) Bluetooth включен")
            return True, None
    except Exception as e:
        error = "(Х) Bluetooth выключен"
        print(error)
        return False, error

async def connectionDEVICE():
    returns, text = await check_bluetooth()
    if not(returns):
        print(text)
        return False, text
    
    print("Успешное подключение!")
    return True, "Успешное подключение!"

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
        on_click=connectionDEVICE,
        data="connect_DEVICE",
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