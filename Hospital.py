import os
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize
from PatientRegistration import PatientReg
from Patient import Patient


class Hospital(QWidget):
    def __init__(self, id, cur, conn):
        super(QWidget, self).__init__()
        self.id = id
        self.cur = cur
        self.conn = conn
        self.setStyleSheet('`/DB/f2.JPG')
        self.setWindowTitle('Персонал')
        desk = QApplication.desktop()
        self.setFixedSize(1440, 900)
        x = (desk.width() - self.width()) // 2
        y = (desk.height() - self.height()) // 2
        self.setGeometry(x, y, 1440, 900)
        self.cur.execute("select fname, sname, pname, dob, department from pd where doctorid = %s", (str(self.id),))
        q = self.cur.fetchone()
        fname = q[0]
        sname = q[1]
        pname = q[2]
        dob = q[3]
        department = q[4]
        self.font = QFont()
        self.font.setPixelSize(22)
        self.info = QLabel(self)
        self.info.setText('Имя: ' + sname + ' ' + fname + ' ' + pname)
        self.info2 = QLabel(self)
        self.info2.setText('Дата рождения: ' + dob)
        self.info3 = QLabel(self)
        self.info3.setText('Отделение №: ' + department)
        self.info.move(5, 5)
        self.info2.move(5, 35)
        self.info3.move(5, 65)
        self.info.setFont(self.font)
        self.info2.setFont(self.font)
        self.info3.setFont(self.font)

        self.addBut = QPushButton(self)
        self.addBut.setText('Новый пациент')
        self.addBut.setGeometry(1265, 40, 170, 50)
        self.addBut.setFont(self.font)
        self.addBut.clicked.connect(self.add)
        self.regPatient = PatientReg(cur=self.cur, doctorid=self.id, conn=conn)

        self.updd = QPushButton(self)
        self.updd.setIcon(QIcon('icons/upd.png'))
        self.updd.setIconSize(QSize(30, 30))
        self.updd.setGeometry(1360, 5, 30, 30)
        self.updd.clicked.connect(self.upd)
        self.updd.setFont(self.font)

        self.ext = QPushButton(self)
        self.ext.setIcon(QIcon('icons/ext.png'))
        self.ext.setIconSize(QSize(30, 30))
        self.ext.setGeometry(1395, 5, 30, 30)
        self.ext.setFont(self.font)
        self.ext.clicked.connect(self.exit)

        self.grid = QTableWidget(self)
        self.grid.setGeometry(0, 96, 1920, 804)
        self.grid.setColumnCount(6)
        self.grid.setFont(self.font)
        self.grid.verticalHeader().hide()
        for i in range(6):
            self.grid.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        self.upd()
        self.grid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.grid.cellClicked.connect(self.openPat)

    def upd(self):
        self.grid.clear()
        self.grid.setRowCount(0)
        self.grid.setHorizontalHeaderLabels(['ID',
                                             '                              Фамилия                               ',
                                             '                               Имя                                ',
                                             '                             Отчество                             ',
                                             '                              Пол                               ',
                                             '                          Дата рождения                        '])
        self.cur.execute("select patientid, sname, fname, pname, sex, dob from patient where doctorid = %s order by sname", (str(self.id),))
        rows = self.cur.fetchall()
        i = 0
        for elem in rows:
            self.grid.setRowCount(self.grid.rowCount() + 1)
            j = 0
            for t in elem:
                self.grid.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1

    def add(self):
        self.regPatient.show()

    def openPat(self, row):
        idd = self.grid.item(row, 0).text()
        self.patient = Patient(cur=self.cur, id=str(idd), conn=self.conn)
        self.patient.show()

    def exit(self):
        self.close()
        os.system('python3 main.py')


