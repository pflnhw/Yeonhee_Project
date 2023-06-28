from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from ButtonWindow import ButtonWindow
import sys
import time
import json

localDatabase = {}
users = []
    
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

        # 비밀번호 표시
        self.visiblePasswordCheckBox = QCheckBox('비밀번호 표시', self)
        self.visiblePasswordCheckBox.toggled.connect(self.onToggledPassword)

        # 로그인 버튼 생성
        loginButton = QPushButton('로그인')
        loginButton.clicked.connect(self.onClickSigIn)

        # 회원가입 버튼 생성
        signupButton = QPushButton('회원가입')
        signupButton.clicked.connect(self.onClickSigUp)

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

    # 비밀번호 표시
    def onToggledPassword(self, toggled):
        if toggled:
            self.passwordLineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.passwordLineEdit.setEchoMode(QLineEdit.Password)

    # 아이디, 비밀번호 저장
    def onClickSigUp(self):
        inputId = self.idLineEdit.text()
        inputPW = self.passwordLineEdit.text()
        print('onClickSignUp inputId:', inputId)
        print('onClickSignUp inputPW:', inputPW)

        # 등록진행
        self.onSignUp(inputId, inputPW)

    # 회원가입
    def onSignUp(self, id, pw):
        now = time.time()

        for user_1 in users:
            userId = user_1['id']
            if id == userId or len(id)<3:
                print('이미 존재하는 사용자거나 너무 짧습니다.')
                return

        new_user = {
            'id': id,
            'pw': pw,
            'created': now,
            'modified': now,
        }

        users.append(new_user)
        localDatabase['users'] = users

        # localDatabase를 json 파일로 생성 후 저장
        with open('./db.json', 'w') as f:
            json.dump(localDatabase, f, indent=2)
    
    # 아이디, 비밀번호 저장
    def onClickSigIn(self):
        print("onClickSigIn")

        inputId = self.idLineEdit.text()
        inputPw = self.passwordLineEdit.text()
        print("onClickSigIn inputId: ", inputId)
        print("onClickSigIn inputPw: ", inputPw)

        self.onSigIn(inputId, inputPw)

    # 로그인
    def onSigIn(self, id, pw):
        isAuth = False
        for user in users:
            userId = user['id']
            userPw = user['pw']

            if id == userId and pw == userPw:
                # 인증됨
                isAuth = True

                self.close()
                self.second = ButtonWindow()

                break

        # isAuth를 기준으로 로그인 상태를 갱신
        print('isAuth: ', isAuth)
        print('id: ', id)

        return isAuth

def prepare():
    # 파일 데이터를 읽어와 메모리에 준비
    with open('./db.json') as f:
        localDatabase = json.load(f)

    global users
    users = localDatabase.get('users', [])
    # print("users: ", users)

if __name__ == "__main__":
    prepare()
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec_()
