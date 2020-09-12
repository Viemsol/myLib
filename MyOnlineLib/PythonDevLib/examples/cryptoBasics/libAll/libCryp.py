from .libDisp import *
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import pyDH
import sys
import os
##############
#
##############
def dispInfoPadding():
    printI("Padding : Modern Hash function or Encryption Function process data in blocks of fixed size.Data which is fed to this function need to be padded OR these functions automatically pad the data to meed block size.")
##############
#Function take byte array as input and pad random or fixed bytes at end ,Padding.AES_blocksize
# 'Random', 'Space','Null' (pad with null bytes ,used for encryption),'ZeroLen' (pad with zero but last bytes is padlength)
# NOTE above mode dose not work and , function pad with pad length byte only
##############
def padByteArray(byteArray,padBlockSize):
    from cryptography.hazmat.primitives import padding
    padder = padding.PKCS7(padBlockSize*8).padder() #padded string input
    padded_data = padder.update(bytes((byteArray)))
    padded_data = padded_data + padder.finalize()
    return bytearray(padded_data)
##############
#Function unpad the data bytes pading bytes is equal to number of padding bytes
##############
def unpadByteArray(byteArray,padBlockSize):
    from cryptography.hazmat.primitives import padding
    unpadder = padding.PKCS7(padBlockSize*8).unpadder() #padded string input
    unpadded_data = unpadder.update(bytes((byteArray)))
    unpadded_data = unpadded_data + unpadder.finalize()
    return bytearray(unpadded_data)
##############
#Function Comutes CRC32 of byte array input
##############
def crc32ByteArray(byteArray):
        intcrc32 = binascii.crc32(byteArray) & 0xffffffff
        some_bytes = intcrc32.to_bytes(4, sys.byteorder)
        byteArray = bytearray((some_bytes))
        return byteArray
##############
#Function compute SHA , MD5 digest of byte array data
##############
def hashByteArray(byteArrayDat, hashType):
    digest=0
    if(hashType == "SHA1"):
        digest = hashes.Hash(hashes.SHA1(), backend=default_backend())
    elif(hashType == "SHA256"):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    elif(hashType == "SHA512"):
        digest = hashes.Hash(hashes.SHA3_512(), backend=default_backend())
    elif(hashType == "MD5"):
        digest = hashes.Hash(hashes.MD5(), backend=default_backend())
    else:# no match
        printE("HESH Type Not supported , Lib support only (SHA1 ,SHA256,SHA512,MD5)")
        return byteArrayDat
    digest.update(bytes(byteArrayDat))
    byteArrayDat = digest.finalize()
    return(bytearray(byteArrayDat))

##############
#Function gives random data array of length
##############
def getRand(length):
     return (bytearray(os.urandom(length)))

##############
#Function take byte array data input ,encrypt with AES /AES auth and output encrypted byte array
##############
def encDataSym(byteArrayData,Key,IV,encMode,enc):
    cipherHandle = 0
    if(encMode == 'AESECB'):
        cipherHandle = Cipher(algorithms.AES(Key), modes.ECB(), backend=default_backend()) # based on key size AES automaticaly switch it to 128 or 256
    elif(encMode == 'AESCBC'):
        cipherHandle = Cipher(algorithms.AES(Key), modes.CBC(IV), backend=default_backend())
    else:
        printE("Encryption Mode Not Supported")
        return byteArrayData
    if(enc):#encryption
        encryptor = cipherHandle.encryptor()
        outByteArray =  encryptor.update(byteArrayData)
        encryptor.finalize()
        return bytearray(outByteArray)
    else:#decryption
        decryptor = cipherHandle.decryptor()
        outByteArray =  decryptor.update(byteArrayData)
        decryptor.finalize()
        return bytearray(outByteArray)
        
##############
#Function generate encrption key securely for differant moddes
##############
def genKeySec(encMode,len):
    if(encMode == 'AESGCM'):
        key = AESGCM.generate_key(bit_length=len*8)
    elif(encMode == 'AESCCM'):
        key = AESCCM.generate_key(bit_length=len*8)
    elif(encMode == 'ChaCha20Poly1305'):
         key = ChaCha20Poly1305.generate_key()
    else:
        printE("Key not generated for this mode , random key value generated")
        key = getRand(len)
    return bytearray(key)

