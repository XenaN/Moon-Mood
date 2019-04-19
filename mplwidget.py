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
        self.steps_visible = 6.0
        self.n = 0
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

    def setStep(self, step):
        """
        Метод обновляет self.step
        """
        self.steps_visible = step
        self.scroll.setValue(0)
        self.updateScrollArea(self.scroll.value())


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
        if value == 0:                                      # set_lim утанавливает границы жестко, в том числе убирает смещение по оси x
            if self.steps_visible == 6:                      # в итоге пересечение осей по значением происходит строго в координате 0,0
                left = -0.5                                 # для того, чтобы даты не наезжали на ось введено искусственно смещение на 0,5
            else:
                left = self.steps_visible / -15 - 0.25       # это смещение меняется в зависимости от количества точек на оси

            right = 0 + self.steps_visible
        else:
            left = value * (self.maxScroll - self.steps_visible) / self.scroll.maximum()
            right = left + self.steps_visible

        self.updateRequest.emit(left, right)

    def wheelEvent(self, event=QWheelEvent):
        """
        Метод реагирует на движение колеса мыши.
        При движении колеса мыши двигает скролл.
        При нажатии клавиши Ctrl и движении колеса меняет размер графика.
        """
        modifiers = QApplication.keyboardModifiers()
        delta = event.angleDelta().y()

        if modifiers == QtCore.Qt.ControlModifier:
            if delta < 0:
                if self.steps_visible > 1.5:
                    self.steps_visible -= 1
            else:
                if self.steps_visible < self.maxScroll:
                    self.steps_visible += 1

            self.checkScrollVisibility()
            self.updateScrollArea(self.scroll.value())

        else:
            if self.steps_visible == self.maxScroll:
                return

            step_coef = (self.steps_visible / self.maxScroll + 0.036) / 0.0312  # высчитаны коэффициенты по формуле линейной зависимости
            if delta > 0:                                                  # x = step_coef, y = self.step_visible/self.maxScroll
                step_scroll = self.scroll.value() + step_coef              # y = ax + b
            else:                                                          # 6/50 = 5*a + b - 5 комфортный шаг при 6 точках на графике из 50
                step_scroll = self.scroll.value() - step_coef              # 45/50 = 30*a + b

            self.scroll.setValue(step_scroll)

    def checkScrollVisibility(self):
        """
        Метод прячет скролл, когда это необходимо
        """
        if self.steps_visible == self.maxScroll:
            self.scroll.setEnabled(False)
            self.scroll.setValue(0)
            self.updateScrollArea(self.scroll.value())
        else:
            self.scroll.setEnabled(True)
