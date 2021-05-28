from PyQt5.QtCore import QCoreApplication
import mobase

from .rootbuilder import RootBuilder

class RootBuilderPlugin(mobase.IPluginFileMapper):
    """ Main Root Builder plugin. Handles auto build features """

    def __init__(self):
        super(RootBuilderPlugin, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.rootBuilder = RootBuilder(self.organiser)
        self.startingRootExe = False
        self.organiser.onAboutToRun(lambda appName: self.build(appName))
        self.organiser.onFinishedRun(lambda appName, resultCode: self.clear(appName, resultCode))

    def name(self):
        return "RootBuilder"

    def displayname(self):
        return "RootBuilder"

    def author(self):
        return "Kezyma"

    def description(self):
        return self.__tr("Allows management of base game files by utilising a Root folder within individual mods.")
    
    def version(self):
        return mobase.VersionInfo(0, 0, 1, mobase.ReleaseType.alpha) 

    def isActive(self):
        return self.rootBuilder.settings.enabled()

    def __tr(self, trstr):
        return QCoreApplication.translate("RootBuilder", trstr)

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

    def mappings(self):
        """ Returns mappings, if there are any, for usvfs mode. """
        return self.rootBuilder.mappings()

    def build(self, appName):
        """ Runs a build if autobuild is enabled and potentially redirects the exe being run """
        res = True
        # Check if this is a secondary run from redirect.
        if (self.startingRootExe == False):
            # Run a build if autobuild is enabled.
            if self.rootBuilder.settings.autobuild():
                self.rootBuilder.build()
            # Possibly redirect to a different exe.
            if self.rootBuilder.settings.redirect():
                res = self.redirect(appName)
        return res

    def clear(self, appName, resultCode):
        """ Runs a clear operation if autobuild is enabled. """
        if self.rootBuilder.settings.autobuild():
            self.rootBuilder.clear()

    def redirect(self, appName):
        """ Redirects an app to the game path version if it is from a root mod folder. """
        # Check if the app shares a path with the mods path.
        if self.rootBuilder.paths.sharedPath(self.rootBuilder.paths.modsPath(), appName):
            self.startingRootExe = True
            # Check if the exe exists in the game path.
            exeGamePath = self.rootBuilder.paths.gamePath() / self.rootBuilder.paths.rootRelativePath(appName)
            if exeGamePath.exists():
                # Run the game path version of the application.
                self.organiser.waitForApplication(self.organiser.startApplication(str(exeGamePath)))
                self.startingRootExe = False
                # Return false to prevent the original run.
                return False
        return True
        