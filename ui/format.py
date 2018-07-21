#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PyQt5.QtGui import QIcon, QFont


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        self.textEdit = QTextEdit()
        
        self.setCentralWidget(self.textEdit)


        bold = QAction(QIcon('b.jpg'),'Bold', self)

        bold.triggered.connect(self.actionBold)

        italic = QAction(QIcon('i.jpg'), 'Italic', self)

        italic.triggered.connect(self.actionItalic)

        underlined = QAction(QIcon('u.jpg'), 'Underlined', self)

        underlined.triggered.connect(self.actionUnderlined)


        toolbar = self.addToolBar('Formatting')

        toolbar.addAction(bold)

        toolbar.addAction(italic)

        toolbar.addAction(underlined)


        self.setGeometry(300, 300, 350, 250)

        self.setWindowTitle('Main window')

        self.show()


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


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())