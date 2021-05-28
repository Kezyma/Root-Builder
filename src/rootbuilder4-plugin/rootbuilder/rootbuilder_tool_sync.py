from PyQt5.QtCore import QCoreApplication
from .rootbuilder_tool import RootBuilderTool
from .rootbuilder import RootBuilder
import mobase

class RootBuilderSyncTool(RootBuilderTool):
    def __init__(self):
        super(RootBuilderSyncTool, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.rootBuilder = RootBuilder(self.organiser)
        return True

    def name(self):
        return "RootBuilder Sync Tool"

    def displayName(self):
        return "RootBuilder/Sync"

    def master(self):
        return "RootBuilder"
    
    def author(self):
        return "Kezyma"
    
    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Runs a sync operation using current settings.")

    def __tr(self, trstr):
        return QCoreApplication.translate("RootBuilder", trstr)

    def display(self):
        self.rootBuilder.sync()