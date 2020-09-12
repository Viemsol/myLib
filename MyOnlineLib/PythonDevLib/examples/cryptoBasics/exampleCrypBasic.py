#pip install pycrypto
#notes
#binascii.hexlify,Return the hexadecimal representation of the binary data.very byte of data is converted into the corresponding 2-digit hex representation. The returned bytes object is therefore twice as long as the length of data.
from libAll.libDisp import *
from libAll.libCryp import *
import binascii
import zlib
import os
import textwrap

init(autoreset=True) # use init()  fro color to retain every print, use print(Style.RESET_ALL) to reset

def login():
    printI("You want to save password for this login in same file. how you will save it securly? ")
    while(True):
        passwordSHA256 = b"e10adc3949ba59abbe56e057f20f883e"
        g = input("Enter Password : ") 
        md5out = hashByteArray(strlen2ByteArray(g),'MD5')
        dispClear()
        printD ("MD5" ,md5out)
        if(binascii.hexlify(md5out) == passwordSHA256): #"123456"
            printS("Valid Password !!")
            break
        printE("Invalid Password !!")
        printI("Hint:MD5 digest of password is stored in code!"+Back.GREEN +"e10adc3949ba59abbe56e057f20f883e")
        printI("Passwords are not stored in Database, its Digest are stored in Database.\nso if Database is compromised Passwords are not known to Attacker.\nAlso when password is stored as Digest there are many passwords matching same digest")
def cryptoHash(byteArrayData):
    printH("CRYPTO HASHES")
    dispHashinfo()
    hashTest = hashByteArray(byteArrayData,'MD5') # its 20 byte long or its 160 bit size digest
    printD("MD5",hashTest)
    input("")
    hashTest = hashByteArray(byteArrayData,'SHA1') # its 20 byte long or its 160 bit size digest
    printD("SHA1",hashTest)
    input("")
    hashTest = hashByteArray(byteArrayData,'SHA256') # its 20 byte long or its 160 bit size digest
    printD("SHA256",hashTest)
    input("")
    hashTest = hashByteArray(byteArrayData,'SHA512') # its 20 byte long or its 160 bit size digest
    printD("SHA512",hashTest)
    input("")
    printD("CRC32",crc32ByteArray(byteArrayData))
    input("")
	
def cryptoSymatricEnc(padTest):
    printH("Symatric Encryption ")
    dispSymCryptInfo()
    printI("Notes: input text block size should be multiple of key size.\ni.e key is 16 bytes then input text should be padded so that its multiple of 16 bytes.\n")
    printD("PAD",padTest)
    key = getRand(16)
    iv = getRand(16)
    input("")
    printD('KEY-ECB',key)
    printD('IV-ECB',iv)
    input("")
    encData = encDataSym(padTest,key,iv,'AESECB',1)#padding of data is handled automatically by hash function
    printD('ENC-ECB',encData)
    input("")
    decData = encDataSym(encData,key,iv,'AESECB',0)#padding of data is handled automatically by hash function
    printD('DEC-ECB',decData)
    input("")
    encData = encDataSym(padTest,key,iv,'AESCBC',1)#padding of data is handled automatically by hash function
    printD('ENC-CBC',encData)
    input("")
    decData = encDataSym(encData,key,iv,'AESCBC',0)#padding of data is handled automatically by hash function
    printD('DEC-CBC',decData)
    input("")

def cryptoSymatricEncAuth(padTest):
    printH(" Symatric Encryption with Authentication ")
    dispSymCryptWithAuthInfo()
    input("")
    printD("PAD",padTest)
    input("")
    aesAuthKey = genKeySec('AESGCM',16)
    printD('KEY-GCM',aesAuthKey)
    input("")
    nonce = getRand(12)
    printD('NONC-GCM',nonce)
    input("")
    auth = getRand(12)
    printD('NONC-GCM',auth)
    input("")
    encDataAuth = encDataSymAuth(padTest,aesAuthKey,auth,nonce,'AESGCM',1)
    printD('ENC-GCM',encDataAuth)
    decDataAuth = encDataSymAuth(encDataAuth,aesAuthKey,auth,nonce,'AESGCM',0)
    printD('DEC-GCM',decDataAuth)
    input("")
    printI("if ay of Encrypted data/nonce/key/Authdata changed then Authentication fails!!!\nIn this example 0th byte of encrypted text is now changed to 0x01 and tryed to decrypt.\nAESGCM can detect liability in cypher text!!")
    input("")
    positionIdx = 0
    printI("Blow is Valid Encrypted text")
    printD('ENC-GCM',encDataAuth)
    input("")
    encDataAuth[positionIdx] = 0x01
    printI("Blow is Encrypted text miliated .. check 1st byte its changed to " +Back.GREEN +"0x01"+Back.RESET)
    printI("AES-GCM Algorithm On Decryption of this miliated text can validate data integrity failure")
    printI("AES Algorithm canot detect data integrity by itself , so we need to implement it saperately and validate it seperately")
    printD('ERR-GCM',encDataAuth)
    input("")
    printI("Decrypting Data...")
    decDataAuth = encDataSymAuth(encDataAuth,aesAuthKey,auth,nonce,'AESGCM',0)
    printD('DEC-GCM',decDataAuth)

