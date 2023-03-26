from networkx import draw, Graph
from matplotlib.pyplot import savefig
from numpy import kron, eye, uint8, hstack, zeros, vstack, array
from os import makedirs
from os.path import exists
from scipy.sparse import spmatrix, csr_matrix
from pymatching import Matching

def genRepPCM(distance: int)->spmatrix:
    """
    Generates a repetition code parity-check-matrix
    Args:
        distance(Int): distance of the code 
    Returns:
        pcm(np.array([[]])): repetition code parity check matrix corresponding to distance
    """
    nq = distance   # number of qubits
    na = nq - 1     # number of ancillas
    pcm = array([[0 for _ in range(nq)] for _ in range(na)])
    for i in range(na):
        pcm[i][i] = 1
        pcm[i][(i+1) % nq] = 1
    return csr_matrix(pcm)

def genRingPCM(distance: int)->spmatrix:
    """
    Generates a ring code parity-check-matrix

    Args:
        distance: distance of the code

    Returns:
        pcm: generated parity check matrix of distance
    """
    pcm = eye(distance, dtype=uint8)
    for i in range(distance):
        pcm[i][(i+1)%distance] = 1
    return csr_matrix(pcm)

def genHGPPcm(first_code: spmatrix, second_code: spmatrix)-> spmatrix:
    """
    Generates a hypergraph product code parity-check-matrix 
    from two valid codes parity-check-matrices
    """
    firstm = first_code.todense()
    secondm = second_code.todense()
    m1, n1 = firstm.shape[0], firstm.shape[1]
    m2, n2 = secondm.shape[0], secondm.shape[1]
    
    Hx = hstack(
        [kron(firstm, eye(n2, dtype=uint8)), \
            kron(eye(m1, dtype=uint8), secondm.T)])
    Hz = hstack(
            [kron(eye(n1, dtype=uint8), secondm), \
                kron(firstm.T, eye(m2, dtype=uint8))])
    
    top = hstack((Hx, zeros(Hx.shape, dtype=uint8)))
    bottom = hstack((zeros(Hz.shape, dtype=uint8), Hz))
    HGPPcm = csr_matrix(vstack((top, bottom)))
    
    return HGPPcm
def calc_logicals(hx, hz):
    
def main()-> None:
    if not exists("img/figures/"):
            makedirs("img/figures")
    
    ring = genRepPCM(3)
    error = zeros(18, dtype=uint8)
    error[2] = 1
    torus = genHGPPcm(ring, ring)
    # syndrome = torus @ error
    toricMatching = Matching(torus)
    print(torus.shape)
    # print(toricMatching.decode(syndrome)==error)
    # toricMatching.draw()
    # filename = "torusgraph.png"
    
    # savefig("img/figures/"+filename)

if __name__ == '__main__':
    main()