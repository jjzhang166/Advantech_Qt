#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'baixue'

'''
test
'''

from PyQt4 import QtCore, QtGui, Qt
import PyQt4.Qwt5 as Qwt
import numpy as np
from qwtchart import *


class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon(":/images/images/logo.png"))
        # self.setWindowOpacity(1.0) # 透明度
        self.setMinimumSize(800,600)
        
        self.chart = QwtChart()
        self.btn_start = QtGui.QPushButton('start')
        self.btn_stop = QtGui.QPushButton('stop')

        self.btn_start.clicked.connect(self.start)
        self.btn_stop.clicked.connect(self.stop)

        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.btn_start)
        self.layout.addWidget(self.btn_stop)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.chart)
        mainLayout.addLayout(self.layout)

        self.setLayout(mainLayout)
        

    def update_chart(self, data):
        self.chart.appendData(data)

    def start(self):
        pass

    def stop(self):
        pass
        
    def closeEvent(self, event):
        self.stop()
        self.close()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())






