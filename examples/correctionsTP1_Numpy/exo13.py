import numpy as np
import time

def f(x):
    return 1 + 2*x

def g(x):
    return 1 + 2*x

def trap_boucle(n, f, a=0., b=1.):
    """
    methode des trapezes avec une boucle python
    """
    h = (b - a)/n
    res = 0.
    for i in xrange(1, n):
        res += f(a+i*h)
    return h*(f(a)/2 + f(b)/2 + res)

def trap_vec(n, f, a=0., b=1.):
    """
    methode des trapezes vectorisee
    """
    h = (b - a)/n
    x = np.linspace(a, b, n + 1)
    res = f(x)
    return h/2*np.sum(res[:-1] + res[1:])

if __name__ == '__main__':
    n = 10000000
    
    t1 = time.clock()
    trap_boucle(n, g)
    print 'time for loop', time.clock() - t1
    
    t1 = time.clock()
    trap_vec(n, g)
    print 'time for vec', time.clock() - t1
