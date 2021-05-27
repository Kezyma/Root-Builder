from PyQt5.QtCore import QCoreApplication, qDebug, qInfo
from pathlib import Path
from os import listdir
import mobase, os, json, pathlib

class AutoRootFiles():
    #region Init
    def __init__(self, organizer, paths):
        self._org = organizer
        self._paths = paths
        super(AutoRootFiles, self).__init__()
    #endregion

    #region Files
    def getExclusionList(self):
        return [
            "Morrowind.ini", # This can cause problems.
            "Saves", # Don't start fiddling with saves.
            self._paths.gameDataPath() # VFS already handles the data dir
        ]

    def getLinkableExt(self):
        return [
            "dll",
            "exe"
        ]

    def getGameFileList(self):
        qInfo("AutoRoot: Loading game file list.")
        baseFiles = self.getFolderFileList(self._paths.gamePath())

        qInfo("AutoRoot: Excluding invalid files.")
        validFiles = []
        for file in baseFiles:
            exclude = False
            for exc in self.getExclusionList():
                if self._paths.sharedPath(self._paths.gamePath() / exc, file):
                    qInfo("AutoRoot: " + str(file) + " is invalid, excluding.")
                    exclude = True
            if exclude == False:
                qInfo("AutoRoot: " + str(file) + " is valid, including.")
                validFiles.append(file)
        return validFiles

    def getModFileList(self):
        modList = self.getRootModlist()
        validFiles = []
        qInfo("AutoRoot: Finding mod root files.")
        for mod in modList:
            exclude = False
            for exc in self.getExclusionList():
                if (self._paths.modPath() / mod / "Root" / exc).exists():
                    exclude = True
                    qInfo("AutoRoot: " + str(mod) + " is invalid, excluding.")
            if exclude == False:
                qInfo("AutoRoot: " + str(mod) + " is valid, loading files.")
                validFiles.extend(self.getFolderFileList(self._paths.modPath() / mod / "Root"))
        return validFiles

    def getLinkableModFiles(self):
        modFiles = self.getModFileList()
        validFiles = {}
        qInfo("AutoRoot: Finding linkable mod root files.")
        for file in modFiles:
            exclude = True
            for ext in self.getLinkableExt():
                if (str(file).endswith(ext)):
                    exclude = False
            if (exclude == False):
                qInfo("AutoRoot: Found linkable file " + str(file))
                relativePath = str(self._paths.rootRelativePath(str(file)))
                if relativePath in validFiles:
                    validFiles[relativePath] = str(file)
                else:
                    validFiles.update({relativePath:str(file)})
        return validFiles
                
    def getFolderFileList(self, path):
        res = []
        qInfo("AutoRoot: Searching " + str(path))
        for fp in listdir(path):
            afp = path / fp
            if (Path.is_file(afp)):
                qInfo("AutoRoot: Found file " + str(afp))
                res.append(afp)
            if (Path.is_dir(afp)):
                qInfo("AutoRoot: Found dir " + str(afp))
                res.extend(self.getFolderFileList(afp))
        return res

    def getRootModlist(self):
        qInfo("AutoRoot: Loading current modlist.")
        modslist = self._org.modList().allModsByProfilePriority()
        rootMods = []
        for mod in modslist:
            if (self._org.modList().state(mod) & mobase.ModState.active):
                if (self._paths.modPath() / mod / "Root").exists():
                    qInfo("AutoRoot: Found root folder in " + mod)
                    exclude = False
                    for path in self.getExclusionList():
                        if (self._paths.modPath() / mod / "Root" / path).exists():
                            exclude = True
                    if (exclude == False):
                        rootMods.append(mod)
                    else:
                        qInfo("AutoRoot: " + mod + " has invalid root files, skipping.")
        qInfo("AutoRoot: Modlist loaded.")
        return rootMods

    def getRootMappingList(self, modList):
        mappings = []
        for mod in modList:
            rootMapping = mobase.Mapping()
            rootMapping.source = str(self._paths.modPath() / mod / "Root")
            rootMapping.destination = str(self._paths.gamePath())
            rootMapping.isDirectory = True
            rootMapping.createTarget = False
            mappings.append(rootMapping)
            qInfo("AutoRoot: Configured mapping for " + mod)
        return mappings
    #endregion

