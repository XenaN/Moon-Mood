class MoonModel:
    """
    Класс MoonModel представляет собой реализацию модели данных.

    Модель предоставляет интерфейс, через который можно работать
    с хранимыми значениями.

    Модель содержит методы регистрации, удаления и оповещения
    наблюдателей.
    """

    def __init__(self):
        self._mX = []  # значения столбца Х
        self._mY = []  # значения столбца Y
        self._mRowCount = 1  # список строк в таблице
        self._mObservers = []  # список наблюдателей

    @property
    def x(self):
        return self._mX

    @property
    def y(self):
        return self._mY

    @property
    def rowCount(self):
        return self._mRowCount

    @x.setter
    def x(self, list_value):
        self._mX = list_value

        self._mY.append(0)
        print("3x", len(self._mX), len(self._mY))

        self._mRowCount = len(self._mX) + 1
        print("4x", self._mRowCount)
        # if self._mX > self._mY:
        #     self._mRowCount = len(self._mX) + 1
        #     print("4x", self._mRowCount)

        self.notifyObservers()

    @y.setter
    def y(self, list_value):
        self._mY = list_value

        self._mX.append(0)
        print("3y", len(self._mX), len(self._mY))

        self._mRowCount = len(self._mY) + 1
        print("4y", self._mRowCount)

        # if len(self._mY > self._mX:
        #     self._mRowCount = len(self._mY) + 1
        #     print("4y", self._mRowCount)

        self.notifyObservers()

    # def appendToX(self, value):
    #     self._mx.append(value)

    def addObserver(self, in_observer):
        self._mObservers.append(in_observer)

    def removeObserver(self, in_observer):
        self._mObservers.remove(in_observer)

    def notifyObservers(self):
        for x in self._mObservers:
            x.dataChanged()
