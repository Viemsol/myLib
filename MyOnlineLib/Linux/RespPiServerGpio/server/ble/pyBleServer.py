#!/usr/bin/env python
#Run.py
import os
from bluetooth import *
#from wifi import Cell, Scheme
import subprocess
import time

wpa_supplicant_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"
sudo_mode = "sudo "
menuOption="---Menu---\n1:Configur Wifi\n2:Get Pi Ip Address\n3:GPIO Test\n4:I2C test\n5:UART Test\n6:PWM Test\n7:Set Password\nSelect Option:\n"
def CreateWifiConfig(SSID, password):
    config_lines = [
    '\n',
    'network={',
    '\tssid="{}"'.format(SSID.strip()),
    '\tpsk="{}"'.format(password.strip()),
    '\tkey_mgmt=WPA-PSK',
    '}'
    ]

    config = '\n'.join(config_lines)
    print(config)

    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a+") as wifi:
        wifi.write(config)

    print("Wifi config added")
  
def wifi_connect(ssid, psk):
    # write wifi config to file
    CreateWifiConfig(ssid,psk)
    # reconfigure wifi
    cmd = sudo_mode + 'wpa_cli -i wlan0 reconfigure'
    cmd_result = os.system(cmd)
    print (cmd + " - " + str(cmd_result))
    time.sleep(10)
    cmd = 'iwconfig wlan0'
    cmd_result = os.system(cmd)
    print (cmd + " - " + str(cmd_result))
    cmd = 'ifconfig wlan0'
    cmd_result = os.system(cmd)
    print (cmd + " - " + str(cmd_result))
    p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = p.communicate()
    if out:
        ip_address = out.strip()
    else:
        ip_address = "<Not Set>"
    return ip_address

def readDataStrip():
    cmd = client_sock.recv(1024)
    return(cmd.strip())

def handle_client(client_sock) :
    # get ssid
    client_sock.settimeout(60) # Sets the socket to timeout after 60 second of no activity
    client_sock.send("Enter Password:\n")
    cmd = readDataStrip()
    if(cmd != '1234'):
        client_sock.send("Invalid Password:" + cmd)
        return
    client_sock.send(menuOption)
    cmd = readDataStrip()
    print ("command Received: "+cmd)
    if(cmd == ''):
        return
    if(cmd == '1'):# set SSID PW
        print("set SSID PW")
        client_sock.send("Enter  WIFI SSID:\n")
        print ("Waiting for SSID...")
        ssid = readDataStrip()
        if ssid == '' :
            return
        print ("ssid received")
        print (ssid)
        # get psk
        client_sock.send("Enter WIFI SSID:\n")
        print ("Waiting for PSK...")
        psk = readDataStrip()
        if psk == '' :
            return
        print ("psk received")
        print (psk)
        ip_address = wifi_connect(ssid, psk)
        print ("ip address: " + ip_address)
        client_sock.send("Connected to ip-address:" + ip_address + "!")

    elif(cmd == '2'): # get IP
        print("get IP")
        p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            ip_address = out
        else:
            ip_address = "<Not Set>"
        client_sock.send("IP Address:"+ip_address)
    else:
        client_sock.send("\nThis Option not implemented\n")
    client_sock.send("\nSession Closed, Reconnect Socket\n\n")
#serial port profile set
#sudo sdptool add SP
time.sleep(10) # learning if this delay is not their sudo commab not work
out = os.system("sudo sdptool add SP")
print("Running Port.py\nadding serial port profile :",out)

#subprocess.call(['sdptool', 'add','SP'], shell=True)
try:
    while True:
        server_sock=BluetoothSocket( RFCOMM )
        server_sock.bind(("",PORT_ANY))
        server_sock.listen(1)
        port = server_sock.getsockname()[1]
        uuid = "815425a5-bfac-47bf-9321-c5ff980b5e11"
        advertise_service( server_sock, "RPi Wifi config",
                           service_id = uuid,
                           service_classes = [ uuid, SERIAL_PORT_CLASS ],
                           profiles = [ SERIAL_PORT_PROFILE ])
        print ("Waiting for connection on RFCOMM channel %d" % port)
        client_sock, client_info = server_sock.accept()
        print ("Accepted connection from ", client_info)
        try:
            handle_client(client_sock)
        except Exception as error:#this will only happen on soket timed out after 60 second
            print ("Caught BluetoothError: ", error)
        client_sock.close()
        server_sock.close()
except (KeyboardInterrupt, SystemExit):
    print ('\nExiting\n')