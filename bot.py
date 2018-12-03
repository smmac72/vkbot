import time
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType

def subUser():
    userID = event.obj.from_id # ИД юзера
    with open("people.txt") as ids:
        users = [row.strip() for row in ids]
    if (str(userID) not in users): # проверка на отсутствие подписки и регистрация
        people = open('people.txt','r')
        prev = people.read()
        people.close()
        people = open('people.txt','w')
        if (len(users) != 0):
            prev += '\n'
            people.write(prev + str(userID))
        vk.messages.send(
            user_id=userID,
            random_id = 0,
            message="Вы подписались!"
        )
        print(userID, "user subscribed!");
        people.close()
    else: # если подписка уже есть
        vk.messages.send(
            user_id=userID,
            random_id = 0,
            message="Вы уже подписаны!"
        )


def unsubUser():
    userID = event.obj.from_id # ИД юзера
    with open("people.txt") as ids:
        users = [row.strip() for row in ids]
    if (str(userID) in users): # проверка на наличие подписки и регистрация
        people = open('people.txt','w')
        text = ''
        for i in range(len(users)):
            if users[i] != str(userID):
                text += str(userID) + '\n'
        people = open('people.txt','w')
        people.write(text)
        vk.messages.send(
            user_id=userID,
            random_id = 0,
            message="Вы отписались!"
        )
        print(userID, "user subscribed!");
        people.close()
    else: # если подписка уже есть
        vk.messages.send(
            user_id=userID,
            random_id = 0,
            message="Вы еще не подписаны!"
        )

def subConversation():
    chatID = event.chat_id # ID чата
    with open("chats.txt") as ids:
        chats = [row.strip() for row in ids]
    if (str(chatID) not in chats): # проверка на отсутствие подписки беседы и регистрация
        chat = open('chats.txt','r')
        prev = chat.read()
        chat.close()
        chat = open('chats.txt','w')
        if (len(chats) != 0):
            prev += '\n'
        chat.write(prev + str(chatID))
        vk.messages.send(
            chat_id=chatID,
            random_id = 0,
            message="Ваша беседа подписана!"
        )
        print(chatID, "group subscribed!");
        chat.close()
    else: # если подписка уже есть
        vk.messages.send(
            chat_id=chatID,
            random_id = 0,
            message="Ваша беседа уже подписана!"
        )

def unsubConversation():
    chatID = event.chat_id # ID чата
    with open("chats.txt") as ids:
        chats = [row.strip() for row in ids]
    if (str(chatID) in chats): # проверка на наличие подписки беседы и удаление
        text = ''
        for i in range(len(chats)):
            if chats[i] != str(chatID):
                text += str(chatID) + '\n'
        chat = open('chats.txt','w')
        chat.write(text)
        vk.messages.send(
            chat_id=chatID,
            random_id = 0,
            message="Ваша беседа отписана!"
        )
        print(chatID, "group unsubscribed!");
        chat.close()
    else: # если подписки нет
        vk.messages.send(
            chat_id=chatID,
            random_id = 0,
            message="Ваша беседа еще не подписана!"
        )
        
def addToDelayed(att):
    send = event.obj.text # текст, введенный юзером
    if (len(send) > 5): # действие с сообщением с текстом
        # создание списков людей, которым откладыватся рассылки #
        date = send[6:22]
        send = send[23:]
        with open("people.txt") as ids:
            users = [row.strip() for row in ids]
        with open("chats.txt") as ids:
            chat = [row.strip() for row in ids]

        #########################################################

        if (len(att) != 0): # отправка рассылки при наличии аттачментов
            print(send)
            print(att)
            print(date)
        else: # отправка рассылки без аттачментов
            print(send)
            print(date)
    else: # отправка рассылки без текста
        if (len(att) != 0): # но с аттачментами
            with open("people.txt") as ids:
                users = [row.strip() for row in ids]
            with open("chats.txt") as ids:
                chat = [row.strip() for row in ids]
            print(att)
    return   

