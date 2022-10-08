from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
# The main modules for Qt are QtWidgets, QtGui and QtCore.

import sys,time

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
        Your code goes in this function
        '''
        print("Thread start")
        #time.sleep(5)
        #print("Thread complete")
        while self.running:
            print("running")
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

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        # stylesheet = "MainWindow{background-color: red;background-image:"+filename+";}"
        stylesheet = """MainWindow{
            background-color: red; 
            background-image: url(background.png); 
            background-position: center;
            }"""
        self.setStyleSheet(stylesheet)

        self.setMinimumSize(600,450)
        self.app = app
        self.counter = 0

        login_layout = QVBoxLayout()

        """ BACKGROUND STUFF
        self.backgroundimg = QPicture()
        painter = QPainter(self.backgroundimg)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setPen(QPen(Qt.black, 12, Qt.SolidLine, Qt.RoundCap))

        #painter.drawLine(100,100,200,200)
        painter.drawEllipse(50,50,100,100)
        self.backgroundwidget = QLabel()
        self.backgroundwidget.setPicture(self.backgroundimg)
        self.backgroundwidget.show()
        login_layout.addWidget(self.backgroundwidget)
        """

        self.label1 = QLabel("Tübitak Projesi")
        self.label1.setFont(QFont("Arial",24))
        self.label1.setAlignment(Qt.AlignHCenter)
        login_layout.addWidget(self.label1)

        self.label2 = QLabel("Deprem Uygulaması \n Lorem Ipsum")
        self.label2.setFont(QFont("Arial",16))
        self.label2.setAlignment(Qt.AlignHCenter)
        login_layout.addWidget(self.label2)

        login_layout.setContentsMargins(0,0,0,-1010)
        #self.input.textChanged.connect(self.label.setText)
        
        buttonstylesheet = r"color: black; background-color: white; border: 2px solid black; border-radius:2px;"
        buttonfont = QFont("Arial",24)
        buttonfont2 = QFont("Arial",16)

        self.input = QLineEdit()
        self.input.setFixedWidth(200)
        self.input.setMinimumHeight(25)
        #self.input.textChanged.connect(self.label.setText)
        self.input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.input.setContentsMargins(20,0,0,0)
        self.input.setFont(buttonfont2)
        self.input.setStyleSheet(buttonstylesheet)
        login_layout.addWidget(self.input)

        self.input2 = QLineEdit()
        self.input2.setFixedWidth(200)
        self.input2.setMinimumHeight(25)
        self.input2.setFont(buttonfont2)
        #self.input.textChanged.connect(self.label.setText)
        self.input2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.input2.setContentsMargins(20,0,0,0)
        self.input2.setStyleSheet(buttonstylesheet)
        login_layout.addWidget(self.input2)
        #self.input.setWindowIcon

        self.enterbutton = QPushButton()
        self.enterbutton.setText("Giriş Yap")
        self.enterbutton.setFont(buttonfont)
        self.enterbutton.setMaximumSize(240,50)
        self.enterbutton.setStyleSheet(buttonstylesheet)

        login_layout.addWidget(self.enterbutton)

        self.label3 = QLabel("Lorem Ipsum Dolor Amet \nLorem Ipsum Dolor Amet")
        self.label3.setFont(QFont("Arial",16))
        self.label3.setAlignment(Qt.AlignmentFlag.AlignBottom)
        login_layout.addWidget(self.label3)
        
        login_layout.setSpacing(-1)
        login_layout.setStretch(0,0)
        login_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.login_container = QWidget()
        self.login_container.setLayout(login_layout)
        self.enterbutton.clicked.connect(self.app.worker.loginButtonPress)


        inapp_layout = QVBoxLayout()

        self.label3 = QLabel("Tübitak Projesi")
        self.label3.setFont(QFont("Arial",24))
        self.label3.setAlignment(Qt.AlignHCenter)
        inapp_layout.addWidget(self.label3)

        self.infowidget = InfoWidget(self)
        inapp_layout.addWidget(self.infowidget)

        self.label6 = QLabel("Lorem Ipsum Dolor Amet \nLorem Ipsum Dolor Amet")
        self.label6.setFont(QFont("Arial",16))
        self.label6.setAlignment(Qt.AlignmentFlag.AlignBottom)
        inapp_layout.addWidget(self.label6)
        
        inapp_layout.setSpacing(-1)
        inapp_layout.setStretch(0,0)
        inapp_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.inapp_container = QWidget()
        self.inapp_container.setLayout(inapp_layout)

        # Set the central widget of the Window.
        self.setCentralWidget(self.login_container)

        #self.setCentralWidget(self.backgroundwidget)
        #self.backgroundwidget.Widget

        self.show()

        #self.timer = QTimer()
        #self.timer.setInterval(1000)
        #self.timer.timeout.connect(self.recurring_timer)
        #self.timer.start()


    def bpress(self):
        # these 2 lines are for creating a new thread
        #worker = Worker()
        #self.threadpool.start(worker)
        
        #time.sleep(5)
        pass

    def closeEvent(self, event):
        self.app.closeApp()
        event.accept()


    #def recurring_timer(self):
    #    self.counter +=1
    #    self.l.setText("Counter: %d" % self.counter)


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

    # Qt.WidgetAttribute.WA_StyledBackground
    
    # app.setWindowIcon(QtGui.QIcon('hand.ico'))
    # icon için özel .ico dosyası lazım

    app = APP()

    

    # Start the event loop.
    qapp.exec()

    # Your application won't reach here until you exit and the event
    # loop has stopped.
    print("ended application")
