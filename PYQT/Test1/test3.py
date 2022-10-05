from PyQt5.QtCore import Qt,QThread,QObject,pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QPushButton,QLabel, QLineEdit, QVBoxLayout,QMenu,QAction,QCheckBox
from PyQt5 import QtGui
# The main modules for Qt are QtWidgets, QtGui and QtCore.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import sys,time



global driver #this is a messy way to do this but whatever

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() #ALWAYS USE THIS

        self.setWindowTitle("My App")
        self.setMinimumSize(700,400) # minimum ekran boyutları


        """
        self.button = QPushButton("Press Me!")

        self.bvalue = False
        self.button.setCheckable(True)
        self.button.clicked.connect(self.button_clicked)
        self.button.clicked.connect(self.button_toggled)
        # Set the central widget of the Window.
        self.setCentralWidget(self.button)
        """
        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)


        self.input.setAlignment(Qt.AlignHCenter)
        self.label.setAlignment(Qt.AlignHCenter)
        

        self.checkbox = QCheckBox()
        self.checkbox.setCheckState(Qt.PartiallyChecked)
        self.checkbox.stateChanged.connect(self.show_state)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)
        layout.addWidget(self.checkbox)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def show_state(self,e):
        print(e)
    
    def setText(self,inp):
        self.label.text = inp

    # uygulama kapatıldığında çağrılacak fonksiyonu değiştirme
    def closeEvent(self, event):
        self.tdriver.close() #tarayıcıyı kapatmak
        self.obj.running = False
        event.accept() #buna ignore dersek daha üst node'a gidip bunu kabul edebilir misin diye soruyor 
        # bu yüzden ignore dersen uygulamayı kapatamıyorsunxx accept uygulamayı kapatabilmeni sağlıyor

    # Bu uygulamanın içine sağ tık yaptığında 3 tane seçenek çıkmasını sağlıyor
    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(e.globalPos()) 

    def uh_oh(self):
        print("uh oh bad stuff happened, this is called from the main app")
    
    """
    def button_clicked(self):
        print("clicked")
    def button_toggled(self,checked): #neden bilmiyorum ama pyqt bunun toggle old. anlayabiliyor
        self.bvalue = checked
        self.button.setEnabled(False)
        print("but is",checked)
    """


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)
# app.setWindowIcon(QtGui.QIcon('hand.ico'))
# icon için özel .ico dosyası lazım


# Create a Qt widget, which will be our window.
window = MainWindow() #QMainWindow()   #QWidget()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.
# bunu acil durum olduğunda arkaplandan hemen ekranın önüne getirmek için kullanabiliriz

# Subclassing QObject and using moveToThread
# http://blog.qt.digia.com/blog/2007/07/05/qthreads-no-longer-abstract
class SomeObject(QObject):
    finished = pyqtSignal() # if I understood correctly we create our own QOebject like a widget and we control what thing is emitted
    twin = window #for some reason this works and if I try to use def __init__ with super()__init__() it just doesnt work so yeah...

    PATH = "chromedriver.exe"

    website_url = "http://www.koeri.boun.edu.tr/scripts/lst2.asp"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(website_url)

    running = True

    def long_running(self):
        count = 0
        while self.running:
            time.sleep(5)
            try:
                driver.refresh()
            except:
                self.running = False
                break

            element = driver.find_element(By.CSS_SELECTOR, "pre") #<pre> ismine sahip olan şeyi buluyo

            formatted_text = element.text
            lines = formatted_text.splitlines(True) #False \n olmasın, True \n olsun anlamında
            

            print(lines[20])
            
            count += 1
        self.send_something_to_gui()
        print("broke someobject's thread")
        self.finished.emit()
    def send_something_to_gui(self):
        print("whyy")
        self.twin.uh_oh()


objThread = QThread()
obj = SomeObject()
obj.moveToThread(objThread)
obj.finished.connect(objThread.quit)
objThread.started.connect(obj.long_running)
# objThread.finished.connect(app.exit) # bence bu çalışmamalı ama emin değiim  #edit: evet çalışmamalı bu

window.tdriver = obj.driver
window.obj = obj

objThread.start()

# Start the event loop.
app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.
print("ended application")