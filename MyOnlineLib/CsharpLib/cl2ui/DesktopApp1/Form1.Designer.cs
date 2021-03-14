namespace DesktopApp1
{
    partial class Form1
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
            this.TxtLink_linkLabel1 = new System.Windows.Forms.LinkLabel();
            this.debugInstructionsLabel = new System.Windows.Forms.Label();
            this.Heading = new System.Windows.Forms.Label();
            this.Bt_Exit = new System.Windows.Forms.Button();
            this.label_st = new System.Windows.Forms.Label();
            this.lab_WrStatus = new System.Windows.Forms.Label();
            this.Log = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.Bt_Login = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.Lab_Config_Ver = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // TxtLink_linkLabel1
            // 
            this.TxtLink_linkLabel1.AutoSize = true;
            this.TxtLink_linkLabel1.Location = new System.Drawing.Point(817, 50);
            this.TxtLink_linkLabel1.Name = "TxtLink_linkLabel1";
            this.TxtLink_linkLabel1.Size = new System.Drawing.Size(117, 20);
            this.TxtLink_linkLabel1.TabIndex = 0;
            this.TxtLink_linkLabel1.TabStop = true;
            this.TxtLink_linkLabel1.Text = "Tool Help Page";
            this.TxtLink_linkLabel1.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.linkLabel1_LinkClicked);
            // 
            // debugInstructionsLabel
            // 
            this.debugInstructionsLabel.AutoSize = true;
            this.debugInstructionsLabel.ForeColor = System.Drawing.Color.Blue;
            this.debugInstructionsLabel.Location = new System.Drawing.Point(28, 56);
            this.debugInstructionsLabel.Name = "debugInstructionsLabel";
            this.debugInstructionsLabel.Size = new System.Drawing.Size(127, 20);
            this.debugInstructionsLabel.TabIndex = 1;
            this.debugInstructionsLabel.Text = "Tool Version: 1.0";
            // 
            // Heading
            // 
            this.Heading.AutoSize = true;
            this.Heading.Font = new System.Drawing.Font("Modern No. 20", 16F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Heading.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(192)))), ((int)(((byte)(0)))));
            this.Heading.Location = new System.Drawing.Point(26, 9);
            this.Heading.Name = "Heading";
            this.Heading.Size = new System.Drawing.Size(297, 34);
            this.Heading.TabIndex = 3;
            this.Heading.Text = "Saura Tool Heading";
            // 
            // Bt_Exit
            // 
            this.Bt_Exit.Font = new System.Drawing.Font("Modern No. 20", 14F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Bt_Exit.ForeColor = System.Drawing.Color.Red;
            this.Bt_Exit.Location = new System.Drawing.Point(983, 440);
            this.Bt_Exit.Name = "Bt_Exit";
            this.Bt_Exit.Size = new System.Drawing.Size(244, 43);
            this.Bt_Exit.TabIndex = 6;
            this.Bt_Exit.Text = "Exit";
            this.Bt_Exit.UseVisualStyleBackColor = true;
            this.Bt_Exit.Click += new System.EventHandler(this.Bt_Exit_Click);
            // 
            // label_st
            // 
            this.label_st.AutoSize = true;
            this.label_st.Font = new System.Drawing.Font("Modern No. 20", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label_st.ForeColor = System.Drawing.Color.Black;
            this.label_st.Location = new System.Drawing.Point(34, 446);
            this.label_st.Name = "label_st";
            this.label_st.Size = new System.Drawing.Size(71, 22);
            this.label_st.TabIndex = 9;
            this.label_st.Text = "Status:";
            // 
            // lab_WrStatus
            // 
            this.lab_WrStatus.AutoSize = true;
            this.lab_WrStatus.Location = new System.Drawing.Point(118, 450);
            this.lab_WrStatus.MaximumSize = new System.Drawing.Size(800, 40);
            this.lab_WrStatus.Name = "lab_WrStatus";
            this.lab_WrStatus.Size = new System.Drawing.Size(0, 20);
            this.lab_WrStatus.TabIndex = 10;
            // 
            // Log
            // 
            this.Log.AllowDrop = true;
            this.Log.AutoSize = true;
            this.Log.Location = new System.Drawing.Point(118, 381);
            this.Log.MaximumSize = new System.Drawing.Size(800, 60);
            this.Log.Name = "Log";
            this.Log.Size = new System.Drawing.Size(0, 20);
            this.Log.TabIndex = 12;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Modern No. 20", 10F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.ForeColor = System.Drawing.Color.Black;
            this.label2.Location = new System.Drawing.Point(34, 376);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(51, 22);
            this.label2.TabIndex = 11;
            this.label2.Text = "Log:";
            // 
            // Bt_Login
            // 
            this.Bt_Login.Font = new System.Drawing.Font("Modern No. 20", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Bt_Login.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(192)))));
            this.Bt_Login.Location = new System.Drawing.Point(983, 382);
            this.Bt_Login.Name = "Bt_Login";
            this.Bt_Login.Size = new System.Drawing.Size(244, 43);
            this.Bt_Login.TabIndex = 13;
            this.Bt_Login.Text = "Login";
            this.Bt_Login.UseVisualStyleBackColor = true;
            this.Bt_Login.Click += new System.EventHandler(this.Bt_Login_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.ForeColor = System.Drawing.Color.Blue;
            this.label1.Location = new System.Drawing.Point(183, 56);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(88, 20);
            this.label1.TabIndex = 14;
            this.label1.Text = "Ini Version:";
            // 
            // Lab_Config_Ver
            // 
            this.Lab_Config_Ver.AutoSize = true;
            this.Lab_Config_Ver.ForeColor = System.Drawing.Color.Blue;
            this.Lab_Config_Ver.Location = new System.Drawing.Point(272, 57);
            this.Lab_Config_Ver.Name = "Lab_Config_Ver";
            this.Lab_Config_Ver.Size = new System.Drawing.Size(0, 20);
            this.Lab_Config_Ver.TabIndex = 15;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.ForeColor = System.Drawing.Color.Blue;
            this.label4.Location = new System.Drawing.Point(817, 15);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(397, 20);
            this.label4.TabIndex = 17;
            this.label4.Text = "Developer:Sauraurja Tech [ sauraurjatech@gmail.com ]";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1239, 509);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.Lab_Config_Ver);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.Bt_Login);
            this.Controls.Add(this.Log);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.lab_WrStatus);
            this.Controls.Add(this.label_st);
            this.Controls.Add(this.Bt_Exit);
            this.Controls.Add(this.Heading);
            this.Controls.Add(this.debugInstructionsLabel);
            this.Controls.Add(this.TxtLink_linkLabel1);
            this.ForeColor = System.Drawing.SystemColors.WindowText;
            this.Name = "Form1";
            this.Text = "Saura Tool Heading";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.LinkLabel TxtLink_linkLabel1;
        private System.Windows.Forms.Label debugInstructionsLabel;
        private System.Windows.Forms.Label Heading;
        private System.Windows.Forms.Button Bt_Exit;
        private System.Windows.Forms.Label label_st;
        private System.Windows.Forms.Label lab_WrStatus;
        private System.Windows.Forms.Label Log;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button Bt_Login;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label Lab_Config_Ver;
        private System.Windows.Forms.Label label4;
    }
}

