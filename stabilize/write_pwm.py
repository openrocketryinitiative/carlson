#!/usr/bin/python

import subprocess
import os
import time
from argparse import ArgumentParser

parser = ArgumentParser(description="write PWM commands to all servos")
parser.add_argument("-p", "--pwm", type=int, help="PWM value to write to all servos")
parser.add_argument("-s", "--command", type=str, help="predefined servo position command, i.e. low, mid, high")
args = parser.parse_args()

os.system('sudo servod --p1pins="11,13,15"')

pwm = args.pwm

try:
    if args.command.lower() == "low":
        pwm = 1000
    elif args.command.lower() == "mid":
        pwm = 1500
    elif args.command.lower() == "high":
        pwm = 2000
except:
    pass

for i in range(3):
    print 'setting servo {} to {}'.format(i, pwm)
    os.system("echo {}={}us > /dev/servoblaster".format(i, pwm))
