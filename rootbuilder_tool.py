from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from pathlib import Path
from .rootbuilder import RootBuilder
from .rootbuilder_base import RootBuilderBase
import mobase


class RootBuilderTool(RootBuilderBase, mobase.IPluginTool):

    #region Init
    def __init__(self):
        super(RootBuilderTool, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.rootBuilder = RootBuilder(self.organiser)
        return True
    #endregion

    def settings(self):
        return []

    def __tr(self, trstr):
        return QCoreApplication.translate("RootBuilder", trstr)
        
    def master(self):
        return self.baseName()