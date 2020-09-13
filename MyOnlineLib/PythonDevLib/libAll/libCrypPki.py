from libDisp import *
from libCryp import *
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime
from OpenSSL import crypto
from cryptography.hazmat.primitives.serialization import load_pem_private_key
def printPkiInfo():
    printH("Digital Certificates  or public key infrastructure (PKI) ")
    printI("PKI: hardware, software and procedures needed to create, manage, distribute, use, store and revoke digital certificates and manage public-key encryption. X.509 certificates are commonly used in protocols like TLS. X.509v3 is defined in RFC 5280 (which obsoletes RFC 2459 and RFC 3280).X.509 certificates are used to authenticate clients and servers....In short Certificate Management is All About the Trust!!!")
    printI("------->X.509 certificate encoding formats and extensions 1) base64 (ASCII) Binary format")
    printI("1) base64 (ASCII) encoding :  Privacy-Enhanced Mail (PEM) format(*.pem, *.crt, *.ca-bundle) PKCS#7( *.cer, *.p7b, *.p7s.) 2) Binary format : DER Format(.der , .cer) , PKCS#12 (.pfx ,.p12)")
    printI("(file with —–BEGIN PKCS7—- line on top means that it’s a PKCS7 security certificate file) and (—–BEGIN CERTIFICATE—- header starts a PEM encoded certificate)")
    input("")

def printCsrInfo():
    printI("------>Certificate Signing Request (CSR)")
    printI("1)You generate a private/public key pair.2)You create a request for a certificate, which is signed by your key (to prove that you own that key)called CSR .3)You give your CSR to a CA (but not the private key).4)The CA validates that you own the resource (e.g. domain) you want a certificate for.5)The CA gives you a certificate, signed by them, which identifies your public key, and the resource you are authenticated for.6)You configure your server to use that certificate, combined with your private key, to server traffic.")
    input("")
def dispSelfSigendCertinfo():
    printH("Creating a self-signed certificate")
    printI("Self-signed certificates are not issued by a certificate authority, but instead they are signed by the private key corresponding to the public key they embed.This means that other people don’t trust these certificates, but it also means they can be issued very easily. In general the only use case for a self-signed certificate is local testing, where you don’t need anyone else to trust your certificate.If CA private key get compromised and key is in handof attacker , attaker can sign and give cetificate to anyone and those certificte will be trusted by all global cerver...thats why if such thing happen we have revocation cert list and root  CA come online for very short duration to approve CSR to minimize chance of attack ")
    input("")
#####################
# # function generate CSR to be sent to CA for signing
# # if privKey == 0 it will be genrated
# # passkey , priv key is encrypted with passkey, no encryption if passkey =0
# # sigTyp, "SECP256R1, RSA2048, SECP384R1,   SECP521R1, RSA2048"
######################

