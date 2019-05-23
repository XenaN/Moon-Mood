import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *
import cProfile, pstats

from moon_model import MoonModel
from moon_controller import MoonController


if __name__ == '__main__':
    QCoreApplication.setOrganizationName('Xena')
    QCoreApplication.setApplicationName('Moon')

    # pr = cProfile.Profile()
    # pr.enable()

    app = QApplication(sys.argv)
    model = MoonModel()
    controller = MoonController(model)
    controller.openLastFile()
    result = app.exec_()

    # pr.disable()
    # sortby = 'tottime'
    # ps = pstats.Stats(pr).sort_stats(sortby)
    # ps.print_stats()

    sys.exit(result)




