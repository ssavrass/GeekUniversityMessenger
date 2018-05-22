# -*- coding: utf-8 -*-
#meta class single tone

import settings

import socket

import select

import collections

import time

import json

from server import EchoServer

from database.database import SqliteDB

from jsonformat.jimprotocolserver import JSONResponse, JSONRequest


class Descriptor():

    def __init__(self, val = None, name = None):
        self.val = val
        self.name = name

    def __get__(self, obj, objtype):
        print('Retrieving', self.val) 
        return self.val

    def __set__(self, obj, val):
        print ('Updating', self.name)
        self.val = val


class Chat(EchoServer):


    def __init__(self):
        EchoServer.__init__(self)
        self.database = SqliteDB()
        self.desc = Descriptor()
                        
    def mainloop(self):
        
        try:

            while True:

                # Обрабатываем подключения к серверу
                self.connect()

                self.perform_mainloop()

                # Создаем копию словаря подключений для возможности в дальнейшем вносить изменения в оригинал
                work_copy = self._connections.copy()
                
                # Извлекаем коллекцию клиентских socket-объектов
                clients = work_copy.values()

                # Определяем коллекции готовых к записи или чтению клиентских socket-объектов
                rlist, wlist, xist = select.select(clients, clients, [], 0)

                print('waiting')
    
                time.sleep(1)

                for address, client in work_copy.items():
                    
                    # Сохраняем запрос клиента к серверу
                    
                        
                    try:

                        # Если клиентский socket-объект готов к чтению, получаем данные от клиента
                        if client in rlist:
                            
                            self.read(client, address)


                        # Если клиентский socket-объект готов к записи, отправляем сообщения на клиент
                        if client in wlist:
                            str_address = address[0] + ':' + str(address[1])
                            if self._requests:
                                
                                # Извлекаем первый запрос
                                request = self._requests[str_address]

                                print(request._envelope)
                                self.database.add_message(1, 2, request.body, time.ctime())

                                time.sleep(2)

                                # Отправляем запрос слиенту
                                self.write(client, request, address)

                                self._requests = dict()

                    
                    except (ConnectionResetError, BrokenPipeError) as err:

                        # В случае разрыва соединения с клиентом и наличии данного клиента в списке подключений
                        
                        del self._connections[address]
   
        except KeyboardInterrupt:
            self.database.session.close()
            # Обрабатываем сочетание клавишь Ctrl+C
            
            pass
                    

if __name__ == '__main__':

    chat = Chat()

    chat.mainloop()

    #print(chat._connections)



