from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from pathlib import Path
from .rootbuilder import RootBuilder
import mobase

class RootBuilderTool(mobase.IPluginTool):

    #region Init
    def __init__(self):
        super(RootBuilderTool, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.rootBuilder = RootBuilder(self.organiser)
        return True
    #endregion

    def version(self):
        return mobase.VersionInfo(4, 0, 1, mobase.ReleaseType.alpha)

    def isActive(self):
        return self.rootBuilder.settings.enabled()

    def settings(self):
        return []

    def __tr(self, trstr):
        return QCoreApplication.translate("RootBuilder", trstr)

    def icon(self):
        return QIcon(str(Path(__file__).parent.joinpath("rootbuilder.ico")))