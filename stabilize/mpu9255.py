from smbus import SMBus
import numpy as np

############################################## Definitions ############################################# 

# definitions of sensors adresses 
MAG_ADDRESS 	= 0x0C # magnetometer 
MPU_ADDRESS 	= 0x68	 # main chip adress

#control registers 
USER_CTRL  		= 0x6A
PWR_MGMT_2 		= 0x6B
INT_PIN_CFG 	= 0x37
ST1 			= 0x02
#ST2 			= 0x09
CNTL 			= 0x0A
ACCEL_CONFIG 	= 0x1C
GYRO_CONFIG 	= 0x1B
CONFIG 			= 0x1A
SMPLRT_DIV 		= 0x19
GYRO_CONFIG 	= 0x1B
ACCEL_CONFIG 	= 0x1C
INT_PIN_CFG 	= 0x37
INT_ENABLE 		= 0x38

# data registers 
MAG_XOUT_L 		= 0x03
GYRO_XOUT_H 	= 0x43 
ACCEL_XOUT_H 	= 0x3B

i2c = SMBus(1)
############################################## MPU9255 class ################################################

class MPU9255():
	def __init__(self):
		# self.ax=0
		# self.ay=0
		# self.az=0
		# self.gx=0
		# self.gy=0
		# self.gz=0
		# self.mx=0
		# self.my=0
		# self.mz=0
		self.init_mpu()

	def init_mpu(self):
		i2c.write_byte_data(MPU_ADDRESS,PWR_MGMT_2, 0b00000000) # enable gyro and acc 
		i2c.write_byte_data(MPU_ADDRESS,CONFIG, 0x03) # set DLPF_CFG to 11 
		i2c.write_byte_data(MPU_ADDRESS,SMPLRT_DIV, 0x04)# set prescaler sample rate to 4 
		c = i2c.read_byte_data(MPU_ADDRESS,GYRO_CONFIG) 

		print 'Init: got gyro config {}'.format(c)
		i2c.write_byte_data(MPU_ADDRESS,GYRO_CONFIG, c & ~0x02)# set second option from tavle 
		i2c.write_byte_data(MPU_ADDRESS,GYRO_CONFIG, c & ~0x18)# set scale to +- 250 dps
		c = i2c.read_byte_data(MPU_ADDRESS,ACCEL_CONFIG) 
		print 'Init: got accel config {}'.format(c)
		i2c.write_byte_data(MPU_ADDRESS,ACCEL_CONFIG, c & ~0x18) # set scale to +- 2G 
		
		i2c.write_byte_data(MPU_ADDRESS,INT_PIN_CFG, 0x22)# BYPASS ENABLE, LATCH_INT_EN 
		i2c.write_byte_data(MPU_ADDRESS,INT_ENABLE, 0x01) # RAW_RDY_EN 
		# magnetometer init procedure 
		i2c.write_byte_data(MAG_ADDRESS, CNTL, 0x00)
		i2c.write_byte_data(MAG_ADDRESS, CNTL, 0x16) 

	def set_acc_scale(self, value):
		# 1 = 2g
		# 2 = 4g
		# 3 = 8g
		# 4 = 16g
		self.set_scale(value, ACCEL_CONFIG)

	def set_gyro_scale(self, value):
		# 1 = 250 deg/sec
		# 2 = 500 deg/sec
		# 3 = 1000 deg/sec
		# 4 = 2000 deg/sec
		self.set_scale(value, GYRO_CONFIG)

	def set_scale(self, value, address):
		val=i2c.read_byte_data(MPU_ADDRESS,address)
		if value == 1:# +- 2g
			val &= ~((1<<3)|(1<<4))# set bit 3 and 4 to 0
		elif value == 2:# +- 4g
			val &= ~(1<<4)# set bit 4 to zero
			val |= (1<<3)# set bit 3 to 1 
		elif value == 3:# +- 8g
			val &= ~(1<<3)# set bit 3 to zero
			val |= (1<<4)# set bit 4 to 1 
		elif value == 4:# +- 16g
			val |= (1<<4)|(1<<3)# set bit 3 and 4 to 1
		else:
			print 'Value is {}'.format(val)
		i2c.write_byte_data(MPU_ADDRESS,address,val)# commit changes 

	def read_axes_data(self, address):
		i2c.write_byte(MPU_ADDRESS,address) 
		raw_data = np.zeros(6, dtype = int)
		for i in range(6):
		  raw_data[i] = i2c.read_byte(MPU_ADDRESS)
		#data processing
		ax = (raw_data[0] << 8) | raw_data[1]  
		ay = (raw_data[2] << 8) | raw_data[3] 
		az = (raw_data[4] << 8) | raw_data[5] 
		return np.array([ax, ay, az])

	def read_acc(self):
		return self.read_axes_data(ACCEL_XOUT_H)

	def read_gyro(self):
		return self.read_axes_data(GYRO_XOUT_H)


# void MPU9255::read_mag()
# {
#   uint8_t rawData[6] 
#   i2c.read_byte_data(MAG_ADDRESS, ST1)
# # get some data 
#   i2c.beginTransmission(MAG_ADDRESS) 
#   i2c.i2c.write_byte_data(MAG_XOUT_L) 
#   i2c.endTransmission(false) 
#   uint8_t i = 0
#   i2c.requestFrom(MAG_ADDRESS, 8) 
#   while (i2c.available()) {
#     rawData[i++] = i2c.i2c.read_byte_data()
#   } 
# # process data 
# mx=((int16_t)rawData[1] << 8) | rawData[0] 
# my=((int16_t)rawData[3] << 8) | rawData[2] 
# mz=((int16_t)rawData[5] << 8) | rawData[4] 
# }

if __name__ == '__main__':
	mpu = MPU9255()