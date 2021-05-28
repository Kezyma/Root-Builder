from PyQt5.QtCore import QCoreApplication
from .rootbuilder_tool import RootBuilderTool
from .rootbuilder import RootBuilder
import mobase

class RootBuilderClearTool(RootBuilderTool):
    def __init__(self):
        super(RootBuilderClearTool, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.rootBuilder = RootBuilder(self.organiser)
        return True

    def name(self):
        return "RootBuilder Clear Tool"

    def displayName(self):
        return "Root Builder/Clear"

    def master(self):
        return "RootBuilder"
    
    def author(self):
        return "Kezyma"
    
    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Runs a clear operation using current settings.")

    def __tr(self, trstr):
        return QCoreApplication.translate("RootBuilder", trstr)

    def display(self):
        self.rootBuilder.clear()