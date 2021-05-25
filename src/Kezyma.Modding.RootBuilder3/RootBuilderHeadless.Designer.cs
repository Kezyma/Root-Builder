
namespace Kezyma.Modding.RootBuilder3
{
    partial class RootBuilderHeadless
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
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
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.lstLog = new System.Windows.Forms.ListBox();
            this.strStatus = new System.Windows.Forms.StatusStrip();
            this.prgBarStatus = new System.Windows.Forms.ToolStripProgressBar();
            this.lblBarStatus = new System.Windows.Forms.ToolStripStatusLabel();
            this.clearWorker = new System.ComponentModel.BackgroundWorker();
            this.syncWorker = new System.ComponentModel.BackgroundWorker();
            this.buildWorker = new System.ComponentModel.BackgroundWorker();
            this.strStatus.SuspendLayout();
            this.SuspendLayout();
            // 
            // lstLog
            // 
            this.lstLog.Dock = System.Windows.Forms.DockStyle.Top;
            this.lstLog.FormattingEnabled = true;
            this.lstLog.ItemHeight = 15;
            this.lstLog.Location = new System.Drawing.Point(0, 0);
            this.lstLog.Name = "lstLog";
            this.lstLog.SelectionMode = System.Windows.Forms.SelectionMode.None;
            this.lstLog.Size = new System.Drawing.Size(642, 184);
            this.lstLog.TabIndex = 0;
            // 
            // strStatus
            // 
            this.strStatus.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.prgBarStatus,
            this.lblBarStatus});
            this.strStatus.Location = new System.Drawing.Point(0, 183);
            this.strStatus.Name = "strStatus";
            this.strStatus.Size = new System.Drawing.Size(642, 22);
            this.strStatus.SizingGrip = false;
            this.strStatus.TabIndex = 18;
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
            // clearWorker
            // 
            this.clearWorker.WorkerReportsProgress = true;
            this.clearWorker.WorkerSupportsCancellation = true;
            this.clearWorker.DoWork += new System.ComponentModel.DoWorkEventHandler(this.clearWorker_DoWork);
            this.clearWorker.ProgressChanged += new System.ComponentModel.ProgressChangedEventHandler(this.clearWorker_ProgressChanged);
            this.clearWorker.RunWorkerCompleted += new System.ComponentModel.RunWorkerCompletedEventHandler(this.clearWorker_RunWorkerCompleted);
            // 
            // syncWorker
            // 
            this.syncWorker.WorkerReportsProgress = true;
            this.syncWorker.WorkerSupportsCancellation = true;
            this.syncWorker.DoWork += new System.ComponentModel.DoWorkEventHandler(this.syncWorker_DoWork);
            this.syncWorker.ProgressChanged += new System.ComponentModel.ProgressChangedEventHandler(this.syncWorker_ProgressChanged);
            this.syncWorker.RunWorkerCompleted += new System.ComponentModel.RunWorkerCompletedEventHandler(this.syncWorker_RunWorkerCompleted);
            // 
            // buildWorker
            // 
            this.buildWorker.WorkerReportsProgress = true;
            this.buildWorker.WorkerSupportsCancellation = true;
            this.buildWorker.DoWork += new System.ComponentModel.DoWorkEventHandler(this.buildWorker_DoWork);
            this.buildWorker.ProgressChanged += new System.ComponentModel.ProgressChangedEventHandler(this.buildWorker_ProgressChanged);
            this.buildWorker.RunWorkerCompleted += new System.ComponentModel.RunWorkerCompletedEventHandler(this.buildWorker_RunWorkerCompleted);
            // 
            // RootBuilderHeadless
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(642, 205);
            this.Controls.Add(this.strStatus);
            this.Controls.Add(this.lstLog);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow;
            this.Name = "RootBuilderHeadless";
            this.SizeGripStyle = System.Windows.Forms.SizeGripStyle.Hide;
            this.Text = "Kezyma\'s Root Builder for Mod Organizer 2";
            this.Load += new System.EventHandler(this.RootBuilderHeadless_Load);
            this.strStatus.ResumeLayout(false);
            this.strStatus.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ListBox lstLog;
        private System.Windows.Forms.StatusStrip strStatus;
        private System.Windows.Forms.ToolStripProgressBar prgBarStatus;
        public System.Windows.Forms.ToolStripStatusLabel lblBarStatus;
        private System.ComponentModel.BackgroundWorker clearWorker;
        private System.ComponentModel.BackgroundWorker syncWorker;
        private System.ComponentModel.BackgroundWorker buildWorker;
    }
}