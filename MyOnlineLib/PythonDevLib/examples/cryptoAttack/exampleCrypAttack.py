'''
p, a, b, G, N (elliptic curve params)
Q = public key
e = hash of data
R, S = signature
private:
m = random
k = private key.
A signature is a pair of numbers R, S computed by the signer
R = (mG)...x axis point
S = (e + kR)/m
It is imperative to have a random m for every.signature: from a pair of signatures that use the same m, we can compute m and k
R = (mG)x , R = (mG)x
S1 =(e1 + kR) / m , S2 = (e2 + kR) / m
S1 - S2 =(e1 - e2 )/m
m = (e1 - e2)/(S1 - S2)
k =(mSi - ei)/R
k = = (e1S2 - e2S1) / R(S1 - S2)
'''