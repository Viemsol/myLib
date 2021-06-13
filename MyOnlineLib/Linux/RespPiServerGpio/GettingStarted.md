# Pi zero 

## Setup Hardware
- Format (use SD card formatter Software)8 GB sd card and install repbian OS with Basic graphis using image.exe utility
- Other method is download .iso file from https://www.raspberrypi.org/software/operating-systems/ and write it to sd card using Win32 Disk imager
- inser SD card to pi and boot , check Destop , mouse  keyboard working.
- change respberry pi password
- Connect to wifi
- Go to Start - > Configurations -> Enable Needed Pheripherals -> Camera -> GPIO -> SSH etc save and reboot.

## Configure static ip address for repberry pi
On your LAN / WIFI local network, The private IP addresses of individual devices can change though, depending on the configuration of the DHCP server.
To be able to reach Raspberry Pi on the same address in your own LAN, you have to provide it with a static, private IP address. 

On Netger wifi rauter Login **192.168.1.1** with UN:admin, PW:password

On hatway ZTE wifi rauter Login **192.168.1.1** with UN:admin, PW:MACADDRESS without colon i.e(94E3EE04D430)

Select ADVANCED > Setup > LAN Setup. The LAN page displays. In the Address Reservation section, click the Add button.
Select IP , MAC  address you want save and restart RPi. 192.168.1.x. => 192.168.1.10.

Now from your open cmd and try > ping 192.168.1.10 , Rpi should respond

## Running SSH on Repberi Pi

![Image ](image/puttySSh.png)

Once login is success try below command in putty shell
```code
python3 --version 
```
## Install below modules  on pi via ssh

```code
sudo apt install bluetooth libbluetooth-dev
pip3 install pybluez
```

## Raspberry Pi Info 

Note: the numbering of the GPIO pins is not in numerical order; GPIO pins 0 and 1 are present on the board (physical pins 27 and 28) but are reserved for advanced use (see below).

![Image ](image/RaspberryPiZeroW5.jpg)

- Voltages
Two 5V pins and two 3V3 pins are present on the board, as well as a number of ground pins (0V), which are unconfigurable. The remaining pins are all general purpose 3V3 pins, meaning outputs are set to 3V3 and inputs are 3V3-tolerant.

- Outputs
A GPIO pin designated as an output pin can be set to high (3V3) or low (0V).

- Inputs
A GPIO pin designated as an input pin can be read as high (3V3) or low (0V). This is made easier with the use of internal pull-up or pull-down resistors. Pins GPIO2 and GPIO3 have fixed pull-up resistors, but for other pins this can be configured in software.

- More
As well as simple input and output devices, the GPIO pins can be used with a variety of alternative functions, some are available on all pins, others on specific pins.

    - PWM (pulse-width modulation)
    Software PWM available on all pins
    Hardware PWM available on GPIO12, GPIO13, GPIO18, GPIO19
    - SPI
    SPI0: MOSI (GPIO10); MISO (GPIO9); SCLK (GPIO11); CE0 (GPIO8), CE1 (GPIO7)
    SPI1: MOSI (GPIO20); MISO (GPIO19); SCLK (GPIO21); CE0 (GPIO18); CE1 (GPIO17); CE2 (GPIO16)
    - I2C
    Data: (GPIO2); Clock (GPIO3)
    - EEPROM Data: (GPIO0); EEPROM Clock (GPIO1)
    - Serial
    TX (GPIO14); RX (GPIO15)
    
Type below command to get all pins status.This tool is provided by the GPIO Zero Python library, which is installed by default on the Raspberry Pi OS desktop image, but not on Raspberry Pi OS Lite.
```code
pinout
```

![Image ](image/gpio.png)

Python script to read and write GPIO.To control an LED connected to GPIO17, and Button at GIO 2:
Note pin value passed as  parameter is GPIO no and not physical pin no , refer above diagram
```code
from gpiozero import LED, Button

led = LED(17)
button = Button(2)

while True:
    if button.is_pressed:
        led.on()
    else:
        led.off()
```

Use below command to edit Pheripheral configuration
```code
sudo nano /boot/config.txt
```

## Rpi WIFI Server 


### create server certs and python server script
    - Create Server CSR and get it signed by root CA. Refer Open SSL Document for creating same.
    - Keep Server Private key, Cert and python script in same folder in Rpi.

### Run WIFI Server in RPI

- copy all files from server/wifi to pi from pc (use CLI scp command for same).
- Make file Executable , File name change its color from gray to green.

```code
chmod +x pyWifiServer.py
```
- Run it

```code
sudo python pyWifiServer.py
```
- check if server is responding by below command

