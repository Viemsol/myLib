using MyProg;
using System;
using System.Data;
using System.Data.OleDb;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.IO.MemoryMappedFiles;
using System.Text;
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
        // function to create combo box
        public static DialogResult ComboBox(string title, String[] InputList, ref string SelectValue)
        {
            Form form = new Form();
            Label label = new Label();
            Button buttonOk = new Button();
            Button buttonCancel = new Button();
            ComboBox mybox = new ComboBox();

            form.Text = title;

            buttonOk.Text = "OK";
            buttonCancel.Text = "Cancel";
            buttonOk.DialogResult = DialogResult.OK;
            buttonCancel.DialogResult = DialogResult.Cancel;

           
            label.SetBounds(9, 20, 372, 13);
            mybox.SetBounds(12, 36, 372, 20);
            buttonOk.SetBounds(228, 72, 75, 23);
            buttonCancel.SetBounds(309, 72, 75, 23);

            label.AutoSize = true;
           
            mybox.Anchor = mybox.Anchor | AnchorStyles.Right;
            buttonOk.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;
            buttonCancel.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;

            mybox.Items.AddRange(InputList);
            mybox.Text = InputList[0];
            // Add this ComboBox to form

            form.ClientSize = new Size(396, 107);
            form.Controls.AddRange(new Control[] {mybox , buttonOk, buttonCancel });
            form.ClientSize = new Size(Math.Max(300, label.Right + 10), form.ClientSize.Height);
            form.FormBorderStyle = FormBorderStyle.FixedDialog;
            form.StartPosition = FormStartPosition.CenterScreen;
            form.MinimizeBox = false;
            form.MaximizeBox = false;
            form.AcceptButton = buttonOk;
            form.CancelButton = buttonCancel;

            DialogResult dialogResult = form.ShowDialog();
            SelectValue = mybox.Text.ToString();

            return dialogResult;
        }

        // funtion dispaly contet of txt / excel file
        public void displayFile(String FilePath, String Heading)
        {
            String fileExt = Path.GetExtension(FilePath); //get the file extension  
            if(fileExt.CompareTo(".xls") == 0 || fileExt.CompareTo(".txt") == 0)
            { 
            Form form = new Form();
            
            if (fileExt.CompareTo(".xls") == 0)
            {

                try
                {
                    DataGridView dataGridView1 = new DataGridView();

                    DataTable dtExcel = new DataTable();
                    dtExcel = ReadExcel(FilePath, fileExt); //read excel file  
                    dataGridView1.Visible = true;
                    dataGridView1.DataSource = dtExcel;
                    dataGridView1.ClientSize = new Size(dtExcel.Columns.Count * 100 + 10, dtExcel.Rows.Count * 25 + 10);


                    form.Controls.AddRange(new Control[] { dataGridView1 });
                    form.ClientSize = new Size(dtExcel.Columns.Count * 100 + 10, dtExcel.Rows.Count * 25 + 10);
                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.Message.ToString());
                }

            }
            else if (fileExt.CompareTo(".txt") == 0)
            {
                Label label = new Label();
                label.AutoSize = true;
                string content = File.ReadAllText(FilePath);

                if (content != null)
                {
                        label.Text = content;
                }
                else
                {
                        label.Text = "No Data";
                }
                form.Controls.AddRange(new Control[] { label });
                form.ClientSize = new Size(label.Width +10, label.Height +10);

                }
                form.Text = Heading;
            form.FormBorderStyle = FormBorderStyle.FixedDialog;
            form.StartPosition = FormStartPosition.CenterScreen;
            form.MinimizeBox = false;
            form.MaximizeBox = false;

            DialogResult dialogResult = form.ShowDialog();
        }
        else
        {
            MessageBox.Show("Please choose .txt or.xls file only.", "Warning", MessageBoxButtons.OK, MessageBoxIcon.Error); //custom messageBox to show error  
        }
     }
        //Function For Custom Input Prompt
        public static DialogResult InputBox(string title, string promptText, ref string value)
        {
            Form form = new Form();
            Label label = new Label();
            Button buttonOk = new Button();
            Button buttonCancel = new Button();
            TextBox textBox = new TextBox();
            

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

       
        string LogToFile;
        string paraToCli;
        string helpLink;
        string fileToCli;
        //cli cmmd
        string Cli_Cmd;

        Timer tmr;
        OpenFileDialog openFileDialog1;
        IniFile MyCredIni;
        IniFile MyIni;
        ProcessStartInfo startInfo;
        int xAxix = constants.X_DEFAULT, YAxix = constants.Y_DEFAULT;
        System.Windows.Forms.ToolTip ToolTip1;
        public void log2file(String message)
        {
            if (LogToFile.Contains("true"))
            {
                File.AppendAllText("log.txt", (message+"\r\n"));
            }
        }
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
            // config version
            String iniVersion = MyIni.Read("iniVersion", "Product");
            if(iniVersion == "")
            {
                iniVersion = "Not Found";
            }
            Lab_Config_Ver.Text = iniVersion;

            ////script
            LogToFile = MyIni.Read("LogToFile", "Product").ToLower();
            log2file("----------cl2ui log-----------");
            //script
            paraToCli = MyIni.Read("paraToCli", "Product");
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
           
            fileToCli = MyIni.Read("fileToCli", "Product");
            //writin ini file
            // MyIni.Write("DefaultVolume", "100", "Audio");

            startInfo = new ProcessStartInfo(fileToCli);
            
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
            openFileDialog1.Title = " ";
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

        

        // functions to display content of excel sheet
        public DataTable ReadExcel(string fileName, string fileExt)
        {
            string conn = string.Empty;
            DataTable dtexcel = new DataTable();
            if (fileExt.CompareTo(".xls") == 0)
                conn = @"provider=Microsoft.Jet.OLEDB.4.0;Data Source=" + fileName + ";Extended Properties='Excel 8.0;HRD=Yes;IMEX=1';"; //for below excel 2007  
            else
                conn = @"Provider=Microsoft.ACE.OLEDB.12.0;Data Source=" + fileName + ";Extended Properties='Excel 12.0;HDR=NO';"; //for above excel 2007  
            using (OleDbConnection con = new OleDbConnection(conn))
            {
                try
                {
                    OleDbDataAdapter oleAdpt = new OleDbDataAdapter("select * from [Sheet1$]", con); //here we read data from sheet1  
                    oleAdpt.Fill(dtexcel); //fill excel data into dataTable  
                }
                catch(Exception ex) {
                    MessageBox.Show(ex.Message.ToString());
                }
            }
            return dtexcel;
        }
        // function creates memeory mapped filr
        MemoryMappedFile CreatetMMF(string file,int bytes)
        {
            MemoryMappedFile MMFRef = MemoryMappedFile.CreateNew(file, bytes);
            return MMFRef;
        }
        //reade from mmf file
       uint ReadFromMMF(string file, UInt32 address)
        {
            MemoryMappedFile MMFRef = MemoryMappedFile.OpenExisting(file);
            MemoryMappedViewAccessor Accessor = MMFRef.CreateViewAccessor();
            uint val = Accessor.ReadUInt32(address);
            Accessor.Dispose();
            return (val);
        }
        //write value to mmf file
        private void WriteValueToMMF(MemoryMappedFile Ref,UInt32 address, int value)
        {
            MemoryMappedViewAccessor Accessor = Ref.CreateViewAccessor();
            Accessor.Write(address, value);
            Accessor.Dispose();
        }
        
        // function run Python script in CLI
        private bool runPythonCli(string Arguments)
        {
            bool cmdStatus = false;
         
            startInfo.Arguments = Arguments;
            Log.Text = "CLI:" + startInfo.FileName + " "+ Arguments;
            log2file("\r\nExecuting>File: "+ startInfo.FileName +"\r\nPerameter: "+ Arguments);
            try
            {
                // Start the process with the info we specified.
                // Call WaitForExit and then the using statement will close.
                using (Process exeProcess = Process.Start(startInfo))
                {
                    exeProcess.WaitForExit();
                    if(exeProcess.ExitCode!=0)
                    {
                        log2file("Error Exit Code : "+ exeProcess.ExitCode.ToString());
                       // MessageBox.Show("Executable Return Error Code: " + exeProcess.ExitCode.ToString() +"\r\nEdit settings.ini and restart application");
                    }
                    else
                    {
                        cmdStatus=true;
                    }
                    
                }
            }
            catch(Exception e)
            {
                // Log error.
                // MessageBox.Show("Error executing .exe or script command");
                log2file("Exception executing .exe or script command\r\n" + e.ToString());
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
            String ButtonArg = "";
            String ButtonCliName = "";
            String ButtonArgHelp = "";
            String ButtonArgOptPera = "";
            int argIdx = 0;
            bool operationCancel = false;
            bool ShowOutput = false;
            String ShowOutputFile = "";
            String ShowOutputFileHeading = "";

            errHint = MyIni.Read("ButtonErrorHint", button.Name);
            // scan through all arguments in button
            String fileToCliOveride = MyIni.Read("fileToCliOveride", button.Name);
            String paraToCliOveride = MyIni.Read("paraToCliOveride", button.Name);

            //script overide check .py /.bat ...etc
            if (paraToCliOveride.Contains("."))
            {
                Cli_Cmd = paraToCliOveride + " ";
            }
            else if(paraToCliOveride.Contains("none"))
            {
                Cli_Cmd = "";
            }
            else
            {
                Cli_Cmd = paraToCli + " ";
            }

                
            // overide check python.exe/bat.exe...
            if (fileToCliOveride.Contains("."))
            {
                startInfo.FileName = fileToCliOveride;
            }
            else
            {
                startInfo.FileName = fileToCli;
            }
            // scan through all arguments in button
            while (MyIni.KeyExists("ButtonArg" + argIdx.ToString(), button.Name))
            {
                ButtonCliName = MyIni.Read("ButtonCliName"+ argIdx.ToString(), button.Name);
                ButtonArg = MyIni.Read("ButtonArg" + argIdx.ToString(), button.Name).ToLower();
                ButtonArgHelp = MyIni.Read("ButtonArgHelp" + argIdx.ToString(), button.Name);
                ButtonArgOptPera = MyIni.Read("ButtonArgOptPera" + argIdx.ToString(), button.Name);
                
                if (ButtonArg == "filepath" || ButtonArg == "folderpath")
                {
                    if(ButtonArg == "filepath")
                    {
                        openFileDialog1.Title = " " + ButtonArgHelp;
                    }
                    else
                    {
                        openFileDialog1.Title = " "+ ButtonArgHelp;
                    }
 
                    if (openFileDialog1.ShowDialog() == DialogResult.OK)
                    {
                        scriptPerameter = openFileDialog1.FileName;
                    }
                    else
                    {
                        operationCancel = true;
                        break;
                    }

                    scriptPerameter += " ";
                }

                if (ButtonArg == "string")
                {
                    if(InputBox(ButtonArgHelp, "", ref scriptPerameter) == DialogResult.OK)
                    {
                        // do nothin
                    }
                    else
                    {
                        operationCancel = true;
                        break;
                    }
                    scriptPerameter += " ";
                }

                if (ButtonArg == "combo")
                {                    
                    string[] ArgOptPeraList = ButtonArgOptPera.Split(',');
                    if(ComboBox(ButtonArgHelp, ArgOptPeraList, ref scriptPerameter) == DialogResult.OK)
                    {
                        // do nothin
                    }
                    else
                    {
                        operationCancel = true;
                        break;
                    }
                    scriptPerameter += " ";
                }

                if (ButtonArg == "showoutput")
                {
                    ShowOutput = true;
                    ButtonCliName = "";
                    scriptPerameter = "";
                    ShowOutputFile = ButtonArgOptPera;
                    ShowOutputFileHeading = ButtonArgHelp;
                }
                argIdx++;

                Cli_Cmd += (ButtonCliName + scriptPerameter);
                scriptPerameter = "";
            }

            if (!operationCancel)
            {
                
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
                if(ShowOutput)
                {
                    //display content of dataOut.txt
                    displayFile(ShowOutputFile, ShowOutputFileHeading);
                }
               
            }
            else
            {
                Log.Text = "Operation canceled";
                log2file("Operation canceled");
            }
        }
    }
}
