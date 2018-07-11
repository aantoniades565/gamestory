import matplotlib.pyplot as plt
import numpy as np
import os
import math
y = np.load('energy_processed_d1.npy')
x = [(i+1) for i in range(len(y))]
plt.plot(x, y)
plt.axis([0, len(y)+1, 0, max(y)])

sorted_energy = sorted(y, reverse=True)
thres = sorted_energy[math.floor(0.001*len(y))]

horiz_line_data = np.array([thres for i in range(len(y))])
plt.plot(x, horiz_line_data, 'r--')

plt.show()
plt.savefig(os.path.basename("energy_d1") + '.svg')