from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [2, 3, 4, 7, 4, 5, 6, 5, 4, 3]

plt.plot(x, y, 'ro', label='original')
x_new = np.arange(1, 15, 0.1)
f = interp1d(x, y, fill_value='extrapolate', kind='cubic')

y_new = f(x_new)

plt.plot(x_new, y_new, '--', label='interpolation')
plt.legend()
plt.show()

