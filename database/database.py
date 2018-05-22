import time

import json

from sqlalchemy import create_engine
# Импортируем необходимые классы (типы данных, таблицы, метаданные, ключи)
from sqlalchemy import Table, Column, Integer, String, MetaData

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

class Database():
    def __init__(self):
        self.saved_data = dict()
    def save(self, data):
        self.saved_data.update({time.ctime():data})
        

class Filedatabase(Database):
    def __init__(self):
        Database.__init__(self)
        self.file = open('serverdata.txt', 'w')
    def savetofile(self, data):
        self.file.write(data)

# Функция declarative_base создаёт базовый класс для декларативной работы
Base = declarative_base()

# На основании базового класса можно создавать необходимые классы
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
    def __repr__(self):
        return "<User('%s','%s', '%s')>" % \
                     (self.name, self.fullname, self.password)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    senderid = Column(Integer)
    receiverid = Column(Integer)
    message = Column(String)
    timestamp = Column(String)
    
    def __init__(self, senderid, receiverid, message, timestamp):
        self.senderid = senderid
        self.receiverid = receiverid
        self.message = message
        self.timestamp = timestamp

    def __repr__(self):
        return "<Message('%s','%s', '%s', '%s')>" % \
            (self.senderid, self.receiverid, self.message, self.timestamp)

class UserHistory(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    logintime = Column(Integer)
    userip = Column(String)
    
    
    def __init__(self, userid, logintime, userip):
        self.userid = userid
        self.logintime = logintime
        self.userip = userip
        

    def __repr__(self):
        return "<Message('%s','%s', '%s', '%s')>" % \
            (self.userid, self.logintime, self.userip)		 

class SqliteDB():

	def __init__(self, path = 'sqlite:///ServerInfo.sqlite'):
	    engine = self.connect(path)
	    self.engine = engine
	    Session = sessionmaker(bind=engine)
	    session = Session()
	    self.session = session
	    self.path = path

	def connect(self, path):   
		
		return create_engine(path)

	def create_database(self, engine):
		# Подготовим "запрос" на создание таблицы users внутри каталога MetaData
		metadata = MetaData()
		users_table = Table('users', metadata,
		    Column('id', Integer, primary_key=True),
		    Column('name', String),
		    Column('fullname', String),
		    Column('password', String)
		)
		history_table = Table('history', metadata,
			Column('id', Integer, primary_key=True),
		    Column('userid', Integer),
		    Column('logintime', String),
		)
		contactlist_table = Table('contactlist', metadata,
			Column('id', Integer, primary_key=True),
		    Column('userid', Integer),
		    Column('conactid', Integer),
		)

		messages_table = Table('messages', metadata,
			Column('id', Integer, primary_key=True),
		    Column('senderid', Integer),
		    Column('receiverid', Integer),
		    Column('message', String),
		    Column('timestamp', String)
		)

		# Выполним запрос CREATE TABLE
		metadata.create_all(engine)

	def add_user(self, name, fullname, password):

		classic_user = User(name, fullname, password)
		self.session.add(classic_user)
		self.session.commit()

	def add_message(self, senderid, receiverid, message, timestamp):

		new_message = Message(senderid, receiverid, message, timestamp)
		self.session.add(new_message)
		self.session.commit()

	def get_all_messages(self, senderid, receiverid):

		return self.session.query(Message).filter_by(senderid=senderid,receiverid=receiverid).order_by(Message.id.asc()).all()

	def close_session(self):
		self.session.close()		


# a = SqliteDB()
# #a.create_database(a.engine)
# a.add_user("sergey", 'sergey savrasov', 'password')
# a.add_message('2','3','yo',time.ctime())
# q_user = a.session.query(Message).filter_by(message="yo").all()
# print('Simple query:', q_user)
# q_user = a.session.query(User).filter_by(name="sergey").first()
# print('Simple query:', q_user)
# msg = a.get_all_messages('2','3')
# print('All messages:', msg)
# a.close_session()


