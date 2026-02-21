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
    print(response)
    return response


def send_message(from_id, text_mes, interface):
    try:
        interface.sendText(text_mes, destinationId=from_id) #отправка ответа
    except Exception as e:
        print(f"//ERROR: {e}")
       
def generating_response(from_id, text, interface):
    response = AI_return(text)

    if len(response) <= 100:
        send_message(from_id, response, interface)
    else:
        string = response
        words_str = string.split(" ")
        len_string = len(string) // 100 + 1 * int(len(string)%100 > 0)

        for i in range(len_string):
            mes = string[:100]
            words_mes = len(mes.split(" "))

            total_mes = " ".join(words_str[:words_mes])

            while len(total_mes) > 100:
                words_mes -= 1
                total_mes = " ".join(words_str[:words_mes])
    
            send_message(from_id, total_mes, interface)
            time.sleep(1)
            
            words_str = words_str[words_mes:]
            string = string[len(total_mes):]

def check_request(packet, interface):
    text = packet.get('decoded', {}).get('text') 
    if text:
        from_id = packet.get('fromId', 'unknown') #получение из пакета данных ID отправителя
        node = interface.nodes.get(from_id, {}).get('user', {})
        sender = node.get('longName', f'Node {from_id}')
        print(f"[{time.strftime('%H:%M:%S')}] {from_id}: {text}")

        generating_response(from_id, text, interface)

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