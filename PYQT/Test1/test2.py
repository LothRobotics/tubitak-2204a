from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QPushButton,QLabel, QLineEdit, QVBoxLayout
# The main modules for Qt are QtWidgets, QtGui and QtCore.


import sys


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() #ALWAYS USE THIS

        self.setWindowTitle("My App")
        self.setMinimumSize(700,400) # minimum ekran boyutları
        
        self.button = QPushButton("Press Me!")

        self.bvalue = False
        self.button.setCheckable(True)
        self.button.clicked.connect(self.button_clicked)
        self.button.clicked.connect(self.button_toggled)
        

        # Set the central widget of the Window.
        self.setCentralWidget(self.button)
    
    def button_clicked(self):
        print("clicked")
    def button_toggled(self,checked): #neden bilmiyorum ama pyqt bunun toggle old. anlayabiliyor
        self.bvalue = checked
        self.button.setEnabled(False)
        print("but is",checked)



# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow() #QMainWindow()   #QWidget()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.
# bunu acil durum olduğunda arkaplandan hemen ekranın önüne getirmek için kullanabiliriz



# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.
print("ended application")