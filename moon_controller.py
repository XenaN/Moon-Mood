from moon_view import MoonView

# from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class MoonController:
    """
    Класс MoonController представляет реализацию контроллера.
    Согласовывает работу представления с моделью.
    """
    def __init__(self, in_model):
        """
        Конструктор принимает ссылку на модель.
        Конструктор создаёт и отображает представление.
        """
        self._mModel = in_model
        self._mView = MoonView(self, self._mModel)

        self._mView.show()

    def onItemChanged(self, item):
        # print(int(item.data(Qt.DisplayRole)))
        # print(str(item.data(QtCore.Qt.DisplayRole)))
        print(2, str(item.data(0)))

        if item.column() == 0:
            if len(self._mModel.x) > item.row():
                self._mModel.x[item.row()] = int(item.data(Qt.DisplayRole))
            else:
                a = self._mModel.x
                a.append(int(item.data(Qt.DisplayRole)))
                self._mModel.x = a

        if item.column() == 1:
            if len(self._mModel.y) > item.row():
                self._mModel.y[item.row()] = int(item.data(Qt.DisplayRole))
            else:
                a = self._mModel.y
                a.append(int(item.data(Qt.DisplayRole)))
                self._mModel.y = a

    # def setX(self):
    #     """
    #     При завершении редактирования поля ввода данных для X,
    #     контроллер изменяет свойство x модели.
    #     """
    #     x = self._mView.tableWidget.item(n, 0).text()
    #     self._mModel.x = float(x)
    #
    # def setY(self):
    #     """
    #     При завершении редактирования поля ввода данных для Y,
    #     контроллер изменяет свойство y модели.
    #     """
    #     y = self._mView.ui.le_y.text()
    #     self._mModel.y = float(y)
