from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import QSize
import threading
import time
import os
import cv2
savedEnv = {}
for k, v in os.environ.items():
    if k.startswith("QT_") and "cv2" in v:
        #print(k, v)
        savedEnv[k] = v
        del os.environ[k]


class ShowVideo(QWidget):
    def __init__(self, id):
        super(ShowVideo, self).__init__()
        self.id = id
        #self.event = threading.Event()
        self.setGeometry(0, 0, 1920, 1080)
        self.font = QFont()
        self.font.setPixelSize(20)
        self.label = QLabel(self)
        self.img = 'img.jpg'
        self.pxmp = QPixmap(self.img)
        self.label.setPixmap(self.pxmp)

        self.but = QPushButton(self)
        self.but.setIcon(QIcon('icons/ext.png'))
        self.but.setIconSize(QSize(100, 100))
        self.but.setFont(self.font)
        self.but.setGeometry(910, 490, 100, 100)
        self.but.setStyleSheet('background: rgb(159,163,163);')
        self.but.clicked.connect(self.add)
        #self.is_recording = False

    def web(self):
        for k in savedEnv:
            os.environ[k] = savedEnv[k]
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 17)  # Частота кадров
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)  # Ширина кадров в видеопотоке.
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Высота кадров в видеопотоке.
        codec = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(f'video/{self.id}.avi', codec, 17.0, (640, 480))
        t = time.time()
        while True:
            ret, img = cap.read()
            if not time.time() - t < 5:
                break
            out.write(img)
        out.release()
        cap.release()
        cv2.destroyAllWindows()


    def add(self):
        self.start_recording()

    def start_recording(self):
        def thread_function(vid):
            vid.web()

        t = threading.Thread(target=thread_function, args=(self,))
        t.start()
