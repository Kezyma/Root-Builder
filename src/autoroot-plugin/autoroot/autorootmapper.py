from PyQt5.QtCore import QCoreApplication, qDebug, qInfo
from pathlib import Path
import mobase, os, json, pathlib

class AutoRootMapper():
    #region Init
    def __init__(self, organizer, paths, files):
        self._org = organizer
        self._paths = paths
        self._files = files
        super(AutoRootMapper, self).__init__()
    #endregion

    #region Mapping
    def mappings(self):
        qInfo("AutoRoot: Building root mappings.")

        if not self._paths.rootOverwritePath().exists():
            qInfo("AutoRoot: Creating root overwrite folder.")
            os.mkdir(self._paths.rootOverwritePath())

        qInfo("AutoRoot: Generating mod root mappings.")
        rootModsList = self._files.getRootModlist()
        rootMappingList = self._files.getRootMappingList(rootModsList)

        qInfo("AutoRoot: Configuring root overwrite.")
        overwriteMap = mobase.Mapping()
        overwriteMap.source = str(self._paths.rootOverwritePath())
        overwriteMap.destination = str(self._paths.gamePath())
        overwriteMap.isDirectory = True
        overwriteMap.createTarget = True
        rootMappingList.append(overwriteMap)

        qInfo("AutoRoot: Mapping configuration complete.")
        return rootMappingList

    def cleanup(self):
        if self._paths.rootOverwritePath().exists():
            if len(os.listdir(self._paths.rootOverwritePath())) == 0:
                os.rmdir(self._paths.rootOverwritePath())
        return
    #endregion