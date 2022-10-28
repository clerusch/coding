import numpy as np
import matplotlib.pyplot as plt
from pymatching import Matching
from sys import argv

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

def lerCalc(pcmType, nr = 100, dist = 5, per = 0.3):
    """
    Calculates a logical error rate of dist code assuming specific physical error rate

    Args:
        pcmType(Int->PCM): Function to generate a pcm from a distance
        nr(Int)   :        Number of runs
        dist(Int) :        Distance of the code to analyse
        per(Float):        Physical error rate to assume during analysis
    
    Returns:
        ler(Float):        Logical error rate of coding scheme with given parameters
    """
    pcm = pcmType(dist)
    matching = Matching(pcm)
    nle = 0
    for _ in range(nr):
        error = (np.random.rand(dist) < per).astype(np.uint8)
        syndrome = (pcm@error) % 2
        corr = matching.decode(syndrome)
        res = (corr + error) % 2
        if sum(res) > 0:
            nle += 1
    ler = nle/nr
    return ler

def main(dists = [3, 9]):
    """
    This will test and Plot schemes at distances
    """
    for d in dists:
        ler = []
        per = [i/10 for i in range(10)]
        for p in per:
            new_ler = lerCalc(genRepPCM,1000, d, p)
            ler.append(new_ler)
        plt.plot(per, ler, label=f"rep {d}")
        ler = []
        per = [i/10 for i in range(10)]
        for p in per:
            new_ler = lerCalc(genRingPCM,1000, d, p)
            ler.append(new_ler)
        plt.plot(per, ler, label=f"ring {d}")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
    
