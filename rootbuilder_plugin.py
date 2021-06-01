from PyQt5.QtCore import QCoreApplication
import mobase

from .rootbuilder import RootBuilder
from .rootbuilder_base import RootBuilderBase

class RootBuilderPlugin(RootBuilderBase, mobase.IPluginFileMapper):
    """ Main Root Builder plugin. Handles auto build features """

    def __init__(self):
        super(RootBuilderPlugin, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.rootBuilder = RootBuilder(self.organiser)
        self.startingRootExe = False
        self.organiser.onAboutToRun(lambda appName: self.build(appName))
        self.organiser.onFinishedRun(lambda appName, resultCode: self.clear(appName, resultCode))
        return True

    def name(self):
        return self.baseName()

    def displayname(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Allows management of base game files by utilising a Root folder within individual mods.")

    def __tr(self, trstr):
        return QCoreApplication.translate("RootBuilder", trstr)

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
        