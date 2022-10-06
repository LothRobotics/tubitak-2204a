from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
# The main modules for Qt are QtWidgets, QtGui and QtCore.

import sys,time




class Worker(QRunnable):
    '''
    Worker thread
    '''
    running = True

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




class MainWindow(QMainWindow):


    def __init__(self, app, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setMinimumSize(600,450)

        self.app = app
        self.counter = 0

        layout = QVBoxLayout()
        
        self.label1 = QLabel("Tübitak Projesi")
        self.label1.setFont(QFont("Arial",24))
        self.label1.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.label1)


        self.label2 = QLabel("Deprem Uygulaması \n Lorem Ipsum")
        self.label2.setFont(QFont("Arial",16))
        self.label2.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.label2)


        """
        for _ in range(6):
            lbl = QLabel("Deprem Uygulaması \n Lorem Ipsum")
            lbl.setFont(QFont("Arial",16))
            lbl.setAlignment(Qt.AlignHCenter)
            layout.addWidget(lbl)
        """

        print(layout.setContentsMargins(0,0,0,-1010))
        #self.input.textChanged.connect(self.label.setText)
        
        self.input = QLineEdit()
        self.input.setFixedWidth(200)
        #self.input.textChanged.connect(self.label.setText)
        self.input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.input.setContentsMargins(20,0,0,0)
        layout.addWidget(self.input)

        self.input2 = QLineEdit()
        self.input2.setFixedWidth(200)
        #self.input.textChanged.connect(self.label.setText)
        self.input2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.input2.setContentsMargins(20,0,0,0)
        layout.addWidget(self.input2)
        #self.input.setWindowIcon

        self.enterbutton = QPushButton()
        self.enterbutton.setMinimumSize(20,10)
        self.enterbutton.setMaximumSize(240,40)

        layout.addWidget(self.enterbutton)

        

        #self.checkbox = QCheckBox()
        #self.checkbox.setCheckState(Qt.PartiallyChecked)
        #self.checkbox.stateChanged.connect(self.show_state)
        #layout.addWidget(self.checkbox)
        
        self.label3 = QLabel("Lorem Ipsum Dolor Amet \nLorem Ipsum Dolor Amet")
        self.label3.setFont(QFont("Arial",16))
        self.label3.setAlignment(Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(self.label3)
        
        layout.setSpacing(-1)
        layout.setStretch(0,0)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

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
        self.windowmanager = MainWindow(self)
        self.windowmanager.show() # bunu acil durum olduğunda arkaplandan hemen ekranın önüne getirmek için kullanabiliriz

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.worker = Worker()
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
    # app.setWindowIcon(QtGui.QIcon('hand.ico'))
    # icon için özel .ico dosyası lazım

    app = APP()
    #app.obj_thread.start() TODO: ADD THIS 31

    # Start the event loop.
    qapp.exec()

    # Your application won't reach here until you exit and the event
    # loop has stopped.
    print("ended application")
