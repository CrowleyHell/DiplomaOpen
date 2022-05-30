from PyQt5.QtWidgets import QErrorMessage, QWidget, QPushButton, QLabel, QLineEdit, QDateEdit, QComboBox, QApplication
from PyQt5.QtGui import QFont
import datetime

class PatientReg(QWidget):
    def __init__(self, cur, doctorid, conn):
        super(QWidget, self).__init__()
        self.cur = cur
        self.conn = conn
        self.doctorid = doctorid
        self.setWindowTitle('Пациент')
        desk = QApplication.desktop()
        self.setFixedSize(1440, 900)
        x = (desk.width() - self.width()) // 2
        y = (desk.height() - self.height()) // 2
        self.setGeometry(x, y, 1440, 900)
        self.font = QFont()
        self.font.setPixelSize(22)

        self.sname = QLineEdit(self)
        self.snameText = QLabel(self)
        self.snameText.setText("Фамилия*")
        self.snameText.setFont(self.font)
        self.sname.setFont(self.font)
        self.snameText.setGeometry(self.width()/2 - 395, self.height()/2 - 145, 150, 30)
        self.sname.setGeometry(self.width()/2 - 200, self.height()/2 - 145, 400, 30)

        self.fname = QLineEdit(self)
        self.fnameText = QLabel(self)
        self.fnameText.setText("Имя*")
        self.fnameText.setFont(self.font)
        self.fname.setFont(self.font)
        self.fnameText.setGeometry(self.width()/2 - 395, self.height()/2 - 105, 150, 30)
        self.fname.setGeometry(self.width()/2 - 200, self.height()/2 - 105, 400, 30)

        self.pname = QLineEdit(self)
        self.pnameText = QLabel(self)
        self.pnameText.setText("Отчество")
        self.pnameText.setFont(self.font)
        self.pname.setFont(self.font)
        self.pnameText.setGeometry(self.width()/2 - 395, self.height()/2 - 65, 150, 30)
        self.pname.setGeometry(self.width()/2 - 200, self.height()/2 - 65, 400, 30)

        self.dob = QDateEdit(self)
        self.dobText = QLabel(self)
        self.dobText.setText("Дата рождения*")
        self.dobText.setFont(self.font)
        self.dob.setFont(self.font)
        self.dobText.setGeometry(self.width()/2 - 395, self.height()/2 - 25, 170, 30)
        self.dob.setGeometry(self.width()/2 - 200, self.height()/2 - 25, 400, 30)

        self.sexBox = QComboBox(self)
        self.sexBox.addItem("Мужской")
        self.sexBox.addItem("Женский")
        self.sexText = QLabel(self)
        self.sexText.setText("Пол*")
        self.sexBox.setGeometry(self.width()/2 - 200, self.height()/2 + 25, 150, 30)
        self.sexText.setFont(self.font)
        self.sexText.setGeometry(self.width()/2 - 395, self.height()/2 + 25, 150, 30)

        self.pnum = QLineEdit(self)
        self.pnumText = QLabel(self)
        self.pnumText.setText("Номер телефона*")
        self.pnumText.setFont(self.font)
        self.pnum.setFont(self.font)
        self.pnumText.setGeometry(self.width()/2 - 395, self.height()/2 + 65, 190, 30)
        self.pnum.setGeometry(self.width()/2 - 200, self.height()/2 + 65, 400, 30)

        self.adr = QLineEdit(self)
        self.adrText = QLabel(self)
        self.adrText.setText("Домашний адрес*")
        self.adrText.setFont(self.font)
        self.adr.setFont(self.font)
        self.adrText.setGeometry(self.width()/2 - 395, self.height()/2 + 105, 190, 30)
        self.adr.setGeometry(self.width()/2 - 200, self.height()/2 + 105, 400, 30)

        self.pol = QLineEdit(self)
        self.polText = QLabel(self)
        self.polText.setText("Полис №*")
        self.polText.setFont(self.font)
        self.pol.setFont(self.font)
        self.polText.setGeometry(self.width()/2 - 395, self.height()/2 + 145, 150, 30)
        self.pol.setGeometry(self.width()/2 - 200, self.height()/2 + 145, 400, 30)

        self.reg = QPushButton(self)
        self.reg.setText('Регистрация')
        self.reg.setFont(self.font)
        self.reg.setGeometry(self.width()/2 - 75, self.height()/2 + 185, 150, 30)
        self.reg.clicked.connect(self.add)

    def nameExists(self, sname, fname, pname, dob):
        self.cur.execute("select sname, fname, pname, dob from patient ")
        pd = self.cur.fetchall()
        j = 0
        for i in range(len(pd)):
            if str(sname) == pd[i][0] and str(fname) == pd[i][1] and str(pname) == pd[i][2] and str(dob) == pd[i][3]:
                j += 1
        if j >= 1:
            return True
        else:
            return False

    def isaplha(self, str, alp=set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
        return not alp.isdisjoint(str)

    def add(self):
        if self.fname.text() != '' and self.sname.text() != '' \
                and self.dob.text() != '' and self.adr.text() != '' \
                and self.sexBox.currentText() != '' and self.pol.text() != '':
            if str(self.isaplha(self.fname.text())) and str(self.isaplha(self.sname.text())) \
                    and str(self.isaplha(self.adr.text())) \
                    and self.pnum.text().isdigit() and self.pol.text().isdigit():
                if len(self.pol.text()) == 16 and len(self.pnum.text()) == 11:
                    if not self.nameExists(self.sname.text(), self.fname.text(), self.pname.text(), self.dob.text()):
                        try:
                            self.cur.execute("insert into patient (fname, sname, pname, dob, sex, doctorid, adr, pol) values (%s, %s, %s, %s, %s, %s, %s, %s) returning patientid",
                                             (str(self.fname.text()), str(self.sname.text()), str(self.pname.text()), str(self.dob.text()), str(self.sexBox.currentText()), self.doctorid,
                                              str(self.adr.text()), str(self.pol.text())))
                            self.patientid = self.cur.fetchone()[0]
                            self.cur.execute("insert into medfile (compl, ddate, patientid) values (%s, %s, %s) returning fileid", ('Первичный прием', str(datetime.date.today().strftime('%d.%m.%Y')), str(self.patientid)))
                            self.fileid = self.cur.fetchall()[0]
                            self.fname.setText('')
                            self.sname.setText('')
                            self.pname.setText('')
                            self.adr.setText('')
                            self.pol.setText('')
                            self.conn.commit()
                            self.close()
                        except Exception as e:
                            print(e)
                            pass
                    else:
                        errMes = QErrorMessage(self)
                        errMes.setWindowTitle("Ошибка")
                        errMes.showMessage("Пациент уже зарегистрирован")
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
        else:
            errMes = QErrorMessage(self)
            errMes.setWindowTitle("Ошибка")
            errMes.showMessage("Данные введены неверно")
            return
