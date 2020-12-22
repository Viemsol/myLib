def base36encode(number, filLen=5,alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
	"""Converts an integer to a base36 string."""
	if not isinstance(number, (int, int)):
		raise TypeError('number must be an integer')

	base36 = ''
	sign = ''

	if number < 0:
		sign = '-'
		number = -number
	out =""
	if 0 <= number < len(alphabet):
		out =  sign + alphabet[number]
	else:
		while number != 0:
			number, i = divmod(number, len(alphabet))
			base36 = alphabet[i] + base36
		out = sign + base36
	
	while(len(out)<filLen):
		out = "0"+out

	print(out)
	return out

def base36decode(number):
    return int(number, 36)
#convert list to string ie [a,b,c,d] = "abcd"
def list2Str(listData,saperator=''): # if no sperator use ''
	print(listData)
	listToStr = saperator.join(map(str, listData))
	print(listToStr)
	return listToStr
def list2Bytes(listDat):
	return(bytes(listDat))
def list2Array(listDat):
	return(array(listDat))
#convert list 3 string ie [a,b,c,d] = "abcd"
def byte2Str(byteData):
	strData = byteData.decode("utf-8")
	return strData



###################
# function return  bytes from hex string it only process 0-9 ,a-f , A-F else thows exception
# eg "10AB" =   0x10 0xAB ,---- "1" invalid input , "01" this is valid input shuld be multiple of 2
###################
def hexStrToBytes(hexStr):
    data = bytearray.fromhex(hexStr) # get bytes from hex string
    return data
###################
# function return  string haxdecimal representation of integr input 
###################
def intToHexString(intData):
    return(hex(intData))

##########
#function take string as input ang return byte array also null chrecter is included in array
##########
def str2ByteArray(strData):
    data = bytearray(strData,'utf-8')
    data.append(0) # append null charecter
    return data

##########
#function take string as input and return byte array, null chrecter is NOT included in array
##########
def strlen2ByteArray(strData):
    data = bytearray(strData,'utf-8')
    return data

###########
#convert raw bytes to hex representation  ,b'0123' => 30313233
##########
def bytesToHex(bytesObj):
    hexData = bytesObj.hex()
    return(hexData)
##############

###########
#convert raw bytes to hex representation  ,b'0123' => 30313233
##########
def bytes2List(bytesObj):
    return(list(bytesObj))
##############

##########
#take raw bytes as input, conver them to string representing each byte in hex format
##########
def bytesToHexFormat(byteArray):
    strHexOut = '0x'+' 0x'.join('{:02x}'.format(x) for x in byteArray)
    return strHexOut
##########

###########
#convert raw bytes to hex representation  ,b'0123' => 0x30 0x31 0x32 0x33
##########
def bytesToHexSufix(bytesObj,suffix):
    strHexOut = suffix+' '+suffix.join('{:02x}'.format(x) for x in byteArray)
##############
#Function conver byte object to string b'abcd' => abcd
###########
def bytesToAscii(bytesObj):
    return(bytesObj.decode("utf-8"))
##########
#convert large intger to byte array or bytes ie 
# 1234566666666666666666666666687765443 to raw bytes 0x23, 0x45 ......
#len is byte array length (32 meanse output byte array is 32 byte long)
##########
def intToBytes(intData,len):
    byteArrayout = intData.to_bytes(len, byteorder='big')
    return(byteArrayout)
##########
#funtion clears the CLI display
##########

##########
#funtion adds sigle byte after evry byte
#eg ntToBytes(b"abc",0) = b'a\x00b\x00c\x00'
##########
def insertByteAfterOne(byteArr,byteIncer):
	new = bytes(0)
	for value in byteArr:
		new += bytes([value]) + bytes([byteIncer&0xFF])
	return(new)