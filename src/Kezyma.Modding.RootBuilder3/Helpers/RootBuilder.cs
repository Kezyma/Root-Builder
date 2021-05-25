using Kezyma.Modding.RootBuilder3.Models;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Reflection.Metadata.Ecma335;
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Text.RegularExpressions;
using System.Transactions;
using System.Windows.Forms;
using System.Windows.Forms.Design;

namespace Kezyma.Modding.RootBuilder3.Helpers
{
    public class RootBuilder
    {
        public RootBuilder(string iniPath = "", bool? cache = null, bool? backup = null, bool debug = false)
        {
            _debug = debug;
            if (File.Exists(iniPath)) InitialiseFromIni(iniPath, cache, backup);
            else if (!string.IsNullOrWhiteSpace(RootBuilderData.LastGameId)) InitialiseFromId(RootBuilderData.LastGameId);
        }

        private bool _debug;

        #region Icons
        public Image GetCurrentIcon()
        {
            if (!string.IsNullOrWhiteSpace(CurrentGameData.Icon))
            {
                byte[] bytes = Convert.FromBase64String(CurrentGameData.Icon);
                using MemoryStream stream = new MemoryStream(bytes);
                return Image.FromStream(stream);
            }
            var icon = new IconLoader(RootBuilderData.IconSources).GetIconForPath(CurrentGameData.GamePath, Process.GetCurrentProcess().MainModule.FileName).ToBitmap();
            using MemoryStream memoryStream = new MemoryStream();
            icon.Save(memoryStream, ImageFormat.Png);
            byte[] bitmapBytes = memoryStream.GetBuffer();
            CurrentGameData.Icon = Convert.ToBase64String(bitmapBytes, Base64FormattingOptions.InsertLineBreaks);
            SaveRootBuilderData();
            return icon;
        }

        public Image GetDefaultIcon() => new IconLoader(new string[] {}).GetIconForPath("", Process.GetCurrentProcess().MainModule.FileName).ToBitmap();
        #endregion

