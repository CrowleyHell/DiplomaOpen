from PyQt5.QtWidgets import QComboBox, QTableWidgetItem, QHeaderView, QWidget, QDialog
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
import threading
import datetime



class StateTrateAnxietyInventory(QDialog):
    def __init__(self, cur, id, conn, event):
        super(QDialog, self).__init__()
        #self.conn, self.cur = self.connection()
        self.conn = conn
        self.cur = cur
        self.id = id
        self.event = event
        #self.event = threading.Event()
        self.count = 0
        self.answers1 = []
        self.answers2 = []
        self.setWindowTitle('STAI. First Block')
        desk = QApplication.desktop()
        self.setFixedSize(720, 450)
        x = (desk.width() - self.width()) // 2
        y = (desk.height() - self.height()) // 2
        self.setGeometry(x, y, 720, 450)
        self.font = QFont()
        self.font.setPixelSize(22)

        self.answerBox = QComboBox(self)
        self.answerBox.addItem("Нет, это не так")
        self.answerBox.addItem("Пожалуй, так")
        self.answerBox.addItem("Верно")
        self.answerBox.addItem("Совершенно верно")
        self.answerBox.setGeometry(60, self.height()/2 - 30, 300, 60)
        self.answerBox.setFont(self.font)
        self.questions = self.questions()

        self.qText = QLabel(self)
        self.qText.setFont(self.font)
        self.qText.setWordWrap(True)
        self.qText.setText(self.questions[self.count])
        self.count += 1
        self.qText.setGeometry(self.width()/2 - 300, self.height()/2 - 90, 500, 70)
        self.confBut = QPushButton(self)
        self.confBut.setText('Подтвердить')
        self.confBut.setFont(self.font)
        self.confBut.setGeometry(self.width()/2 - 300, self.height()/2 + 40, 150, 40)
        self.confBut.clicked.connect(self.next_question)
        self.is_finished = False



    def questions(self):
        questions = []
        file = open('STAI', 'r')
        for line in file:
            questions.append(str(line))
        # print(len(questions))
        questions.append('Я готов завершить тест')

        return questions

    def next_question(self):
        if self.count <= 40:
            self.qText.setText(self.questions[self.count])
            # print(self.count)
            if self.answerBox.currentText() == "Нет, это не так":
                if self.count <= 20:
                    self.answers1.append(1)
                else:
                    self.answers2.append(1)
            elif self.answerBox.currentText() == "Пожалуй, так":
                if self.count <= 20:
                    self.answers1.append(2)
                else:
                    self.answers2.append(2)
            elif self.answerBox.currentText() == "Верно":
                if self.count <= 20:
                    self.answers1.append(3)
                else:
                    self.answers2.append(3)
            elif self.answerBox.currentText() == "Совершенно верно":
                if self.count <= 20:
                    self.answers1.append(4)
                else:
                    self.answers2.append(4)
            self.count += 1
        # elif self.count == 39:
        #     print(self.questions[self.count])
        else:
            #res1, res2 = self.count_result()
            #self.add(res1, res2)
            self.count_result()
            #self.close()
            #self.event.set()


    def count_result(self):
        # print(self.answers1)
        # print(self.answers2)
        a1 = self.answers1[2] + self.answers1[3] + self.answers1[5] + self.answers1[6] + self.answers1[8] + self.answers1[11] + self.answers1[12] + \
            + self.answers1[13] + self.answers1[16] + self.answers1[17]
        b1 = self.answers1[0] + self.answers1[1] + self.answers1[4] + self.answers1[7] + self.answers1[9] + self.answers1[10] + self.answers1[14] + self.answers1[15] + \
            + self.answers1[18] + self.answers1[19]
        # print(a1, b1)
        res1 = a1 - b1
        # print('res1', res1)
        a2 = self.answers2[1] + self.answers2[2] + self.answers2[3] + self.answers2[4] + self.answers2[7] + self.answers2[8] + self.answers2[10] + self.answers2[11] + \
            + self.answers2[13] + self.answers2[14] + self.answers2[16] + self.answers2[17] + self.answers2[19]
        b2 = self.answers2[0] + self.answers2[5] + self.answers2[6] + self.answers2[9] + self.answers2[12] + self.answers2[15] + self.answers2[18]
        res2 = a2 - b2 + 35
        #print('1!!!', res1, res2)
        try:
            # print(res1, res2, self.id)
            # self.cur.execute("update patient set sitanx = %s, persanx = %s where patientid = %s",
            #                  (str(res1), str(res2), self.id))
            strr = 'Уровень общей тревожности: ' + str(res2) + '\nУровень ситуационной тревожности: ' + str(
                res1)
            self.cur.execute("insert into medfile (compl, ddate, patientid) "
                             "values (%s, %s, %s) returning fileid",
                             (str(strr), str(datetime.date.today().strftime('%d.%m.%Y')), self.id))
            self.fileid = self.cur.fetchone()[0]
            #print('2!!', str(self.fileid))
            self.conn.commit()
            self.close()
            #self.event.set()
        except Exception as e:
            print(e)
            pass
        # print('res2', res2)
        #return res1, res2
        # self.cur.execute("insert into patient (sitanx, persanx) values (%s, %s) returning patientid",
        #                  (str(res1), str(res2)))

    # def add(self, res1, res2):
        # try:
        #     # print(res1, res2, self.id)
        #     self.cur.execute("update patient set sitanx = %s, persanx = %s where patientid = %s",
        #                      (str(res1), str(res2), self.id))
        #     self.conn.commit()
        #     self.close()
        #     #self.event.set()
        # except Exception as e:
        #     print('here', e)
        #     pass



