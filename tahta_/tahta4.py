from PyQt5.QtWidgets import QSystemTrayIcon,QApplication,QMenu
from PyQt5.QtCore import QObject,pyqtSignal,QRunnable,pyqtSlot,QThreadPool
from PyQt5.QtGui import QIcon

import json,sys,time,os,datetime,hashlib
from typing import Dict

from logging.handlers import TimedRotatingFileHandler
import logging

sys.path.insert(1, '.') #also look for 1 folder back #TODO: Comment this when releasing the app
from database_handler import DatabaseHandler
from updater import InvalidReleaseVer, VersionChecker
from ui import MainWindow

db = DatabaseHandler("data/db_credentials.json")
RUN_PATH = "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"

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

today = datetime.datetime.now()

# Create file handler for logging to a file (logs all five levels)
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

timed_file_handler = TimedRotatingFileHandler(filename='logs/uygulama {}.log'.format( today.strftime('%Y_%m_%d') #today.strftime('%Y_%m_%d - %H_%M_%S')
),
    when='D', interval=1, backupCount=5, encoding='utf-8', delay=False)
timed_file_handler.setLevel(logging.INFO)
timed_file_handler.setFormatter(CustomFormatter())

logger.addHandler(consolehandler)
logger.addHandler(timed_file_handler)

logger.warning("_______________________ STARTING APP _______________________")

class Theme:
    def __init__(self) -> None:
        pass

class AppTray(QSystemTrayIcon):
    def __init__(self, wm_closewindow, wm_openwindow): #windowmanager
        super().__init__(QIcon("appdata/app_icon.ico"))
        self.wm_closewindow = wm_closewindow
        self.wm_openwindow = wm_openwindow
        self.setToolTip("Hello")
        self.show()
        self.menu = QMenu()
        exitaction = self.menu.addAction("Uygulamayı kapat")
        exitaction.triggered.connect(qapp.quit)
        self.closewindow = self.menu.addAction("Pencereyi gizle")
        self.closewindow.triggered.connect(self.wm_closewindow)
        self.openwindow = self.menu.addAction("Pencereyi göster")
        self.openwindow.triggered.connect(self.wm_openwindow)
        
        self.setContextMenu(self.menu)

