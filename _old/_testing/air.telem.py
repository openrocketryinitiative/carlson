# Carlson v2
#
# This code reads the 10-DOF sensor values every 1/sample_rate seconds and
# saves them to disk. It also packs them into a C-type struct and sends them
# over telemetry to the base station (albeit at a lower data rate).
#
# Benjamin Shanahan, Elias Berkowitz, Isaiah Brand

# import sys, getopt
# sys.path.append(".")

import config

# Import sensor libraries
import RTIMU
from BMP280 import BMP280

import serial, struct, time, math, sys, os

# Configure serial port where telemetry radio is connected to Carlson
telem = serial.Serial(port=config.port, baudrate=config.baud, timeout=config.serial_timeout)
print "Initialized telemetry on port %s at baud %d." % (config.port, config.baud)

# Stores last unique command received by rocket
current_command = ""

# Send heartbeats to ground station
while (True):
    telem.write(config.HEARTBEAT)
    command = telem.read(1)
    if command == config.ARM:
        print "ARMED"
        telem.write(command)  # respond to ground station
        break;  # go into armed state
    time.sleep(config.heartbeat_delay)

# Past here, rocket is armed

while (True):

    # Read incoming command over telemetry
    command = telem.read(1)
    if command != "" and command != current_command:
        current_command = command
        if command == config.DEPLOY:
            print "DEPLOYED CHUTE"
        elif command == config.STOP:
            print "STOPPED DATA LOGGING"
        elif command == config.ARM:
            print "ROCKET ALREADY ARMED"
        else:
            print "UNRECOGNIZED COMMAND"
        # Respond to ground station
        telem.write(command)