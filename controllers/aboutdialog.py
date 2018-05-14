from os.path import join
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from settings import DESIGN_PATH, RESOURCE_PATH, DEVELOPERS, LICENSE


class AboutDialog(QDialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(AboutDialog, self).__init__(parent)
        self.ui = loadUi(join(DESIGN_PATH, 'aboutdialog.ui'), self)
        self.ui.lbPixMap.setPixmap(
            QPixmap(join(RESOURCE_PATH, 'tamandua_logo.png')))

        self.ui.lbDevelopers.setText('\n'.join(DEVELOPERS))
        self.ui.lbLicense.setText('\n'.join(LICENSE))

    @Slot(bool)
    def on_btnFechar_clicked(self, ):
        self.close()
