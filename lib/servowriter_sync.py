from threading import Thread, Lock
import numpy as np
import os
import time

class ServoWriter(object):
    """Use ServoBlaster library to write PWM to servos on Raspberry Pi 3.

    ServoBlaster library can be found here:

        https://github.com/richardghirst/PiBits/tree/master/ServoBlaster

    :param int servo_writer_interval: Interval between servo motor writes, in milliseconds.
    """

    def __init__(self, servo_write_interval=0):
        os.system("sudo killall servod")  # kill any running servod processes
        self.angles                 = np.array([0, 0, 0])  # start vertical
        self.us                     = np.array([1500, 1500, 1500])
        self.one_over_pi            = 1. / np.pi
        self.servo_pins             = [11,13,15]
        os.system("sudo killall servod")
        print str(self.servo_pins)[1:-1]
        os.system("sudo servod --p1pins=\"{}\"".format(str(self.servo_pins)[1:-1]))

    def start(self):
        print '[servowriter_sync]: start() does nothing.'

    def write_to_servos(self):
        print '[servowriter_sync]: write_to_servos() does nothing.'

    def stop(self):
        """Stop servod process.
        """
        os.system("sudo killall servod")
        print("Stopped servod.")

    def push_new_angles(self, new_angles):
        """Push new angles to servod.

        :param list new_angles: New angles to write to servo motors
        """
        self.angles = new_angles
        self.us = np.clip(self.angles*self.one_over_pi*500.+1500,1000,2000)
        for motor, us in enumerate(self.us):
            os.system("echo {}={}us > /dev/servoblaster".format(motor, us))

    def read_angles(self):
        """Read angles array. 
        """
        return self.angles

