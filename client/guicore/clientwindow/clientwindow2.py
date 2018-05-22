# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clientwindow2.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

import sys
sys.path.append('/home/ssavrass/Documents/GeekBrainsPython/Course6HW/jim/database')
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from database import SqliteDB, Message
from PyQt5.QtCore import pyqtSlot

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(70, 420, 491, 111))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(450, 540, 111, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.send_message(self.textEdit.toPlainText()))
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 20, 67, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(620, 20, 67, 17))
        self.label_2.setObjectName("label_2")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(70, 40, 491, 361))
        self.tableWidget.setObjectName("tableView")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(570, 40, 181, 361))
        self.listView.setObjectName("listView")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(610, 410, 99, 27))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.populate()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Send Message"))
        self.label.setText(_translate("MainWindow", "Chat"))
        self.label_2.setText(_translate("MainWindow", "Contacts"))
        self.pushButton_2.setText(_translate("MainWindow", "Edit Contats"))

    def populate(self):
        self.tableWidget.clearContents()
        database = SqliteDB()
        messages = database.get_all_messages('2','3')
        self.tableWidget.setRowCount(len(messages))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['Message', 'Time'])
        for i, item in enumerate(messages):
            message = QtWidgets.QTableWidgetItem(str(item.message))
            timestamp = QtWidgets.QTableWidgetItem(str(item.timestamp))
            self.tableWidget.setItem(i, 0, message)
            self.tableWidget.setItem(i, 1, timestamp)
        self.tableWidget.resizeColumnsToContents()
        
    
    # def update_chat(self):
        
    #     self.populate()
    
    def send_message(self, message):
        timestamp = time.ctime()
        database = SqliteDB()
        database.add_message("2", "3", message, timestamp)
        print(database.path)
        print(database.get_all_messages('2','3'))
        print("sent", message)
        self.textEdit.clear()
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(message)))
        self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(timestamp)))

            # def update_contacts(self):
        #

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

