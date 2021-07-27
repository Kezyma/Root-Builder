# Root Builder
## v4.1.*

### Introduction
Root Builder allows you to manage mod files that go inside the base game folder instead of the Data (or Data Files for Morrowind) folder. It provides functions that allow you to copy mod files to the game folder, synchronise them with the files in Mod Organizer and to clean up and restore the original game folder. It also provides the ability to fully automate this process on each launch.

### Installation
If you currently have any version of RootBuilder prior to 4.0.*, run a full clear operation and delete all files associated with RootBuilder before installing this version. They are incompatible and may cause problems if present.

Copy the rootbuilder folder to Mod Organizer's plugins folder. If Mod Organizer is installed at `D:\MO\`, the plugins folder will be located at `D:\MO\plugins\`
Make sure that the individual plugin files `*.py` are located at `D:\MO\plugins\rootbuilder\` and not directly copied into the plugins folder itself.

### Uninstallation

To remove Root Builder entirely. First run a Clear operation to clean up any installed files and return your game to a vanilla state.

Delete the following folders from Mod Organizer, assuming Mod Organizer is installed at `D:\MO\`:
`D:\MO\plugins\rootbuilder\`
`D:\MO\plugins\data\rootbuilder\`

### Mod Setup
When packaging mods for Mod Organizer, you must move any files intended to go into the base game folder into a new folder called Root that sits alongside other Data folders such as Meshes or Textures. 

For example, if your original mod is packaged like this;
	
	SomeModDll.dll
	SomeModExe.exe
	Data\SomeModEsp.esp
	Data\Textures\ASpecialTexture.dds
	Data\Meshes\VeryPrettyModel.nif

You would need to rearrange it for Mod Organizer as follows;
	
	Root\SomeModDll.dll
	Root\SomeModExe.exe
	SomeModEsp.esp
	Textures\ASpecialTexture.dds
	Meshes\VeryPrettyModel.nif

Where the esp file and the Meshes and Textures will be picked up by Mod Organizer as usual, but the files intended for the base game folder are now in a subfolder called Root.

### Usage
A new item will appear in the tools menu of Mod Organizer with the three main functions of RootBuilder, build, sync and clear.

RootBuilder will, by default, run a build whenever you run an application through Mod Organizer and a clear when the application closes, this can be turned off in settings by disabling autobuild(default=true).

Ideally, you want to have the game folder as unmodified as possible during the first build if backup(default=true) and/or cache(default=true) is enabled. This enables RootBuilder to correctly restore a vanilla game on each clear as well as more accurately track every change made to the game. If you wish to change the game files in the cache and/or backup, disable the setting, run a build and then run a clear. Then re-enable the setting. On the next build, a fresh backup and/or cache will be taken.

#### Build
When a build runs, the following happpens;
- The current game folder is hashed and the data recorded.
	- If data from a previous build exists, it will be loaded instead.
	- If cache data exists and previous build data does not, it will be loaded instead.
- If cache(default=true) is enabled , the data will be saved as a cache for all future runs.
	- If not, any existing cache file is deleted.
- If backup(default=true) is enabled , any base game files that are not currently backed up, will be.
	- If backup isn't enabled, any any game files that conflict with mod files in root folders will be backed up.
- If usvfsmode(default=false) and linkmode(default=false) are enabled , any valid files will be linked to the game folder and the list recorded.
- Otherwise, all mod files in the root folder are copied to the game folder.

#### Sync
Sync only has an effect if usvfs mode is disabled and a build has been run.

When a sync runs, the following happens;
- Data from the last build is loaded.
- Each file in the game folder is checked.
	- If it came from a mod, it's compared with the original file and will overwrite it if changed.
	- If it came from the base game, it's compared with the original file and the file will be copied to Mod Organizer's overwrite folder if it has changed.
	- If it's a new file, it will be copied to Mod Organizer's overwrite folder.
- Data for the current build is updated to include references to any files that were copied to the overwrite folder and any changed hashes are updated.

Please note, if you run a sync that copies files to overwrite and then you move them to a mod, you must run build again or RootBuilder will think they are still in the overwrite folder and may copy them back there on the next sync or clear.

#### Clear
When a clear runs, the following happens;
- A Sync operation is run, to make sure any changes to the game files are not lost.
- If any files have been linked while linkmode(default=false) is enabled, the links in the game folder will be removed.
- Any files that have been copied across to the game folder will be deleted.
- Any base game files that have changed and also have a backup will be restored from the backup.
- If backup(default=true) is disabled, any backed up files will be deleted.
- Data for the last build is deleted.

### Settings

#### enabled (default: true)
Determines whether the RootBuilder plugin is enabled in Mod Organizer.

#### cache (default: true)
If enabled, on the first build being run, the hashes of the game folder will be cached. This is ideal if you have a fresh game installation or are confident that you do not plan on changing files in the game folder manually.

If disabled, if any cache already exists for the current game, it will be cleared on the next build.

#### backup (default: true)
If enabled, on the first build being run, the contents of the game folder will be backed up. This is ideal if you have a fresh game installation or are confident that you do not plan on changing files in the game folder manually.

If disabled, RootBuilder will try to identify any conflicts between your installed mods and the game folder and back only those conflicts up.

If disabled, any existing backup will be deleted on the next clear.

#### autobuild (default: true)
If enabled, whenever you run an application through Mod Organizer, a build will be run before the application and a clear will be run when the application closes.

#### redirect (default: true)
If enabled, when running an application through Mod Organizer, if that application is in a root folder within a mod and also exists in the game folder, it will redirect the application to launch from the game folder instead.

#### usvfsmode (default: false)
Requires autobuild to be enabled.

If enabled, instead of copying files to and from the game folder, RootBuilder will utilise Mod Organizer's usvfs to handle root files. This will only work with autobuild since it is handled when you launch an application through Mod Organizer. Do not attempt to manually build, sync or clear when using this mode. Make sure to run a clear before enabling/disabling this setting or unintentional results may occur.

Please note, this does not work with all game and mod combinations.

#### linkmode (default: false)
Requires usvfsmode to be enabled.

If enabled, on top of using usvfs, RootBuilder will create links in the game folder pointing to specific mod root files. This can improve the compatibility of usvfs mode.

Please note, this does not work with all game and mod combinations.

#### linkextensions (default: "exe,dll")
A comma separated list of file extensions that are valid for linking if linkmode is enabled.

#### exclusions (default: "Saves,Morrowind.ini")
A comma separated list of files and folders in the base game folder that will be ignored by RootBuilder.

Any mods that contain these files and folders will be ignored and skipped during build.
