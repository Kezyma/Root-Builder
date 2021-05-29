from PyQt5.QtCore import QCoreApplication
from shutil import copy2
from pathlib import Path
from .rootbuilder_settings import RootBuilderSettings
from .rootbuilder_paths import RootBuilderPaths
from .rootbuilder_files import RootBuilderFiles
import mobase, os, hashlib, json, shutil

class RootBuilderLinker():
    """ Root Builder link module. Used to create links for specific file types. """

    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.settings = RootBuilderSettings(self.organiser)
        self.paths = RootBuilderPaths(self.organiser)
        self.files = RootBuilderFiles(self.organiser)
        super(RootBuilderLinker, self).__init__()

    def build(self):
        """ Generates links for all linkable mod files and saves records of each of them """
        # Get all linkable mod files.
        linkFileData = self.files.getLinkableModFiles()
        for file in linkFileData:
            relativePath = self.paths.rootRelativePath(file)
            gamePath = self.paths.gamePath() / relativePath
            # If the linkable file is already in the game folder, rename it.
            if gamePath.exists():
                shutil.move(gamePath, Path(str(gamePath) + ".rbackup"))
            # Create the dirs if they don't exist.
            if not gamePath.parent.exists():
                    os.makedirs(gamePath.parent)
            # Try and create a link. This will fail if a link is already there.
            Path(file).link_to(gamePath)
        # Save our link data.
        if not self.paths.rootLinkDataFilePath().exists():
            self.paths.rootLinkDataFilePath().touch()
        with open(self.paths.rootLinkDataFilePath(), "w") as jsonFile:
            json.dump(linkFileData, jsonFile)

    def clear(self):
        """ Clears any created links from mod files """
        # Check if we have any link data and load it if we do.
        if self.paths.rootLinkDataFilePath().exists():
            linkFileData = json.load(open(self.paths.rootLinkDataFilePath()))
            # Loop through our link data and unlink individual files.
            for file in linkFileData:
                relativePath = self.paths.rootRelativePath(file)
                gamePath = self.paths.gamePath() / relativePath
                if gamePath.exists():
                    gamePath.unlink(True)
                if Path(str(gamePath) + ".rbackup").exists():
                    shutil.move(Path(str(gamePath) + ".rbackup"), gamePath)
            # Remove our link data file.
            os.remove(self.paths.rootLinkDataFilePath())
