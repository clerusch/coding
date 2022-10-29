import numpy as np

distance = 2
hx = np.array([[0,1],
               [1,0]])
hz = np.array([[1,0],
               [0,1]])
def cHypergraph(hx,hz,distance):
    lhx = np.kron(hx, np.eye(distance))
    rhx = np.kron(np.eye(distance), hz.T)
    hhx = np.concatenate((lhx,rhx), axis=1)

    lhz = np.kron(np.eye(distance), hz)
    rhz = np.kron(hx.T, np.eye(distance))
    hhz = np.concatenate((lhz,rhz), axis=1)
    return hhx, hhz
    # return hhx, hhz

# print(lhx,rhx,hhx)