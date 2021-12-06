from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from pathlib import Path
from .rootbuilder import RootBuilder
from .rootbuilder_base import RootBuilderBase
import mobase


class RootBuilderTool(RootBuilderBase, mobase.IPluginTool):

    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        return super().init(organiser)

    def settings(self):
        return []

    def __tr(self, trstr):
        return QCoreApplication.translate(self.baseName(), trstr)
        
    def master(self):
        return self.baseName()