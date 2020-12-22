using MyCrypto;
using MyProg;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using Timer = System.Windows.Forms.Timer;

// This is the code for your desktop app.
// Press Ctrl+F5 (or go to Debug > Start Without Debugging) to run your app.

namespace DesktopApp1
{
    public partial class Form1 : Form
    {
        // function to change form size if needed in future , if button grows
        public void ChangeSize(int width, int height)
        {
            this.Size = new Size(width, height);
        }
        static class constants
        {
            // button position
            public const int BUT_COLUM_MAX = 4;

            public const int X_DEFAULT = 20;
            public const int Y_DEFAULT = 80;
            public const int X_INCRIMENT = 180;
            public const int Y_INCREMENT = 40;
        
        }

        //Class for .ini button properties
        class scriptButtonProp
        {
            public String ButtonName;
            public String ButtonInfo ;
            public String ButtonFunctionName;
            public String ButtonType;
            public String ButtonErrorHint ;
            public String ButtonColor;
        }

        //Function For Custom Input Prompt
        public static DialogResult InputBox(string title, string promptText, ref string value)
        {
            Form form = new Form();
            Label label = new Label();
            TextBox textBox = new TextBox();
            Button buttonOk = new Button();
            Button buttonCancel = new Button();

            form.Text = title;
            label.Text = promptText;
            textBox.Text = value;

            buttonOk.Text = "OK";
            buttonCancel.Text = "Cancel";
            buttonOk.DialogResult = DialogResult.OK;
            buttonCancel.DialogResult = DialogResult.Cancel;

            label.SetBounds(9, 20, 372, 13);
            textBox.SetBounds(12, 36, 372, 20);
            buttonOk.SetBounds(228, 72, 75, 23);
            buttonCancel.SetBounds(309, 72, 75, 23);

            label.AutoSize = true;
            textBox.Anchor = textBox.Anchor | AnchorStyles.Right;
            buttonOk.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;
            buttonCancel.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;

            form.ClientSize = new Size(396, 107);
            form.Controls.AddRange(new Control[] { label, textBox, buttonOk, buttonCancel });
            form.ClientSize = new Size(Math.Max(300, label.Right + 10), form.ClientSize.Height);
            form.FormBorderStyle = FormBorderStyle.FixedDialog;
            form.StartPosition = FormStartPosition.CenterScreen;
            form.MinimizeBox = false;
            form.MaximizeBox = false;
            form.AcceptButton = buttonOk;
            form.CancelButton = buttonCancel;

            DialogResult dialogResult = form.ShowDialog();
            value = textBox.Text;
            return dialogResult;
        }
        string controllerFile;
        string helpLink;
        string pythonPath;
        //cli cmmd
        string  Cli_Cmd;

