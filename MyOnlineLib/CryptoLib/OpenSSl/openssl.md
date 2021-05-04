# Creating Certs using openssl

## 1. Notes
- No use of underscore "_" in any names of certificate or certificate content, some server do not like it and faile varififcatin

## 2. Creating Root CA

### Create Root Key
```code
openssl ecparam -name prime256v1 -genkey -noout -out rootca/rootcaPrivateKey.pem
```
**Note:** Keep This key secret with root CA, this key is used by you to sign other cert

### create random number this is needed for openssl 
```code
openssl rand -writerand .rnd
```

### Create and self sign the Root Certificate
```code
openssl req -sha256 -new -x509 -key rootca/rootcaPrivateKey.pem -out rootca/rootcaCert.pem -days 10000 -subj "/C=IN/ST=GA/O=sauraurjaroot, Inc./CN=sauraurja.com"
```

## 3. Creating CSR (this is to be done by each device / server to get certified)
Create a certificate (procedere to be done for reach device/server)
This procedure needs to be followed for each server/device that needs a trusted certificate from our CA

### Create the private key of devicekey

```code
openssl ecparam -name prime256v1 -genkey -noout -out servername/servernamePrivateKey.pem
```
**Note** Keep This key secret with device, this key is used by bevice for mutual authentication with other devices

###  Create the signing (csr)

The certificate signing request is where you specify the details for the certificate you want to generate. This request will be processed by the owner of the Root key (you in this case since you create it earlier) to generate the certificate.
Important: Please mind that while creating the signign request is important to specify the Common Name providing the IP address or domain name for the service, otherwise the certificate cannot be verified.

This method generates the same output suitable for use in your automation .
```code
openssl req -new -sha256 -key servername/servernamePrivateKey.pem -subj "/C=IN/ST=GA/O=servername, Inc./CN=servername.com" -out servername/servernameCsr.pem
```
**Note** CN=servername.com suld be device IP address as its dynamic ip address so i.e **CN=192.168.1.2**

### Verify the csr's content
```code
openssl req -in servername/servername.csr -noout -text
```

## 4. CSR request proccesed by root CA and deliver signed certificate to device

THis is done by root CA after receving CSR request
### Generate the certificate using the device csr ( device publick key is incuded in csr file) along with the CA Root privatekey key.

```code
openssl x509 -req -in servername/servernameCsr.pem -CA rootca/rootcaCert.pem -CAkey rootca/rootcaPrivateKey.pem -CAcreateserial -out servername/servernameCert.pem -days 500 -sha256
```

### Verify the certificate's content

```code
openssl x509 -in servername/servernameCert.pem -text -noout
```

## 5. Cert Format nd Convertion
You may have seen digital certificate files with a variety of filename extensions, such as .crt, .cer, .pem, or .der. These extensions generally map to two major encoding schemes for X.509 certificates and keys: PEM (Base64 ASCII), and DER (binary). However, there is some overlap and other extensions are used, so you can’t always tell what kind of file you are working with just from looking at the filename; you may need to open it in a text editor and take a look for yourself.

### PEM
PEM (originally “Privacy Enhanced Mail”) is the most common format for X.509 certificates, CSRs, and cryptographic keys. A PEM file is a text file containing one or more items in Base64 ASCII encoding, each with plain-text headers and footers (e.g. -----BEGIN CERTIFICATE----- and -----END CERTIFICATE-----). A single PEM file could contain an end-entity certificate, a private key, or multiple certificates forming a complete chain of trust. Most certificate files downloaded from SSL.com will be in PEM format.

### DER
DER (Distinguished Encoding Rules) is a binary encoding for X.509 certificates and private keys. Unlike PEM, DER-encoded files do not contain plain text statements such as -----BEGIN CERTIFICATE-----. DER files are most commonly seen in Java contexts.

Note extention use are .pem for all types like cert,key and csr. but windoes understand cert by extention "cert .cer .crt" so rename cert file name xtention from.pem to .crt

### Convert PEM to DER Format
```code
openssl x509 -outform der -in servername/servernameCert.pem -out servername/servernameCert.der
```

### Convert DER to PEM Format
```code
openssl x509 -inform der -in servername/servernameCert.der -out servername/servernameCert.pem
```
## 6. Help on Commands
[link to Openssl Help!](https://gist.github.com/Soarez/9688998)

## 7. Other openssl command
TODO

