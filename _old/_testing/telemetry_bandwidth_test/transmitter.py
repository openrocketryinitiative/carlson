"""
Test bandwidth of 915 MHz telemetry radios to explore streaming real-time data
from the rocket, in-flight.
"""

from sys import path
path.insert(0, "../../../lib")

from telemetry import Telemetry
from time import sleep, time

MESSAGE_SIZE = 1     # size of message in bytes
MESSAGE_RATE = 5    # message interval in Hertz
N_MESSAGES   = 20  # number of messages to send

if __name__ == "__main__":

    # Create and connect to telemetry radio.
    transmitter = Telemetry()

    print "Sending {} messages at {} Hz.".format(N_MESSAGES, MESSAGE_RATE)
    print "Estimated total time: {} seconds.".format(float(N_MESSAGES) / float(MESSAGE_RATE))
    startTime = time()
    for m in range(N_MESSAGES):
        transmitter.write("x" * MESSAGE_SIZE)
        sleep(1.0 / float(MESSAGE_RATE))

    print "Sent all messages in {} seconds.".format(time() - startTime)
