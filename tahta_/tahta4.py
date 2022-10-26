from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import json
import sys,time,os

import hashlib

sys.path.insert(1, '.') #also look for 1 folder back #TODO: Comment this when releasing the app
from database_handler import DatabaseHandler

db = DatabaseHandler("db_credentials.json")

RUN_PATH = "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"


def check_connection():
    connection = db.get("checkconnection", ["check == True"] )

    if connection == [{'check': 'True'}]:
        return True
    else:
        return False

class Workaround(QObject):
    logged = pyqtSignal()
    autologged = pyqtSignal()

class Worker(QRunnable):
    '''
    Worker thread
    '''
    running = True
    def __init__(self,app):
        super().__init__()
        self.app = app
        self.timer = 0 #timer in seconds

    def get_windowmanager(self):
        self.windowmanager = self.app.windowmanager

    @pyqtSlot()
    def run(self):
        '''
        The code goes in this function
        '''
        print("Thread start")
        while self.running:
            st = time.time()
            print(".")
            time.sleep(1)
            self.timer += time.time() - st

            if self.app.inapp: #TODO: Add authentication and school login
                pass
            if int(self.timer) % 60 == 0:
                self.windowmanager.ConnectionSetText()

            # self.get_announcement() #maybe not put this in here? 

            if self.timer > 60*10:
                print("10 Minute check")
                self.timer = 0

    def get_announcement(self):
        pass

    def check_db_connection(self):
        pass

    def loginButtonPress(self):
        _translate = QCoreApplication.translate
        print("LOGIN")

        if len(self.windowmanager.lineEdit.text()) < 1 or len(self.windowmanager.lineEdit_2.text()) < 1: 
            print("ERROR LENGTH OF CLASSNAME OR PASSWORD TOO SHORT")
            self.windowmanager.loginerror("Şifre veya Sınıf ismi çok kısa") 
        else:
            self.app.classname:str = self.windowmanager.lineEdit.text()
            self.app.password:str = self.windowmanager.lineEdit_2.text()
            hashed_password = hashlib.sha256(self.app.password.encode()).hexdigest()
            
            print(f"password:{self.app.password} hashed password: {hashed_password}")
            
            result = db.get("accounts", [f"password == {hashed_password}"] )
            if type(result) == bool:
                pass
            
            else:
                if len(result) < 1:
                    self.windowmanager.loginerror("Yanlış Şifre")
                    print("WRONG PASSWORD")
                elif len(result) > 1:
                    print("MORE THAN 1 ACCOUNT WITH THE SAME PASSWORD")
                    self.windowmanager.loginerror("Giriş yapmada belli bir hatayla karşılaşıldı") 
                else:
                    print("CLASSNAME:",self.app.classname, "SCHOOL:","TESTOKULU")
                    self.app.workaround.logged.emit()

    def StartUpLogin(self,inp1:str,inp2:str): #NOTE: I have to create another func for this since I cant give arguments with a slot
        _translate = QCoreApplication.translate
        print("LOGIN")

        if len(inp1) < 1 or len(inp2) < 1: 
            print("ERROR LENGTH OF CLASSNAME OR PASSWORD TOO SHORT")
            self.windowmanager.loginerror("Şifre veya Sınıf ismi çok kısa") 
        else:
            self.app.classname = inp1
            self.app.password = inp2
            hashed_password = hashlib.sha256(self.app.password.encode()).hexdigest()
            
            print(f"password:{self.app.password} hashed password: {hashed_password}")
            
            result = db.get("accounts", [f"password == {hashed_password}"] )
            if type(result) == bool:
                pass
            
            else:
                if len(result) < 1:
                    self.windowmanager.loginerror("Yanlış Şifre")
                    print("WRONG PASSWORD")
                elif len(result) > 1:
                    print("MORE THAN 1 ACCOUNT WITH THE SAME PASSWORD")
                    self.windowmanager.loginerror("Giriş yapmada belli bir hatayla karşılaşıldı") 
                else:
                    print("CLASSNAME:",self.app.classname, "SCHOOL:","TESTOKULU")
                    self.app.workaround.autologged.emit()

