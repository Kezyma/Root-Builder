from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from typing import List
from pathlib import Path
import subprocess
import mobase  

from .rootbuilder import RootBuilder  
from .rootbuilder import RootBuilderBuild
from .rootbuilder import RootBuilderClear
from .rootbuilder import RootBuilderSync

def createPlugins() -> List[mobase.IPlugin]:
    return [RootBuilder(), RootBuilderBuild(), RootBuilderSync(), RootBuilderClear()]
