from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    # xpos, ypos, width, height
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("Hello World")

    label = QtWidgets.QLabel(win)
    label.setText("my first label")
    label.move(50, 50)

    b1 = QtWidgets.QPushButton(win)
    b1.setText("Click me")

    # show the window
    win.show()

    sys.exit(app.exec_())

window()