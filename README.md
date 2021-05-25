# Kezyma's Root Builder for Mod Organizer 2
#### v3 Readme

Root Builder allows you to manage mod files that go inside the base game folder instead of the Data (or Data Files for Morrowind) folder. It provides functions that allow you to copy mod files to the game folder, synchronise them with the files in Mod Organizer and to clean up and restore the original game folder.

## Mod Setup

When packaging mods for mod organizer, you must move any files intended to go into the base game folder into a new folder called Root that sits alongside other Data folders such as Meshes or Textures. 

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

## Plugin Setup

If you would like to use Root Builder as a plugin, copy the entire RootBuilder folder into your Mod Organizer's plugin folder.
Assuming Mod Organizer is installed at `D:/MO/` the plugin folder is at `D:/MO/plugins`

When you launch Mod Organizer, Root Builder will be added to your tools menu.
There are four options;
`-GUI-` which launches Root Builder using the current profile.
`Build`, `Sync` and `Clear` which run Root Builder with different command line arguments.

There are also settings to enable cache, backup and debug mode (these only matter for the Build, Sync and Clear commands).

## Root Builder Setup

If you are not using Root Builder as a Mod Organizer plugin, you only need the RootBuilder3.exe file, the python scripts and icon file are exclusively for the Mod Organizer plugin.

Run RootBuilder3.exe, you can do this inside or outside of Mod Organizer, it should work either way.

Select your ModOrganizer.ini file in the window that opens.
If you are running a portable Mod Organizer install, the ini file will be located in the Mod Organizer folder.
If you're running a local instance, it'll be the folder you selected to set the instance up in, by default it'll be in the following location;

	C:\Users\%USER%\AppData\Local\ModOrganizer\

Root Builder should now automatically detect the location of your currently loaded game and the profile you have loaded in Mod Organizer.
The game will also be added to the list of games, which you can switch between. 
These are tied to the game install, not the Mod Organizer install, so you can not have multiple ModOrganizer.ini files for the same game.

### Build

Build is used to copy the files from your mods folders into your base game folder.

When you click on Build, the following things will happen.
- All current files in the base game folder will be scanned and recorded. 
	- If you have already clicked Build, this step is skipped and currently recorded data is used.
- All currently active mods will be scanned and any Root files will be recorded, overwriting based on your load order.
- Any files that would be overwritten by mod files are temporarily backed up.
- Root mod files are copied into the base game directory.

### Sync

Sync is used to update the files in your mods folders with any changes that have occurred since the last Build.

When you click on Sync, the following things will happen.
- All files in the base game folder will be scanned.
- Your current modlist will be updated.
- Any files that came from mods and that have changed will be copied back to the original mod folder.
- Any original game files that have changed and that have a backup available will be copied to the overwrite folder.
	- Files without a backup available will be left where they are, to prevent possible complications later.
- Any new files that have been created will be copied to the overwrite folder.

### Clear

Clear is the same as Sync, except that it will also restore the base game folder to (as close as possible to) its original state. 

When you click on Clear, the following things will happen.
- Root Builder will run the Sync function.
- All files in the base game folder will be scanned.
- Any original game files that have changed and that have a backup available will be restored.
- Any mod files or new files will be deleted.
- Any created folders will be deleted.
- Any backed up files will be deleted.
- Recorded data is cleared.

### Cache

If Cache is enabled, during the initial scanning of game files, a copy of the scanned data for these files is recorded. These scan results are then used in place of scanning again for any future builds. This is ideal if you have a perfectly vanilla installation.

If Cache is disabled and there is already an existing cache for this game, it will be deleted on the next Build.

### Backup

If Backup is enabled, after the initial scanning of game files, a backup of all root files will be taken instead of only known conflicts. This is ideal if you have a perfectly vanilla installation as it means you can pick up on every change made. It also assists in identifying changing base game files outside of Root Builder, such as ini edits and 4gb patches. 

If Backup is enabled, it will prevent the Clear function from clearing the backed up files.

## Command Line Usage

RootBuilder3.exe can also be called from the command line with the following parameters;

	-ini "C:\Absolute\Path\To\ModOrganizer.ini"
Specifies the ModOrganizer install to use.

	-cache
	-backup
Enables cache and/or backup modes.
If these flags are not specified but you have enabled cache or backup for this game in the GUI, it will use those settings. Otherwise they both default to false.

	-build
	-sync
	-clear
Specifies which of the three actions to run. If you use one of these, Root Builder will run in a headless mode.

	-debug
If combined with the build, sync or clear command, will leave the log window open after completing.

So you can create a shortcut that looks something like this;

	RootBuilder3.exe -build -cache -backup -ini "D:\MO2\ModOrganizer.ini"

and like this;

	RootBuilder3.exe -clear -cache -backup -ini "D:\MO2\ModOrganizer.ini"

And use them to quickly build, clear or sync.
