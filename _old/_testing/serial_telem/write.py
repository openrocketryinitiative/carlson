import serial, struct, time

from random import random

s = serial.Serial(port="/dev/ttyUSB0", baudrate=57600)
t = 0;

data_struct = "fff"
print "data_struct is %d bytes" % struct.calcsize(data_struct)

while (True):

    a, b, c = random()+t, random()+t, random()+t
    
    data = struct.pack(data_struct, a, b, c)

    nbytes = s.write(data)
    print "Wrote %d bytes (%.2f, %.2f, %.2f)." % (nbytes, a, b, c)

    time.sleep(1)
    t = t + 1;