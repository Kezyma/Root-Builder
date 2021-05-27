from PyQt5.QtCore import QCoreApplication, qDebug, qInfo
from PyQt5.QtGui import QIcon
from pathlib import Path
import mobase, os, json, pathlib, shutil

from . import autorootpaths as arp
from . import autorootfiles as arf
from . import autorootmapper as arm
from . import autorootbackup as arb
from . import autorootlinker as arl

class AutoRootTool(mobase.IPluginTool):

    #region Init
    def __init__(self):
        super(AutoRootTool, self).__init__()

    def init(self, organizer):
        qInfo("AutoRootTool: Initialising helpers.")
        self._org = organizer
        self._paths = arp.AutoRootPaths(organizer)
        self._files = arf.AutoRootFiles(organizer, self._paths)
        self._mapper = arm.AutoRootMapper(organizer, self._paths, self._files)
        self._backup = arb.AutoRootBackup(organizer, self._paths, self._files)
        self._linker = arl.AutoRootLinker(organizer, self._paths, self._files)
        self.startingRootExe = False

        qInfo("AutoRootTool: Running.")
        return True
    #endregion

    def version(self):
        return mobase.VersionInfo(0, 0, 1, mobase.ReleaseType.alpha)

    def isActive(self):
        return self._org.pluginSetting("AutoRoot", "enabled")

    def backupEnabled(self):
        return self._org.pluginSetting("AutoRoot", "backup")

    def cacheEnabled(self):
        return self._org.pluginSetting("AutoRoot", "cache")

    def settings(self):
        return []

    def __tr(self, trstr):
        return QCoreApplication.translate("AutoRootTool", trstr)

    def icon(self):
        return QIcon(str(Path(__file__).parent.joinpath("autoroot.ico")))

class AutoRootCleanupTool(AutoRootTool):
    def __init__(self):
        super(AutoRootCleanupTool, self).__init__()

    def name(self):
        return "AutoRoot Cleanup Tool"

    def displayName(self):
        return "AutoRoot/Cleanup"

    def master(self):
        return "AutoRoot"
    
    def author(self):
        return "Kezyma"
    
    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Runs a operation attempting to clear up any broken links in the event of a failed clear on application exit.")

    def __tr(self, trstr):
        return QCoreApplication.translate("AutoRootCleanupTool", trstr)

    def display(self):
        qInfo("AutoRootTool: Starting clear.")

        self._linker.clear()
        self._backup.restore(self.backupEnabled())
        self._mapper.cleanup()
        
        qInfo("AutoRootTool: Clear complete.")
        return

class AutoRootBackupTool(AutoRootTool):
    def __init__(self):
        super(AutoRootBackupTool, self).__init__()
    
    def name(self):
        return "AutoRoot Backup Tool"

    def displayName(self):
        return "AutoRoot/Backup"

    def master(self):
        return "AutoRoot"
    
    def author(self):
        return "Kezyma"
    
    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Runs a backup operation to take a full backup of base game files. (backup and cache must be enabled or this will be cleared on next run)")

    def __tr(self, trstr):
        return QCoreApplication.translate("AutoRootBackupTool", trstr)

    def display(self):
        qInfo("AutoRootTool: Starting backup.")
        self._backup.backup(self.backupEnabled(), self.cacheEnabled())
        qInfo("AutoRootTool: Backup complete.")

        qInfo("AutoRootTool: Clearing temp data.")
        os.remove(self._paths.rootTempPath())
        qInfo("AutoRootTool: Temp data cleared.")
        return

class AutoRootDeleteTool(AutoRootTool):
    def __init__(self):
        super(AutoRootDeleteTool, self).__init__()

    def name(self):
        return "AutoRoot Delete Tool"

    def displayName(self):
        return "AutoRoot/Delete"

    def master(self):
        return "AutoRoot"
    
    def author(self):
        return "Kezyma"
    
    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Deletes any game file backup and cache for the current game.")

    def __tr(self, trstr):
        return QCoreApplication.translate("AutoRootDeleteTool", trstr)

    def display(self):
        if self._paths.rootCachePath().exists():
            qInfo("AutoRootTool: Clearing cache.")
            os.remove(self._paths.rootCachePath())
            qInfo("AutoRootTool: Cache cleared.")

        if self._paths.rootBackupPath().exists():
            qInfo("AutoRootTool: Clearing backup files.")
            shutil.rmtree(self._paths.rootBackupPath())
            qInfo("AutoRootTool: Backup files cleared.")
        return

    