class MainWindow(QMainWindow):
    def __init__(self, app, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.app = app
        #self.setObjectName("MainWindow")
        self.setFixedSize(776, 448)

        self.settings = QSettings(RUN_PATH, QSettings.NativeFormat) 
        # self.settings.contains("MainWidget")  # checks if it will start on startup
        self.settings.setValue("MainWidget",sys.argv[0]); #set the app for startup

        self.SetupUI()

    def SetupUI(self):
        self.centralwidget = QWidget(self) #TTTT
        self.centralwidget.setStyleSheet(
            "* {\n"
            "    font-family: 'Roboto', sans-serif;\n"
            "}\n"
            "\n"
            "#frame {\n"
            "    background-color: #e7f5ff;\n"
            "    font-size: 16px;\n"
            "}\n"
            "\n"
            "#apptitle {\n"
            "    font-size: 44px;\n"
            "}\n"
            "\n"
            "#indicator {\n"
            "    background-color: #333;\n"
            "}\n"
            "\n"
            "#description {\n"
            "    color: #555;\n"
            "    font-size: 20px\n"
            "}\n"
            "#Errorlabel {\n"
            "    color: #e01f1f;\n"
            "    font-size: 20px\n"
            "}\n"
            "\n"
            "QLineEdit {\n"
            "    background-color: #333333;\n"
            "    border-radius: 6px;\n"
            "    color: #AAA;\n"
            "    font-size: 16px;\n"
            "    font-weight: 400;\n"
            "    font-family: 'Roboto', sans-serif;\n"
            "    padding-left: 5px;\n"
            "}\n"
            "\n"
            "QLineEdit:hover {\n"
            "    background-color: #444;\n"
            "}\n"
            "\n"
            "QLineEdit:focus {\n"
            "    border: 2px solid #4dabf7;\n"
            "}\n"
            "\n"
            "QPushButton {\n"
            "    background-color: #1c7ed6;\n"
            "    color: #EDF2FF;\n"
            "    border: none;\n"
            "    border-radius: 9px;\n"
            "    font-size: 16px;\n"
            "}\n"
            "\n"
            "QPushButton:hover, QPushButton:focus {\n"
            "    background-color: #228be6;\n"
            "}\n"
            "\n"
            "#alttext {\n"
            "    color: #777;\n"
            "    font-size: 14px;\n"
            "    font-weight: 400;\n"
            "}"
        )
        self.centralwidget.setObjectName("centralwidget")

        self.login_container = QFrame(self.centralwidget)
        self.login_container.setGeometry(QRect(0, 0, 776, 448))
        self.login_container.setFrameShape(QFrame.StyledPanel)
        self.login_container.setFrameShadow(QFrame.Raised)
        self.login_container.setObjectName("frame")

        self.inapp_container = QFrame()
        self.inapp_container.setGeometry(QRect(0, 0, 776, 448))
        self.inapp_container.setFrameShape(QFrame.StyledPanel)
        self.inapp_container.setFrameShadow(QFrame.Raised)
        self.inapp_container.setObjectName("frame2")
        self.inapp_container.setStyleSheet(
            "* {\n"
            "    font-family: 'Roboto', sans-serif;\n"
            "}\n"
            "\n"
            "#frame2 {\n"
            "    background-color: #e7f5ff;\n"
            "    font-size: 16px;\n"
            "}\n"
            "\n"
            "#apptitle {\n"
            "    font-size: 44px;\n"
            "}\n"
            "#classlabel {\n"
            "    font-size: 26px;\n"
            "}\n"
            "#schoollabel {\n"
            "    font-size: 26px;\n"
            "}\n"
            "#announcelabel {\n"
            "    font-size: 26px;\n"
            "}\n"
            "#dbcontrollabel {\n"
            "    font-size: 26px;\n"
            "}\n"
            "\n" 
            "#indicator {\n"
            "    background-color: #333;\n"
            "}\n"
            "\n"
            "#description {\n"
            "    color: #555;\n"
            "    font-size: 20px\n"
            "}\n"
            "\n"
            "QLineEdit {\n"
            "    background-color: #333333;\n"
            "    border-radius: 6px;\n"
            "    color: #AAA;\n"
            "    font-size: 16px;\n"
            "    font-weight: 400;\n"
            "    font-family: 'Roboto', sans-serif;\n"
            "    padding-left: 5px;\n"
            "}\n"
            "\n"
            "QLineEdit:hover {\n"
            "    background-color: #444;\n"
            "}\n"
            "\n"
            "QLineEdit:focus {\n"
            "    border: 2px solid #4dabf7;\n"
            "}\n"
            "\n"
            "QPushButton {\n"
            "    background-color: #1c7ed6;\n"
            "    color: #EDF2FF;\n"
            "    border: none;\n"
            "    border-radius: 9px;\n"
            "    font-size: 16px;\n"
            "}\n"
            "\n"
            "QPushButton:hover, QPushButton:focus {\n"
            "    background-color: #228be6;\n"
            "}\n"
            "\n"
            "#alttext2 {\n"
            "    color: #777;\n"
            "    font-size: 14px;\n"
            "    font-weight: 400;\n"
            "}"
        )
        #self.infowidget = InfoWidget(self)
        #self.infowidget.setParent(self.inapp_container)

        self.apptitle = QLabel(self.login_container)
        self.apptitle.setGeometry(QRect(0, 0, 776, 60))
        self.apptitle.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.apptitle.setObjectName("apptitle")

        self.apptitle2 = QLabel(self.inapp_container)
        self.apptitle2.setGeometry(QRect(0, 0, 776, 60))
        self.apptitle2.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.apptitle2.setObjectName("apptitle")
        
        self.classlabel = QLabel(self.inapp_container)
        self.classlabel.setGeometry(QRect(150, 93, 500, 50))
        self.classlabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignTop)
        self.classlabel.setObjectName("classlabel")
        
        self.schoollabel = QLabel(self.inapp_container)
        self.schoollabel.setGeometry(QRect(150, 150, 500, 50))
        self.schoollabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignTop)
        self.schoollabel.setObjectName("schoollabel")

        self.announcelabel = QLabel(self.inapp_container)
        self.announcelabel.setGeometry(QRect(150, 200, 500, 50))
        self.announcelabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignTop)
        self.announcelabel.setObjectName("announcelabel")
        
        self.dbcontrollabel = QLabel(self.inapp_container)
        self.dbcontrollabel.setGeometry(QRect(150, 250, 500, 50))
        self.dbcontrollabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignTop)
        self.dbcontrollabel.setObjectName("dbcontrollabel")
        

        self.indicator2 = QFrame(self.inapp_container)
        self.indicator2.setGeometry(QRect(88, 60, 600, 2))
        self.indicator2.setFrameShape(QFrame.HLine)
        self.indicator2.setFrameShadow(QFrame.Sunken)
        self.indicator2.setObjectName("indicator")


        self.indicator = QFrame(self.login_container)
        self.indicator.setGeometry(QRect(88, 60, 600, 2))
        self.indicator.setFrameShape(QFrame.HLine)
        self.indicator.setFrameShadow(QFrame.Sunken)
        self.indicator.setObjectName("indicator")
        self.description = QLabel(self.login_container)
        self.description.setGeometry(QRect(88, 75, 600, 51))
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setWordWrap(True)
        self.description.setObjectName("description")
        self.lineEdit = QLineEdit(self.login_container)
        self.lineEdit.setGeometry(QRect(285, 175, 200, 40))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setMaxLength(20)
        self.lineEdit_2 = QLineEdit(self.login_container)
        self.lineEdit_2.setGeometry(QRect(285, 230, 200, 40))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setMaxLength(20)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.pushButton = QPushButton(self.login_container)
        self.pushButton.setGeometry(QRect(310, 290, 150, 40))
        self.pushButton.setObjectName("pushButton")
        self.alttext = QLabel(self.login_container)
        self.alttext.setGeometry(QRect(0, 400, 776, 41))
        self.alttext.setAlignment(Qt.AlignCenter)
        self.alttext.setObjectName("alttext")

        self.errorlabel = QLabel(self.login_container)
        self.errorlabel.setGeometry(QRect(0, 290, 550, 40))
        self.errorlabel.setObjectName("Errorlabel")
        self.errorlabel.setText("TEST")
        self.errorlabel.hide()

        self.alttext2 = QLabel(self.inapp_container)
        self.alttext2.setGeometry(QRect(0, 400, 776, 41))
        self.alttext2.setAlignment(Qt.AlignCenter)
        self.alttext2.setObjectName("alttext2")

        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()

    def ConnectionSetText(self):
        if check_connection():
            self.dbcontrollabel.setText('Veritabanı Durumu: <font color="#56cc41">Bağlantı Stabil</font>')
        else:
            self.dbcontrollabel.setText('Veritabanı Durumu: <font color="#c92a2a">Bağlantı Bulunamadı</font>')

    def connect_login(self):
        """To connect the signal and slot"""
        self.pushButton.clicked.connect(self.app.worker.loginButtonPress)

    def loginerror(self,text:str):
        self.errorlabel.setText(text)

        result = self.errorlabel.fontMetrics().boundingRect(self.errorlabel.text()).width() 
        
        self.errorlabel.setGeometry(QRect( 388-int(result/2) , 280, 550, 40)) #FIXME: i dont have a better idea to do this
        self.pushButton.setGeometry(QRect(310, 320, 150, 40))
        self.errorlabel.show()
        # This is not the best way to center a text but its good enough atm

    def loginsuccesful(self):
        _translate = QCoreApplication.translate

        self.classlabel.setText(_translate("MainWindow", f"SINIF: {self.app.classname}"))
        self.schoollabel.setText(_translate("MainWindow", f"OKUL: {self.app.schoolname}"))
        self.announcelabel.setText(_translate("MainWindow", f"DUYURU: {self.app.lastannouncement}"))

        self.ConnectionSetText()
        
        self.app.inapp = True
        self.setCentralWidget(self.inapp_container)
        print("login successful")

    def autologinsuccessful(self):
        _translate = QCoreApplication.translate
        self.classlabel.setText(_translate("MainWindow", f"SINIF: {self.app.classname}"))
        self.schoollabel.setText(_translate("MainWindow", f"OKUL: {self.app.schoolname}"))
        self.announcelabel.setText(_translate("MainWindow", f"DUYURU: {self.app.lastannouncement}"))

        self.ConnectionSetText()
        
        self.app.inapp = True
        self.setCentralWidget(self.inapp_container)
        print("Succesfull startup login")

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.apptitle.setText(_translate("MainWindow", "Tübitak Projesi"))
        self.apptitle2.setText(_translate("MainWindow", "Tübitak Projesi"))
        self.description.setText(
            _translate(
                "MainWindow",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc vulputate libero et velit interdum, ac aliquet odio mattis.",
            )
        )
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Sınıf Adı"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Şifre"))
        self.pushButton.setText(_translate("MainWindow", "Sınıfı Kaydet"))
        self.alttext.setText(
            _translate(
                "MainWindow",
                "Girdiğiniz bilgilerin doğruluğundan ve uygunluğundan “Tübitak Projesi” ve geliştiricileri sorumlu değildir. \n"
                "Copyrighted by Tübitak Projesi.",
            )
        )
        self.alttext2.setText(
            _translate(
                "MainWindow",
                "Girdiğiniz bilgilerin doğruluğundan ve uygunluğundan “Tübitak Projesi” ve geliştiricileri sorumlu değildir. \n"
                "Copyrighted by Tübitak Projesi.",
            )
        )


