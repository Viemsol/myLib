def picFlashDevice(model,hexpath):
	#path = "C:\Program Files\Microchip\MPLABX\v4.05\mplab_ipe\pk3cmd.exe" #add this to env variable
	if(os.path.isfile(hexpath)):
		printD("Flashing "+hexpath)
		#cliEx("pk3cmd.exe -P16F18313 -V3.3 -B -C")
		cliEx("pk3cmd.exe -P16F18313 -F"+hexpath+" -V3.3 -M -Y -H")
	else:
		printD("Hex File Not Found")