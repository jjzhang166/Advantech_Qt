#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'baixue'

'''
单线程
'''

import math
from PyQt4 import QtCore, QtGui, Qt
import PyQt4.Qwt5 as Qwt
import numpy as np
from Adsapi import *


class Chart(Qwt.QwtPlot):
    def __init__(self, *args):
        super(Chart, self).__init__(*args)
        # set title
        self.setTitle(u'<h4><font color=red>图表</font></h4>')
        # 背景色
        self.setCanvasBackground(Qt.Qt.white)
        # 插入图例--曲线名
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.RightLegend)

        # a variation on the C++ example
        self.plotLayout().setAlignCanvasToScales(True)
        
        # 创建网格
        grid = Qwt.QwtPlotGrid()
        grid.attach(self)
        grid.setPen(Qt.QPen(Qt.Qt.gray, 0, Qt.Qt.DotLine))
        
        # set axis titles
        self.setAxisTitle(Qwt.QwtPlot.xBottom, u'Time(s)')
        self.setAxisTitle(Qwt.QwtPlot.yLeft, u'Values')
        
        # set Scale Range
        self.setAxisScale(Qwt.QwtPlot.xBottom, 0.0, 10000.0)
        self.setAxisScale(Qwt.QwtPlot.yLeft, -10.0, 10.0)

        # insert a few curves
        self.curve = Qwt.QwtPlotCurve(u'curveA')
        self.curve.setPen(Qt.QPen(Qt.Qt.red))
        self.curve.attach(self)

        # insert a horizontal marker at y = xxx
        mY = Qwt.QwtPlotMarker()
        mY.setLabel(Qwt.QwtText('Maker:Y'))
        mY.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
        mY.setLineStyle(Qwt.QwtPlotMarker.HLine)
        mY.setYValue(0.0)
        mY.setLinePen(Qt.QPen(Qt.Qt.green, 1, Qt.Qt.DashDotLine))
        mY.attach(self)

        # insert a vertical marker
        mX = Qwt.QwtPlotMarker()
        mX.setLabel(Qwt.QwtText('Maker:X'))
        mX.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
        mX.setLineStyle(Qwt.QwtPlotMarker.VLine)
        mX.setXValue(5000)
        mX.setLinePen(Qt.QPen(Qt.Qt.green, 1, Qt.Qt.DashDotLine))
        mX.attach(self)

        # Initialize data
        self.x = np.arange(0.0, 10001.0, 1.0)
        self.curveAData = np.zeros(len(self.x), np.float)

    def setData(self, AData):
        self.curve.setData(self.x, AData)
        self.replot()

    def appendData(self, AData):
        self.curveAData = np.concatenate((self.curveAData[len(AData):], AData), 1)
        self.curveA.setData(self.x, self.curveAData)
        self.replot()

    def clear(self):
        self.curveA.setData(self.x, [])
        self.replot()

    
class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(Qt.QIcon(":/images/images/logo.png"))
        self.setWindowOpacity(1.0)
        self.setMinimumSize(800,600)
        
        self.chart = Chart()
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

        self.isActive = False

    def start(self):
        deviceNum = 0
        self.count = 100
        # Open device
        self.DriverHandle = DRV_DeviceOpen(deviceNum)
        # Allocate INT & data buffer for interrupt transfer
        self.usINTBuf, self.pUserBuf = AllocateDataBuffer(self.count)
        # Start interrupt transfer
        DRV_FAIIntStart(self.DriverHandle, 1000, 0, 4, self.count, self.usINTBuf, TrigSrc=0, cyclic=1, IntrCount=1)

        self.timerId = self.startTimer(10)
        self.isActive = True

    def acquise(self):
        FAICheck = DRV_FAICheck(self.DriverHandle)
        stopped = FAICheck[1]
        if stopped == 1:self.stop()
        halfReady = FAICheck[4]
        if halfReady == 0:
            return None
        else:
            # Get data from driver
            overrun = DRV_FAITransfer(self.DriverHandle, self.pUserBuf, self.count)
            data = GetBufferData(self.pUserBuf, self.count)
        return data

    def stop(self):
        if self.isActive == True:
            DRV_FAIStop(self.DriverHandle)
            self.killTimer(self.timerId)
            self.active = False
        
    def timerEvent(self, e):
        data = self.acquise()
        if data == None:
            return None
        else:
            self.chart.append(data)
        
    def closeEvent(self, event):
        self.stop()
        self.close()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())