def cryptoSigning(padTest):
    dispAsymInfo()
    dispECCInfo()
    dispRsaInfo()
    printD("PAD",padTest)
    input("")
    printGreen("ASymatric Encryption Test : ECC")
    printI("Key pair generation,Signature and Signature varification")
    input("")
    eccPrivKey = getPrivKey('SECP256R1')
    printD("ECC_PRK",bytearray(serializePrivKey(eccPrivKey,'1234'))) # private key stored encrypted
    input("")
    eccPubKey = getPublKey(eccPrivKey)
    printD("ECC_PUK",bytearray(serializePubKey(eccPubKey))) # private key stored encrypted
    input("")
    printI("Varifiying Signature")
    input("")
    sig = signData(padTest,eccPrivKey)
    printD("ECC_SIG",bytearray(sig))
    if(signVerifyData(padTest,sig,eccPubKey)):
        printS("Valid Signature")
    else:
        printE("Invalid Signature")
    input("")
    printGreen("ASymatric Encryption Test : RSA")
    input("")
    rsaPrivKey = getPrivKey('RSA2048')
    printD("RSA_PRK",bytearray(serializePrivKey(rsaPrivKey,'1234'))) # private key stored encrypted
    input("")
    rsaPubKey = getPublKey(rsaPrivKey)
    printD("RSA_PUK",bytearray(serializePubKey(rsaPubKey))) # private key stored encrypted
    input("")
    
    sig = signData(padTest,rsaPrivKey)
    printD("RSA_SIG",bytearray(sig))
    input("")
    printI("Varifiying Signature with message") 
    input("")
    if(signVerifyData(padTest,sig,rsaPubKey)):
        printS("Valid Signature")
    else:
        printE("Invalid Signature")
    input("")    
    printGreen("Varifiying Signature with hash")
    input("")
    hash = hashByteArray(padTest,'SHA256')
    printD("SHA256",bytearray(hash))                       #hash digest SHA256      32
    input("")
    modulus = (rsaPubKey.public_numbers().n)               #modulus
    printD("RSA_MOD_",bytearray(intToBytes((modulus),256))) #RSA public key modulus  256
    input("")
    modulus = (rsaPubKey.public_numbers().e)               #exponent
    printD("EXP_RSA",bytearray(intToBytes((modulus),4)))   #RSA public key exponent  4
    input("")
    printD("RSA_RSA",bytearray(sig))                       #rsa signature           256
    input("")
    if(signVerifyHash(hash,sig,rsaPubKey)):
        printS("Valid Signature")
    else:
        printE("Invalid Signature")
    
    input("")
    sig2 = signHash(hash,rsaPrivKey)
    printD("RSA_SIG",bytearray(sig2)) 
    if(signVerifyHash(hash,sig2,rsaPubKey)):
        printS("Valid Signature")
    else:
        printE("Invalid Signature")
    input("")
    printI("Signature: If data OR Signature is altered on transit Signature validation fails...lets try it ")
    input("")
    printI("Note difference between valid and invalid signature below , byte 3 is now changed to" +Back.GREEN +"0x01"+Back.RESET)
    printD("VAL_SIG",bytearray(sig))
    if(signVerifyHash(hash,sig,rsaPubKey)):
        printS("Valid Signature")
    else:
        printE("Invalid Signature") 
    #lements of a bytes object cannot be changed , so change bytes to byte array and then back to bytes
    sigTmp = bytearray(sig)
    sigTmp[2] = 0x01
    sigTmp = bytes(sigTmp)
    printD("ERR_SIG",bytearray(sigTmp))
    input("")
    if(signVerifyHash(hash,sigTmp,rsaPubKey)):
        printS("Valid Signature")
    else:
        printE("Invalid Signature")
    input("")
