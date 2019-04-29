from PyQt5.QtCore import pyqtSignal, QDate, QObject

class MoonModel(QObject):
    """
    Класс MoonModel представляет собой реализацию модели данных.

    Модель предоставляет интерфейс, через который можно работать
    с хранимыми значениями.

    Модель содержит методы регистрации, удаления и оповещения
    наблюдателей.
    """
    cleanPhaseRequest = pyqtSignal(QDate)
    calculatePhaseRequest = pyqtSignal(QDate)
    setNullPhaseRequest = pyqtSignal()
    dataChangedRequest = pyqtSignal()
    rowCountChangedRequest = pyqtSignal()

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.__Date = []              # значения столбца даты
        self.__Mood = []              # значения столбца Mood
        self.__RowCount = 1           # список строк в таблице
        self.__Moon = []              # список фаз луны по оси Y

    def getDate(self):
        """
        Возвращает список для отрисовки графика
        """
        return self.__Date

    def getMood(self, index=None):
        """
        Возвращает список для отрисовки графика
        """
        if index == None:
            return self.__Mood
        else:
            return self.__Mood[index]

    def getMoon(self):
        """
        Возвращает список для отрисовки графика
        """
        return self.__Moon

    def getRowCount(self):
        """
        Возвращает количество строк
        """
        return self.__RowCount

    def setRowCount(self, row_count):
        """
        Меняет количество строк
        """
        self.__RowCount = row_count

    def addEmptyDate(self):
        """
        Обнуляет модель, когда строка остется одна
        """
        self.__Date = [None]
        self.__Moon = [None]
        self.__Mood = [None]
        self.setNullPhaseRequest.emit()

    def addDate(self, date):
        """
        Добавляет в модель дат первую записанную дату
        """
        self.__Date.append(date)
        self.calculatePhaseRequest.emit(date)
        self.rowCountChangedRequest.emit()

    def addNextDate(self):
        """
        Метод добавляет еще одну дату, чтобы появилась новая строка с ней
        """
        self.__RowCount = len(self.__Mood) + 1      # увеличиваем количество строк на одну

        b = self.__Date[-1].addDays(1)
        self.__Date.append(b)                  # добавляем следующую дату в список Date
        self.__Mood.append(None)               # ему же приписываем значение None в Y

        self.calculatePhaseRequest.emit(b)
        self.rowCountChangedRequest.emit()

    def getDateString(self, index):
        """
        Возвращает дату в виде строки
        """
        return self.__Date[index].toString("dd.MM.yyyy")

    def changedDates(self, date):
        """
        Меняет первую дату в списке и увеличивает на один все последующие
        """
        self.__Date[0] = date                            # заменяем старые даты на новые
        for j in range(1, len(self.__Date)):             # и последующие увеличиваем на день после новой даты
            self.__Date[j] = self.__Date[j - 1].addDays(1)

        self.__Moon = []
        self.setNullPhaseRequest.emit()
        for i in self.__Date:
            self.calculatePhaseRequest.emit(i)
        self.dataChangedRequest.emit()

    def getLengthDate(self):
        """
        Возвращает длину списка дат
        """
        return len(self.__Date)

    def addMood(self, mood, index=None):
        """
        Добавляет в модель mood новые значения
        """
        if index == None:
            self.__Mood.append(mood)
        else:
            self.__Mood[index] = mood

    def addMoon(self, moon):
        """
        Добавляет в модель луны новые значения
        """
        self.__Moon.append(moon)

    def setNullModel(self):
        """
        Обунляет модель
        """
        self.__Date = []
        self.__Mood = []
        self.__Moon = []
        self.__RowCount = 1
        self.setNullPhaseRequest.emit()

    def cleanerRow(self):
        """
        Метод проверяет есть ли пустые строки в в конце
        """
        if self.__RowCount > 2:                                          # если строк больше 2х, то удаляем строки и данные из Y и Date
            while self.__Mood[-2] is None and self.__Mood[-1] is None:     # пока встречаются два значения None в Y
                self.__RowCount -= 1
                self.__Date.pop()
                self.__Mood.pop()
                self.__Moon.pop()
                self.cleanPhaseRequest.emit(self.__Date[-1])
                self.rowCountChangedRequest.emit()
                if len(self.__Mood) == 1:
                    break
        if self.__RowCount == 2:                                   # если две строки, то последняя это добавчная, а первая должна быть None
            if self.__Mood[0] is None:                             # в таком случае оставляем одну строку со старыми данными
                self.__RowCount = 1
                self.__Date = [self.__Date[0]]
                self.__Mood = [self.__Mood[0]]
                self.__Moon = [self.__Moon[0]]
                self.rowCountChangedRequest.emit()

