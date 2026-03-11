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

async def connectionDEVICE(page: ft.Page, status_text: ft.Text):
    
    
    status_text.value = "Проверка Bluetooth..."
    page.update()
    
    returns, message  = await check_bluetooth()
    if not(returns):
        status_text.value = message
        page.update()
        print(message)

        return
    
    status_text.value = "Успешное подключение!"
    page.update()
    print("Успешное подключение!")
    return




def main(page: ft.Page):
    page.title = "XAB-LFGOT"
    page.window.resizable = False
    page.window.width = 1200
    page.window.height = 800
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER    
    #обновление страницы
    page.update()
    
    # получаем размеры экрана
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    
    # центрируем окно
    page.window.left = (screen_width - 1200) // 2
    page.window.top = (screen_height - 800) // 2
    
    status_text = ft.Text("Ожидание подключения...", size=14, weight=ft.FontWeight.W_600)
    
    async def on_connect_click(e):
        await connectionDEVICE(page, status_text)

    but_conekt = ft.TextButton(
        content="Подключиться к Mesh-сети",
        icon_color=ft.Colors.BLUE_300,
        on_click=on_connect_click,
        data="connect_DEVICE",
    )

    calculator_container = ft.Container(
        alignment=ft.alignment.Alignment.CENTER,
        width=600, #ширина, длянну не указываем - растянеться
        bgcolor = ft.Colors.WHITE, #цвет фона
        border_radius = ft.BorderRadius.all(20), #задание радиуса у контура
        padding=ft.Padding.all(100),#это общий оступ (сверх, слева, справа, снизу)

        content=ft.Column([ status_text, but_conekt
        ])
    
    )

    #обновление страницы
    page.add(calculator_container)
    page.update()

if __name__ == "__main__":
    ft.run(main)