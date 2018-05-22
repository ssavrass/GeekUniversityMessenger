# -*- coding: utf-8 -*-

import socket

import settings

from jsonformat.jimprotocolclient import JSONResponse, JSONRequest

import zlib
        
#context manager
class ServerClientTransaction:
    
    def __enter__(self):
        print("Transaction started...")

    def __exit__(self, exc_type, value, traceback):
        print(exc_type, value, traceback)
        if exc_type is None:
            print("Transaction transmitted to server")
        return False

class ClientVerifier(type):
    def __new__(cls, clsname, superclasses, attributedict):
        print("clsname: ", clsname)
        print("superclasses: ", superclasses)
        print("attributedict: ", attributedict)
        return type.__new__(cls, clsname, superclasses, attributedict)             

class EchoClient(metaclass=ClientVerifier):

    def __init__(self):

        # Создаем экземпляр сокет соединения
        self._sock = socket.socket()

        # Связываем сокет соединение с хостом и портом сервера 
        self._sock.connect((settings.HOST, settings.PORT))
   
    def read(self):

        # Получаем данные с сервера
        bytes_data = self._sock.recv(settings.BUFFER_SIZE)

        # bytes_data = zlib.decompress(comp_data)

        # Приводим полученные данные к строковому виду
        JSON_data = JSONResponse(bytes_data)

        # Выводим полученные данные на экран
        print(JSON_data._envelope)

    def write(self, optional =''):

        # Вводим данные с клавиатуры
        if optional == '':
            str_data = input('Enter data: ')
        else:
            str_data = optional
            print(optional)

        JSONdata = JSONRequest("Send to server",str_data)
        #server
        JSONdata.add_header('server', settings.HOST)
        #port
        JSONdata.add_header('port', settings.PORT)
       
      

        # Приводим отправляемые данные к байтовому виду
        bytes_data = JSONdata.to_bytes()

        # comp_data = zlib.compress(bytes_data)

        # Отправляем данные на сервер
        self._sock.send(bytes_data)
    
    def perform_run(self):

        pass

    def run(self):

        try:

            while True:
                with ServerClientTransaction() as transaction:

                    # Вводим данны и отправляем на сервер
                    self.write()

                    # Получаем ответ сервера
                    self.read()

                    self.perform_run()

        except KeyboardInterrupt:

            # Обрабатываем сочетание клавишь Ctrl+C
            pass





if __name__ == '__main__':

     client = EchoClient()

     client.run() 