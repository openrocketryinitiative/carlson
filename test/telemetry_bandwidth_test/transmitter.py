"""
Test bandwidth of 915 MHz telemetry radios to explore streaming real-time data
from the rocket, in-flight.
"""

from sys import path
path.insert(0, "../../lib")

from telemetry import Telemetry
from time import sleep, time
from argparse import ArgumentParser

MESSAGE_RATE = 5   # default message interval in Hertz
N_MESSAGES   = 20  # default number of messages to send
MESSAGE_SIZE = 1   # default message size in bytes

if __name__ == "__main__":

    # parse args from command line
    parser = ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=N_MESSAGES, help="how many messages to send")
    parser.add_argument("-s", "--size", type=int, default=MESSAGE_SIZE, help="how big is each message in bytes")
    parser.add_argument("-r", "--rate", type=int, default=MESSAGE_RATE, help="message send rate in Hertz")
    args = parser.parse_args()

    # create and connect to telemetry radio
    transmitter = Telemetry()
    firstMessage = True
    estimatedTime = float(args.number) / float(args.rate)
    startWrite = 0
    totalWriteTime = 0

    print "sending {} messages at {} Hz".format(args.number, args.rate)
    print "estimated minimum total time (with message send time of 0): {} seconds".format(estimatedTime)
    print "receiver should receive {} bytes in total".format(args.number * args.size)
    startTime = time()
    for m in range(args.number):
        startWrite = time()
        transmitter.write("x" * args.size)
        totalWriteTime = time() - startWrite
        sleep(1.0 / float(args.rate))

    elapsedTime = time() - startTime
    print "sent all messages in {} seconds".format(elapsedTime)
    print "on average, it took around {} ms to send a {}-byte message".format(totalWriteTime/args.number*1000, args.size)