def encDataSymAuth(byteArrayData,Key,auth,nonce,encMode,enc):
    encHandle = 0
    if(encMode == 'AESGCM'):
        encHandle = AESGCM(bytes(Key))
    elif(encMode == 'ChaCha20Poly1305'):
        encHandle = ChaCha20Poly1305(Key)
    elif(encMode == 'AESCCM'):
        encHandle = AESCCM(Key)
    else:
        printE("Enc mode not supported")
        return byteArrayData
    if(enc):
        encdecByteArray = encHandle.encrypt(bytes(nonce), bytes(byteArrayData), bytes(auth))
        return  bytearray(encdecByteArray)
    else:
        try:
            encdecByteArray = encHandle.decrypt(bytes(nonce), bytes(byteArrayData), bytes(auth))
            printS("Authentication pass")
            return bytearray(encdecByteArray)
        except:
            printE("Authentication fail")
            return 0
def dispHashinfo():
    printI("Hashing takes big data and reduce it to small data. just to explain concept of hash ...lets say you and your friend saw a movie and you both do not remamber its name, so how you can convince each other that both of you have saw same movie? ... yes by explaining some of the seance but not all frame by frame..and if you both aggree on the that small amount of information ..you both can conclude you have seen same movie..thats what hash is..if you reduce big random data to samall ..acording to infomation thory you canot reroduce it back from small data , but that small data have inough information needed to prove that its the original dig data...Hash are irrivarsibal function and hashes can collied :)")
    printI("Digest do not give any info on input length,\nDigest are one way functions i.e. from digest input cannot be recovered\nOnly Attack on password digest is brout force OR rainbow table directory of digest")
    input("")
def dispSymCryptInfo():
    printGreen("Symmetric encryption")
    printI("Symmetric encryption is a way to encrypt or hide the contents of material where the sender and receiver both use the same secret key. Note that symmetric encryption is not sufficient for most applications because it only provides secrecy but not authenticity. That means an attacker can’t see the message but an attacker can create bogus messages and force the application to decrypt them. ie Suffers ...Malleability. Also it canot provide Non - repudiation")
    input("")
def dispSymCryptWithAuthInfo():
    printI("Only Symmetric Encryption is not enough as it alone do not provide Authentication, and suffers from melliabbility.it is strongly recommended to combine encryption with a message authentication code, such as HMAC and other method such as including CRC in the message.AESGCM, ChaCha20Poly1305, AESCCM mode is a type of block cipher mode that simultaneously encrypts the message as well as authenticating it.")
    input("")
def dispSerializationInfo():
    printH("Serialization")
    printI("Asymmetric private and public keys to bytes")
    printI("1) PEM keys are recognizable because they all begin with" + Back.GREEN + "-----BEGIN {format}-----" + Back.RESET +" and end with " + Back.GREEN + "-----END {format}-----" + Back.RESET)
    printI("A PEM block which starts with -----BEGIN CERTIFICATE----- is not a public or private key, it’s an X.509 Certificate. ")
    printI("2) DER is an ASN.1 encoding type. There are no encapsulation boundaries and the data is binary.")
    printI("3) OpenSSH Public Key The format used by OpenSSH to store public keys")
    printI("4) PKCS12  PKCS12 is a binary format described in RFC 7292. It can contain certificates, keys, and more. PKCS12 files commonly have a pfx or p12 file suffix.")
    input("")
