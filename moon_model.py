class MoonModel:
    """
    Класс MoonModel представляет собой реализацию модели данных.

    Модель предоставляет интерфейс, через который можно работать
    с хранимыми значениями.

    Модель содержит методы регистрации, удаления и оповещения
    наблюдателей.
    """

    def __init__(self):
        self.Date = []  # значения столбца Х
        self.Y = []  # значения столбца Y
        self.RowCount = 1  # список строк в таблице
        self._mObservers = []  # список наблюдателей

    def addDate(self):
        self.RowCount = len(self.Y) + 1

        date = self.Date.copy()
        b = date[-1].addDays(1)
        self.Date.append(b)
        self.Y.append(None)

        self.notifyObservers()

    def cleanerRow(self):
        # есть баг с удалением строк вначале таблицы
        if self.RowCount > 2:
            while self.Y[-2] is None and self.Y[-1] is None:
                self.RowCount -= 1
                self.Date.pop()
                self.Y.pop()
                # print(self.Date, self.Y, self.RowCount)
                self.notifyObservers()
        if self.RowCount == 2:
            if self.Y[0] is None:
                self.RowCount = 1
                self.Date = [self.Date[0]]
                self.Y = [self.Y[0]]
                self.notifyObservers()


    def addObserver(self, in_observer):
        self._mObservers.append(in_observer)

    def removeObserver(self, in_observer):
        self._mObservers.remove(in_observer)

    def notifyObservers(self):
        # print('observers')
        for x in self._mObservers:
            x.rowCountChanged()