        #region Build
        public void Build(Action<string> log = null, Action<int, string> progress = null)
        {
            ScanGameFiles(log, progress);
            ScanModFiles(log, progress);
            BackupGameFiles(log, progress);
            DeployModFiles(log, progress);
            
            CurrentGameData.Built = true;
            SaveRootBuilderData();
        }
        private void ScanGameFiles(Action<string> log = null, Action<int, string> progress = null)
        {
            if (!CurrentGameData.GameFiles.Any())
            {
                if (CurrentGameData.Cache && CacheExists(CurrentGameData.Id))
                {
                    log("Loading game file cache.");
                    CurrentGameData.GameFiles = GetCacheFiles(CurrentGameData.Id);
                    log("Game file cache loaded.");
                }
                else
                {
                    log("Scanning game files.");
                    var gameFiles = GetCurrentGameFolderFiles();

                    double i = 0, t = gameFiles.Count;
                    foreach (var file in gameFiles)
                    {
                        CurrentGameData.GameFiles.Add(new RootBuilderFileData
                        {
                            Path = file,
                            RelativePath = RelativePath(file, CurrentGameData.GamePath),
                            Hash = ComputeHash(file)
                        });
                        i++;
                        progress((int)(i / t * 100), $"Scanned {file}");
                    }
                    progress(0, $"Scanned {gameFiles.Count} game files.");

                    if (CurrentGameData.Cache)
                    {
                        log("Saving game data cache.");
                        SetCacheFiles(CurrentGameData.Id, CurrentGameData.GameFiles);
                    }
                    else
                    {
                        log("Checking for existing cache and deleting.");
                        ClearCachedFiles(CurrentGameData.Id);
                    }
                }
            }
        }
        private void ScanModFiles(Action<string> log = null, Action<int, string> progress = null)
        {
            log("Loading modlist.");
            var modlistPath = Path.Join(CurrentGameData.ProfilePath, "modlist.txt");
            if (File.Exists(modlistPath))
            {
                var modList = File.ReadAllLines(modlistPath)
                    .Where(x => x.StartsWith("+"))
                    .Select(x => x[1..])
                    .Reverse()
                    .ToList();
                log($"Found {modList.Count} active mods.");
                double i = 0, t = modList.Count;
                foreach (var mod in modList)
                {
                    var modRootPath = Path.Join(CurrentGameData.ModsPath, mod, "Root");
                    if (Directory.Exists(modRootPath))
                    {
                        var modFiles = Directory.GetFiles(modRootPath, "*", SearchOption.AllDirectories);
                        foreach (var file in modFiles)
                        {
                            var relativePath = RelativePath(file, modRootPath);
                            var currentData = CurrentGameData.ModFiles.FirstOrDefault(x => x.RelativePath == relativePath);
                            if (currentData == null)
                            {
                                currentData = new RootBuilderFileData { RelativePath = relativePath };
                                CurrentGameData.ModFiles.Add(currentData);
                            }
                            currentData.Path = file;
                            currentData.Hash = ComputeHash(file);
                        }
                    }
                    i++;
                    progress((int)(i / t * 100), $"Scanned {mod}");
                }

                log("Scanning overwrite.");
                var overwriteRoot = Path.Join(CurrentGameData.OverwritePath, "Root");
                if (Directory.Exists(overwriteRoot))
                {
                    var overwriteFiles = Directory.GetFiles(overwriteRoot, "*", SearchOption.AllDirectories);
                    i = 0; 
                    t = overwriteFiles.Count();
                    foreach (var file in overwriteFiles)
                    {
                        var relativePath = RelativePath(file, overwriteRoot);
                        var currentData = CurrentGameData.ModFiles.FirstOrDefault(x => x.RelativePath == relativePath);
                        if (currentData == null)
                        {
                            currentData = new RootBuilderFileData { RelativePath = relativePath };
                            CurrentGameData.ModFiles.Add(currentData);
                        }
                        currentData.Path = file;
                        currentData.Hash = ComputeHash(file);
                        i++;
                        progress((int)(i / t * 100), $"Scanned {relativePath}");
                    }
                }

                progress(0, $"Scanned {CurrentGameData.ModFiles.Count} mod files.");
            }
        }
        private void BackupGameFiles(Action<string> log = null, Action<int, string> progress = null)
        {
            if (CurrentGameData.Backup)
            {
                log("Backing up game files.");
                double i = 0, t = CurrentGameData.GameFiles.Count;
                foreach (var file in CurrentGameData.GameFiles)
                {
                    var backupPath = Path.Join(RootBuilderBackupPath(CurrentGameData.Id), file.RelativePath);
                    var backupDir = Directory.GetParent(backupPath);
                    if (!backupDir.Exists) backupDir.Create();
                    i++;
                    if (!File.Exists(backupPath))
                    {
                        File.Copy(file.Path, backupPath);
                        progress((int)(i / t * 100), $"Backed up {file.RelativePath}");
                    }
                }
                progress(0, $"Files backed up.");
            }
            else
            {
                log("Backing up conflicts.");
                var conflicts = CurrentGameData.GameFiles.Select(x => x.RelativePath)
                    .Intersect(CurrentGameData.ModFiles.Select(x => x.RelativePath))
                    .ToList();
                double i = 0, t = conflicts.Count;
                foreach (var file in conflicts)
                {
                    var gameFile = CurrentGameData.GameFiles.FirstOrDefault(x => x.RelativePath == file);
                    var backupPath = Path.Join(RootBuilderBackupPath(CurrentGameData.Id), file);
                    i++;
                    if (!File.Exists(backupPath))
                    {
                        var backupDir = Directory.GetParent(backupPath);
                        if (!backupDir.Exists) backupDir.Create();
                        File.Copy(gameFile.Path, backupPath, true);
                        progress((int)(i / t * 100), $"Backed up {file}");
                    }
                }
                log("Conflicts backed up.");
            }
        }
        private void DeployModFiles(Action<string> log = null, Action<int, string> progress = null)
        {
            log("Deploying mod files.");
            double i = 0, t = CurrentGameData.ModFiles.Count;
            foreach (var modFile in CurrentGameData.ModFiles)
            {
                var gamePath = Path.Join(CurrentGameData.GamePath, modFile.RelativePath);
                var gameParent = Directory.GetParent(gamePath);
                if (!gameParent.Exists)
                {
                    gameParent.Create();
                    CurrentGameData.CreatedDirectories.Add(gameParent.ToString());
                }
                File.Copy(modFile.Path, gamePath, true);
                i++;
                progress((int)(i / t * 100), $"Deployed {modFile.RelativePath}");
            }
            progress(0, "Mod files deployed.");
        }
        #endregion

