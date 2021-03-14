import time
import sys
def DispPer(Per):# display persentage
    sys.stdout.write("\r%d%%" % i)
    sys.stdout.flush()

def DispPerBar(Heading,Per,max):# display persentage  
        tmp = Heading + ": "+"#"*(int((Per/max)*20)) +" [" +str(int((Per/max)*100)) +"%]"
        sys.stdout.write("\r"+tmp)
        sys.stdout.flush()
'''
for i in range(0,10):
    Display(i)
    time.sleep(0.1)
for i in range(0,900):
    DisplayBar("Downloading",i+1,900)
    time.sleep(0.01)
'''
    