def check_connection(): #FIXME: There must be a better way to do this
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

    conn_settext_signal = pyqtSignal(str)
    
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

            if self.app.inapp:
                pass
            if int(self.timer) % 10 == 0:
                logger.info("Connectionsettext check")
                if check_connection(): 
                    self.app.signalmanager.conn_settext_signal.emit('Veritabanı Durumu: <font color="#56cc41">Bağlantı Stabil</font>')
                else:
                    self.app.signalmanager.conn_settext_signal.emit('Veritabanı Durumu: <font color="#c92a2a">Bağlantı Bulunamadı</font>')

            # self.get_announcement() #maybe not put this in here? 

            if self.timer > 60*10:
                logger.info("10 Minute check")
                self.timer = 0

    def testupdate(self):
        logger.info("worker testupdate START")
        self.app.ver_checker.update()
        logger.info("worker testupdate END")

    def get_announcement(self):
        pass

    def loginButtonPress(self):
        logger.info("LOGIN ATTEMPT")

        if len(self.windowmanager.lineEdit.text()) <1 or len(self.windowmanager.lineEdit_2.text()) < 1:
            logger.error("LENGTH OF CLASSNAME OR PASSWORD TOO SHORT")
            return None
        
        # no problem
        self.app.classname = self.windowmanager.lineEdit.text()
        password = self.windowmanager.lineEdit_2.text()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        logger.info("CREATED HASHED_PASSWORD")
        result = db.get("accounts", [f"password == {hashed_password}", 
            f"username == {self.app.username}"], auto_format=False)

        if type(result) == bool:
            return None
        if len(result) < 1:
            logger.error("WRONG PASSWORD")
            self.windowmanager.loginerror("Yanlış Şifre")
            return None
        elif len(result) > 1:
            logger.error("HAVING TROUBLE LOGGING INTO ACCOUNT") 
            self.windowmanager.loginerror("Giriş yapmada belli bir hatayla karşılaşıldı") 
            return None

        logger.info(f"LOGGED IN, CLASSNAME: {self.app.classname} SCHOOL: {self.app.schoolname}")
        id = result[0].id
        formatted_result = result[0].to_dict()

        classrooms = formatted_result["classrooms"] #get the classrooms
        self.app.schoolname = formatted_result["school"]["school_name"] #get the schoolname from db 
            
        if classrooms.__contains__(self.app.classname):
            logger.info("CLASSKEY ALREADY EXISTS")
            classkey = classrooms[self.app.classname]
        else:
            logger.info("CLASSKEY DOESNT EXIST")
            logger.info("CREATING NEW CLASSKEY")
            # furkana sor burayı 
            classkey = hashlib.sha256((hashed_password + id + self.app.classname).encode()).hexdigest()
            classrooms[self.app.classname] = classkey
            logger.info("CREATED KEY")
        
        with open("data\data.json","r", encoding="utf-8") as datafile:
            data = json.load(datafile)
            data["classkey"] = classkey
            data["schoolname"] = self.app.schoolname
        with open("data\data.json", "w", encoding="utf-8") as datafile:
            json.dump(data, datafile, ensure_ascii=False, indent=4)

        db.update('accounts', id, {'classrooms': classrooms}) # update the new
        if check_connection():
            self.app.signalmanager.conn_settext_signal.emit('Veritabanı Durumu: <font color="#56cc41">Bağlantı Stabil</font>')
        else:
            self.app.signalmanager.conn_settext_signal.emit('Veritabanı Durumu: <font color="#c92a2a">Bağlantı Bulunamadı</font>')
        
        self.app.signalmanager.logged.emit()

    def StartUpLogin(self): 
        logger.info("ATTEMPTING AUTO-LOGIN")

        result = db.get("accounts", [f"username == {self.app.username}"], auto_format=False )
        if type(result) == bool:
            return None
        if len(result) < 1:
            self.windowmanager.loginerror("Yanlış Şifre")
            logger.error("WRONG PASSWORD")
            return None
        elif len(result) > 1:
            logger.error("ACCOUNT PROBLEMS")
            self.windowmanager.loginerror("Giriş yapmada hatayla karşılaşıldı")
            return None

        formatted_result = result[0].to_dict()
        classrooms:dict = formatted_result["classrooms"] 
        
        if classrooms.__contains__(self.app.classname) == False:
            self.windowmanager.loginerror("Otomatik giriş yapılamadı.")
            logger.error("CLASSROOMS DOESNT HAVE CLASSNAME IN DB")
            return None
        if (classrooms.__contains__(self.app.classname)) and (classrooms[self.app.classname] != self.app.classkey):
            self.windowmanager.loginerror("Otomatik giriş yapılamadı.")
            logger.error("CLASSKEY != DB CLASSKEY")
            return None

        # get the schoolname from db
        self.app.schoolname = formatted_result["school"]["school_name"]

        with open("data\data.json","r", encoding="utf-8") as datafile:
            data = json.load(datafile)
            data["schoolname"] = self.app.schoolname
        with open("data\data.json","w", encoding="utf-8") as datafile:
            json.dump(data, datafile, ensure_ascii=False, indent=4)

        if check_connection():
            self.app.signalmanager.conn_settext_signal.emit('Veritabanı Durumu: <font color="#56cc41">Bağlantı Stabil</font>')
        else:
            self.app.signalmanager.conn_settext_signal.emit('Veritabanı Durumu: <font color="#c92a2a">Bağlantı Bulunamadı</font>')
        self.app.signalmanager.autologged.emit()

        if self.app.shouldupdate:
            self.app.signalmanager.remindupdate.emit()
        else:
            self.app.signalmanager.close_updatereminder.emit()
        logger.info("SUCCESSFUL AUTO-LOGIN")


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
        
        self.tray = AppTray(  self.windowmanager.hide, self.windowmanager.show )
        self.ver_checker = VersionChecker(self,self.version)

        self.signalmanager.logged.connect(self.windowmanager.loginsuccesful)
        self.signalmanager.autologged.connect(self.windowmanager.autologinsuccessful)
        self.signalmanager.remindupdate.connect(self.windowmanager.remind_update)
        self.signalmanager.close_updatereminder.connect(self.windowmanager.close_update_reminder)
        self.signalmanager.updatedone.connect(self.windowmanager.close_update_reminder)
        
        intercept = lambda msg : self.windowmanager.ConnectionSetText(msg)
        self.signalmanager.conn_settext_signal.connect( intercept ) #you create an intermediary func(with lambda) like this when you want to pass data in signals 
        #TODO: FIXME: From what I've read this can result in a memory leak but if this creates an problem we should fix it

        self.windowmanager.updateacceptbut.clicked.connect(self.worker.testupdate)
        self.windowmanager.updateacceptbut.clicked.connect(self.windowmanager.close_update_buttons)

        self.windowmanager.updaterefusebut.clicked.connect(self.signalmanager.close_updatereminder)
        self.lastannouncement = "DENEME_DUYURU"
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

        self.classkey = None if self.data["classkey"] == 'None' else self.data["classkey"] #changed this from password to classkey
        self.classname = None if self.data["classname"] == 'None' else self.data["classname"]
        self.schoolname = None if self.data["schoolname"] == 'None' else self.data["schoolname"] #changed this from title to schoolname
        self.username = None if self.data["username"] == 'None' else self.data["username"]

        if "None" in self.data.values():
            logger.info("NOT LOGGED IN")
        else:
            logger.info("DATA IS ALREADY THERE, TRYING TO LOG INTO ACCOUNT")
            self.worker.StartUpLogin()

    def closeApp(self):
        """called when app is closed"""
        self.inapp = False #it might give an error since it deleted the QLabel even tho its trying to access it
        self.worker.running = False
        logger.info(f"autodelete for worker is: {self.worker.autoDelete()}")

if __name__ == '__main__':
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    qapp = QApplication(sys.argv)

    qapp.setWindowIcon(QIcon('appdata/app_icon.ico'))
    # FIXME: https://stackoverflow.com/questions/17914960/pyqt-runtimeerror-wrapped-c-c-object-has-been-deleted
    # https://stackoverflow.com/questions/5339062/python-pyside-internal-c-object-already-deleted
    # I dont think this will happen but if it does, here are some links to fix it 

    app = APP()
    qapp.exec()

    app.closeApp()
    logger.info("ended application")
    
    sys.exit()