def dispAsymInfo():
    printH("Asymmetric cryptography")
    printI("Asymmetric cryptography is a branch of cryptography where a secret key can be divided into two parts, a public key and a private key. The public key can be given to anyone, trusted or not, while the private key must be kept secret (just like the key in symmetric cryptography).")
    printI("Use of Public key is to encrypt data and send , only person having private key can decrypt it, other use of public key is to verify received data is coming from rigth person ")
    printI("private key is used by sender to encrypt data which need autencticty, private key is used to decrypt data send by other users (by encrypting it with public key")
    input("")
    printI("Asymmetric cryptography used for sharing Symatric keys ie (DHKey exchange,ECDH),Used for Signing and used for proving proof of identity ")
    printI("Using asymmetric cryptography, messages can be signed with a private key, and then anyone with the public key is able to verify that the message was created by someone possessing the corresponding private key. ")
    printI("Also note that Asymmetric cryptography is rearely use to encrypt data (as its 1000 times slower then Symatric encryption) , if its not so critical like bank trsection")
    printI("For signing any Message, Message digest is used for encryption and not entire message.Authenticity can be verified with Non repudiation.Non repudiation canot be achived with AES encryption with AUth (AES-GCM) only authntication can be achived.If data OR Signature is altered on transit Signature validation fails")
    printI("Some of the Asymmetric cryptography schemas are ELEGMAl DH (discrete logarithms coplex problem, i.e X^Y = Z , easy to calculate Z if you know X and Y but knowing Z and X its difficult to calculate Y ..(X and Z are public and Y is private) ),RSA (Complexity in finding prime fectors..ie P1*P2 = K .. P1 and P2 are prime numbers...  it is very fast to multiply two large prime numbersP1 nad p2 and get the result  K , but you have a number K which you know is the product of two primes, finding these two prime P1 and P2 numbers is very hard..ie..known methods need lasge computing power to do so), ECC (Eclleptic curve problem..operation over EC  P*K = Y  is  Y and P are public and K is private .. but finding K from P and Y is very difficult) ")
    printRed("Note: with enough time / high computational power(add cost) any crypto algorithm can be broken. computational power required to break any cryptosystem disicides stregnt or leven of security provided by crypto algorithm.ie. length of 256-bit ECC key povide same level of security as 3072-bit RSA key. ")
    input("")
def dispECCInfo():
    printGreen("ECC (Elliptic Curve Cryptography)")
    printI("Elliptic Curve Cryptography: Elliptic curves provide equivalent security at much smaller key sizes than other asymmetric cryptography systems such as RSA or DSA. For many operations elliptic curves are also significantly faster; elliptic curve diffie-hellman is faster than diffie-hellman.")
    printI("Curves with a size of less than 224 bits should not be used. You should strongly consider using curves of at least 224 bits")
    printI("Generally the NIST prime field (“P”) curves are significantly faster than the other types suggested by NIST at both signing and verifying with ECDSA.")
    printI("In ECC private key is just random number and public key is point on the Elliptic curve (x,y).Public key can be derived esily from private key by just multipying it with Base point on the curve. but reverse is very difficult.")
    printI("So if in ECC, random number generator do not have enough entropy , prdeiction of private key is easy")
    printRed("Note: NIST curves are not safe, check SafeCurves project  by Daniel J. Bernstein and Tanja Lange")
    input("")
def dispRsaInfo():
    printGreen("RSA (Rivest–Shamir–Adleman)")
    printI("RSA :Unlike symmetric cryptography, where the key is typically just a random series of bytes, RSA keys have a complex internal structure with specific mathematical properties.")
    input("")
def dispDHInfo():
    printH("DH Key Exchange")
    dispDhConceptInfo()
    dispDhWorkingInfo()
    printI("Diffie-Hellman (DH) groups determine the strength of the key used in the key exchange process. Higher group numbers are more secure, but require additional time to compute the key.DH Group 1: 768-bit group,DH Group 2: 1024-bit group ,DH Group 5: 1536-bit group,DH Group 14: 2048-bit group,DH Group 15: 3072-bit group,DH Group 19: 256-bit elliptic curve group,DH Group 20: 384-bit elliptic curve group Both peers in a VPN exchange must use the same DH group The nature of the Diffie-Hellman key exchange, however, makes it susceptible to man-in-the-middle (MITM) attacks, since it doesn't authenticate either party involved in the exchange. The MITM maneuver can also create a key pair and spoof messages between the two parties, who think they're both communicating with each other. This is why Diffie-Hellman is used in combination with an additional authentication method, generally digital signatures. 1976 DH key exchange,1978 RSA.DH method allow two people who never met befor ,share secret key and comunicate securly, it also provide forword secresey..think how it can be achived with RSA?.can forword secrecy can be achived with RSA?...What All DH dose is cmmunicate shared secret securly between stanger , it do not authenticate or varify who is the stranger is , whether person we are talking to is trusted one or not ...it is done by certs ..but DH make sure ..whatever conversation we are having with stanger is secure...simple Dh or ECDH  do not give forward secrecy ie if private key is compromised , shared key can be calculated. So always use ephemeral(key lasting for short duration) form ECDHE (or EECDH).ECDHE we generate new key pair every handshake")
    input("")
