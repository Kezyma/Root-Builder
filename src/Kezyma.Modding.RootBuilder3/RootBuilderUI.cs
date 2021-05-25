using Kezyma.Modding.RootBuilder3.Enumerations;
using Kezyma.Modding.RootBuilder3.Helpers;
using Kezyma.Modding.RootBuilder3.Utility;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Kezyma.Modding.RootBuilder3
{
    public partial class RootBuilderUI : Form
    {
        public RootBuilderUI(RootBuilder rootBuilder)
        {
            _rootBuilder = rootBuilder;
            InitializeComponent();
            BindGamePicker();
            InitialiseUI();
            lstLog.Visible = false;
            Height -= lstLog.Height;
        }

        private RootBuilder _rootBuilder;

        private void Log(string message)
        {
            lblBarStatus.Text = message;
            lstLog.Items.Add(message);
            lstLog.TopIndex = lstLog.Items.Count - 1;
        }

        private void Progress(int progress, string message)
        {
            var state = 1;
            if (message.Contains("failed", StringComparison.InvariantCultureIgnoreCase)) state = 2;

            prgBarStatus.Value = progress;
            prgBarStatus.ProgressBar.SetState(state);
            Log(message);
        }
        private void buildWorker_ProgressChanged(object sender, ProgressChangedEventArgs e) => Progress(e.ProgressPercentage, e.UserState.ToString());
        private void syncWorker_ProgressChanged(object sender, ProgressChangedEventArgs e) => Progress(e.ProgressPercentage, e.UserState.ToString());
        private void clearWorker_ProgressChanged(object sender, ProgressChangedEventArgs e) => Progress(e.ProgressPercentage, e.UserState.ToString());

        private void BindGamePicker()
        {
            if (_rootBuilder.GameList.Any())
            {
                ddlSelectedGame.SelectedIndexChanged -= new EventHandler(ddlSelectedGame_SelectedIndexChanged);
                ddlSelectedGame.DataSource = new BindingSource(_rootBuilder.GameList, null);
                ddlSelectedGame.DisplayMember = "Value";
                ddlSelectedGame.ValueMember = "Key";
                ddlSelectedGame.SelectedIndexChanged += new EventHandler(ddlSelectedGame_SelectedIndexChanged);
            }
        }

        private void InitialiseUI()
        {
            if (_rootBuilder.Initialised)
            {
                EnableInputs(true);
                chkBackup.Checked = _rootBuilder.CurrentGameData.Backup;
                chkCache.Checked = _rootBuilder.CurrentGameData.Cache;
                lblGamePath.Text = $"Game: {_rootBuilder.CurrentGameData.GamePath}";
                lblMOProfile.Text = $"Profile: {_rootBuilder.CurrentGameData.Profile}";
                lblMOini.Text = _rootBuilder.CurrentGameData.MOIniPath;
                ddlSelectedGame.SelectedItem = _rootBuilder.GameList.First(x => x.Key == _rootBuilder.CurrentGameData.Id);
            }
            else
            {
                EnableInputs(false);
                lblGamePath.Text = $"Game: ...";
                lblMOProfile.Text = $"Profile: ...";
                lblMOini.Text = "...";
                ddlSelectedGame.SelectedItem = null;
            }
            btnSelectMOini.Enabled = true;
        }
        private void EnableInputs(bool enabled)
        {
            btnDelete.Enabled = enabled;
            btnSelectMOini.Enabled = enabled;
            btnBuild.Enabled = enabled;
            btnSync.Enabled = _rootBuilder.CurrentGameData?.Built ?? false;
            btnClear.Enabled = _rootBuilder.CurrentGameData?.Built ?? false;
            chkBackup.Enabled = enabled;
            chkCache.Enabled = enabled;
        }
        private void btnSelectMOini_Click(object sender, EventArgs e)
        {
            using var fs = new OpenFileDialog();
            var res = fs.ShowDialog();
            if (res == DialogResult.OK)
            {
                var iniFile = fs.FileName;
                _rootBuilder.InitialiseFromIni(iniFile);
                BindGamePicker();
                InitialiseUI();
            }
        }

        private void btnSync_Click(object sender, EventArgs e) { EnableInputs(false); syncWorker.RunWorkerAsync(); }
        private void btnBuild_Click(object sender, EventArgs e) { EnableInputs(false); buildWorker.RunWorkerAsync(); }
        private void btnClear_Click(object sender, EventArgs e) { EnableInputs(false); clearWorker.RunWorkerAsync(); }

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

        private void buildWorker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e) { EnableInputs(true); Log("Build Complete"); }
        private void syncWorker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e) { EnableInputs(true); Log("Sync Complete"); }
        private void clearWorker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e) { EnableInputs(true); Log("Clear Complete"); }

        private void chkCache_CheckedChanged(object sender, EventArgs e)
        {
            _rootBuilder.CurrentGameData.Cache = chkCache.Checked;
            _rootBuilder.SaveRootBuilderData();
        }
        private void chkBackup_CheckedChanged(object sender, EventArgs e)
        {
            _rootBuilder.CurrentGameData.Backup = chkBackup.Checked;
            _rootBuilder.SaveRootBuilderData();
        }

        private void btnShowLog_Click(object sender, EventArgs e)
        {
            lstLog.Visible = !lstLog.Visible;
            if (lstLog.Visible) Height += lstLog.Height;
            else Height -= lstLog.Height;
        }

        private void ddlSelectedGame_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (ddlSelectedGame.SelectedItem is KeyValuePair<string, string>)
                _rootBuilder.InitialiseFromId(((KeyValuePair<string, string>)ddlSelectedGame.SelectedItem).Key);
            InitialiseUI();
        }

        private void btnDelete_Click(object sender, EventArgs e)
        {
            var confirm = MessageBox.Show("Are you sure you want to delete this configuration? This will delete all information relating to this game.", $"Are you sure?", MessageBoxButtons.YesNo);
            if (confirm == DialogResult.Yes)
            {
                _rootBuilder.Delete(((KeyValuePair<string, string>)ddlSelectedGame.SelectedItem).Key);
                BindGamePicker();
                InitialiseUI();
            }
        }
    }
}
