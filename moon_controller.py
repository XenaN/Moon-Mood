from PyQt5.QtCore import Qt, QObject, QDate
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

        self.c_date = QDate()

        self._mView.show()

    def onItemChanged(self, item):
        # print(item)
        new_data = item.data(Qt.DisplayRole)

        if item.column() == 0:
            self.c_date = self.c_date.fromString(new_data, "dd.MM.yyyy")
            if self.c_date.isValid() is False:
                item.setText(None)
            else:
                if len(self._mModel.date) > item.row():
                    a = self._mModel.date
                    a[item.row()] = self.c_date
                    for j in range(item.row()+1, len(a)):
                        a[j] = a[j-1].addDays(1)
                    self._mModel.date = a
                    self._mView.dataChanged(item.row())
                else:
                    a = self._mModel.date
                    a.append(self.c_date)
                    self._mModel.date = a

        if item.column() == 1:
            if new_data == '':
                new_data = None
            else:
                new_data = int(item.data(Qt.DisplayRole))

            if self.validate(item) is True or new_data is None:
                a = self._mModel.y
                a[item.row()] = new_data
                self._mModel.y = a
            else:
                item.setText(None)

        self._mModel.cleanerRow()
        self._mView.update_graph()

    # устанавливаем валидатор поля ввода данных
    def validate(self, item):
        # rx = r"-?[0-9]*[.{0}]?[0-9]*"

        i = item.data(Qt.DisplayRole)
        p = 0
        result = self.validator.validate(i, p)
        return result[0] == 2