def dispDhConceptInfo():
    printGreen("DH Concept")
    printI("Ram want to communicate with Laxman sacurly. and do not want ravan in between to know what he is taking..both rama and laxmana do not have any key shared previously ....how thy will communicate ? Ram send 5 problem to Laxman and sy pick any one")
    printI("1) x=2^100 + 10^1567895 2) x= 2 * log(2345677^333567) y = 3456789! 3) x= 2 * 1000 y = 2+4 , 4) x=2^100 y=4567^10 5) x=4^234567 y=45^4567")
    printI("laxmana randomly pick one problem let say 3 , find x and y and olny tell rama its x= 2000 value openly")
    printI("As Rama have alredy pre calculated calculated all the solution  rama knows x=2000 is for problem 3 , now ram says value of Y will be our secret key")
    printI("Now Ravan in middle know X=2000 , but dont know for which problem value of x=2000 , assuming each prolem takes 10 min to calculate ravan need 50 min Or on an average 30 min as he need to solve all problems to know for which problem x =2000 , but laxmana need only 10 min ..so for 20 min moth can talk securly till Ravan knows the secert...")
    input("")
    printRed("Still proble is ...How Rama trust Laxmana?...ie the person sending X=2000 is sent by Laxmana and not by Ravana :) .. this problem is solved by Certificte and Third party CA..we will check in next sessions")
    input("")
def dispDhWorkingInfo():
    printI("How DH works ? 5*2*3 = (5*2)*3 = (5*3)*2 = (2*3)*5 = 30 , if we have 3 set of number thir multiplication can be done in 3 differant ways. in DH thre is one common number R shred with everyone and then two pariesselect one random number A and B, both finds R^A=X and R^B=Y, X and  Y  is shared openly between each other,.....knowing Y and R its difficult to guess B...same way its difficult to find A by knowing X and R....this pheno is called one way function..so A and B is alwys remain secret and only owner will know... now Z = X^A = Y^B, Z is shared secret. and man in middle knows three things X,Y,R but without knowing A and B he canot compute Z. also R^A and X^A might be very very big numbers so they are computed in modular arithmatic....ie evenn if actual value of X^A is very very big , but as its done in moduler arithmaic result is alwys finite number from 0 - (N -1) ")
    input("")
def dispDigitalSiginfo():
    printI("Signing and claiming ownership of data is a basic act in cyber space, especially to approve financial transactions, and verify critical instructions. All digital mony trasections relay on Digital signature")
    input("")
def dispKdfInfo():
    printH("Key Derivation Function")
    printI("In cryptography, a key derivation function (KDF) is a cryptographic hash function that derives one or more secret keys from a secret value such as a master key, a password, or a passphrase using a pseudorandom function.[1][2] KDFs can be used to stretch keys into longer keys or to obtain keys of a required format, such as converting a group element that is the result of a Diffie–Hellman key exchange into a symmetric key for use with AES. Keyed cryptographic hash functions are popular examples of pseudorandom functions used for key derivation.KDF key is basically a derived key from original key, so if derived key get compromised its dificult to get original key. KDF also can be used to stregnthen keys from some weak crypto algorithm.In Unix The password entered by the user is run through a key derivation function to create a hashed version of the new password, which is saved. Only the hashed version is stored; the entered password is not saved for security reasons.When the user logs on, the password entered by the user during the log on process is run through the same key derivation function and the resulting hashed version is compared with the saved version. If the hashes are identical, the entered password is considered to be correct, and the user is authenticated. In theory, it is possible for two different passwords to produce the same hash. However, cryptographic hash functions are designed in such a way that finding any password that produces the same hash is very difficult and practically infeasible, so if the produced hash matches the stored one, the user can be authenticated.KDF is also used in Multiparty key-agreement protocols,Key stretching and key strengthening.KDF are Memory intensive then other Hash function .. so broutforcing and making rainbow table or dictionary is costly.In cryptography, key stretching techniques are used to make a possibly weak key, typically a password or passphrase, more secure against a brute-force attack by increasing the resources (time and possibly space) it takes to test each possible key.PBKDF2HMAC,HKDF are some examples")
    input("")
