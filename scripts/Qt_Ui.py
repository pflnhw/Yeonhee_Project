from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
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

        # 아이디 입력창
        self.idLineEdit = QLineEdit(self)
        self.idLineEdit.setPlaceholderText('아이디를 입력')
        # 유효성확인 설정
        idRegExp = QRegExp('[A-Za-z0-9]{4,16}')
        idValidator = QRegExpValidator(idRegExp, self)
        self.idLineEdit.setValidator(idValidator)

        # 비밀번호 입력창
        self.passwordLineEdit = QLineEdit(self)
        self.passwordLineEdit.setPlaceholderText('비밀번호 입력')
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        # 유효성확인 설정
        passwordRegExp = QRegExp('[A-Za-z0-9]{8,20}')
        passwordValidator = QRegExpValidator(passwordRegExp, self)
        self.passwordLineEdit.setValidator(passwordValidator)

        self.visiblePasswordCheckBox = QCheckBox('비밀번호표시', self)
        self.visiblePasswordCheckBox.toggled.connect(self.onToggledPassword)

        # 로그인 버튼 생성
        loginButton = QPushButton('로그인')
        loginButton.clicked.connect(self.login)

        # 회원가입 버튼 생성
        signupButton = QPushButton('회원가입')
        signupButton.clicked.connect(self.signup)

        # layout 생성
        layout = QVBoxLayout()
        layout.addWidget(self.imageLabel)
        layout.addWidget(self.idLineEdit)
        layout.addWidget(self.passwordLineEdit)
        layout.addWidget(self.visiblePasswordCheckBox)
        layout.addWidget(loginButton)
        layout.addWidget(signupButton)

        self.setLayout(layout)

        # 해당 위젯의 크기 조절
        self.resize(QApplication.primaryScreen().availableSize()/2)

    def onToggledPassword(self, toggled):
        if toggled:
            self.passwordLineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.passwordLineEdit.setEchoMode(QLineEdit.Password)

    def login(self):
        pass

    def signup(self):
        pass
        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec_()