class APP:
    def __init__(self) -> None:
        self.workaround = Workaround()
        self.worker = Worker(self)
        self.windowmanager = MainWindow(self)
        self.windowmanager.show() # bunu acil durum olduğunda arkaplandan hemen ekranın önüne getirmek için kullanabiliriz
        self.worker.get_windowmanager()
        self.windowmanager.connect_login()

        self.workaround.logged.connect(self.windowmanager.loginsuccesful)
        self.workaround.autologged.connect(self.windowmanager.autologinsuccessful)

        self.lastannouncement = "DENEME_DUYURU"
        self.isconnected2db = "CONNECTED_2_DB"
        self.inapp = False

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.threadpool.start(self.worker)
        self.Check_Updates()

    def Check_Updates(self):
        with open("data.json","r") as file:
            self.data = json.load(file)
        self.version = self.data["version"]
        self.password = None if self.data["password"] == 'None' else self.data["password"]
        self.classname = None if self.data["classname"] == 'None' else self.data["classname"]
        self.schoolname = None if self.data["title"] == 'None' else self.data["title"] #title = schoolname 
        if "None" in self.data.values():
            print("NOT LOGGED IN")
        else:
            print("DATA IS ALREADY THERE, TRYING TO LOG INTO ACCOUNT")
            self.worker.StartUpLogin(self.classname,self.password)

    def closeApp(self):
        """called when app is closed"""
        self.inapp = False #this is important since if you dont it might give an error since it deleted the QLabel even tho its trying to access it
        self.worker.running = False
        print("autodelete for worker is:",self.worker.autoDelete())

if __name__ == '__main__':
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    qapp = QApplication(sys.argv)

    qapp.setWindowIcon(QIcon('icon.ico'))
    # icon için özel .ico dosyası lazım

    app = APP()
    qapp.exec()
    
    
    app.closeApp()
    print("ended application")
