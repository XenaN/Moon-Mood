class MoonModel:
    """
    Класс MoonModel представляет собой реализацию модели данных.

    Модель предоставляет интерфейс, через который можно работать
    с хранимыми значениями.

    Модель содержит методы регистрации, удаления и оповещения
    наблюдателей.
    """

    def __init__(self):
        self._mDate = []  # значения столбца Х
        self._mY = []  # значения столбца Y
        self._mRowCount = 1  # список строк в таблице
        self._mObservers = []  # список наблюдателей

    @property
    def date(self):
        return self._mDate

    @property
    def y(self):
        return self._mY

    @property
    def rowCount(self):
        return self._mRowCount

    @date.setter
    def date(self, list_value):
        self._mDate = list_value

        if self._mRowCount == 1 and self._mY == []:
            self._mY.append(None)
        # self.notifyObservers()

    @y.setter
    def y(self, list_value):
        self._mY = list_value
        print(self._mY)

    def addDate(self):
        self._mRowCount = len(self._mY) + 1

        date = self._mDate.copy()
        b = date[-1].addDays(1)
        self._mDate.append(b)
        self._mY.append(None)

        print(self._mDate, self._mY, self._mRowCount)
        self.notifyObservers()

    def cleanerRow(self):
        if self._mRowCount > 2:
            while self._mY[-2] is None and self._mY[-1] is None:
                self._mRowCount -= 1
                self._mDate.pop()
                self._mY.pop()
                self.notifyObservers()
        if self._mRowCount == 2:
            if self._mY[0] is None:
                self._mRowCount = 1
                self._mDate = [self._mDate[0]]
                self._mY = [self._mY[0]]
                self.notifyObservers()


    def addObserver(self, in_observer):
        self._mObservers.append(in_observer)

    def removeObserver(self, in_observer):
        self._mObservers.remove(in_observer)

    def notifyObservers(self):
        # print('observers')
        for x in self._mObservers:
            x.rowCountChanged()
