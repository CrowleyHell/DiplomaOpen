import sys
from PyQt5.QtWidgets import QApplication
from Authorization import Authorization
from Registration import Registration



# app = QApplication(sys.argv)
#
# def restart():
#     wannarestart = True
#     app.quit()

# wannarestart = True

if __name__ == '__main__':
    # while wannarestart:
    #     wannarestart = False
    app = QApplication(sys.argv)
    ex = Authorization()
    ex.connection()
    reg = Registration(ex.conn, ex.cur)
    ex.show()
    sys.exit(app.exec())

