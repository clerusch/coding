import numpy as np
import matplotlib.pyplot as plt
from pymatching import Matching
from scipy.sparse import hstack, kron, eye, csr_matrix, block_diag
from ldpc import mod2

############################ Constants #############################
steaneH = np.array([[1, 0, 0, 1, 0, 1, 1],
                      [0, 1, 0, 1, 1, 0, 1],
                      [0, 0, 1, 0, 1, 1, 1]])
steanelogicals = np.array([[1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]])
############################ Helper functions ######################
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

def ring_code(n):
    """
    scipy sparse Parity check matrix of a ring code with length n.
    """
    return csr_matrix(genRingPCM(n))

def rep_code(n):
    """
    scipy sparse Parity check matrix of a rep code with n qubits
    """
    return csr_matrix(genRepPCM(n))

def genSteaneLookupTable():
    H = np.array([[1, 0, 0, 1, 0, 1, 1],
               [0, 1, 0, 1, 1, 0, 1],
               [0, 0, 1, 0, 1, 1, 1]])
    null = np.zeros(H.shape)
    firstline = np.hstack((H, null))
    secondline = np.hstack((null, H))
    pcm = np.vstack((firstline, secondline))
    dict = {}
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for h in range(2):
                    for l in range(2):
                        for m in range(2):
                            for n in range(2):
                                for l in range(2):
                                    for m in range(2):
                                        for n in range(2):
                                            for o in range(2):
                                                for p in range(2):
                                                    for q in range(2):
                                                        for r in range(2):
                                                            for s in range(2):
                                                                for t in range(2):
                                                                    for u in range(2):
                                                                        error = np.array([i,j,k,h,l,m,n,o,p,q,r,s,t,u])
                                                                        syndrome = tuple(pcm@error)
                                                                        if syndrome in dict:
                                                                            dict[syndrome].append(error)
                                                                        else:
                                                                            dict[syndrome] = [error]
    return dict

def genSteaneHLookupTable(H):
    null = np.zeros(H.shape)
    firstline = np.hstack((H, null))
    secondline = np.hstack((null, H))
    pcm = np.vstack((firstline, secondline))
    dict = {}
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for h in range(2):
                    for l in range(2):
                        for m in range(2):
                            for n in range(2):
                                for l in range(2):
                                    for m in range(2):
                                        for n in range(2):
                                            error = np.array([i,j,k,h,l,m,n])
                                            syndrome = tuple(pcm@error)
                                            if syndrome in dict:
                                                dict[syndrome].append(error)
                                            else:
                                                dict[syndrome] = [error]
    return dict

def genXStabilizers(first_pcm_generator, second_pcm_generator, dist):
    """
    check matrix for the X stabilizers of a hypergraph product code of distance dist
    """
    H1 = first_pcm_generator(dist)
    H2 = second_pcm_generator(dist)
    H = hstack(
        [kron(H1, eye(H2.shape[1])), kron(eye(H1.shape[0]), H2.T)],
        dtype=np.uint8
    )
    return H

def genZStabilizers(first_pcm_generator, second_pcm_generator, dist):
    """
    check matrix for the Z stabilizers of a hypergraph product code of distance dist
    """
    H1 = first_pcm_generator(dist)
    H2 = second_pcm_generator(dist)
    H = hstack(
            [kron(eye(H1.shape[1]), H2), kron(H1.T, eye(H2.shape[0]))],
            dtype=np.uint8
        )
    return H

def genHxHz(first_code, second_code, d):
    """
    generates Hx and Hz of a hgp code from two codes
    """
    Hx = genXStabilizers(first_code, second_code, d).todense()
    Hz = genZStabilizers(first_code, second_code, d).todense()
    # Hx = np.hstack((Hx, np.zeros(Hx.shape, dtype=np.uint8)))
    # Hz = np.hstack((np.zeros(Hz.shape, dtype=np.uint8), Hz))

    return Hx, Hz

def compute_lz(hx,hz):
            #lz logical operators
            #lz\in ker{hx} AND \notin Im(Hz.T)
            # hx = hx.todense()
            # hz = hz.todense()
            ker_hx=mod2.nullspace(hx) #compute the kernel basis of hx
            im_hzT=mod2.row_basis(hz) #compute the image basis of hz.T

            #in the below we row reduce to find vectors in kx that are not in the image of hz.T.
            log_stack=np.vstack([im_hzT,ker_hx])
            pivots=mod2.row_echelon(log_stack.T)[3]
            log_op_indices=[i for i in range(im_hzT.shape[0],log_stack.shape[0]) if i in pivots]
            log_ops=log_stack[log_op_indices]
            return log_ops

def calc_logicals(hx, hz):
    """ calculates actual logical operators from two parity check matrices of 
    codes generating a hgp code
    """

    lx = compute_lz(hz, hx)
    lz = compute_lz(hx, hz)
    lx=np.vstack((np.zeros(lz.shape,dtype=np.uint8),lx))
    lz=np.vstack((lz,np.zeros(lz.shape,dtype=np.uint8)))
    # temp = mod2.inverse(lx@lz.T %2)
    # lx  = temp@lx % 2
    return np.hstack((lx, lz))

