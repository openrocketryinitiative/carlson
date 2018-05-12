import time
import numpy as np
from finangler import FinAngler
from pid import PID
from servowriter import ServoWriter

class Stabilizer(object):
    """PID controller for angling the rocket canards.
    """

    def __init__(self):
        self.yaw_pid      = PID(0,0,0)
        self.rp_pid       = PID(0.1,0,0)
        self.finangler    = FinAngler()
        self.servo_writer = ServoWriter()
        self.set_sp(0,0)
        self.reset()
        self.servo_writer.start()

    def step(self, r, p, y):
        self.curr_time = time.time() - self.start_time
        dt = self.curr_time - self.prev_time
        angle, mag  = self.rp_to_angle_mag(r, p)
        rp_command  = self.rp_pid.step(mag, dt)
        yaw_command = self.yaw_pid.step(y, dt)
        # print mag, rp_command
        fin_angles  = self.finangler.calc_angles(angle, rp_command, yaw_command)
        self.servo_writer.push_new_angles(fin_angles)
        self.prev_time = self.curr_time

    def rp_to_angle_mag(self, r, p):
        push_angle = np.arctan2(-np.sin(r), -np.sin(p))
        push_force = np.arccos(np.cos(r) * np.cos(p))
        return push_angle, push_force

    def set_sp(self, rp, yaw):
        self.setpoint_rp  = rp
        self.setpoint_yaw = yaw

    def reset(self):
        self.yaw_pid.reset()
        self.rp_pid.reset()     
        self.start_time = time.time()
        self.prev_time  = self.start_time
        self.curr_time  = self.start_time


if __name__ == "__main__":
    from sensor import Sensor
    sensor     = Sensor(configFile="../config/RTIMULib")
    stabilizer = Stabilizer()
    fusionPose = None
    while True:
        data = sensor.read_imu()
        if data is None and fusionPose is not None:
            stabilizer.step(*fusionPose)
        elif data is not None:
            fusionPose = data["fusionPose"]
            print fusionPose