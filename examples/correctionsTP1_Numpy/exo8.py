import numpy as np

x = np.linspace(0, 1, 3)
# y = 2*x + 1
y = x.copy(); y *= 2; y += 1
print x, y 
np.savez("xytab.npz", x=x, y=y)
