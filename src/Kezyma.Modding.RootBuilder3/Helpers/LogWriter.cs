using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;

namespace Kezyma.Modding.RootBuilder3.Helpers
{
    public static class LogWriter
    {
        public static void Log(string message)
        {
            if (!File.Exists(LogFile))
                File.WriteAllText(LogFile, message);
            else File.AppendAllLines(LogFile, new[] { message });
        }

        public static void ClearLog()
        {
            if (File.Exists(LogFile))
                File.WriteAllText(LogFile, "");
        }

        private static readonly string ExePath = Path.GetDirectoryName(Process.GetCurrentProcess().MainModule.FileName);
        private static readonly string LogFile = Path.Join(ExePath, "RootBuilder.log");
    }
}
