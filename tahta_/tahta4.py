from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import json
import sys,time,os,datetime

import hashlib

sys.path.insert(1, '.') #also look for 1 folder back #TODO: Comment this when releasing the app
from database_handler import DatabaseHandler
from updater import InvalidReleaseVer, VersionChecker

db = DatabaseHandler("data/db_credentials.json")

RUN_PATH = "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"

from logging.handlers import TimedRotatingFileHandler
import logging

class CustomFormatter(logging.Formatter):
    dgrey = "\x1b[1;30m" 
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - (%(filename)s:%(lineno)d) - [%(levelname)s] :::  %(message)s "

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: dgrey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# create logger with 'spam_application'
logger = logging.getLogger("My_app")
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
consolehandler = logging.StreamHandler()
consolehandler.setLevel(logging.DEBUG)
consolehandler.setFormatter(CustomFormatter())

# Create file handler for logging to a file (logs all five levels)
today = datetime.date.today()
#file_handler = logging.FileHandler('logs/uygulama {} .log'.format(today.strftime('%Y_%m_%d')))
#file_handler.setLevel(logging.DEBUG)
#file_handler.setFormatter(CustomFormatter())

g = time.localtime()
minute = g.tm_min
hour = g.tm_hour
second = g.tm_sec

if os.path.isdir("logs"):
    print("logs folder found")
else: #make sure that the logs folder is ready to put files in so filehandler doesnt raise an error
    print("no logs folder found")
    os.makedirs("logs")

timed_file_handler = TimedRotatingFileHandler(filename='logs/uygulama {}.log'.format(today.strftime('%Y_%m_%d')),
    when='D', interval=1, backupCount=5, encoding='utf-8', delay=False)
timed_file_handler.setLevel(logging.INFO)
timed_file_handler.setFormatter(CustomFormatter())

logger.addHandler(consolehandler)
logger.addHandler(timed_file_handler)

logger.warning("________________________STARTING SCRIPT_______________________")

class AppTray(QSystemTrayIcon):
    def __init__(self):
        super().__init__(QIcon("icon.ico"))
        self.setToolTip("Hello")
        self.show()
        self.menu = QMenu()
        exitaction = self.menu.addAction("Exit")
        exitaction.triggered.connect(qapp.quit)
        
        self.setContextMenu(self.menu)

def check_connection():
    connection = db.get("checkconnection", ["check == True"] )

    if connection == [{'check': 'True'}]:
        return True
    else:
        return False

