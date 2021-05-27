from PyQt5.QtCore import QCoreApplication, qDebug, qInfo
import mobase, os, json, pathlib

from . import autorootpaths as arp
from . import autorootfiles as arf
from . import autorootmapper as arm
from . import autorootbackup as arb
from . import autorootlinker as arl

class AutoRoot(mobase.IPluginFileMapper):

    #region Init
    def __init__(self):
        super(AutoRoot, self).__init__()

    def init(self, organizer):
        qInfo("AutoRoot: Initialising helpers.")
        self._org = organizer
        self._paths = arp.AutoRootPaths(organizer)
        self._files = arf.AutoRootFiles(organizer, self._paths)
        self._mapper = arm.AutoRootMapper(organizer, self._paths, self._files)
        self._backup = arb.AutoRootBackup(organizer, self._paths, self._files)
        self._linker = arl.AutoRootLinker(organizer, self._paths, self._files)
        self.startingRootExe = False

        qInfo("AutoRoot: Initialising events.")
        self._org.onAboutToRun(lambda appName: self.build(appName))
        self._org.onFinishedRun(lambda appName, resultCode: self.clear(appName, resultCode))

        qInfo("AutoRoot: Running.")
        return True
    #endregion

    #region Plugin Info
    def name(self):
        return "Auto Root"
    
    def author(self):
        return "Kezyma"
    
    def description(self):
        return self.__tr("Does cool stuff.")
    
    def version(self):
        return mobase.VersionInfo(0, 0, 1, mobase.ReleaseType.alpha)
    #endregion

    #region Plugin Settings
    def settings(self):
        return [
            mobase.PluginSetting("enabled",self.__tr("Enable"),True),
            mobase.PluginSetting("cache",self.__tr("Cache"), True),
            mobase.PluginSetting("backup",self.__tr("Backup"), True)
            ]
    
    def isActive(self):
        return self._org.pluginSetting(self.name(), "enabled")

    def backupEnabled(self):
        return self._org.pluginSetting(self.name(), "backup")

    def cacheEnabled(self):
        return self._org.pluginSetting(self.name(), "cache")
    #endregion

    #region Localisation
    def __tr(self, trstr):
        return QCoreApplication.translate("AutoRoot", trstr)
    #endregion
 
    def mappings(self):
        return self._mapper.mappings()

    def build(self, appName):
        qInfo("AutoRoot: Starting build.")
        res = True
        
        if (self.startingRootExe == False):
            self._backup.backup(self.cacheEnabled(), self.backupEnabled())
            self._linker.build()
            res = self.redirect(appName)
            
        return res

    def clear(self, appName, resultCode):
        qInfo("AutoRoot: Starting clear.")

        self._linker.clear()
        self._backup.restore(self.backupEnabled())
        self._mapper.cleanup()
        
        qInfo("AutoRoot: Clear complete.")
        return

    #region Redirect
    def redirect(self, appName):        
        # Identify if the app is from a root mod folder
        if self._paths.sharedPath(self._paths.modPath(), appName):
            # this is a mod exe, time to redirect
            qInfo("AutoRoot: Mod root exe launch detected, preventing initial launch.")
            self.startingRootExe = True

            # Find path to linked exe in game folder
            fileRootPath = self._paths.rootRelativePath(appName)
            linkedExePath = self._paths.gamePath() / fileRootPath
            # Check that it actually exists in the game folder
            if (linkedExePath.exists()):
                # Launch the new exe file
                qInfo("AutoRoot: Redirecting to " + str(linkedExePath))
                result, exitCode = self._org.waitForApplication(
                    self._org.startApplication(str(linkedExePath)))

                # We're done, close and prevent it from continuing with the original run
                qInfo("AutoRoot: Application closed.")
                self.startingRootExe = False
                return False
            else:
                qInfo("AutoRoot: Could not find game exe, resuming initial launch.")
        # This isn't in a root mod folder, launch it
        return True 
    #endregion