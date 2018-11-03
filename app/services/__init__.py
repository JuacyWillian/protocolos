from dropbox import dropbox
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode


class BaseBackup():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, ):
        raise NotImplementedError("function 'login' not implemented")

    def logout(self, ):
        raise NotImplementedError("Not Implemented Function")

    def doBackup(self, ):
        raise NotImplementedError("function 'doBackup' not implemented")

    def doRestaurBackup(self, ):
        raise NotImplementedError("function 'doRestaurBackup' not implemented")


class Dropbox(BaseBackup):
    localfile = ''
    backuppath = '/' + localfile
    token = '67cJunbJf4IAAAAAAAAmPBXvssPJ2RmexhOhd6RkBO5JXz3BcVDIOfdI51wqxA8V'

    def login(self, ):
        self.dbox = dropbox.Dropbox(self.token)

    def doBackup(self, ):
        with open(self.localfile, 'rb') as f:
            try:
                self.dbox.files_upload(f.read(),
                                       self.backuppath, mode=WriteMode('overwrite'))
            except ApiError as err:
                # This checks for the specific error where a user doesn't have
                # enough Dropbox space quota to upload this file
                if (err.error.is_path() and
                        err.error.get_path().reason.is_insufficient_space()):
                    print("ERROR: Cannot back up; insufficient space.")
                elif err.user_message_text:
                    print(err.user_message_text)
                else:
                    print(err)


class GoogleDrive(BaseBackup):
    pass


class OneDrive(BaseBackup):
    pass
