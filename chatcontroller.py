# -*- coding: utf-8 -*-
from client import EchoClient

import settings

import zlib

from jsonformat.jimprotocolclient import JSONResponse, JSONRequest

class ChatController(EchoClient):
    
    def __init__(self):
        EchoClient.__init__(self)

    def send(self, input_data):

        str_data = input_data
            
        JSONdata = JSONRequest("Send to server",str_data)
        #server
        JSONdata.add_header('server', settings.HOST)
        #port
        JSONdata.add_header('port', settings.PORT)

        #client
        JSONdata.add_header('client', self._sock.getsockname())
       
        # Приводим отправляемые данные к байтовому вид
        bytes_data = JSONdata.to_bytes()

        # comp_data = zlib.compress(bytes_data)

        # Отправляем данные на сервер
        self._sock.send(bytes_data)

    def read(self):

            # Получаем данные с сервера
            bytes_data = self._sock.recv(settings.BUFFER_SIZE)

            # bytes_data = zlib.decompress(comp_data)

            # Приводим полученные данные к строковому виду
            JSON_data = JSONResponse(bytes_data)

            # Выводим полученные данные на экран
            print(JSON_data._envelope)



