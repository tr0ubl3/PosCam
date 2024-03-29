import sys
from PyQt4 import QtGui, QtCore
import math

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Mentor")
        self.setWindowIcon(QtGui.QIcon('ids.png'))
        self.home()
        self.x_move = 0
        self.y_move = 0
        self.x_move_1 = 0
        self.y_move_2 = 0
        self.x_spacer = 250
        self.x_min = 10
        self.electrod = 100 #in microni
        self.x_calibration = 100
        self.increment = 1800.0

    def home(self):

        self.showFullScreen()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap("1.jpg")
        painter.drawPixmap(self.rect(), pixmap)
        color = QtGui.QColor(255, 0, 0)
        pen = QtGui.QPen(color, 3)
        pen.setStyle(QtCore.Qt.DashLine)
        painter.setPen(pen)
        # linie orizontala
        painter.drawLine(0, self.rect().height() / 2 + self.y_move, self.rect().width(), self.rect().height() / 2 + self.y_move)

        # linie verticala stanga
        color = QtGui.QColor(0, 0, 255)
        pen = QtGui.QPen(color, 3)
        pen.setStyle(QtCore.Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(self.rect().width() / 2 + self.x_move - self.x_spacer, 0, self.rect().width() / 2 + self.x_move - self.x_spacer, self.rect().height())

        # linie verticala dreapta
        color = QtGui.QColor(0, 0, 255)
        pen = QtGui.QPen(color, 3)
        pen.setStyle(QtCore.Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(self.rect().width() / 2 + self.x_move_1 + self.x_spacer, 0, self.rect().width() / 2 + self.x_move_1 + self.x_spacer, self.rect().height())

        # afisare distanta intre liniile verticale
        painter.setPen(QtGui.QColor(125, 125, 125))
        painter.setFont(QtGui.QFont('Consolas', 30))
        val_afisata = (self.electrod * (self.x_move_1 - self.x_move + 2 * self.x_spacer)) / self.x_calibration #(self.rect().width() / 2 + self.x_move_1 + self.x_spacer) - (self.rect().width() / 2 + self.x_move - self.x_spacer)
        #print(lol)
        painter.drawText(50, 100, u'\u00D8' + ' ' + str(val_afisata) + ' ' + u'\u03BCm')

        # afisare calcul unghi
        unghi_teta = math.degrees(math.atan(self.increment/(val_afisata / 2)))
        painter.drawText(50, 150, u'\u2221' + ' ' + str(round(90 - unghi_teta, 2)) + u'\u00B0' + ', increment de ' + str(self.increment/1000) + ' mm')

    def keyPressEvent(self, e):
        k = e.key()
        m = int(e.modifiers())

        if QtGui.QKeySequence(m + k) == QtGui.QKeySequence('Right'):
            self.x_move += 10
        if QtGui.QKeySequence(m + k) == QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Right):
            self.x_move += 1
            #print(self.x_move)
        if QtGui.QKeySequence(m + k) == QtGui.QKeySequence('Left'):
            self.x_move -= 10
            #print(self.x_move)
        if QtGui.QKeySequence(m + k) == QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Left):
            self.x_move -= 1
        if e.key() == QtCore.Qt.Key_Up:
            self.y_move -= 10
            #print(self.y_move)
        if e.key() == QtCore.Qt.Key_Down:
            self.y_move += 10
            #print(self.y_move)
        if QtGui.QKeySequence(m + k) == QtGui.QKeySequence('Ctrl+Right'):
            self.x_move_1 += 10
        if QtGui.QKeySequence(m + k) == QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_Right):
            self.x_move_1 += 1
        if QtGui.QKeySequence(m + k) == QtGui.QKeySequence('Ctrl+Left'):
            self.x_move_1 -= 10
        if QtGui.QKeySequence(m + k) == QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_Left):
            self.x_move_1 -= 1
        if QtGui.QKeySequence(m + k) == QtGui.QKeySequence('Ctrl+N'):
            self.x_move = 0
            self.y_move = 0
            self.x_move_1 = 0
            self.y_move_2 = 0
            self.x_calibration = 100
        if e.key() == QtCore.Qt.Key_C:
            self.showDialogCalibration()
        if e.key() == QtCore.Qt.Key_I:
            self.showDialogIncrement()
        self.update()

    def showDialogCalibration(self):
        text, result = QtGui.QInputDialog.getText(self, 'Calibrare camera ', 'Introdu diametrul electrodului:')
        if result == True:
            self.electrod = int(text)
            self.x_calibration = self.x_move_1 - self.x_move + 2 * self.x_spacer

    def showDialogIncrement(self):
        text, result = QtGui.QInputDialog.getText(self, 'Increment ', 'Introdu incrementul in mm:')
        if result == True:
            self.increment = float(text) * 1000

    def close_application(self):
        #print("custom")
        sys.exit()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()