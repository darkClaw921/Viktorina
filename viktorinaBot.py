import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from PIL import Image, ImageDraw, ImageFont

# VK API import
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api import VkUpload 

# OS import
import time
import os
from threading import Thread
import threading

# Help files import
import setings
import test 
import viktorinaCreateSheet
import viktorinaQuestions
import json


# VK setings
vk_session = vk_api.VkApi(token = setings.vkDdkgtaApi)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

viktorinaCreateSheet.createSheet()
viktorinaCreateSheet.createCell(len(viktorinaQuestions.questions))
sheet = viktorinaCreateSheet.sheet

questionsData = viktorinaQuestions.questions

nextQuestion = True 
usersId = [] # список людей которые уже учавствуют или уже прошли тест
usersId.append(0) # добавляем фантомного пльзователя 
start = False
rowQuestion = 5
columCell = 0
numberQestuon = 2

def inputNextQuestion():
    global nextQuestion

    while True:
        input('Отправить следующий вопрос? ')
        
        nextQuestion = False
        time.sleep(3)

        nextQuestion = True

Thread(target=inputNextQuestion).start()

def keyboardCreater(ButtonText1, ButtonText2, ButtonText3, ButtonText4): 
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(ButtonText1)
    keyboard.add_line()
    keyboard.add_button(ButtonText2)
    keyboard.add_line()
    keyboard.add_button(ButtonText3)
    keyboard.add_line()
    keyboard.add_button(ButtonText4)
    
    keyboard = keyboard.get_keyboard()

    return keyboard

def printQuestion(random_id, user_id):
    global columCell, questionsData, rowQuestion, nextQuestion
    
    countRegisterUser = sheet.get("A24")
    print(countRegisterUser)
    countRegisterUser = countRegisterUser[0]
    countRegisterUser = countRegisterUser[0]
    print(countRegisterUser)
    columCell = int(countRegisterUser)

    sheet.update_cell(24, 1, int(countRegisterUser) + 1)

    columCell += 2
    privateColumCell = columCell
    privateRowCell = rowQuestion

    
    firstConnection(user_id, privateColumCell)
    

    for question in questionsData:

        typeQuest = len(viktorinaQuestions.questions[question])

        photo = None
        keyboard = None

        print(typeQuest)
        if typeQuest == 1:
            if viktorinaQuestions.questions[question] != [''] :
                
                photo = viktorinaQuestions.questions[question]
        
        elif typeQuest == 5:
            
            photo = viktorinaQuestions.questions[question]
            keyboard = keyboardCreater(*viktorinaQuestions.questions[question])
        
        else:
            print(viktorinaQuestions.questions[question])
            keyboard = keyboardCreater(*viktorinaQuestions.questions[question]) # * что-то вроде разбиения 
            
        vk.messages.send(
                    user_id=user_id,
                    random_id=random_id,
                    attachment = photo,
                    message = question,
                    keyboard = keyboard
                )

        if getMessege(questionsData[question], user_id):

            otvet = vk.messages.getHistory(user_id = user_id, count = 1)
            # распарсили ответ
            otvet = otvet['items']
            otvet = otvet[0]
            otvet = otvet['text']

            sheet.update_cell(privateColumCell+1, privateRowCell, "1")
            sheet.update_cell(privateColumCell, privateRowCell, str(otvet))

            privateRowCell += 1

            while nextQuestion:
                time.sleep(1)
           
        else:
            
            otvet = vk.messages.getHistory(user_id = user_id, count = 1)
            
            # распарсили ответ
            otvet = otvet['items']
            otvet = otvet[0]
            otvet = otvet['text']

            sheet.update_cell(privateColumCell+1, privateRowCell, "0")
            sheet.update_cell(privateColumCell, privateRowCell, str(otvet))
            privateRowCell += 1
            
            while nextQuestion:
                time.sleep(1)
            
                    
