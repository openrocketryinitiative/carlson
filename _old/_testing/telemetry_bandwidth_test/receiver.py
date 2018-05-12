"""
Test bandwidth of 915 MHz telemetry radios to explore streaming real-time data
from the rocket, in-flight.
"""

from sys import path
path.insert("../../../lib/telemetry.py")

MESSAGE_SIZE = 1  # size of message in bytes

if __name__ == "__main__":

    # Create and connect to telemetry radio.
    receiver = Telemetry()

    bytesRead = 0
    while True:
        received = receiver.read()
        bytesRead += MESSAGE_SIZE
        print(x)