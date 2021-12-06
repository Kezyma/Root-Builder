from PyQt5.QtCore import QCoreApplication
from .rootbuilder_tool import RootBuilderTool
from PyQt5.QtGui import QIcon
from pathlib import Path
import mobase

class RootBuilderBuildTool(RootBuilderTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        return super().init(organiser)

    def name(self):
        return self.baseName() + " Build Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Build"

    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Runs a build operation using the current settings.")

    def __tr(self, trstr):
        return QCoreApplication.translate(self.baseName(), trstr)

    def icon(self):
        return QIcon(str(Path(__file__).parent.joinpath("ui-plus.ico")))

    def display(self):
        self.rootBuilder.build()