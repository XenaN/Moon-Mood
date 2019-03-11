from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from abc import ABCMeta, abstractmethod

from moon_pyqtfile import Ui_MainWindow

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
        self.setWindowTitle("First project")

        # связываем событие завершения редактирования с методом контроллера
        print(1)
        self.ui.tableWidget.itemChanged.connect(self._mController.onItemChanged)

    def update_graph(self):
        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.plot(self._mModel.x, self._mModel.y, 'go--', linewidth=2, markersize=5)
        self.ui.MplWidget.canvas.draw()

    def dataChanged(self):
        """
        Метод вызывается при изменении модели.
        Изменяет количество строк.
        """

        row_count = int(self._mModel.rowCount)
        self.ui.tableWidget.setRowCount(row_count)
        for j in range(2):
            item = QTableWidgetItem()
            self.ui.tableWidget.setItem(row_count, j, item)





