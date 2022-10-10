import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

RUN_PATH = "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"

class MainWidget(QWidget):

    def __init__(self,parent=None):
        super(MainWidget, self).__init__(parent)
        self.settings = QSettings(RUN_PATH, QSettings.NativeFormat)
        self.setupUi()       
        # Check if value exists in registry
        self.checkbox.setChecked(self.settings.contains("MainWidget"))

    def setupUi(self):
        self.checkbox = QCheckBox("Boot at Startup", self)
        button = QPushButton("Close", self)
        button.clicked.connect(self.close)
        layout = QVBoxLayout(self)
        layout.addWidget(self.checkbox)
        layout.addWidget(button)

    def closeEvent(self, event):
        if self.checkbox.isChecked():
            self.settings.setValue("MainWidget",sys.argv[0]);
        else:
            self.settings.remove("MainWidget");
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWidget()
    w.show()
    app.exec_()