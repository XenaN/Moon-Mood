from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
import matplotlib.ticker as ticker

from abc import ABCMeta, abstractmethod

from moon_pyqtfile import Ui_MainWindow


# class MoonObserver(metaclass=ABCMeta):
#     """
#     Абстрактный суперкласс для всех наблюдателей.
#     """
#
#     @abstractmethod
#     def dataChanged(self):
#         """
#         Метод который будет вызван у наблюдателя при изменении модели.
#         """
#         pass


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
        x = []
        y1 = self._mModel.getMood()
        y2 = self._mModel.getMoon()
        for i in self._mModel.getDate():                                 # переводим данные из формата QDate в строку
            if i is not None:
                x.append(i.toString('dd.MM.yy'))
            else:
                x.append(None)                                      # значение None пока появляется только в первой ячеке

        a, b, c = len(x), len(y1), len(y2)

        self.ui.MplWidget.canvas.axes.clear()                       # очищаем область для графика, иначе он сохранят старые отредактированные данные
        self.ui.MplWidget.initAxes(self.ui.MplWidget.canvas.axes)

        if self._mModel.getLengthDate() == 0 or self._mModel.getDate() == [None]: # в случае остсутвия первой даты,
            self.ui.MplWidget.canvas.axes.tick_params(                            # ось Х оставить пустой
                                        axis='x',
                                        which='both',
                                        bottom=False,
                                        top=False,
                                        labelbottom=False)

        if self.left is not None:                                          # меняем пределы при прокрутке скрола
            self.ui.MplWidget.canvas.axes.set_xlim(self.left, self.right)
            delta_lim = self.right-self.left
            if delta_lim >= 8.5:                                           # меняем количество тиков, когда график сильно сжимается
                self.ui.MplWidget.canvas.axes.xaxis.set_major_locator(ticker.MaxNLocator(6))

        self.ui.MplWidget.canvas.axes.plot(x, y1, 'go--', linewidth=2, markersize=2)  # создание графика
        self.ui.MplWidget.canvas.axes.plot(x, y2, color=[0, 0, 1], linewidth=2)
        self.ui.MplWidget.canvas.draw()                                               # его отрисовка

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

