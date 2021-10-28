import mobase
from .rootbuilder_plugin import RootBuilderPlugin
from .rootbuilder_tool_build import RootBuilderBuildTool
from .rootbuilder_tool_clear import RootBuilderClearTool
from .rootbuilder_tool_sync import RootBuilderSyncTool
from .rootbuilder_tool_build_cache import RootBuilderBuildCacheTool
from .rootbuilder_tool_clear_cache import RootBuilderClearCacheTool
from .rootbuilder_tool_create_backup import RootBuilderCreateBackupTool
from .rootbuilder_tool_delete_backup import RootBuilderDeleteBackupTool

def createPlugins():
    return [RootBuilderPlugin(),RootBuilderBuildTool(),RootBuilderClearTool(),RootBuilderSyncTool(),RootBuilderBuildCacheTool(),RootBuilderClearCacheTool(),RootBuilderCreateBackupTool(),RootBuilderDeleteBackupTool()]
