import pymongo as pm
from database import SqliteDB, User, Message

conn = pm.MongoClient("localhost", 27017)

db = conn.messenger

users = db.users
messages = db.messages


sqldb = SqliteDB()

allusers = sqldb.session.query(User).all()

allmessages = sqldb.session.query(Message).all()

for user in allusers:
	users.insert({'id':str(user.id),'name':user.name, 'fullname':user.fullname, 'password':user.password})

for message in allmessages:
	messages.insert({'id':str(message.id),'senderid':message.senderid, 'receiverid':message.receiverid, 'message':message.message, 'timestamp':message.timestamp})	


print(list(users.find({'id':'2'})))
print(list(messages.find({'id':'2'})))

users.remove()
messages.remove()