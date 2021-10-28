from PyQt5.QtCore import QCoreApplication
import mobase

class RootBuilderSettings():
    """ Root Builder settings module. Used to load various plugin settings. """

    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        super(RootBuilderSettings, self).__init__()

    def __tr(self, trstr):
        return QCoreApplication.translate("RootBuilder", trstr)   

    def enabled(self):
        """ Determines whether Root Builder is enabled. """
        return self.organiser.pluginSetting("RootBuilder", "enabled")

    def cache(self):
        """ Determines whether to cache game file hashes. """
        return self.organiser.pluginSetting("RootBuilder", "cache")

    def backup(self):
        """ Determines whether to take a full game backup. """
        return self.organiser.pluginSetting("RootBuilder", "backup")

    def autobuild(self):
        """ Determines whether to build automatically on run. """
        return self.organiser.pluginSetting("RootBuilder", "autobuild")

    def linkmode(self):
        """ Determines whether to use file linking. """
        return self.organiser.pluginSetting("RootBuilder", "linkmode")

    def usvfsmode(self):
        """ Determines whether to use usvfs root mapping. """
        return self.organiser.pluginSetting("RootBuilder", "usvfsmode")

    def linkextensions(self):
        """ Extensions to be linked if link mode is enabled. """
        return self.organiser.pluginSetting("RootBuilder", "linkextensions").split(",")

    def exclusions(self):
        """ Files to be excluded from all operations. """
        return self.organiser.pluginSetting("RootBuilder", "exclusions").split(",")

    def redirect(self):
        """ Whether to redirect apps launched from mod root folders. """
        return self.organiser.pluginSetting("RootBuilder", "redirect")

