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
        new_data = item.data(Qt.DisplayRole)
        if new_data == '':
            new_data = None
        else:
            new_data = int(item.data(Qt.DisplayRole))

        if self.validate(item) is True or new_data is None:

            if item.column() == 0:
                if len(self._mModel.x) > item.row():
                    self._mModel.x[item.row()] = new_data
                else:
                    a = self._mModel.x
                    a.append(new_data)
                    self._mModel.x = a

            if item.column() == 1:
                if len(self._mModel.y) > item.row():
                    self._mModel.y[item.row()] = new_data
                else:
                    a = self._mModel.y
                    a.append(new_data)
                    self._mModel.y = a
        else:
            item.setText(None)

        self._mView.update_graph()

    # устанавливаем валидатор поля ввода данных
    def validate(self, item):
        # rx = r"-?[0-9]*[.{0}]?[0-9]*"

        i = item.data(Qt.DisplayRole)
        p = 0
        result = self.validator.validate(i, p)
        return result[0] == 2
