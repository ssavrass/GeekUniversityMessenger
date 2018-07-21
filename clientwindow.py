# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clientwindow2.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

import sys, os
import io
# sys.path.append('/home/ssavrass/Documents/GeekBrainsPython/Course6HW/jim/database')
from PIL import Image, ImageDraw #Подключим необходимые библиотеки.
from PIL.ImageQt import ImageQt
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QMenuBar, QLabel, QFileDialog
from PyQt5.QtGui import QIcon, QFont, QPixmap
from database import SqliteDB, Message, User
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer
from graphicchat import GraphicChat
import threading
from authenticate import client_authenticate


class Login(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(Login, self).__init__()
        self.chat = GraphicChat()
        self.loginUi()
        self.show()
        self.user = ""

    
    def loginUi(self):
        self.setObjectName("Dialog")
        self.resize(400, 300)
        self.lineEdit1 = QtWidgets.QLineEdit(self)
        self.lineEdit1.setGeometry(QtCore.QRect(90, 70, 261, 27))
        self.lineEdit1.setObjectName("lineEdit1")
        self.lineEdit2 = QtWidgets.QLineEdit(self)
        self.lineEdit2.setGeometry(QtCore.QRect(90, 140, 261, 27))
        self.lineEdit2.setObjectName("lineEdit2")
        self.loginButton = QtWidgets.QPushButton(self)
        self.loginButton.setGeometry(QtCore.QRect(250, 190, 99, 27))
        self.loginButton.setObjectName("loginButton")
        self.loginButton.clicked.connect(lambda: self.login(self.lineEdit1.text(), self.lineEdit2.text(), self.chat.db))
        self.pushButton2 = QtWidgets.QPushButton(self)
        self.pushButton2.setGeometry(QtCore.QRect(250, 220, 99, 27))
        self.pushButton2.setObjectName("pushButton2")
        self.pushButton2.clicked.connect(lambda: self.close())
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setGeometry(QtCore.QRect(90, 50, 91, 17))
        self.label1.setObjectName("label1")
        self.label2 = QtWidgets.QLabel(self)
        self.label2.setGeometry(QtCore.QRect(90, 120, 71, 17))
        self.label2.setObjectName("label2")

        self.retranslateloginUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateloginUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Login"))
        self.loginButton.setText(_translate("Dialog", "Login"))
        self.pushButton2.setText(_translate("Dialog", "Exit"))
        self.label1.setText(_translate("Dialog", "Username"))
        self.label2.setText(_translate("Dialog", "Password"))

    def login(self, username, password, database):
       
        if self.chat.login_user(username, password, database) == True:
            self.user = username
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Bad user or password') 

   

    

# class Login(QtWidgets.QDialog):
#     def __init__(self, parent=None):
#         super(Login, self).__init__(parent)
#         self.textName = QtWidgets.QLineEdit(self)
#         self.textPass = QtWidgets.QLineEdit(self)
#         self.buttonLogin = QtWidgets.QPushButton('Login', self)
#         self.buttonLogin.clicked.connect(self.handleLogin)
#         layout = QtWidgets.QVBoxLayout(self)
#         layout.addWidget(self.textName)
#         layout.addWidget(self.textPass)
#         layout.addWidget(self.buttonLogin)
        

#     def handleLogin(self):
#         if (self.textName.text() == 'foo' and
#             self.textPass.text() == 'bar'):
#             self.accept()
#         else:
#             QtWidgets.QMessageBox.warning(
#                 self, 'Error', 'Bad user or password')



class ClientWindow(QMainWindow):
    def __init__(self, parent=None):
        self.app = QtWidgets.QApplication(sys.argv)
        super(ClientWindow, self).__init__(parent)

    
        self.login = Login()
        self.chat = self.login.chat
        self.contactlist = {}
    
        if self.login.exec_() == QtWidgets.QDialog.Accepted:

            client_authenticate(self.chat._sock, b'secretkey')  

            self.database = self.chat.db
            self.setupUi()
            self.tickertimer = QTimer()
            self.clientlist = []
            self.tickertimer.timeout.connect(lambda: self.update_chat())
            self.delay = 1000 #ms (1s = 1000ms
            self.tickertimer.start(self.delay)
            self.senderid = self.chat.db.senderid
            self.chat.db.recieverid = 1
            self.recieverid = self.chat.db.recieverid
            self.show()
            self.chat.send("USER ONLINE")
            sys.exit(self.app.exec_())

        



    # def login(self, username, password):

    #     if self.chat.login_user(username, password) == True:
    #         self.logged_in = True



    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(850, 650)
        self.lbl = QLabel(self)
        self.lbl.move(580,440)
        self.lbl.resize(150,150)
        self.get_avatar_image()
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(70, 420, 491, 111))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(450, 540, 111, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.send_message(self.senderid, self.recieverid, self.textEdit.toPlainText()))
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 20, 67, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(620, 20, 67, 17))
        self.label_2.setObjectName("label_2")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(70, 40, 491, 361))
        self.tableWidget.setObjectName("tableView")
        self.listView = QtWidgets.QListWidget(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(570, 40, 181, 361))
        self.listView.setObjectName("listView")
        self.listView.itemSelectionChanged.connect(self.populate_chat)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(610, 410, 99, 27))
        self.pushButton_2.setObjectName("pushButton_2")
        self.setCentralWidget(self.centralwidget)

        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.setObjectName("toolBar")
       
        self.addformat()
        self.retranslateUi()
        self.openFile = QAction(QIcon('ui/open.png'), 'Open and Save', self)
        self.openFile.setShortcut('Ctrl+O')
        self.openFile.setStatusTip('Open File')
        self.openFile.triggered.connect(self.showDialog)

        
        self.menubar = self.menuBar()
        filemenu = self.menubar.addMenu('File')
        filemenu.addAction(self.openFile)
        
        QtCore.QMetaObject.connectSlotsByName(self)
        
        #self.populate_chat(self.chat.db.id)
        self.populate_contacts()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Close file', '/home')[0]
        image = Image.open(fname)
        

        width = 150
        height = 150

        image = image.resize((width, height), Image.ANTIALIAS)

        img_tmp = ImageQt(image.convert('RGBA'))

        pixmap = QPixmap.fromImage(img_tmp)
    
        self.lbl.setPixmap(pixmap)
        file = open(fname, "rb")
        img = file.read()
        file.close()

        self.database.add_image(img)

    def get_avatar_image(self):
        
        output = io.BytesIO()
        image = output.write(self.database.get_image().Data)
        image = Image.open(output)

        width = 150
        height = 150

        image = image.resize((width, height), Image.ANTIALIAS)

        img_tmp = ImageQt(image.convert('RGBA'))

        pixmap = QPixmap.fromImage(img_tmp)
    
        self.lbl.setPixmap(pixmap)

    def addformat(self):

       
    
        bold = QAction(QIcon('ui/b.jpg'),'Bold', self)

        bold.triggered.connect(self.actionBold)

        italic = QAction(QIcon('ui/i.jpg'), 'Italic', self)

        italic.triggered.connect(self.actionItalic)

        underlined = QAction(QIcon('ui/u.jpg'), 'Underlined', self)

        underlined.triggered.connect(self.actionUnderlined)

        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolBar)

        
        
        self.toolBar.addAction(bold)

        self.toolBar.addAction(italic)

        self.toolBar.addAction(underlined)

    def actionBold(self):

        myFont = QFont()

        myFont.setBold(True)

        # myFont.setWeight(700)

        self.textEdit.setFont(myFont)


    def actionItalic(self):

        myFont = QFont()

        myFont.setItalic(True)

        self.textEdit.setFont(myFont)


    def actionUnderlined(self):

        myFont = QFont()

        myFont.setUnderline(True)

        self.textEdit.setFont(myFont)



    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", str(self.login.user)))
        self.pushButton.setText(_translate("MainWindow", "Send Message"))
        self.label.setText(_translate("MainWindow", "Chat"))
        self.label_2.setText(_translate("MainWindow", "Contacts"))
        self.pushButton_2.setText(_translate("MainWindow", "Edit Contats"))

    def populate_chat(self):
        self.tableWidget.clearContents()
        
        self.recieverid = self.contactlist[self.listView.selectedItems()[0].text()]
        self.chat.db.recieverid = self.recieverid
        print(self.contactlist)
        print(self.recieverid)
        messages = self.database.get_all_messages(self.senderid, self.recieverid)
        print(messages)
        self.tableWidget.setRowCount(len(messages))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['User','Message', 'Time'])
        for i, item in enumerate(messages):
            user = QtWidgets.QTableWidgetItem(self.database.get_userbyid(item.senderid).name)
            message = QtWidgets.QTableWidgetItem(str(item.message))
            timestamp = QtWidgets.QTableWidgetItem(str(item.timestamp))
            self.tableWidget.setItem(i, 0, user)
            self.tableWidget.setItem(i, 1, message)
            self.tableWidget.setItem(i, 2, timestamp)
            self.tableWidget.resizeColumnsToContents()

    def populate_contacts(self):
        contacts = self.database.get_all_contacts()
        print(self.chat.db.senderid)
        for i, item in enumerate(contacts):

            if item.id != self.chat.db.senderid:
                self.listView.addItem(item.fullname)
                self.contactlist[item.fullname] = item.id
        
    
    def update_chat(self):
        self.recieverid = self.contactlist[self.listView.selectedItems()[0].text()]
        self.chat.db.recieverid = self.recieverid
        print(self.recieverid)
        print(self.senderid)
        timestamp = time.ctime()
        threading1 = threading.Thread(target=self.chat.read)
        threading1.daemon = True
        threading1.start()
        print('updating')
        print(self.chat.response)
        if self.chat.response:
            response = self.chat.response.pop()
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(self.database.get_userbyid(response['headers']['senderid']).name))
            self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(response['body']))
            self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(timestamp)))
    
    def send_message(self, senderid, recieverid, message):
        timestamp = time.ctime()
        self.database.add_message(senderid, recieverid, message, timestamp)
        # print(database.path)
        # print(database.get_all_messages('2','3'))
        # print("sent", message)
        self.textEdit.clear()
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(self.login.user))
        self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(message)))
        self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(timestamp)))
        self.chat.send(message)
        # thread = threading.Thread(target=self.chat.send, args=(message), daemon = True)
        # thread.start()


if __name__ == "__main__":

    client = ClientWindow()
   

