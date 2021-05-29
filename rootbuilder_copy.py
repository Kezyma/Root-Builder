from PyQt5.QtCore import QCoreApplication
from shutil import copy2
from pathlib import Path
from .rootbuilder_settings import RootBuilderSettings
from .rootbuilder_paths import RootBuilderPaths
from .rootbuilder_files import RootBuilderFiles
from .rootbuilder_backup import RootBuilderBackup
import mobase, os, hashlib, json, shutil

class RootBuilderCopy():
    """ Root Builder copy module. Used to copy files to and from mod folders. """

    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.settings = RootBuilderSettings(self.organiser)
        self.paths = RootBuilderPaths(self.organiser)
        self.files = RootBuilderFiles(self.organiser)
        self.backup = RootBuilderBackup(self.organiser)
        super(RootBuilderCopy, self).__init__()

    def build(self):
        """ Copies root mod files to the game folder """
        # Check for existing data and load it.
        fileData = self.getModData()
        # Get list of current mod files.
        modFiles = self.files.getRootModFiles()
        # Iterate over current mod files and update our data.
        for file in modFiles:
            relativePath = self.paths.rootRelativePath(file)
            modFileData = {
                    "Path" : str(file),
                    "Hash" : ""#str(self.backup.hashFile(file))
                }
            # If this is already in our data, compare them, update if newer.
            if str(relativePath) in fileData:
                if fileData[str(relativePath)]["Hash"] != modFileData["Hash"]:
                    fileData[str(relativePath)] = modFileData
            # If the file is not in the existing data, add it.
            else:
                fileData.update({str(relativePath):modFileData})
        # Copy all mod files into the game folder
        for relativePath in fileData.keys():
            sourcePath = Path(fileData[relativePath]["Path"])
            destPath = self.paths.gamePath() / relativePath
            if sourcePath.exists():
                if not destPath.parent.exists():
                    os.makedirs(destPath.parent)
                copy2(sourcePath, destPath)
        # Save data
        self.saveModData(fileData)
        return
    
    def sync(self):
        """ Copies changed mod files back to their original mod folders. """
        # Only run if there's already data.
        if self.hasModData():
            # Get existing data
            modData = self.getModData()
            backupData = self.backup.getFileData()
            gameFiles = self.files.getGameFileList()
            for file in gameFiles:
                relativePath = self.paths.gameRelativePath(file)
                if str(relativePath) in modData:
                    # This is a mod file, check if it has changed and copy it back if it has.
                    fileHash = str(self.backup.hashFile(file))
                    if  fileHash != modData[str(relativePath)]["Hash"]:
                        copy2(file, modData[str(relativePath)]["Path"])
                        modData[str(relativePath)]["Hash"] = fileHash
                elif str(file) in backupData:
                    # This is a vanilla game file, check if it has changed and copy to overwrite and add to modData if it has.
                    fileHash = str(self.backup.hashFile(file))
                    if  fileHash != backupData[str(file)]:
                        overwritePath = self.paths.rootOverwritePath / relativePath
                        if not overwritePath.parent.exists():
                            os.makedirs(overwritePath.parent)
                        copy2(file, overwritePath)
                        modData[str(relativePath)] = { "Path" : overwritePath, "Hash" : fileHash }
                else:
                    # This is a new file, copy it to overwrite and add to modData.
                    overwritePath = self.paths.rootOverwritePath / relativePath
                    if not overwritePath.parent.exists():
                        os.makedirs(overwritePath.parent)
                    copy2(file, overwritePath)
                    modData.update({ str(relativePath) : { "Path" : overwritePath, "Hash" : fileHash } })
            # Save mod data.
            self.saveModData(modData)
        return

    def clear(self):
        """ Cleans up the game folder of any copied mod files, updating the originals where they have changed. """
        # Only run if there's already data.
        if self.hasModData():
            # Run a sync to update any existing mod files before deleting the game folder versions.
            self.sync()
            # Get existing data
            fileData = self.getModData()
            for relativePath in fileData.keys():
                gamePath = self.paths.gamePath() / relativePath
                # If the file exists in the game, delete it.
                if gamePath.exists():
                    os.remove(gamePath)
            # Clear the existing mod data
            self.clearModData()
        return

    def hasModData(self):
        """ Checks if mod file data exists. """
        return self.paths.rootModDataFilePath().exists()

    def getModData(self):
        """ Gets a dictionary of existing mod files with their hashes. """
        fileData = {}
        # If we have already run a build, just load the data from that.
        if (self.paths.rootModDataFilePath().exists()):
            fileData = json.load(open(self.paths.rootModDataFilePath()))

        return fileData

    def saveModData(self, fileData=dict):
        """ Saves current mod data. """
        if self.paths.rootModDataFilePath().exists():
            self.paths.rootModDataFilePath().touch()
        with open(self.paths.rootModDataFilePath(), "w") as rcJson:
            json.dump(fileData, rcJson)

    def clearModData(self):
        """ Removes any existing mod data. """
        if self.paths.rootModDataFilePath().exists():
            os.remove(self.paths.rootModDataFilePath())