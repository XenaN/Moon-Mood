import sys
#from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np
import random
import one_copy

class MyWin (QMainWindow, one_copy.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        #loadUi("one_copy.ui", self)

        self.setWindowTitle("First project")

        self.update_graph()

    def update_graph(self):
        f = random.randint(1, 100)
        length_of_signal = 100
        t = np.linspace(0, 1, length_of_signal)

        cosinus_signal = np.cos(2 * np.pi * f * t)
        sinus_signal = np.sin(2 * np.pi * f * t)

        self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        self.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
        self.MplWidget.canvas.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWin()
    window.show()

    sys.exit(app.exec_())