        public void Sync(Action<string> log = null, Action<int, string> progress = null)
        {
            if (CurrentGameData.Built)
            {
                ScanModFiles(log, progress);

                log("Scanning game files.");
                var gameFiles = GetCurrentGameFolderFiles();

                double i = 0, t = gameFiles.Count;
                foreach (var file in gameFiles)
                {
                    var relativePath = RelativePath(file, CurrentGameData.GamePath);
                    i++;
                    // If the file is in the list of mod files and has changed, copy it back to the mod folder.
                    if (CurrentGameData.ModFiles.Any(x => x.RelativePath == relativePath))
                    {
                        var modFile = CurrentGameData.ModFiles.FirstOrDefault(x => x.RelativePath == relativePath);
                        var currentHash = ComputeHash(file);
                        if (currentHash != modFile.Hash)
                        {
                            modFile.Hash = currentHash;
                            File.Copy(file, modFile.Path, true);
                            progress((int)(i / t * 100), $"Updated: {relativePath}");
                        }
                    }
                    // Else if the file is in the list of game files and has changed and has a backup, copy it to the overwrite folder.
                    else if (CurrentGameData.GameFiles.Any(x => x.RelativePath == relativePath))
                    {
                        var gameFile = CurrentGameData.GameFiles.FirstOrDefault(x => x.RelativePath == relativePath);
                        var backupPath = Path.Join(RootBuilderBackupPath(CurrentGameId), relativePath);
                        if (File.Exists(backupPath) && ComputeHash(file) != gameFile.Hash)
                        {
                            var overwritePath = Path.Join(CurrentGameData.OverwritePath, "Root", relativePath);
                            var parentPath = Directory.GetParent(overwritePath);
                            if (!parentPath.Exists) parentPath.Create();
                            File.Copy(file, overwritePath, true);
                            progress((int)(i / t * 100), $"Overwrite (Changed): {relativePath}");
                        }
                    }
                    // If the file does not exist in either list, copy it back to the overwrite folder.
                    else
                    {
                        var overwritePath = Path.Join(CurrentGameData.OverwritePath, "Root", relativePath);
                        var parentPath = Directory.GetParent(overwritePath);
                        if (!parentPath.Exists) parentPath.Create();
                        File.Copy(file, overwritePath, true);
                        progress((int)(i / t * 100), $"Overwrite (New): {relativePath}");
                    }
                }
                progress(0, "Updated mod files.");
                SaveRootBuilderData();
            }
            else
            {
                log($"Not built.");
            }
        }
        public void Clear(Action<string> log = null, Action<int, string> progress = null)
        {
            if (CurrentGameData.Built)
            {
                // Sync the current files
                Sync(log, progress);

                // Get list of current game files
                log("Scanning game files.");
                var gameFiles = GetCurrentGameFolderFiles();

                double i = 0, t = gameFiles.Count;
                // Loop over list of current game files
                foreach (var file in gameFiles)
                {
                    var relativePath = RelativePath(file, CurrentGameData.GamePath);
                    i++;
                    if (CurrentGameData.GameFiles.Any(x => x.RelativePath == relativePath))
                    {
                        var gameFile = CurrentGameData.GameFiles.FirstOrDefault(x => x.RelativePath == relativePath);
                        var backupPath = Path.Join(RootBuilderBackupPath(CurrentGameId), relativePath);
                        if (File.Exists(backupPath) && ComputeHash(file) != gameFile.Hash)
                        {
                            // Restore any vanilla files that have changed.
                            try
                            {
                                File.Delete(file);
                                File.Copy(backupPath, file, true);
                                progress((int)(i / t * 100), $"Restored: {relativePath}");
                            }
                            catch (Exception e)
                            {
                                log($"Restore failed: {relativePath} Message: {e.Message}");
                            }
                        }
                    }
                    else
                    {
                        // Clear any new files.
                        try
                        {
                            File.Delete(file);
                            progress((int)(i / t * 100), $"Deleted: {relativePath}");
                        }
                        catch (Exception e)
                        {
                            log($"Delete failed: {relativePath} Message: {e.Message}");
                        }
                    }
                }
                progress(0, "Copied files deleted.");

                log("Deleting empty folders.");
                // Delete any created directories.
                if (CurrentGameData.CreatedDirectories != null)
                    foreach (var dir in CurrentGameData.CreatedDirectories)
                        if (Directory.Exists(dir))
                            try
                            {
                                Directory.Delete(dir, true);
                            }
                            catch (Exception e)
                            {
                                log($"Delete failed: {dir} Message: {e.Message}");
                            }
                log("Empty folders deleted.");

                if (!CurrentGameData.Backup)
                {
                    log("Deleting backup files.");
                    // Clear any backed up files
                    Directory.Delete(RootBuilderBackupPath(CurrentGameId), true);
                    log("Backup files deleted.");
                }

                CurrentGameData.GameFiles = new List<RootBuilderFileData>();
                CurrentGameData.ModFiles = new List<RootBuilderFileData>();
                CurrentGameData.CreatedDirectories = new List<string>();
                CurrentGameData.Built = false;
                SaveRootBuilderData();
                log("Root data cleared.");
            }
        }

