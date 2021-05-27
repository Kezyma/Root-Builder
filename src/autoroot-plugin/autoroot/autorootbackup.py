from PyQt5.QtCore import QCoreApplication, qDebug, qInfo
from pathlib import Path
from shutil import copy2
import mobase, os, json, pathlib, shutil, hashlib

class AutoRootBackup():
    #region Init
    def __init__(self, organizer, paths, files):
        self._org = organizer
        self._paths = paths
        self._files = files
        super(AutoRootBackup, self).__init__()
    #endregion

    #region Backup
    def backup(self, backup, cache):
        backupFiles = []
        gameFiles = self._files.getGameFileList()
        gameHashes = []
        updateCache = False

        if (backup == True):
            qInfo("AutoRoot: Backup enabled, adding all game files.")
            backupFiles.extend(gameFiles)
        else:
            qInfo("AutoRoot: Backup disabled, identifying conflicts.")
            modFiles = self._files.getLinkableModFiles().values()
            for modFile in modFiles:
                relativePath = self._paths.rootRelativePath(modFile)
                existingPath = self._paths.gamePath() / relativePath
                if (existingPath.exists()):
                    qInfo("AutoRoot: Found conflict, adding " + str(modFile))
                    backupFiles.append(existingPath)
            
        qInfo("AutoRoot: Loading game file data.")
        gameFileData = {}
        if (cache == True and self._paths.rootCachePath().exists()):
            qInfo("AutoRoot: Cache exists, loading.")
            gameFileData = json.load(open(self._paths.rootCachePath()))
            qInfo("AutoRoot: Cache loaded.")
        else:
            updateCache = cache
            for file in gameFiles:
                qInfo("AutoRoot: Hashing " + str(file))
                gameFileData.update({str(file):str(self.hashFile(file))})
            
        qInfo("AutoRoot: Backing up files")
        for file in backupFiles:
            relativePath = self._paths.gameRelativePath(file)
            backupPath = self._paths.rootBackupPath() / relativePath
            if (backupPath.exists()):
                fileHash = self.hashFile(file)
                if str(file) not in gameFileData or fileHash != gameFileData[str(file)]:
                    qInfo("AutoRoot: File has changed, updating backup " + str(file))
                    gameFileData[str(file)] = fileHash
                    copy2(str(file), str(backupPath))
                    updateCache = cache
            else:
                qInfo("AutoRoot: Backing up " + str(file))
                if not os.path.exists(os.path.dirname(backupPath)):
                    os.makedirs(os.path.dirname(backupPath))
                copy2(str(file), str(backupPath))

        if cache == True & updateCache == True:
            qInfo("AutoRoot: Updating cache.")
            if not self._paths.rootCachePath().exists():
                self._paths.rootCachePath().touch()
            with open(self._paths.rootCachePath(), "w") as jsonFile:
                json.dump(gameFileData, jsonFile)
            qInfo("AutoRoot: Cache updated.")

        if cache == False and self._paths.rootCachePath().exists():
            qInfo("AutoRoot: Clearing cache.")
            os.remove(self._paths.rootCachePath())
            qInfo("AutoRoot: Cache cleared.")

        qInfo("AutoRoot: Saving temp data.")
        if not self._paths.rootTempPath().exists():
            self._paths.rootTempPath().touch()
        with open(self._paths.rootTempPath(), "w") as jsonFile:
            json.dump(gameFileData, jsonFile)
        qInfo("AutoRoot: Temp data saved.")
        return

    def restore(self, backup):
        qInfo("AutoRoot: Restoring files.")

        gameFiles = self._files.getGameFileList()
        tempData = json.load(open(self._paths.rootTempPath()))

        for gameFile in gameFiles:
            if str(gameFile) in tempData:
                if tempData[str(gameFile)] != self.hashFile(gameFile):
                    qInfo("AutoRoot: File has changed " + str(gameFile))
                    relativePath = self._paths.gameRelativePath(gameFile)
                    backupPath = self._paths.rootBackupPath() / relativePath
                    if backupPath.exists():
                        qInfo("AutoRoot: Moving " + str(gameFile) + " to overwrite.")
                        copy2(gameFile, self._paths.rootOverwritePath() / self._paths.gameRelativePath(gameFile))
                        qInfo("AutoRoot: Moved " + str(gameFile) + " to overwrite.")
                        qInfo("AutoRoot: Restoring " + str(gameFile) + " from backup.")
                        copy2(backupPath, gameFile)
                        qInfo("AutoRoot: Restored " + str(gameFile) + " from backup.")
                    else:
                        qInfo("AutoRoot: No backup exists for " + str(gameFile))
            else:
                qInfo("AutoRoot: New file found " + str(gameFile) + " moving to overwrite.")
                shutil.move(gameFile, self._paths.rootOverwritePath() / self._paths.gameRelativePath(gameFile))
                qInfo("AutoRoot: Moved " + str(gameFile) + " to overwrite.")

        for tempFile in tempData.keys():
            if not Path(tempFile).exists():
                qInfo("AutoRoot: File missing " + str(tempFile))
                relativePath = self._paths.gameRelativePath(Path(tempFile))
                backupPath = self._paths.rootBackupPath() / relativePath
                if backupPath.exists():
                    qInfo("AutoRoot: Backup exists, restoring " + str(tempFile))
                    copy2(backupPath, Path(tempFile))
                    qInfo("AutoRoot: Restored " + str(tempFile) + " from backup.")
        
        if backup == False and self._paths.rootBackupPath().exists():
            qInfo("AutoRoot: Clearing backup files.")
            shutil.rmtree(self._paths.rootBackupPath())
            qInfo("AutoRoot: Backup files cleared.")

        qInfo("AutoRoot: Clearing temp data.")
        os.remove(self._paths.rootTempPath())
        qInfo("AutoRoot: Temp data cleared.")
        return

    def hashFile(self, path):
        func = getattr(hashlib, 'md5')()
        f = os.open(path, (os.O_RDWR | os.O_BINARY))
        for block in iter(lambda: os.read(f, 2048*func.block_size), b''):
            func.update(block)
        os.close(f)
        return func.hexdigest()

    #endregion