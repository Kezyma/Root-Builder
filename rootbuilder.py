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

    def build(self):
        self.backup.backup()
        if self.settings.usvfsmode():
            if self.settings.linkmode():
                self.linker.build()
                return
            return
        else:
            self.copier.build()
            return

    def sync(self):
        self.copier.sync()
        return

    def clear(self):
        self.linker.clear()
        self.copier.clear()
        self.backup.restore()
        self.mapper.cleanup()

    def mappings(self):
        return self.mapper.mappings()
        

        