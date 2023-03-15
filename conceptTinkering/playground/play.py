import numpy as np
import matplotlib.pyplot as plt
from pymatching import Matching
#from lib.pcmGenerators import genRingPCM, genRepPCM, cHypergraph
#from lib.helperrank import rankmod2, rref_mod_2
from scipy.sparse import hstack, kron, eye, csr_matrix, block_diag

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
def toricXLogicals(dist):
    """
    binary matrix with each row being an x logical operator of a toric code
    """
    H1 = csr_matrix(([1], ([0],[0])), shape=(1,dist), dtype=np.uint8)
    H0 = csr_matrix(np.ones((1, dist), dtype=np.uint8))
    x_logicals = block_diag([kron(H1, H0), kron(H0, H1)])
    x_logicals.data = x_logicals.data % 2
    x_logicals.eliminate_zeros()
    return csr_matrix(x_logicals)
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
def repetition_code(n):
    """
    Parity check matrix of a repetition code with length n.
    """
    row_ind, col_ind = zip(*((i, j) for i in range(n) for j in (i, (i+1)%n)))
    data = np.ones(2*n, dtype=np.uint8)
    return csr_matrix((data, (row_ind, col_ind)))

dist = 5
bla = genRingPCM(3)

c = repetition_code(dist).todense()
d = csr_matrix(genRepPCM(dist)).todense()
#print(c, "\n", "hi", "\n", d)
a = csr_matrix(([1], ([0],[0])), shape=(1,dist), dtype=np.uint8)
b = csr_matrix(np.ones((1, dist), dtype=np.uint8))
j = toricXLogicals(5)
print(j.todense()) 



#saved one:
def lerCalc(H, logicals, nr=1000, per = 0.3):
    "calculates logical error rate assuming a noise model of p/3 X,Y,Z errors"
    matching = Matching.from_check_matrix(H, faults_matrix=logicals)
    numErrors = 0
    for _ in range(nr):
        noise = np.zeros(H.shape[1])
        for i in range(len(noise)/2):
            # this is physical X errors, editing first half of entries
            if np.random.rand() < per/3:
                noise[i] = (noise[i]+1) % 2
            # this is physical Z errors, editing second half of entries
            if np.random.rand() < per/3:
                noise[i+len(noise)/2] = (noise[i+len(noise)/2] + 1) % 2
            # this is physical Y errors, assuming same syndrome as X and Z implies same error
            if np.random.rand() < per/3:
                noise[i] = (noise[i]+1) % 2
                noise[i+len(noise)/2] = (noise[i+len(noise)/2] + 1) % 2
        #noise = np.random.binomial(1, per, H.shape[1])
        noise = csr_matrix(noise)
        syndrome = H@noise % 2
        predict = matching.decode(syndrome)
        actualLflips = logicals@noise % 2
        if not np.array_equal(actualLflips, predict):
            numErrors += 1
    return numErrors/nr

dist = int(np.sqrt(H.shape[1]/2))
message1 = np.zeros(dist)