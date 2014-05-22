
def g1(x):
    return x**2

def g2(x, a, b):
    return a*x**2 + b*x

def derivees(f, x, h=0.0001, extrarg=()):
    """
    Calcul approche des derivees premiere et seconde de la fonction f
    """
    f1 = f(x, *extrarg)
    f2 = f(x+h, *extrarg)    
    f3 = f(x-h, *extrarg)

    df = (f2 - f3)/(2.*h)
    ddf = (f2 -2*f1 + f3)/h**2

    return df, ddf

if __name__ == '__main__':
    print derivees(g1, 1)
    print derivees(g2, 1, extrarg=(1, 1))
    print derivees(g2, 1, extrarg=(1, 2))
