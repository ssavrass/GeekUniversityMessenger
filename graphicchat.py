# -*- coding: utf-8 -*-

import settings

from chatcontroller import ChatController

class GraphicChat(ChatController):

    def __init__(self):
        ChatController.__init__(self)

class ConsoleChat(GraphicChat):

    def __init__(self):
        GraphicChat.__init__(self)

    def write(self):
        str_data = input('Enter data: ')
        return str_data

    def run(self):

        try:

            while True:
                
                # Вводим данны
                data = self.write()

                 #отправляем на сервер
                self.send(data)

                # Получаем ответ сервера
                self.read()


        except KeyboardInterrupt:

            # Обрабатываем сочетание клавишь Ctrl+C
            pass    




if __name__ == '__main__':

    client = ConsoleChat()

    client.run()