def generateCSR(privKey,passkey,sigTyp,orgName,comName,extention,filepri):
    if(privKey == 0):
        printI("Generating private key...")
        privKey = getPrivKey(sigTyp)
    printI("writing private key to file...")
    with open(filepri +"_key.pem", "wb") as f:
        if(passkey):
            f.write(privKey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(bytes(passkey))))
        else:
            f.write(privKey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()))
    printI("Generating cert...")
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        # Provide various details about who we are.
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"IN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Goa"),
        #x509.NameAttribute(NameOID.LOCALITY_NAME, u""),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, orgName),
        x509.NameAttribute(NameOID.COMMON_NAME, comName),
    ])).add_extension(
        x509.SubjectAlternativeName([
            # Describe what sites we want this certificate for.
            x509.DNSName(orgName),
            x509.DNSName(extention),
    ]),
        critical=False,
    # Sign the CSR with our private key.
    ).sign(privKey, hashes.SHA256(), default_backend())
    # Write our CSR out to disk.
    printI("Writing cert to file...This CSR can be sent to CA or can be Self signed. Private key file key.pem to be kept secret with client")
    with open(filepri + "_csr.pem", "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))
    #print(privKey.private_numbers().private_value)
    #tmpkey = privKey.private_numbers().private_value
    #print(type(tmpkey))
    #print()
    #printD('HASH',hashByteArray(bytearray(tmpkey.to_bytes(32, byteorder='big')),'SHA1'))
    #printD('HASH',hashByteArray(bytearray(tmpkey.to_bytes(32, byteorder='big')),'SHA256'))

#####################
# function get private key stored in file , if file is not password protected pass passkey value 0
#
#####################
def getPrivkeyfromFile(fileLocation,passkey):
    pem_data = 0
    with open(fileLocation, mode='rb') as public_file:
        pem_data = public_file.read()
    if(passkey):
        return(load_pem_private_key(pem_data, password=passkey, backend=default_backend()))
    else:
        return(load_pem_private_key(pem_data,password=None, backend=default_backend()))
#####################
# read csr object from csr file
#
#####################
def getCsrfromFile(fileLocation):
    pem_data = 0
    with open(fileLocation, mode='rb') as public_file:
        pem_data = public_file.read()
    csr = x509.load_pem_x509_csr(pem_data, default_backend())
    return csr

#####################
# reads public key from certtificate
#
#####################
def getPubKeyfromCert(fileLocation):
    pem_data = 0
    cert = getCertObjfromCert(fileLocation)
    return(cert.public_key())

#####################
# ???
#
#####################
def getFigurprintCert(fileLocation,hashType):
    cert = getCertObjfromCert(fileLocation)
    if(hashType == "SHA256"):
        return(cert.fingerprint(hashes.SHA256()))
    else:
        printI("SHA not supported")
        return(0)

#####################
# get cert object from cert file
#
#####################
def getCertObjfromCert(fileLocation):
    pem_data = 0
    with open(fileLocation, mode='rb') as public_file:
        pem_data = public_file.read() 
    return( x509.load_pem_x509_certificate(pem_data, backend=default_backend()))    

#####################
# get SNerial number from cert file
#
#####################
def getSnfromCert(fileLocation):
    pem_data = 0
    cert = getCertObjfromCert(fileLocation)
    return(cert.serial_number)

#####################
# get key type 
#
#####################
def getKeyType(key):
    if(isinstance(key, rsa.RSAPublicKey)):
        return("RSA")
        
#####################
# return hash function used in certificate
#
#####################
def getCertHashTyp(fileLocation):
    with open(fileLocation, mode='rb') as public_file:
        pem_data = public_file.read()
    if(isinstance(pem_data.signature_hash_algorithm, hashes.SHA256)):
        return('SHA256')

#####################
# generate self signed cert
#
#####################
def generateSelfSigned(privateKey,orgName,comName,extention,validity_days):
     # subject and issuer are always the same.
    subject = issuer = x509.Name([
     x509.NameAttribute(NameOID.COUNTRY_NAME, u"IN"),
     x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Goa"),
     x509.NameAttribute(NameOID.ORGANIZATION_NAME, orgName),
     x509.NameAttribute(NameOID.COMMON_NAME, comName),
    ])
    
    cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(privateKey.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.datetime.utcnow()
    ).not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=validity_days)# Our certificate will be valid for 10 days
    ).add_extension(x509.SubjectAlternativeName([x509.DNSName(extention)]),critical=False
    ).sign(privateKey, hashes.SHA256(), default_backend())                              # Sign our certificate with our private key
    
    with open("ca_cert.pem", "wb") as f:                            # Write our certificate out to disk.
        f.write(cert.public_bytes(serialization.Encoding.PEM))

############
# this is how CA signes the csr sent by user
# in short csr get converted into certificate
############

