import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-4., 4., 50)
plt.figure(1)
plt.subplot(221) 
plt.plot(x, -x**4+x**3+x**2+1, 'o-')
plt.title("$f$")
plt.subplot(222)
plt.plot(x, -4*x**3+3*x**2+2*x, '-')
plt.title("$f^{(1)}$")
plt.subplot(223)
plt.plot(x, -12*x**2+6*x+2, '--')
plt.title("$f^{(2)}$")
plt.subplot(224)
plt.plot(x, -24*x+6, ':')
plt.title("$f^{(3)}$")
plt.savefig("1D_subplot1.pdf")
plt.tight_layout()
plt.savefig("1D_subplot1.pdf")

x = np.linspace(-4., 4., 50)
fig=plt.figure(2)
plt.subplot(2, 2, 1)
plt.plot(x, -x**4+x**3+x**2+1, 'o-')
plt.title("$f$")
plt.subplot(2, 2, 3)
plt.plot(x, -4*x**3+3*x**2+2*x, '-')
plt.title("$f^{(1)}$")
plt.subplot(1, 2, 2)
plt.plot(x, -12*x**2+6*x+2, '--')
plt.title("$f^{(2)}$")
plt.axes([.7, .1, .1, .1])
plt.plot(x, -24*x+6, ':')
plt.title("$f^{(3)}$")
plt.tight_layout()
plt.savefig("1D_subplot2.pdf")
plt.show()
