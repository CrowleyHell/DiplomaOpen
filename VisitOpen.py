from PyQt5.QtWidgets import QTextEdit, QWidget, QPushButton, QLabel, QApplication
from PyQt5.QtGui import QFont
import os


class VisitOpen(QWidget):
    def __init__(self, conn, cur, id, pid):
        super(QWidget, self).__init__()
        self.conn = conn
        self.cur = cur
        self.id = id
        self.pid = pid
        self.setWindowTitle('Посещение')
        desk = QApplication.desktop()
        self.setFixedSize(1440, 900)
        x = (desk.width() - self.width()) // 2
        y = (desk.height() - self.height()) // 2
        self.setGeometry(x, y, 1440, 900)
        self.cur.execute("select * from medfile where fileid = %s", (str(self.id),))
        self.data = self.cur.fetchall()
        self.font = QFont()
        self.font.setPixelSize(22)
        self.ddate = QLabel(self)
        #print(self.data)

        self.ddate.setText('Дата: ' + str(self.data[0][5]))
        self.ddate.setGeometry(10, 10, 400, 30)
        self.ddate.setFont(self.font)

        self.com = QTextEdit(self)
        self.com1 = QLabel(self)
        self.com1.setFont(self.font)
        self.com1.setText('Жалобы: ')
        self.com1.setGeometry(self.width()/2 - 450, 60, 150, 30)
        self.com.setFont(self.font)
        self.com.setText(self.data[0][4])
        self.com.setGeometry(self.width()/2 - 300, 60, 600, 150)
        self.com.setReadOnly(True)

        self.diag = QTextEdit(self)
        self.diag.setFont(self.font)
        self.diag.setGeometry(self.width()/2 - 300, 380, 600, 150)
        self.diag.setText(self.data[0][1])
        self.diag.setReadOnly(True)
        self.diag1 = QLabel(self)
        self.diag1.setFont(self.font)
        self.diag1.setText('Диагноз: ')
        self.diag1.setGeometry(self.width()/2 - 450, 380, 100, 30)

        self.pr = QTextEdit(self)
        self.pr.setGeometry(self.width()/2 - 300, 540, 600, 150)
        self.pr.setText(self.data[0][3])
        self.pr.setFont(self.font)
        self.pr.setReadOnly(True)
        self.pr1 = QLabel(self)
        self.pr1.setFont(self.font)
        self.pr1.setText('Назначения: ')
        self.pr1.setGeometry(self.width()/2 - 450, 540, 150, 30)

        self.ch = QTextEdit(self)
        self.ch.setGeometry(self.width()/2 - 300, 220, 600, 150)
        self.ch.setText(self.data[0][2])
        self.ch.setFont(self.font)
        self.ch.setReadOnly(True)
        self.ch1 = QLabel(self)
        self.ch1.setFont(self.font)
        self.ch1.setText('Хронические \nзаболевания: ')
        self.ch1.setGeometry(self.width()/2 - 450, 220, 150, 60)

        self.picbut = QPushButton(self)
        self.picbut.setText('Скачать файл')
        self.picbut.setFont(self.font)
        self.picbut.setGeometry(self.width()/2 - 100, 700, 200, 50)
        self.picbut.clicked.connect(self.download)

    def download(self):
        self.cur.execute("select pathh from files where fileid = %s", (str(self.id),))
        addr = self.cur.fetchall()
        for i in addr:
            #print(i[0])
            os.system('eog -n ' + str(i[0]) + '&')

