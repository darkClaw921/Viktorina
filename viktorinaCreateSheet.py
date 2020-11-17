import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Global variable
sheet = None

def createSheet():
    global sheet

    print('Создание таблицы ...')
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'] # что то для чего-то нужно Костыль
    creds = ServiceAccountCredentials.from_json_keyfile_name("/Users/igorgerasimov/Desktop/Python/intelectCasino/ViktorinaProfkom-50c0fbdcd821.json", scope) # Секретынй файл json для доступа к API
    client = gspread.authorize(creds)
    sheet = client.open('intelCasino').sheet1 # Имя таблицы
    print('Таблица создана')
    
    
    
def createCell(countCell):
    global sheet

    print('Создание ячеек...')

    sheet.update_cell(1, 1, "id пользователя")
    sheet.update_cell(1, 2, "Номер вопроса")
    sheet.update_cell(1, 3, "Имя ")
    sheet.update_cell(1, 4, "Фамилия")
    sheet.update_cell(1, 5, "Название команды")
    indexCell = 5

    # for numberQues in range(countCell):
    #     indexCell += 1
    #     sheet.update_cell(1, indexCell, f"Вопрос {numberQues+1}")

    print('Ячейки созданы')

