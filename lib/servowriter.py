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
        self.angles                 = [0, 0, 0]  # start vertical
        self.thread                 = Thread(target=self.write_to_servos)
        self.thread.daemon          = True
        self.thread_lock            = Lock()
        self.thread_running         = True
        self.servo_write_interval   = servo_write_interval  # (ms) how often to write to servo?
        self.one_over_pi            = 1 / np.pi
        self.servo_write_order      = [2,1,0]  # write servo motors in this order

    def start(self):
        """Start servod (ServoBlaster daemon) on certain pins, and start the 
        servo writer thread.
        """
        os.system('sudo servod --p1pins="11,13,15"')
        self.thread.start()
        print("Started servo writer thread.")

    def stop(self):
        """Stop servo writer thread.
        """
        self.thread_running = False
        os.system("sudo killall servod")
        print("Stopped servo writer thread.")

    def push_new_angles(self, new_angles):
        """Push new angles to the servo writer. Thread safe.

        :param list new_angles: New angles to write to servo motors, when ready.
        """
        self.thread_lock.acquire()
        self.angles = new_angles
        self.thread_lock.release()

    def read_angles(self):
        """Read angles array. Thread safe.
        """
        self.thread_lock.acquire()
        output_angles = self.angles
        self.thread_lock.release()
        return output_angles

    def radians_to_us(self, theta):
        """Convert theta (radians) to a microsecond pulse width to move the 
        servo motors correctly.

        :param float theta: Angle in radians.
        """
        us = theta*self.one_over_pi*500 + 1500
        return max(1000, min(2000, us))

    def write_to_servos(self):
        """Thread function.
        """
        while self.thread_running:
            angles = self.read_angles()
            for motor in self.servo_write_order:
                angle = angles[motor]
                os.system("echo {}={}us > /dev/servoblaster".format(
                    motor, self.radians_to_us(angle)))
            time.sleep(self.servo_write_interval * 0.001)
