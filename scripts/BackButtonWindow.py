#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sys
import time

class BackButtonWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
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
        pass
    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    backButtonWindow = BackButtonWindow()
    backButtonWindow.show()

    app.exec_()