```code
https://192.168.1.10:5000/hello
crome may display site is unsafe but proceed (as cert is signed by self signed root crated by you)
```
- Now Test if server can be run in background as Demon task , go to root directory and try running server. this is to ensure that server runse even from root directory

```code
sudo nohup python /home/pi/Project/server/wifi/pyWifiServer.py &
```

- Now configure server in boot up task **rc.local** file (now on every boot server will be running)

```code
sudo nano /etc/rc.local
```

Add bleow lines at end just before exit 0

```code
#User specific scripts
sudo bash -c 'python /home/pi/Project/server/wifi/pyWifiServer.py > /home/pi/Project/server/wifi/pyWifiServer.txt 2>&1' &
```
- Now reboot RPi and check if server is running automatically on bootup

```code
sudo reboot
```
- Checking debug logs of server with below command all print and erros will be saved in below file
```code
cat /home/pi/Project/server/wifi/pyWifiServer.txt
```
- Now from your PC browser try connecting to server by 

```code
https://192.168.1.10:5000/hello
```

**Trouble shooting Wifi Server**
- Relative references of files (certificate and other files refereed in script) do not work when we run script from root (rc.local) so use complete path in script
- Server use port 5000. Server will not start if any program is using port 5000.Use below to check if any program is using port.
```code
    sudo lsof -i:5000
    or
    use below to kill
    sudo kill PID
    sudo kill 1234
```
- What if Wifi is not present will server start?
    
### Setup WIFI Soft AP on Rpi (RPI3 switch between wifi AP and client)

1) Setup Soft AP Configurations

```code
sudo apt-get install hostapd

sudo nano /etc/hostapd/hostapd.conf
# Set Below in same
interface=wlan0
ssid=HydroSys4
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=3
wpa_passphrase=password
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP

```

Edit Hostapd

```code
sudo nano /etc/init.d/hostapd

# Add Below to DAEMON_CONF

DAEMON_CONF=/etc/hostapd/hostapd.conf
```
2) Setting Up DNSMasq
It’s now time to install DNSMasq. DNSmasq is required to provide dhcp server for the wifi AP connection.

```code
sudo apt-get install dnsmasq

sudo nano /etc/dnsmasq.conf

# add below

interface=wlan0
dhcp-range=192.168.0.100,192.168.0.200,12h
```


To enable host apd on boot
```code
sudo systemctl enable hostapd.service 
```

To  activate the dnsmasq service at boot
```code
sudo systemctl enable dnsmasq.service 
```

3) Swiching from AP to client mode
```code
sudo systemctl stop hostapd.service
sudo systemctl stop dnsmasq.service
```

### Setup BLE Server on Rpi

- Install Bluz As above
Now edit below file and make sure Below is BLE discoverable always:

```code
sudo nano /etc/bluetooth/main.conf
and enale below lines
DiscoverableTimeout = 0
```

Now edit below file to run BLE in Compatibility mode:

```code
sudo nano /etc/systemd/system/dbus-org.bluez.service OR sudo nano /lib/systemd/system/bluetooth.service. Both are same.

change ExecStart=/usr/lib/bluetooth/bluetoothd to ExecStart=/usr/lib/bluetooth/bluetoothd -C
```

![Image ](image/bleserver.png)


- copy all files from server/ble to pi from pc (use CLI scp command for same).
- Make file Executable , File name change its color from gray to green.

```code
chmod +x pyBleServer.py
chmod +x sa.py
```

check if Pairing agent (simple agent by bluz)can run in demon(baground)



```code
sudo nohup python /home/pi/Project/server/ble/sa.py &

```

Run and test Serial Port profile BLE python Server 

```code
sudo python /home/pi/Project/server/ble/pyBleServer.py
```

Now Its time to put sa.py and pyBleServer.py to rc.local so taht they can run on bootup

```code
sudo nano /etc/rc.local
```

Add bleow lines at end just before exit 0

```code
#User specific scripts
sudo bash -c 'python /home/pi/Project/server/ble/sa.py > /home/pi/Project/server/ble/sa.txt 2>&1' &
sudo bash -c 'python /home/pi/Project/server/ble/pyBleServer.py > /home/pi/Project/server/ble/pyBleServer.txt 2>&1' &
```

![Image ](image/setDemonScripts.png)

- Now reboot RPi and check if BLE server is running automatically on bootup

```code
sudo reboot
```
- Checking debug logs of server with below command all print and erros will be saved in below file

```code
cat /home/pi/Project/server/ble/pyBleServer.txt
cat /home/pi/Project/server/ble/sa.txt
```

