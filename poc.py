import meshtastic.ble_interface
from pubsub import pub
import time
from ollama import chat

DEVICE_ADDRESS = "Meshtastic_7bb8"  
model_name = 'llama3.2:1b'

def AI_return(request):

    messages = [
    {
        'role': 'system',
        'content': 'Ты русскоязычный ассистент. ОБЯЗАТЕЛЬНЫЕ ПРАВИЛА: Отвечай на русском языке. Максимум 150 символов'
    },
    {
        'role': 'user',
        'content': request[1:]
    }
    ]
    response = chat(model=model_name, messages=messages).message.content #генрация ответа от ИИ

    while len(response) > 150:
        response = chat(model=model_name, messages=messages).message.content #генрация ответа от ИИ
    return response


def send_message(from_id, text, interface):
    text_return = AI_return(text)
    try:
        interface.sendText(text_return, destinationId=from_id) #отправка ответа
    except Exception as e:
        print(f"//ERROR: {e}")
       

def check_request(packet, interface):
    text = packet.get('decoded', {}).get('text') 
    if text:
        from_id = packet.get('fromId', 'unknown') #получение из пакета данных ID отправителя
        node = interface.nodes.get(from_id, {}).get('user', {})
        sender = node.get('longName', f'Node {from_id}')
        print(f"[{time.strftime('%H:%M:%S')}] {from_id}: {text}")

        send_message(from_id, text, interface)

try:
    interface = meshtastic.ble_interface.BLEInterface(address=DEVICE_ADDRESS) #создание объекта подключения 
    print("//Ожидание сообщений ... ")
    pub.subscribe(check_request, "meshtastic.receive") #подписка на сообщения внутри mesh-сети
    
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    print("//Остановка")
except Exception as e:
    print(f"//ERROR: {e}")
    import traceback
    traceback.print_exc() 
finally:
    if 'interface' in locals():
        interface.close()