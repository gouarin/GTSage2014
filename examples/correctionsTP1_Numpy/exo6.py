import numpy as np

A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
b = np.array([-3, -2, -1])

print A.dtype, b.dtype
print np.dot(A, b)
