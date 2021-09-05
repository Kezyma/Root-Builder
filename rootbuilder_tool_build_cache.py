from PyQt5.QtCore import QCoreApplication
from .rootbuilder_tool import RootBuilderTool
from .rootbuilder import RootBuilder
from .rootbuilder import RootBuilderBackup
import mobase

class RootBuilderBuildCacheTool(RootBuilderTool):
    def __init__(self):
        super(RootBuilderBuildCacheTool, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.rootBuilder = RootBuilder(self.organiser)
        self.backup = RootBuilderBackup(self.organiser)
        return True

    def name(self):
        return self.baseName() + " Build Cache Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Utilities: Build Cache"

    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Scans and caches results if no cache already exists.")

    def __tr(self, trstr):
        return QCoreApplication.translate("RootBuilder", trstr)

    def display(self):
        self.backup.buildCache()
        