import numpy as np
import matplotlib.pyplot as plt
from pymatching import Matching
from sys import argv
"""
This is to test decoding algorithms for repetition based codes
"""

def genRepPCM(distance):
    nq = distance   # number of qubits
    na = nq - 1     # number of ancillas
    pcm = np.array([[0 for _ in range(nq)] for _ in range(na)])
    for i in range(na):
        pcm[i][i] = 1
        pcm[i][(i+1) % nq] = 1
    return pcm

def lercalc(nr = 100, dist = 5, per = 0.3):
    pcm = genRepPCM(dist)
    matching = Matching(pcm)
    nle = 0
    for _ in range(nr):
        error = (np.random.rand(dist) < per).astype(np.uint8)
        syndrome = (pcm@error) % 2
        corr = matching.decode(syndrome)
        res = (corr + error) % 2
        if sum(res) > 0:
            nle += 1
    return nle/nr

def main(dists = [3,5,9,29,35]):
    """
    For simplicity's sake this will test on a zero message
    """
    for d in dists:
        ler = []
        per = [i/10 for i in range(10)]
        for p in per:
            new_ler = lercalc(1000, d, p)
            ler.append(new_ler)
        plt.plot(per, ler, label=d)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
