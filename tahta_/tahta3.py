from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont,QPainter,QPen,QImage,qRgba,QPixmap,QColor,QPicture
# The main modules for Qt are QtWidgets, QtGui and QtCore.

import sys,time
qapp = QApplication(sys.argv)



pi = QPicture()
painter = QPainter(pi)


painter.setPen(QPen(Qt.black, 12, Qt.SolidLine, Qt.RoundCap))
painter.drawLine(0, 0, 200, 200)
painter.end()


l = QLabel()
l.setPicture(pi);
l.show();




qapp.exec()

