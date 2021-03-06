from PyQt5 import QtCore, QtWidgets

from moon_mplwidget import MplWidget



class Ui_MainWindow(object):
    """
     Модуль от QT дизайнера
    """
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(941, 478)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)

        self.MplWidget = MplWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MplWidget.sizePolicy().hasHeightForWidth())
        self.MplWidget.setSizePolicy(sizePolicy)
        self.MplWidget.setObjectName("MplWidget")
        self.MplWidget.setMinimumSize(QtCore.QSize(500, 300))
        self.horizontalLayout.addWidget(self.MplWidget)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(315, 300))
        self.tableWidget.setMaximumSize(QtCore.QSize(7000000, 15000000))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.horizontalLayout.addWidget(self.tableWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 941, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.fileMenu = self.menubar.addMenu('File')

        self.newFile = QtWidgets.QAction(MainWindow)
        self.newFile.setText('New File')
        self.newFile.setShortcut('Ctrl+N')
        self.fileMenu.addAction(self.newFile)

        self.openButton = QtWidgets.QAction(MainWindow)
        self.openButton.setText('Open')
        self.openButton.setShortcut('Ctrl+O')
        self.fileMenu.addAction(self.openButton)

        self.saveAsButton = QtWidgets.QAction(MainWindow)
        self.saveAsButton.setText('Save as')
        self.fileMenu.addAction(self.saveAsButton)

        self.saveButton = QtWidgets.QAction(MainWindow)
        self.saveButton.setText('Save')
        self.saveButton.setShortcut('Ctrl+S')
        self.fileMenu.addAction(self.saveButton)

        # self.settingsButton = QtWidgets.QAction(MainWindow)
        # self.settingsButton.setText('Settings')
        # self.settingsButton.setShortcut('Ctrl+P')
        # self.fileMenu.addAction(self.settingsButton)

        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Date"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Mood"))
