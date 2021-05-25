from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from typing import List
from pathlib import Path
import subprocess

class RootBuilderBase(mobase.IPluginTool):
    def __init__(self):
        super(RootBuilderBase, self).__init__()

    def init(self, organizer):
        self.iOrganizer = organizer
        return True

    def name(self):
        return "Kezyma's Root Builder v3"

    def author(self):
        return "Kezyma"

    def description(self):
        return self.__tr("Enables use of a Root folder to manage base game files.")

    def version(self):
        return mobase.VersionInfo(3, 0, 1, mobase.ReleaseType.alpha)

    def settings(self):
        return [mobase.PluginSetting("cache", "Cache", True),
                mobase.PluginSetting("backup", "Backup", True),
                mobase.PluginSetting("debug", "Debug", True)]

    def useHashCache(self):
        return self.iOrganizer.pluginSetting(self.name(), "cache")

    def useRootBackup(self):
        return self.iOrganizer.pluginSetting(self.name(), "backup")

    def debugMode(self):
        return self.iOrganizer.pluginSetting(self.name(), "debug")

    def exePath(self):
        return str(self.iOrganizer.basePath()) + "\\plugins\\RootBuilder3.exe"

    def buildArgs(self, mainArg):
        args = [ str(self.exePath()), str(mainArg), "-ini", str(self.iniPath()) ]
        if (self.useHashCache()):
            args.append("-cache")
        if (self.useRootBackup()):
            args.append("-backup")
        if (self.debugMode()):
            args.append("-debug")
        return args

    def iniPath(self):
        return self.iOrganizer.basePath() + "\\ModOrganizer.ini"
        
    def icon(self):
        return QIcon("plugins\\RootBuilder.ico")

    def __tr(self, str):
        return QCoreApplication.translate("RootBuilder", str)

class RootBuilder(RootBuilderBase):
    def __init__(self):
        super(RootBuilder, self).__init__()

    def displayName(self):
        return "Root Builder/-GUI-"

    def tooltip(self):
        return self.__tr("Launches the Root Builder GUI.")

    def display(self):
        return subprocess.call(self.buildArgs("-gui"))

    def __tr(self, str):
       return QCoreApplication.translate("RootBuilder", str) 

class RootBuilderBuild(RootBuilderBase):
    def __init__(self):
        super(RootBuilderBuild, self).__init__()

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
        super(RootBuilderSync, self).__init__()

    def displayName(self):
        return "Root Builder/Sync"

    def tooltip(self):
        return self.__tr("Syncs Root files.")

    def display(self):
        return subprocess.call(self.buildArgs("-sync"))

    def __tr(self, str):
        return QCoreApplication.translate("RootBuilder", str)

class RootBuilderClear(RootBuilderBase):
    def __init__(self):
        super(RootBuilderClear, self).__init__()

    def displayName(self):
        return "Root Builder/Clear"

    def tooltip(self):
        return self.__tr("Syncs and clears Root files.")

    def display(self):
        return subprocess.call(self.buildArgs("-clear"))

    def __tr(self, str):
        return QCoreApplication.translate("RootBuilder", str)

def createPlugins() -> List[mobase.IPlugin]:
    return [RootBuilder(), RootBuilderBuild(), RootBuilderSync(), RootBuilderClear()]
