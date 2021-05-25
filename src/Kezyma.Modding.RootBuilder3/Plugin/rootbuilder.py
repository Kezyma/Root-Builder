from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from typing import List
from pathlib import Path
import subprocess
import mobase

class RootBuilderBase(mobase.IPluginTool):
    def __init__(self):
        super(RootBuilderBase, self).__init__()

    def init(self, organizer):
        self.iOrganizer = organizer
        return True

    def modname(self):
        return "Root Builder v3"

    def name(self):
        return self.modname()

    def author(self):
        return "Kezyma"

    def description(self):
        return self.__tr("Enables use of a Root folder to manage base game files.")

    def settings(self):
        return []

    def version(self):
        return mobase.VersionInfo(3, 0, 1, mobase.ReleaseType.alpha)

    def useHashCache(self):
        return self.iOrganizer.pluginSetting(self.modname(), "cache")

    def useRootBackup(self):
        return self.iOrganizer.pluginSetting(self.modname(), "backup")

    def debugMode(self):
        return self.iOrganizer.pluginSetting(self.modname(), "debug")

    def buildArgs(self, mainArg):
        args = [ str(self.exePath()), str(mainArg), "-ini", str(self.iniPath()) ]
        if (self.useHashCache()):
            args.append("-cache")
        if (self.useRootBackup()):
            args.append("-backup")
        if (self.debugMode()):
            args.append("-debug")
        return args
    
    def exePath(self):
        return str(Path(__file__).parent.joinpath("RootBuilder3.exe"))

    def iniPath(self):
        return str(QtWidgets.qApp.property("dataPath")) + "\\ModOrganizer.ini"
        
    def icon(self):
        return QIcon(str(Path(__file__).parent.joinpath("RootBuilder.ico")))

    def __tr(self, str):
        return QCoreApplication.translate("RootBuilder", str)

class RootBuilder(RootBuilderBase):
    def __init__(self):
        super().__init__()

    def displayName(self):
        return "Root Builder/-GUI-"

    def settings(self):
        return [mobase.PluginSetting("cache", "Cache", True),
                mobase.PluginSetting("backup", "Backup", True),
                mobase.PluginSetting("debug", "Debug", False)]

    def tooltip(self):
        return self.__tr("Launches the Root Builder GUI.")

    def display(self):
        return subprocess.call(self.buildArgs("-gui"))

    def __tr(self, str):
       return QCoreApplication.translate("RootBuilder", str) 

class RootBuilderBuild(RootBuilderBase):
    def __init__(self):
        super().__init__()
        
    def init(self, organizer):
        self.iOrganizer = organizer
        return True

    def name(self):
        return "Root Builder v3 - Build"

    def master(self):
        return self.modname()

    def displayName(self):
        return "Root Builder/Build"

    def tooltip(self):
        return self.__tr("Runs a Root build.")

    def display(self):
        return subprocess.call(self.buildArgs("-build"))

    def __tr(self, str):
        return QCoreApplication.translate("RootBuilder", str)

class RootBuilderSync(RootBuilderBase):
    def __init__(self):
        super().__init__()

    def name(self):
        return "Root Builder v3 - Sync"
        
    def master(self):
        return self.modname()

    def displayName(self):
        return "Root Builder/Sync"
        
    def init(self, organizer):
        self.iOrganizer = organizer
        return True

    def tooltip(self):
        return self.__tr("Syncs Root files.")

    def display(self):
        return subprocess.call(self.buildArgs("-sync"))

    def __tr(self, str):
        return QCoreApplication.translate("RootBuilder", str)

class RootBuilderClear(RootBuilderBase):
    def __init__(self):
        super().__init__()
        
    def name(self):
        return "Root Builder v3 - Clear"
        
    def master(self):
        return self.modname()

    def displayName(self):
        return "Root Builder/Clear"
        
    def init(self, organizer):
        self.iOrganizer = organizer
        return True

    def tooltip(self):
        return self.__tr("Syncs and clears Root files.")

    def display(self):
        return subprocess.call(self.buildArgs("-clear"))

    def __tr(self, str):
        return QCoreApplication.translate("RootBuilder", str)
