from PyQt5.QtCore import QCoreApplication
from pathlib import Path
import mobase, pathlib, os

class RootBuilderPaths():
    """ Root Builder path module. Used to load various paths for the plugin. """

    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        super(RootBuilderPaths, self).__init__()

    _gamePath = str()
    def gamePath(self):
        """ Gets the path to the current game folder. """
        if self._gamePath == str():
            self._gamePath = self.organiser.managedGame().gameDirectory().path()
        return Path(self._gamePath)

    _modsPath = str()
    def modsPath(self):
        """ Gets the path to the current mod folder. """
        if self._modsPath == str():
            self._modsPath = self.organiser.modsPath()
        return Path(self._modsPath)

    _gameDataDir = str()
    def gameDataDir(self):
        """ Gets the name of the data directory for the current game. """
        if self._gameDataDir == str():
            self._gameDataDir = pathlib.PurePath(Path(self.organiser.managedGame().dataDirectory().path())).name
        return self._gameDataDir

    _rootOverwritePath = str()
    def rootOverwritePath(self):
        """ Gets the path to root folder from within the overwrite folder. """
        if self._rootOverwritePath == str():
            self._rootOverwritePath = Path(self.organiser.overwritePath()) / "Root"
        return Path(self._rootOverwritePath)

    _pluginDataPath = str()
    def pluginDataPath(self):
        """ Gets the path to the data folder for this plugin. """
        if self._pluginDataPath == str():
            self._pluginDataPath = Path(self.organiser.pluginDataPath()) / "rootbuilder"
        if not Path(self._pluginDataPath).exists():
            os.makedirs(self._pluginDataPath)
        return Path(self._pluginDataPath)

    _rootBackupPath = str()
    def rootBackupPath(self):
        """ Gets the path to the backup folder for the current game. """
        if self._rootBackupPath == str():
            self._rootBackupPath = self.rootBuilderGameDataPath() / "backup"
        if not Path(self._rootBackupPath).exists():
            os.makedirs(self._rootBackupPath)
        return Path(self._rootBackupPath)

    _rootBuilderGameDataPath = str()
    def rootBuilderGameDataPath(self):
        """ Gets the path to the RootBuilder data folder for the current game. """
        if self._rootBuilderGameDataPath == str():
            self._rootBuilderGameDataPath = self.pluginDataPath() / self.safeGamePathName()
        if not Path(self._rootBuilderGameDataPath).exists():
            os.makedirs(self._rootBuilderGameDataPath)
        return Path(self._rootBuilderGameDataPath)

    _rootCacheFilePath = str()
    def rootCacheFilePath(self):
        """ Gets the path to the cache file for the current game. """
        if self._rootCacheFilePath == str():
            self._rootCacheFilePath = self.rootBuilderGameDataPath() / Path("RootBuilderCacheData.json")
        return Path(self._rootCacheFilePath)

    _rootBackupDataFilePath = str()
    def rootBackupDataFilePath(self):
        """ Gets the path to the current backup data file. """
        if self._rootBackupDataFilePath == str():
            self._rootBackupDataFilePath = self.rootBuilderGameDataPath() / Path("RootBuilderBackupData.json")
        return Path(self._rootBackupDataFilePath)

    _rootModDataFilePath = str()
    def rootModDataFilePath(self):
        """ Gets the path to the current mod data file. """
        if self._rootModDataFilePath == str():
            self._rootModDataFilePath = self.rootBuilderGameDataPath() / Path("RootBuilderModData.json")
        return Path(self._rootModDataFilePath)

    _rootLinkDataFilePath = str()
    def rootLinkDataFilePath(self):
        """ Gets the path to the current link data file. """
        if self._rootLinkDataFilePath == str():
            self._rootLinkDataFilePath = self.rootBuilderGameDataPath() / Path("RootBuilderLinkData.json")
        return Path(self._rootLinkDataFilePath)

    _safeGamePathName = str()
    def safeGamePathName(self):
        """ Gets a file safe string representing the current game install. """
        if self._safeGamePathName == str():
            self._safeGamePathName = self.safePathName(self.gamePath())
        return self._safeGamePathName

    def rootRelativePath(self, path):
        """ Gets the part of a path relative to the Root folder. """
        return Path(str(path)[(str(os.path.abspath(Path(path))).lower().find(os.path.sep + "root") + 6):])
    
    def gameRelativePath(self, path):
        """ Gets the part of a path relative to the current game folder. """
        return Path(str(os.path.abspath(Path(path))).replace(str(os.path.abspath(self.gamePath())), "")[1:])

    def safePathName(self, path):
        """ Gets a file safe string representing a specific path. """
        return "_".join(os.path.normpath(path).split(os.path.sep)).replace(":", "").replace(" ", "_")

    def sharedPath(self, basePath, childPath):
        """ Determines whether one path is a child of another path. """       
        if os.path.commonpath([os.path.abspath(basePath), os.path.abspath(childPath)]) == os.path.commonpath([os.path.abspath(basePath)]):
            return True
        return False