# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'capsensor_ui.ui'
#
# Created: Mon Jul 11 22:45:34 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(573, 442)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_3 = QtGui.QWidget(self.frame)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.timeLabel = QtGui.QLabel(self.widget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeLabel.sizePolicy().hasHeightForWidth())
        self.timeLabel.setSizePolicy(sizePolicy)
        self.timeLabel.setObjectName("timeLabel")
        self.horizontalLayout_3.addWidget(self.timeLabel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.stateLabel = QtGui.QLabel(self.widget_3)
        self.stateLabel.setObjectName("stateLabel")
        self.horizontalLayout_3.addWidget(self.stateLabel)
        self.verticalLayout_3.addWidget(self.widget_3)
        self.tableWidget = QtGui.QTableWidget(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tableWidget)
        self.verticalLayout.addWidget(self.frame)
        self.widget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.serialPortEdit = QtGui.QLineEdit(self.widget)
        self.serialPortEdit.setObjectName("serialPortEdit")
        self.horizontalLayout.addWidget(self.serialPortEdit)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.startPushButton = QtGui.QPushButton(self.widget)
        self.startPushButton.setObjectName("startPushButton")
        self.horizontalLayout.addWidget(self.startPushButton)
        self.stopPushButton = QtGui.QPushButton(self.widget)
        self.stopPushButton.setObjectName("stopPushButton")
        self.horizontalLayout.addWidget(self.stopPushButton)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtGui.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.logFileLabel = QtGui.QLabel(self.widget_2)
        self.logFileLabel.setObjectName("logFileLabel")
        self.horizontalLayout_2.addWidget(self.logFileLabel)
        self.filePushButton = QtGui.QToolButton(self.widget_2)
        self.filePushButton.setObjectName("filePushButton")
        self.horizontalLayout_2.addWidget(self.filePushButton)
        self.verticalLayout.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Capillary  Sensor", None, QtGui.QApplication.UnicodeUTF8))
        self.timeLabel.setText(QtGui.QApplication.translate("MainWindow", "Time (s): ", None, QtGui.QApplication.UnicodeUTF8))
        self.stateLabel.setText(QtGui.QApplication.translate("MainWindow", "Stopped", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Serial Port", None, QtGui.QApplication.UnicodeUTF8))
        self.startPushButton.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.stopPushButton.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.logFileLabel.setText(QtGui.QApplication.translate("MainWindow", "Log File: None", None, QtGui.QApplication.UnicodeUTF8))
        self.filePushButton.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
