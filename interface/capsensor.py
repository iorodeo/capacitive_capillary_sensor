"""
Test GUI for acquiring data from the capillary capacitance sensors. 
"""
import sys
import os
import os.path
import platform
import serial
import time
from PyQt4 import QtGui
from PyQt4 import QtCore
from capsensor_ui import Ui_MainWindow
from sensor_comm import SensorComm
from logger import Logger
from filters import LowpassFilter


DEFAULT_LOG_FILE = 'capsense_data.txt'
TIMER_INTERVAL_MS = 10

class CapSensor(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(CapSensor, self).__init__(parent)
        self.setupUi(self)
        self.connectActions()
        self.setupTimer()
        self.initialize()

    def connectActions(self):
        self.startPushButton.pressed.connect(self.startPressed_Callback)
        self.startPushButton.clicked.connect(self.startClicked_Callback)
        self.stopPushButton.clicked.connect(self.stopClicked_Callback)
        self.filePushButton.clicked.connect(self.fileClicked_Callback)
        self.serialPortEdit.editingFinished.connect(self.serialPortEdit_Callback)

    def setupTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(TIMER_INTERVAL_MS)
        self.timer.timeout.connect(self.timer_Callback)

    def initialize(self):

        # Set default log file
        self.userHome = os.getenv('USERPROFILE')
        if self.userHome is None:
            self.userHome = os.getenv('HOME')
        self.defaultLogPath = os.path.join(self.userHome, DEFAULT_LOG_FILE)
        self.logPath = self.defaultLogPath
        self.logFileLabel.setText('Log File: %s'%(self.logPath))

        # Set last directory
        self.lastDir = self.userHome

        # Set default com port
        osType = platform.system()
        if osType == 'Linux':
            self.port = '/dev/ttyUSB1'
        else:
            self.port = 'com1'
        self.serialPortEdit.setText(self.port)
           
        # Setup list view
        self.horizontalHeaderLabels = ['Sample #', 'Freq (Hz)', 'Value (pF)']
        self.numSensors = 4
        self.tableWidget.setRowCount(self.numSensors)
        self.tableWidget.setColumnCount(len(self.horizontalHeaderLabels))
        self.tableWidget.setHorizontalHeaderLabels(self.horizontalHeaderLabels)
        self.sensorLabels = []
        for i in range(0,self.numSensors):
            self.sensorLabels.append('Sensor %d'%(i,))
        self.tableWidget.setVerticalHeaderLabels(self.sensorLabels)

        # Create table items
        self.tableItem = {}
        for i in range(0,self.numSensors):
            for j in range(0,len(self.horizontalHeaderLabels)):
                    self.tableItem[(i,j)] = QtGui.QTableWidgetItem()
                    self.tableWidget.setItem(i,j,self.tableItem[(i,j)])

        # Set up sensor object
        self.sensor = None
        self.logger = None

        # Setup time information
        self.firstTime = None

        # Setup frequency data
        self.lastSampleTime = {}
        self.freqFilter = {}
        for i in range(0,self.numSensors):
            self.freqFilter[i] = LowpassFilter(fc=1.5)

        # List of widgets to disable during a run
        self.stopEnabledList = ['startPushButton', 'filePushButton', 'serialPortEdit']
        self.stopDisabledList = ['stopPushButton']

        self.runEnabledList = ['stopPushButton',] 
        self.runDisabledList = ['startPushButton', 'filePushButton', 'serialPortEdit']

        self.initDisabledList = ['filePushButton', 'serialPortEdit']

        # Initialize state infromation
        self.running = False
        self.stateLabel.setText('Stopped')
        self.setEnabledForState('Stopped')

    def setEnabledForState(self,state):
        if state.lower() == 'running':
            for name in self.runDisabledList:
                widget = getattr(self,name)
                widget.setEnabled(False)
            for name in self.runEnabledList:
                widget = getattr(self,name)
                widget.setEnabled(True)
        elif state.lower() == 'stopped': 
            for name in self.stopEnabledList:
                widget = getattr(self,name)
                widget.setEnabled(True)
            for name in self.stopDisabledList:
                widget = getattr(self,name)
                widget.setEnabled(False)
        elif state.lower() == 'initializing':
            for name in self.initDisabledList:
                widget = getattr(self,name)
                widget.setEnabled(False)

    def timer_Callback(self):

        # Read sensor data
        data = self.sensor.readData()
        if data is not None:
            if data['type'] == 'sensor':
                self.stateLabel.setText('Running')

                # Update log files
                self.logger.addData(data['number'],data)
                self.logger.write()

                # Write time information
                timeSec = 1.0e-3*data['time']
                if self.firstTime is None:
                    self.firstTime = timeSec
                timeSec = timeSec - self.firstTime
                self.timeLabel.setText('Time (s): %1.0f'%(timeSec,))

                # Write data to table
                num = data['number']
                if num < self.numSensors:
                    self.tableItem[(num,0)].setText(str(data['count']))
                    valueStr = '%1.6f'%(data['value'],)
                    self.tableItem[(num,2)].setText(valueStr)
                    sampleTime = 1.0e-3*data['time']
                    try:
                        dt = sampleTime - self.lastSampleTime[num]
                        freq = 1.0/(dt)
                        #freqStr = '%1.2f'%(freq,)
                        freqFilt = self.freqFilter[num].update(freq,dt)
                        freqStr = '%1.2f'%(freqFilt,)
                    except KeyError:
                        self.freqFilter[num].state = 0
                        freqStr = ''
                        pass
                    self.tableItem[(num,1)].setText(freqStr)
                    self.lastSampleTime[num] = sampleTime 

    def serialPortEdit_Callback(self):
        self.port = str(self.serialPortEdit.text())

    def startPressed_Callback(self):
        """
        Called before start Clicked
        """
        # Set initializing text and disable appropriate widgets
        self.stateLabel.setText('Initializing')
        self.setEnabledForState('Initializing')

        # Clear table items
        for i in range(0,self.numSensors):
            for j in range(0,len(self.horizontalHeaderLabels)):
                self.tableItem[(i,j)].setText('')

    def startClicked_Callback(self):

        # Set push button enables and update state
        self.setEnabledForState('Running')

        # Try to open serial port
        try:
            self.sensor = SensorComm(port=self.port)
        except serial.serialutil.SerialException, e:
            QtGui.QMessageBox.critical(self,'Error', '%s'%(e,))
            self.sensor = None
            self.stateLabel.setText('Stopped')
            self.setEnabledForState('Stopped')
            return

        # Try to open log file
        try:
            self.logger = Logger(self.logPath)
        except IOError, e:
            Qt.Gui.QMessageBox.critical(self,'Error', 'unable to open log file: %s'%(e,))
            self.stopSensor()
            return

        # Start timer running
        self.running = True
        self.firstTime = None
        self.lastSampleTime = {}
        self.timer.start()

    def stopClicked_Callback(self):
        # Close and delete sensor object
        self.stopSensor()
        
        # Stop timer
        self.timer.stop()
        self.running = False

        # Finish writing file, stop and delete logger
        try:
            self.logger.writeRemaining()
            self.logger.close()
            del self.logger
            self.logger = None
        except:
            pass

        # Update pushbutton enables and state
        self.setEnabledForState('Stopped')
        self.stateLabel.setText('Stopped')

    def fileClicked_Callback(self):
        filename = QtGui.QFileDialog.getSaveFileName(None,'Select log file',self.lastDir)
        filename = str(filename)
        if filename:
            # Set new log file
            self.logPath = filename
            #self.statusbar.showMessage('Log File: %s'%(filename,))
            # Set last directory
            self.lastDir =  os.path.split(filename)[0]

    def stopSensor(self):
        try:
            self.sensor.close()
            del self.sensor
            self.sensor = None
        except:
            pass

    def main(self):
        self.show()

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    capSensor = CapSensor()
    capSensor.main()
    app.exec_()
