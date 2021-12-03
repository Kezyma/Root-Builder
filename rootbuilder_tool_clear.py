from PyQt5.QtCore import QCoreApplication
from .rootbuilder_tool import RootBuilderTool
from .rootbuilder import RootBuilder
from PyQt5.QtGui import QIcon
from pathlib import Path
import mobase

class RootBuilderClearTool(RootBuilderTool):
    def __init__(self):
        super(RootBuilderClearTool, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.rootBuilder = RootBuilder(self.organiser)
        return True

    def name(self):
        return self.baseName() + " Clear Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Clear"
    
    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Runs a clear operation using current settings.")

    def __tr(self, trstr):
        return QCoreApplication.translate("RootBuilder", trstr)

    def icon(self):
        return QIcon(str(Path(__file__).parent.joinpath("ui-minus.ico")))

    def display(self):
        self.rootBuilder.clear()