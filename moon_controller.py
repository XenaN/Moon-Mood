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
        print(str(item.data(0))) # надо преобразовать в дисплей роль

        if item.column() == 0:
            print(2)
            if int(item.data(Qt.DisplayRole)) in self._mModel.x:
                self._mModel.x[item.row()] = int(item.data(Qt.DisplayRole))
            else:
                self._mModel.x.append(int(item.data(Qt.DisplayRole)))

        if item.column() == 1:
            if int(item.data(Qt.DisplayRole)) in self._mModel.y:
                self._mModel.y[item.row()] = int(item.data(Qt.DisplayRole))
            else:
                self._mModel.y.append(int(item.data(Qt.DisplayRole)))

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
