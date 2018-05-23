import sys
from datetime import datetime
from enum import Enum
from os.path import join

from PyQt5.QtCore import pyqtProperty as Property
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtWidgets import (QApplication, QDialog, QListWidgetItem,
                             QMainWindow, QTableWidget)
from PyQt5.uic import loadUi

from controllers.protocoldialog import ProtocolDialog
from controllers.confirmdialog import ConfirmDialog
from controllers.aboutdialog import AboutDialog
from models import Protocolo
from settings import DESIGN_PATH


class MyQListWidgetItem(QListWidgetItem):
    def __init__(self, protocolo, *args, **kwargs):
        QListWidgetItem.__init__(self, *args, **kwargs)
        self.protocolo = protocolo
        self.setText(self.protocolo.start.strftime("%c"))


class MainWindow(QMainWindow):
    _protocolo = None
    changeProtocolo = Signal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = loadUi(join(DESIGN_PATH, 'main_window.ui'), self)
        self.load_items()
        self.changeProtocolo.connect(self.protocoloChanged)

    def protocoloChanged(self, *args):
        self.updateDetails()

    def updateDetails(self, ):
        self.ui.lbNumber.setText(self.protocolo.number)
        self.ui.lbStart.setText(self.protocolo.start.strftime('%c'))
        self.ui.lbEnd.setText(self.protocolo.end.strftime('%c'))
        self.ui.lbReason.setText(self.protocolo.reason)

    def clearDetails(self, ):
        self.ui.lbNumber.setText('')
        self.ui.lbStart.setText('')
        self.ui.lbEnd.setText('')
        self.ui.lbReason.setText('')

    @property
    def protocolo(self, ):
        return self._protocolo

    @protocolo.setter
    def protocolo(self, v):
        if isinstance(v, Protocolo):
            if v != self._protocolo:
                pass
            self._protocolo = v
            self.changeProtocolo.emit()

    def load_items(self, ):
        self.ui.listProtocolo.clear()

        for p in Protocolo.getAll():
            self.ui.listProtocolo.addItem(MyQListWidgetItem(p))

    def on_listProtocolo_itemClicked(self, item: QListWidgetItem):
        self.protocolo = Protocolo.getByNumber(item.protocolo.number)

    @Slot(bool)
    def on_btnNew_clicked(self, ):
        self.novoProtocolo()

    @Slot(bool)
    def on_btnEdit_clicked(self, ):
        if not self.protocolo:
            return
        pd = ProtocolDialog(self, protocolo=self.protocolo)
        result = pd.exec_()

        if result == QDialog.Accepted:
            self.protocolo.number = pd.number
            self.protocolo.start = pd.start
            self.protocolo.end = pd.end
            self.protocolo.reason = pd.reason
            self.protocolo.update()
            self.load_items()
            self.clearDetails()

    @Slot(bool)
    def on_btnRemove_clicked(self, ):
        if not self.protocolo:
            return

        cd = ConfirmDialog(self, "Tem certeza que quer Excluir este item?")
        if cd.exec_() == QDialog.Accepted:
            self.protocolo.remove()

            self.protocolo = None
            self.load_items()
            self.clearDetails()

    @Slot()
    def on_actionNovo_triggered(self, ):
        self.novoProtocolo()

    def novoProtocolo(self, ):
        pd = ProtocolDialog(self)
        result = pd.exec_()

        if result == QDialog.Accepted:
            self.protocolo = Protocolo(*pd.getData())
            self.protocolo.insert()
        self.load_items()

    @Slot()
    def on_actionRealizarBackup_triggered(self, ):
        print("salvando backup")

    @Slot()
    def on_actionRestaurarBackup_triggered(self, ):
        print("restaurando backup")

    @Slot()
    def on_actionSobre_triggered(self, ):
        aboutDialog = AboutDialog()
        aboutDialog.exec_()

    @Slot()
    def on_actionFechar_triggered(self, ):
        self.close()
