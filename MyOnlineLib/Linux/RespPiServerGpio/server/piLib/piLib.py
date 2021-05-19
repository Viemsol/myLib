#import btpycom
import smbus
import serial
import spidev
import RPi.GPIO as GPIO
import time
import socket               # Import socket module
import threading
import pigpio
 
i2c_ch = 1
pwm12 = 0
pwm13 = 0
serialObject0 = 0
gpioInit = 0
pi_pinst = 0

htmlMenu = '''
<html>
<head>  
<title>rpi Local Server</title> 
<style>
html {
  scroll-behavior: smooth;
}</style> 
</head>
<body>

<h1 style="font-size:50px; color:blue;">Welcome to rPi Local Server</h1>
<h1 style="font-size:25px; color:green;">1) API Format</h1>
<p>Request: [Command Data Data]<br />Positive Responce: [Command RespData]<br />Negative Responce: [error]</p>

<h1 style="font-size:25px; color:green;">2) API Menu</h1>

<p><mark class="yellow">1) Displat Menu</mark><br />https://192.168.1.10:5000/menu<br /><br />
<mark class="yellow">2)UART Initialization "uartInit BaudRate(int) TimeoutSec(int)"</mark><br />
https://192.168.1.10:5000/Command?piCmd=uartInit 9600 1<br /><br />
<mark class="yellow">3) UART TX "uartTx DataInHex" </mark><br />
https://192.168.1.10:5000/Command?piCmd=uartTx 1234<br /><br />
<mark class="yellow">4) UART RX "uartRx ByteReadCount"</mark><br />
https://192.168.1.10:5000/Command?piCmd=uartRx 4<br /><br />
<mark class="yellow">5) UART TX and RX "uartTxRx ByteReadCount SendDataInHex"</mark><br />
https://192.168.1.10:5000/Command?piCmd=uartTxRx 3 01FF<br /><br />
<mark class="yellow">6) SPI TX and RX"spiTxRx DataInHex"</mark><br />
https://192.168.1.10:5000/Command?piCmd=spiTxRx 01FF<br /><br />
<mark class="yellow">7) I2C Read "i2cRead Address RegAdd ByteReadCount"</mark><br />
https://192.168.1.10:5000/Command?piCmd=i2cRead 01 02 03<br /><br />
<mark class="yellow">8) I2C Write "i2cAddress RegAdd TxDataInHex"</mark><br />
https://192.168.1.10:5000/Command?piCmd=i2cWrite 01 02 01FF<br /><br />
<mark class="yellow">9) PWM Set supported on GPIO12 and 13 "pwmSet Pwmpin DutyCycle(0:0percent to 1000:100persent) Frequency(Hz)"</mark><br />
RC servo rotation 0, 1ms width, use https://192.168.1.10:5000/Command?piCmd=pwmSet 13 50 50<br />
RC servo rotation 0, 1ms width, use https://192.168.1.10:5000/Command?piCmd=pwmSet 13 100 50<br />
https://192.168.1.10:5000/Command?piCmd=pwmSet 13 50 1000<br /><br />
<mark class="yellow">10) Read Gpio "gpioRead GpioPin"</mark><br />
https://192.168.1.10:5000/Command?piCmd=gpioRead 13<br /><br />
<mark class="yellow">11) Write Gpio "gpioWrite GpioPin value"</mark><br />
https://192.168.1.10:5000/Command?piCmd=gpioWrite 13 0<br /><br />
</p>

<h1 style="font-size:25px; color:green;">3) JSON API Format</h1>
<p>req.post(url1,verify=False,timeout=5,json={'piCmd': 'pwmSet 13 100 50'})<br />
Response is always in raw string format<br /><br />
</p>

<h1 style="font-size:25px; color:green;">3) Token Generation</h1>
<h1 style="font-size:25px; color:green;">4) Contect</h1>
</body>
</html>

'''
#################### Pheripherals #################
def uartInit(uartBaud = 9600,uartTimeout=1): #9600,sec
    global serialObject0
    serialObject0 = serial.Serial("/dev/ttyS0", uartBaud, timeout=uartTimeout)
    serialObject0.close()
    print("Uart Serial Port Initialized")
    return("uartInit")
