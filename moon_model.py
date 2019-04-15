class MoonModel:
    """
    Класс MoonModel представляет собой реализацию модели данных.

    Модель предоставляет интерфейс, через который можно работать
    с хранимыми значениями.

    Модель содержит методы регистрации, удаления и оповещения
    наблюдателей.
    """

    def __init__(self):
        self.Date = []              # значения столбца даты
        self.Mood = []              # значения столбца Mood
        self.RowCount = 1           # список строк в таблице
        self.Moon = []
        self._mObservers = []       # список наблюдателей

    def addDate(self):
        """
        Метод добавляет еще одну дату, чтобы появилась новая строка с ней
        """
        self.RowCount = len(self.Mood) + 1      # увеличиваем количество строк на одну

        b = self.Date[-1].addDays(1)
        self.Date.append(b)                  # добавляем следующую дату в список Date
        self.Mood.append(None)               # ему же приписываем значение None в Y

        self.notifyObservers()               # оповещаем наблюдателей

    def cleanerRow(self):
        """
        Метод проверяет есть ли пустые строки в в конце
        """
        if self.RowCount > 2:                                          # если строк больше 2х, то удаляем строки и данные из Y и Date
            while self.Mood[-2] is None and self.Mood[-1] is None:     # пока встречаются два значения None в Y
                self.RowCount -= 1
                self.Date.pop()
                self.Mood.pop()
                if len(self.Mood) == 1:
                    break
            self.notifyObservers()
        if self.RowCount == 2:                                   # если две строки, то последняя это добавчная, а первая должна быть None
            if self.Mood[0] is None:                             # в таком случае оставляем одну строку со старыми данными
                self.RowCount = 1
                self.Date = [self.Date[0]]
                self.Mood = [self.Mood[0]]
                self.notifyObservers()

    def addObserver(self, in_observer):
        self._mObservers.append(in_observer)

    def removeObserver(self, in_observer):
        self._mObservers.remove(in_observer)

    def notifyObservers(self):
        for x in self._mObservers:
            x.rowCountChanged()
