import sys
import binascii
import textwrap
from colorama import init
from colorama import Fore, Back, Style
import os



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
def dispClear():
    os.system('cls')

def printGreen(text):
    testInfo = text.replace('\n', ' ').replace('\r', '').replace('\t', '')
    testInfo = '\n'.join(textwrap.wrap(testInfo, 100))
    print (Fore.GREEN + testInfo+ '\n')

def printRed(text):
    testInfo = text.replace('\n', ' ').replace('\r', '').replace('\t', '')
    testInfo = '\n'.join(textwrap.wrap(testInfo, 100))
    print (Fore.RED + testInfo+ '\n')
#Print Error in red
##########
def printE(text): #print error
    testInfo = text.replace('\n', ' ').replace('\r', '').replace('\t', '')
    testInfo = '\n'.join(textwrap.wrap(testInfo, 100))
    print (Back.RED + testInfo)

##########
#Print Sucess in green
##########
def printS(text): #print Sucess
    print (Back.GREEN + text)

##########
#Print Info in Yellow
##########
def printI(text): #print info
    testInfo = text.replace('\n', ' ').replace('\r', '').replace('\t', '')
    testInfo = '\n'.join(textwrap.wrap(testInfo, 100))
    print (Fore.YELLOW + testInfo+'\n')

##########
#Print Info in Heading
##########
def printH(text): #Print Heading
	print (Fore.GREEN+ text.center(80, '#'))

def printTagValAligned(tag,text,tagMaxLen):
    tagSpacelen = len(tag)
    if(tagSpacelen > tagMaxLen):
        tagSpacelen = 0
    else:
        tagSpacelen = tagMaxLen - tagSpacelen
    text = ('\n  '+(" "*tagMaxLen)).join(textwrap.wrap(text, 64))
    print(tag[:tagMaxLen] +" "*tagSpacelen+": " +text)
#########################
#  below function takes string or byte array as argument and format it and display data as ASCCI and bytes
##########################
def printD(tag,Data,disAllFormat=0): #Print data,keys, for tag only 8 charectes will be taken disAllFormat=0 both, 1 = assi only and 2 = hex only 
    tagSpacelen = len(tag)
    if(tagSpacelen > 8):
        tagSpacelen = 0
    else:
        tagSpacelen = 8 - tagSpacelen
    if( (type(Data) == str) or ((type(Data) == bytearray) or (type(Data) == bytes)) ): 
        datLen = len(Data)
    if((type(Data) == str) and datLen):
        # we have string
        strLen = str(datLen +1)
        # we have byte array of string
        bytArray = bytearray(Data,'utf-8')
        bytArray.append(0) # append null charecter       
        if(disAllFormat != 2):
            text1 = '\n\t\t     '.join(textwrap.wrap(str(Data), 40))
            print(tag[:8] +" "*tagSpacelen + "(ASCII):["+ strLen +"] "+text1)
        if(disAllFormat != 1):
            rawByt = ' 0x'.join('{:02x}'.format(x) for x in bytArray)
            rawByt = '\n\t\t     '.join(textwrap.wrap(rawByt, 40))
            print(tag[:8] +" "*tagSpacelen + "( Hex ):["+ strLen +"] 0x"+rawByt+"\n")
    elif(((type(Data) == bytearray) or (type(Data) == bytes)) and datLen):
        # we have bytes
        datLen = str(datLen)
        try:
            if(disAllFormat != 2):
                text1 = '\n\t\t     '.join(textwrap.wrap((Data.decode('utf-8')), 40))
                print(tag[:8]+" "*tagSpacelen + "(ASCII):["+ datLen +"] "+text1)
        except:
            if(disAllFormat != 2):
                print("")# array canot be decoded into ascii
        if(disAllFormat != 1):
            rawByt = ' 0x'.join('{:02x}'.format(x) for x in Data)
            rawByt = '\n\t\t     '.join(textwrap.wrap(rawByt, 40))
            print(tag[:8]+" "*tagSpacelen + "( Hex ):["+ datLen +"] 0x"+rawByt+"\n")
init(autoreset=True) # use init()  fro color to retain every print, use print(Style.RESET_ALL) to reset
libtest = 0
if(libtest):
    printH("pythonLib")
    
    bytes = b'1234'
    printI("this is byte to hex string convertion test input b'1234' : output :")
    print(bytesToHex(bytes))
    printI("this is hex string to bytes convertion test input ""10aB")
    printD("OUTPUT",hexStrToBytes("10aB"),2)
    printI("this is integer to hex string test input  100 ")
    printD("OUTPUT",intToHexString(100),0)
    printI("This is String Disply test")
    printD("TAG","1234")
    printI("This is bytearray Disply test")
    printD("TAG",str2ByteArray("1234"))
    printE("This is Error in  pythonLib")
    printS("Sucess!!")