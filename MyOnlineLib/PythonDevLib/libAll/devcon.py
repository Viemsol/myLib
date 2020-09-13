import subprocess
from libRun import *
devconIdUsbCom = "USB\VID_0403&PID_6001\FTHC1GUK"
devconIdPiKit3 = "USB\VID_04D8&PID_900A\DEFAULT_PK3_"
def devconListDev():
	# Fetches the list of all usb devices:
	result = subprocess.run(['devcon', 'hwids', '=usb'], capture_output=True, text=True)
	return(result)
def devconList():
	cliEx("devcon find usb*")
def devconEnable(deviceId):
	cmd = 'devcon enable "@'+ deviceId+'"'
	print(cmd)
	cliEx(cmd)
def devconDisable(deviceId):
	cmd = 'devcon disable "@'+ deviceId+'"'
	print(cmd)
	cliEx(cmd)
test = 0
if(test):
	devconList()
	devconDisable(devconIdUsbCom)
	devconEnable(devconIdUsbCom)
'''
# To display status
#print(devcon_win.HP_TrueVision_HD()) 
# Or
print(devcon_win.HP_TrueVision_HD('status')) 

# To change status
print(devcon_win.HP_TrueVision_HD('enable')) # will show options after 'devcon_win.'
'''