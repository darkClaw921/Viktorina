fileData = open('/Users/igorgerasimov/Desktop/Python/Viktorina/dataBaseUser.txt', "r+")

def addUserInDataBase(userId=int, numberOfQuestion=None):
    fileData.write(f"{userId} {numberOfQuestion} \n")
    pass

def checkForUserInDataBase(userId=int):
    numberOfLine = 1
    for user in fileData:
        user = user.split(" ")
        print(user)

        if int(user[0]) == userId:
            return print('True',numberOfLine)
        else:
            numberOfLine += 1

    return print('False')

def getUserData(userId=int):
    pass

addUserInDataBase(1233142112,'Вопрос 1')
checkForUserInDataBase(1233142111)

fileData.close