def dhcryptoExample_1():
	# Variables Used
	sharedPrime = 23    # p
	sharedBase = 5      # g
	 
	aliceSecret = 6     # a
	bobSecret = 15      # b
	 
	# Begin
	print( "Publicly Shared Variables:")
	print( "Publicly Shared Prime: " + hex(sharedPrime ))
	print( "Publicly Shared Base:  " + hex(sharedBase ))
	 
	# Alice Sends Bob A = g^a mod p
	A = (sharedBase**aliceSecret) % sharedPrime
	print( "Alice Sends Over Public Chanel: " + hex( A ))
	 
	# Bob Sends Alice B = g^b mod p
	B = (sharedBase ** bobSecret) % sharedPrime
	print("Bob Sends Over Public Chanel: " + hex(B ))
	print( "------------" )
	print( "Privately Calculated Shared Secret:" )
	# Alice Computes Shared Secret: s = B^a mod p
	aliceSharedSecret = (B ** aliceSecret) % sharedPrime
	print( "Alice Shared Secret: " + hex(aliceSharedSecret ))
	 
	# Bob Computes Shared Secret: s = A^b mod p
	bobSharedSecret = (A**bobSecret) % sharedPrime
	print( "Bob Shared Secret: "  + hex( bobSharedSecret ))
def cryptoKeyexchange():
    dispDHInfo()
    dispKdfInfo()
    printI("lets see Simple DH example ...DH keyexcange is based on exponential complxity")
    input("")
    dhcryptoExample_1()
    input("")
    #person 1
    dh1 = getDhInit("DH2048")
    dh1PubKey = getDhGenPubKey("DH2048",dh1)
    printD("PUBK1",dh1PubKey)
    #person 2
    dh2 = getDhInit("DH2048")
    dh2PubKey = getDhGenPubKey("DH2048",dh2)
    printD("PUBK2",dh2PubKey)
    #share public key to each other and calculate shared secret
    dh1Sharedkey = getDhSharedKey("DH2048",dh1,dh2PubKey)
    dh2Sharedkey = getDhSharedKey("DH2048",dh2,dh1PubKey)
    printD("SECRET1",dh1Sharedkey)
    printD("SECRET2",dh2Sharedkey)
    if(dh1Sharedkey == dh2Sharedkey):
        printS ("DH Success")
    else:
        printE ("DH Fail")
    
    printGreen("ECDH key exachnge")
    printI("ECDH do not give forward secrecy ie if private key is compromised , shared key can be calculated. So always use ephemeral form ECDHE (or EECDH)")
    printI("ECDHE we generate new key pair every handshake")
    printI("Public key shared between two parties")
    server_private_key = getDhInit("SECP384R1")
    server_public_key  = getDhGenPubKey("SECP384R1",server_private_key)

    clint_private_key = getDhInit("SECP384R1")
    clint_public_key  = getDhGenPubKey("SECP384R1",clint_private_key)
    printD("ECCPUB1",server_public_key)
    printD("ECCPUB2",clint_public_key)
    input("")
    server_shared_key = getDhSharedKey("SECP384R1",server_private_key,clint_public_key) #shared secret calculated by Server
    clint_shared_key = getDhSharedKey("SECP384R1",clint_private_key,server_public_key) #shared secret calculated by Clint
    printI("Secret Generated by two paries")
    printD("ECCSEC1",server_shared_key)
    printD("ECCSEC2",clint_shared_key)
    input("")
    server_derived_key = deriveKey(server_shared_key) # Perform key derivation.
    clint_derived_key = deriveKey(clint_shared_key)  # Perform key derivation.
    printI("strong key is derived from secret, by both parties using key deivation function")
    printD("DKEY1",server_derived_key)
    printD("DKEY2",clint_derived_key)
    input("")
    # And now we can demonstrate that the handshake performed in the opposite direction gives the same final value

    if ((server_derived_key == clint_derived_key) and (server_shared_key == clint_shared_key)):
        printS("ECDH Key exchange Success")
    else:
        printE("ECDH Key derivation Fail")

printH("****** Welcome to Crypto example's  by Nandkumar *******")
#inputs we take can be string or raw data bytes , but we will cosider all data in as raw data bytes can be string or any other data format we will first converted
#everything to raw bytes and perform crypto operation

#pwtext ="123456"

login()
printH("CRYPTO INPUT")
text = "0123456789abcdefghi" # string input
byteArrayData = str2ByteArray(text)
printI("We will take below input string for all our crypto test. we will convert all string to byte array for crypto operations")
printD("TEXT",byteArrayData)
input("")
dispInfoPadding()
printI("Note extra bytes padded at end of the text , to make text size multiple of 16 bytes")
padText = padByteArray(byteArrayData,16)
printD("PadText",padText)
input("")
cryptoHash(byteArrayData)
#cryptoHashLenExtAtt(text)
cryptoSymatricEnc(padText)
cryptoSymatricEncAuth(padText)
cryptoSigning(padText)
cryptoKeyexchange()
#key darivation functio
#certificates
#mykeyexchange
#mySyencryption
#srp or PKAS
