import subprocess
import os
import time

os.system('sudo servod --p1pins="11,13,15"')
val = 1000
while True:
    val = 2000 if val == 1000 else 1000
    for i in range(3):
        print 'Setting servo {} to {}'.format(i,val)
        os.system("echo {}={}us > /dev/servoblaster".format(i,val))
    time.sleep(.1)
