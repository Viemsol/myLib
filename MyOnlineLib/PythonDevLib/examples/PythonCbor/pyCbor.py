from cbor2 import dump, CBORTag, dumps, loads
import json

def cborWrite(file):
    obj = 0
    # Efficiently deserialize from a file
    with open(file, 'rb') as fp:
        obj = load(fp)
    return obj    
def cborWrite(obj,file): #file'output.cbor'
    # Efficiently serialize an object to a file
    with open(file, 'wb') as fp:
        dump(obj, fp)

# note heare  CBOR used for transmitting data over network and use JSOn for processing.
jsonData ={"name": "Amar", "age": 40, "city": "New York"}
print("Jason Data: {}".format(jsonData))

# Serialize an json object to CBOR
cborEnc = dumps(jsonData)
print("Cbor Encoded Data: {}".format(cborEnc))
# Deserialize a CBOR to Python
# data is in binary form , convert it tinto string
cborDec = loads(cborEnc)
print("Cbor Decoded Data: {}".format(cborDec))
jsonStr = json.dumps(cborDec) # create json string from list 
print("Json String Data: {}".format(jsonStr))
# create python dictionay out of Json string
jsonDict = json.loads(jsonStr) # parse json to dictonary
print("Json Dictionary Data: {}".format(jsonDict))
print( "Json Value for key 'name' : {}".format(jsonDict["name"]))
