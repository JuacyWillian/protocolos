from datetime import datetime
from os.path import join

from PyQt5.QtCore import pyqtSlot as Slot, Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from app.settings import DESIGN_PATH


class ProtocolDialog(QDialog):
    def __init__(self, parent=None, protocolo=None):
        QDialog.__init__(self, parent, flags=Qt.Window)
        self.ui = loadUi(join(DESIGN_PATH, 'protocoldialog.ui'), self)
        self.ui.inputStart.setDateTime(datetime.now())
        self.ui.inputEnd.setDateTime(datetime.now())
        self.setWindowTitle("Adicionar Protocolo")

        if protocolo:
            self.inputNumber.setText(protocolo.number)
            self.inputNumber.setEnabled(False)
            self.inputStart.setDateTime(protocolo.start)
            self.inputEnd.setDateTime(protocolo.end)
            self.inputReason.setText(protocolo.reason)

    @Slot()
    def on_buttonBox_accepted(self, ):
        self.accept()

    @Slot()
    def on_buttonBox_rejected(self, ):
        self.reject()

    @property
    def number(self, ):
        return self.ui.inputNumber.text()

    @property
    def start(self, ):
        return self.ui.inputStart.dateTime().toPyDateTime()

    @property
    def end(self, ):
        return self.ui.inputEnd.dateTime().toPyDateTime()

    @property
    def reason(self, ):
        return self.ui.inputReason.toPlainText()

    def getData(self, ):
        return (
            self.inputNumber.text(),
            self.inputStart.dateTime().toPyDateTime(),
            self.inputEnd.dateTime().toPyDateTime(),
            self.inputReason.toPlainText(),
        )
