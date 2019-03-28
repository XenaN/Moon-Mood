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

        # устанавливаем валидатор для значения Y
        self.validator = QIntValidator(-10, 10, self)

        # создаем экземпляр класса формата даты
        self.c_date = QDate()

        # запускаем визуальное представление??
        self._mView.show()

    def onItemChanged(self, item):
        """
        Метод реагирует на сигнал
        Изменяет данные модели
        """
        # print(item)
        new_data = item.data(Qt.DisplayRole)                                   # вытаскиваем из item данные

        if item.column() == 0:                                                 # если данные забиты в столбце с датой
            if new_data == '' and len(self._mModel.Date) == 1:                 # в случае пустой первой ячейки записываем значение None
                self._mModel.Date[item.row()] = None
            else:
                self.c_date = self.c_date.fromString(new_data, "dd.MM.yyyy")   # данные из формата дата переводим в строку
                if self.c_date.isValid() is False:                             # если дата не подходящего вида оставляем ячейку пустой
                    item.setText(None)
                else:
                    if len(self._mModel.Date) > item.row():                     # если данные поменялись в середине стобца, а не в конце
                        self._mModel.Date[item.row()] = self.c_date             # то заменяем старые на новые
                        for j in range(item.row() + 1, len(self._mModel.Date)): # и последующие увеличиваем на день после новой даты
                            self._mModel.Date[j] = self._mModel.Date[j-1].addDays(1)
                        if len(self._mModel.Date) > 1:                          # в таком случае запускаем замену всех последующих
                            self._mView.dataChanged(item.row())                 # данных в ячеках
                    else:
                        self._mModel.Date.append(self.c_date)                   # если добавляются новые данные
                        if self._mModel.Y == []:                                # обязательно добавляем значение None в Y
                            self._mModel.Y.append(None)                         # чтобы график не вылетел

        if item.column() == 1:                                    # если столбец для mood
            # if new_data == '' or self.validate(item) is not True: # в случае пустой записи, в модель Y пишется None
            #     new_data = None
            # else:
            #     new_data = int(item.data(Qt.DisplayRole))         # в другом случае строка переводится в значение

            if self.validate(item) is True:   # если данные проходят валидацию или None
                self._mModel.Y[item.row()] = int(new_data)        # то записываем в модель новые значения
                if self.checkNextRow(item) is True:               # метод проверяет последняя строка заполнена ли, если заполнена
                    self._mModel.addDate()                        # вызваем метод добавления строк с новыми датами
            else:
                self._mModel.Y[item.row()] = None                 # если данные не проходят валидацию, ячейку оставляем пустой
                item.setText(None)

        self._mModel.cleanerRow()                                 # подчищаем лишние ячейки пустые
        self._mView.updateGraph()                                 # запускаем отрисовку графика

    def validate(self, item):
        """
        Метод проверяет корректность написания данных Mood
        """
        # rx = r"-?[0-9]*[.{0}]?[0-9]*"

        i = item.data(Qt.DisplayRole)
        p = 0
        result = self.validator.validate(i, p)
        return result[0] == 2

    def checkNextRow(self, item):
        """
        Метод проверяет есть строки после измененной ячейки
        """
        if (item.row()+1) == self._mModel.RowCount:
            return True
        else:
            return False