def uartTx(byteListIn):
    global serialObject0
    if(serialObject0 == 0):
       uartInit()
    serialObject0.open()
    serialObject0.reset_input_buffer()
    serialObject0.reset_output_buffer()
    serialObject0.write(byteListIn)
    # wait for tx to finish?
    serialObject0.close()
    print ("UART Sent :", byteListIn)
    return("uartTx")
def uartRx(lenToRead):
    global serialObject0
    if(serialObject0 == 0):
       uartInit()
    serialObject0.open()
    byteListOut = serialObject0.read(lenToRead)
    serialObject0.reset_input_buffer()
    serialObject0.reset_output_buffer()
    serialObject0.close()
    print ("UART receive :", byteListOut)
    return("uartRx "+List2hexStr(byteListOut))

def uartTxRx(readLen,byteListIn):
    global serialObject0
    if(serialObject0 == 0):
        uartInit()
    if(len(byteListIn)):
        serialObject0.open()
    serialObject0.reset_input_buffer()
    serialObject0.reset_output_buffer()
    serialObject0.write(byteListIn)
    byteListOut = serialObject0.read(readLen)
    #print(byteListOut)
    serialObject0.reset_input_buffer()
    serialObject0.reset_output_buffer()
    serialObject0.close()
    print ("UART Sent :", byteListIn)
    print ("UART receive :", byteListOut)
    return("uartTxRx "+List2hexStr(byteListOut))


def spiTxRx(byteListIn):
    spi = spidev.SpiDev()
    spi.open(0,0) #bus=0, ch=0
    print("Spi Send :",byteListIn)
    byteListOut = spi.xfer2(byteListIn) # byteListOut is byte list return bytes
    print("Spi Receive :",byteListOut)
    return("spiTxRx "+List2hexStr(byteListOut))
    
def i2cRead(i2c_address,reg_config,bytesToRead):
    global i2c_ch
    # Initialize I2C (SMBus)
    bus = smbus.SMBus(i2c_ch)
    byteListOut = bus.read_i2c_block_data(i2c_address, reg_config, bytesToRead)
    print("I2c Read:", byteListOut)
    return("i2cRead "+List2hexStr(byteListOut))
    
def i2cWrite(i2c_address,reg_config,byteListIn):
    global i2c_ch
    bus = smbus.SMBus(i2c_ch)
    print("I2c Send :",byteListIn)
    bus.write_i2c_block_data(i2c_address, reg_config, byteListIn)
    return("i2cWrite")
def pwmSet(pin,duty,freq=1000): # pin =12 and 13 , dut 0 -100, frq in khz
    global pi
    if((pin == 12) or (pin == 13)):
        if not pi.connected:
            return("error")
        pi.set_mode(pin, pigpio.OUTPUT)
        pi.hardware_PWM(pin, freq, 1e3*duty) # frq in Hz  dutycycle 0:0% to 1000:100%
        print("Pin12 pwm set")
        return("pwmSet "+str(pin))
    else:
        print("Inavlid input")
        return("error")
def pwmGet(pin):
    return("error")

def pwmStop(pin):
    return("error")
 
def initGpio():
    global gpioInit
    # Use GPIO numbers not pin numbers
    if(gpioInit==0):
        GPIO.setmode(GPIO.BCM)
        gpioInit = 1

def gpioWrite(pin,value):
    # set up the GPIO channels - one input and one output
    GPIO.setup(pin, GPIO.OUT)
    if(value):
        GPIO.output(pin, True) 
    else:
        GPIO.output(pin, False)
    print("GPIO value write pin,value",pin,value)
    return("gpioWrite "+str(pin)+" "+str(value))

def gpioRead(pin):    
    GPIO.setup(pin, GPIO.IN)
    value = GPIO.input(pin)
    print("GPIO value Read pin,value",pin,value)
    return("gpioRead "+str(pin)+" "+str(value))

