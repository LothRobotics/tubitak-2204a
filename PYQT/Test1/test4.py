from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time

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


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0

        layout = QVBoxLayout()

        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.bpress)

        layout.addWidget(self.l)
        layout.addWidget(b)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.worker = Worker()
        self.threadpool.start(self.worker)


    def bpress(self):
        # these 2 lines are for creating a new thread
        #worker = Worker()
        #self.threadpool.start(worker)
        
        #time.sleep(5)
        pass

    def closeEvent(self, event):
        self.worker.running = False
        print("autodelete for worker is:",self.worker.autoDelete())
        event.accept()

    def recurring_timer(self):
        self.counter +=1
        self.l.setText("Counter: %d" % self.counter)




app = QApplication([])
window = MainWindow()
app.exec_()