import datetime
import threading
import time
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType


    
def subUser(event):
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


def unsubUser(event):
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

def subConversation(event):
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

def unsubConversation(event):
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
        
def addToDelayed(event, att):
    send = event.obj.text # текст, введенный юзером
    if (len(send) > 5): # действие с сообщением с текстом
        # создание списков людей, которым откладыватся рассылки #
        date = send[6:22]
        send = send[23:]
        if (len(send) != 0):

            #########################################################
            with open("dates.txt") as ids:
                dates = [row.strip() for row in ids]
            text = ''
            for i in range(len(dates)):
                text += dates[i] + '\n'
            text += date + '\n'
            dt = open("dates.txt", mode = 'w')
            dt.write(text)
            dt.close()

            name = str(len(dates)+1) + ".txt"
            delayed = open(name, mode = 'w')

            inp = ''
            if (len(att) != 0): # отправка рассылки при наличии аттачментов
                inp += 'att: ' + att + '\n'
                inp += 'send: ' + send
            else: # отправка рассылки без аттачментов
                inp += 'send: ' + send
        else: # отправка рассылки без текста
            if (len(att) != 0): # но с аттачментами
                inp += 'att: ' + att
        
        delayed.write(inp)
        delayed.close()
    return   

def PostDelayed():
    longpoll = VkBotLongPoll(vk_session, '174143158')
    while (True):
        now = datetime.datetime.now()
        with open("dates.txt") as ids:
            dates = [row.strip() for row in ids]
        for i in range(len(dates)):
            day = int(dates[i][0] + dates[i][1])
            month = int(dates[i][3] + dates[i][4])
            year = int(dates[i][6] + dates[i][7] + dates[i][8] + dates[i][9])
            hour = int(dates[i][11] + dates[i][12])
            minute = int(dates[i][14] + dates[i][15])

            curTime = time.ctime(time.time()).split()
            curDay = int(curTime[2])
            curMonth = curTime[1]
            if curMonth == 'Jan':
                curMonth = 1
            elif curMonth == 'Feb':
                curMonth = 2
            elif curMonth == 'Mar':
                curMonth = 3
            elif curMonth == 'Apr':
                curMonth = 4
            elif curMonth == 'May':
                curMonth = 5
            elif curMonth == 'Jun':
                curMonth = 6
            elif curMonth == 'Jul':
                curMonth = 7
            elif curMonth == 'Aug':
                curMonth = 8
            elif curMonth == 'Sep':
                curMonth = 9
            elif curMonth == 'Oct':
                curMonth = 10
            elif curMonth == 'Nov':
                curMonth = 11
            elif curMonth == 'Dec':
                curMonth = 12
            curYear = int(curTime[4])
            curTime = curTime[3]
            curHour = int(curTime[0] + curTime[1])
            curMinute = int(curTime[3] + curTime[4])
            if (curYear == year and curMonth == month and curDay == day and curHour == hour and curMinute == minute):
                with open(str(i+1) + ".txt") as ids:
                    sends = [row.strip() for row in ids]
                
                with open("people.txt") as ids:
                    users = [row.strip() for row in ids]
                with open("chats.txt") as ids:
                    chat = [row.strip() for row in ids]
                if len(sends) != 1:
                    for ids in users:
                        vk.messages.send(
                            user_id=ids,
                            random_id = 0,
                            message = sends[1][6:],
                            attachment = sends[0][5:]
                        )
                    for ids in chat:
                        vk.messages.send(
                            chat_id=ids,
                            random_id = 0,
                            message = sends[1][6:],
                            attachment = sends[0][5:]
                        )
                else:
                    if (sends[0][0:3] == 'att'):
                        for ids in users:
                            vk.messages.send(
                                user_id=ids,
                                random_id = 0,
                                attachment = sends[0][5:]
                            )
                        for ids in chat:
                            vk.messages.send(
                                chat_id=ids,
                                random_id = 0,
                                attachment = sends[0][5:]
                            )
                    elif(sends[0][0:4] == 'send'):
                        for ids in users:
                            vk.messages.send(
                                user_id=ids,
                                random_id = 0,
                                message = sends[0][6:]
                            )
                        for ids in chat:
                            vk.messages.send(
                                chat_id=ids,
                                random_id = 0,
                                message = sends[0][6:]
                            )
                        
                    

        time.sleep(60)
        
def SendMessage(event):
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
           addToDelayed(event, att)
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

def isAdmin(event):
    userID = event.obj.from_id # ИД юзера
    with open("admins.txt") as ids: # чек айдишников админов
        adms = [row.strip() for row in ids]
    for ids in adms:
        if str(ids) == str(userID): # поиск ид пользователя среди админов
            sending = 1 # присвоение админки
    return (sending == 1)


def Bot():
    longpoll = VkBotLongPoll(vk_session, '174143158')
    for event in longpoll.listen():
        if (event.type == VkBotEventType.MESSAGE_NEW): # если новое сообщение
            if (len(event.obj.text) != 0):
                if (event.obj.text[0] == '/'):
                    text = event.obj.text
                    if (text == '/sub'):
                        if (event.from_user):
                            subUser(event)
                        elif (event.from_chat):
                            subConversation(event)
                    elif (text == '/unsub'):
                        if (event.from_user):
                            unsubUser(event)
                        elif (event.from_chat):
                            unsubConversation(event)
                    elif (text[:5] == '/send'):
                        if (isAdmin(event)):
                            SendMessage(event)

vk_session = vk_api.VkApi(token='212bfe399afff4b3ea2d0f12d16e2885fb92320f365f6fb514a56b6ae32f12de0456269c19df73e5503a1')
# longpoll = VkBotLongPoll(vk_session, '174143158')
vk = vk_session.get_api()

post = threading.Event()
postThread = threading.Thread(target=PostDelayed)

bot = threading.Event()
botThread= threading.Thread(target = Bot)

postThread.start()
botThread.start()

post.set()

postThread.join()
botThread.join()





################# А ТУТ ОН КОНЧАЕТСЯ ##################################

# todo:
# 1. Отписка от беседы +
# 2. Возможность постить в нужные беседы и нужным людям
# 3. Отложенный постинг TBA
# 4. Работа в режими "mention only"
# 5. Кнопочки
# 6. Рефакторинг +



