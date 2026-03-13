import flet as ft
import ctypes

import asyncio
from bleak import BleakScanner

import meshtastic.ble_interface  #интерфейс для блютуз
from pubsub import pub 
import time
import threading
DEVICE_ADDRESS = "Meshtastic_7bb8"  


def check_request(packet):  #логика обработки сообщений из mesh сети
    try:
        message = packet.get('decoded', {}).get('text', '')
        sender = packet.get('fromId', 'неизвестно')
        if message != None:
            print(f"\nMesh сеть: {sender}: {message}")

    except Exception as e:
        print(f"(!!!) {e}")

def connect_meshtastic(device_address): #подключение к mesh сети
    try:
        interface = meshtastic.ble_interface.BLEInterface(address=device_address)
        print("Подключено к Meshtastic")
        return interface
    except Exception as e:
        print(f"(!!!!) Ошибка подключения: {e}")
        return None

def run_meshtastic(device_address, message_handler, status_callback=None): #запуск mesh сети
    interface = connect_meshtastic(device_address)
    
    if not interface:
        if status_callback:
            status_callback("Ошибка подключения к Meshtastic")
        return
    
    if status_callback:
        status_callback("Подключено к Meshtastic!")
    
    try:
        status_callback("Ожидание сообщений")
        print("// Ожидание сообщений //")
        pub.subscribe(message_handler, "meshtastic.receive")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n// Остановка //")
    finally:
        interface.close()
        print("// Соединение закрыто //")

async def check_bluetooth(): #проверка блютуз
    try:
        devices = await BleakScanner.discover(timeout=2)
        if devices is not None:
            print("Bluetooth включен")
            return True, None
    
    except Exception as e:
        error = "Bluetooth выключен"
        print("(!!!) Bluetooth выключен")
        return False, error

#основная логика 
async def connectionDEVICE(page: ft.Page, status_text: ft.Text): 
    
    status_text.value = "Проверка Bluetooth..."
    page.update()
    
    returns, message = await check_bluetooth()
    if not returns:
        status_text.value = message
        page.update()
        print(message)
        return
    
    status_text.value = f"Проверка подключения к {DEVICE_ADDRESS}..."
    page.update()

    await asyncio.sleep(1)
    
    # Запускаем в отдельном потоке
    thread = threading.Thread(
        target=run_meshtastic,
        args=(DEVICE_ADDRESS, check_request),
        daemon=True
    )
    thread.start()
    
    # Даем время на подключение
    await asyncio.sleep(3)
    
    # Финальное обновление статуса
    if thread.is_alive():
        status_text.value = "Подключение активно"
    else:
        status_text.value = "Ошибка подключения"
    
    page.update()
    print("Процесс подключения завершен")

 
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
    
    status_text = ft.Text(
        "Ожидание подключения...", 
        size=14, 
        weight=ft.FontWeight.W_600)
    
    async def on_connect_click(e):
        await connectionDEVICE(page, status_text)
 
    but_conekt = ft.TextButton(
        content="//// Подключиться к Mesh-сети ////",
        on_click=on_connect_click,
        style=ft.ButtonStyle(color="#11D53F", bgcolor="#dff9fb"),
        data="connect_DEVICE",
    )

    calculator_container = ft.Container(
        alignment=ft.alignment.Alignment.CENTER,
        width=600, #ширина, длянну не указываем - растянеться
        bgcolor ='#833471', #цвет фона
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