###################
# function return  bytes from hex string it only process 0-9 ,a-f , A-F else thows exception
# eg "01FF" =   [1,255] ,---- "1" invalid input , "01" this is valid input shuld be multiple of 2
###################
def hexStr2List(hexStr):
    data = bytearray.fromhex(hexStr) # get bytes from hex string
    return (list(data))

###################
# function return  bytes from hex string it only process 0-9 ,a-f , A-F else thows exception
# eg [1,255]=  "01FF"  ,---- "1" invalid input , "01" this is valid input shuld be multiple of 2
###################
def List2hexStr(listObj):
    res = ''.join(format(x, '02x') for x in listObj)
    return(res)
def ProcessData(msg):#string bytes
    print('Message Received {}'.format(msg))
    cmd = (msg.decode("utf-8")).split(' ') # make list
    initGpio()
    if(cmd[0] == "uartInit"):
        res = uartInit(int(cmd[1]),int(cmd[2]))
    elif(cmd[0] == "uartTx"):
        res = uartTx(hexStr2List(cmd[1]))
    elif(cmd[0] == "uartRx"):
        res = uartRx(int(cmd[1]))
    elif(cmd[0] == "uartTxRx"):
        res = uartTxRx(int(cmd[1]),hexStr2List(cmd[2]))
    elif(cmd[0] == "spiTxRx"):
        res = spiTxRx(hexStr2List(cmd[1]))
    elif(cmd[0] == "i2cRead"):
        res  = i2cRead(int(cmd[1]),int(cmd[2]),int(cmd[3]))
    elif(cmd[0] == "i2cWrite"):
        res = i2cWrite(int(cmd[1]),int(cmd[2]),hexStr2List(cmd[3]))
    elif(cmd[0] == "pwmSet"):
        res = pwmSet(int(cmd[1]),int(cmd[2]),int(cmd[3]))
    elif(cmd[0] == "pwmStop"):
        res = pwmStop(int(cmd[1]))
    elif(cmd[0] == "gpioRead"):
        res = gpioRead(int(cmd[1]))
    elif(cmd[0] == "gpioWrite"):
        res = gpioWrite(int(cmd[1]),int(cmd[2]))
    elif(cmd[0] == "htmlMenu"):
        res = htmlMenu
    else:
        res = "error"
    print("Sending Response: {}".format(res))
    return(res.encode('utf-8'))
def onNewClient(clientsocket,addr):
    msg = clientsocket.recv(1024)
    #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
    try:
        resBytes = ProcessData(msg)
        clientsocket.send(resBytes)
    except:
        clientsocket.send(b"error")
    print("connection Close")
    clientsocket.close()

def startServer(host,port):     
    s = socket.socket()         # Create a socket object
    print("host name : {} port :{}".format(host,port))
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # It can listen up to 5 clients
    while True:
        clientsocket, addr = s.accept()     # Establish connection with client.
        print('Got connection from', addr)
        x = threading.Thread(target=onNewClient, args=(clientsocket,addr))
        x.start()
    s.close()
    

host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
print("Starting piLib Server")
pi = pigpio.pi()
startServer(host,port)
GPIO.cleanup()
#PINS are GPIO pins
'''
print(ProcessData(b"uartInit 9600 1"))
print(ProcessData(b"uartTx 1234"))
print(ProcessData(b"uartRx 4"))
print(ProcessData(b"uartTxRx 3 01FF"))

print(ProcessData(b"spiTxRx 01FF"))

#print(ProcessData(b"i2cRead 01 02 03")) # i2c need device to be connected
#print(ProcessData(b"i2cWrite 01 02 01FF"))

print(ProcessData(b"pwmSet 13 50 1000"))
print(ProcessData(b"pwmGet 13"))
print(ProcessData(b"pwmStop 13"))
while True:
    print(ProcessData(b"gpioWrite 14 0"))
    time.sleep(1)
    print(ProcessData(b"gpioWrite 14 1"))
    time.sleep(1)
print(ProcessData(b"gpioRead 13"))
print(ProcessData(b"gpioRead 13"))
print(ProcessData(b"gpioWrite 13 1"))
print(ProcessData(b"gpioRead 13"))
'''
