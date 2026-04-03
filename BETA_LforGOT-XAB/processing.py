import time

def sendtext_mesh(interface, message, sender):
    interface.sendText(message, destinationId=sender)

def helps(interface, sender):
    help_text ="Отправь запрос ИИ по примеру: [? текст вопроса]"
    sendtext_mesh(interface, help_text, sender) 
  

def command_proces(interface, mess_user, sender):
    command = mess_user[1:].split(" ")
    until = command[0]

    match until:
        case 'help':
            helps(interface, sender) #справочные команды
        case _:
            sendtext_mesh(
                interface, 
                "Ошибка: нет такой команды -> /help",
                sender) #ошибка ошибка
    return

def generating_AI(mess_user):

    from models import AI_return
    mess = mess_user[1:]
    request = AI_return(mess)
    return request

def request_ai(interface, mess_user, sender):
    sendtext_mesh(
        interface, 
        "Обработки запроса >>", 
        sender)
    
    mes = generating_AI(mess_user)

    if len(mes) <= 100:
        sendtext_mesh(interface, mes, sender)
    else:
        string = mes
        
        while len(string) > 0:
            if len(string) <= 100:
                sendtext_mesh(interface, string, sender)
                break
            
            chunk = string[:100]
            last_space = chunk.rfind(' ')
            
            if last_space != -1:
                total_mes = chunk[:last_space]
            else:
                total_mes = chunk
            
            sendtext_mesh(interface, total_mes, sender)
            
            time.sleep(3)
            string = string[len(total_mes):].lstrip()
 

def request_mesh(interface, mess_user, sender):
    index = mess_user[0]
    match index:
        case '?':
            request_ai(interface, mess_user, sender)
            
        case '/':
            command_proces(interface, mess_user, sender)
        case _:
            sendtext_mesh(
                interface, 
                "Ошибка: -> /help",
                sender)


