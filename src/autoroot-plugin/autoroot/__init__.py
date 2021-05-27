import mobase
from . import autoroot
from . import autoroottool

# Init
def createPlugins():
    return [autoroot.AutoRoot(), autoroottool.AutoRootCleanupTool(), autoroottool.AutoRootBackupTool(), autoroottool.AutoRootDeleteTool()]