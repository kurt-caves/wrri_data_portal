import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel


def main():
    # app instance
    app = QApplication(sys.argv)

    # main window
    window = QMainWindow()
    window.setWindowTitle("Simple App")
    window.setGeometry(100, 100, 400, 200)

    # create label widget
    label = QLabel("Hello World", window)
    label.move(150, 80)

    # show the window
    window.show()

    # execute the app
    sys.exit(app.exec())

if __name__ == '__main__':
    main()