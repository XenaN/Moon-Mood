from PyQt5.QtWidgets import *
from PyQt5 import QtCore, Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QWheelEvent

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplWidget(QWidget):
    """
    Модуль создания графика без данных
    """

    updateRequest = pyqtSignal(float, float)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())                    # создаем область где будет отрисовываться график

        vertical_layout = QVBoxLayout()                          # создается лэйаут без отступов
        vertical_layout.addWidget(self.canvas)
        vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.canvas.axes = self.canvas.figure.add_subplot(111)   # создаем сам график

        self.initAxes(self.canvas.axes)                          # устанавливаем оси
        self.canvas.axes.tick_params(                            # изменяем ось X, чтобы была пустой
                                    axis='x',          # changes apply to the x-axis
                                    which='both',      # both major and minor ticks are affected
                                    bottom=False,      # ticks along the bottom edge are off
                                    top=False,         # ticks along the top edge are off
                                    labelbottom=False)

        self.setLayout(vertical_layout)

        self.scroll = QScrollBar(QtCore.Qt.Horizontal)
        vertical_layout.addWidget(self.scroll)
        self.step = 6.5
        self.maxScroll = 6
        self.setupScrollArea()

    def initAxes(self, figure):
        """
        Метод опускющий вниз ось X и устанавливабщий границы оси Y
        """
        figure.set_ylim(-10.3, 10.3)
        figure.set_xlim(-0.5, 6)

        figure.spines['bottom'].set_position('center')
        figure.spines['right'].set_color('none')
        figure.spines['top'].set_color('none')

        figure.xaxis.set_ticks_position('bottom')

    def setMaxScroll(self, maximum):
        """
        Метод устанавливабщий макисмальное значение для скролла
        """
        self.maxScroll = maximum

    def setupScrollArea(self):
        """
        Метод инициализирует скролл и делает коннект на его движение
        """
        self.scroll.setPageStep(10)
        self.scroll.valueChanged.connect(self.updateScrollArea)
        self.updateScrollArea(self.scroll.minimum())

    def updateScrollArea(self, value):
        """
        Метод устанавливает новые границы для графика при движении скролла
        """
        if value == 0:
            left = -0.5
        else:
            left = value*(self.maxScroll-self.step)/self.scroll.maximum()
        right = left + self.step
        self.updateRequest.emit(left, right)

    def wheelEvent(self, event=QWheelEvent):
        """
        Метод реагирует на движение колеса мыши.
        При движении колеса мыши двигает скролл.
        При нажатии клавиши Ctrl и движении колеса меняет размер графика.
        """
        delta = event.angleDelta().y()
        modifiers = QApplication.keyboardModifiers()

        if modifiers == QtCore.Qt.ControlModifier:
            if delta < 0:
                if self.step > 1.5:
                    self.step -= 1
            else:
                if self.step <= self.maxScroll + 1:
                    self.step += 1
            self.updateScrollArea(self.scroll.value())

        else:
            if delta > 0:
                step_scroll = self.scroll.value() - 5
            else:
                step_scroll = self.scroll.value() + 5

            self.scroll.setValue(step_scroll)
