import time
import asyncio
from bleak import BleakScanner
from pubsub import pub
import meshtastic.ble_interface

import threading
import queue

DEVICE_NAME = "Meshtastic_7bb8"   

data_queue = queue.Queue()
stop_event = threading.Event()

def check_bluetooth(device_name, timeout=5):

    async def scan():
        devices = await BleakScanner.discover(timeout=timeout)
        for d in devices:
            if d.name and device_name in d.name:
                return d.address
        return None

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        address = loop.run_until_complete(scan())
        loop.close()
        return address #адресс для подключения к mesh-устройству
    
    except Exception as e:
        data_queue.put(("error", f"Ошибка при сканировании Bluetooth: {e}"))
        return None

def check_request(packet):
    try:
        message = packet.get('decoded', {}).get('text', '')
        sender = packet.get('fromId', 'неизвестно')
        if message:
            data_queue.put(('mes', sender, message))
    except Exception as e:
        data_queue.put(("error", f"Ошибка обработки: {e}"))

def connect_meshtastic(address):
    try:
        interface = meshtastic.ble_interface.BLEInterface(address=address)
        data_queue.put(("status","Подключено к Meshtastic"))
        return interface
    except Exception as e:
        data_queue.put(("error", f"Ошибка подключения: {e}"))
        return None

def run_meshtastic(device_address):
    interface = connect_meshtastic(device_address) 
    if not interface:
        return

    data_queue.put(("status", "Ожидание сообщений..."))
    pub.subscribe(check_request, "meshtastic.receive")

    try:
        while not stop_event.is_set():
            time.sleep(1)
    except Exception as e:
        data_queue.put(('error', f"Ошибка в цикле: {e}"))
    finally:
        interface.close()
        data_queue.put(('status', "Соединение закрыто"))

def connect_mesh():
    data_queue.put(('status', "Поиск устройства Meshtastic по Bluetooth..."))
    address = check_bluetooth(DEVICE_NAME)

    if not address:
        print(('error', f"'{DEVICE_NAME}' не найдено"))
        data_queue.put(None)
        return

    data_queue.put(('status', f"Найден адрес: {address}"))
    data_queue.put(('status', f"Подключение к {address}..."))

    run_meshtastic(address)

    data_queue.put(None)
 

def main():
    t2 = threading.Thread(target=connect_mesh, name="MeshtasticThread")
    t2.start()

    print("Основной поток запущен. Для выхода нажмите Ctrl+C")
    try:
        while not stop_event.is_set():
            try:
                data = data_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if data is None:
                print("Получен сигнал завершения.")
                break

            if isinstance(data, tuple):
                msg_type = data[0]
                if msg_type == 'message':
                    _, sender, text = data
                    print(f"[Mesh] {sender}: {text}")
                elif msg_type == 'status':
                    _, text = data
                    print(f"[Статус] {text}")
                elif msg_type == 'error':
                    _, text = data
                    print(f"[Ошибка] {text}")
                else:
                    print(f"[Неизвестно] {data}")
            else:
                print(f"[Данные] {data}")
    except KeyboardInterrupt:
        print("\nПрерывание с клавиатуры. Останавливаем...")
        stop_event.set()
    finally:
        stop_event.set()  # гарантируем сигнал
        t2.join()
        print("Основной поток завершён.")

if __name__ == "__main__":
    main()