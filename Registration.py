import hashlib
import uuid
from PyQt5.QtWidgets import QErrorMessage, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication


def password(pw):
    hash = uuid.uuid4().hex
    return hashlib.sha256(hash.encode() + pw.encode()).hexdigest() + '-' + hash


def checkpw(hashpw, pw):
    password, hash = hashpw.split('-')
    return password == hashlib.sha256(hash.encode() + pw.encode()).hexdigest()


class Registration(QWidget):
    def __init__(self, conn, cur):
        super(QWidget, self).__init__()
        self.conn = conn
        self.cur = cur
        desk = QApplication.desktop()
        self.setFixedSize(1440, 900)
        x = (desk.width() - self.width()) // 2
        y = (desk.height() - self.height()) // 2
        self.setGeometry(x, y, 1440, 900)
        self.setWindowTitle('Регистрация')
        self.font = QFont()
        self.font.setPixelSize(20)

        self.sname = QLineEdit(self)
        self.snameText = QLabel(self)
        self.snameText.setText("Фамилия*")
        self.sname.setFont(self.font)
        self.snameText.setFont(self.font)
        self.snameText.setGeometry(self.width()/2 - 370, self.height()/2 - 120, 150, 30)
        self.sname.setGeometry(self.width()/2 - 200, self.height()/2 - 120, 400, 30)

        self.fname = QLineEdit(self)
        self.fnameText = QLabel(self)
        self.fnameText.setText("Имя*")
        self.fname.setFont(self.font)
        self.fnameText.setFont(self.font)
        self.fnameText.setGeometry(self.width()/2 - 370, self.height()/2 - 80, 150, 30)
        self.fname.setGeometry(self.width()/2 - 200, self.height()/2 - 80, 400, 30)

        self.pname = QLineEdit(self)
        self.pnameText = QLabel(self)
        self.pnameText.setText("Отчество")
        self.pname.setFont(self.font)
        self.pnameText.setFont(self.font)
        self.pnameText.setGeometry(self.width()/2 - 370, self.height()/2 - 40, 150, 30)
        self.pname.setGeometry(self.width()/2 - 200, self.height()/2 - 40, 400, 30)

        self.log = QLineEdit(self)
        self.logText = QLabel(self)
        self.logText.setText("Логин*")
        self.log.setFont(self.font)
        self.logText.setFont(self.font)
        self.logText.setGeometry(self.width()/2 - 370, self.height()/2, 150, 30)
        self.log.setGeometry(self.width()/2 - 200, self.height()/2, 400, 30)

        self.pas = QLineEdit(self)
        self.pasText = QLabel(self)
        self.pasText.setText("Пароль*")
        self.pas.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.pas.setFont(self.font)
        self.pasText.setFont(self.font)
        self.pasText.setGeometry(self.width()/2 - 370, self.height()/2 + 40, 150, 30)
        self.pas.setGeometry(self.width()/2 - 200, self.height()/2 + 40, 400, 30)

        self.dob = QDateEdit(self)
        self.dobText = QLabel(self)
        self.dobText.setText("Дата рождения*")
        self.dobText.setFont(self.font)
        self.dob.setFont(self.font)
        self.dobText.setGeometry(self.width()/2 - 370, self.height()/2 + 80, 170, 30)
        self.dob.setGeometry(self.width()/2 - 200, self.height()/2 + 80, 400, 30)

        self.dep = QLineEdit(self)
        self.depText = QLabel(self)
        self.depText.setText("Отделение*")
        self.dep.setFont(self.font)
        self.depText.setFont(self.font)
        self.depText.setGeometry(self.width()/2 - 370, self.height()/2 + 120, 150, 30)
        self.dep.setGeometry(self.width()/2 - 200, self.height()/2 + 120, 400, 30)

        self.reg = QPushButton(self)
        self.reg.setText('Регистрация')
        self.reg.setFont(self.font)
        self.reg.setGeometry(self.width()/2 - 75, self.height()/2 + 160, 150, 30)
        self.reg.clicked.connect(self.add)

    def nameExists(self, sname, fname, pname, dob):
        self.cur.execute("select sname, fname, pname, dob from pd ")
        pd = self.cur.fetchall()
        j = 0
        for i in range(len(pd)):
            if sname == pd[i][0] and fname == pd[i][1] and pname == pd[i][2] and dob == pd[i][3]:
                j += 1
        if j >= 1:
            return True
        else:
            return False



    def logExists(self, login):
        self.cur.execute("select log from login")
        log = self.cur.fetchall()
        for i in range(len(log)):
            if login == log[i][0]:
                return True
            else:
                return False

    def isaplha(self, str, alp=set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
        return not alp.isdisjoint(str)

    def add(self):
        if self.fname.text() != '' and self.sname.text() != '' \
                and self.dob.text() != '' and self.pas.text() != '' \
                and self.log.text() != '' and self.dep.text() != '':
            if str(self.isaplha(self.fname.text())) and str(self.isaplha(self.sname.text())) \
                    and str(self.pas.text()).isalnum() and str(self.log.text()).isalnum() \
                    and self.dep.text().isdigit():
                if len(self.log.text()) >= 6 and len(self.pas.text()) >= 6:
                    if not self.nameExists(self.sname.text(), self.fname.text(), self.pname.text(), self.dob.text()):
                        if not self.logExists(self.log.text()):
                            ppas = password(self.pas.text())
                            try:
                                self.cur.execute(
                                    "insert into pd (fname, sname, pname, dob, department) values (%s, %s, %s, %s, %s) returning doctorid",
                                    (str(self.fname.text()), str(self.sname.text()), str(self.pname.text()), str(self.dob.text()),
                                    self.dep.text()))
                                self.doctorid = self.cur.fetchone()[0]
                                self.fname.setText('')
                                self.sname.setText('')
                                self.pname.setText('')
                                self.dob.setText('')
                                self.dep.setText('')
                                self.cur.execute("insert into login(log, pw, ownerid) values (%s, %s, %s)",
                                                 (str(self.log.text()), str(ppas), self.doctorid))
                                self.conn.commit()
                                self.close()
                            except Exception as e:
                                print(e)
                                pass
                        else:
                            errMes = QErrorMessage(self)
                            errMes.setWindowTitle("Ошибка")
                            errMes.showMessage("Данный логин занят")
                            return
                    else:
                        errMes = QErrorMessage(self)
                        errMes.setWindowTitle("Ошибка")
                        errMes.showMessage("Пользователь уже существует")
                        return
                else:
                    errMes = QErrorMessage(self)
                    errMes.setWindowTitle("Ошибка")
                    errMes.showMessage("Логин и пароль должны содержать как минимум 6 символов")
                    return
            else:
                errMes = QErrorMessage(self)
                errMes.setWindowTitle("Ошибка")
                errMes.showMessage("Данные введены неверно")
                return
        else:
            errMes = QErrorMessage(self)
            errMes.setWindowTitle("Ошибка")
            errMes.showMessage("Данные введены неверно")
            return