import serial, struct

s = serial.Serial(port="/dev/ttyUSB0", baudrate=57600, timeout=6)

data_struct = "fff"
data_struct_size = struct.calcsize(data_struct)
print "data_struct is %d bytes" % data_struct_size

while (True):
    bytestream = s.read(data_struct_size)
    data = struct.unpack(data_struct, bytestream)
    print "received:", data