from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sys
import sys
import time
import json

import hashlib


sha1 = hashlib.new('sha1')

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

        self.visiblePasswordCheckBox = QCheckBox('비밀번호표시', self)
        self.visiblePasswordCheckBox.toggled.connect(self.onToggledPassword)

        # 로그인 버튼 생성
        self.loginButton = QPushButton('로그인')
        self.loginButton.clicked.connect(self.login)

        # 회원가입 버튼 생성
        self.signupButton = QPushButton('회원가입')
        self.signupButton.clicked.connect(self.signup)

        # layout 생성
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.signupButton)
        buttonLayout.addWidget(self.loginButton)

        layout = QVBoxLayout()
        layout.addWidget(self.imageLabel)
        layout.addWidget(self.idLineEdit)
        layout.addWidget(self.passwordLineEdit)
        layout.addWidget(self.visiblePasswordCheckBox)

        layout.addLayout(buttonLayout)



        self.setLayout(layout)

        # 해당 위젯의 크기 조절
        self.resize(QApplication.primaryScreen().availableSize()/2)

    def onToggledPassword(self, toggled):
        if toggled:
            self.passwordLineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.passwordLineEdit.setEchoMode(QLineEdit.Password)

    def onClickSigUp(self):
        inputId = self.idLineEdit.text()
        inputPw = self.passwordLineEdit.text()

        print("onClickSigIn inputId: ", inputId)
        print("onClickSigIn inputPw: ", inputPw)
        self.onSignUp(inputId, inputPw)

    def signup(self, id, pw):
        formatPw = str(f'{pw}#jkon')
        formatPw = formatPw.encode('utf-8')
        sha1.update(formatPw)
        pwHash = sha1.hexdigest()
        print('pwHash: ', pwHash)

        formatId = str(f'{pw}#jkon')
        formatId = formatId.encode('utf-8')
        sha1.update(formatId)
        newId = sha1.hexdigest()
        print('newId: ', newId)

        now = time.time()
        
        new_user = {
            'id' : newId,
            'username' : id,
            'pw' : pwHash,
            'created' : now,
            'modified' : now,
        }

        already = False
        for user_1 in users:
            userId = user_1['id']
            userPw = user_1['pw']

            if id == userId and pw == userPw:
                already = True
                break

        if already:
            print('이미 존재하는 사용자')
            return 
        #################################################
        users.append(new_user)
        localDatabase['users'] = users

        # TODO: localDatabase -> json 파일로 생성 후 저장
        with open('./db.json', 'w') as f:
            json.dump(localDatabase, f, indent=2)

# 로그인 
    def login(self):
        print("login")

        inputId = self.idLineEdit.text()
        inputPw = self.passwordLineEdit.text()
        print("login inputId: ", inputId)
        print("login inputPw: ", inputPw) 
        
        self.onSigIn(inputId, inputPw)

# 로그인 확인
    def onSigIn(self, id, pw):
        # 로그인 기본값
        isAuth = False
        for user in users:
            userId = user['id']
            userPw = user['pw']

            formatPw = str(f'{pw}#jkon')
            formatPw = formatPw.encode('utf-8')
            sha1.update(formatPw)
            pwHash = sha1.hexdigest()
            print('pwHash: ', pwHash)

            formatId = str(f'{pw}#jkon')
            formatId = formatId.encode('utf-8')
            sha1.update(formatId)
            newId = sha1.hexdigest()
            print('newId: ', newId)

            if newId == userId and pwHash == userPw:
                # 인증됨
                isAuth = True
                break
        # isAuth 를 기준으로 로그인 상태를 갱신
        print('isAuth: ', isAuth)
        print('id: ', id)
        return isAuth
# 사전준비 작업용 함수
def prepare():
    #  파일 데이터를 읽어와 메모리에 준비
    with open('./db.json') as f:
        localDatabase = json.load(f)

    global users
    users = localDatabase.get('users', [])
    print("users: ", users)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec_()