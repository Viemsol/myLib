import BaseHTTPServer, SimpleHTTPServer
import ssl
import argparse
import os

parser = argparse.ArgumentParser(description='Local Server')
parser.add_argument('-p', '--port', dest='port', type= int,
    help= "Server Port", default= 8000)
parser.add_argument('-ip', '--ip', dest='ip', type= str,
    help= "Server ip", default= '0.0.0.0')
args = parser.parse_args()

httpd = BaseHTTPServer.HTTPServer((args.ip, args.port),
        SimpleHTTPServer.SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket,
        keyfile= "ca_key.pem",
        certfile= "ca_cert.pem", server_side=True)
print "Serving on", args.ip, args.port
httpd.serve_forever()