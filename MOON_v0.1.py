import sys

from PyQt5.QtWidgets import *

from moon_model import MoonModel
from moon_controller import MoonController


if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = MoonModel()
    controller = MoonController(model)
    sys.exit(app.exec_())