def sign_csr(user_csr_file,ca_private_key_file, passKey,ca_cert_file, validity_days, filePrefix):
    # get ca keys
    caPrivKey = getPrivkeyfromFile(ca_private_key_file,passKey)
    caCert = getCertObjfromCert(ca_cert_file)
    #read user csr
    user_csr = getCsrfromFile(user_csr_file)
    
    valid_from = datetime.datetime.utcnow()
    valid_until = valid_from + datetime.timedelta(days=validity_days)

    builder = (
        x509.CertificateBuilder()
        .subject_name(user_csr.subject)
        .issuer_name(caCert.subject)
        .public_key(user_csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(valid_from)
        .not_valid_after(valid_until)
    )

    for extension in user_csr.extensions:
        builder = builder.add_extension(extension.value, extension.critical)

    cert = builder.sign(
        private_key=caPrivKey,
        algorithm=hashes.SHA256(),
        backend=default_backend(),
    )
    if(isinstance(cert, x509.Certificate)):
        printI("certificate varified")
    with open(filePrefix + "_cert.pem", "wb") as keyfile:
        keyfile.write(cert.public_bytes(serialization.Encoding.PEM))
#####################
#Display certificate info
#
#####################
def dipCertInfo(fileLocation,disAllFormat=0):
    cert = getCertObjfromCert(fileLocation)
    spacLen = 15
    print("\nIssuer")
    printTagValAligned("Common Name", cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value,spacLen)
    printTagValAligned("Country",cert.issuer.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value,spacLen)
    printTagValAligned("State", cert.issuer.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value,spacLen)
    print("\nIssued to Subject")
    printTagValAligned("Common Name", cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value,spacLen)
    printTagValAligned("Country",cert.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value,spacLen)
    printTagValAligned("State", cert.subject.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value,spacLen)

    printTagValAligned("serial_number", str(cert.serial_number),spacLen)
    printTagValAligned("Hash Algo", cert.signature_hash_algorithm.name,spacLen)
    printTagValAligned("SIGnature Algo",cert.signature_algorithm_oid._name,spacLen)
    printTagValAligned("not_valid_before (DD/MM/YYYY)",   str(cert.not_valid_before.day) +"/"+ str(cert.not_valid_before.month)+"/"+ str(cert.not_valid_before.year),spacLen)
    printTagValAligned("not_valid_after  (DD/MM/YYYY)"  ,str(cert.not_valid_after.day) +"/"+ str(cert.not_valid_after.month)+"/"+ str(cert.not_valid_after.year),spacLen)
    printTagValAligned("Cert version" , str(cert.version),spacLen)
    printTagValAligned("PUB_KEY",bytesToAscii(cert.public_key().public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)),spacLen)
    #printD("CERT",(cert.tbs_certificate_bytes))
    printTagValAligned("SIG",bytesToHex(cert.signature),spacLen)
    #printD("EXT",cert.extensions)

#####################
#function varifies if certificate is trusteed by ca cert or not , chain of trust is not yet implemented , so need to validate one after other
#
#####################
def validateCert(certToValidate,inter,caCertFile):
    cert_to_check = getCertObjfromCert(certToValidate)
    user_pubkey =  getPubKeyfromCert(certToValidate)
    
    ca_cert = getCertObjfromCert(caCertFile)
    issuer_public_key = getPubKeyfromCert(caCertFile)
    
    if(signVerifyData(cert_to_check.tbs_certificate_bytes,cert_to_check.signature,issuer_public_key)): # RSA cert generation donot support PSS padding if need to use pss need to chnge it wile generating SIG and while verifying also we need to use PSS , currently PKCS1v15 is used as pedding
        printS("Sig Valid")
    else:
        printE("Sig Not Valid 1")

    #hash = getFigurprintCert(certToValidate,'SHA256')
    #printD("Hash1",bytearray(hash))
    #hash = hashByteArray(cert_to_check.tbs_certificate_bytes,'SHA256')
    #print (user_pubkey.public_numbers().e) #public exponent
    #print (user_pubkey.public_numbers().n) # public modulus
    #print ((user_pubkey.public_numbers())) # exponent and modulus together forms rsa public key
    #printD("Usig",bytearray(cert_to_check.signature))

libtest = 0
if(libtest):
    printPkiInfo()
    input("")
    printCsrInfo()
    input("")
    dispSelfSigendCertinfo()
    input("")
    sigtyp = "SECP256R1" # RSA2048 ,SECP256R1
    #lets generate dummy CA first  (cerificate authority which will signe other certificate)
    generateCSR(0,0,sigtyp,"CACompony","CAcompony.com","CAcomponyextention.com",'ca' )  # generate two files now privatekey and csr reuquest file
    caPrivKey = getPrivkeyfromFile("ca_key.pem",0)
    generateSelfSigned(caPrivKey,"TestCompony","testcompony.com","testcomponyextention.com",360)  # tis will be CA certificate
    
    generateCSR(0,0,sigtyp,"USERCompony","USERcompony.com","USERcomponyextention.com",'user') # user csr
    sign_csr("user_csr.pem","ca_key.pem",0,"ca_cert.pem",360,'user')
    validateCert("user_cert.pem",0,"ca_cert.pem")
    dipCertInfo("user_cert.pem")
