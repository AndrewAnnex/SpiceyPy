__author__ = 'Apollo117'

import SpiceyPy as spice
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#First make sure we don't stop if an error occurs
spice.erract("set", 10, "report")

# You must download the needed kernels, please read testMetaK.txt for links
spice.furnsh('./testMetaK.txt')

step = 10000
utc = ['Jun 20, 2004', 'Dec 1, 2005']

# get et values one and two, we could vectorize str2et
etone = spice.str2et(utc[0])
ettwo = spice.str2et(utc[1])

#get times
times = list(range(step))
times = [x*(ettwo-etone)/step + etone for x in times]

#check times:
print(times[0:3])

#Run spkpos as a vectorized function

positions, lighttimes = spice.spkpos('Cassini', times, 'J2000', 'NONE', 'SATURN BARYCENTER')

print("Positions: ")
print(positions[0:3])

print("Light Times: ")
print(lighttimes[0:3])

#Clean up
spice.kclear()

#Plot the resulting positions:
fig = plt.figure()
ax = fig.gca(projection='3d')
positions = np.array(positions)
ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], label="Cassini Position")
ax.legend()
plt.show()

