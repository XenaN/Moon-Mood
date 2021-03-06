import datetime

from PyQt5.QtCore import pyqtSlot, QDate, QObject
from astral import Astral

'''0 = New Moon
7 = First Quarter
14 = Full Moon
21 = Last Quarter'''


class MoonPhase(QObject):
    """
    Класс отвечающий за соответствие даты и фазы луны
    """
    def __init__(self, in_model, parent=None):
        QObject.__init__(self, parent)
        self._mModel = in_model
        self.astral = Astral()
        self.quarter_phase = []
        self.variantY = [[1.9, 3.8, 5.6, 7.1, 8.3, 9.2, 9.8],
                            [2.2, 4.3, 6.2, 7.8, 9.0, 9.7],
                            [2.6, 5.0, 7.1, 8.7, 9.7],
                            [1.7, 3.4, 5.0, 6.4, 7.7, 8.7, 9.4, 9.8]]

        # связываем событие очищения модели луны и очищение фаз луны
        self._mModel.cleanPhaseRequest.connect(self.cleanPhase)

        # связываем событие пустой первой строки и очищение фаз луны
        self._mModel.setNullPhaseRequest.connect(self.setNullQuarterPhase)

        # связываем событие пустой первой строки и очищение фаз луны
        self._mModel.calculatePhaseRequest.connect(self.calculatePhase)

    @pyqtSlot(QDate)
    def calculatePhase(self, date):
        """
        Метод считает фазы луны по датам
        """
        date = date.toPyDate()
        if self.checkDateinQuarterPhase(date) is False:
            self.checkMoonPhase(date)
        self.checkFirstDay(date)
        self.checkLastDay(date)
        self.fillModelMoon(date)

    @pyqtSlot()
    def setNullQuarterPhase(self):
        """
        Метод вызывается при сбросе данных
        """
        self.quarter_phase = []

    @pyqtSlot(QDate)
    def cleanPhase(self, date):
        """
        Метод удаляет фазы лун
        """
        if date < self.quarter_phase[-2][0]:
            self.quarter_phase.pop()

    def checkDateinQuarterPhase(self, date):
        found = False
        if self.quarter_phase != []:
            for i in range(0, len(self.quarter_phase)):
                if self.quarter_phase[i][0] == date:
                    found = True
        return found


    def checkMoonPhase(self, date):
        """
        Метод проверяет, какие даты соответствуют ровно четвертям
        (новолуние, первая четверть, полнолуние, вторая четверть)
        Записывает их в список quarter_phase
        """
        moon_phase = self.astral.moon_phase(date=date)
        if moon_phase == 0:
            self.quarter_phase.append((date, -10))
        elif moon_phase == 7 or moon_phase == 21:
            self.quarter_phase.append((date, 0))
        elif moon_phase == 14:
            self.quarter_phase.append((date, 10))

    def checkFirstDay(self, first_day):
        """
        Метод проверяет, является ли переданная дата четвертью, если нет, то проверяет ПРЕДЫДУЩУЮ дату,
        пока не найдет четверть. И запишет ее в quarter_phase
        """
        if self.quarter_phase == []:   #  or self.quarter_phase[0][0] != first_day  or self.quarter_phase[-2][0] > first_day
            date = first_day - datetime.timedelta(1)

            moon_phase = self.astral.moon_phase(date=date)
            if moon_phase == 0:
                self.quarter_phase = [(date, -10)] + self.quarter_phase
            elif moon_phase == 7 or moon_phase == 21:
                self.quarter_phase = [(date, 0)] + self.quarter_phase
            elif moon_phase == 14:
                self.quarter_phase = [(date, 10)] + self.quarter_phase
            else:
                self.checkFirstDay(date)

    def checkLastDay(self, last_day):
        """
        Метод проверяет, является ли переданная дата четвертью, если нет, то проверяет СЛЕДУЮЩУЮ дату,
        пока не найдет четверть. И запишет ее в quarter_phase
        """
        if self.quarter_phase[-1][0] < last_day:
            date = last_day + datetime.timedelta(1)
            self.checkMoonPhase(date)
            self.checkLastDay(date)

    def fillModelMoon(self, date):
        """
        Метод заполняет модель Moon
        """
        for j in range(0, len(self.quarter_phase)-1):
            if self.quarter_phase[j][0] < date < self.quarter_phase[j+1][0]:
                length = self.checkLengthQuater(self.quarter_phase[j+1][0], self.quarter_phase[j][0])
                y = date - self.quarter_phase[j][0]
                y = y.days - 1
                side = self.checkSideQuarter(j, length)
                self._mModel.addMoon(side[y])
            elif date == self.quarter_phase[j][0]:
                self._mModel.addMoon(self.quarter_phase[j][1])
            elif date == self.quarter_phase[j+1][0]:
                self._mModel.addMoon(self.quarter_phase[j+1][1])

    def checkLengthQuater(self, date_phase1, date_phase2):
        """
        Метод проверяет, какой длины четверть и возвращает соответствущий индекс списка variantY
        """
        delta = date_phase1 - date_phase2
        delta = delta.days
        if delta == 8:
            return 0
        elif delta == 7:
            return 1
        elif delta == 6:
            return 2
        elif delta == 9:
            return 3

    def checkSideQuarter(self, index_quarter, index_lenght):
        """
        Метод проверяет, направленность кривой луны.
        """
        other_variantY = []
        if self.quarter_phase[index_quarter][1] == 0 and self.quarter_phase[index_quarter+1][1] == 10:
            return self.variantY[index_lenght]
        elif self.quarter_phase[index_quarter][1] == 10 and self.quarter_phase[index_quarter+1][1] == 0:
            other_variantY = self.variantY[index_lenght].copy()
            other_variantY.reverse()
            return other_variantY
        elif self.quarter_phase[index_quarter][1] == 0 and self.quarter_phase[index_quarter+1][1] == -10:
            for i in self.variantY[index_lenght]:
                i = i * -1
                other_variantY.append(i)
            return other_variantY
        elif self.quarter_phase[index_quarter][1] == -10 and self.quarter_phase[index_quarter + 1][1] == 0:
            other_variantY = self.variantY[index_lenght].copy()
            other_variantY.reverse()
            for i in range(0, len(other_variantY)):
                other_variantY[i] = other_variantY[i] * -1
            return other_variantY




