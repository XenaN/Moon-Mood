from PyQt5.QtCore import Qt, QObject, QDate
from PyQt5.QtGui import QIntValidator
from PyQt5 import QtWidgets

from moon_view import MoonView
from moon_phase import MoonPhase


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
        self._mMoonPhase = MoonPhase(self._mModel)

        # устанавливаем валидатор для значения Y
        self.validator = QIntValidator(-10, 10, self)

        # создаем экземпляр класса формата даты
        self.c_date = QDate()

        # имя файла
        self.file_name = ''

        # запускаем визуальное представление??
        self._mView.show()

    def onItemChanged(self, item):
        """
        Метод реагирует на сигнал
        Изменяет данные модели
        """
        # print(item)
        if item.column() == 0:                                    # если данные забиты в столбце с датой
            self.changeModelDate(item)

        elif item.column() == 1:                                    # если столбец для mood
            self.changeModelMood(item)

        self._mModel.cleanerRow()                                 # подчищаем лишние ячейки пустые
        self._mView.updateGraph()                                 # запускаем отрисовку графика

    def changeModelDate(self, item):
        """
        Меняет модель Date определенным образом
        """
        new_data = item.data(Qt.DisplayRole)                          # вытаскиваем из item данные
        if new_data == '' and (self._mModel.getLengthDate() == 1 or self._mModel.getLengthDate() == 0):
            self._mModel.addEmptyDate()                               # в случае пустой первой ячейки записываем значение None
            return

        self.c_date = self.c_date.fromString(new_data, "dd.MM.yyyy")  # данные из формата дата переводим в QDate
        if self.c_date.isValid() is False and item.row() == 0:        # если дата не подходящего вида оставляем ячейку пустой
            item.setText(None)
            return

        if self._mModel.getLengthDate() > item.row():                 # если данные поменялись в середине стобца, а не в конце
            if item.row() == 0:                                       # если ошибка в первой строке, то ее можно исправить
                self._mModel.changedDates(self.c_date)
            else:
                item.setText(self._mModel.getDateString(item.row()))
        else:
            self._mModel.addDate(self.c_date)                        # если добавляются новые данные
            self._mModel.addMood(None)

    def changeModelMood(self, item):
        """
        Меняет модель Mood определенным образом
        """
        new_data = item.data(Qt.DisplayRole)                     # вытаскиваем из item данные
        if self.validate(item.data(Qt.DisplayRole)) is True:     # если данные проходят валидацию или None
            self._mModel.addMood(int(new_data), item.row())      # то записываем в модель новые значения
            if self.checkNextRow(item) is True:                  # метод проверяет последняя строка заполнена ли, если заполнена
                self._mModel.addNextDate()                       # вызваем метод добавления строк с новыми датами
        else:
            self._mModel.addMood(None, item.row())               # если данные не проходят валидацию, ячейку оставляем пустой
            item.setText(None)

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
        if (item.row()+1) == self._mModel.getRowCount():
            return True
        else:
            return False

    def cleanAll(self):
        """
        Метод очищает все данные
        """
        self._mModel.setNullModel()
        self._mMoonPhase.setNullQuarterPhase()
        self._mView.ui.tableWidget.clearContents()
        self._mView.ui.tableWidget.setRowCount(1)
        self._mView.ui.MplWidget.setMaxScroll(0)

    def openNewFile(self):
        """
        Метод вызывается при открытии нового файла
        """
        self.file_name = ''
        self.cleanAll()
        self._mView.ui.MplWidget.setStep(6.0)

        self._mView.resetFigure()
        self._mView.ui.MplWidget.canvas.draw()

    def saveAsData(self):
        """
        Метод вызывается при сохранении данных
        """
        name = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', '', 'Mood Moon Files (*.mmf)')
        self.file_name = name
        if name[0] == '':
            return

        with open(name[0], 'w') as file:
            for i in range(0, self._mModel.getLengthDate()):
                    data = self._mModel.getDateString(i) + '\t' + str(self._mModel.getMood(i)) + '\n'
                    file.write(data)

    def saveData(self):
        """
        Метод вызывается при сохранении данных
        """
        if self.file_name == '':
            return

        name = self.file_name

        with open(name[0], 'w') as file:
            for i in range(0, self._mModel.getLengthDate()):
                    data = self._mModel.getDateString(i) + '\t' + str(self._mModel.getMood(i)) + '\n'
                    file.write(data)

    def openFile(self):
        """
        Метод вызывается при открытии файла с сохраненными данными
        """
        name = QtWidgets.QFileDialog.getOpenFileName(None, "Open Mood and Moon File", "", "Mood Moon Files (*.mmf)")
        self.file_name = name
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
        if data[-1] == '':
            data = data[:-1]

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
                self._mModel.addDate(self.c_date)                         # сохраняем в модель даты

            if d[1] != 'None':                                            # число сохраняем модель Y
                if self.validate(d[1]) is True:
                    d[1] = int(d[1])
                    self._mModel.addMood(d[1])
                else:
                    pass
            else:
                self._mModel.addMood(None)



        if self._mModel.getDate() != [] or self._mModel.getMood() != []:    # провека не полностью ли таблица пустая
            self._mModel.setRowCount(self._mModel.getLengthDate())  # сохраянем в модель число строк
            if self._mModel.getMood(-1) is not None:                        # проверка наличия последней пустой строки
                self._mModel.addNextDate()

            self._mView.ui.MplWidget.setMaxScroll(self._mModel.getRowCount())
            self._mView.dataFilling()                                       # запускаем заполнение таблицы
            self._mView.updateGraph()                                       # запускаем отрисовку графика

        else:
            self._mModel.setRowCount(1)
            self._mView.resetFigure()
            self._mView.ui.MplWidget.canvas.draw()