def getPrivKey(asymMode):
    if(asymMode == 'SECP256R1'):
         key = ec.generate_private_key(ec.SECP256R1(), default_backend()) #replace SECP384R1 with SECP256R1 OR SECP521R1..OR other
    elif(asymMode == 'SECP384R1'):
         key = ec.generate_private_key(ec.SECP384R1(), default_backend())
    elif(asymMode == 'SECP521R1'):
         key = ec.generate_private_key(ec.SECP521R1(), default_backend())
    elif(asymMode == 'RSA2048'):
         key = rsa.generate_private_key(public_exponent=65537, key_size=2048,backend=default_backend())
    else:
        printE("Key not generated for this mode , random key value generated")
        key = getRand(32)
    return key

def getPublKey(privKey):
    return(privKey.public_key())
    
def serializePrivKey(privKey,password):
    serOut = ""
    if(password):
        serOut = privKey.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.BestAvailableEncryption(bytes(password,'utf-8' )))
    else:
        serOut = privKey.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption())
    return serOut

def serializePubKey(pubKey):
    return(pubKey.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo))

def signHash(byteArrayDataHash,privKey):
    signature = 0
    try:
        if(isinstance(privKey, EllipticCurvePrivateKey)):
            signature = privKey.sign(bytes(byteArrayDataHash),ec.ECDSA(utils.Prehashed(hashes.SHA256())))# in this mathod digest is used to sign and verify
            #signature = private_key.sign(data,ec.ECDSA(hashes.SHA256()))# in this mathod digest of data is calculated and then signed by function itself
        elif (isinstance(privKey, rsa.RSAPrivateKey)):
            signature = privKey.sign(bytes(byteArrayDataHash),padding.PKCS1v15(),utils.Prehashed(hashes.SHA256() ))
        else:
            printE("Signing Mode Not supported")
    except:
        printE("Signing Mode Not supported")
    return signature
   
def signData(byteArrayData,privKey):
    signature = 0
    try:
        if isinstance (privKey, EllipticCurvePrivateKey):
            digestMsg = hashByteArray(byteArrayData,'SHA256')
            signature = privKey.sign(bytes(digestMsg),ec.ECDSA(utils.Prehashed(hashes.SHA256())))# in this mathod digest is used to sign and verify
        elif (isinstance(privKey, rsa.RSAPrivateKey)):
            print("RSA")
            signature = privKey.sign(bytes(byteArrayData),padding.PKCS1v15(),hashes.SHA256())# in this mathod digest is computed by signigin function
        else:
            printE("Signing Mode Not supported")
    except:
        printE("Signing Mode Not supported")
    return signature

def signVerifyData(byteArrayData,signature,pubKey):
    if isinstance(pubKey, rsa.RSAPublicKey):
        pubKey.verify( signature, bytes(byteArrayData), padding.PKCS1v15(), hashes.SHA256() )
    elif isinstance(pubKey, EllipticCurvePublicKey):
        digestMsg = hashByteArray(byteArrayData,'SHA256')
        pubKey.verify(signature, bytes(digestMsg), ec.ECDSA(utils.Prehashed(hashes.SHA256())))
    else:
        printE("\nSignature Not supported!")
        return 0
    printS("Signature OK !")
    return 1
    try:
        if isinstance(pubKey, rsa.RSAPublicKey):
            pubKey.verify( signature, bytes(byteArrayData), padding.PKCS1v15(), hashes.SHA256() )
        elif isinstance(pubKey, EllipticCurvePublicKey):
            digestMsg = hashByteArray(byteArrayData,'SHA256')
            pubKey.verify(signature, bytes(digestMsg), ec.ECDSA(utils.Prehashed(hashes.SHA256())))
        else:
            printE("\nSignature Not supported!")
            return 0
        printS("Signature OK !")
        return 1
    except:
        printE("\nSignature Fail!")
        return 0

