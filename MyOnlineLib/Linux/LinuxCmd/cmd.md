# linux command

## to remove files 

### remove all files
rm *

### remove all files in current directory with extention .pdf
rm *.pdf

### remove some selected files from current directory
rm file_name1 file_name2

## to remove Directory

### remove folder in current path
To delete a directory containing files, use rm -r.
rm -r dirname


### Remove mutiple folders
rm -r dirname1 dirname2 dirname3


## Lis files and directory

### list files and directory
ls

### list all hidden files and directory
ls -a

## display current path from Rooth
“pwd” command. It gives us the absolute path, which means the path that starts from the root

pwd

## moving accrees directory 

### If you just type “cd” and press enter, it takes you to the home directory.

cd

### go to folder , folder name is case sensitive
cd foldername

### if folder name have sapces then i.e Raspberry Pi then use **\** in place of sapce
cd Raspberry\ Pi

## create folder
Use the mkdir command when you need to create a folder
mkdir floderName

## carete a file
touch — The touch command is used to create a file.
touch test.txt

## halp command **man ** Diaplay user manual of command , & **--help** display way to use command

man dir

cd --help

## copying files 

### **cp** 
cp nand.txt /home/pi/project

## Moving and renaming file
Use the **mv** command to move files through the command line. We can also use the mv command to rename a file.

### renaming file
 
mv test1.txt test2.txt

### moving
mv test1.txt /home/pi/project/test2.txt

## view files
**cat** — Use the cat command to display the contents of a file. It is usually used to easily view programs.
cat test.txt

## **sudo** make changes as Admin 
**sudo** — A widely used command in the Linux command line, sudo stands for "SuperUser Do". So, if you want any command to be done with administrative or root privileges, you can use the sudo command.
sudo touch test.txt

## Check DIsk Space
df — Use the df command to see the available disk space in each of the partitions in your system. You can just type in df in the command line and you can see each mounted partition and their used/available space in % and in KBs. If you want it shown in megabytes, you can use the command “df -m”.

df

df -m

## clear screen
clear

## system Info
Using the command **uname -a** prints most of the information about the system. This prints the kernel release date, version, processor type, etc.

uname -a

## make executable program kind of **.exe**
Imagine you have a python code named numbers.py in your computer. You'll need to run **python numbers.py** every time you need to run it. Instead of that, when you make it executable, you'll just need to run **numbers.py** in the terminal to run the file. To make a file executable, you can use the command **chmod +x numbers.py** in this case.

chmod +x numbers.py

**Note**: Now when you list files using **ls** this file name color will be displayed green indicating it can be executed directly eith name

## HotName
Typing in **hostname -I** gives you your IP address in your network.
Typing in **hostname** gives you Name.

hostname -I

hostname

## ping 

ping google.com  # ping globle IP DNS , press **ctrl + C** to close sending pkts 
ping 192.168.1.2 # ping local ip, press **ctrl + C** to close sending pkts 

# Stop any running command
press **Ctrl+C** can be used to stop any command in terminal safely.

# Exit terminal
You can exit from the terminal by using the exit command.

exit

# power off computer
You can power off or reboot the computer by using the command sudo halt and sudo reboot.

sudo reboot

## Remote commad
**Note** below command works only on **cmd.exe** and not on **putty** or **bash** 

### If you are on the remote machine:
scp user@hostname:D:\text.txt user@hostname:/etc/var/test/test.txt

### If you are currently on Windows machine:
scp C:\Users\ndhavalikar\Desktop\iestscp\test.txt pi@192.168.1.10:/home/pi/Project

### Copy all files and folders recursively from local to remote using scp
scp C:\Users\ndhavalikar\Desktop\iestscp\*t pi@192.168.1.10:/home/pi/Project

### copy all file from windos folder to pi folder
scp C:\Users\ndhavalikar\Desktop\RespPiZero\server\* pi@192.168.1.10:/home/pi/Project/wifiBleServ








