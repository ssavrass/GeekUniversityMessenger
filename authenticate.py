import hmac
import os
import sys
from database import SqliteDB
import socket
 
def client_authenticate(connection, secret_key):
    ''' Аутентификация клиента на удаленном сервисе.
        Параметр connection - сетевое соединение (сокет);
        secret_key - ключ шифрования, известный клиенту и серверу
    '''
    message = connection.recv(32)
    hash = hmac.new(secret_key, message)
    digest = hash.digest()
    connection.send(digest)

def server_authenticate(connection, secret_key):
    ''' Запрос аутентификаии клиента.
        сonnection - сетевое соединение (сокет);
        secret_key - ключ шифрования, известный клиенту и серверу
    '''
    # 1. Создаётся случайное послание и отсылается клиентв
    message = os.urandom(32)
    connection.send(message)

    # 2. Вычисляется HMAC-функция от послания с использованием секретного ключа
    hash = hmac.new(secret_key, message)
    digest = hash.digest()

    # 3. Пришедший ответ от клиента сравнивается с локальным результатом HMAC
    response = connection.recv(len(digest))
    return hmac.compare_digest(digest, response)


def login_required(func):
    
    def func_wrapper(*args):
        client = args[1]
        db = SqliteDB()
        while True:
            print("What would you like to do? (enter number 1, 2, 3) \n 1 login with username and password \n 2 create new user \n 3 exit ")
            data = input("Enter number: ")
            if data == "1":          
                username = input("Enter Username: \n")
                password = input("Enter Password: \n")
                if db.authenticate_user(username,password) == True:
                    print("Successfuly Authenticated!")
                    client_authenticate(client, b'secretkey')
                    break
                    
                else:
                    print("username or password incorrect type 3 to exit, 1 to try again")

            if data == "2":
                name = input("Enter Username: \n")
                fullname = input("Enter Full Name: \n")
                password = input("Enter Password: \n")
                db.add_user(name, fullname, password)
            if data == "3":
                sys.exit()
        db.close_session()
        return func(*args)
    return func_wrapper

def login_requiredgraphic(func):
    
    def func_wrapper(*args):
        
        username = args[1]
        password = args[2]
        db = args[3]
        if db.authenticate_user(username,password) == True:
            print("Successfuly Authenticated!")
            #client_authenticate(client, b'secretkey')
            return True
                   
        else:
            print("username or password incorrect")   
            return False
    return func_wrapper

