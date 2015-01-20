#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'baixue'

'''
多线程
'''

import math
from PyQt4 import QtCore, QtGui, Qt
import PyQt4.Qwt5 as Qwt
import numpy as np
from Ads_DAQ import DAQ_Task


class Chart(Qwt.QwtPlot):
    def __init__(self, *args):
        super(Chart, self).__init__(*args)
        #set title
        self.setTitle(u'<h4><font color=red>图表</font></h4>')
        #背景色
        self.setCanvasBackground(Qt.Qt.white)
        #插入图例--曲线名
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.RightLegend)

        # a variation on the C++ example
        self.plotLayout().setAlignCanvasToScales(True)
        
        #创建网格
        grid = Qwt.QwtPlotGrid()
        grid.setPen(Qt.QPen(Qt.Qt.gray, 0, Qt.Qt.DotLine))
        grid.attach(self)
        
        # set axis titles
        self.setAxisTitle(Qwt.QwtPlot.xBottom, u'Time(s)')
        self.setAxisTitle(Qwt.QwtPlot.yLeft, u'Values')
        
        # set Scale Range
        self.setAxisScale(Qwt.QwtPlot.xBottom, 0.0, 200.0)
        self.setAxisScale(Qwt.QwtPlot.yLeft, -10.0, 10.0)

        # insert a few curves
        self.curveA = Qwt.QwtPlotCurve(u'curveA')
        self.curveA.setPen(Qt.QPen(Qt.Qt.red))
        self.curveA.setStyle(Qwt.QwtPlotCurve.Lines)
        self.curveA.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.Ellipse,
                                            Qt.Qt.yellow,
                                            QtGui.QPen(Qt.Qt.blue),
                                            Qt.QSize(5, 5) ))
        self.curveA.attach(self)

        self.curveB = Qwt.QwtPlotCurve(u'curveB')
        self.curveB.setPen(Qt.QPen(Qt.Qt.blue))
        self.curveB.attach(self)

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
        mX.setXValue(100)
        mX.setLinePen(Qt.QPen(Qt.Qt.green, 1, Qt.Qt.DashDotLine))
        mX.attach(self)

        #Initialize data
        self.x = np.arange(0.0, 201.0, 1.0)
        self.curveAData = np.array([0.0], dtype=np.float)
        self.curveBData = np.array([0.0], dtype=np.float)


    def setData(self, AData, BData):
        self.curveA.setData(self.x, AData)
        self.curveB.setData(self.x, BData)
        self.replot()

    def appendData(self, AData, BData):
        if not type(AData) == 'list':
            AData = np.array([AData], dtype=np.float)
        if not type(BData) == 'list':
            BData = np.array([BData], dtype=np.float)
        self.curveAData = np.concatenate((self.curveAData if len(self.curveAData)<=200 else self.curveAData[len(AData):], AData), 1)
        self.curveBData = np.concatenate((self.curveBData if len(self.curveBData)<=200 else self.curveBData[len(BData):], BData), 1)
        self.curveA.setData(self.x, self.curveAData)
        self.curveB.setData(self.x, self.curveBData)
        self.replot()

    def clear(self):
        self.curveAData = np.array([0.0], dtype=np.float)
        self.curveBData = np.array([0.0], dtype=np.float)
        self.curveA.setData(self.x, self.curveAData)
        self.curveB.setData(self.x, self.curveBData)
        self.replot()


class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(Qt.QIcon(":/images/images/logo.png"))
        # self.setWindowOpacity(1.0) # 透明度
        self.setMinimumSize(800,600)
        
        self.chart = Chart()
        self.btn_start = QtGui.QPushButton('start')
        self.btn_stop = QtGui.QPushButton('stop')
        self.btn_clear = QtGui.QPushButton('clear')

        self.btn_start.clicked.connect(self.start)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_clear.clicked.connect(self.chart.clear)

        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.btn_start)
        self.layout.addWidget(self.btn_stop)
        self.layout.addWidget(self.btn_clear)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.chart)
        mainLayout.addLayout(self.layout)

        self.setLayout(mainLayout)

        self.task_DAQ = DAQ_Task()
        self.task_DAQ.signal_DAQ.connect(self.update_chart)

    def update_chart(self, data):
        self.chart.appendData(data[0], data[1])

    def start(self):
        if self.task_DAQ.isRunning():
            return
        self.task_DAQ.start(DeviceNum=0, startChan=0, numChan=2, gains=(4,4))

    def stop(self):
        if self.task_DAQ.isRunning():
            self.task_DAQ.terminate()
            self.task_DAQ.wait()
        
    def closeEvent(self, event):
        self.task_DAQ.stop()
        self.close()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())






