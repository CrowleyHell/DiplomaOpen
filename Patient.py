import os
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QWidget, QFrame
import datetime
from PyQt5.QtWidgets import QPushButton, QLabel, QErrorMessage
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize
import Processing
from Visit import Visit
import threading
import time
import psycopg2
from VisitOpen import VisitOpen
from ShowVideo import ShowVideo
from StateTrateAnxietyInventory import StateTrateAnxietyInventory


class Patient(QWidget):
    def __init__(self, cur, id, conn):
        super(QWidget, self).__init__()
        self.cur = cur
        self.id = id
        self.conn = conn
        self.setWindowTitle('Пациент')
        #print(str(self.id))
        self.fId = 0
        self.event = threading.Event()
        desk = QApplication.desktop()
        self.setFixedSize(1440, 900)
        x = (desk.width() - self.width()) // 2
        y = (desk.height() - self.height()) // 2
        self.setGeometry(x, y, 1440, 900)
        self.cur.execute("select * from patient where patientid = %s", (str(self.id),))
        self.data = self.cur.fetchall()
        #print(str(self.data))
        self.font = QFont()
        self.font.setPixelSize(22)
        self.info = QLabel(self)
        self.info.setText(
            'Имя: ' + str(self.data[0][0]) + ' ' + str(self.data[0][1]) + ' ' + str(self.data[0][2]))
        self.info2 = QLabel(self)
        self.info2.setText('Пол: ' + str(self.data[0][5]) + '  Дата рождения: ' + str(self.data[0][8]) + '  Полис №: ' + str(self.data[0][7]))
        self.info.move(5, 5)
        self.info2.move(5, 30)
        self.info.setFont(self.font)
        self.info2.setFont(self.font)
        self.frame = QFrame(self)
        self.frame.setFont(self.font)
        self.frame.setLineWidth(3)
        self.frame.setMidLineWidth(3)
        self.frame.setFrameShape(QFrame.HLine)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.frame.setGeometry(0, 57, 1440, 3)

        # Add
        self.addBut = QPushButton(self)
        self.addBut.setIcon(QIcon('icons/add.png'))
        self.addBut.setIconSize(QSize(40, 40))
        self.addBut.setGeometry(5, 65, 40, 40)
        self.addBut.setFont(self.font)
        self.addBut.clicked.connect(self.add)
        self.vis = Visit(conn=self.conn, cur=self.cur, id=self.data[0][3])

        self.testBut = QPushButton(self)
        self.testBut.setText('Этап 1')
        self.testBut.setFont(self.font)
        self.testBut.setGeometry(1145, 65, 120, 40)
        self.testBut.clicked.connect(self.testadd)
        self.test = StateTrateAnxietyInventory(conn=self.conn, cur=self.cur, id=self.data[0][3], event=self.event)

        self.vidTest = QPushButton(self)
        self.vidTest.setText('Этап 2')
        self.vidTest.setFont(self.font)
        self.vidTest.setGeometry(1270, 65, 120, 40)
        self.vidTest.clicked.connect(self.video)

        self.vid = ShowVideo(id=self.id)

        # Download all
        self.picbut = QPushButton(self)
        self.picbut.setIcon(QIcon('icons/down.png'))
        self.picbut.setIconSize(QSize(25, 25))
        self.picbut.setFont(self.font)
        self.picbut.setGeometry(1370, 5, 30, 30)
        self.picbut.clicked.connect(self.download)

        # Update
        self.updd = QPushButton(self)
        self.updd.setIcon(QIcon('icons/upd.png'))
        self.updd.setIconSize(QSize(30, 30))
        self.updd.setGeometry(1405, 5, 30, 30)
        self.updd.setFont(self.font)
        self.updd.clicked.connect(self.upd)

        self.resBut = QPushButton(self)
        #self.resBut.setText('Рез')
        self.resBut.setStyleSheet('background: rgb(51, 51, 51);')
        self.resBut.setFont(self.font)
        self.resBut.setGeometry(1395, 65, 40, 40)
        self.resBut.clicked.connect(self.result)

        self.grid = QTableWidget(self)
        self.grid.setGeometry(0, 110, 1440, 790)
        self.grid.setColumnCount(5)
        self.grid.setFont(self.font)
        self.grid.verticalHeader().hide()
        self.grid.setEditTriggers(QTableWidget.NoEditTriggers)
        self.grid.cellClicked.connect(self.openVis)
        for i in range(5):
            self.grid.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        self.upd()

    def openVis(self, row):
        idd = self.grid.item(row, 0).text()
        self.openVis = VisitOpen(conn=self.conn, cur=self.cur, id=str(idd), pid=str(self.data[0][3]))
        self.openVis.show()

    def add(self):
        self.vis.show()

    def testadd(self):
        self.test.show()

    def download(self):
        self.cur.execute("select pathh from files where patientid = %s", (str(self.data[0][3]),))
        addr = self.cur.fetchall()
        for i in addr:
            #print(i[0])
            os.system('eog -n ' + str(i[0]) +'&')

    def upd(self):
        self.grid.clear()
        self.grid.setRowCount(0)
        self.grid.setHorizontalHeaderLabels(['ID',
                                             '           Дата         ',
                                             '                               Жалобы                             ',
                                             '                               Диагноз                            ',
                                             '                     Назначения                     '])
        self.cur.execute("select fileid, ddate, compl, diag, prescr from medfile where patientid = %s order by fileid desc", (self.data[0][3],))
        rows = self.cur.fetchall()
        #print('tyt', str(rows))
        self.fId = rows[0][0]

        #print('3!!!', str(self.fId))
        i = 0
        for elem in rows:
            self.grid.setRowCount(self.grid.rowCount() + 1)
            j = 0
            for t in elem:
                self.grid.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1

    def video(self):
        self.vid.show()

    def result(self):
        Processing.proc(self.id)
        ready = QErrorMessage(self)
        ready.setWindowTitle("Готово")
        ready.showMessage("Файл готов")
        # self.cur.execute("select sitanx, persanx from patient where patientid = %s", (str(self.id),))
        # anx = self.cur.fetchall()
        try:
            self.cur.execute("insert into files (patientid, pathh, fileid) values (%s, %s, %s)",
                             (self.id, f'results/{self.id}.jpg', self.fId))
            self.conn.commit()
            #self.close()
        except Exception as e:
            print(e)
            pass





