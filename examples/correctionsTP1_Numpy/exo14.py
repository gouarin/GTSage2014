import numpy as np

def f(x, n=0.5):
    y = np.empty(x.shape)
    c = 1. + 1./n
    y[x <= 0.5] = n/(n+1)*(0.5**c - (0.5 - x[x<=.5])**c)
    y[x > 0.5] = n/(n+1)*(0.5**c - (x[x>.5] - 0.5)**c)
    #y[x <= 0.5] = x
    #y[x > 0.5] = -x
    return y
    
if __name__ == '__main__':
    m = 101
    x = np.linspace(0, 1, m)
    print f(x, .5)
