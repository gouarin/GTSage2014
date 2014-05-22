import numpy as np

def ball(n=100):
    v0 = 5.
    g = 9.81
    t = np.linspace(0., 2.*v0/g, n)
    return v0*t-0.5*g*t**2

if __name__ == "__main__":
    ball()

