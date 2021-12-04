from shutil import copy2
from pathlib import Path
from .rootbuilder_settings import RootBuilderSettings
from .rootbuilder_paths import RootBuilderPaths
from .rootbuilder_files import RootBuilderFiles
import mobase, os, hashlib, json, shutil, stat
from PyQt5.QtCore import QCoreApplication, qInfo

class RootBuilderBackup():
    """ Root Builder backup module. Used to back up and restore vanilla game installations. """

    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.settings = RootBuilderSettings(self.organiser)
        self.paths = RootBuilderPaths(self.organiser)
        self.files = RootBuilderFiles(self.organiser)
        super(RootBuilderBackup, self).__init__()

    def backup(self):
        """ Backs up base game files, or conflicts if backup is disabled. """
        # Get hashes for our current vanilla game install
        fileData = self.getFileData()
        # Identify the files we're going to back up
        backupFiles = self.getBackupList(fileData)
        # Back up our files
        self.backupFileList(backupFiles)
        # Save the current data
        self.saveFileData(fileData)

    def restore(self):
        """ Restores the game to the most vanilla state possible, copying changes to overwrite. """
        # Check if it's possible to restore.
        if self.canRestore():
            if not self.paths.rootOverwritePath().exists():
                os.makedirs(self.paths.rootOverwritePath())
            # Get hashes for our current vanilla game install.
            fileData = self.getFileData()
            # Iterate through everything in the current game folder and look for changes.
            gameFiles = self.files.getGameFileList()
            for file in gameFiles:
                if (Path(file).exists()):
                    # If we have a record of this file, check for changes.
                    if str(file) in fileData:
                        # If file has changed, check if we have a backup.
                        if fileData[str(file)] != str(self.hashFile(file)):
                            backupPath = self.paths.rootBackupPath() / self.paths.gameRelativePath(file)
                            # If we have a backup, move the file to overwrite and restore.
                            if backupPath.exists():
                                overwritePath = self.paths.rootOverwritePath() / self.paths.gameRelativePath(file)
                                self.moveTo(str(file), str(overwritePath))
                                self.copyTo(str(backupPath), str(file))
                    # If this is a new file, move it to overwrite.
                    else:
                        overwritePath = self.paths.rootOverwritePath() / self.paths.gameRelativePath(file)
                        self.moveTo(str(file), str(overwritePath))
            # Iterate through the files we've got data for.
            for file in fileData.keys():
                # Check to see if the file has been deleted.
                if not Path(file).exists():
                    backupPath = self.paths.rootBackupPath() / self.paths.gameRelativePath(file)
                    # If the file has been deleted and has a backup, restore it.
                    if backupPath.exists():
                        self.copyTo(str(backupPath), str(file))
        # Clean up any empty game folders.
        gameFolders = self.files.getGameFolderList()
        for folder in gameFolders:
            if folder.exists():
                if len(self.files.getFolderFileList(folder)) == 0:
                    shutil.rmtree(folder)
        # If backup is disabled, we can clear any backed up files now that the restore is complete.
        if self.settings.backup() is False:
            self.clearBackupFiles()
        # Delete current backup data.
        self.clearFileData()

    def hashFile(self, path):
        """ Hashes a file and returns the hash """
        func = getattr(hashlib, 'md5')()
        if (Path(path).exists()):
            os.chmod(path, stat.S_IWRITE)
        f = os.open(path, (os.O_RDWR | os.O_BINARY))
        for block in iter(lambda: os.read(f, 2048*func.block_size), b''):
            func.update(block)
        os.close(f)
        return func.hexdigest()

    def backupFileList(self, backupFiles=list):
        """ Backs up a list of game files if not already backed up. """
        # Loop through our list of files.
        for file in backupFiles:
            relativePath = self.paths.gameRelativePath(file)
            backupPath = self.paths.rootBackupPath() / relativePath
            # Back them up if they don't already exist.
            if not backupPath.exists() and Path(file).exists():
                self.copyTo(str(file), str(backupPath))

    def getBackupList(self, fileData=dict):
        """ Gets a list of files that should be backed up. """
        backupFiles = []
        # If backup is enabled, we want to back up all the vanilla files.
        if self.settings.backup():
            backupFiles = fileData.keys()
        # Otherwise, we need to identify which files are going to conflict.
        else:
            conflictFiles = []
            # If we're in linkmode, only linked files could cause conflicts.
            if self.settings.linkmode():
                conflictFiles = self.files.getLinkableModFiles()
            # Otherwise, every root mod file could be a conflict.
            else:
                conflictFiles = self.files.getRootModFiles()
            # Loop through the mod files and see if we have data for them.
            for file in conflictFiles:
                relativePath = self.paths.rootRelativePath(file)
                gamePath = self.paths.gamePath() / relativePath
                # If we have data, we need to back this file up.
                if str(gamePath) in fileData:
                    backupFiles.append(gamePath)
        return backupFiles

    def getFileData(self):
        """ Gets a dictionary of vanilla game files with their hashes. """
        fileData = {}
        # If we have already run a build, just load the data from that.
        if (self.paths.rootBackupDataFilePath().exists()):
            fileData = json.load(open(self.paths.rootBackupDataFilePath()))
        # If we have a cache file for this game already load that.
        elif (self.settings.cache() and self.paths.rootCacheFilePath().exists()):
            fileData = json.load(open(self.paths.rootCacheFilePath()))
        # Hash the base game files.
        else:
            for file in self.files.getGameFileList():
                fileData.update({str(file):str(self.hashFile(file))})
            # If cache is enabled, save the data to cache.
            if self.settings.cache():
                if not self.paths.rootCacheFilePath().exists():
                    self.paths.rootCacheFilePath().touch()
                with open(self.paths.rootCacheFilePath(), "w") as rcJson:
                    json.dump(fileData, rcJson)
            # Otherwise, clear any cache if it exists.
            else:
                self.clearCache()
        return fileData

    def saveFileData(self, fileData=dict):
        """ Saves current file data to the backup data path """
        if self.paths.rootBackupDataFilePath().exists():
            self.paths.rootBackupDataFilePath().touch()
        with open(self.paths.rootBackupDataFilePath(), "w") as rcJson:
            json.dump(fileData, rcJson)

    def clearFileData(self):
        """ Clears the current backup data file """
        if self.paths.rootBackupDataFilePath().exists():
            self.deletePath(self.paths.rootBackupDataFilePath())

    def clearBackupFiles(self):
        """ Clears the current backup file folder """
        if self.paths.rootBackupPath().exists():
            shutil.rmtree(self.paths.rootBackupPath())

    def buildCache(self):
        """ Triggers a cache build if none exists """
        return self.getFileData()

    def clearCache(self):
        """ Clears the current cache file """
        if self.paths.rootCacheFilePath().exists():    
            self.deletePath(self.paths.rootCacheFilePath())

    def canRestore(self):
        """ Checks if backup data exists and therefore whether a restore is possible """
        # We can attempt to restore as long as we have some data, either from a current run or from cache
        # We don't want to run this if we don't have data and risk generating data from a contaminated install
        backupDataExists = self.paths.rootBackupDataFilePath().exists()
        cacheDataExists = self.paths.rootCacheFilePath().exists()
        return backupDataExists or cacheDataExists

    def copyTo(self, fromPath=Path, toPath=Path):
        if (Path(toPath).exists()):
            os.chmod(toPath, stat.S_IWRITE)
        os.makedirs(os.path.dirname(toPath), exist_ok=True)
        copy2(fromPath, toPath)

    def replaceDir(self, fromPath=Path, toPath=Path):
        if (Path(toPath).exists()):
            shutil.rmtree(toPath)
        shutil.copytree(fromPath, toPath)

    def deletePath(self, path=Path):
        if (Path(path).exists()):
            os.chmod(path, stat.S_IWRITE)
        os.remove(path)

    def moveTo(self, fromPath=Path, toPath=Path):
        if (Path(toPath).exists()):
            os.chmod(toPath, stat.S_IWRITE)
        os.makedirs(os.path.dirname(toPath), exist_ok=True)
        shutil.move(str(fromPath), str(toPath))
    
    def migrateLegacyGameData(self):
        """ Migrates pre-versioned data to the new folder. """
        # Move the backup files.
        if Path(self.paths.rootBuilderLegacyGameDataPath() / "backup").exists():
            self.moveTo(self.paths.rootBuilderLegacyGameDataPath() / "backup", self.paths.rootBuilderGameDataPath())

        # Move the json files.
        if Path(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderCacheData.json").exists():
            self.moveTo(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderCacheData.json", self.paths.rootCacheFilePath())
        
        if Path(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderBackupData.json").exists():
            self.moveTo(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderBackupData.json", self.paths.rootBackupDataFilePath())
        
        if Path(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderModData.json").exists():
            self.moveTo(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderModData.json", self.paths.rootModDataFilePath())
        
        if Path(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderLinkData.json").exists():
            self.moveTo(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderLinkData.json", self.paths.rootLinkDataFilePath())

    def hasGameUpdateBug(self):
        """ Determines if this game has the update bug. """
        legacyPath = self.paths.rootBuilderLegacyGameDataPath()
        currentPath = self.paths.rootBuilderGameDataPath() # Create it if it doesn't already exist.
        versionFolders = sorted(self.files.getSubFolderList(legacyPath, False), reverse=True)
        versionFolders.remove(currentPath)

        # If there is at least one past version of the game, it might need a fix.
        if len(versionFolders) > 0:
            hasBug = False
            # If either of the build data files are present, then we've got a bug.
            for folder in versionFolders:
                if Path(folder / "RootBuilderModData.json").exists():
                    hasBug = True
                if Path(folder / "RootBuilderLinkData.json").exists():
                    hasBug = True
                if Path(folder / "RootBuilderBackupData.json").exists():
                    hasBug = True
            return hasBug
        else:
            return False
    
    def fixGameUpdateBug(self):
        """ Moves files to try and resolve the game update bug. """
        legacyPath = self.paths.rootBuilderLegacyGameDataPath()
        currentPath = self.paths.rootBuilderGameDataPath()
        versionFolders = sorted(self.files.getSubFolderList(legacyPath, False), reverse=True)
        versionFolders.remove(currentPath)
        qInfo(str(currentPath))
        # If there is at least one past version of the game, it might need a fix.
        if len(versionFolders) > 0:
            # Get the current and previous version folders.
            foundBug = False
            for folder in versionFolders:
                qInfo(str(folder))
                if not foundBug:
                    if Path(folder / "RootBuilderModData.json").exists():
                        self.moveTo(str(folder / "RootBuilderModData.json"), str(self.paths.rootModDataFilePath()))
                        foundBug = True
                    if Path(folder / "RootBuilderLinkData.json").exists():
                        self.moveTo(str(folder / "RootBuilderLinkData.json"), str(self.paths.rootLinkDataFilePath()))
                        foundBug = True
                    if Path(folder / "RootBuilderBackupData.json").exists():
                        self.moveTo(str(folder / "RootBuilderBackupData.json"), str(self.paths.rootBackupDataFilePath()))
                        foundBug = True
                    if foundBug and Path(folder / "RootBuilderCacheData.json").exists():
                        self.copyTo(str(folder / "RootBuilderCacheData.json"), str(self.paths.rootCacheFilePath()))
                    if foundBug and Path(folder / "backup").exists():
                        self.replaceDir(str(folder / "backup"), str(self.paths.rootBackupPath()))

            


