using System;
using System.Collections.Generic;
using System.Text;

namespace Kezyma.Modding.RootBuilder3.Models
{
    public class RootBuilderGameData
    {
        public RootBuilderGameData()
        {
            GameFiles = new List<RootBuilderFileData>();
            ModFiles = new List<RootBuilderFileData>();
            CreatedDirectories = new List<string>();
            Backup = false;
            Cache = false;
            Built = false;
        }

        public string Id { get; set; }
        public string Name { get; set; }
        public string GamePath { get; set; }
        public string ModsPath { get; set; }
        public string MOIniPath { get; set; }
        public string ProfilePath { get; set; }
        public string Profile { get; set; }
        public string OverwritePath { get; set; }
        public bool Backup { get; set; }
        public bool Cache { get; set; }
        public bool Built { get; set; }
        public string Icon { get; set; }

        public List<RootBuilderFileData> GameFiles { get; set; }
        public List<RootBuilderFileData> ModFiles { get; set; }
        public List<string> CreatedDirectories { get; set; }
    }
}