def makeHgpPcm(Hx, Hz):
    """
    Makes a full parity check matrix including x and z checks for a 
    hypergraph product code of two other codes
    """
    # Hx = genXStabilizers(first_code, second_code, d).todense()
    # Hz = genZStabilizers(first_code, second_code, d).todense()
    Hx = np.hstack((Hx, np.zeros(Hx.shape, dtype=np.uint8)))
    Hz = np.hstack((np.zeros(Hz.shape, dtype=np.uint8), Hz))
    H = np.vstack((Hx, Hz))
    print(H)
    return csr_matrix(H)

############################# Hotstuff #############################
def lerCalc(H, logicals, nr=1000, per = 0.3):
    "calculates logical error rate assuming a noise model of p/3 X,Y,Z errors"
    matching = Matching.from_check_matrix(H)#, faults_matrix=logicals)
    numErrors = 0
    for _ in range(nr):
        noise = np.zeros(H.shape[1], dtype=np.uint8)
        halflength = int(len(noise)/2)
        for i in range(halflength):
            # this is physical X errors, editing first half of entries
            if np.random.rand() < per/3:
                noise[i] = (noise[i]+1) % 2
            # this is physical Z errors, editing second half of entries
            if np.random.rand() < per/3:
                noise[i+halflength] = (noise[i+halflength] + 1) % 2
            # this is physical Y errors, assuming same syndrome as X and Z implies same error
            if np.random.rand() < per/3:
                noise[i] = (noise[i]+1) % 2
                noise[i+halflength] = (noise[i+halflength] + 1) % 2
        noise = csr_matrix(noise)
        noise = noise.T
        syndrome = csr_matrix(((H@noise).todense() % 2))
        prediction = csr_matrix(matching.decode(syndrome.todense())).T
        predicted_flips = (logicals@prediction).todense() % 2
        actualLflips = (logicals@noise).todense() % 2
        if not np.array_equal(actualLflips, predicted_flips):
            numErrors += 1
    return numErrors/nr

def steaneLerCalc(H, logicals, nr=1000, per = 0.3):
    "calculates logical error rate decoding steane code with a lookup table assuming a noise model of p/3 X,Y,Z errors"
    numErrors = 0
    looktable = genSteaneHLookupTable(steaneH)
    for _ in range(nr):
        noise = np.zeros(H.shape[1], dtype=np.uint8)
        halflength = int(len(noise)/2)
        for i in range(halflength):
            # this is physical X errors, editing first half of entries
            if np.random.rand() < per/3:
                noise[i] = (noise[i]+1) % 2
            # this is physical Z errors, editing second half of entries
            if np.random.rand() < per/3:
                noise[i+halflength] = (noise[i+halflength] + 1) % 2
            # this is physical Y errors, assuming same syndrome as X and Z implies same error
            if np.random.rand() < per/3:
                noise[i] = (noise[i]+1) % 2
                noise[i+halflength] = (noise[i+halflength] + 1) % 2
        noise = noise.T
        syndrome = H@noise % 2
        prediction = looktable[tuple(syndrome)][0]
        predicted_flips = logicals@prediction % 2
        actualLflips = logicals@noise % 2
        if not np.array_equal(actualLflips, predicted_flips):
            numErrors += 1
    return numErrors/nr

def thresholdPlotter(dists, pers, nr, first_code, second_code):
    """
    plots logical error rates of a quantum code with a list of distances
    and physical error rates
    """
    np.random.seed(2)
    log_errors_all_dist = []
    for d in dists:
        print("Simulating d = {}".format(d))
        Hx, Hz = genHxHz(first_code, second_code, d)
        H = makeHgpPcm(Hx, Hz)
        logicals = csr_matrix(calc_logicals(Hx, Hz))
        lers = []
        for per in pers:
            print(f"per={per}")
            lers.append(lerCalc(H, logicals, nr, per))
        log_errors_all_dist.append(np.array(lers))
    plt.figure()
    for dist, logical_errors in zip(dists, log_errors_all_dist):
        std_err = (logical_errors*(1-logical_errors)/nr)**0.5
        plt.errorbar(pers, logical_errors, yerr=std_err, label="L={}".format(dist))
    plt.xlabel("Physical error rate")
    plt.ylabel("Logical error rate")
    # plt.yscale('log')
    plt.legend(loc=0)
    plt.show()

def main():
    dists = range(5,16,4)
    pers = np.linspace(0.1, 0.2, 20)
    nr = 10000
    #stabilizerGenerator = genXStabilizers(ring_code, ring_code, 6)
    thresholdPlotter(dists, pers, nr, ring_code, ring_code)
    
    
    

if __name__ == "__main__":
    main()