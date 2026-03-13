import time
import asyncio
from bleak import BleakScanner
from pubsub import pub
import meshtastic.ble_interface

DEVICE_NAME = "Meshtastic_7bb8"   

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
        print(f"(!!!)мОшибка при сканировании Bluetooth: {e}")
        return None

def check_request(packet):
    try:
        message = packet.get('decoded', {}).get('text', '')
        sender = packet.get('fromId', 'неизвестно')
        if message:
            print(f"\n ///Mesh сеть: {sender}: {message}")
    except Exception as e:
        print(f"(!!!!) Ошибка обработки: {e}")

def connect_meshtastic(address):
    try:
        interface = meshtastic.ble_interface.BLEInterface(address=address)
        print("///Подключено к Meshtastic")
        return interface
    except Exception as e:
        print(f"(!!!!) Ошибка подключения: {e}")
        return None

def run_meshtastic(device_address, message_handler):
    interface = connect_meshtastic(device_address) 
    if not interface:
        return

    print("\n /// Ожидание сообщений...")
    pub.subscribe(message_handler, "meshtastic.receive")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n(!!!!) Остановка ")
    finally:
        interface.close()
        print("(!!!!) Соединение закрыто")

def connect_mesh():
    print("/// Поиск устройства Meshtastic по Bluetooth...")
    address = check_bluetooth(DEVICE_NAME)
    if not address:
        print(f"(!!!!)'{DEVICE_NAME}' не найдено.")
        return

    print(f"/// Найден адрес: {address}")
    print(f"/// Подключение к {address}...")
    run_meshtastic(address, check_request)

connect_mesh()