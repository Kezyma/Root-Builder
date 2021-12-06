from PyQt5.QtCore import QCoreApplication
from .rootbuilder_tool import RootBuilderTool
from PyQt5.QtGui import QIcon
from pathlib import Path
import mobase

class RootBuilderSyncTool(RootBuilderTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        return super().init(organiser)

    def name(self):
        return self.baseName() + " Sync Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Sync"

    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Runs a sync operation using current settings.")

    def __tr(self, trstr):
        return QCoreApplication.translate(self.baseName(), trstr)

    def icon(self):
        return QIcon(str(Path(__file__).parent.joinpath("ui-sync.ico")))

    def display(self):
        self.rootBuilder.sync()