# Date = [QDate(2019, 4, 4), QDate(2019, 4, 5), QDate(2019, 4, 6), QDate(2019, 4, 7), QDate(2019, 4, 8),
#         QDate(2019, 4, 9), QDate(2019, 4, 10),
#         QDate(2019, 4, 11), QDate(2019, 4, 12), QDate(2019, 4, 13), QDate(2019, 4, 14), QDate(2019, 4, 15),
#         QDate(2019, 4, 16), QDate(2019, 4, 17), QDate(2019, 4, 18), QDate(2019, 4, 19), QDate(2019, 4, 20),
#         QDate(2019, 4, 21), QDate(2019, 4, 22), QDate(2019, 4, 23), QDate(2019, 4, 24), QDate(2019, 4, 25),
#         QDate(2019, 4, 26), QDate(2019, 4, 27), QDate(2019, 4, 28), QDate(2019, 4, 29), QDate(2019, 4, 30)]
# for date in Date:
#     print(date, calculatePhase(date))

# def calculatePhase(date):
#     day = date.day()
#     month = date.month()
#     year = date.year()
#     ages = [18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
#     offsets = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]
#     description = ["new (totally dark)",
#                    "waxing crescent (increasing to full)",
#                    "in its first quarter (increasing to full)",
#                    "waxing gibbous (increasing to full)",
#                    "full (full light)",
#                    "waning gibbous (decreasing from full)",
#                    "in its last quarter (decreasing from full)",
#                    "waning crescent (decreasing from full)"]
#     if day == 31:
#         day = 1
#     days_into_phase = ((ages[(year + 1) % 19] + ((day + offsets[month - 1]) % 30) + (year < 1900)) % 30)
#     # index = int((days_into_phase + 2) * 16 / 59.0)
#     # if index > 7:
#     #     index = 7
#     # status = description[index]
#
#     light = int(2 * days_into_phase * 100 / 29)
#     if light > 100:
#         light = abs(light - 200)
#
#     return light


# import math, decimal, datetime
# dec = decimal.Decimal
#
#
# def position(date):
#    diff = date - datetime.date(2001, 1, 1)
#    days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
#    lunations = dec("0.20439731") + (days * dec("0.03386319269"))
#
#    return lunations % dec(1)
#
# def phase(pos):
#    index = (pos * dec(8)) + dec("0.5")
#    index = math.floor(index)
#    return {
#       0: "New Moon",
#       1: "Waxing Crescent",
#       2: "First Quarter",
#       3: "Waxing Gibbous",
#       4: "Full Moon",
#       5: "Waning Gibbous",
#       6: "Last Quarter",
#       7: "Waning Crescent"
#    }[int(index) & 7]
# for date in Date:
#     date = date.toPyDate()
#     pos = position(date)
#     phasename = phase(pos)
#
#     roundedpos = round(float(pos), 3)
#     print (date, "%s (%s)" % (phasename, roundedpos))
