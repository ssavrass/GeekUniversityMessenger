# -*- coding: utf-8 -*-
#meta class single tone

import asyncio

import threading

import settings

import socket

import select

import collections

import time

import json

from server import EchoServer

from database import SqliteDB

from jsonformat.jimprotocolserver import JSONResponse, JSONRequest

from authenticate import server_authenticate


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
      

    def connect(self, secret_key):

        try:

            # Получаем подключение клиента
            client, address = self._sock.accept()
            if server_authenticate(client, secret_key):
            # Сохраняем подключение клиента
                self._connections.append(client)
            else:
                client.close()
                

        except OSError:

            # Обрабатываем timeout сервера
            pass
                        
    def mainloop(self):
        
        try:

            while True:

                # Обрабатываем подключения к серверу
                self.connect(b'secretkey')

                self.perform_mainloop()
                
                # coro = self.create_server

                # server = self.loop

                # Определяем коллекции готовых к записи или чтению клиентских socket-объектов
                rlist, wlist, xist = select.select(self._connections, self._connections, [], 0)

                print('waiting')
    
                time.sleep(1)                 

           

                # Если клиентский socket-объект готов к чтению, получаем данные от клиента
                for client in rlist:
                    
                    try:
                        thread = threading.Thread(target=self.read, args=(client,), daemon = True)
                        thread.start()
                    except (ConnectionResetError, BrokenPipeError):

                        self._connections.remove(client)
    


                # Если клиентский socket-объект готов к записи, отправляем сообщения на клиент

                if self._requests:
                    request = self._requests.pop()
                    
                    for client in wlist:
                    # Извлекаем первый запрос
                    
                        print(request._envelope)
                        self.database.add_message(1, 2, request.body, time.ctime())

                        try:
                            thread = threading.Thread(target=self.write, args=(client, request,), daemon = True)
                            thread.start()
                        except (ConnectionResetError, BrokenPipeError):

                            self._connections.remove(client)
                

               

                    
                
   
        except KeyboardInterrupt:
            self.database.session.close()
            # Обрабатываем сочетание клавишь Ctrl+C
            
            pass
                    

if __name__ == '__main__':

    chat = Chat()

    chat.mainloop()

    #print(chat._connections)