def signVerifyHash(digest,signature,pubKey):
    try:
        if(isinstance(pubKey, EllipticCurvePublicKey)):
            pubKey.verify(signature, bytes(byteArrayData), ec.ECDSA(utils.Prehashed(hashes.SHA256())))
        elif(isinstance(pubKey, rsa.RSAPublicKey)):
            pubKey.verify( signature, bytes(digest),padding.PKCS1v15(),utils.Prehashed(hashes.SHA256()))
        else:
            printE("Signature Not supported!")
            return 0
        printS("Signature OK !")
        return 1
    except:
        printE("Signature Fail!")
        return 0
def getDhInit(asymMode):
    if(asymMode == 'SECP256R1'):
        dhPera = ec.generate_private_key(ec.SECP256R1(), default_backend()) #replace SECP384R1 with SECP256R1 OR SECP521R1..OR other
    elif(asymMode == 'SECP384R1'):
        dhPera = ec.generate_private_key(ec.SECP384R1(), default_backend() )
    elif(asymMode == 'SECP521R1'):
        dhPera = ec.generate_private_key(ec.SECP521R1(), default_backend())
    elif(asymMode == 'DH2048'):
        dhPera = pyDH.DiffieHellman() #By default it uses the group 14 (2048 bit  prime number). To use another group (e.g., 15): d1 = pyDH.DiffieHellman(15) #or pyDH.DiffieHellman(group=15)
    else:
        printE("Unknown mode")
        dhPera = 0
    return dhPera

def getDhGenPubKey(asymMode,dhPrivKey):
    if (asymMode == 'SECP521R1') or (asymMode == 'SECP384R1') or (asymMode == 'SECP256R1'):
        pubKey = dhPrivKey.public_key() #send this key to peer
    elif (asymMode == 'DH2048'):
        pubKey = dhPrivKey.gen_public_key() #send this key to peer
    else:
        printE("Key not generated for this mode , random key value generated")
        pubKey = getRand(32)
    return pubKey

def getDhSharedKey(asymMode,dhPrivKey,peerPubKey): 
    if (asymMode == 'SECP521R1') or (asymMode == 'SECP384R1') or (asymMode == 'SECP256R1'):
        sharedKey = dhPrivKey.exchange(ec.ECDH(), peerPubKey) #send this key to peer
    elif (asymMode == 'DH2048'):
        sharedKey =  hexStrToBytes(dhPrivKey.gen_shared_key(peerPubKey)) # pyDh return shared key as string so convert it to bytes
    else:
        printE("Key not generated for this mode , random key value generated")
        sharedKey = getRand(32)
    return sharedKey
def deriveKey(key): #function increse the strength of the key , similare to hash
    derivedKey = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'handshake data', backend=default_backend()).derive(key) # Perform key derivation.
    return derivedKey
def cryptoKeyDarivation(): # not used
	printH("Key Derivation")
	#PBKDF2 (Password Based Key Derivation Function 2) is typically used for deriving a cryptographic key from a password.
	backend = default_backend()
	salt = os.urandom(16)
	kdf = PBKDF2HMAC( algorithm=hashes.SHA256(),length=32,salt=salt, iterations=100000, backend=backend)
	key = kdf.derive(b"my great password")
	# verify
	kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000, backend=backend)
	kdf.verify(b"my great password", key)

