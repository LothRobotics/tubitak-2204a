
from ui_theme import central_widget_theme, inapp_container_theme

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QFrame, QLabel, QLineEdit, QPushButton)
from PyQt5.QtCore import (QSettings, QRect, Qt,
                          QCoreApplication, pyqtSlot, pyqtSignal)
#from PyQt5 import QtCore
import sys

RUN_PATH = "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"


class MainWindow(QMainWindow):
    def __init__(self, app, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.app = app
        # self.setObjectName("MainWindow")
        self.setFixedSize(776, 448)

        self.settings = QSettings(RUN_PATH, QSettings.NativeFormat)
        # self.settings.contains("MainWidget")  # checks if it will start on startup
        # set the app for startup
        self.settings.setValue("MainWidget", sys.argv[0])
        self.SetupUI()

    def SetupUI(self):
        self.centralwidget = QWidget(self)  # TTTT
        self.centralwidget.setStyleSheet(
            central_widget_theme
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
            inapp_container_theme
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
        self.schoollabel.setGeometry(QRect(150, 150, 600, 50))
        self.schoollabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignTop)
        self.schoollabel.setObjectName("schoollabel")

        self.announcelabel = QLabel(self.inapp_container)
        self.announcelabel.setGeometry(QRect(150, 200, 500, 50))
        self.announcelabel.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignTop)
        self.announcelabel.setObjectName("announcelabel")

        self.dbcontrollabel = QLabel(self.inapp_container)
        self.dbcontrollabel.setGeometry(QRect(150, 250, 500, 50))
        self.dbcontrollabel.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignTop)
        self.dbcontrollabel.setObjectName("dbcontrollabel")

        self.updatecontainer = QFrame(self.inapp_container)
        self.updatecontainer.setGeometry((776//2) - (500//2), 120, 500, 200)
        self.updatecontainer.setObjectName("UpdateContainer")

        self.updatetext = QLabel(self.inapp_container)
        self.updatetext.setText(
            " Uygulama için yeni bir güncelleme bulundu,\n     uygulamayı güncellemek ister misiniz?")
        self.updatetext.setGeometry((776//2) - (440//2), 90, 440, 200)
        self.updatetext.setObjectName("UpdateText")

        self.updateacceptbut = QPushButton(self.inapp_container)
        self.updateacceptbut.setText("Evet")
        self.updateacceptbut.setGeometry(510, 250, 100, 50)
        self.updateacceptbut.setObjectName("UpdateAcceptButton")

        self.updaterefusebut = QPushButton(self.inapp_container)
        self.updaterefusebut.setText("Hayır")
        self.updaterefusebut.setGeometry(168, 250, 100, 50)
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
        self.lineEdit.setGeometry(QRect(285, 140, 200, 40))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setMaxLength(20)
        self.lineEdit_2 = QLineEdit(self.login_container)
        self.lineEdit_2.setGeometry(QRect(285, 195, 200, 40))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setMaxLength(20)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)

        self.lineEdit_3 = QLineEdit(self.login_container)
        self.lineEdit_3.setGeometry(QRect(285, 250, 200, 40))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setMaxLength(20)
        self.lineEdit_3.setEchoMode(QLineEdit.Password)


        self.pushButton = QPushButton(self.login_container) #sınıfı kaydet butonu
        self.pushButton.setGeometry(QRect(310, 310, 150, 40))
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

    def close_update_buttons(self):
        self.updateacceptbut.hide()
        self.updaterefusebut.hide()

    @pyqtSlot(str)  # bunu kullanmak için qobject olması lazım classın?
    def ConnectionSetText(self, msg: str):
        self.dbcontrollabel.setText(msg)

    def connect_login(self):  # FIXME:
        """To connect the signal and slot"""
        self.pushButton.clicked.connect(self.app.worker.loginButtonPress)

    def loginerror(self, text: str):
        self.errorlabel.setText(text)

        result = self.errorlabel.fontMetrics().boundingRect(self.errorlabel.text()).width()

        # FIXME: i dont have a better idea to do this
        self.errorlabel.setGeometry(QRect(388-int(result/2), 280, 550, 40))
        self.pushButton.setGeometry(QRect(310, 320, 150, 40))
        self.errorlabel.show()
        # This is not the best way to center a text but its good enough atm

    def loginsuccesful(self):
        _translate = QCoreApplication.translate

        self.classlabel.setText(_translate(
            "MainWindow", f"SINIF: {self.app.classname}"))
        self.schoollabel.setText(_translate(
            "MainWindow", f"OKUL: {self.app.schoolname}"))
        self.announcelabel.setText(_translate(
            "MainWindow", f"DUYURU: {self.app.lastannouncement}"))

        self.app.inapp = True
        self.setCentralWidget(self.inapp_container)

    def autologinsuccessful(self):
        _translate = QCoreApplication.translate
        self.classlabel.setText(_translate(
            "MainWindow", f"SINIF: {self.app.classname}"))
        self.schoollabel.setText(_translate(
            "MainWindow", f"OKUL: {self.app.schoolname}"))
        self.announcelabel.setText(_translate(
            "MainWindow", f"DUYURU: {self.app.lastannouncement}"))

        self.app.inapp = True
        self.setCentralWidget(self.inapp_container)

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
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Kullanıcı Adı"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "Şifre"))

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
