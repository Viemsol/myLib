import requests as req
import time

url1 = 'https://192.168.1.10:5000/Command'
pwmSetMin = {'piCmd': 'pwmSet 13 25 50'}
url2 = 'https://192.168.1.10:5000/Command'
pwmSetMax = {'piCmd': 'pwmSet 13 100 50'}
# below is servo cycle test over https, plastic servo last for ~ 100 hes and metal gear ~150hrs Operation
count =0
while True:
    try:
        x = req.post(url1,verify=False,timeout=5,json=pwmSetMin) # no cert validation, 5 sec timeout
        print(x)
        #.content gives you access to the raw bytes of the response payload
        print(x.content)
        #responce into a string using a character encoding such as UTF-8.
        print(x.text)
        #The response headers can give you useful information, such as the content type of the response payload and a time limit on how long to cache the response.
        print(x.headers)
        time.sleep(5)
        x = req.post(url2,verify=False,timeout=5,json=pwmSetMax) # no cert validation, 5 sec timeout
        time.sleep(5)
    except Timeout:
        print('The request timed out')
    count =count +1
    print("Cycle: {}".format(count))
