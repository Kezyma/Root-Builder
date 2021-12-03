import mobase
from .rootbuilder_plugin import RootBuilderPlugin
from .rootbuilder_tool_build import RootBuilderBuildTool
from .rootbuilder_tool_clear import RootBuilderClearTool
from .rootbuilder_tool_sync import RootBuilderSyncTool
from .rootbuilder_tool_manage import RootBuilderManageTool

def createPlugins():
    return [RootBuilderPlugin(),RootBuilderBuildTool(),RootBuilderClearTool(),RootBuilderSyncTool(),RootBuilderManageTool()]
