# main.py
import sys
from PyQt5 import QtWidgets
from main_page_copy import Ui_MainWindow
from site_widget import site_Form
import siteQuery

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect the main window's button to show_site_form
        self.pushButton.clicked.connect(self.show_site_form)

        # Set up the site form
        self.site_form_widget = QtWidgets.QWidget()
        self.site_form = site_Form()
        self.site_form.setupUi(self.site_form_widget)
        
        # Connect the button in site_form to get_text
        self.site_form.pushButton.clicked.connect(self.get_text)

        self.site_form_widget.show()

    def show_site_form(self):
        self.site_form_widget.show()

    def get_text(self):
        text_msg = self.site_form.lineEdit.text()
        print(text_msg)
        record = siteQuery.sitequery(text_msg)
        print(record, type(record))
        if record[0] == 0:
            print("No record found")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
