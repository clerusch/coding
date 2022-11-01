import numpy as np
dist = 5
nq = dist       # number of qubits
na = nq - 1     # number of ancillas
pcm = np.array([[0 for _ in range(nq)] for _ in range(na)])
for i in range(na):
    pcm[i][i] = 1
    pcm[i][(i+1) % nq] = 1
print(pcm) 