def SendMessage():
    userID = event.obj.from_id # ИД юзера
    conv = vk.messages.getConversationsById(peer_ids = userID) # получение информации о диалоге
    lMes = conv.get('items')[0].get('last_message_id') # получение ID последнего сообщения в диалоге с пользователем
    stats = vk.messages.getById(
        message_ids = lMes,
        extended = 1
    )
    atts = stats.get('items')[0].get('attachments') # получение аттачментов сообщения
    att = '' # список аттачментов

    ### добавление аттачментов в список ###

    for i in range(len(atts)):
        attType = atts[i].get('type')
        att += attType + str(atts[i].get(attType).get('owner_id')) + '_' + str(atts[i].get(attType).get('id')) + ','
        if (str(atts[i].get(attType).get('access_key')) != 'None'):
            att = att[:len(att)-1]
            att += '_' + str(atts[i].get(attType).get('access_key')) + ','
    att = att[:len(att)-1] # обрезка запятой в конце

    #######################################

    send = event.obj.text # текст, введенный юзером
    if (len(send) > 11):
       if (send[8] == '.' or send[8] == '/' and send[11] == '.' or send[11] == '/' and send[19] == ':'):
           addToDelayed(att)
           return
    if (len(send) > 6): # действие с сообщением с текстом
        # создание списков людей, которым отсылаются рассылки #
        send = send[6:]
        with open("people.txt") as ids:
            users = [row.strip() for row in ids]
        with open("chats.txt") as ids:
            chat = [row.strip() for row in ids]

        #######################################################

        if (len(att) != 0): # отправка рассылки при наличии аттачментов
            for ids in users:
                vk.messages.send(
                    user_id=ids,
                    random_id = 0,
                    message = send,
                    attachment = att
                )
            for ids in chat:
                vk.messages.send(
                    chat_id=ids,
                    random_id = 0,
                    message = send,
                    attachment = att
                )
        else: # отправка рассылки без аттачментов
            for ids in users:
                vk.messages.send(
                    user_id=ids,
                    random_id = 0,
                    message = send,
                )
            for ids in chat:
                vk.messages.send(
                    chat_id=ids,
                    random_id = 0,
                    message = send,
                )
    else: # отправка рассылки без текста
        if (len(att) != 0): # но с аттачментами
            with open("people.txt") as ids:
                users = [row.strip() for row in ids]
            with open("chats.txt") as ids:
                chat = [row.strip() for row in ids]
            for ids in users:
                vk.messages.send(
                    user_id=ids,
                    random_id = 0,
                    attachment = att
                )
            for ids in chat:
                vk.messages.send(
                    chat_id=ids,
                    random_id = 0,
                    attachment = att
                )
    return

def isAdmin():
    userID = event.obj.from_id # ИД юзера
    with open("admins.txt") as ids: # чек айдишников админов
        adms = [row.strip() for row in ids]
    for ids in adms:
        if str(ids) == str(userID): # поиск ид пользователя среди админов
            sending = 1 # присвоение админки
    return (sending == 1)

def ProcessCommand():
    text = event.obj.text
    if (text == '/sub'):
        if (event.from_user):
            subUser()
        elif (event.from_chat):
            subConversation()
    elif (text == '/unsub'):
        if (event.from_user):
            unsubUser()
        elif (event.from_chat):
            unsubConversation()
    elif (text[:5] == '/send'):
        if (isAdmin()):
            SendMessage()
    return


####################### ВОТ ТУТ НАЧИНАЕТСЯ БОТ #######################
### авторизация ###
vk_session = vk_api.VkApi(token='212bfe399afff4b3ea2d0f12d16e2885fb92320f365f6fb514a56b6ae32f12de0456269c19df73e5503a1')
longpoll = VkBotLongPoll(vk_session, '174143158')
vk = vk_session.get_api()
###################

for event in longpoll.listen():
    if (event.type == VkBotEventType.MESSAGE_NEW): # если новое сообщение
        if (len(event.obj.text) != 0):
            if (event.obj.text[0] == '/'):
                ProcessCommand()

################# А ТУТ ОН КОНЧАЕТСЯ ##################################

# todo:
# 1. Отписка от беседы +
# 2. Возможность постить в нужные беседы и нужным людям
# 3. Отложенный постинг
# 4. Работа в режими "mention only"
# 5. Кнопочки
# 6. Рефакторинг +



