from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
import matplotlib.ticker as ticker
from scipy.interpolate import BSpline
import numpy as np

from abc import ABCMeta, abstractmethod

from moon_pyqtfile import Ui_MainWindow


class MoonMeta(type(QtCore.QObject), ABCMeta):
    """
    Модуль реализации метакласса, необходимого для работы представления.

    type(QtCore.QObject) - метакласс общий для оконных компонентов Qt.
    ABCMeta - метакласс для реализации абстрактных суперклассов.
    MoonMeta - метакласс для представления.
    """
    pass


class MoonView(QMainWindow, metaclass=MoonMeta):
    """
    Класс отвечающий за визуальное представление MoonModel.
    """

    def __init__(self, in_controller, in_model, parent=None):
        super(QMainWindow, self).__init__(parent)
        self._mController = in_controller
        self._mModel = in_model
        self.left = None                                           # переменная для границы графика, пока их не поменяет скролл
        self.right = None                                          # переменная для границы графика, пока их не поменяет скролл

        # подключаем визуальное представление
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # название программы
        self.setWindowTitle("Moon-Mood")

        # связываем событие завершения редактирования с методом контроллера
        self.ui.tableWidget.itemChanged.connect(self._mController.onItemChanged, type=Qt.QueuedConnection)

        # связываем событие new file с методом открыть новый файл
        self.ui.newFile.triggered.connect(self._mController.openNewFile)

        # связываем событие save as с методом сохранить данные как
        self.ui.saveAsButton.triggered.connect(self._mController.saveAsData)

        # связываем событие save с методом сохранить данные
        self.ui.saveButton.triggered.connect(self._mController.saveData)

        # связываем событие open с методом открытия файла
        self.ui.openButton.triggered.connect(self._mController.openFile)

        # связываем событие изменения границ графка с отрисовкой графика
        self.ui.MplWidget.updateRequest.connect(self.onUpdateRequest)

        # связываем событие изменения модели с изменением данных в таблице
        self._mModel.dataChangedRequest.connect(self.dataChanged)

        # связываем событие изменения модели с изменением размера таблицы
        self._mModel.rowCountChangedRequest.connect(self.rowCountChanged)

        # связываем события изменений чекбоксов с отрисовкой графика
        self.ui.MplWidget.checkBoxMoon.toggled.connect(self.updateGraph)
        self.ui.MplWidget.checkBoxMood.toggled.connect(self.updateGraph)
        self.ui.MplWidget.checkBoxAverageMood.toggled.connect(self.updateGraph)

        # запоминаем буфер обмена
        self.app = QApplication.instance()
        self.clipboard = QApplication.clipboard()

    @pyqtSlot(float, float)
    def onUpdateRequest(self, left, right):
        """
        Метод реагирует на сигнал и устанавливает новые границы график
        """
        self.left = left
        self.right = right
        self.updateGraph()

    def updateGraph(self):
        """
        Отрисовка графика
        """
        self.correctionAxesValues()
        self.resetFigure()

        if self.left is not None:                                          # меняем пределы при прокрутке скрола
            self.ui.MplWidget.canvas.axes.set_xlim(self.left, self.right)
            delta_lim = self.right-self.left
            if delta_lim >= 8.5:                                           # меняем количество тиков, когда график сильно сжимается
                self.ui.MplWidget.canvas.axes.xaxis.set_major_locator(ticker.MaxNLocator(6))

        if self._mModel.getLengthDate() == 0 or self._mModel.getDate() == [None]:
            self.ui.MplWidget.canvas.draw()
            return

        if self.ui.MplWidget.checkBoxMood.isChecked():
            self.ui.MplWidget.canvas.axes.plot(self.X, self.Y1, 'go-', linewidth=2, markersize=2)
        else:
            self.ui.MplWidget.canvas.axes.plot(self.X, self.Y1, alpha=0.0)

        if self.ui.MplWidget.checkBoxMoon.isChecked():
            self.ui.MplWidget.canvas.axes.plot(self.X2, self.Y2, color=[0, 0, 1], linewidth=2, alpha=0.5)

        if self.ui.MplWidget.checkBoxAverageMood.isChecked() and self._mModel.getLengthDate() > 15:
            self.ui.MplWidget.canvas.axes.plot(self.X3, self.Y3, 'r-')

        self.ui.MplWidget.canvas.draw()

    def resetFigure(self):
        """
        Метод чистит область графика
        """
        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.initAxes(self.ui.MplWidget.canvas.axes)

        if self._mModel.getLengthDate() == 0 or self._mModel.getDate() == [None]:
            self.ui.MplWidget.canvas.axes.tick_params(
                axis='x',
                which='both',
                bottom=False,
                top=False,
                labelbottom=False)

    def correctionAxesValues(self):
        """
        Метод изменяет массивы данных модели в соответствии с необходимым графиком
        """
        if self._mModel.getLengthDate() == 0 or self._mModel.getDate() == [None]:
            return

        self.Y1 = self._mModel.getMood()
        y2 = self._mModel.getMoon()
        self.X = []
        for i in self._mModel.getDate():
                self.X.append(i.toString('dd.MM.yy'))

        new_x1 = []
        for i in range(0, len(self.X)):
            new_x1.append(i)

        if len(new_x1) > 7:
            self.X2 = np.linspace(0, len(new_x1), len(new_x1) * 10)
            spl = BSpline(new_x1, y2, k=3)
            self.Y2 = spl(self.X2)

            self.X3 = np.linspace(0, len(new_x1), len(new_x1)//5)
            spl = BSpline(new_x1, self.Y1, k=1)
            self.Y3 = spl(self.X3)

        else:
            self.X2 = self.X
            self.Y2 = y2

    @pyqtSlot()
    def rowCountChanged(self):
        """
        Метод вызывается при изменении модели.
        Изменяет количество строк.
        """
        row_count = int(self._mModel.getRowCount())
        self.ui.MplWidget.setMaxScroll(row_count)
        self.ui.tableWidget.setRowCount(row_count)      # создаем количество строк
        self.ui.tableWidget.blockSignals(True)          # блокируем сигнал иначе любое изменение вызывает сигнал для контролера

        z = row_count - 1
        item = QTableWidgetItem(self._mModel.getDateString(z))  # создаем новую ячейку с датой на день больше предыдущей
        self.ui.tableWidget.setItem(row_count-1, 0, item)

        row = self.ui.tableWidget.selectedItems()               # выделяем следующую ячейку
        next_row = row[0].row() + 1
        self.ui.tableWidget.setCurrentCell(next_row, 1)

        self.ui.tableWidget.blockSignals(False)

    @pyqtSlot()
    def dataChanged(self):
        """
        Метод вызывается при изменении модели.
        Изменяет данные ячеек с датами, в случае изменения даты в середине столбца.
        """
        self.ui.tableWidget.blockSignals(True)                                    # блокируется сигнал для свободного изменения ячейки

        row_count = int(self._mModel.getRowCount())
        for j in range(1, row_count):                                             #для каждой ячейки после измененной записывается новая дата
            item = QTableWidgetItem(self._mModel.getDateString(j))
            self.ui.tableWidget.setItem(j, 0, item)

        self.ui.tableWidget.blockSignals(False)

    def dataFilling(self):
        """
        Метод вызывается при отрытии файла.
        Заполняет столбцы Date и Mood.
        """
        self.ui.tableWidget.blockSignals(True)

        row_count = int(self._mModel.getRowCount())                                    # создаем количество строк
        self.ui.MplWidget.setMaxScroll(row_count)
        self.ui.tableWidget.setRowCount(row_count)
        for j in range(0, row_count):                                             # оздаем ячейки и заполняем их датами с файла
            item = QTableWidgetItem(self._mModel.getDateString(j))
            self.ui.tableWidget.setItem(j, 0, item)
        for j in range(0, row_count):                                             # оздаем ячейки и заполняем их данными Mood с файла
            if type(self._mModel.getMood(j)) is int:
                item = QTableWidgetItem(str(self._mModel.getMood(j)))
            else:
                item = QTableWidgetItem('')                                       # последняя дата идет со значение None, оставляем пустую ячейку
            self.ui.tableWidget.setItem(j, 1, item)

        self.ui.tableWidget.blockSignals(False)

    def keyPressEvent(self, event):
        """
        Метод пехеватывает нажатие клавиш Ctrl+C и Ctrl+V
        """
        if event.key() == Qt.Key_Control:
            self.keyControlPressed = True
        if event.key() == Qt.Key_C:
            if self.keyControlPressed:
                self._mController.copyDataSelectedRows()              #запускаем функцию для выделения ячеек и вычленения из них текста

        if event.key() == Qt.Key_V:
            if self.keyControlPressed:
                self._mController.pasteDataSelectedRows()             #запускаем функцию для вставки текста
