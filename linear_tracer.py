import matplotlib.pyplot as plt
from random import random
import numpy as np
from time import time, time_ns

def random_betwen(min_value : float, max_value : float, decimals : int) -> float:
    return round(random() * (max_value - min_value) + min_value, decimals)

x1 = 0
x2 = 30
step = 0.5

y_max = 20
y_min = 0
decimals = 2
y1 = random_betwen(y_min, y_max, decimals)
y2 = random_betwen(y_min, y_max, decimals)

x = np.arange(x1, x2 + step, step)
print(x)

y = (x * (y2 - y1) + x2 * y1 - x1 * y2) / (-x1 + x2)

print(f"Ponto inicial: ({x1}, {y1})")
print(f"Ponto final:   ({x2}, {y2})")

plt.plot(x, y, '-go')
plt.plot(x1, y1,'ro')
plt.plot(x2, y2,'ro')
plt.show()