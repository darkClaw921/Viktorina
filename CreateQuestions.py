r"""
Создает файл с вопросами на основе шаблона из баззы вопросов 

Шаблон 
    Вопрос$Ответ&photo-194390511_457239113@Кнопка1 кнопка2 кнопка3 кнопка4
Формат созданного файла  
    Eсли в шаблоне небудет какогото элемента то он будет равен None
    'Ответ' : None,

    questions = { 
    'Вопрос 1' : {'Вопрос': 'Вопрос ', 
                'Ответ' : 'Ответ ', 
                'Фото' : 'photo-194390511_457239113', 
                'Клавиатура' : 'Кнопка1 кнопка2 кнопка3 кнопка4'
                },
"""
import re

fileQuestionsRead = open('/Users/igorgerasimov/Desktop/Python/Viktorina/questionsViktorina.txt')
fileQuestionsWrite = open('/Users/igorgerasimov/Desktop/Python/Viktorina/viktorinaQuestionsTest.py', 'w')

numberQuestion = 0 
fileQuestionsWrite.write('questions = { ')

for line in fileQuestionsRead:
    try:
        numberQuestion += 1 
        questions = re.split(r'[$&@]', line)

        count = 0

        for element in questions:
            if element == '':
                questions[count] = None
            else:
                element = element.split('\n')
                questions[count] = f"""'{element[0]}'"""
            count += 1

        openSkoba = '{'
        closeSkoba = '}'

        fileQuestionsWrite.write(f"""
    'Вопрос {numberQuestion}' : {openSkoba}'Вопрос': {questions[0]}, 
                'Ответ' : {questions[1]}, 
                'Фото' : {questions[2]}, 
                'Клавиатура' : {questions[3]}
                {closeSkoba},""")
        

    except BaseException:
        print("возникло исключение")
        continue

fileQuestionsWrite.write('\n}')
fileQuestionsRead.close
fileQuestionsWrite.close
