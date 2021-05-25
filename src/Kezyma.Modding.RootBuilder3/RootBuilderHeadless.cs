using Kezyma.Modding.RootBuilder3.Enumerations;
using Kezyma.Modding.RootBuilder3.Helpers;
using Kezyma.Modding.RootBuilder3.Utility;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Kezyma.Modding.RootBuilder3
{
    public partial class RootBuilderHeadless : Form
    {
        public RootBuilderHeadless(RootBuilder rootBuilder, RunType runType, bool debug = false)
        {
            _rootBuilder = rootBuilder;
            _debug = debug;
            _runType = runType;
            LogWriter.ClearLog();
            InitializeComponent();
        }

        private readonly RootBuilder _rootBuilder;
        private readonly bool _debug;
        private readonly RunType _runType;

        private void Log(string message)
        {
            lblBarStatus.Text = message;
            lstLog.Items.Add(message);
            lstLog.TopIndex = lstLog.Items.Count - 1;
            LogWriter.Log(message);
        }

        private void Progress(int progress, string message)
        {
            var state = 1;
            if (message.Contains("failed", StringComparison.InvariantCultureIgnoreCase)) state = 2;

            prgBarStatus.Value = progress;
            prgBarStatus.ProgressBar.SetState(state);
            Log($"{(progress > 0 ? $"{progress}% " : "")}{message}");
        }

        private void buildWorker_ProgressChanged(object sender, ProgressChangedEventArgs e) => Progress(e.ProgressPercentage, e.UserState.ToString());
        private void syncWorker_ProgressChanged(object sender, ProgressChangedEventArgs e) => Progress(e.ProgressPercentage, e.UserState.ToString());
        private void clearWorker_ProgressChanged(object sender, ProgressChangedEventArgs e) => Progress(e.ProgressPercentage, e.UserState.ToString());

        private void buildWorker_DoWork(object sender, DoWorkEventArgs e)
            => _rootBuilder.Build(
                (message) => buildWorker.ReportProgress(0, message),
                (progress, message) => buildWorker.ReportProgress(progress, message));
        private void syncWorker_DoWork(object sender, DoWorkEventArgs e)
            => _rootBuilder.Sync(
                (message) => syncWorker.ReportProgress(0, message),
                (progress, message) => syncWorker.ReportProgress(progress, message));
        private void clearWorker_DoWork(object sender, DoWorkEventArgs e)
            => _rootBuilder.Clear(
                (message) => clearWorker.ReportProgress(0, message),
                (progress, message) => clearWorker.ReportProgress(progress, message));

        private void buildWorker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            if (e.Error != null) Log("Build failed. Check log file.");
            else Log("Build complete.");
            if (!_debug) Close();
        }
        private void syncWorker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            if (e.Error != null) Log("Sync failed. Check log file.");
            else Log("Sync complete.");
            if (!_debug) Close();
        }
        private void clearWorker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            if (e.Error != null) Log("Clear failed. Check log file.");
            else Log("Clear complete.");
            if (!_debug) Close();
        }

        private void RootBuilderHeadless_Load(object sender, EventArgs e)
        {
            switch (_runType)
            {
                case RunType.Build:
                    buildWorker.RunWorkerAsync();
                    break;
                case RunType.Sync:
                    syncWorker.RunWorkerAsync();
                    break;
                case RunType.Clear:
                    clearWorker.RunWorkerAsync();
                    break;
            }
        }
    }
}
