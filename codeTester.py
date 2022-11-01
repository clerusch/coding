import numpy as np
import matplotlib.pyplot as plt
from pymatching import Matching
from pcmGenerators import genRingPCM, genRepPCM, cHypergraph

def lerCalc(pcm, nr = 100, dist = 5, per = 0.3):
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
    matching = Matching(pcm)
    nle = 0
    for _ in range(nr):
        error = (np.random.rand(4*dist**2) < per).astype(np.uint8)
        syndrome = (pcm@error) % 2
        corr = matching.decode(syndrome)
        res = (corr + error) % 2
        if sum(res) > 0:
            nle += 1
    ler = nle/nr
    return ler

def main(dists = [5,9,11]):
    """
    This will test and Plot schemes at distances
    """
    
    for d in dists:
        h1 = genRingPCM(d)
        h2 = genRingPCM(d)
        pcm = cHypergraph(h1,h2,d)
        ler = []
        per = [i/10 for i in range(10)]
        for p in per:
            new_ler = lerCalc(pcm,1000, d, p)
            ler.append(new_ler)
        plt.plot(per, ler, label=f"rep {d}")
        # ler = []
        # per = [i/10 for i in range(10)]
        # for p in per:
        #     new_ler = lerCalc(genRingPCM,1000, d, p)
        #     ler.append(new_ler)
        # plt.plot(per, ler, label=f"ring {d}")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()