from PySide2.QtWidgets import(QApplication, QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy, QPushButton, QFileDialog, QMessageBox)
from PySide2.QtGui import QPixmap, QImage
import sys

class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('Serving Robot')

        # QLabel 생성 및 기타 설정 (이미지 표시를 위한 기본 설정)
        # 기본 빈이미지를 표시
        self.imageLabel = QLabel()
        self.imageLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        fileName = "./res/Serving.jpg"
        image = QImage(fileName)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))

        # 로그인 버튼 생성
        loginButton = QPushButton('로그인')
        loginButton.clicked.connect(self.login)

        # 회원가입 버튼 생성
        signupButton = QPushButton('회원가입')
        signupButton.clicked.connect(self.signup)

        # layout 생성
        layout = QVBoxLayout()
        layout.addWidget(self.imageLabel)
        layout.addWidget(loginButton)
        layout.addWidget(signupButton)

        self.setLayout(layout)

        # 해당 위젯의 크기 조절
        self.resize(QApplication.primaryScreen().availableSize()/2)

    def login(self):
        pass

    def signup(self):
        pass
        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec_()