        Timer tmr;
        OpenFileDialog openFileDialog1;
        IniFile MyCredIni;
        IniFile MyIni;
        ProcessStartInfo startInfo;
        int xAxix = constants.X_DEFAULT, YAxix = constants.Y_DEFAULT;
        System.Windows.Forms.ToolTip ToolTip1;
        // creates UI Form
        public Form1()
        {
            InitializeComponent();
            // Handle the ApplicationExit event to know when the application is exiting.
            Application.ApplicationExit += new EventHandler(this.OnApplicationExit);

            ToolTip1 = new System.Windows.Forms.ToolTip();
            //read credentials
            // Cryptography.EncryptFile("ABCDEFGH", "cred.ini", "credout.ini");
            // Cryptography.DecryptFile("ABCDEFGH", "credout.ini", "cred.ini");
            MyCredIni = new IniFile("cred.ini");
            MyCredIni.Write("username", "Enter User Name", "Cred"); //erase cred if any
            MyCredIni.Write("password", "Enter Password", "Cred"); // erase cred 
            //Read Ini file and update variables
            MyIni = new IniFile("settings.ini");
           
            if(MyIni.Read("credStore", "Product") == "true")
            {
                //cred
                if (!((MyCredIni.KeyExists("username", "Cred")) && (MyCredIni.KeyExists("password", "Cred"))))
                {
                    MessageBox.Show("cred.ini file not correct / Login Error");
                }
                lab_WrStatus.Text = "Set Login Credentials";
            }
            else
            {
                Bt_Login.Visible = false;
            }
            
            //Heading
           
            String toolName = MyIni.Read("toolName", "Product");
            this.Text = toolName;
            Heading.Text = toolName;
            //script
            controllerFile = MyIni.Read("controllerFile", "Product");
            //help page
            helpLink = MyIni.Read("helpLink", "Product");
            // buttons
            int But_Idx = 0;
            String tempSection = "Button" + (But_Idx.ToString());
            scriptButtonProp tempScrButton = new scriptButtonProp();

            // create GUI dynamically using ini file
            while (MyIni.KeyExists("ButtonName", tempSection))
            {

                tempScrButton.ButtonName = MyIni.Read("ButtonName", tempSection);
                tempScrButton.ButtonInfo = MyIni.Read("ButtonInfo", tempSection);
                tempScrButton.ButtonFunctionName = MyIni.Read("ButtonFunctionName", tempSection);
                tempScrButton.ButtonType = MyIni.Read("ButtonType", tempSection);
                tempScrButton.ButtonErrorHint = MyIni.Read("ButtonErrorHint", tempSection);
                tempScrButton.ButtonColor = MyIni.Read("ButtonColor", tempSection);
                // create button
                CreateDynamicButton(tempScrButton, tempSection);
                But_Idx++;
                tempSection = "Button" + (But_Idx.ToString());
            }
           
            pythonPath = MyIni.Read("pythonPath", "Other");
            //writin ini file
            // MyIni.Write("DefaultVolume", "100", "Audio");

            startInfo = new ProcessStartInfo(pythonPath);
            startInfo.CreateNoWindow = false;
            startInfo.UseShellExecute = false;
            startInfo.WindowStyle = ProcessWindowStyle.Minimized;

            tmr = new Timer();

            tmr.Interval = 2000;
            tmr.Enabled = true;
            tmr.Tick += new System.EventHandler(OnTimerEvent);

            openFileDialog1 = new OpenFileDialog();
            openFileDialog1.InitialDirectory = Directory.GetCurrentDirectory();
            openFileDialog1.RestoreDirectory = true;
            openFileDialog1.Title = "Select Device .hex File";
            openFileDialog1.DefaultExt = "hex";
            openFileDialog1.CheckFileExists = true;
            openFileDialog1.CheckPathExists = true;
            openFileDialog1.ReadOnlyChecked = true;
            openFileDialog1.ShowReadOnly = true;
        }

        //// function heldle opening Web Link
        private void linkLabel1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            // Click on the link below to continue learning how to build a desktop app using WinForms!
            System.Diagnostics.Process.Start(helpLink);

        }
        //// function to Exit tool
        private void Bt_Exit_Click(object sender, EventArgs e)
        {
            this.Close();
        }
        private void OnApplicationExit(object sender, EventArgs e)
        {
            MyCredIni.Write("username", "Enter User Name", "Cred");
            MyCredIni.Write("password", "Enter Password", "Cred");
        }
        // login function
        private void Bt_Login_Click(object sender, EventArgs e)
        {
            String tempData="";
            InputBox("Enter User Name", "", ref tempData);
            MyCredIni.Write("username", tempData, "Cred");
            InputBox("Enter Password", "", ref tempData);
            MyCredIni.Write("password", tempData, "Cred");
            lab_WrStatus.Text = "";
        }

        // function to open any text file
        private void OpenTxtFile(string file)
        {
            ProcessStartInfo startInfo1 = new ProcessStartInfo("notepad.exe");
            startInfo1.CreateNoWindow = false;
            startInfo1.UseShellExecute = false;
            startInfo1.WindowStyle = ProcessWindowStyle.Minimized;
            startInfo1.Arguments = file;
            Process.Start(startInfo1);
            //TODO: Delee object
        }

        // function run Python script in CLI
        private bool runPythonCli(string Arguments)
        {
            bool cmdStatus = false;
            startInfo.Arguments = Arguments;
            try
            {
                // Start the process with the info we specified.
                // Call WaitForExit and then the using statement will close.
                using (Process exeProcess = Process.Start(startInfo))
                {
                    exeProcess.WaitForExit();
                    if(exeProcess.ExitCode!=0)
                    {
                        MessageBox.Show("Python Return Error Code: " + exeProcess.ExitCode.ToString() +"\nEdit settings.ini and restart application");
                    }
                    else
                    {
                        cmdStatus=true;
                    }
                    
                }
            }
            catch
            {
                // Log error.
                MessageBox.Show("Error executing python command");
            }
            return cmdStatus;
        }

