# -*- coding: utf-8 -*-

import settings

import socket

import select

import collections

from jsonformat.jimprotocolserver import JSONResponse, JSONRequest

import time

import logging

import zlib

# Быстрая настройка логгирования может быть выполнена так:
logging.basicConfig(
    filename = "app_01.log",
    format = "%(levelname)-10s %(asctime)s %(message)s",
    level = logging.INFO
)

# Для использования логгера его нужно получить/создать функцией getLogger
log = logging.getLogger('basic')

#context manager
class ServerClientTransaction:
    
    def __enter__(self):
        print("Server waiting for message from client...")

    def __exit__(self, exc_type, value, traceback):
        print(exc_type, value, traceback)
        if exc_type is None:
            print("Message from client received")
        return False

class ServerVerifier(type):
    def __new__(cls, clsname, superclasses, attributedict):
        print("clsname: ", clsname)
        print("superclasses: ", superclasses)
        print("attributedict: ", attributedict)
        if not 'mainloop' in attributedict:
            raise "No mainloop"
        return type.__new__(cls, clsname, superclasses, attributedict)           


class EchoServer(metaclass=ServerVerifier):

    def __init__(self):

        # Создаем список для хранения клиентских соединений
        self._connections = dict()

        # Создаем список для хранения клиентских запросов
        self._requests = dict()

        # Создаем экземпляр сокет соединения
        self._sock = socket.socket()

        # Связываем сокет соединение с хостом и портом сервера 
        self._sock.bind((settings.HOST, settings.PORT))

        # Ждем обращений клиентов 
        self._sock.listen(settings.CLIENTS_NUM)

        # Отпределяем время ожидания запроса клиента 
        self._sock.settimeout(settings.TIMEOUT)


    def connect(self):

        try:

            # Получаем подключение клиента
            client, address = self._sock.accept()

            # Сохраняем подключение клиента
            self._connections.update({address:client})

        except OSError:

            # Обрабатываем timeout сервера
            pass
   
    
    
    def action(func):
        
        def func_wrapper(*args):
            
            if func.__name__ == 'read':
                self = args[0]
                client = args[1]
                address = args[2]
            
                str_address = address[0] + ':' + str(address[1])
                # Получаем данные от клиента
                data = client.recv(settings.BUFFER_SIZE)

                # Если полученные данные не являются пустой строкой 
                if data:

                    # Приводим полученные данные к строковому виду
                    # data = zlib.decompress(comp_data)
                    JSON_data = JSONRequest(data)


                    # Сохраняем запрос на сервере
                    self._requests.update({str_address:JSON_data})
                
                     


            if func.__name__ == 'write': 
               
                self = args[0]
                client = args[1]
                request = args[2] 
                address = args[3]
                
                
                    
                # Приводим отправляемые данные к байтовому виду
                

                JSON_message = JSONResponse("200", "server received message from client", request.body)
                
                for key, value in request.headers:
                    JSON_message.add_header(key, value)
                
                bytes_message = JSON_message.to_bytes()

                # comp_data = zlib.compress(bytes_message)

                # Отправляем данные на клиент
                client.send(bytes_message)
                
            

        return func_wrapper  
    

    @action
    def read(self, client, address):

        pass

    @action
    def write(self, client, request, address):

        pass

    def perform_mainloop(self):
        
        pass            

    def mainloop(self):

        try:

            while True:

                

                # Обрабатываем подключения к серверу
                self.connect()

                self.perform_mainloop()

                # Создаем копию словаря подключений для возможности в дальнейшем вносить изменения в оригинал
                work_copy = self._connections.copy()
                log.info(self._connections)
                # Извлекаем коллекцию клиентских socket-объектов
                clients = work_copy.values()

                # Определяем коллекции готовых к записи или чтению клиентских socket-объектов
                rlist, wlist, xist = select.select(clients, clients, [], 0)

                print('wating')

                time.sleep(2)
    

                for address, client in work_copy.items():
                    
                    # Сохраняем запрос клиента к серверу
                    with ServerClientTransaction() as transaction:
                        
                        try:

                            # Если клиентский socket-объект готов к чтению, получаем данные от клиента
                            if client in rlist:
                                log.info("Server log read")
                                self.read(client, address)


                            # Если клиентский socket-объект готов к записи, отправляем сообщения на клиент
                            if client in wlist:
                                str_address = address[0] + ':' + str(address[1])
                                if self._requests:
                                    log.info("Server log write")
                                    # Извлекаем первый запрос
                                    request = self._requests[str_address]

                                    print(request._envelope)

                                    time.sleep(2)

                                    # Отправляем запрос слиенту
                                    self.write(client, request, address)

                                    self._requests = dict()

                        
                        except (ConnectionResetError, BrokenPipeError) as err:

                            # В случае разрыва соединения с клиентом и наличии данного клиента в списке подключений
                            log.exception('deleted', exc_info=err)
                            del self._connections[address]
       
        except KeyboardInterrupt as err:

            # Обрабатываем сочетание клавишь Ctrl+C
            log.exception('KeyboardInterrupt', exc_info=err)
            pass




if __name__ == '__main__':

    server = EchoServer()

    server.mainloop()