        public Dictionary<string, string> GameList => RootBuilderData.GameData.ToDictionary(x => x.Id, x => $"{x.Name} ({x.GamePath})");
        public void Delete(string gameId)
        {
            var backupPath = RootBuilderBackupPath(gameId);
            if (Directory.Exists(backupPath)) Directory.Delete(backupPath, true);
            var cachePath = RootBuilderCachePath(gameId);
            if (File.Exists(cachePath)) File.Delete(cachePath);
            RootBuilderData.GameData.RemoveAll(x => x.Id == gameId);
            if (RootBuilderData.LastGameId == gameId) RootBuilderData.LastGameId = "";
        }
        private List<string> GetCurrentGameFolderFiles()
        {
            var gameFiles = Directory.GetFiles(CurrentGameData.GamePath, "*", SearchOption.TopDirectoryOnly).ToList();
            var gameFolders = Directory.GetDirectories(CurrentGameData.GamePath).ToList();
            foreach (var exc in RootBuilderData.Exclusions) gameFolders.Remove(Path.Join(CurrentGameData.GamePath, exc));
            foreach (var folder in gameFolders) gameFiles.AddRange(Directory.GetFiles(folder, "*", SearchOption.AllDirectories));
            foreach (var exc in RootBuilderData.Exclusions) gameFolders.Remove(Path.Join(CurrentGameData.GamePath, exc));
            return gameFiles;
        }

        #region Root Builder Data
        private readonly string _rootBuilderDataPath = Path.Join(RootBuilderExePath, "RootBuilderData.json");
        private RootBuilderData _rootBuilderData;
        private RootBuilderData RootBuilderData
        {
            get
            {
                if (_rootBuilderData != null) return _rootBuilderData;
                if (File.Exists(_rootBuilderDataPath)) _rootBuilderData = JsonConvert.DeserializeObject<RootBuilderData>(File.ReadAllText(_rootBuilderDataPath));
                else _rootBuilderData = new RootBuilderData();
                return _rootBuilderData;
            }
            set
            {
                _rootBuilderData = value;
                File.WriteAllText(_rootBuilderDataPath, JValue.Parse(JsonConvert.SerializeObject(_rootBuilderData)).ToString(Formatting.Indented));
            }
        }
        public void SaveRootBuilderData() => RootBuilderData = RootBuilderData;
        #endregion

