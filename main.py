import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from controllers.mainwindow import MainWindow

import models

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
