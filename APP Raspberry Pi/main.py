import flet as ft
import ctypes

import threading
import queue
import time
import random

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
    
    # блок с тектом
    status_text = ft.Text(
        "Ожидание подключения...", 
        size=14, 
        weight=ft.FontWeight.W_600)
    
    # очередь сообщениц
    mess_queue = queue.Queue() 
    
    # запущенная в потоке функция
    def worker_thread():
        time.sleep(2)

        result_text = f"Сгенерированный текст: {random.randint(1,100)}"
        mess_queue.put(result_text)

    # запуск потока
    def start_thread():
        but_conekt.disabled = True
        status_text.value = "Поток запущен..."
        page.update()

        thread = threading.Thread(target=worker_thread, daemon=True)
        thread.start()
    
    # прослушевание очереди
    def queue_listener():
        while True:
            result = mess_queue.get()  #ожидание 1 сообщения, далее последующих
            
            status_text.value = result
            but_conekt.disabled = False

            page.update()

    # кнопка
    but_conekt = ft.TextButton(
        content="//// Подключиться к Mesh-сети ////",
        on_click=start_thread,
        style=ft.ButtonStyle(color="#11D53F", bgcolor="#dff9fb"),
        data="connect_DEVICE",
    )

    # контейнер
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

    #прослушивание потока
    threading.Thread(target=queue_listener, daemon=True).start()
if __name__ == "__main__":
    ft.run(main)