from os.path import join

from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
from PyQt5.QtWidgets import (QDialog, QListWidgetItem,
                             QMainWindow)
from PyQt5.uic import loadUi

from app.controllers.aboutdialog import AboutDialog
from app.controllers.backupdialog import BackupDialog
from app.controllers.confirmdialog import ConfirmDialog
from app.controllers.protocoldialog import ProtocolDialog
from app.models import Protocolo
from app.services import Dropbox, GoogleDrive, OneDrive
from app.settings import DESIGN_PATH

SERVICES = {
    "dropbox": Dropbox,
    "gdrive": GoogleDrive,
    "onedrive": OneDrive,
}


class MyQListWidgetItem(QListWidgetItem):
    def __init__(self, protocolo, ):
        QListWidgetItem.__init__(self, )
        self.protocolo = protocolo
        self.setText(self.protocolo.start.strftime("%c"))


class MainWindow(QMainWindow):
    _protocolo = None
    changeProtocolo = Signal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        path = join(DESIGN_PATH, 'main_window.ui')
        self.ui = loadUi(path, self)
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

    def on_listProtocolo_itemClicked(self, item: MyQListWidgetItem):
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
        backupDialog = BackupDialog(self, title="Realizar Backup")
        if backupDialog.exec_() == QDialog.Accepted:
            username = backupDialog.email
            password = backupDialog.password
            __service = SERVICES[backupDialog.service.value]

            service = __service(username, password)
            service.doBackup()

    @Slot()
    def on_actionRestaurarBackup_triggered(self, ):
        backupDialog = BackupDialog(self, title="Restaurar Backup")
        if backupDialog.exec_() == QDialog.Accepted:
            username = backupDialog.email
            password = backupDialog.password
            __service = SERVICES[backupDialog.service.value]

            service = __service(username, password)
            service.doRestaurBackup()

    @Slot()
    def on_actionSobre_triggered(self, ):
        aboutDialog = AboutDialog(self)
        aboutDialog.exec_()

    @Slot()
    def on_actionFechar_triggered(self, ):
        self.close()
