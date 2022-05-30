import hashlib
import uuid
import psycopg2
from PyQt5.QtWidgets import  QErrorMessage, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QSize
from Registration import Registration
from Hospital import Hospital
from PyQt5.QtWidgets import QApplication


def password(pw):
    hash = uuid.uuid4().hex
    return hashlib.sha256(hash.encode() + pw.encode()).hexdigest() + '-' + hash


def checkpw(hashpw, pw):
    password, hash = hashpw.split('-')
    return password == hashlib.sha256(hash.encode() + pw.encode()).hexdigest()


class Authorization(QWidget):
    def __init__(self):
        super(Authorization, self).__init__()
        desk = QApplication.desktop()
        self.setFixedSize(1440, 900)
        x = (desk.width() - self.width()) // 2
        y = (desk.height() - self.height()) // 2
        self.setGeometry(x, y, 1440, 900)
        self.setWindowTitle('Авторизация')
        self.font = QFont()
        self.font.setPixelSize(22)

        self.emb = QLabel(self)
        self.emb.setPixmap(QPixmap('icons/emb.png').scaled(QSize(400, 400)))
        self.emb.setGeometry(self.width()/2 - 200, 20, 400, 400)

        self.log = QLineEdit(self)
        self.lText = QLabel(self)
        self.lText.setText('Логин')
        self.lText.setFont(self.font)
        self.log.setFont(self.font)
        self.lText.setGeometry(self.width()/2 - 300, self.height()/2 - 20, 100, 30)
        self.log.setGeometry(self.width()/2 - 200, self.height()/2 - 20, 400, 30)

        self.pw = QLineEdit(self)
        self.pw.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.pText = QLabel(self)
        self.pText.setText('Пароль')
        self.pText.setFont(self.font)
        self.pw.setFont(self.font)
        self.pText.setGeometry(self.width()/2 - 300, self.height()/2 + 20, 100, 30)
        self.pw.setGeometry(self.width()/2 - 200, self.height()/2 + 20, 400, 30)

        self.enterBut = QPushButton(self)
        self.enterBut.setText('Вход')
        self.enterBut.setFont(self.font)
        self.enterBut.setGeometry(self.width()/2 - 200, self.height()/2 + 60, 150, 30)
        self.regBut = QPushButton(self)
        self.regBut.setGeometry(self.width()/2 + 50, self.height()/2 + 60, 150, 30)
        self.regBut.setText('Регистрация')
        self.regBut.setFont(self.font)
        self.enterBut.clicked.connect(self.enterance)
        self.regBut.clicked.connect(self.registration)

        self.show()
        self.conn, self.cur = self.connection()
        self.registrationWindow = Registration(conn=self.conn, cur=self.cur)

    def connection(self):
        self.conn = psycopg2.connect(user="postgres",
                                     password="devint56",
                                     host="127.0.0.1",
                                     port="5432",
                                     database="postgres")
        self.cur = self.conn.cursor()
        return self.conn, self.cur

    def enterance(self):
        if self.log.text() == "" or self.pw.text() == "":
            errMes = QErrorMessage(self)
            errMes.setWindowTitle("Ошибка")
            errMes.showMessage("Введите данные")
            return
        self.cur.execute("select pw, ownerid from login where log = %s", (str(self.log.text()),))
        q = self.cur.fetchone()
        if q is None:
            errMes = QErrorMessage(self)
            errMes.setWindowTitle("Ошибка")
            errMes.showMessage("Неверные логин или пароль")
            return
        pww = q[0]
        ownerid = q[1]
        if checkpw(pww, self.pw.text()):
            self.hos = Hospital(id=ownerid, cur=self.cur, conn=self.conn)
            self.hos.show()
            self.hide()
        else:
            errMes = QErrorMessage(self)
            errMes.setWindowTitle("Ошибка")
            errMes.showMessage("Неверные логин или пароль")
            return

    def registration(self):
        self.registrationWindow.show()