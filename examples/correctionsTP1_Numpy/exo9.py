import numpy as np

def initial_condition(x):
    if np.isscalar(x):
        return 3.0
    else:
        return 3.0*np.ones(x.shape)
        
print initial_condition(2)
print initial_condition(np.ones((2, 2)))
