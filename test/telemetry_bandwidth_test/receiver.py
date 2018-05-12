"""
Test bandwidth of 915 MHz telemetry radios to explore streaming real-time data
from the rocket, in-flight.
"""

from sys import path, stdout
path.insert(0, "../../lib")

from telemetry import Telemetry
from time import time

if __name__ == "__main__":

    # Create and connect to telemetry radio.
    receiver = Telemetry(port="/dev/ttyUSB0", baud=57600)

    print "Waiting for messages to be sent."
    messagesRead = 0
    bytesRead    = 0
    while True:
        bytesAvailable = receiver.bytesAvailable()
        if bytesAvailable > 0:  # bytes are waiting to be read
            received = receiver.read(bytesAvailable)
            messagesRead += 1
            bytesRead    += bytesAvailable
            stdout.write("#{}:\t{} bytes [{} bytes total]\n".format(
                messagesRead, bytesAvailable, bytesRead))