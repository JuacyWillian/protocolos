from os.path import join

from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from app.settings import DESIGN_PATH


class ConfirmDialog(QDialog):
    def __init__(self, parent=None, msg=None, ):
        super(ConfirmDialog, self).__init__(parent)
        self.ui = loadUi(join(DESIGN_PATH, 'confirmdialog.ui'), self)
        self.ui.lbMessage.setText(msg)

    @Slot(bool)
    def on_btnOk_clicked(self, ):
        self.accept()

    @Slot(bool)
    def on_btnCancel_clicked(self, ):
        self.reject()
