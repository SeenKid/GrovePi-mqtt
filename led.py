import time
from grovepi import *
 
# connection led à D3
led = 3
poten = 0
 
pinMode(led,"OUTPUT")
pinMode(poten, "INPUT")
time.sleep(0.1)
 
while True:
    try:
        # Lecture du Potentiometre
        var = analogRead(poten)

        # Envoie signal vers LED
        analogWrite(led, var//4)
        showup = (var//4)
        print(showup)
        
    except IOError:           
        print ("Error")