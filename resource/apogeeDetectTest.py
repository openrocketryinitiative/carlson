import math
import numpy as np
import matplotlib.pyplot as plt
import sys

f = open(sys.argv[1])
data = []
for line in f.read().split('\n')[0:-1]:
	data.append(map(float, line.split(',\t')))

bdata = np.array(data)

start_time_index = np.argmin(np.abs(bdata[:,0] - 3.5))
stop_time_index = np.argmin(np.abs(bdata[:,0] - 8.))

# bdata = bdata[start_time_index:stop_time_index,:]

start = start_time_index
end = stop_time_index
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


snaps = np.abs(gyroX) + np.abs(gyroY)
angles = np.arcsin(np.cos(fuseX)*np.cos(fuseY))

snap_time = times[np.argmax(snaps)]
flip_time = times[np.argmin(np.abs(angles))]



# angles = []

# for index, time in enumerate(times):
# 	r = fuseX[index]
# 	p = fuseY[index]
# 	e = np.array([0,0,1]).T
# 	Rr = np.array([[1,         0,          0],
# 				   [0, np.cos(r), -np.sin(r)],
# 				   [0, np.sin(r), np.cos(r)]])

# 	Rp = np.array([[np.cos(p), 0, -np.sin(p)],
# 				   [0,         1,          0],
# 				   [np.sin(p), 0, np.cos(p)]])

# 	angles.append(np.arcsin(np.dot(np.matmul(Rp, np.matmul(Rr,e)), e)))

# angles = np.array([angles]).T


#plt.scatter(times, bdata[start:end, 1], label='state', s=6, c='purple', lw=0)   # state
plt.scatter(times, np.degrees(fuseX), label='fusionX', s=6, c=(1,.3,.3), lw=0)    # fusion X
plt.scatter(times, np.degrees(fuseY), label='fusionY', s=6, c=(.75,.3,.3), lw=0)  # fusion Y
plt.scatter(times, np.degrees(fuseZ), label='fusionZ', s=6, c=(.5,0,0), lw=0)   # fusion Z
plt.scatter(times, compassX, label='compassX', s=6, c=(.8,.5,1), lw=0)    # compass X
plt.scatter(times, compassY, label='compassY', s=6, c=(.8,.25,1), lw=0)  # compass Y
plt.scatter(times, compassZ, label='compassZ', s=6, c=(.8,.0,1), lw=0)   # compass Z
plt.scatter(times, accelX, label='accelX', s=6, c=(0,0,1), lw=0)    # gyro X
plt.scatter(times, accelY, label='accelY', s=6, c=(0,0,.75), lw=0)  # gyro Y
plt.scatter(times, accelZ, label='accelZ', s=6, c=(0,0,.5), lw=0)  # gyro Z
plt.scatter(times, np.degrees(gyroX), label='gyroX', s=6, c=(0,1,0), lw=0)   
plt.scatter(times, np.degrees(gyroY), label='gyroY', s=6, c=(0,.75,0), lw=0) 
plt.scatter(times, np.degrees(gyroZ), label='gyroZ', s=6, c=(0,.5,0), lw=0)  

# plt.scatter(times, snaps, label = 'abs(gyroX) + abs(gyroY)', s=6, c=(.8,.2,1), lw=0)
# plt.scatter(times, np.degrees(angles), label = 'cos(r)cos(p)', s=6, c=(0.2,1,0.5),lw=0)

plt.legend(loc=3)
# plt.axvline(snap_time, c=(.8,.2,1))
# plt.axvline(x=flip_time, c=(0.2,1,0.5))
plt.axvline(x=4.59)
plt.axvline(x=5.85)
plt.axvline(x=7.04)
# for i in range(5, 11):
# 	if i >= 8:
# 		c = 'b'
# 	else:
# 		c = 'r'
# 	plt.scatter(times, bdata[start:end, 5], label='%ith column' % i, s=6,c=c, lw=0)

# plt.legend()
plt.show()
