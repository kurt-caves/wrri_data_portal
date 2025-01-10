import sys
# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi #load ui files
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget


'''
https://www.youtube.com/watch?v=RxGlB9U64fg&list=PLs3IFJPw3G9KhF7BeGOItwoKKLD8e3Dwu&index=7
'''

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui", self)
        self.login.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotocreate)
    
    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocreate(self):
        create = CreateAccountScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex()+1)

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen,self).__init__()
        loadUi("login.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)

    def loginfunction(self):
        user = self.emailfield.text() # extract text
        password = self.passwordfield.text()

        user_pwd = {
            'name' : 'john',
            'password': '12345'
        }

        if len(user) == 0 or len(password) == 0:
            self.error.setText("Please input all fields.")
        else:
            if user == user_pwd["name"] and password == user_pwd["password"]:
                print("good login")
            else:
                self.error.setText("Invalid username or password")

class CreateAccountScreen(QDialog):
    def __init__(self):
        super(CreateAccountScreen, self).__init__()
        loadUi("createacc.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.signupfunction)

    def signupfunction(self):
        fillprofile = FillProfileScreen()
        widget.addWidget(fillprofile)
        widget.setCurrentIndex(widget.currentIndex()+1)

app = QApplication(sys.argv)
welcome = WelcomeScreen()

widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)

widget.show()
try:
    sys.exit(app.exec_())
except:
    print("exiting")