from PyQt5.QtWidgets import QPushButton, QFileDialog, QWidget, QTextEdit, QLabel, QDateEdit, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDir


class Visit(QWidget):
    def __init__(self, conn, cur, id):
        super(QWidget, self).__init__()
        self.conn = conn
        self.cur = cur
        self.id = id
        desk = QApplication.desktop()
        self.setFixedSize(1440, 900)
        x = (desk.width() - self.width()) // 2
        y = (desk.height() - self.height()) // 2
        self.setGeometry(x, y, 1440, 900)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.font = QFont()
        self.font.setPixelSize(22)
        self.setWindowTitle('Прием')

        self.date = QDateEdit(self)
        self.dateText = QLabel(self)
        self.dateText.setText("Дата приема")
        self.date.setFont(self.font)
        self.dateText.setFont(self.font)
        self.dateText.setGeometry(self.width()/2 - 450, 20, 150, 30)
        self.date.setGeometry(self.width()/2 - 300, 20, 400, 30)

        self.com = QTextEdit(self)
        self.comText = QLabel(self)
        self.comText.setText("Жалобы:*")
        self.com.setFont(self.font)
        self.comText.setFont(self.font)
        self.comText.setGeometry(self.width()/2 - 450, 60, 150, 30)
        self.com.setGeometry(self.width()/2 - 300, 60, 600, 150)

        self.ch = QTextEdit(self)
        self.chText = QLabel(self)
        self.chText.setText("Хронические \nзаболевания:")
        self.ch.setFont(self.font)
        self.chText.setFont(self.font)
        self.chText.setGeometry(self.width()/2 - 450, 220, 150, 60)
        self.ch.setGeometry(self.width()/2 - 300, 220, 600, 150)

        self.diag = QTextEdit(self)
        self.diagText = QLabel(self)
        self.diagText.setText("Диагноз")
        self.diag.setFont(self.font)
        self.diagText.setFont(self.font)
        self.diagText.setGeometry(self.width()/2 - 450, 380, 100, 30)
        self.diag.setGeometry(self.width()/2 - 300, 380, 600, 150)

        self.pr = QTextEdit(self)
        self.prText = QLabel(self)
        self.prText.setText("Назначения:*")
        self.pr.setFont(self.font)
        self.prText.setFont(self.font)
        self.prText.setGeometry(self.width()/2 - 450, 540, 150, 30)
        self.pr.setGeometry(self.width()/2 - 300, 540, 600, 150)

        self.addBut = QPushButton(self)
        self.addBut.setText('Добавить')
        self.addBut.setFont(self.font)
        self.addBut.setGeometry(self.width()/2 - 300, 700, 170, 30)
        self.addBut.clicked.connect(self.add)

        self.picBut = QPushButton(self)
        self.picBut.setText('Загрузить файл')
        self.picBut.setFont(self.font)
        self.picBut.setGeometry(self.width()/2 + 130, 700, 170, 30)
        self.picBut.clicked.connect(self.upload)
        self.filenames = ''

    def upload(self):
        file = QFileDialog(self)
        file.setGeometry(850, 120, 150, 30)
        file.setFileMode(QFileDialog.ExistingFiles)
        file.setNameFilter("*.jpg")
        file.setDirectory(QDir.homePath())
        if file.exec_():
            self.filenames = file.selectedFiles()
        # for i in self.filenames:
        #     print(str(i))

    def add(self):
        if self.date.text() != '' and self.com.toPlainText() != '' and self.pr.toPlainText() != '':
            try:
                self.cur.execute("insert into medfile (diag, chronic, prescr, compl, ddate, patientid) "
                                 "values (%s, %s, %s, %s, %s, %s) returning fileid",
                                 (str(self.diag.toPlainText()), str(self.ch.toPlainText()), str(self.pr.toPlainText()),
                                  str(self.com.toPlainText()),
                                  str(self.date.text()), self.id))
                self.fileid = self.cur.fetchone()[0]
                self.diag.setText('')
                self.ch.setText('')
                self.pr.setText('')
                self.com.setText('')
                for i in self.filenames:
                    self.cur.execute("insert into files (patientid, pathh, fileid) values (%s, %s, %s)",
                                     (self.id, str(i), str(self.fileid)))
                self.conn.commit()
                self.close()
            except Exception as e:
                print(e)
                pass
        self.close()