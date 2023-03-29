import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x, y, z, = [10, 20], [10, 20], [10, 20]



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x,y,z)

plt.show()