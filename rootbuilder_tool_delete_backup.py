from PyQt5.QtCore import QCoreApplication
from .rootbuilder_tool import RootBuilderTool
from .rootbuilder import RootBuilder
from .rootbuilder import RootBuilderBackup
import mobase

class RootBuilderDeleteBackupTool(RootBuilderTool):
    def __init__(self):
        super(RootBuilderDeleteBackupTool, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.rootBuilder = RootBuilder(self.organiser)
        self.backup = RootBuilderBackup(self.organiser)
        return True

    def name(self):
        return self.baseName() + " Delete Backup Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Utilities: Delete Backup"

    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Deletes the current set of backup files.")

    def __tr(self, trstr):
        return QCoreApplication.translate("RootBuilder", trstr)

    def display(self):
        self.backup.clearBackupFiles()
