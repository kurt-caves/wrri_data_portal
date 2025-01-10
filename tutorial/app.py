from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QLineEdit, QVBoxLayout
from PyQt6.QtCore import QSize, Qt

# QApplication is the application handler
# Only needed for access to command line arguments
import sys
from random import choice

# MainWindow is a subclass of QMainWindow
# by calling super... we insure the parent class QMainWindow is initialized before we add custom logic
# we are basically setting up the parent class which is the base / foundation

window_titles = [
    'My App',
    'My App',
    'Still My App',
    'Still My App',
    'What on earth',
    'What on earth',
    'This is surprising',
    'This is surprising',
    'Something went wrong'
]

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    # these functions can only take two parameters self and a boolean: checked
    # or whatever you want to call it
    
    
    
    
    def the_button_was_clicked(self):
        print("Clicked")
        new_window_title = choice(window_titles)
        print("Setting title: %s" % new_window_title)
        self.setWindowTitle(new_window_title)
        self.n_times_clicked += 1
    
    def the_window_title_changed(self, window_title):
        print("Window title changed: %s" % window_title)

        if window_title == 'Something went wrong':
            self.button.setDisabled(True)
        print(self.n_times_clicked)
    
    def the_button_was_released(self):
        self.button_is_checked = self.button.isChecked()
        print(self.button_is_checked)
    
    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked
        print(self.button_is_checked)


app = QApplication(sys.argv)

window = MainWindow()
window.show()



app.exec()

# # sys.argv allows command line arguments when running the app
# # for no arg's use QApplication([])
# app = QApplication(sys.argv)

# # create Qt widget, which is the window
# # window = QWidget()
# # window = QPushButton("Push Me")
# window = QMainWindow()
# window.show()

# start the event loop
