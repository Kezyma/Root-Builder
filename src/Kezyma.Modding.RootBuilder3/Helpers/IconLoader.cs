using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Text;

namespace Kezyma.Modding.RootBuilder3.Helpers
{
    public class IconLoader
    {
        public IconLoader(string[] searchedFiles)
        {
            _searchedFiles = searchedFiles;
        }

        private string[] _searchedFiles;

        public Icon GetIconForPath(string gamePath, string defaultFile)
        {
            foreach (var search in _searchedFiles)
            {
                var path = Path.Join(gamePath, search);
                if (File.Exists(path))
                    return Icon.ExtractAssociatedIcon(path);
            }
            if (File.Exists(defaultFile))
                return Icon.ExtractAssociatedIcon(defaultFile);
            else return SystemIcons.WinLogo;
        }
    }
}
