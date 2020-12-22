
import sys
import os
import subprocess
import time
import random
import string
from subprocess import Popen
import argparse
import configparser
def writeLog(Log):
    with open('pythLog.txt', 'a') as fh:
        fh.write(Log + '\n')
        fh.close()
    
def writeOut(Key,Value):
    with open('pythOut.txt', 'a') as fh:
        fh.write(Key + " " + Value)
        fh.close()
# Create the parser
#With the prog keyword, you specify the name of the program that will be used in the help
#By default, the library uses the value of the sys.argv[0] element to set the name of the program, 
#which as you probably already know is the name of the Python script you have executed. However,
#you can specify the name of your program just by using the prog
my_parser = argparse.ArgumentParser(prog='tool',
									usage='%(prog)s command [option]',
									prefix_chars='-',
                                    description='CLI tool for Factory programming Connected Devices Version 1.0')

# Add the arguments
my_parser.add_argument("cmd", nargs='?', default="EMPTY",help=': fact_build, provision, post_img,all..\n e.g. arg.py factBuild -un useradmin@gmail.com -pw adminpassword -vc "Version Info"')
my_parser.add_argument("-pathProv", nargs='?', default="EMPTY",help='path of application image (device alredy provisiond) ')
my_parser.add_argument("-N", nargs='?', default="1",help='Number of est Cycles')
#my_parser.add_argument("-bootPath", nargs='?', default="EMPTY",help='path of boot image image.current directory if not provided')
#my_parser.add_argument("-devType", nargs='?', default="EMPTY",help='set Device type')
#my_parser.add_argument("-un", nargs='?',help='user name e.g. arg.py login -un useradmin@gmail.com -pw adminpassword')
#my_parser.add_argument("-pw", nargs='?',help='password')
#my_parser.add_argument("-vc", nargs='?',help='version comment')

listToStr = ' '.join(map(str, sys.argv))
writeLog(listToStr)

args = my_parser.parse_args()

writeLog("settings.ini")
config = configparser.ConfigParser()
config.sections()

# read values from a section
#string_val = config.get('section_a', 'string_val')
#bool_val = config.getboolean('section_a', 'bool_val')
#int_val = config.getint('section_a', 'int_val')
#float_val = config.getfloat('section_a', 'pi_val')
config.read('cred.ini')
username = config.get('Cred', 'username')
password = config.get('Cred', 'password')
config.read('settings.ini')
otaImageComment = config.get('Product', 'otaImageComment')
appPath = config.get('Product', 'appPath')
bootPath = config.get('Product', 'bootPath')
deviceModel = config.get('Product', 'deviceModel')
if(len(deviceModel)!=2):
	sys.exit(1)
pushOTAImageToServer = config.getint('Product', 'pushOTAImageToServer')
comport = config.get('Other', 'comport')
baudRate = config.getint('Other', 'baudRate')
timeout = config.getfloat('Other', 'timeout')
picProgVoltage = config.getfloat('Other', 'picProgVoltage')
picPartNo = config.get('Other', 'picPartNo')
cmdStatus = 1
writeLog("Executing Command "+  args.cmd)
if args.cmd == 'EMPTY':
    print('NO COMMAND')
elif args.cmd == 'factBuild': # build finial (combine APP and BL )image to be flashed
	print("executing factBuild")
	cmdStatus = 0		
elif args.cmd == 'provision':      #flashes image to device and flashes SN
	print("executing provision")
	cmdStatus = 0
elif args.cmd == 'provisionLocal':
	print("executing provisionLocal")
	if(args.pathProv != "EMPTY"):
		print("Arg received"+args.pathProv)
		cmdStatus = 0
	else:
		print("No parameters paased")
		cmdStatus = 2
elif args.cmd == 'picFlashSaveKey': #only program program memory other data preserved
	if(args.pathProv):
		cmdStatus = 0
elif ((args.cmd == 'commission') or (args.cmd == 'runTest')):      # capture and commition the device
	cmdStatus = 0
elif args.cmd == 'all':
	print('This tkes one munit...\ngenerating nessesory files...')
	cmdStatus = 0
	#1) genrate factory image if not present, OTA and Factory image

	#2) Provision and flash the device

	#3) disconnect Programmer and connect power to USB COM port

	#4) ping device and validate we are in application (provision sucess!!!)

	#6) Commission the device (using fact key)...store both master and user keys

	#7) test Action command (with user key)

	#8) test config command (with master key)

	#9) send OTA command and send OTA image (OTA command -> Image -> app valid)

	#10) verify that we are in application after OTA

	#11) 7) test Action command (with user key) and 8) test config command (with master key)

	#12) Try sending Invalid Command or try sending Replay command...No Responce

	#12) Break OTA and try to recover device

	#13) Break OTA and FDR and try to recover device..

	#14) Test success!!!
	
else:
    printE(args.cmd + " is invalid command")

sys.exit(cmdStatus)
