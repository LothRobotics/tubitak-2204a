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
        print("LOGIN")
        self.app.classname = self.app.windowmanager.input.text()
        self.app.windowmanager.infowidget.label1.setText("SINIF: {}".format(self.app.classname))
        self.app.windowmanager.infowidget.label2.setText("OKUL: {}".format("ÖRNEK"))

        print("USERNAME:",self.app.classname, "SCHOOL:","ÖRNEK")
        self.app.windowmanager.setCentralWidget(self.app.windowmanager.inapp_container) 

class InfoWidget(QWidget):
    def __init__(self,windowmanager,*args,**kwargs) -> None:
        super(InfoWidget, self).__init__(*args, **kwargs)
        self.windowmanager = windowmanager
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setStretch(0,0)

        self.label1 = QLabel("Sınıf ismi")
        self.label1.setFont(QFont("Arial",16))
        self.label1.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.label1)
        self.label1.setMaximumHeight(20)

        self.label2 = QLabel("AAA")
        self.label2.setFont(QFont("Arial",16))
        self.label2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.label2)

        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    def __init__(self, app, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #self.setObjectName("MainWindow")
        self.setFixedSize(776, 448)

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
        self.inapp_container.setObjectName("frame") #### PUT THE INAPP LAYOUT STUFF IN THIS CONTAINER


        self.apptitle = QLabel(self.login_container)
        self.apptitle.setGeometry(QRect(0, 0, 776, 60))
        self.apptitle.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.apptitle.setObjectName("apptitle")
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
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        #QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.apptitle.setText(_translate("MainWindow", "Tübitak Projesi"))
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


class APP:
    def __init__(self) -> None:
        self.worker = Worker(self)
        self.windowmanager = MainWindow(self)
        self.windowmanager.show() # bunu acil durum olduğunda arkaplandan hemen ekranın önüne getirmek için kullanabiliriz

        self.classname = None

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