libtest = 0
if(libtest):
    printI("Pad Unpad Test")
    padTest = padByteArray(str2ByteArray("1234"),16)
    printD("PAD",padTest)
    unpadTest = unpadByteArray(padTest,16)
    printD("UNPAD",unpadTest)
    printI("Hash Test")
    hashTest = hashByteArray(padTest,'MD5') # its 20 byte long or its 160 bit size digest
    printD("MD5",hashTest)
    hashTest = hashByteArray(padTest,'SHA1') # its 20 byte long or its 160 bit size digest
    printD("SHA1",hashTest)
    hashTest = hashByteArray(padTest,'SHA256') # its 20 byte long or its 160 bit size digest
    printD("SHA256",hashTest)
    hashTest = hashByteArray(padTest,'SHA512') # its 20 byte long or its 160 bit size digest
    printD("SHA512",hashTest)
    printD("CRC32",crc32ByteArray(padTest))
    
    printI("Symatric Encryption Test")
    printD("PAD",padTest)
    key = getRand(16)
    iv = getRand(16)
    printD('KEY-ECB',key)
    printD('IV-ECB',iv)
    encData = encDataSym(padTest,key,iv,'AESECB',1)#padding of data is handled automatically by hash function
    printD('ENC-ECB',encData)
    decData = encDataSym(encData,key,iv,'AESECB',0)#padding of data is handled automatically by hash function
    printD('DEC-ECB',decData)
    
    printI("Symatric Encryption with Authentication Test")
    aesAuthKey = genKeySec('AESGCM',16)
    printD('KEY-GCM',aesAuthKey)
    nonce = getRand(12)
    printD('NONC-GCM',nonce)
    auth = getRand(12)
    printD('AUTH-GCM',auth)
    encDataAuth = encDataSymAuth(padTest,aesAuthKey,auth,nonce,'AESGCM',1)
    printD('ENC-GCM',encDataAuth)
    decDataAuth = encDataSymAuth(encDataAuth,aesAuthKey,auth,nonce,'AESGCM',0)
    printD('DEC-GCM',decDataAuth)
    input("")
    
    printI("ASymatric Encryption Test : ECC")
    printI("Key pair generation,Signature and Signature varification")
    input("")
    eccPrivKey = getPrivKey('SECP256R1')
    printD("ECC_PRK",bytearray(serializePrivKey(eccPrivKey,'1234'))) # private key stored encrypted
    eccPubKey = getPublKey(eccPrivKey)
    printD("ECC_PUK",bytearray(serializePubKey(eccPubKey))) # private key stored encrypted
    printI("Varifiying Signature")
    sig = signData(padTest,eccPrivKey)
    printD("ECC_SIG",bytearray(sig))
    if(signVerifyData(padTest,sig,eccPubKey)):
        printS("Valid Signature")
    else:
        printE("Invalid Signature")

    printI("ASymatric Encryption Test : RSA")
    rsaPrivKey = getPrivKey('RSA2048')
    printD("RSA_PRK",bytearray(serializePrivKey(rsaPrivKey,'1234'))) # private key stored encrypted
    rsaPubKey = getPublKey(rsaPrivKey)
    printD("RSA_PUK",bytearray(serializePubKey(rsaPubKey))) # private key stored encrypted
    
    sig = signData(padTest,rsaPrivKey)
    printD("RSA_SIG",bytearray(sig))
    
    printI("Varifiying Signature with message") 
    if(signVerifyData(padTest,sig,rsaPubKey)):
        printS("Valid Signature")
    else:
        printE("Invalid Signature")
        
    printI("Varifiying Signature with hash")
    hash = hashByteArray(padTest,'SHA256')
    printD("SHA256",bytearray(hash))                       #hash digest SHA256      32
    modulus = (rsaPubKey.public_numbers().n)               #modulus
    printD("RSA_MOD",bytearray(intToBytes((modulus),256))) #RSA public key modulus  256
    modulus = (rsaPubKey.public_numbers().e)               #exponent
    printD("RSA_EXP",bytearray(intToBytes((modulus),4)))   #RSA public key exponent  4
    printD("RSA_SIG",bytearray(sig))                       #rsa signature           256
    if(signVerifyHash(hash,sig,rsaPubKey)):
        printS("Valid Signature")
    else:
        printE("Invalid Signature")
    
    sig2 = signHash(hash,rsaPrivKey)
    printD("RSA_SIG",bytearray(sig2)) 
    if(signVerifyHash(hash,sig2,rsaPubKey)):
        printS("Valid Signature")
    else:
        printE("Invalid Signature")
    