#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sys
from LineDetect import Start

class BackButtonWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # self.x = x
        self.setWindowTitle('BackButton Window')
        self.show()

        self.backmoveButton = QPushButton('음식을 받고 화면을 눌러주세요.')
        self.backmoveButton.clicked.connect(self.onClickBackMove)
        self.backmoveButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        font = self.backmoveButton.font()
        font.setPointSize(100)
        self.backmoveButton.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(self.backmoveButton)

        self.setLayout(layout)
        self.resize(QApplication.primaryScreen().availableSize())

    def onClickBackMove(self):
        self.close()
        # if self.x == 1:
        #     self.BackMove1()
        # elif self.x == 2:
        #     self.BackMove2()
        # elif self.x == 3:
        self.BackMove4()
        # elif self.x == 4:
        #     self.BackMove4()

    # def BackMove1(self):
    #     # print(self.x)
    #     Qr_res = "http://m.site.naver.com/1aDPf"
    #     Start(Qr_res)


    # def BackMove2(self):
    #     # print(self.x)
    #     Qr_res = "http://m.site.naver.com/1aDPD"
    #     Start(Qr_res)

    # def BackMove3(self):
    #     # print(self.x)
    #     Qr_res = "http://m.site.naver.com/1aDPR"
    #     Start(Qr_res)

    def BackMove4(self):
        # print(self.x)
        Qr_res = "http://m.site.naver.com/1aDPY"
        Start(Qr_res)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    backButtonWindow = BackButtonWindow()
    backButtonWindow.show()

    app.exec_()