def getMessege (stringOtvet, user_id): # Получаем сообщение от конкретного пользователя
    for event in longpoll.listen(): # цикл для каждго ивента сервера
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == user_id: # ждать ответа от данного юзера 
            vk.messages.getConversations(offset = 0, count = 1)  
    
            if event.text == stringOtvet: # если событие текст и он равен сообщению которое отправил пользователь
                return True

            return False

def newUser(userId):
    global columCell

    print("Проверка пользователя")

    try:

        usersId.index(userId)
        print("Cтарый пользователь")
        numberOfQuestion = usersId.index(userId) * 2
        print(f'Находиться в {numberOfQuestion} строке')

        # sheet.update_cell(1,30,'20')
        # sheet.update_cell(30,1,'43')
        # countRegisterUser = sheet.get("A30")
        # countRegisterUser = countRegisterUser[0]
        # countRegisterUser = countRegisterUser[0]
        # print(countRegisterUser)


        return False

    except ValueError:

        # countRegisterUser = sheet.get("A30")
        # countRegisterUser = countRegisterUser[0]
        # countRegisterUser = countRegisterUser[0]
        # print(countRegisterUser)
        # columCell = int(countRegisterUser)

        # columCell += 1
        # sheet.update_cell(2, 1, int(countRegisterUser) + 1)
        print("Новый пользователь")
        return True

    userInfo = vk.users.get(user_ids = event.user_id) 
    print(userInfo)# Получили ответ в виде массива из одного списка
    

def firstConnection(user_id, columCell):
    # global columCell

    userInfo = vk.users.get(user_ids = user_id)
    userInfo = userInfo[0] 

    # sheet.update_cell(columCell, 1, f"""vk.com/id{user_id}""")
    
    sheet.update_cell(columCell, 1, user_id)
    sheet.update_cell(columCell, 2, '1')
    sheet.update_cell(columCell, 3, userInfo["first_name"])
    sheet.update_cell(columCell, 4, userInfo["last_name"])

        
    print(f"Пользователь {user_id} подключился")

def checkWhoUser(user_id):
    """
    Проверет есть ли user_id в таблице 
    Если есть то возвращает cписок 
    (True, 'номер строки') иначе (False, номер строки')
    """
    countRegisterUser = sheet.get("A24")
    countRegisterUser = countRegisterUser[0][0]

    # for user in countRegisterUser:
    #     userID = sheet.get(f'A{user*2}')
    #     userID = userID[0][0]
    # print(countRegisterUser)
    # countRegisterUser = countRegisterUser[0]
    # countRegisterUser = countRegisterUser[0]
    # print(countRegisterUser)
    # columCell = int(countRegisterUser)

    # sheet.update_cell(24, 1, int(countRegisterUser) + 1)
    sheet.update_cell(24, 2, f'=MATCH({user_id}; A1:A{int(countRegisterUser)+1}; 0)')
    empetyUser = sheet.get("B24")
    empetyUser = empetyUser[0][0]
    print(empetyUser)

    if empetyUser == '#N/A':
        print('Такого нет')
        return False,empetyUser
    else:
        print('Такой есть ')
        return True,empetyUser

startMessage = '1'

print(checkWhoUser(34))

for event in longpoll.listen():
    print(event.type)
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        vk.messages.getConversations(offset = 0, count = 1) 

        startMessage = event.text 

        print(startMessage.lower)
        if (startMessage.lower == 'а' or 'a '):
            print(start)
            start = True
        else:
            print(start)
            start = False
        
        if start:

            # whoUser = newUser(event.user_id)
            whoUser = checkWhoUser(event.user_id)

            if not whoUser[0]:
                print("Новый пользователь - добавлен в базу")

                usersId.append(event.user_id)

                Thread(target=printQuestion, args=(event.random_id, event.user_id,)).start() # Запуск нового потока для нового пользвоателя
            else:
                print("Старый пользователь - действий не требуется")
        else: 
            start = False