- Now from your Android mobile try pairing Resp-pi BLE device it suld not ask any pass key and get paired.
- Now Use any Bluetooth Terminal software and try connecting to server , on sucessfull connection BLE server shuld ask for password enter "1234"
- Server should display menu
- You can use this to check IP address of Rpi , this IP then used for COnnecting to pi remotely over shell/Putty
- You can also set new SSID and PW and connect 

All Wifi configurations are stored in below and can be edited with below command

```code
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

**Trouble shoot Ble Server:**
- if serial profile is not set properly by pyBleServer.py , while connection Android terminal will throw error. thre is sleep(10) delay in script, before we set it (sudo sdptool add SP).

- use below to test BLE manually

```code
sudo nano bluetoothctl 
```

- use blow to restat both ble damon tasks  (sa.py and pyBleServer.py )

```code
sudo systemctl daemon-reload;
```

- To restart bluetooth service if needed
```code
sudo systemctl restart bluetooth.service;
```
## SSH over USB

1)remove sd card and edit  **cmdline.txt**
After rootwait, append this text leaving only one space between rootwait and the new text (otherwise it might not be parsed correctly):
```code
modules-load=dwc2,g_ether
```
If there was any text after the new text make sure that there is only one space between that text and the new text
Save the file

2)edit  **config.txt**


Append this line to the bottom of it:
```code
dtoverlay=dwc2
```
Save the file

3) insert SD card to Pi, power Resp Pi, now open putty ssh session with name **raspberrypi.local**

4)If you have not enabled ssh OR no access to HDMI , save empty file named ssh in boot, **remove .txt** extension

5) user is **pi**, and the password is **raspberry**

6) use ifconfig and get usb0 ip address and now using windows command scp we can trasfer files using **scp**
## change UN and PW using SSH
 
To change PW type below and follow instructions
```code
passwd
```


## enable peripherals using SSH
Edit config.txt file OR use  **sudo respi-config**  and use arrow keys to configure 
1) edit sd card and open config.txt 
https://elinux.org/RPiconfig
i.e  add below to enable camera
```code
#Enable Camera
start_x=1
```

2) Add wifi config in below file 
```code
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

```
Add Below

```code
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=IN
network={
        ssid="yourSSID"
        psk="password"
        key_mgmt=WPA-PSK
}
```

## setting up mqtt on Rpi
https://www.youtube.com/watch?v=Pb3FLznsdwI

## Dynamic Ip and local IP

Dynamic IP is IP provided to WIFI Router by ISP and its comman to all devices conected to that rauter. Local IP is IP provided by Wifi Rauter to each device
connected to WIF rauter. Local IP can be made static by changeing WIFI settings. Dynamic or public IP can be made static by paying ISP.

### windoes command to get local IP
```code
ipconfig
``` 

### windoes command to get Dynamic or Public  IP
```code
nslookup myip.opendns.com resolver1.opendns.com
```

### Linux command to get local IP
```code
ifconfig
``` 

### Linux command to get Dynamic or Public  IP
```code
nslookup myip.opendns.com resolver1.opendns.com
```

## put your local website or IOT device communicate over Internet.

As we know Static Ip is costly we can use poer forwording to communicate with our devices over internet.

### 1) Port Forwording
Wifi rauter can be Configured to forword all request comming on that port to perticular static Local IP.
Public IP of rauter let say is 115.30.123.56 , and port forwarding config is 7867-> 168.197.1.3 then all request 115.30.123.56:7867 to port **7867**
will be forworded to 168.197.1.3 device.
As you know Public IP of router 115.30.123.56 may chnage on every poer cycle,thee shuld be some why to communicate it with remote device.
one way is to use some free db and alwys IOT db update that db every 10 min with Dynamic IP. now clint can get Dynamic IP of IOT device and connect with port
**7867**.

### 2) SSH Tunneling

### 2) Reverse SSH Tunneling 

## Attacks
### DNS Reflection ATTACk 
Attacker send dns request to serach google IP, but with source address= Attck ITEm address (flipkart IP), now DNS send repose(IP of gggole to flipkart) Source IP address. Attaker send differant DNS request for which rsponce from DNS is large data to flipkart and flipkart will be flodded with fals DNS responce.
Thow this DNS responces will be discared by flipkart as flip kart did not requested it,But it will waste its time processing/decryting same.

### TCP half or SYN half attack
Attacker spend TCP SYN packet  but with false or different source address in packet to server . server send TC ACK to unknown server and wait.
as unknown address do not replay. Attacker flood half TCP request from different computer and distributed computer to server, and Legitimate user get denial of service . 
