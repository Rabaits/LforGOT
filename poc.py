import meshtastic.ble_interface
from pubsub import pub
import time

import subprocess

from ollama import chat

DEVICE_ADDRESS = "Meshtastic_7bb8"  
model_name = 'llama3.2:1b'

def AI_return(request):

    messages = [
    {
        'role': 'system',
        'content': 'Пользователь живёт в РФ, ты отвечаешь ТОЛЬКО на русском языке, твой ответ не должен привышать 150 символов'
    },
    {
        'role': 'user',
        'content': request[1:]
    }
    ]
    response = chat(model=model_name, messages=messages).message.content

    while len(response) > 150:
        response = chat(model=model_name, messages=messages).message.content

    print(response)
    return response


def send_mess(from_id, text, interface):
    text_return = AI_return(text)
    try:
        interface.sendText(text_return, destinationId=from_id)
    except Exception as e:
        print(f"[ERROR] Не удалось отправить сообщение: {e}")
       




def print_message(packet, interface):
    text = packet.get('decoded', {}).get('text')
    if text:
        from_id = packet.get('fromId', 'unknown')
        node = interface.nodes.get(from_id, {}).get('user', {})
        sender = node.get('longName', f'Node {from_id}')
        print(f"[{time.strftime('%H:%M:%S')}] {sender}: {text}")
        send_mess(from_id, text, interface)

try:
    print(f"[INFO] Подключение к {DEVICE_ADDRESS}...")
    interface = meshtastic.ble_interface.BLEInterface(address=DEVICE_ADDRESS)
    print("[SUCCESS] Connected! Ожидание сообщений (Ctrl+C для выхода)...")
    
    pub.subscribe(print_message, "meshtastic.receive")
    
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\n[INFO] Остановка...")
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc() 
finally:
    if 'interface' in locals():
        interface.close()