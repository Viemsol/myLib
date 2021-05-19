#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import time

def startClient(host,port):
    while True:
        s = socket.socket()         # Create a socket object
        print("client name : {} port:{}".format(host,port))
        s.connect((host, port))
        s.send(b'Request from Client1')
        a = s.recv(1024)
        print(a) # procces responce
        if(a == 'quit'):
            break;
        time.sleep(5)
    s.close()                     # Close the socket when done

host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
startClient(host,port)