class SignalManager(QObject):
    logged = pyqtSignal()
    autologged = pyqtSignal()

    remindupdate = pyqtSignal()
    close_updatereminder = pyqtSignal()
    startupdating = pyqtSignal()

    updatedone = pyqtSignal()
    
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
        logger.info("Thread start")
        while self.running:
            st = time.time()
            time.sleep(1)
            self.timer += time.time() - st

            if self.app.inapp: #TODO: Add classroom adding
                pass
            if int(self.timer) % 60 == 0:
                logger.warning("ConnectionSetText directly called from worker")
                self.windowmanager.ConnectionSetText() #FIXME: WHY does this not use a signal

            # self.get_announcement() #maybe not put this in here? 

            if self.timer > 60*10:
                logger.info("10 Minute check")
                self.timer = 0

    def testupdate(self):
        print("worker testupdate start")
        self.app.ver_checker.update()
        print("worker testupdate END")

    def get_announcement(self):
        pass

    def check_db_connection(self):
        pass

    def loginButtonPress(self):
        logger.info("LOGIN")

        if len(self.windowmanager.lineEdit.text()) < 1 or len(self.windowmanager.lineEdit_2.text()) < 1:
            logger.error("ERROR LENGTH OF CLASSNAME OR PASSWORD TOO SHORT")
            self.windowmanager.loginerror("Şifre veya Sınıf ismi çok kısa") 
        else:
            self.app.classname:str = self.windowmanager.lineEdit.text()
            self.app.password:str = self.windowmanager.lineEdit_2.text()
            hashed_password = hashlib.sha256(self.app.password.encode()).hexdigest()
            
            logger.info(f"password:{self.app.password} hashed password: {hashed_password}")

            result = db.get("accounts", [f"password == {hashed_password}"], auto_format = False )

            if type(result) == bool:
                pass
            else:
                if len(result) < 1:
                    self.windowmanager.loginerror("Yanlış Şifre")
                    logger.error("WRONG PASSWORD")
                elif len(result) > 1:
                    logger.error("MORE THAN 1 ACCOUNT WITH THE SAME PASSWORD")
                    self.windowmanager.loginerror("Giriş yapmada belli bir hatayla karşılaşıldı") 
                else:
                    logger.info(f"CLASSNAME: {self.app.classname} SCHOOL: {self.app.schoolname}")
                    
                    id:str = result[0].id
                    classrooms:dict = result[0].to_dict()["classrooms"]
                    
                    found = False
                    for key, val in classrooms.items():
                        if self.app.classname == key:
                            found = True
                            logger.info("FOUND THE CLASS")
                            
                    loginkey = None
                    if found: #hesap zaten var
                        loginkey = classrooms[self.app.classname]
                        logger.info(f"CLASS ALREADY EXISTS, KEY: {loginkey}")
                    else: #hesap yok, yeni hesap oluştur
                        loginkey = hashlib.sha256((id + self.app.classname).encode()).hexdigest()
                        classrooms[self.app.classname] = loginkey
                        logger.info(f"CLASS DOESN'T EXIST, CREATED KEY: {loginkey}")

                    db.update('accounts', id, {'classrooms': classrooms }) #TODO: Save the data and change autologin to use the key instead

                    self.app.signalmanager.logged.emit()

    def StartUpLogin(self,inp1:str,inp2:str): #NOTE: I have to create another func for this since I cant give arguments with a slot
        logger.info("LOGIN")

        if len(inp1) < 1 or len(inp2) < 1: 
            logger.error("ERROR LENGTH OF CLASSNAME OR PASSWORD TOO SHORT")
            self.windowmanager.loginerror("Şifre veya Sınıf ismi çok kısa") 
        else:
            self.app.classname = inp1
            self.app.password = inp2
            hashed_password = hashlib.sha256(self.app.password.encode()).hexdigest()
            
            logger.info(f"password:{self.app.password} hashed password: {hashed_password}")
            
            result = db.get("accounts", [f"password == {hashed_password}"] )
            if type(result) == bool:
                pass
            
            else:
                if len(result) < 1:
                    self.windowmanager.loginerror("Yanlış Şifre")
                    logger.error("WRONG PASSWORD")
                elif len(result) > 1:
                    logger.error("MORE THAN 1 ACCOUNT WITH THE SAME PASSWORD")
                    self.windowmanager.loginerror("Giriş yapmada belli bir hatayla karşılaşıldı")
                else:
                    logger.info("CLASSNAME:",self.app.classname, "SCHOOL:","TESTOKULU")
                    self.app.signalmanager.autologged.emit()
                    if self.app.shouldupdate:
                        self.app.signalmanager.remindupdate.emit()
                    else:
                        self.app.signalmanager.close_updatereminder.emit()

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
            "#UpdateContainer {\n"
            "    background-color: #2a4980; border-radius: 6px;  \n"
            "}\n"
            "#UpdateText {\n"
            "    font-size: 22px; color: #cbdbf7  ;\n"
            "}\n"
            "#UpdateRefuseButton {\n"
            "    font-size: 22px;\n"
            "}\n"
            "#UpdateAcceptButton {\n"
            "    font-size: 22px;\n"
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
        
        self.updatecontainer = QFrame(self.inapp_container)
        self.updatecontainer.setGeometry((776//2) - (500//2) ,120,500,200)
        self.updatecontainer.setObjectName("UpdateContainer")

        self.updatetext = QLabel(self.inapp_container)
        self.updatetext.setText(" Uygulama için yeni bir güncelleme bulundu,\n     uygulamayı güncellemek ister misiniz?")
        self.updatetext.setGeometry((776//2) - (440//2),90,440,200)
        self.updatetext.setObjectName("UpdateText")

        self.updateacceptbut = QPushButton(self.inapp_container)
        self.updateacceptbut.setText("Evet")
        self.updateacceptbut.setGeometry(510,250,100,50)
        self.updateacceptbut.setObjectName("UpdateAcceptButton")

        self.updaterefusebut = QPushButton(self.inapp_container)
        self.updaterefusebut.setText("Hayır")
        self.updaterefusebut.setGeometry(168,250,100,50)
        self.updaterefusebut.setObjectName("UpdateRefuseButton")

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

    def remind_update(self):
        print("UPDATE UI SHOW")
        self.updatecontainer.show()
        self.updatetext.show()
        self.updateacceptbut.show()
        self.updaterefusebut.show()
    def close_update_reminder(self):
        print("UPDATE UI CLOSE")
        self.updatecontainer.hide()
        self.updatetext.hide()
        self.updateacceptbut.hide()
        self.updaterefusebut.hide()
    def set_updating_text(self,message:str):
        print("JUST DO IT")
        self.updatetext.setText(message)

    def close_update_buttons(self):
        self.updateacceptbut.hide()
        self.updaterefusebut.hide()

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
        logger.info("login successful")

    def autologinsuccessful(self):
        _translate = QCoreApplication.translate
        self.classlabel.setText(_translate("MainWindow", f"SINIF: {self.app.classname}"))
        self.schoollabel.setText(_translate("MainWindow", f"OKUL: {self.app.schoolname}"))
        self.announcelabel.setText(_translate("MainWindow", f"DUYURU: {self.app.lastannouncement}"))

        self.ConnectionSetText()
        
        self.app.inapp = True
        self.setCentralWidget(self.inapp_container)
        logger.info("Succesfull startup login")

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
        logger.info("Create APP Instance")
        self.signalmanager = SignalManager()
        logger.info("Create SignalManager Instance")
        self.worker = Worker(self)
        logger.info("Create Worker Instance")
        self.windowmanager = MainWindow(self)
        logger.info("Create WindowManager Instance")
        self.windowmanager.show() # bunu acil durum olduğunda arkaplandan hemen ekranın önüne getirmek için kullanabiliriz
        logger.info("Show Window")
        self.worker.get_windowmanager()
        logger.info("Connect Login")
        self.windowmanager.connect_login()
        
        with open("data/version.json","r") as file:
            self.version:float = json.load(file)["version"]
        
        self.tray = AppTray()
        self.ver_checker = VersionChecker(self,self.version)

        self.signalmanager.logged.connect(self.windowmanager.loginsuccesful)
        self.signalmanager.autologged.connect(self.windowmanager.autologinsuccessful)
        self.signalmanager.remindupdate.connect(self.windowmanager.remind_update)
        self.signalmanager.close_updatereminder.connect(self.windowmanager.close_update_reminder)
        self.signalmanager.updatedone.connect(self.windowmanager.close_update_reminder)
        
        self.windowmanager.updateacceptbut.clicked.connect(self.worker.testupdate) #TODO:
        self.windowmanager.updateacceptbut.clicked.connect(self.windowmanager.close_update_buttons)
        
        #self.ver_checker.progresssignal.connect(self.windowmanager.set_updating_text)
        #self.ver_checker.finishedsignal.connect(self.windowmanager.close_update_reminder)

        self.windowmanager.updaterefusebut.clicked.connect(self.signalmanager.close_updatereminder)

        self.lastannouncement = "DENEME_DUYURU" #TODO:
        self.isconnected2db = "CONNECTED_2_DB" 
        self.inapp = False

        self.threadpool = QThreadPool()
        logger.info("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.threadpool.start(self.worker)
        logger.info("Start Worker")
        self.Check_Updates()

    def Check_Updates(self):
        with open("data/data.json","r",encoding="utf-8") as file:
            self.data = json.load(file)
        
        logger.info("CHECKING VERSION")
        #self.signalmanager.startupdating.connect(self.ver_checker.update)
        self.shouldupdate = False

        try:
            result = self.ver_checker.check_version()
            if result:
                logger.info("NEW UPDATE")
            else:
                logger.info("ALREADY THE NEWEST VERSION")
            self.shouldupdate = result
        except InvalidReleaseVer:
            logger.error("INVALID VERSION")

        self.password = None if self.data["password"] == 'None' else self.data["password"]
        self.classname = None if self.data["classname"] == 'None' else self.data["classname"]
        self.schoolname = None if self.data["title"] == 'None' else self.data["title"] #title = schoolname 
        if "None" in self.data.values():
            logger.info("NOT LOGGED IN")
        else:
            logger.info("DATA IS ALREADY THERE, TRYING TO LOG INTO ACCOUNT")
            self.worker.StartUpLogin(self.classname,self.password)

    def closeApp(self):
        """called when app is closed"""
        self.inapp = False #this is important since if you dont it might give an error since it deleted the QLabel even tho its trying to access it
        self.worker.running = False
        logger.info(f"autodelete for worker is: {self.worker.autoDelete()}")

if __name__ == '__main__':
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    qapp = QApplication(sys.argv)

    qapp.setWindowIcon(QIcon('icon.ico'))
    # icon için özel .ico dosyası lazım

    app = APP()
    qapp.exec()
    
    app.closeApp()
    logger.info("ended application")
    
    sys.exit()
