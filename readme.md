# Root Builder
## v4.0.*

### Introduction
Root Builder allows you to manage mod files that go inside the base game folder instead of the Data (or Data Files for Morrowind) folder. It provides functions that allow you to copy mod files to the game folder, synchronise them with the files in Mod Organizer and to clean up and restore the original game folder. It also provides the ability to fully automate this process on each launch.


### Installation
If you currently have any version of RootBuilder prior to 4.0.*, run a full clear operation and delete all files associated with RootBuilder before installing this version. They are incompatible and may cause problems if present.
Copy the rootbuilder folder to Mod Organizer's plugins folder. If Mod Organizer is installed at `D:\MO\`, the plugins folder will be located at `D:\MO\plugins\`

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
RootBuilder will, by default, run a build whenever you run an application through Mod Organizer and a clear when the application closes, this can be disabled in settings.

#### Build
When a build runs, the following happpens;
- The game folder will be hashed and the results recorded. If data already exists, it will be loaded.
- If backup is enabled, a full backup of the game folder will be taken, otherwise, only conflicts between mod and game files will be backed up.
- If usvfs mode and link mode are enabled, links will be created in the game folder for all linkable files and a list of these will be recorded.
- If usvfs mode is not enabled, all root mod files will be copied to the game folder and recorded.

#### Sync
Sync only has an effect if usvfs mode is disabled.
When a sync runs, the following happens;
- Any copied mod files that have changed will be copied back to the mod folder.
- Any base game files that have changed will be copied to the overwrite folder.
- Any new files will be copied to the overwrite folder.
Please note, if you run a sync that copies files to overwrite and then you move them to a mod, you must run build again or RootBuilder will think they are still in the overwrite folder and may copy them back there on the next sync or clear.

#### Clear
When a clear runs, the following happens;
- A sync is run.
- If any files have been linked, they will be unlinked.
- If any files have been copied, they will be deleted.
- If any base game files have changed and also have a backup, the original backup will be restored.

### Settings

#### enabled (default: true)
Determines whether the RootBuilder plugin is enabled in Mod Organizer.

### cache (default: true)
If enabled, on the first build being run, the hashes of the game folder will be cached. This is ideal if you have a fresh game installation or are confident that you do not plan on changing files in the game folder manually.
If disabled, if any cache already exists for the current game, it will be cleared on the next build.

### backup (default: true)
If enabled, on the first build being run, the contents of the game folder will be backed up. This is ideal if you have a fresh game installation or are confident that you do not plan on changing files in the game folder manually.
If disabled, RootBuilder will try to identify any conflicts between your installed mods and the game folder and back only those conflicts up.
If disabled, any existing backup will be deleted on the next clear.

### autobuild (default: true)
If enabled, whenever you run an application through Mod Organizer, a build will be run before the application and a clear will be run when the application closes.

### redirect (default: true)
If enabled, when running an application through Mod Organizer, if that application is in a root folder within a mod and also exists in the game folder, it will redirect the application to launch from the game folder instead.

### usvfsmode (default: false)
If enabled, instead of copying files to and from the game folder, RootBuilder will utilise Mod Organizer's usvfs to handle root files. 
Please note, this does not work with all games and mod combinations.

### linkmode (default: false)
Requires usvfsmode to be enabled.
If enabled, on top of using usvfs, RootBuilder will create links in the game folder pointing to specific mod root files. This can improve the compatibility of usvfs mode.
Please note, this does not work with all games and mod combinations.

### linkextensions (default: "exe,dll")
A comma separated list of file extensions that are valid for linking if linkmode is enabled.

### exclusions (default: "Saves,Morrowind.ini")
A comma separated list of files and folders in the base game folder that will be ignored by RootBuilder.
Any mods that contain these files and folders will be ignored and skipped during build.
