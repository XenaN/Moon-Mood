from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QMutex

from abc import ABCMeta, abstractmethod

from moon_pyqtfile import Ui_MainWindow

import numpy as np
from matplotlib.dates import datestr2num

class MoonObserver(metaclass=ABCMeta):
    """
    Абстрактный суперкласс для всех наблюдателей.
    """

    @abstractmethod
    def dataChanged(self):
        """
        Метод который будет вызван у наблюдателя при изменении модели.
        """
        pass


class MoonMeta(type(QtCore.QObject), ABCMeta):
    """
    Модуль реализации метакласса, необходимого для работы представления.

    type(QtCore.QObject) - метакласс общий для оконных компонентов Qt.
    ABCMeta - метакласс для реализации абстрактных суперклассов.
    MoonMeta - метакласс для представления.
    """
    pass


class MoonView(QMainWindow, MoonObserver, metaclass=MoonMeta):
    """
    Класс отвечающий за визуальное представление MoonModel.
    """

    def __init__(self, in_controller, in_model, parent=None):
        # super().__init__()
        super(QMainWindow, self).__init__(parent)
        self._mController = in_controller
        self._mModel = in_model

        # подключаем визуальное представление
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # регистрируем представление в качестве наблюдателя
        self._mModel.addObserver(self)

        # название программы
        self.setWindowTitle("Moon-Mood")

        # связываем событие завершения редактирования с методом контроллера
        self.ui.tableWidget.itemChanged.connect(self._mController.onItemChanged, type=Qt.QueuedConnection)

    def updateGraph(self):
        # print('graph')
        # print(self._mModel.Date, self._mModel.Y)
        x = []
        for i in self._mModel.Date:
            if i is not None:
                x.append(i.toString('dd.MM.yy'))
            else:
                x.append(None)
        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.initAxes(self.ui.MplWidget.canvas.axes)

        if len(self._mModel.Date) == 0 or self._mModel.Date == [None]:
            self.ui.MplWidget.canvas.axes.tick_params(
                                        axis='x',  # changes apply to the x-axis
                                        which='both',  # both major and minor ticks are affected
                                        bottom=False,  # ticks along the bottom edge are off
                                        top=False,  # ticks along the top edge are off
                                        labelbottom=False)

        self.ui.MplWidget.canvas.axes.plot(x, self._mModel.Y, 'go--', linewidth=2, markersize=5)
        self.ui.MplWidget.canvas.draw()
        # print('graph end')


    def rowCountChanged(self):
        """
        Метод вызывается при изменении модели.
        Изменяет количество строк.
        """

        row_count = int(self._mModel.RowCount)
        self.ui.tableWidget.setRowCount(row_count)
        self.ui.tableWidget.blockSignals(True)
        z = row_count - 1
        item = QTableWidgetItem(self._mModel.Date[z].toString('dd.MM.yyyy'))
        self.ui.tableWidget.setItem(row_count-1, 0, item)
        self.ui.tableWidget.blockSignals(False)

    def dataChanged(self, item_row):
        self.ui.tableWidget.blockSignals(True)
        row_count = int(self._mModel.RowCount)
        for j in range(item_row+1, row_count):
            item = QTableWidgetItem(self._mModel.Date[j].toString('dd.MM.yyyy'))
            self.ui.tableWidget.setItem(j, 0, item)
        self.ui.tableWidget.blockSignals(False)
