import math
import numpy as np
import matplotlib.pyplot as plt
import sys

f = open(sys.argv[1])
data = []
for line in f.read().split('\n')[0:-1]:
	data.append(map(float, line.split(',\t')))

bdata = np.array(data)

start_time = 10
end_time = 20
start = np.argmin(np.abs(bdata[:,0] - start_time))
end = np.argmin(np.abs(bdata[:,0] - end_time))
start = 0
end = -1

times = bdata[start:end,0]
states = bdata[start:end,1]
fuseX = bdata[start:end,2]
fuseY = bdata[start:end,3]
fuseZ = bdata[start:end,4]
compassX = bdata[start:end,5]
compassY = bdata[start:end,6]
compassZ = bdata[start:end,7]
accelX = bdata[start:end,8]
accelY = bdata[start:end,9]
accelZ = bdata[start:end,10]
gyroX = bdata[start:end,11]
gyroY = bdata[start:end,12]
gyroZ = bdata[start:end,13]

angles_from_vertical = np.arccos(np.cos(fuseX)*np.cos(fuseY))

# Rx = np.array([
# 	[1,0,0],
# 	[0, np.cos(fuseX), -np.sin(fuseX)], 
# 	[0, np.sin(fuseX), np.cos(fuseX)]
# 	])
# Ry = np.array([
# 	[np.cos(fuseY),0,np.sin(fuseY)], 
# 	[0,1,0], 
# 	[-np.sin(fuseY),0,np.cos(fuseY)]
# 	])
# Rz = np.array([
# 	[np.cos(fuseZ), -np.sin(fuseZ), 0], 
# 	[np.sin(fuseZ), np.cos(fuseZ), 0],
# 	[0,0,1]
# 	])

# z_iden = np.array([0,0,1])
# R = np.matmul(np.matmul(Rx, Ry),Rz)
# R_on_z = np.matmul(R, z_iden)

# push1 = np.arctan2(R_on_z[1], R_on_z[0])
push1 = np.arctan2(np.sin(fuseY), np.sin(fuseX))
push_angle = -push1 

# plt.scatter(times, states, label='state', s=6, c='purple', lw=0)   # state
plt.scatter(times, np.degrees(fuseX), label='fusionX', s=6, c=(1,.3,.3), lw=0)    # fusion X
plt.scatter(times, np.degrees(fuseY), label='fusionY', s=6, c=(.75,.3,.3), lw=0)  # fusion Y
plt.scatter(times, np.degrees(fuseZ), label='fusionZ', s=6, c=(.5,0,0), lw=0)   # fusion Z
# plt.scatter(times, compassX, label='compassX', s=6, c=(.8,.5,1), lw=0)    # compass X
# plt.scatter(times, compassY, label='compassY', s=6, c=(.8,.25,1), lw=0)  # compass Y
# plt.scatter(times, compassZ, label='compassZ', s=6, c=(.8,.0,1), lw=0)   # compass Z
# plt.scatter(times, accelX*0.3454225352, label='accelX', s=6, c=(0,0,1), lw=0)    # gyro X
# plt.scatter(times, accelY*0.3454225352, label='accelY', s=6, c=(0,0,.75), lw=0)  # gyro Y
# plt.scatter(times, accelZ*0.3454225352, label='accelZ', s=6, c=(0,0,.5), lw=0)  # gyro Z
# plt.scatter(times, np.degrees(gyroX), label='gyroX', s=6, c=(0,1,0), lw=0)   
# plt.scatter(times, np.degrees(gyroY), label='gyroY', s=6, c=(0,.75,0), lw=0) 
# plt.scatter(times, np.degrees(gyroZ), label='gyroZ', s=6, c=(0,.5,0), lw=0)  
plt.scatter(times, np.degrees(push_angle), label = 'push_angle', s=6, c=(.8, .3, .8),lw=0)
plt.scatter(times, np.degrees(angles_from_vertical), label = 'cos(r)cos(p)', s=6, c=(0.2,1,0.5),lw=0)
plt.legend(loc=0)

# plt.legend()
plt.show()
