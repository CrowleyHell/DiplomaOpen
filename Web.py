from PyQt5.QtWidgets import QWidget


import cv2
import os
savedEnv = {}
for k, v in os.environ.items():
    if k.startswith("QT_") and "cv2" in v:
        print(k, v)
        savedEnv[k] = v
        del os.environ[k]

class Web(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

    def run(self):
        for k in savedEnv:
            os.environ[k] = savedEnv[k]
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 10)  # Частота кадров
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)  # Ширина кадров в видеопотоке.
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Высота кадров в видеопотоке.
        codec = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('captured.avi', codec, 10.0, (640, 480))
        while True:
            ret, img = cap.read()
            # cv2.imshow("camera", self.img)
            # time.sleep(63000)
            if cv2.waitKey(10) == 27:  # Клавиша Esc
                break
            # cv2.imshow('frame', img)
            out.write(img)
        out.release()
        cap.release()
