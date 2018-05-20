import time
import numpy as np
from finangler import FinAngler
from pid import PID
from servowriter_sync import ServoWriter

class Stabilizer(object):
    """PID controller for angling the rocket canards.
    """

    def __init__(self, yaw_k=(0,0,0), rp_k=(0,0,0)):
        self.yaw_pid      = PID(*yaw_k)
        self.rp_pid       = PID(*rp_k)
        self.finangler    = FinAngler()
        self.servo_writer = ServoWriter()
        self.set_sp(0,0)
        self.reset()
        self.servo_writer.start()

    def step(self, r, p, y):
        if self.recently_reset:
            self.yaw_mid = y
            self.recently_reset = False 
            return 
        self.curr_time = time.time() - self.start_time
        dt = self.curr_time - self.prev_time
        angle, mag  = self.rp_to_angle_mag(r, p)
        rp_command  = self.rp_pid.step(mag, dt)
        yaw_err = y - self.yaw_mid
        if yaw_err > np.pi: yaw_err -= 2*np.pi
        elif yaw_err < -np.pi: yaw_err += 2*np.pi
        yaw_command = self.yaw_pid.step(yaw_err, dt)
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

    def reset(self, yaw=0):
        self.recently_reset =True
        self.yaw_pid.reset()
        self.rp_pid.reset()
        self.start_time = time.time()
        self.prev_time  = self.start_time
        self.curr_time  = self.start_time


if __name__ == "__main__":
    from sensor import Sensor
    sensor = Sensor(configFile="../config/RTIMULib")
    sensor.start()  # start pulling data from IMU in a parallel thread
    stabilizer = Stabilizer()
    fusion_pose = None
    loop_frequency = 10  # Hz
    while sensor.imu_data is None:
        # wait for IMU data to start coming in
        time.sleep(0.5)
    while True:
        loop_start_time = time.time()
        data = sensor.imu_data
        fusion_pose = data["fusionPose"]
        print fusion_pose
        stabilizer.step(*fusion_pose)
        remaining_time = (1./loop_frequency) - (time.time()-loop_start_time)
        if remaining_time > 0:
            time.sleep(remaining_time)
