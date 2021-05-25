
namespace Kezyma.Modding.RootBuilder3
{
    partial class RootBuilderUI
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(RootBuilderUI));
            this.strStatus = new System.Windows.Forms.StatusStrip();
            this.prgBarStatus = new System.Windows.Forms.ToolStripProgressBar();
            this.lblBarStatus = new System.Windows.Forms.ToolStripStatusLabel();
            this.btnBuild = new System.Windows.Forms.Button();
            this.btnClear = new System.Windows.Forms.Button();
            this.chkCache = new System.Windows.Forms.CheckBox();
            this.chkBackup = new System.Windows.Forms.CheckBox();
            this.btnSelectMOini = new System.Windows.Forms.Button();
            this.lblMOini = new System.Windows.Forms.Label();
            this.lblGamePath = new System.Windows.Forms.Label();
            this.lblMOProfile = new System.Windows.Forms.Label();
            this.btnSync = new System.Windows.Forms.Button();
            this.buildWorker = new System.ComponentModel.BackgroundWorker();
            this.syncWorker = new System.ComponentModel.BackgroundWorker();
            this.clearWorker = new System.ComponentModel.BackgroundWorker();
            this.lstLog = new System.Windows.Forms.ListBox();
            this.btnShowLog = new System.Windows.Forms.Button();
            this.ddlSelectedGame = new System.Windows.Forms.ComboBox();
            this.btnDelete = new System.Windows.Forms.Button();
            this.icnCurrentGame = new System.Windows.Forms.PictureBox();
            this.strStatus.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.icnCurrentGame)).BeginInit();
            this.SuspendLayout();
            // 
            // strStatus
            // 
            this.strStatus.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.prgBarStatus,
            this.lblBarStatus});
            this.strStatus.Location = new System.Drawing.Point(0, 269);
            this.strStatus.Name = "strStatus";
            this.strStatus.Size = new System.Drawing.Size(581, 22);
            this.strStatus.SizingGrip = false;
            this.strStatus.TabIndex = 17;
            this.strStatus.Text = "...";
            // 
            // prgBarStatus
            // 
            this.prgBarStatus.Alignment = System.Windows.Forms.ToolStripItemAlignment.Right;
            this.prgBarStatus.Name = "prgBarStatus";
            this.prgBarStatus.Size = new System.Drawing.Size(100, 16);
            // 
            // lblBarStatus
            // 
            this.lblBarStatus.Name = "lblBarStatus";
            this.lblBarStatus.Size = new System.Drawing.Size(16, 17);
            this.lblBarStatus.Text = "...";
            // 
            // btnBuild
            // 
            this.btnBuild.Location = new System.Drawing.Point(12, 101);
            this.btnBuild.Name = "btnBuild";
            this.btnBuild.Size = new System.Drawing.Size(75, 23);
            this.btnBuild.TabIndex = 18;
            this.btnBuild.Text = "Build";
            this.btnBuild.UseVisualStyleBackColor = true;
            this.btnBuild.Click += new System.EventHandler(this.btnBuild_Click);
            // 
            // btnClear
            // 
            this.btnClear.Location = new System.Drawing.Point(174, 101);
            this.btnClear.Name = "btnClear";
            this.btnClear.Size = new System.Drawing.Size(75, 23);
            this.btnClear.TabIndex = 19;
            this.btnClear.Text = "Clear";
            this.btnClear.UseVisualStyleBackColor = true;
            this.btnClear.Click += new System.EventHandler(this.btnClear_Click);
            // 
            // chkCache
            // 
            this.chkCache.AutoSize = true;
            this.chkCache.Location = new System.Drawing.Point(255, 104);
            this.chkCache.Name = "chkCache";
            this.chkCache.Size = new System.Drawing.Size(59, 19);
            this.chkCache.TabIndex = 20;
            this.chkCache.Text = "Cache";
            this.chkCache.UseVisualStyleBackColor = true;
            this.chkCache.CheckedChanged += new System.EventHandler(this.chkCache_CheckedChanged);
            // 
            // chkBackup
            // 
            this.chkBackup.AutoSize = true;
            this.chkBackup.Location = new System.Drawing.Point(320, 104);
            this.chkBackup.Name = "chkBackup";
            this.chkBackup.Size = new System.Drawing.Size(65, 19);
            this.chkBackup.TabIndex = 21;
            this.chkBackup.Text = "Backup";
            this.chkBackup.UseVisualStyleBackColor = true;
            this.chkBackup.CheckedChanged += new System.EventHandler(this.chkBackup_CheckedChanged);
            // 
            // btnSelectMOini
            // 
            this.btnSelectMOini.Location = new System.Drawing.Point(12, 42);
            this.btnSelectMOini.Name = "btnSelectMOini";
            this.btnSelectMOini.Size = new System.Drawing.Size(146, 23);
            this.btnSelectMOini.TabIndex = 30;
            this.btnSelectMOini.Text = "Mod Organizer ini";
            this.btnSelectMOini.UseVisualStyleBackColor = true;
            this.btnSelectMOini.Click += new System.EventHandler(this.btnSelectMOini_Click);
            // 
            // lblMOini
            // 
            this.lblMOini.AutoSize = true;
            this.lblMOini.Location = new System.Drawing.Point(164, 46);
            this.lblMOini.Name = "lblMOini";
            this.lblMOini.Size = new System.Drawing.Size(16, 15);
            this.lblMOini.TabIndex = 31;
            this.lblMOini.Text = "...";
            // 
            // lblGamePath
            // 
            this.lblGamePath.AutoSize = true;
            this.lblGamePath.Location = new System.Drawing.Point(12, 68);
            this.lblGamePath.Name = "lblGamePath";
            this.lblGamePath.Size = new System.Drawing.Size(53, 15);
            this.lblGamePath.TabIndex = 32;
            this.lblGamePath.Text = "Game: ...";
            // 
            // lblMOProfile
            // 
            this.lblMOProfile.AutoSize = true;
            this.lblMOProfile.Location = new System.Drawing.Point(12, 83);
            this.lblMOProfile.Name = "lblMOProfile";
            this.lblMOProfile.Size = new System.Drawing.Size(56, 15);
            this.lblMOProfile.TabIndex = 33;
            this.lblMOProfile.Text = "Profile: ...";
            // 
            // btnSync
            // 
            this.btnSync.Location = new System.Drawing.Point(93, 101);
            this.btnSync.Name = "btnSync";
            this.btnSync.Size = new System.Drawing.Size(75, 23);
            this.btnSync.TabIndex = 34;
            this.btnSync.Text = "Sync";
            this.btnSync.UseVisualStyleBackColor = true;
            this.btnSync.Click += new System.EventHandler(this.btnSync_Click);
            // 
            // buildWorker
            // 
            this.buildWorker.WorkerReportsProgress = true;
            this.buildWorker.WorkerSupportsCancellation = true;
            this.buildWorker.DoWork += new System.ComponentModel.DoWorkEventHandler(this.buildWorker_DoWork);
            this.buildWorker.ProgressChanged += new System.ComponentModel.ProgressChangedEventHandler(this.buildWorker_ProgressChanged);
            this.buildWorker.RunWorkerCompleted += new System.ComponentModel.RunWorkerCompletedEventHandler(this.buildWorker_RunWorkerCompleted);
            // 
            // syncWorker
            // 
            this.syncWorker.WorkerReportsProgress = true;
            this.syncWorker.WorkerSupportsCancellation = true;
            this.syncWorker.DoWork += new System.ComponentModel.DoWorkEventHandler(this.syncWorker_DoWork);
            this.syncWorker.ProgressChanged += new System.ComponentModel.ProgressChangedEventHandler(this.syncWorker_ProgressChanged);
            this.syncWorker.RunWorkerCompleted += new System.ComponentModel.RunWorkerCompletedEventHandler(this.syncWorker_RunWorkerCompleted);
            // 
            // clearWorker
            // 
            this.clearWorker.WorkerReportsProgress = true;
            this.clearWorker.WorkerSupportsCancellation = true;
            this.clearWorker.DoWork += new System.ComponentModel.DoWorkEventHandler(this.clearWorker_DoWork);
            this.clearWorker.ProgressChanged += new System.ComponentModel.ProgressChangedEventHandler(this.clearWorker_ProgressChanged);
            this.clearWorker.RunWorkerCompleted += new System.ComponentModel.RunWorkerCompletedEventHandler(this.clearWorker_RunWorkerCompleted);
            // 
            // lstLog
            // 
            this.lstLog.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.lstLog.FormattingEnabled = true;
            this.lstLog.ItemHeight = 15;
            this.lstLog.Location = new System.Drawing.Point(0, 130);
            this.lstLog.Name = "lstLog";
            this.lstLog.SelectionMode = System.Windows.Forms.SelectionMode.None;
            this.lstLog.Size = new System.Drawing.Size(581, 139);
            this.lstLog.TabIndex = 35;
            // 
            // btnShowLog
            // 
            this.btnShowLog.Location = new System.Drawing.Point(530, 101);
            this.btnShowLog.Name = "btnShowLog";
            this.btnShowLog.Size = new System.Drawing.Size(39, 23);
            this.btnShowLog.TabIndex = 36;
            this.btnShowLog.Text = "Log";
            this.btnShowLog.UseVisualStyleBackColor = true;
            this.btnShowLog.Click += new System.EventHandler(this.btnShowLog_Click);
            // 
            // ddlSelectedGame
            // 
            this.ddlSelectedGame.FormattingEnabled = true;
            this.ddlSelectedGame.Location = new System.Drawing.Point(41, 13);
            this.ddlSelectedGame.Name = "ddlSelectedGame";
            this.ddlSelectedGame.Size = new System.Drawing.Size(447, 23);
            this.ddlSelectedGame.TabIndex = 37;
            this.ddlSelectedGame.SelectedIndexChanged += new System.EventHandler(this.ddlSelectedGame_SelectedIndexChanged);
            // 
            // btnDelete
            // 
            this.btnDelete.Location = new System.Drawing.Point(494, 13);
            this.btnDelete.Name = "btnDelete";
            this.btnDelete.Size = new System.Drawing.Size(75, 23);
            this.btnDelete.TabIndex = 38;
            this.btnDelete.Text = "Delete";
            this.btnDelete.UseVisualStyleBackColor = true;
            this.btnDelete.Click += new System.EventHandler(this.btnDelete_Click);
            // 
            // icnCurrentGame
            // 
            this.icnCurrentGame.Location = new System.Drawing.Point(12, 13);
            this.icnCurrentGame.Name = "icnCurrentGame";
            this.icnCurrentGame.Size = new System.Drawing.Size(23, 23);
            this.icnCurrentGame.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.icnCurrentGame.TabIndex = 39;
            this.icnCurrentGame.TabStop = false;
            // 
            // RootBuilderUI
            // 
            this.AcceptButton = this.btnBuild;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.ClientSize = new System.Drawing.Size(581, 291);
            this.Controls.Add(this.icnCurrentGame);
            this.Controls.Add(this.btnDelete);
            this.Controls.Add(this.ddlSelectedGame);
            this.Controls.Add(this.btnShowLog);
            this.Controls.Add(this.lstLog);
            this.Controls.Add(this.btnSync);
            this.Controls.Add(this.lblMOProfile);
            this.Controls.Add(this.lblGamePath);
            this.Controls.Add(this.lblMOini);
            this.Controls.Add(this.btnSelectMOini);
            this.Controls.Add(this.chkBackup);
            this.Controls.Add(this.chkCache);
            this.Controls.Add(this.btnClear);
            this.Controls.Add(this.btnBuild);
            this.Controls.Add(this.strStatus);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.Name = "RootBuilderUI";
            this.SizeGripStyle = System.Windows.Forms.SizeGripStyle.Hide;
            this.Text = "Kezyma\'s Root Builder for Mod Organizer 2";
            this.strStatus.ResumeLayout(false);
            this.strStatus.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.icnCurrentGame)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.StatusStrip strStatus;
        private System.Windows.Forms.ToolStripProgressBar prgBarStatus;
        public System.Windows.Forms.ToolStripStatusLabel lblBarStatus;
        private System.Windows.Forms.Button btnBuild;
        private System.Windows.Forms.Button btnClear;
        private System.Windows.Forms.CheckBox chkCache;
        private System.Windows.Forms.CheckBox chkBackup;
        private System.Windows.Forms.Button btnSelectMOini;
        private System.Windows.Forms.Label lblMOini;
        private System.Windows.Forms.Label lblGamePath;
        private System.Windows.Forms.Label lblMOProfile;
        private System.Windows.Forms.Button btnSync;
        private System.ComponentModel.BackgroundWorker buildWorker;
        private System.ComponentModel.BackgroundWorker syncWorker;
        private System.ComponentModel.BackgroundWorker clearWorker;
        private System.Windows.Forms.ListBox lstLog;
        private System.Windows.Forms.Button btnShowLog;
        private System.Windows.Forms.ComboBox ddlSelectedGame;
        private System.Windows.Forms.Button btnDelete;
        private System.Windows.Forms.PictureBox icnCurrentGame;
    }
}

