import serial
from .libDisp import *
testModule  = 0
ser = 0
def setComPort(com,baud,timeoutval):
	status = False
	try:
		global ser
		ser = serial.Serial(com, baud, timeout=timeoutval)
		ser.close()
		printI("\n\n\nCom Port:"+com+ " Baudrate:"+str(baud))
		status  = True;
	except:
	  printI("\n\n\nError opening port "+com)
	return status
def serSend(bArray):
	ser.open()
	ser.reset_input_buffer()
	ser.reset_output_buffer()
	ser.write(bArray)
	# wait for tx to finish?
	ser.close()
def serRead(lenToRead):
	ser.open()
	tmp_info = ser.read(lenToRead)
	ser.reset_input_buffer()
	ser.reset_output_buffer()
	ser.close()
	return tmp_info
def SendAndRead(bArray,readLen):
	tmp_info = 0;
	if(len(bArray)):
		ser.open()
		ser.reset_input_buffer()
		ser.reset_output_buffer()
		ser.write(bArray)
		tmp_info = ser.read(readLen)
		ser.reset_input_buffer()
		ser.reset_output_buffer()
		ser.close()
	return(tmp_info)
if(testModule):
	if(setComPort('COM24',57600,0.1)):
		printS("Port open Success")
	else:
		printE("Port open Failed")
	bArray = bytes([1,2,3,4])
	printI("Sending data")
	serSend(bArray)
	printD("Reading data",serRead(4),2) # read 4 bytes
	SendAndRead(bArray,4)