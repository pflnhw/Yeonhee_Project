from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import json

localDatabase = {}
users = []

class ButtonWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('Button Window')

        # 서빙로봇 MOVE 1~4 버튼 생성
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

        # 서빙로봇 MOVE 5~8 버튼 생성
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

        # 서빙로봇 MOVE 9~12 버튼 생성
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

        # 서빙로봇 MOVE 13~16 버튼 생성
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

        # 서빙로봇 MOVE 17~20 버튼 생성
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

        # 레이아웃
        layout = QVBoxLayout()
        layout.addWidget(groupBox1)
        layout.addWidget(groupBox2)
        layout.addWidget(groupBox3)
        layout.addWidget(groupBox4)
        layout.addWidget(groupBox5)

        self.setLayout(layout)
        self.resize(500, 500)


    def move(self):
        pass
    
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
            if id == userId:
                print('이미 존재하는 사용자')
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
