import numpy as np

a = np.array([[0,1],
              [1,0]])
b = np.array([[0,1],
              [1,0]])
c = np.kron(np.eye(2),b)
print(c)