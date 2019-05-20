import sys

from PyQt5.QtWidgets import *
import cProfile, pstats

from moon_model import MoonModel
from moon_controller import MoonController


def startMoon():
    """
    Для работы с программой
    """

    pr = cProfile.Profile()
    pr.enable()
    app = QApplication(sys.argv)
    model = MoonModel()
    controller = MoonController(model)

    result = app.exec_()

    pr.disable()
    sortby = 'tottime'
    # ps = pstats.Stats(pr).strip_dirs().sort_stats(sortby)
    ps = pstats.Stats(pr).sort_stats(sortby)
    ps.print_stats()

    sys.exit(result)

if __name__ == '__main__':
    startMoon()





