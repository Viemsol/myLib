#import btpycom
import smbus
import serial
import spidev
import RPi.GPIO as GPIO

i2c_ch = 1
pwm12 = 0
pwm13 = 0
serialObject0 = 0
gpioInit = 0
pi_pinst = 0

#################### Pheripherals #################
def uartInit(uartBaud = 9600,uartTimeout=1): #9600,sec
    global serialObject0
    serialObject0 = serial.Serial("/dev/ttyS0", uartBaud, timeout=uartTimeout)
    serialObject0.close()
    print("Uart Serial Port Initialized")

def uartTx(bArray):
    global serialObject0
    serialObject0.open()
    serialObject0.reset_input_buffer()
    serialObject0.reset_output_buffer()
    serialObject0.write(bArray)
    # wait for tx to finish?
    serialObject0.close()
    print ("UART Sent :", bArray)

def uartRx(lenToRead):
    global serialObject0
    serialObject0.open()
    tmp_info = serialObject0.read(lenToRead)
    serialObject0.reset_input_buffer()
    serialObject0.reset_output_buffer()
    serialObject0.close()
    print ("UART receive :", tmp_info)
    return tmp_info

def SendAndRead(bArray,readLen):
    global serialObject0
    tmp_info = 0;
    if(len(bArray)):
        serialObject0.open()
        serialObject0.reset_input_buffer()
        serialObject0.reset_output_buffer()
        serialObject0.write(bArray)
        tmp_info = serialObject0.read(readLen)
        #print(tmp_info)
        serialObject0.reset_input_buffer()
        serialObject0.reset_output_buffer()
        serialObject0.close()
        print ("UART Sent :", bArray)
        print ("UART receive :", tmp_info)
    return(tmp_info)

def spiSendRcv(byteArr):
    spi = spidev.SpiDev()
    spi.open(0,0) #bus=0, ch=0
    print("Spi Send :",byteArr)
    r = spi.xfer2(byteArr) # r is byte array return bytes
    print("Spi Receive :",r)
    return(r)
    
def i2cRead(i2c_address,reg_config,bytesToRead):
    global i2c_ch
    # Initialize I2C (SMBus)
    bus = smbus.SMBus(i2c_ch)
    val = bus.read_i2c_block_data(i2c_address, reg_config, bytesToRead)
    print("I2c Read:", val)
    return(val)
    
def i2cWrite(i2c_address,reg_config,bytesArr):
    global i2c_ch
    bus = smbus.SMBus(i2c_ch)
    print("I2c Send :",bytesArr)
    bus.write_i2c_block_data(i2c_address, reg_config, bytesArr)
    return(bytesArr)
    
def pwmSet(pin,duty,freq=1000): # pin =12 and 13 , dut 0 -100, frq in khz
    global pwm12
    global pwm13
    if(pin == 12):
        if(pwm12==0):
            GPIO.setup(pin, GPIO.OUT)  # Set GPIO pin 12 to output mode.
            pwm12 = GPIO.PWM(pin, freq)   # Initialize PWM on pwmPin 100Hz frequency
            pwm12.start(duty)
        pwm12.ChangeDutyCycle(duty)
        print("pin,Dutycycle",pin,duty)
        return("Pin12 pwm set")
    if(pin == 13):
        if(pwm13==0):
            GPIO.setup(pin, GPIO.OUT)  # Set GPIO pin 12 to output mode.
            pwm13 = GPIO.PWM(pin, freq)   # Initialize PWM on pwmPin 100Hz frequency
            pwm13.start(duty)
        pwm13.ChangeDutyCycle(duty)
        print("pin,Dutycycle",pin,duty)
        return("Pin13 pwm set")
    else:
        return("Inavlid input")
def pwmGet(pin):
    return("Not implemented")

def pwmStop(pin):
    global pwm12
    global pwm13
    if(pin == 12):
        if(pwm12):
            pwm12.stop()                         # stop PWM
            pwm12 = 0
            print("Pwm Stop pin",pin)
    if(pin == 13):
        if(pwm13):
            pwm13.stop()                         # stop PWM
            pwm13 = 0
            print("Pwm Stop pin",pin)

def initGpio():
    global gpioInit
    # Use GPIO numbers not pin numbers
    if(gpioInit==0):
        GPIO.setmode(GPIO.BCM)
        gpioInit = 1

def gpioSet(pin,value):
    # set up the GPIO channels - one input and one output
    initGpio()
    if(GPIO.OUT != GPIO.gpio_function(pin)):
        GPIO.setup(pin, GPIO.OUT)
    if(value):
        GPIO.output(pin, True) 
    else:
        GPIO.output(pin, False)
    print("GPIO value write pin,value",pin,value)

def gpioRead(pin):    
    initGpio()
    if(GPIO.IN != GPIO.gpio_function(pin)):
        GPIO.setup(pin, GPIO.IN)
    value = GPIO.input(pin)
    print("GPIO value Read pin,value",pin,value)
    return(value)


###################Testing###############################
#GPIO.setwarnings(False)
print("GPIO test")
print("Set pin 17")
gpioSet(17,1)
print("Read pin 17")
print(gpioRead(17))
print("Clear pin 17")
gpioSet(17,0)
print("Read pin 17")
print(gpioRead(17))

print("PWM test")
print("Set PWM at pin 12, 50%,1Khz")
pwmSet(12,50,1000)


print("I2C test")

i2cData = list(b'i2cData') # conver string to list of chaecters
i2cData=map(lambda x:ord(x),i2cData) # convert list of charecter to list of integer / bytes
print("I2C write Test")
i2cWrite(0x01,0x02,i2cData)
print("I2C read Test")
i2cRead(0x01,0x02,3)# read 3 bytes

print("SPI test")
spiData = list(b'spibyte') # conver string to list of chaecters
spiData=map(lambda x:ord(x),spiData) # convert list of charecter to list of integer / bytes
print("SPI read/write Test")
spiSendRcv(spiData)

print("UART test")
uartData = list(b'i2cDataerfrgt') # conver string to list of chaecters
uartData=map(lambda x:ord(x),uartData) # convert list of charecter to list of integer / bytes
print("UART read/write Test")
uartInit()
uartTx(uartData)
uartRx(uartData)
SendAndRead(uartData,10)# send and then read 10 bytes
