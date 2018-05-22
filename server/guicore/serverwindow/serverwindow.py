# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serverwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer

import time
import sys

class Server(object):

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.setupUi(MainWindow)
        self.tickertimer = QTimer()
        self.tickertimer.timeout.connect(lambda: self.update_server())
        self.delay = 1000 #ms (1s = 1000ms)    
        MainWindow.show()
        sys.exit(self.app.exec_())


    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(610, 30, 161, 481))
        self.listWidget.setObjectName("listWidget")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(350, 30, 221, 481))
        self.listWidget_2.setObjectName("listWidget_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(390, 10, 131, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(660, 10, 67, 17))
        self.label_2.setObjectName("label_2")
        self.listWidget_3 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_3.setGeometry(QtCore.QRect(20, 30, 301, 481))
        self.listWidget_3.setObjectName("listWidget_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(130, 10, 101, 17))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 520, 99, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.start_server())
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(450, 520, 99, 27))
        self.pushButton2.setObjectName("pushButton")
        self.pushButton2.clicked.connect(lambda: self.stop_server())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Client Statistics"))
        self.label_2.setText(_translate("MainWindow", "Clients"))
        self.label_3.setText(_translate("MainWindow", "Server Status"))
        self.pushButton.setText(_translate("MainWindow", "Start Server"))
        self.pushButton2.setText(_translate("MainWindow", "Stop Server"))

    def start_server(self):    
        self.tickertimer.start(self.delay)

    def stop_server(self):
        self.tickertimer.stop()


    def update_server(self):
        
        self.print_status()
        self.clients()
        self.client_statistics()
       
            


    def print_status(self):
        self.listWidget.addItem("yes")
        print("hello")
    def clients(self):
        self.listWidget_2.addItem("yes")
    
    def client_statistics(self):
        self.listWidget_3.addItem("yes")
        


if __name__ == "__main__":
    
    
    server = Server()
    

