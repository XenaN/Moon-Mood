from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import Slider

import numpy as np

class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.canvas.axes = self.canvas.figure.add_subplot(111)

        self.initAxes(self.canvas.axes)
        self.canvas.axes.tick_params(
                                    axis='x',          # changes apply to the x-axis
                                    which='both',      # both major and minor ticks are affected
                                    bottom=False,      # ticks along the bottom edge are off
                                    top=False,         # ticks along the top edge are off
                                    labelbottom=False)

        self.setLayout(vertical_layout)

        # self.scroll = QScrollBar(QtCore.Qt.Horizontal)
        # vertical_layout.addWidget(self.scroll)
        # self.step = .1
        # self.setupSlider()


        # axis_N = self.canvas.figure.add_axes([0.10, 0.03, 0.8, 0.03])
        # slider_N = Slider(axis_N, 'N', 1, 100, valinit=2)
        # print('AXIS: ', self.canvas.axes)
        # slider = Slider(self.canvas.axes, 'XXX', 0.0, 1.0, val=3)
        #self.slider = Slider(self.canvas.axes.xaxis, 'XXX', 0.0, 1.0, val=3)
        #self.slider.on_changed()


    def initAxes(self, figure):
        figure.set_ylim(-10.3, 10.3)

        figure.spines['bottom'].set_position('center')
        figure.spines['right'].set_color('none')
        figure.spines['top'].set_color('none')

        figure.xaxis.set_ticks_position('bottom')

    def setupSlider(self):
        self.lims = np.array(self.canvas.axes.get_xlim())
        self.scroll.setPageStep(self.step * 100)
        self.scroll.actionTriggered.connect(self.update)
        self.update()

    def update(self, evt=None):
        r = self.scroll.value() / ((1 + self.step) * 100)
        l1 = self.lims[0] + r * np.diff(self.lims)
        l2 = l1 + np.diff(self.lims) * self.step
        self.canvas.axes.set_xlim(l1, l2)

