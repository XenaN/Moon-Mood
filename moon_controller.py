from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QRegExpValidator, QValidator, QIntValidator

from moon_view import MoonView


class MoonController(QObject):
    """
    Класс MoonController представляет реализацию контроллера.
    Согласовывает работу представления с моделью.
    """
    def __init__(self, in_model):
        """
        Конструктор принимает ссылку на модель.
        Конструктор создаёт и отображает представление.
        """
        super().__init__()
        self._mModel = in_model
        self._mView = MoonView(self, self._mModel)

        self.validator = QIntValidator(-10, 10, self)

        self._mView.show()

    def onItemChanged(self, item):
        if self.validate(item) is True:
            # print(2, str(item.data(0)))

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
        else:
            item.setText('')

    # устанавливаем валидатор поля ввода данных
    def validate(self, item):
        # rx = r"-?[0-9]*[.{0}]?[0-9]*"

        i = item.data(Qt.DisplayRole)
        p = 0
        result = self.validator.validate(i, p)
        return result[0] == 2

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
