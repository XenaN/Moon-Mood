from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure


class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)

        self.initAxes(self.canvas.axes)
        self.canvas.axes.tick_params(
                                    axis='x',          # changes apply to the x-axis
                                    which='both',      # both major and minor ticks are affected
                                    bottom=False,      # ticks along the bottom edge are off
                                    top=False,         # ticks along the top edge are off
                                    labelbottom=False)

        self.setLayout(vertical_layout)

    def initAxes(self, figure):
        figure.set_ylim(-10, 10)

        figure.spines['bottom'].set_position('center')
        figure.spines['right'].set_color('none')
        figure.spines['top'].set_color('none')

        figure.xaxis.set_ticks_position('bottom')
