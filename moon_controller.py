import os

from PyQt5.QtCore import Qt, QObject, QDate
from PyQt5.QtGui import QIntValidator
from PyQt5 import QtWidgets

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
                        if self._mModel.Mood == []:                             # обязательно добавляем значение None в Y
                            self._mModel.Mood.append(None)                      # чтобы график не вылетел

        if item.column() == 1:                                    # если столбец для mood
            if self.validate(item.data(Qt.DisplayRole)) is True:  # если данные проходят валидацию или None
                self._mModel.Mood[item.row()] = int(new_data)     # то записываем в модель новые значения
                if self.checkNextRow(item) is True:               # метод проверяет последняя строка заполнена ли, если заполнена
                    self._mModel.addDate()                        # вызваем метод добавления строк с новыми датами
            else:
                self._mModel.Mood[item.row()] = None              # если данные не проходят валидацию, ячейку оставляем пустой
                item.setText(None)

        self._mModel.cleanerRow()                                 # подчищаем лишние ячейки пустые
        self._mView.updateGraph()                                 # запускаем отрисовку графика

    def validate(self, item):
        """
        Метод проверяет корректность написания данных Mood
        """
        p = 0
        result = self.validator.validate(item, p)
        return result[0] == 2

    def checkNextRow(self, item):
        """
        Метод проверяет есть строки после измененной ячейки
        """
        if (item.row()+1) == self._mModel.RowCount:
            return True
        else:
            return False

    def cleanAll(self):
        self._mModel.Date = []
        self._mModel.Mood = []
        self._mModel.RowCount = 1
        self._mView.ui.tableWidget.clearContents()
        self._mView.ui.tableWidget.setRowCount(1)

    def openNewFile(self):
        """
        Метод вызывается при открытии нового файла
        """
        self.cleanAll()
        self._mView.updateGraph()
        self._mView.ui.MplWidget.setStep(6.0)

    def saveData(self):
        """
        Метод вызывается при сохранении данных
        """
        name = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', '', 'Mood Moon Files (*.mmf)')
        if name[0] == '':
            return

        with open(name[0], 'w') as file:
            for i in range(0, len(self._mModel.Date)):
                    data = str(self._mModel.Date[i].toString('dd.MM.yyyy')) + '\t' + str(self._mModel.Mood[i]) + '\n'
                    file.write(data)

    def openFile(self):
        """
        Метод вызывается при открытии файла с сохраненными данными
        """

        name = QtWidgets.QFileDialog.getOpenFileName(None, "Open Mood and Moon File", "", "Mood Moon Files (*.mmf)")
        if name[0] == '':
            return

        with open(name[0], 'r') as file:
            data = file.read()
            data = data.split('\n')
            data = data[:-1]

            self.cleanAll()
            self.writeDataToModel(data)

        self._mView.ui.MplWidget.setStep(6.0)

    def copyDataSelectedRows(self):
        """
        Метод вызывается при копировании данных
        Переводит все в строку для буфера обмена
        """
        selectedRows = self._mView.ui.tableWidget.selectedIndexes()
        self.dataForClipboard = ''
        for i in range(0, len(selectedRows)):
            self.dataForClipboard += selectedRows[i].data(Qt.DisplayRole)
            if i%2 == 0:
                self.dataForClipboard += '\t'
            else:
                self.dataForClipboard += '\n'
        self._mView.clipboard.setText(self.dataForClipboard)

    def pasteDataSelectedRows(self):
        """
        Метод вызывается при вставки данных в таблицу
        Вставляет если таблица пустая, если данные там уже есть ничего не делает
        """
        selectedItem = self._mView.ui.tableWidget.selectedIndexes()

        line = self._mView.clipboard.text()
        data = line.split('\n')                                       # убираем перенос

        if selectedItem[0].data(Qt.DisplayRole) is None:              # проверка пустая ли строка
            self.writeDataToModel(data)

        else:
            pass

    def writeDataToModel(self, data):
        """
        Метод переводит данные в необходимы тип и записывает в модель
        Запускает заполнение таблицы и отрисовку графика
        """
        for d in range(0, len(data)):
            data[d] = data[d].split('\t')                                 # разделяем дату и число Mood
        for d in data:
            self.c_date = self.c_date.fromString(d[0], "dd.MM.yyyy")      # дату перефодим в тип QDate
            if self.c_date.isValid() is False:
                pass
            else:
                self._mModel.Date.append(self.c_date)                     # сохраняем в модель даты

            if d[1] != 'None':                                            # число сохраняем модель Y
                if self.validate(d[1]) is True:
                    d[1] = int(d[1])
                    self._mModel.Mood.append(d[1])
                else:
                    pass
            else:
                self._mModel.Mood.append(None)

        if self._mModel.Date != [] or self._mModel.Mood != []:               # провека не полностью ли таблица пустая
            if self._mModel.Mood[-1] is not None:                            # проверка наличия последней пустой строки
                self._mModel.Date.append(self._mModel.Date[-1].addDays(1))
                self._mModel.Mood.append(None)

            self._mModel.RowCount = len(self._mModel.Date)                # сохраянем в модель число строк
            self._mView.dataFilling()                                     # запускаем заполнение таблицы
            self._mView.updateGraph()                                     # запускаем отрисовку графика
