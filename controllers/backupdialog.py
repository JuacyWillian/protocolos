from os.path import join
from enum import Enum

from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from settings import DESIGN_PATH


class BACKUP_SERVICES(Enum):
    DROPBOX = "dropbox"
    GOOGLE_DRIVE = "gdrive"
    ONE_DRIVE = "onedrive"


class BackupDialog(QDialog):
    def __init__(self, parent=None, title="", ):
        super(BackupDialog, self).__init__(parent)
        self.ui = loadUi(join(DESIGN_PATH, 'backupdialog.ui'), self)
        self.setWindowTitle(title)
        if title:
            self.ui.lbTitle.setText(title)

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    @property
    def email(self, ):
        return self.ui.editUsername.text()

    @property
    def password(self, ):
        return self.ui.editPassword.text()

    @property
    def service(self, ):
        if self.ui.radioDropbox.isChecked():
            return BACKUP_SERVICES.DROPBOX

        if self.ui.radioGDrive.isChecked():
            return BACKUP_SERVICES.GOOGLE_DRIVE

        if self.ui.radioOneDrive.isChecked():
            return BACKUP_SERVICES.ONE_DRIVE
