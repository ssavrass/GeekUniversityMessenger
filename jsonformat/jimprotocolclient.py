# -*- coding: utf-8 -*-
import json

import settings

# Response-объект - используется для преобразования "сырых" данных (байтов) в python-объект
class JSONResponse():

    # Конструктор в качестве аргументов принимает исключительно "сырые" данные
    # Внутри конструктора "сырые" данные преобразуются в словарь
    def __init__(self, message_bytes):

        message_str = message_bytes.decode(settings.ENCODING)

        self._envelope = json.loads(message_str)


    @property
    def code(self):

        # Read only свойство code
        code = self._envelope.get('code')

        return code


    @property
    def action(self):

        # Read only свойство action
        action = self._envelope.get('action')

        return action


    @property
    def headers(self):

        # Read only свойство headers
        # Свойство headers содержит дополнительные данные об ответе сервера, например время его совершения
        headers = self._envelope.get('headers')

        for key, value in headers.items():

            yield key, value


    @property
    def body(self):

        # Read only свойство body
        # Свойство body содержит тело ответа сервера
        body = self._envelope.get('body')

        return body


# Request-объект - используется для приведения python-объекта в байтовый вид (для генерации "сырых" данных)
class JSONRequest:

    # Конструктор в качестве аргументов принимает основные данные о запросе
    def __init__(self, action, body, **headers):

        self._headers = headers

        self._action = action

        self._body = body


    # Метод add_header - используется для добавления дополнительных данных о запросе, например времени его совершения
    def add_header(self, key, value):

        self._headers.update({key:value})


    # Метод add_header - используется для удаления дополнительных данных о запросе, если во время его заполнения была допущена ошибка
    def remove_header(self, key):

        del self._headers[key]


    # Метод to_bytes - используется для преобразования данных о запросе в байты
    def to_bytes(self):

        envelope = dict()

        envelope.update({'action':self._action})

        envelope.update({'headers':self._headers})

        envelope.update({'body':self._body})

        data_str = json.dumps(envelope)

        return data_str.encode(settings.ENCODING)