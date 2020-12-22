from .libConvert import *
import sys
import binascii
import textwrap
from colorama import init
from colorama import Fore, Back, Style
import os
def printType(variable):
	print(variable, "is of type", type(variable))
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
	printI("Aligned Display Test")
	printTagValAligned("TAGNAME","TEXT NAME",10)