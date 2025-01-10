# site_form.py
from PyQt5 import QtCore, QtGui, QtWidgets

class site_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        
        # UI Setup Code
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(100, 110, 200, 56))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setWordWrap(True)
        self.verticalLayout.addWidget(self.label)
        
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.verticalLayout.addWidget(self.lineEdit)
        
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Site name:"))
        self.pushButton.setText(_translate("Form", "Search"))
