import flet as ft
import threading

from mesh import connect_mesh, data_queue

def main(page: ft.Page):
    page.title = "XAB-LFGOT"
    page.window.resizable = False
    page.window.width = 1200
    page.window.height = 800
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER    
    
    page.update()
    
    # блок с тектом
    status_text = ft.Text(
        "Ожидание подключения...", 
        size=14, 
        weight=ft.FontWeight.W_600)
    
    # запуск потока
    def start_mesh(e):
        but_conekt.disabled = True
        status_text.value = "Поиск USB устройств..."
        page.update()

        thread = threading.Thread(target=connect_mesh, daemon=True)
        thread.start()
    
    # прослушивание очереди
    log_history = []

    def queue_listener():
        while True:
            data = data_queue.get()

            if data is None:
                but_conekt.disabled = False
                page.update()
                continue

            msg_type = data[0]

            if msg_type == "mes":
                _, sender, text = data
                log_history.append(f">> [{sender}] {text}")

            elif msg_type == "status":
                _, text = data
                log_history.append(f"//// {text}")
                
            elif msg_type == "error":
                _, text = data
                log_history.append(f"(!!!!) {text}")
                
            status_text.value = "\n".join(log_history[-10:])
            page.update()

    # кнопка
    but_conekt = ft.TextButton(
        content="//// Подключиться к Mesh-сети (USB) ////",
        on_click=start_mesh,
        style=ft.ButtonStyle(color="#11D53F", bgcolor="#dff9fb"),
        data="connect_DEVICE",
    )

    # контейнер
    calculator_container = ft.Container(
        alignment=ft.alignment.Alignment.CENTER,
        width=600,
        bgcolor='#833471',
        border_radius=ft.BorderRadius.all(20),
        padding=ft.Padding.all(100),
        content=ft.Column([ status_text, but_conekt ])
    )

    page.add(calculator_container)
    page.update()

    #прослушивание потока
    threading.Thread(target=queue_listener, daemon=True).start()

if __name__ == "__main__":
    ft.run(main)