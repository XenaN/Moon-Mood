import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *
import cProfile, pstats
from fbs_runtime.application_context import ApplicationContext

from moon_model import MoonModel
from moon_controller import MoonController


if __name__ == '__main__':
    QCoreApplication.setOrganizationName('Xena')
    QCoreApplication.setApplicationName('Moon')

    appctxt = ApplicationContext()

    model = MoonModel()
    controller = MoonController(model)

    result = appctxt.app.exec_()

    sys.exit(result)





