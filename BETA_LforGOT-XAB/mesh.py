import time
import asyncio
import serial.tools.list_ports
from pubsub import pub
import meshtastic.serial_interface

import threading
import queue

DEVICE_NAME = "Meshtastic_7bb8"   

data_queue = queue.Queue()
stop_event = threading.Event()

from processing import request_mesh



def check_request(packet, interface):
    try:
        if 'decoded' in packet and packet['decoded'].get('portnum') == 'TEXT_MESSAGE_APP':
            message = packet['decoded'].get('text', '')
            sender = packet.get('fromId', 'неизвестно')
            message_id = packet.get('id', 'unknown')
            
            if message:
                data_queue.put(('mes', sender, message))
                request_mesh(interface, message, sender)

    except Exception as e:
        data_queue.put(("error", f"Ошибка обработки: {e}"))


def find_usb_device():
    try:
        ports = list(serial.tools.list_ports.comports())
        
        for port in ports:
            if "Meshtastic" in port.description or "CP210" in port.description:
                data_queue.put(("status", f"Найдено USB устройство: {port.device}"))
                return port.device

            if "10C4:EA60" in port.hwid:
                data_queue.put(("status", f"Найдено USB устройство (CP210x): {port.device}"))
                return port.device
                
        return None
        
    except Exception as e:
        data_queue.put(("error", f"Ошибка при поиске USB устройств: {e}"))
        return None


def connect_meshtastic(port):
    try:
        # Подключение через USB
        interface = meshtastic.serial_interface.SerialInterface(devPath=port)
        data_queue.put(("status", f"Подключено к Meshtastic через USB (порт: {port})"))
        return interface
    except Exception as e:
        data_queue.put(("error", f"Ошибка подключения через USB: {e}"))
        return None

def run_meshtastic(device_port):
    interface = connect_meshtastic(device_port) 
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
    data_queue.put(('status', "Поиск Meshtastic устройства через USB..."))
    
    # Поиск USB устройства
    device_port = find_usb_device()

    if not device_port:
        data_queue.put(('error', "Meshtastic устройство не найдено через USB"))
        data_queue.put(('status', "Проверьте подключение USB кабеля и драйверы"))
        data_queue.put(None)
        return

    data_queue.put(('status', f"Найден USB порт: {device_port}"))

    # Запуск подключения через USB
    run_meshtastic(device_port)

    data_queue.put(None)