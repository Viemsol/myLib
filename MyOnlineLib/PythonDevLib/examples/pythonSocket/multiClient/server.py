#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import threading

def onNewClient(clientsocket,addr):
    msg = clientsocket.recv(1024)
    #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
    print(msg)
    clientsocket.send(msg)
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
        x = threading.Thread(target=onNewClient, args=(clientsocket,addr), daemon=False)
        x.start()
    s.close()

host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
startServer(host,port)

