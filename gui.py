import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Mentor")
        self.setWindowIcon(QtGui.QIcon('ids.png'))
        self.home()
        self.x_move = 0
        self.y_move = 0

    def home(self):

        self.showFullScreen()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap("1.jpg")
        painter.drawPixmap(self.rect(), pixmap)
        color = QtGui.QColor(255, 0, 0)
        pen = QtGui.QPen(color, 3)
        pen.setStyle(QtCore.Qt.DashDotLine)
        painter.setPen(pen)
        # linie orizontala
        painter.drawLine(0, self.rect().height() / 2 + self.y_move, self.rect().width(), self.rect().height() / 2 + self.y_move)

        # linie verticala
        color = QtGui.QColor(0, 0, 255)
        pen = QtGui.QPen(color, 3)
        pen.setStyle(QtCore.Qt.DashDotLine)
        painter.setPen(pen)
        painter.drawLine(self.rect().width() / 2 + self.x_move, 0, self.rect().width() / 2 + self.x_move, self.rect().height())

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Right:
            self.x_move += 10
            #print(self.x_move)
        if e.key() == QtCore.Qt.Key_Left:
            self.x_move -= 10
            #print(self.x_move)
        if e.key() == QtCore.Qt.Key_Up:
            self.y_move -= 10
            #print(self.y_move)
        if e.key() == QtCore.Qt.Key_Down:
            self.y_move += 10
            #print(self.y_move)
        self.update()


    def close_application(self):
        print("custom")
        sys.exit()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()