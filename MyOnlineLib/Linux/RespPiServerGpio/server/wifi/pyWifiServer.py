from flask import Flask, request, send_from_directory, send_file
from werkzeug.utils import secure_filename
import time
import os
import threading
import inspect
import socket               # Import socket module

piServ = 1 # if running on repberry pi set it to 1

def get_abs_filename(relativFilePath): #relative path to script is input, if script run from other folder use this function to get path
    dirname = os.path.dirname(__file__) 
    filename = os.path.join(dirname, relativFilePath) 
    print(filename)
    return (filename)

print("Current working directory: {0}".format(os.getcwd()))
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "files" # folder path
app.config["MAX_CONTENT_PATH"] = 1024*4   # 4K max file size excepted
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# note in querry sting do not use underscore some server dont like it
@app.route('/greeting/<name>')# "http://192.168.1.2:5000/greeting/Nand" , Nand will be parameter to fuction
def give_greeting(name):
    return 'Hello, {0}!'.format(name)
    
@app.route('/menu') # string to be used by clint "https://192.168.1.10:5000/menu"
def menu():         # function to be used when this string received
    res = sendCommand("htmlMenu".encode('utf-8'))# string to bytes
    return(res.decode("utf-8"))
# Flask Arguments
# The query string begins after the question mark (?) character, And has key-value pairs separated by an ampersand (&) character:
#example.com?arg1=value1&arg2=value2

@app.route('/testGetPost',methods=['GET', 'POST'])# string to be used by clint "http://192.168.1.2:5000/testGetPost?pin=1&value=2"
def testGetPost():
    # auto argument handling , use below if argument is must 
    # if key doesn't exist, returns a 400, bad request error
    #framework = request.args['framework']
    
    # if key doesn't exist, returns None , user handles based on return type , in above method flash handles with error 400 "BAD request automatically"
    #pin = request.args.get('pin')
    pin = request.args['pin']                 # must argument
    value = request.args.get('value')             # optional
    if request.method == 'POST':
        return("Post sucess")
    else:#get
         return("Get sucess")

@app.route('/Command', methods=['GET', 'POST'])# string to be used by clint "https://192.168.1.10:5000/Command" and followed by json data object
def Command():
    piCmd = ""
    if(request.is_json):
        content = request.json
        piCmd = content['piCmd'] 
    else:
        piCmd = request.args['piCmd']                 # must argument
    print("Command Received on Wifi :{}".format(piCmd))
    res = sendCommand(piCmd.encode('utf-8'))# string to bytes
    return(res.decode("utf-8")) # return string alwys
##########################TOken Based####################################
'''
def hexStr2Bytes(hexStr):
    data = bytearray.fromhex(hexStr) # get bytes from hex string
    return(data)
def xorBytes(var, key):
    return bytes(a ^ b for a, b in zip(var, key))
'''
@app.route('/file', methods=['GET', 'POST'])
def File():
    # auto argument handling , use below if argument is must 
    # if key doesn't exist, returns a 400, bad request error
    #framework = request.args['framework']
    print("got file request\nData:"+ ' '.join('{:02x}'.format(x) for x in request.data)  )
    print("Args:")
    print(request.args )
    print("Form:")
    print(request.form )
    print("value:")
    print(request.values )
    
    # if key doesn't exist, returns None , user handles based on return type , in above method flash handles with error 400 "BAD request automatically"
    #if(not allowed_file):
    #return 'file not allowd'
    if request.method == 'POST':
        print("POST request:")
        #request_data = request.form['info_text']
        #print("info:" + request_data)
        f = request.files['filename']
        f.save(secure_filename("abc.txt"))
        return 'file uploaded successfully' #return "OK", 200
    else:
        #f = request.files['filename']
        uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER']) + "\kbc.txt"
        print(uploads)
        return(send_file(uploads, as_attachment=True))
        #return send_from_directory(directory=uploads, filename="test1.txt")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sendCommand(reqBytes):
    host = socket.gethostname() # Get local machine name
    port = 12345                # Reserve a port for your service.
    s = socket.socket()         # Create a socket object
    s.connect((host, port))
    print("sending Request :{}".format(reqBytes))
    s.settimeout(10)
    s.send(reqBytes)
    respBytes = s.recv(1024*4) # max 4K size can be received
    s.close()                     # Close the socket when done
    print("Response received :{}".format(respBytes))
    return(respBytes)
    
#################main#########
if __name__ == '__main__':
    #app.run(debug= True, host = '0.0.0.0')
    print("RespBerry Server")
    path1 = get_abs_filename('servernamePiCert.pem') # this is needed if you run script from other folder, to conver all relative path to full path
    path2 =  get_abs_filename('servernamePiPrivateKey.pem')  # this is needed if you run script from other folder, to conver all relative path to full path
    app.run(debug= True, host = '0.0.0.0' ,ssl_context=(path1, path2)) #CN = 192.168.1.10
    #host = '0.0.0.0' all can access this website , remove ssl_context=('cert.pem', 'key.pem')