#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Advantech DAQ Thread'''

__author__ = 'baixue'


from PyQt4 import QtCore
from Adsapi import *


class DAQ_Task( QtCore.QThread):
    signal_DAQ = QtCore.pyqtSignal(list)
    def __init__(self, parent=None):
        #QThread.__init__(self, parent)
        super(DAQ_Task, self).__init__(self, parent)
        self.DriverHandle = 0
        self.working = False

    def __del__(self):
        self.working = False
        self.wait()

    def start(self, DeviceNum=0, startChan=0, numChan=2, gains=None):
        self.startChan = startChan
        self.numChan = numChan
        self.gains = gains
        try:
            # Open device
            self.DriverHandle = DRV_DeviceOpen(DeviceNum)
            DRV_MAIConfig(self.DriverHandle, numChan, startChan, gains)
        except Ads_Error, e:
            self.quit()
        else:
            self.working = True

    def run(self):
        while self.working:
            values = DRV_MAIVoltageIn(self.DriverHandle, self.numChan, self.startChan, self.gains)
            # emit signal
            signal_DAQ.emit(values)
            self.msleep(100)

    def terminate(self):
        # Close device
        DRV_DeviceClose(self.DriverHandle)

    def stop(self):
        self.working = False


if __name__ == "__main__":
    pass
