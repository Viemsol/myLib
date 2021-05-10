
# Python 3 code to demonstrate
# SHA hash algorithms.
  
import hashlib
  
# initializing string
str = "test data"
  
# encoding GeeksforGeeks using encode()
# then sending to SHA256()
print (hashlib.algorithms_guaranteed)
result = hashlib.sha256(str.encode())
print(result.hexdigest())
result = hashlib.sha384(str.encode())
print(result.hexdigest())