        private void OnTimerEvent(Object source, EventArgs e)
        {
            tmr.Stop();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        /// This method creates a Button control at runtime

        private void CreateDynamicButton(scriptButtonProp buttonStr,String buttonSection)
        {   
            // Create a Button object 

            Button dynamicButton = new Button();
            // Set Button properties

            // dynamicButton.Height = 40; // auto
           dynamicButton.Width = constants.X_INCRIMENT - 30; // 30 is gap between colums
           String tmpButtonColor = buttonStr.ButtonColor.ToLower();
            if (tmpButtonColor == "red")
            {
                dynamicButton.BackColor = Color.Red;
            }
            else if (tmpButtonColor == "green")
            {
                dynamicButton.BackColor = Color.LightGreen;
            }
            else if (tmpButtonColor == "blue")
            {
                dynamicButton.BackColor = Color.Blue;
            }
            else if (tmpButtonColor == "yellow")
            {
                dynamicButton.BackColor = Color.LightYellow;
            }
            else if (tmpButtonColor == "pink")
            {
                dynamicButton.BackColor = Color.LightPink;
            }
            else
            {
                //default
            }
                dynamicButton.Location = new Point(xAxix, YAxix);
            // set button hint
            ToolTip1.SetToolTip(dynamicButton, buttonStr.ButtonInfo); 

            dynamicButton.Text = buttonStr.ButtonName;
            dynamicButton.Name = buttonSection;
            //dynamicButton.Font = new Font("Georgia", 16);
            if(YAxix >= (constants.Y_DEFAULT + constants.Y_INCREMENT * (constants.BUT_COLUM_MAX-1)))
            {
                xAxix += constants.X_INCRIMENT;
                YAxix = constants.Y_DEFAULT;
            }
            else
            {
                YAxix += constants.Y_INCREMENT;
            }
            // Add a Button Click Event handler

            dynamicButton.Click += new EventHandler(DynamicButton_Click);
            // Add Button to the Form. Placement of the Button

            // will be based on the Location and Size of button

            Controls.Add(dynamicButton);

        }
        //Function handles button click
        private void DynamicButton_Click(object sender, EventArgs e)
        {
            string scriptPerameter="";
            var button = (Button)sender;
            String errHint = "";
            String ArgOpt = "";
            String cliFuncName = "";
            errHint = MyIni.Read("ButtonErrorHint", button.Name);
            cliFuncName = MyIni.Read("ButtonCliName", button.Name);
            if (MyIni.KeyExists("ButtonType", button.Name))
            {
                ArgOpt = MyIni.Read("ButtonType", button.Name);
                String ArgHelp = MyIni.Read("ButtonArgHelp", button.Name);
                
                if (ArgOpt == "FilePath" || ArgOpt == "FolderPath")
                {
                    if(ArgOpt == "FilePath")
                    {
                       
                        openFileDialog1.Title = "Select File Path " + ArgHelp;
                    }
                    else
                    {
                        openFileDialog1.Title = "Select folder Path "+ ArgHelp;
                    }
                    
                    if (openFileDialog1.ShowDialog() == DialogResult.OK)
                    {
                        scriptPerameter = openFileDialog1.FileName;
                    }
                }
                if (ArgOpt == "String")
                {
                    InputBox(ArgHelp, "", ref scriptPerameter);
                }
                if (ArgOpt == "Bool")
                {
                    DialogResult res = MessageBox.Show("Select Input", ArgHelp, MessageBoxButtons.YesNo, MessageBoxIcon.Information);
                    if (res == DialogResult.Yes)
                    {
                        scriptPerameter = "1";
                    }
                    if (res == DialogResult.No)
                    {
                        scriptPerameter = "0";
                    }
                }
            }
            Cli_Cmd = controllerFile + " " + cliFuncName + scriptPerameter;

            Log.Text = "Executing CLI:  " + Cli_Cmd;
            if (!runPythonCli(Cli_Cmd))
            {
                lab_WrStatus.ForeColor = Color.Red;
                lab_WrStatus.Text = "Fail. " + errHint;
            }
            else
            {
                lab_WrStatus.ForeColor = Color.Green;
                lab_WrStatus.Text = "Pass ";
            }
        }
    }
}
