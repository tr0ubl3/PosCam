#!/usr/bin/env python

#------------------------------------------------------------------------------
#                 PyuEye example - gui application modul
#
# Copyright (c) 2017 by IDS Imaging Development Systems GmbH.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#------------------------------------------------------------------------------

from PyQt4 import QtCore
from PyQt4 import QtGui
#from PyQt5.QtWidgets import QGraphicsScene, QApplication
#from PyQt5.QtWidgets import QGraphicsView
#from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSlider, QWidget

from pyueye import ueye
#from PyQt4.QtGui import QPixmap

import math
import os


def get_qt_format(ueye_color_format):
    return { ueye.IS_CM_SENSOR_RAW8: QtGui.QImage.Format_Mono,
             ueye.IS_CM_MONO8: QtGui.QImage.Format_Mono,
             ueye.IS_CM_RGB8_PACKED: QtGui.QImage.Format_RGB888,
             ueye.IS_CM_BGR8_PACKED: QtGui.QImage.Format_RGB888,
             ueye.IS_CM_RGBA8_PACKED: QtGui.QImage.Format_RGB32,
             ueye.IS_CM_BGRA8_PACKED: QtGui.QImage.Format_RGB32
    } [ueye_color_format]


class PyuEyeQtView(QtGui.QWidget):

    update_signal = QtCore.pyqtSignal(QtGui.QImage, name="update_signal")

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.image = None

        self.graphics_view = QtGui.QGraphicsView(self)
        self.v_layout = QtGui.QVBoxLayout(self)
        self.h_layout = QtGui.QHBoxLayout()

        self.scene = QtGui.QGraphicsScene(self.graphics_view)
        self.graphics_view.setScene(self.scene)
        self.v_layout.addWidget(self.graphics_view)

        self.scene.drawBackground = self.draw_background
        self.scene.drawForeground = self.draw_foreground
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.update_signal.connect(self.update_image)

        self.processors = []
        self.resize(800, 580)

        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

        self.x_move = 0
        self.y_move = 0
        self.x_move_1 = 0
        self.y_move_2 = 0
        self.x_spacer = 250
        self.x_min = 10
        self.electrod = 200 #in microni
        self.x_calibration = 500
        self.increment = 1800.0

    def on_update_canny_1_slider(self, value):
        pass # print(value)

    def on_update_canny_2_slider(self, value):
        pass # print(value)

    def draw_background(self, painter, rect):
        if self.image:
            image = self.image.scaled(rect.width(), rect.height(), QtCore.Qt.KeepAspectRatioByExpanding)
            painter.drawImage(rect.x(), rect.y(), image)

    def draw_foreground(self, painter, rect):
        color = QtGui.QColor(255, 0, 0)
        pen = QtGui.QPen(color, 3)
        pen.setStyle(QtCore.Qt.DashLine)
        painter.setPen(pen)
        # linie orizontala
        #print(self.rect().height() / 2 + self.y_move)
        painter.drawLine(-self.rect().width(), 0 + self.y_move, self.rect().width()/2, 0 + self.y_move)

        # linie verticala stanga
        color = QtGui.QColor(0, 0, 255)
        pen = QtGui.QPen(color, 3)
        pen.setStyle(QtCore.Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(self.x_move - self.x_spacer, -self.rect().height(), self.x_move - self.x_spacer, self.rect().height())

        # linie verticala dreapta
        color = QtGui.QColor(0, 0, 255)
        pen = QtGui.QPen(color, 3)
        pen.setStyle(QtCore.Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(self.x_move_1 + self.x_spacer, -self.rect().height() / 2, self.x_move_1 + self.x_spacer, self.rect().height())

        # afisare distanta intre liniile verticale
        painter.setPen(QtGui.QColor(125, 125, 125))
        painter.setFont(QtGui.QFont('Consolas', 30))
        val_afisata = (self.electrod * (self.x_move_1 - self.x_move + 2 * self.x_spacer)) / self.x_calibration #(self.rect().width() / 2 + self.x_move_1 + self.x_spacer) - (self.rect().width() / 2 + self.x_move - self.x_spacer)
        #print(lol)
        painter.drawText((-self.rect().width() / 2) + 30 , (-self.rect().height() / 2) + 50, u'\u00D8' + ' ' + str(val_afisata) + ' ' + u'\u03BCm')

        # afisare calcul unghi
        cateta_opusa = (val_afisata - self.electrod) / 2
        if cateta_opusa == 0:
           unghi_teta = 0
           inclinatie = 0
        else:
            unghi_teta = math.degrees(math.atan(self.increment / cateta_opusa))
            inclinatie = (1000 / math.tan(math.radians(unghi_teta)))
        # print(((1000 * self.x_calibration)/self.electrod))

        painter.drawText((-self.rect().width() / 2) + 30, (-self.rect().height() / 2) + 100, 'Inclinatie ' + str(round(inclinatie, 2)) + ' ' + u'\u03BCm' + '/mm')

    def update_image(self, image):
        self.scene.update()

    def user_callback(self, image_data):
        return image_data

    def handle(self, image_data):
        self.image = self.user_callback(self, image_data)

        self.update_signal.emit(self.image)

        # unlock the buffer so we can use it again
        image_data.unlock()

    def shutdown(self):
        self.close()

    def add_processor(self, callback):
        self.processors.append(callback)

    def keyReleaseEvent(self, e):
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
        if QtGui.QKeySequence(m + k) == QtGui.QKeySequence('Ctrl+R'):
            os.system("reboot")
        if QtGui.QKeySequence(m + k) == QtGui.QKeySequence('Ctrl+Q'):
            os.system("shutdown now -h")
        self.scene.update()

    def showDialogCalibration(self):
        text, result = QtGui.QInputDialog.getText(self, 'Calibrare camera ', 'Introdu diametrul electrodului:')
        if result == True:
            self.electrod = int(text)
            self.x_calibration = self.x_move_1 - self.x_move + 2 * self.x_spacer

    def showDialogIncrement(self):
        text, result = QtGui.QInputDialog.getText(self, 'Increment ', 'Introdu incrementul in mm:')
        if result == True:
            self.increment = float(text) * 1000

class PyuEyeQtApp:
    def __init__(self, args=[]):
        self.qt_app = QtGui.QApplication(args)

    def exec_(self):
        self.qt_app.exec_()

    def exit_connect(self, method):
        self.qt_app.aboutToQuit.connect(method)