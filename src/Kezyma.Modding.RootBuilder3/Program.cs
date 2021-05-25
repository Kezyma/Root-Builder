using Kezyma.Modding.RootBuilder3.Enumerations;
using Kezyma.Modding.RootBuilder3.Helpers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Kezyma.Modding.RootBuilder3
{
    static class Program
    {
        /// <summary>
        ///  The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main(string[] args)
        {
            string iniPath = string.Empty,
                lastArg = string.Empty;
            bool? cache = null,
                backup = null;
            bool debug = false;
            var mode = RunType.GUI;

            foreach (var arg in args)
            {
                if (lastArg == "-ini") iniPath = arg;
                if (arg == "-build") mode = RunType.Build;
                if (arg == "-clear") mode = RunType.Clear;
                if (arg == "-sync") mode = RunType.Sync;
                if (arg == "-cache") cache = true;
                if (arg == "-backup") backup = true;
                if (arg == "-debug") debug = true;
                lastArg = arg;
            }

            var rb = new RootBuilder(iniPath, cache, backup, debug);
            switch (mode)
            {
                case RunType.GUI:
                    Application.SetHighDpiMode(HighDpiMode.SystemAware);
                    Application.EnableVisualStyles();
                    Application.SetCompatibleTextRenderingDefault(false);
                    Application.Run(new RootBuilderUI(rb));
                    break;
                default:
                    Application.SetHighDpiMode(HighDpiMode.SystemAware);
                    Application.EnableVisualStyles();
                    Application.SetCompatibleTextRenderingDefault(false);
                    Application.Run(new RootBuilderHeadless(rb, mode, debug));
                    break;
                
            }
        }
    }
}
