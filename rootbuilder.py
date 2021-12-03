from PyQt5.QtCore import QCoreApplication, qInfo
from .rootbuilder_settings import RootBuilderSettings
from .rootbuilder_paths import RootBuilderPaths
from .rootbuilder_files import RootBuilderFiles
from .rootbuilder_backup import RootBuilderBackup
from .rootbuilder_mapper import RootBuilderMapper
from .rootbuilder_linker import RootBuilderLinker
from .rootbuilder_copy import RootBuilderCopy
import mobase

class RootBuilder():
    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.settings = RootBuilderSettings(self.organiser)
        self.paths = RootBuilderPaths(self.organiser)
        self.files = RootBuilderFiles(self.organiser)
        self.backup = RootBuilderBackup(self.organiser)
        self.mapper = RootBuilderMapper(self.organiser)
        self.linker = RootBuilderLinker(self.organiser)
        self.copier = RootBuilderCopy(self.organiser)
        super(RootBuilder, self).__init__()

    def __tr(self, trstr):
        return QCoreApplication.translate("RootBuilder", trstr)

    def migrate(self):
        self.backup.migrateLegacyGameData()

    def updateFix(self):
        if self.backup.hasGameUpdateBug():
            self.backup.fixGameUpdateBug()
            self.clear()
            self.backup.clearBackupFiles()
            self.backup.clearCache()

    def build(self):
        qInfo("RootBuilder: Starting build.")

        qInfo("RootBuilder: Backing up files.")
        self.backup.backup()
        qInfo("RootBuilder: Backed up files.")
        if self.settings.usvfsmode():
            if self.settings.linkmode():
                qInfo("RootBuilder: Generating links.")
                self.linker.build()
                qInfo("RootBuilder: Links generated.")
        else:
            qInfo("RootBuilder: Copying files.")
            self.copier.build()
            qInfo("RootBuilder: Files copied.")

        qInfo("RootBuilder: Build complete.")

    def sync(self):
        qInfo("RootBuilder: Starting sync.")
        self.copier.sync()
        qInfo("RootBuilder: Sync complete.")
        return

    def clear(self):
        qInfo("RootBuilder: Starting clear.")

        qInfo("RootBuilder: Clearing any links.")
        self.linker.clear()
        qInfo("RootBuilder: Links cleared.")

        qInfo("RootBuilder: Clearing any copied files.")
        self.copier.clear()
        qInfo("RootBuilder: Copied files cleared.")

        qInfo("RootBuilder: Restoring game files.")
        self.backup.restore()
        qInfo("RootBuilder: Game files restored.")
        
        qInfo("RootBuilder: Cleaning up overwrite.")
        self.mapper.cleanup()
        qInfo("RootBuilder: Overwrite cleaned.")

        qInfo("RootBuilder: Clear complete.")

    def mappings(self):
        return self.mapper.mappings()
        

        