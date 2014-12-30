#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'baixue'

'''QwtChart'''

from PyQt4 import QtCore, QtGui, Qt
import PyQt4.Qwt5 as Qwt
import numpy as np

colors = (Qt.Qt.black,
          Qt.Qt.blue,
          Qt.Qt.cyan,
          Qt.Qt.darkBlue,
          Qt.Qt.darkCyan,
          Qt.Qt.darkGray,
          Qt.Qt.darkGreen,
          Qt.Qt.darkMagenta,
          Qt.Qt.darkRed,
          Qt.Qt.darkYellow,
          Qt.Qt.gray,
          Qt.Qt.green,
          Qt.Qt.lightGray,
          Qt.Qt.magenta,
          Qt.Qt.red,
          Qt.Qt.white,
          Qt.Qt.yellow)


class QwtChart(Qwt.QwtPlot):
    def __init__(self, *args):
        super(QwtChart, self).__init__(*args)
        # set title
        self.setTitle(u'<h4><font color=red>图表</font></h4>')
        # bgcolor
        self.setCanvasBackground(Qt.Qt.white)
        # legend
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.RightLegend)

        # a variation on the C++ example
        self.plotLayout().setAlignCanvasToScales(True)

        # grid
        grid = Qwt.QwtPlotGrid()
        grid.setPen(QtGui.QPen(Qt.Qt.gray, 0, Qt.Qt.DotLine))
        grid.attach(self)

        # set axis titles
        self.setAxisTitle(Qwt.QwtPlot.xBottom, u'X')
        self.setAxisTitle(Qwt.QwtPlot.yLeft, u'Amplitude')
        
        # set Scale Range
        self.setAxisScale(Qwt.QwtPlot.xBottom, 0.0, 1000.0)
        self.setAxisScale(Qwt.QwtPlot.yLeft, -10.0, 10.0)

        # picker
        self.picker = Qwt.QwtPlotPicker(
            Qwt.QwtPlot.xBottom,
            Qwt.QwtPlot.yLeft,
            Qwt.QwtPicker.PointSelection | Qwt.QwtPicker.DragSelection,
            Qwt.QwtPlotPicker.CrossRubberBand,
            Qwt.QwtPicker.AlwaysOn,
            self.canvas())
        self.picker.setRubberBandPen(QtGui.QPen(Qt.Qt.red))
        self.picker.setTrackerPen(QtGui.QPen(Qt.Qt.red))

        self.connect(self.picker,
                     QtCore.SIGNAL('moved(const QPoint &)'),
                     self.moved)

        # insert a horizontal marker at y = 0
        mY = Qwt.QwtPlotMarker()
        mY.setLabel(Qwt.QwtText('y = 0'))
        mY.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
        mY.setLineStyle(Qwt.QwtPlotMarker.HLine)
        mY.setLinePen(Qt.QPen(Qt.Qt.cyan, 1, Qt.Qt.DashDotLine))
        mY.setYValue(0.0)
        mY.attach(self)

        # insert a vertical marker at x = 500
        mX = Qwt.QwtPlotMarker()
        mX.setLabel(Qwt.QwtText('x = 500'))
        mX.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
        mX.setLineStyle(Qwt.QwtPlotMarker.VLine)
        mX.setLinePen(QtGui.QPen(Qt.Qt.cyan, 1, Qt.Qt.DashDotLine))
        mX.setXValue(500)
        mX.attach(self)

        #Initialize data
        self.curves = []
        self.dataLength = 1000
        self.x = np.arange(0.0, 1001.0, 1.0)

    def addCurve(curveName):
        #insert one curve
        curve = Qwt.QwtPlotCurve(u'%s' % curveName)
        curve.setPen(QtGui.QPen(colors[len(self.curves)-1], 2.0))
        curve.attach(self)
        curve.setData(np.array([0], np.float))
        self.curves.append(curveName, curve)

    def setData(self, data):
        for i, curve in enumerate(self.curves):
            curve[1].setData(data[i])
        self.replot()

    def appendData(self, data):
        for i, curve in enumerate(self.curves):
            curveData = np.concatenate((curve.data(), data[i]), 1)
            curveData = curveData[len(curveData)-self.dataLength:] if len(curveData)>self.dataLength else curveData
            curve.setData(self.x, curveData)
        self.replot()

    def clear(self):
        zero = np.array([0], np.float)
        for curve in self.curves:
            curve[1].setData(zero)
        self.replot()

    # moved()
    def moved(self, point):
        info = "Freq=%g, Ampl=%g" % (
            self.invTransform(Qwt.QwtPlot.xBottom, point.x()),
            self.invTransform(Qwt.QwtPlot.yLeft, point.y()))
    


if __name__ == "__main__":
    pass
