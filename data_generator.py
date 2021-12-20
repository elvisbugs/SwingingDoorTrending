import matplotlib.pyplot as plt
import numpy as np
from swinging_door import SwingingDoor

qty_data = 30
deviation = 2

a = np.random.uniform(0, 100, qty_data)
#b = np.random.uniform(10, 20, qty_data)
#c = np.random.uniform(0, 3, qty_data)

#y = np.concatenate((a,b))
#y = np.concatenate((y,c))

y = a

t = np.arange(stop=len(y),step=1)

sd = SwingingDoor((t[0], y[0]), deviation)

plt.plot(t, y, '-o', color='black')
plt.plot(t[0], sd._superior_dev, 'ro')
plt.plot(t[0], sd._inferior_dev, 'go')

for x, y_c in enumerate(y):
    print(x, y_c)
    sd.check_door((x, y_c))

print(f"{sd.compressed_data=}")

#door_status = sd.check_door()

#plt.plot(t[-1], sd.)
#plt.plot(t[-1], sd._inferior_dev, '')
plt.show()