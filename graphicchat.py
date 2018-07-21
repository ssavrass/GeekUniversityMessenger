# -*- coding: utf-8 -*-

import settings

from chatcontroller import ChatController

import threading

import time

from jsonformat.jimprotocolclient import JSONResponse, JSONRequest

import sys

from authenticate import login_required, login_requiredgraphic

from database import SqliteDB

class GraphicChat(ChatController):

	def __init__(self):
		ChatController.__init__(self)
		self.response = []
		self.db = SqliteDB()
		self.senderid = self.db.senderid
		self.recieverid = self.db.recieverid

	def send(self, input_data):

		self.senderid = self.db.senderid
		self.recieverid = self.db.recieverid
		
		str_data = input_data
		    
		JSONdata = JSONRequest("Send to server",str_data)
		#server
		JSONdata.add_header('server', settings.HOST)
		#port
		JSONdata.add_header('port', settings.PORT)

		#client
		JSONdata.add_header('client', self._sock.getsockname())

		#senderid
		JSONdata.add_header('senderid', self.senderid)

		#recieverid
		JSONdata.add_header('recieverid', self.recieverid)

		# Приводим отправляемые данные к байтовому вид
		bytes_data = JSONdata.to_bytes()

		# comp_data = zlib.compress(bytes_data)

		# Отправляем данные на сервер
		self._sock.send(bytes_data)

	def read(self):
		
		while True:
		    # Получаем данные с сервера
		    bytes_data = self._sock.recv(settings.BUFFER_SIZE)

		    # bytes_data = zlib.decompress(comp_data
		    if bytes_data:

		        # Приводим полученные данные к строковому виду
		        JSON_data = JSONResponse(bytes_data)

		        # Выводим полученные данные на экран
		        print(JSON_data._envelope)

		        if JSON_data._envelope['headers']['recieverid'] == self.senderid:
			        self.response.append(JSON_data._envelope)
	
	
	@login_requiredgraphic  
	def login_user(self, username, password, db):
		
		pass

    
        

class ConsoleChat(ChatController):

	def __init__(self):
	    ChatController.__init__(self)

	
	def write(self):

		while True:
			data = input('Enter data: ')
			self.send(data)
	
		
	def read(self):
		
		while True:
		    # Получаем данные с сервера
		    bytes_data = self._sock.recv(settings.BUFFER_SIZE)

		    # bytes_data = zlib.decompress(comp_data
		    if bytes_data:

		        # Приводим полученные данные к строковому виду
		        JSON_data = JSONResponse(bytes_data)

		        # Выводим полученные данные на экран
		        print(JSON_data._envelope)
		
	        
	@login_required      
	def run(self, client):
		
		try:

			 #отправляем на сервер
			#self.send(data)
			threading1 = threading.Thread(target=self.read)
			threading1.daemon = True
			threading1.start()
			threading2 = threading.Thread(target=self.write)
			threading2.start()
			#self.write()
		

		except KeyboardInterrupt:
			pass




if __name__ == '__main__':

	client = ConsoleChat()

	client.run(client._sock)