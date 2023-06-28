from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from BackButtonWindow import BackButtonWindow
import sys
import time

class ButtonWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # QWidget.__init__(self, parent)
        self.setWindowTitle('Button Window')
        self.show()
        # 서빙로봇 MOVE 버튼 생성
        self.moveButton1 = QPushButton('1번')
        self.moveButton1.clicked.connect(self.move)
        self.moveButton2 = QPushButton('2번')
        self.moveButton2.clicked.connect(self.move)
        self.moveButton3 = QPushButton('3번')
        self.moveButton3.clicked.connect(self.move)
        self.moveButton4 = QPushButton('4번')
        self.moveButton4.clicked.connect(self.move)
        groupBox1 = QGroupBox('group1', self)
        self.buttonLayout1 = QHBoxLayout(groupBox1)
        self.buttonLayout1.addWidget(self.moveButton1)
        self.buttonLayout1.addWidget(self.moveButton2)
        self.buttonLayout1.addWidget(self.moveButton3)
        self.buttonLayout1.addWidget(self.moveButton4)

        self.moveButton5 = QPushButton('5번')
        self.moveButton5.clicked.connect(self.move)
        self.moveButton6 = QPushButton('6번')
        self.moveButton6.clicked.connect(self.move)
        self.moveButton7 = QPushButton('7번')
        self.moveButton7.clicked.connect(self.move)
        self.moveButton8 = QPushButton('8번')
        self.moveButton8.clicked.connect(self.move)
        groupBox2 = QGroupBox('group2', self)
        self.buttonLayout2 = QHBoxLayout(groupBox2)
        self.buttonLayout2.addWidget(self.moveButton5)
        self.buttonLayout2.addWidget(self.moveButton6)
        self.buttonLayout2.addWidget(self.moveButton7)
        self.buttonLayout2.addWidget(self.moveButton8)

        self.moveButton9 = QPushButton('9번')
        self.moveButton9.clicked.connect(self.move)
        self.moveButton10 = QPushButton('10번')
        self.moveButton10.clicked.connect(self.move)
        self.moveButton11 = QPushButton('11번')
        self.moveButton11.clicked.connect(self.move)
        self.moveButton12 = QPushButton('12번')
        self.moveButton12.clicked.connect(self.move)
        groupBox3 = QGroupBox('group3', self)
        self.buttonLayout3 = QHBoxLayout(groupBox3)
        self.buttonLayout3.addWidget(self.moveButton9)
        self.buttonLayout3.addWidget(self.moveButton10)
        self.buttonLayout3.addWidget(self.moveButton11)
        self.buttonLayout3.addWidget(self.moveButton12)

        self.moveButton13 = QPushButton('13번')
        self.moveButton13.clicked.connect(self.move)
        self.moveButton14 = QPushButton('14번')
        self.moveButton14.clicked.connect(self.move)
        self.moveButton15 = QPushButton('15번')
        self.moveButton15.clicked.connect(self.move)
        self.moveButton16 = QPushButton('16번')
        self.moveButton16.clicked.connect(self.move)
        groupBox4 = QGroupBox('group4', self)
        self.buttonLayout4 = QHBoxLayout(groupBox4)
        self.buttonLayout4.addWidget(self.moveButton13)
        self.buttonLayout4.addWidget(self.moveButton14)
        self.buttonLayout4.addWidget(self.moveButton15)
        self.buttonLayout4.addWidget(self.moveButton16)

        self.moveButton17 = QPushButton('17번')
        self.moveButton17.clicked.connect(self.move)
        self.moveButton18 = QPushButton('18번')
        self.moveButton18.clicked.connect(self.move)
        self.moveButton19 = QPushButton('19번')
        self.moveButton19.clicked.connect(self.move)
        self.moveButton20 = QPushButton('20번')
        self.moveButton20.clicked.connect(self.move)
        groupBox5 = QGroupBox('group5', self)
        self.buttonLayout5 = QHBoxLayout(groupBox5)
        self.buttonLayout5.addWidget(self.moveButton17)
        self.buttonLayout5.addWidget(self.moveButton18)
        self.buttonLayout5.addWidget(self.moveButton19)
        self.buttonLayout5.addWidget(self.moveButton20)

        # 종료 버튼
        self.closeButton = QPushButton('종료')
        self.closeButton.clicked.connect(self.onClickClose)

        layout = QVBoxLayout()
        layout.addWidget(groupBox1)
        layout.addWidget(groupBox2)
        layout.addWidget(groupBox3)
        layout.addWidget(groupBox4)
        layout.addWidget(groupBox5)
        layout.addWidget(self.closeButton)

        self.setLayout(layout)
        self.resize(500, 500)

    def onClickClose(self):
        self.close()

    def move(self):
        self.second = BackButtonWindow()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    buttonWindow = ButtonWindow()
    buttonWindow.show()

    app.exec_()
