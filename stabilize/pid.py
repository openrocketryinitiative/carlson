import numpy as np

class PID():
	def __init__(self, kp, ki, kd, control_range=None):
		self.kp = kp
		self.ki = ki
		self.kd = kd
		self.range = control_range
		self.reset()

	def step(self, err, dt):
		self._int_err += err * dt			# calculate derivative and integral of error
		d_err = (err - self._prev_err)/dt

		p = self.kp * err 					# calculate p, i, d components of control
		i = self.ki * self._int_err
		d = self.kd * d_err

		u = p + i + d 						# sum them
		if self.range is not None: u = min(max(u, self.range[0]), self.range[1]) # threshold output
		return u

	def reset(self):
		self._prev_err = 0
		self._int_err = 0
