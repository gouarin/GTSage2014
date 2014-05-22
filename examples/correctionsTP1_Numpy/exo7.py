import numpy as np

A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
A1 = np.ones((2, 2))
A2 = np.array([[1, 2], [2, 1]])

A[:2, :2] = np.dot(A[-2:, -2:] + A1, A2)
print A
