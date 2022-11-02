import numpy as np

def genRepPCM(distance):
    """
    Generates a repetition code parity-check-matrix
    Args:
        distance(Int): distance of the code 
    Returns:
        pcm(np.array([[]])): repetition code parity check matrix corresponding to distance
    """
    nq = distance   # number of qubits
    na = nq - 1     # number of ancillas
    pcm = np.array([[0 for _ in range(nq)] for _ in range(na)])
    for i in range(na):
        pcm[i][i] = 1
        pcm[i][(i+1) % nq] = 1
    return pcm

def genRingPCM(distance):
    """
    Generates a ring code parity-check-matrix

    Args:
        distance(Int): distance of 

    Returns:
        pcm(np.array([[]])): generated parity check matrix of distance
    """
    pcm=np.eye(distance)
    for i in range(distance):
        pcm[i][(i+1)%distance] = 1
    return pcm

def cHypergraph(h1,h2,distance):
    """
    Creates a Hypergraph product code from two classical codes
    
    Args:
        h1(numpy n-d array): first classical code pcm
        h2(numpy m-d array): second classical code pcm
        
    Returns:
        hyper(numpy 4*m*n-d array: Hypergraph product code pcm
    """
    lhx = np.kron(h1, np.eye(distance))
    rhx = np.kron(np.eye(distance), h2.T)
    hx = np.concatenate((lhx,rhx), axis=1)

    lhz = np.kron(np.eye(distance), h2)
    rhz = np.kron(h1.T, np.eye(distance))
    hz = np.concatenate((lhz,rhz), axis=1)
    
    hyper = np.kron(np.array([[1,0],[0,0]]),hx) + np.kron(np.array([[0,0],[0,1]]),hz)
    ## Just putting hx in top left and hz in bottom right
    return hx, hz

