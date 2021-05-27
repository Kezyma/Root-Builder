from PyQt5.QtCore import QCoreApplication, qDebug, qInfo, qWarning
from pathlib import Path
import mobase, os, json, pathlib, shutil

class AutoRootLinker():
    #region Init
    def __init__(self, organizer, paths, files):
        self._org = organizer
        self._paths = paths
        self._files = files
        super(AutoRootLinker, self).__init__()
    #endregion

    #region Backup
    def build(self):
        linkFileData = self._files.getLinkableModFiles()
        qInfo("AutoRoot: Generating links.")
        for file in linkFileData.values():
            relativePath = self._paths.rootRelativePath(str(file))
            gamePath = self._paths.gamePath() / relativePath
            if gamePath.exists():
                qDebug("AutoRoot: Renaming existing file " + str(gamePath))
                shutil.move(gamePath, Path(str(gamePath) + ".autoroot"))
            qDebug("AutoRoot: Linking " + str(file) + " to " + str(gamePath))
            try:
                Path(file).link_to(gamePath)
            except:
                qWarning("AutoRoot: Could not create link " + str(gamePath))


        qInfo("AutoRoot: Saving link data.")
        if not self._paths.linkTempPath().exists():
            self._paths.linkTempPath().touch()
        with open(self._paths.linkTempPath(), "w") as jsonFile:
            json.dump(linkFileData, jsonFile)
        qInfo("AutoRoot: Link data saved.")

    def clear(self):
        qInfo("AutoRoot: Loading link data.")
        if self._paths.linkTempPath().exists():
            linkFileData = json.load(open(self._paths.linkTempPath()))
            qInfo("AutoRoot: Link data loaded.")

            for file in linkFileData.keys():
                gamePath = self._paths.gamePath() / file
                if gamePath.exists():
                    qDebug("AutoRoot: Removing link " + str(gamePath))
                    gamePath.unlink(True)
                if Path(str(gamePath) + ".autoroot").exists():
                    qDebug("AutoRoot: Restoring file " + str(gamePath))
                    shutil.move(Path(str(gamePath) + ".autoroot"), gamePath)

            qInfo("AutoRoot: Clearing link data.")
            os.remove(self._paths.linkTempPath())
            qInfo("AutoRoot: Link data cleared.")
        else:
            qInfo("AutoRoot: No link file exists.")
        
    #endregion