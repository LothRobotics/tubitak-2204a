from PyQt5.QtCore import Qt,QThread,QObject,pyqtSignal,QRect
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QPushButton,QLabel, QLineEdit, QVBoxLayout,QMenu,QAction,QCheckBox
from PyQt5.QtGui import QFont
import sys,time

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self,parent):
        super().__init__() #ALWAYS USE THIS
        self.parent = parent

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
        layout.addWidget(self.enterbutton)

        #self.checkbox = QCheckBox()
        #self.checkbox.setCheckState(Qt.PartiallyChecked)
        #self.checkbox.stateChanged.connect(self.show_state)
        #layout.addWidget(self.checkbox)
        
        self.label3 = QLabel("Lorem Ipsum Dolor Amet \n Lorem Ipsum Dolor Amet")
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

    def show_state(self,e):
        print(e)
    
    def setText(self,inp):
        self.label1.text = inp

    # uygulama kapatıldığında çağrılacak fonksiyonu değiştirme
    def closeEvent(self, event):
        self.parent.code_thread.running = False
        self.parent.code_thread.finished.emit()
        print("ended code_thread")
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

# Subclassing QObject and using moveToThread
# http://blog.qt.digia.com/blog/2007/07/05/qthreads-no-longer-abstract
class SomeObject(QObject):
    finished = pyqtSignal() # if I understood correctly we create our own QOebject like a widget and we control what thing is emitted
    
    PATH = "chromedriver.exe"

    website_url = "http://www.koeri.boun.edu.tr/scripts/lst2.asp"

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver.get(website_url)

    running = True

    def long_running(self):
        while self.running:
            time.sleep(1)
            print("running")
            #try:
            #    driver.refresh()
            #except:
            #    self.running = False
            #    break

            #element = driver.find_element(By.CSS_SELECTOR, "pre") #<pre> ismine sahip olan şeyi buluyo

            #formatted_text = element.text
            #lines = formatted_text.splitlines(True) #False \n olmasın, True \n olsun anlamında
            

            #print(lines[20])
        self.send_something_to_gui()
        print("broke someobject's thread")
        self.finished.emit()
    def send_something_to_gui(self):
        print("whyy")
        self.twin.uh_oh()


class APP:
    def __init__(self) -> None:
        self.windowmanager = MainWindow(self)
        self.windowmanager.show() # bunu acil durum olduğunda arkaplandan hemen ekranın önüne getirmek için kullanabiliriz
        self.code_thread = SomeObject()
        self.obj_thread = QThread()
        self.code_thread.moveToThread(self.obj_thread)
        self.code_thread.finished.connect(self.obj_thread.quit)
        self.obj_thread.started.connect(self.code_thread.long_running)
        # objThread.finished.connect(app.exit) # bence bu çalışmamalı ama emin değiim  #edit: evet çalışmamalı bu


if __name__ == '__main__':
    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    qapp = QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon('hand.ico'))
    # icon için özel .ico dosyası lazım

    app = APP()
    app.obj_thread.start()

    # Start the event loop.
    qapp.exec()

    # Your application won't reach here until you exit and the event
    # loop has stopped.
    print("ended application")