        #region Root Builder Game Data
        public string IniPath;
        public RootBuilderGameData CurrentGameData => RootBuilderData.GameData.FirstOrDefault(x => x.Id == CurrentGameId);
        private string CurrentGameId => RootBuilderData.LastGameId;
        public bool Initialised => CurrentGameData != null;
        public void InitialiseFromIni(string iniPath, bool? cache = null, bool? backup = null)
        {
            if (File.Exists(iniPath))
            {
                var iniSettings = File.ReadAllLines(iniPath);

                var profileRegex = new Regex("selected_profile=@ByteArray\\((?<profile>[^\\)]*)\\)");
                var gamePathRegex = new Regex("gamePath=@ByteArray\\((?<gamePath>[^\\)]*)\\)");

                string game = string.Empty,
                    gamePath = string.Empty,
                    profile = string.Empty,
                    profilePath = string.Empty,
                    modsPath = string.Empty,
                    overwritePath = string.Empty,
                    basePath = Directory.GetParent(iniPath).ToString();

                foreach (var setting in iniSettings)
                {
                    if (setting.StartsWith("gameName="))
                        game = setting.Replace("gameName=", "");
                    if (profileRegex.IsMatch(setting))
                        profile = profileRegex.Match(setting).Groups["profile"].Value;
                    if (gamePathRegex.IsMatch(setting))
                        gamePath = Path.GetFullPath(gamePathRegex.Match(setting).Groups["gamePath"].Value);
                    if (setting.StartsWith("base_directory="))
                        basePath = setting.Replace("base_directory=", "");
                    if (setting.StartsWith("mod_directory="))
                        modsPath = setting.Replace("mod_directory=", "");
                    if (setting.StartsWith("profiles_directory="))
                        profilePath = setting.Replace("profiles_directory=", "");
                    if (setting.StartsWith("overwrite_directory="))
                        overwritePath = setting.Replace("overwrite_directory=", "");
                }

                if (modsPath.Contains("%BASE_DIR%")) modsPath = modsPath.Replace("%BASE_DIR%", basePath);
                if (profilePath.Contains("%BASE_DIR%")) profilePath = profilePath.Replace("%BASE_DIR%", basePath);
                if (overwritePath.Contains("%BASE_DIR%")) overwritePath = overwritePath.Replace("%BASE_DIR%", basePath);

                if (string.IsNullOrWhiteSpace(profile)) profile = "Default";
                if (string.IsNullOrWhiteSpace(modsPath)) modsPath = Path.Join(basePath, "mods");
                if (string.IsNullOrWhiteSpace(profilePath)) profilePath = Path.Join(basePath, "profiles");
                if (string.IsNullOrWhiteSpace(overwritePath)) overwritePath = Path.Join(basePath, "overwrite");

                var currentProfilePath = Path.Join(profilePath, profile);
                var gameId = FileSafePath(gamePath);
                var gameData = new RootBuilderGameData { Id = gameId };
                if (RootBuilderData.GameData.Any(x => x.Id == gameId))
                {
                    gameData = RootBuilderData.GameData.FirstOrDefault(x => x.Id == gameId);
                }
                else
                {
                    RootBuilderData.GameData.Add(gameData);
                }

                gameData.Name = game;
                gameData.Profile = profile;
                gameData.MOIniPath = Path.GetFullPath(iniPath);
                gameData.ProfilePath = Path.GetFullPath(currentProfilePath);
                gameData.ModsPath = Path.GetFullPath(modsPath);
                gameData.GamePath = gamePath;
                gameData.OverwritePath = Path.GetFullPath(overwritePath);

                gameData.Cache = cache.HasValue ? cache.Value : gameData.Cache;
                gameData.Backup = backup.HasValue ? backup.Value : gameData.Backup;

                RootBuilderData.LastGameId = gameId;
                SaveRootBuilderData();
            }
        }
        public void InitialiseFromId(string gameId)
        {
            var game = RootBuilderData.GameData.FirstOrDefault(x => x.Id == gameId);
            if (game != null) InitialiseFromIni(game.MOIniPath, game.Cache, game.Backup);
        }

        #endregion

        #region Root Backups
        private readonly string _rootBuilderBackupPath = Path.Join(RootBuilderExePath, ".rootbuilder");
        private string RootBuilderBackupPath(string gameId) => Path.Join(_rootBuilderBackupPath, gameId);
        private string RootBuilderCachePath(string gameId) => Path.Join(_rootBuilderBackupPath, $"{gameId}.json");
        #endregion

        #region Game Data Cache
        private bool CacheExists(string gameId) => File.Exists(RootBuilderCachePath(gameId));
        private List<RootBuilderFileData> GetCacheFiles(string gameId) => JsonConvert.DeserializeObject<List<RootBuilderFileData>>(File.ReadAllText(RootBuilderCachePath(gameId)));
        private void SetCacheFiles(string gameId, List<RootBuilderFileData> files) => File.WriteAllText(RootBuilderCachePath(gameId), JValue.Parse(JsonConvert.SerializeObject(files)).ToString(Formatting.Indented));
        private void ClearCachedFiles(string gameId)
        {
            if (File.Exists(RootBuilderCachePath(gameId)))
                File.Delete(RootBuilderCachePath(gameId));
        }
        #endregion

        #region Path Helpers
        private static readonly string RootBuilderExePath = Path.GetDirectoryName(Process.GetCurrentProcess().MainModule.FileName);
        private string RelativePath(string path, string rootPath)
        {
            var sPath = SplitPath(path);
            var rPath = SplitPath(rootPath);
            var resPath = string.Empty;
            var changed = false;
            for (int i = 0; i < sPath.Length; i++)
            {
                if (changed || rPath.Length <= i || !string.Equals(sPath[i], rPath[i], StringComparison.InvariantCultureIgnoreCase))
                {
                    changed = true;
                    resPath = Path.Join(resPath, sPath[i]);
                }

            }

            return resPath;
        }
        private string FileSafePath(string path) => string.Join('_', SplitPath(path)).Replace(":", "").Replace(".", "_").Replace(" ", "_");
        private string[] SplitPath(string path) => Path.GetFullPath(path).Split(new char[] { '/', '\\' });
        #endregion

        #region Hash
        private static string ComputeHash(string path)
        {
            using var md5 = MD5.Create();
            using var stream = File.OpenRead(path);
            return Convert.ToBase64String(md5.ComputeHash(stream));
        }
        #endregion
    }
}
