from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


import sys,time

RUN_PATH = "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"


class Worker(QRunnable):
    '''
    Worker thread
    '''
    running = True
    def __init__(self,app):
        super().__init__()
        self.app = app

    def get_windowmanager(self):
        self.windowmanager = self.app.windowmanager

    @pyqtSlot()
    def run(self):
        '''
        The code goes in this function
        '''
        print("Thread start")
        while self.running:
            print(".")
            time.sleep(1)
    
    def loginButtonPress(self):
        _translate = QCoreApplication.translate
        print("LOGIN")

        self.app.classname = self.windowmanager.lineEdit.text()
        #self.windowmanager.infowidget.label1.setText("SINIF: {}".format(self.app.classname))
        #self.windowmanager.infowidget.label2.setText("OKUL: {}".format("ÖRNEK"))
        self.windowmanager.classlabel.setText(_translate("MainWindow", f"SINIF: {self.app.classname}"))
        self.windowmanager.schoollabel.setText(_translate("MainWindow", f"OKUL: {self.app.schoolname}"))
        self.windowmanager.announcelabel.setText(_translate("MainWindow", f"DUYURU: {self.app.lastannouncement}"))
        self.windowmanager.dbcontrollabel.setText(_translate("MainWindow", f"DB: {self.app.isconnected2db}"))

        print("USERNAME:",self.app.classname, "SCHOOL:","ÖRNEK")
        self.app.windowmanager.setCentralWidget(self.app.windowmanager.inapp_container) 

# class InfoWidget(QWidget):
#     def __init__(self,windowmanager,*args,**kwargs) -> None:
#         super(InfoWidget, self).__init__(*args, **kwargs)
#         self.windowmanager = windowmanager
        
#         self.layout = QVBoxLayout()
#         self.layout.setContentsMargins(0,0,0,0)
#         self.layout.setStretch(0,0)

#         self.label1 = QLabel("Sınıf ismi")
#         self.label1.setFont(QFont("Arial",16))
#         self.label1.setAlignment(Qt.AlignmentFlag.AlignTop)
#         self.layout.addWidget(self.label1)
#         self.label1.setMaximumHeight(20)

#         self.label2 = QLabel("AAA")
#         self.label2.setFont(QFont("Arial",16))
#         self.label2.setAlignment(Qt.AlignmentFlag.AlignTop)
#         self.layout.addWidget(self.label2)

#         self.setLayout(self.layout)

class MainWindow(QMainWindow):
    def __init__(self, app, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.app = app
        #self.setObjectName("MainWindow")
        self.setFixedSize(776, 448)

        self.settings = QSettings(RUN_PATH, QSettings.NativeFormat) 
        # self.settings.contains("MainWidget")  # checks if it will start on startup
        self.settings.setValue("MainWidget",sys.argv[0]); #set the app for startup

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
        self.lineEdit_2 = QLineEdit(self.login_container)
        self.lineEdit_2.setGeometry(QRect(285, 230, 200, 40))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QPushButton(self.login_container)
        self.pushButton.setGeometry(QRect(310, 290, 150, 40))
        self.pushButton.setObjectName("pushButton")
        self.alttext = QLabel(self.login_container)
        self.alttext.setGeometry(QRect(0, 400, 776, 41))
        self.alttext.setAlignment(Qt.AlignCenter)
        self.alttext.setObjectName("alttext")

        self.alttext2 = QLabel(self.inapp_container)
        self.alttext2.setGeometry(QRect(0, 400, 776, 41))
        self.alttext2.setAlignment(Qt.AlignCenter)
        self.alttext2.setObjectName("alttext2")

        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        #QMetaObject.connectSlotsByName(MainWindow)

    def connect_login(self):
        self.pushButton.clicked.connect(self.app.worker.loginButtonPress)

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
        self.worker = Worker(self)
        self.windowmanager = MainWindow(self)
        self.windowmanager.show() # bunu acil durum olduğunda arkaplandan hemen ekranın önüne getirmek için kullanabiliriz
        self.worker.get_windowmanager()
        self.windowmanager.connect_login()

        self.classname = None
        self.schoolname = "ÖRNEK_OKUL"
        self.lastannouncement = "DENEME_DUYURU"
        self.isconnected2db = "CONNECTED_2_DB"

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.threadpool.start(self.worker)

    def closeApp(self):
        """called when app is closed"""
        self.worker.running = False
        print("autodelete for worker is:",self.worker.autoDelete())



if __name__ == '__main__':
    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    qapp = QApplication(sys.argv)

    qapp.setWindowIcon(QIcon('icon.ico'))
    # icon için özel .ico dosyası lazım

    app = APP()

    # Start the event loop.
    qapp.exec()

    # Your application won't reach here until you exit and the event
    # loop has stopped.
    app.closeApp()
    print("ended application")
