import math
import numpy as np
import matplotlib.pyplot as plt
import sys

f = open(sys.argv[1])
data = []
for line in f.read().split('\n')[0:-1]:
	data.append(map(float, line.split(',\t')))

bdata = np.array(data)
start = 0
end = len(data)
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

#plt.scatter(times, bdata[start:end, 1], label='state', s=6, c='purple', lw=0)   # state
#plt.scatter(times, np.degrees(bdata[start:end, 2]), label='fusionX', s=6, c=(1,0,0), lw=0)    # fusion X
#plt.scatter(times, np.degrees(bdata[start:end, 3]), label='fusionY', s=6, c=(.75,0,0), lw=0)  # fusion Y
#plt.scatter(times, np.degrees(bdata[start:end, 4]), label='fusionZ', s=6, c=(.5,0,0), lw=0)   # fusion Z
#  plt.scatter(times, bdata[start:end, 5], label='compassX', s=6, c=(0,1,0), lw=0)    # compass X
# plt.scatter(times, bdata[start:end, 6], label='compassY', s=6, c=(0,.75,0), lw=0)  # compass Y
# plt.scatter(times, bdata[start:end, 7], label='compassZ', s=6, c=(0,.5,0), lw=0)   # compass Z
plt.scatter(times, bdata[start:end, 8], label='accelX', s=6, c=(0,0,1), lw=0)    # gyro X
plt.scatter(times, bdata[start:end, 9], label='accelY', s=6, c=(0,0,.75), lw=0)  # gyro Y
plt.scatter(times, bdata[start:end, 10], label='accelZ', s=6, c=(0,0,.5), lw=0)  # gyro Z

plt.scatter(times, bdata[start:end, 5], label='gyroX', s=6, c=(0,1,0), lw=0)   
plt.scatter(times, bdata[start:end, 6], label='gyroY', s=6, c=(0,.75,0), lw=0) 
plt.scatter(times, bdata[start:end, 7], label='gyroZ', s=6, c=(0,.5,0), lw=0)  
plt.legend()

# for i in range(5, 11):
# 	if i >= 8:
# 		c = 'b'
# 	else:
# 		c = 'r'
# 	plt.scatter(times, bdata[start:end, 5], label='%ith column' % i, s=6,c=c, lw=0)

# plt.legend()
plt.show()
