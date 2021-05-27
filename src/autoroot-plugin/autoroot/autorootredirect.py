from PyQt5.QtCore import QCoreApplication, qDebug, qInfo
from pathlib import Path
import mobase, os, json, pathlib

class AutoRootRedirect():
    #region Init
    def __init__(self, organizer, paths):
        self._org = organizer
        self._paths = paths
        super(AutoRootRedirect, self).__init__()
    #endregion

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
                    self._org.startApplication(linkedExePath))

                # We're done, close and prevent it from continuing with the original run
                qInfo("AutoRoot: Application closed.")
                self.startingRootExe = False
                return False
            else:
                qInfo("AutoRoot: Could not find game exe, resuming initial launch.")
        # This isn't in a root mod folder, launch it
        return True 
    #endregion