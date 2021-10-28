from PyQt5.QtCore import QCoreApplication
from .rootbuilder_tool import RootBuilderTool
from .rootbuilder import RootBuilder
from .rootbuilder import RootBuilderBackup
import mobase

class RootBuilderClearCacheTool(RootBuilderTool):
    def __init__(self):
        super(RootBuilderClearCacheTool, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.rootBuilder = RootBuilder(self.organiser)
        self.backup = RootBuilderBackup(self.organiser)
        return True

    def name(self):
        return self.baseName() + " Clear Cache Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Utilities: Clear Cache"

    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Clears the current cache of game file scan results.")

    def __tr(self, trstr):
        return QCoreApplication.translate("RootBuilder", trstr)

    def display(self):
        self.backup.clearCache()
        