from PyQt5.QtCore import QCoreApplication, qDebug, qInfo
from pathlib import Path
import mobase, os, json, pathlib

class AutoRootPaths():
    #region Init
    def __init__(self, organizer):
        self._org = organizer
        super(AutoRootPaths, self).__init__()
    #endregion

    #region Paths
    _gP = str()
    def gamePath(self):
        if self._gP == str():
            self._gP = Path(self._org.managedGame().gameDirectory().path())
        return Path(self._gP)

    _gDp = str()
    def gameDataPath(self):
        if self._gDp == str():
            self._gDp = pathlib.PurePath(Path(self._org.managedGame().dataDirectory().path())).name
        return Path(self._gDp)

    _mP = str()
    def modPath(self):
        if self._mP == str():
            self._mP = Path(self._org.modsPath())
        return Path(self._mP)

    _rOp = str()
    def rootOverwritePath(self):
        if self._rOp == str():
            self._rOp = Path(self._org.overwritePath()) / "Root"
        return Path(self._rOp)
    
    _pDp = str()
    def pluginDataPath(self):
        if self._pDp == str():
            self._pDp = Path(self._org.pluginDataPath()) / "autorootdata"
        if not Path(self._pDp).exists():
            os.makedirs(self._pDp)
        return Path(self._pDp)

    def rootRelativePath(self, path):
        return Path(path[(str(os.path.abspath(path)).lower().find(os.path.sep + "root") + 6):])
    
    def gameRelativePath(self, path):
        return Path(str(os.path.abspath(path)).replace(str(os.path.abspath(self.gamePath())), "")[1:])

    _rBp = str()
    def rootBackupPath(self):
        if self._rBp == str():
            self._rBp = self.pluginDataPath() / self.safePathName(self.gamePath())
        if not Path(self._rBp).exists():
            os.makedirs(self._rBp)
        return Path(self._rBp)

    _rCp = str()
    def rootCachePath(self):
        if self._rCp == str():
            self._rCp = self.pluginDataPath() / Path(self.safePathName(self.gamePath()) + ".json")
        return Path(self._rCp)

    _rTp = str()
    def rootTempPath(self):
        if self._rTp == str():
            self._rTp = self.pluginDataPath() / Path("RootBuilderTempData.json")
        return Path(self._rTp)

    _lTp = str()
    def linkTempPath(self):
        if self._lTp == str():
            self._lTp = self.pluginDataPath() / Path("RootBuilderLinkData.json")
        return Path(self._lTp)
    
    def safePathName(self, path):
        return "_".join(os.path.normpath(path).split(os.path.sep)).replace(":", "").replace(" ", "_")

    def sharedPath(self, basePath, childPath):
        if os.path.commonpath([os.path.abspath(basePath), os.path.abspath(childPath)]) == os.path.commonpath([os.path.abspath(basePath)]):
            return True
        return False
    #endregion

