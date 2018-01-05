import numpy as np
from finangler import FinAngler
from pid import PID
import time

class Stabilizer():
	def __init__(self):
		self.yaw_pid 	= PID(1,0,0)
		self.rp_pid		= PID(1,0,0)
		self.finagnler 	= FinAngler()
		self.set_sp(0,0)
		self.reset()

	def step(self, r, p, y):
		self.curr_time = time.time() - self.start_time
		dt = self.curr_time - self.prev_time

		angle, mag 	= self.rp_to_angle_mag(r,p)
		rp_command 	= rp_pid.step(mag, dt)
		yaw_command = yaw_pid.step(y, dt)

		fin_angles = self.finangler(angle, rp_command, yaw_command)

		self.prev_time = self.curr_time

	def rp_to_angle_mag(self, r, p):
		angle 	= np.atan2(r, p)
		mag  	= np.sqrt(r**2 + p**2)
		return angle, mag

	def set_sp(self, rp, yaw):
		self.setpoint_rp = rp
		self.setpoint_yaw = yaw

	def reset(sefl):
		self.yaw_pid.reset()
		self.rp_pid.reset()		
		self.start_time = time.time()
		self.prev_time 	= self.start_time
		self.curr_time  = self.start_time