import sys
import os
import csv
import json
# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi #load ui files
from mysql.connector import Error
from PyQt5.QtCore import QDate
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QComboBox, QVBoxLayout, QCalendarWidget, QFileDialog, QLineEdit
import siteQuerys
import hashlib

''' Tutorial I followed
https://www.youtube.com/watch?v=RxGlB9U64fg&list=PLs3IFJPw3G9KhF7BeGOItwoKKLD8e3Dwu&index=7
'''
# -----------------------------------------------------------------------------------------------
# Get absolute path to resource, works for dev and PyInstaller
# when using pyinstaller on the command line we need the full path to the ui files
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# the main screen when starting the program
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        ui_file = resource_path("welcomescreen.ui")  # dynamically locate the .ui file
        loadUi(ui_file, self)
        # when Check Sites button is clicked trigger gotositelookup method
        self.checksite.clicked.connect(self.gotositelookup)
        # when Download data button is clicked go to gotodownload method
        self.downloaddata.clicked.connect(self.gotodownload)
        # # when login button is clicked go to loginmethod
        self.logout.clicked.connect(self.gotologin)

    # widgets are the screens the user sees
    # this is the site look up screen
    def gotositelookup(self):
        # check site button was clicked SiteLookupScreen class will handle it
        sitelookupbox = SiteLookupScreen()
        widget.addWidget(sitelookupbox)

        # the widget for the site look up screen becomes visible to user
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    # this is the download data screen
    def gotodownload(self):
        # download data button was clicked the class DownloadScreen will handle it
        download = DownloadScreen()
        widget.addWidget(download)

        # the widget for down load data screen becomes visible to user
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)

        # the widget for down load data screen becomes visible to user
        widget.setCurrentIndex(widget.currentIndex()+1)
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# this is the class that handles the Download screen
class DownloadScreen(QDialog):
    def __init__(self):
        super(DownloadScreen, self).__init__()
        ui_file = resource_path("downloadscreen.ui")  # dynamically locate the .ui file
        loadUi(ui_file, self)
        # if home button is clicked 
        self.home.clicked.connect(self.gobacktowelcomescreen)

        # setting up variables that will be used in most methods in this class
        # to run the methods for the download page we need start and end dates
        # and the site
        self.start_date = None
        self.end_date = None
        self.site = None

        # for selecting dates
        self.calendarWidget.clicked.connect(self.date_selected)
        
        # site name drop down populated by a db query when the page loads
        siteList = siteQuerys.loadsites()
        # we get back tuples, the site name will be the first element in each tuple
        first_elements = [tup[0] for tup in siteList]
        # add a blank line to the drop down box
        self.comboBox.addItem("")
        # add our list of sites to the drop down
        self.comboBox.addItems(first_elements)
        # when a site is chosen from the drop down set the site
        self.comboBox.currentTextChanged.connect(self.setsite)

        # self.comboBox_2.addItem("")
        # this is the dropdown box for choosing the file type
        # daily, 15 min, etc... we set the file type
        self.comboBox_2.currentTextChanged.connect(self.setfile)

        # when downloaddata button is clicked the download data method is used
        # this is the button to download the main data file from the db
        self.downloaddata.clicked.connect(self.download_data)

        # when update button is clicked the table search method is used
        self.update.clicked.connect(self.tablesearch)

        # when downloadsite button is clicked the table search method is used
        # this is the button to download the site metadata
        self.downloadsite.clicked.connect(self.sitedatadownload)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# this method handles the download of site metadata from the Site table
    def sitedatadownload(self):
        # we return a dictionary of the description meta data from 
        # the Site table but its actually a tuple
        dict_to_print = siteQuerys.siteDesUnitsQuery(self.file, self.site)
        # need to add the latitude and longitude to the csv
        lat_long = siteQuerys.latAndLong(self.site)
        # grab the first element from the tuple
        # and turn it into a json object
        new_dict = dict_to_print[0]
        json_dict = json.loads(new_dict)
        
        # ask the user to give the file a name
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(None, "Save CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)

        # if they gave it a name and a file path
        if file_path:
            if not file_path.endswith('.csv'):
                file_path += '.csv'

            # now with the file path we can make the csv
            with open(file_path, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                for key, value in json_dict["metadata"].items():
                    if isinstance(value, list):  # handle lists in metadata
                        writer.writerow([key, ", ".join(value)])
                    else:
                        writer.writerow([key, value])

                writer.writerow(lat_long)
                writer.writerow([])  # add a blank line

                # write columns
                writer.writerow(["Column Name", "Statistic Type", "Unit"])
                for column in json_dict["columns"]:
                    writer.writerow([column["name"], column["stat"], column["unit"]])

            print(f"CSV saved to: {file_path}")
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# this method is used when the update button is clicked
# this method will populate the comboBox_2 with the file types found
# from the Data table query 
    def tablesearch(self):
        # clear the error text
        self.error.setText("")
        
        # we need to put the date in the proper date time format
        start_date_str = self.start_date.toString('yyyy-MM-dd')
        end_date_str = self.end_date.toString('yyyy-MM-dd')
        site = self.site

        # get back a list of file types from the Data table
        fileList = siteQuerys.filetype(site, start_date_str, end_date_str)
        # if we have an empty list error
        if fileList == [] or fileList == None:
            self.error.setText("No records, try another date")
        else:
            # create a list of files
            files = [tup[0] for tup in fileList]
            # add the file list to the dropdown
            self.comboBox_2.addItems(files)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# add the file to self
    def setfile(self, s):
        self.file = s
# ----------------------------------------------------------------
    
# ----------------------------------------------------------------
    def download_data(self):
        start_date_str = self.start_date.toString('yyyy-MM-dd')
        end_date_str = self.end_date.toString('yyyy-MM-dd')
        site = self.site
        # go fetch the data and get back a dictionary that we will print
        dict_toprint = siteQuerys.datadownload(site, start_date_str, end_date_str, self.file)

        # this is the save file option
        options = QFileDialog.Options()
        # ask the user to give the file a name
        file_path, _ = QFileDialog.getSaveFileName(None, "Save CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        # if they gave it a name and a file path
        if file_path:
            if not file_path.endswith('.csv'):
                file_path += '.csv'

            # now with the file path we can make the csv
            with open(file_path, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # write the headr column names
                writer.writerow(dict_toprint.keys())

                # write the rows
                for row in zip(*dict_toprint.values()):
                    writer.writerow(row)

            print(f"CSV saved to: {file_path}")
# ----------------------------------------------------------------
    
# ----------------------------------------------------------------
    def setsite(self, s):
        self.site = s
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# when home button is pressed go back to home screen  
    def gobacktowelcomescreen(self):
        gohome = WelcomeScreen()
        widget.addWidget(gohome)
        widget.setCurrentIndex(widget.currentIndex()+1)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
    def date_selected(self, selected_date):
        #clear the file dropdown box
        self.comboBox_2.clear()
        # retrieve the selected date from the QCalendarWidget
        selected_date = self.calendarWidget.selectedDate()

        if self.start_date is None:
            self.start_date = selected_date
            self.startdate.setText(f"Start Date: {self.start_date.toString()}")
        elif self.end_date is None:
            self.end_date = selected_date
            if self.end_date < self.start_date:
                self.start_date, self.end_date = self.end_date, self.start_date 
            self.startdate.setText(f"Start Date: {self.start_date.toString()}")
            self.enddate.setText(f"End Date: {self.end_date.toString()}")
        else:
            # reset and start a new range selection
            self.start_date = selected_date
            self.end_date = None
            self.startdate.setText(f"Start Date: {self.start_date.toString()}")
            self.enddate.clear()
# ----------------------------------------------------------------


# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
class SiteLookupScreen(QDialog):
    def __init__(self):
        super(SiteLookupScreen, self).__init__()
        ui_file = resource_path("sitelookup.ui")  # dynamically locate the .ui file
        loadUi(ui_file, self)
        self.checksite.clicked.connect(self.checksites)
        self.home.clicked.connect(self.gobacktowelcomescreen)
        
        # grab the name of Sites
        siteList = siteQuerys.loadsites()
        # we get tuples back so we make a list and grab the first elements from each tuple
        first_elements = [tup[0] for tup in siteList]
        
        # this is the drop down box
        self.comboBox.addItems(first_elements)
        self.comboBox.activated.connect(self.activated)
        self.comboBox.currentTextChanged.connect(self.text_changed)
        self.comboBox.currentIndexChanged.connect(self.index_changed)
    
    # go back to home screen
    def gobacktowelcomescreen(self):
        gohome = WelcomeScreen()
        widget.addWidget(gohome)
        widget.setCurrentIndex(widget.currentIndex()+1)
    # this method checks for sites that are entered
    def checksites(self):
        sitetoQuery = self.siteedit.text()
        # print(sitetoQuery)

        # check for sites by name
        queriedSite = siteQuerys.sitequery(sitetoQuery)
        # print(queriedSite)
        if queriedSite == []:
            self.error.setText("Site does not exist")
            
        else:
            self.error.setText("Site Exists")



    def activated(self, index):
        pass
        # print("Activated index:", index)

    def text_changed(self, s):
        pass
        # print("Text changed:", s)

    def index_changed(self, index):
        pass
        # print("Index changed", index)
# -----------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        ui_file = resource_path("loginscreen.ui")  # dynamically locate the .ui file
        loadUi(ui_file, self)

        # if home button is clicked 
        # self.home.clicked.connect(self.gobacktowelcomescreen)

        # we want to obscure the password
        self.password.setEchoMode(QLineEdit.Password)
        # when login button is clicked we need to grab the username and password
        self.loginButton.clicked.connect(self.getunameandpassword)
    
    def getunameandpassword(self):
        userName = self.userName.text()
        password = self.password.text()
    
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        result = siteQuerys.login(userName, hashed_password)
        print("result: ", result)
        if result:
            print("login succesful")
            self.gobacktowelcomescreen()
        else:
            self.error.setText("Wrong username or password")

        # ----------------------------------------------------------------
# when home button is pressed go back to home screen  
    def gobacktowelcomescreen(self):
        gohome = WelcomeScreen()
        widget.addWidget(gohome)
        widget.setCurrentIndex(widget.currentIndex()+1)
# ----------------------------------------------------------------
# -----------------------------------------------------------------------------------------------

    
app = QApplication(sys.argv)
welcome = LoginScreen()
# this section sets up the screen
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()

# this launches the whole program
try:
    sys.exit(app.exec_())
except:
    print("Exiting")