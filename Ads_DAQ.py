#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Advantech DAQ Thread'''

__author__ = 'baixue'


from PyQt4 import QtCore
from Adsapi import *


class DAQ_Task(QtCore.QThread):
    signal_DAQ = QtCore.pyqtSignal(list)
    def __init__(self, parent=None):
        super(DAQ_Task, self).__init__(parent)
        self.DriverHandle = 0
        self.usINTBuf = None # int buffer
        self.pUserBuf = None # user buffer
        self.count = 200
        self.working = False
        #signalName = QtCore.pyqtSignal()

    def __del__(self):
        self.working = False

    def start(self, DeviceNum=0, sampleRate=1000, startChan=0, numChans=2, gains=None, count=200):
        self.count = count
        try:
            # Open device
            self.DriverHandle = DRV_DeviceOpen(DeviceNum)
            # Enable event
            DRV_EnableEvent(self.DriverHandle, EventType=0xf, Enabled=1, Count=512)
        except Ads_Error, e:
            self.quit()
        else:
            # Allocate INT & data buffer for interrupt transfer
            self.usINTBuf, self.pUserBuf = AllocateDataBuffer(count)
            # Start interrupt transfer
            DRV_FAIIntScanStart(self.DriverHandle, sampleRate, numChans, startChan, count, self.usINTBuf, gains, cyclic=1)
            self.working = False
            super(DAQ_Task, self).start()

    def run(self):
        while True:
            FAIEvent = WaitFAIEvent(self.DriverHandle, timeout=3000)
            AI_Terminated = FAIEvent[0]
            if AI_Terminated == True:break
            AI_BufferHalfReady = FAIEvent[1]
            AI_BufferFullReady = FAIEvent[2]
            if AI_BufferHalfReady | AI_BufferFullReady:
                overRun = DRV_FAITransfer(self.DriverHandle, self.pUserBuf, self.count)
            if overRun != 0:
                DRV_ClearOverrun(self.DriverHandle)
                data = GetBufferData(self.pUserBuf, self.count)
                data = SplitArray1DTo2D(data, 2)
                # emit signal
                signal_DAQ.emit(data)

    def terminate(self):
        DRV_FAITerminate(self.DriverHandle)
        # Stop A/D conversion for high speed
        DRV_FAIStop(self.DriverHandle)
        # Close device
        DRV_DeviceClose(self.DriverHandle)
        super(DAQ_Task, self).terminate()

    def stop(self):
        DRV_FAITerminate(self.DriverHandle)
        # Stop A/D conversion for high speed
        DRV_FAIStop(self.DriverHandle)
        # Close device
        DRV_DeviceClose(self.DriverHandle)
        self.wait()


if __name__ == "__main__":
    pass
