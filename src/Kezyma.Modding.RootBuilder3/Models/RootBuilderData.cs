using System;
using System.Collections.Generic;
using System.Text;

namespace Kezyma.Modding.RootBuilder3.Models
{
    public class RootBuilderData
    {
        public RootBuilderData()
        {
            GameData = new List<RootBuilderGameData>();
        }

        public List<RootBuilderGameData> GameData { get; set; }

        public string[] Exclusions { get; set; } = { "Data", "Data Files", "Saves", "Morrowind.ini" };
        public string LastGameId { get; set; }
    }
}
