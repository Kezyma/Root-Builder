from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from pathlib import Path
from .rootbuilder import RootBuilder
import mobase

class RootBuilderBase():

    #region Init
    def __init__(self):
        super(RootBuilderBase, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.rootBuilder = RootBuilder(self.organiser)
        return True
    #endregion

    def version(self):
        return mobase.VersionInfo(4, 2, 1, mobase.ReleaseType.BETA) 

    def isActive(self):
        return self.rootBuilder.settings.enabled()

    def __tr(self, trstr):
        return QCoreApplication.translate("RootBuilder", trstr)

    def icon(self):
        return QIcon(str(Path(__file__).parent.joinpath("ui-menu.ico")))

    def author(self):
        return "Kezyma"

    def baseName(self):
        return "RootBuilder"

    def baseDisplayName(self):
        return "Root Builder"

    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        return [
            mobase.PluginSetting("enabled",self.__tr("Enables RootBuilder"),True),
            mobase.PluginSetting("cache",self.__tr("Enables caching of base game files on first run."), True),
            mobase.PluginSetting("backup",self.__tr("Enables full backup of base game files on first run."), True),
            mobase.PluginSetting("autobuild",self.__tr("Enables automatic build and clear on running an application through Mod Organizer."), True),
            mobase.PluginSetting("linkmode",self.__tr("Enables the use of file linking when using usvfs mode."), False),
            mobase.PluginSetting("usvfsmode",self.__tr("Enables the use of usvfs instead of copying during autobuild."), False),
            mobase.PluginSetting("linkextensions",self.__tr("List of file extensions to create links for if using link mode."), "dll,exe"),
            mobase.PluginSetting("exclusions",self.__tr("List of files and folders to exclude from RootBuilder."), "Saves,Morrowind.ini"),
            mobase.PluginSetting("redirect", self.__tr("Enables automatic redirection of exe files being launched from a mod folder to their respective game folder equivalent."), True)
            ]