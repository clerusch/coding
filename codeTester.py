import numpy as np
import matplotlib.pyplot as plt
from pymatching import Matching
from lib.pcmGenerators import genRingPCM, genRepPCM, cHypergraph
from lib.helperrank import rankmod2, rref_mod_2

def lerCalc(hx, hz, nr = 100, dist = 5, per = 0.3):
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
    matchingx = Matching(hx)
    matchingz = Matching(hz)
    rhx = rankmod2(hx)
    rhz = rankmod2(hz)
    nle = 0
    for _ in range(nr):
        errorx = (np.random.rand(2*dist**2) < per).astype(np.uint8)
        syndromex = (hx@errorx) % 2
        corrx = matchingx.decode(syndromex)
        resx = (corrx + errorx) % 2
        errorz = (np.random.rand(2*dist**2) < per).astype(np.uint8)
        syndromez = (hz@errorz) % 2
        corrz = matchingz.decode(syndromez)
        resz = (corrz + errorz) % 2
        if rhx != rankmod2(np.vstack([hx,resx])) or rhz != rankmod2(np.vstack([hz,resz])):
            nle += 1
            print(corrx,errorx,resx)
            print(np.sum(resx))
            print(corrz,errorz,resz)
            print(np.sum(resz))
    ler = nle/nr
    return ler

def main(dists = [5]):
    """
    This will test and Plot schemes at distances
    """
    for d in dists:
        h1 = genRingPCM(d)
        h2 = genRingPCM(d)
        hx, hz = cHypergraph(h1,h2,d)
        ler = []
        pmax = .02
        per = np.linspace(0,pmax,10)
        for p in per:
            new_ler = lerCalc(hx, hz,2000, d, p)
            ler.append(new_ler)
        plt.plot(per, ler, label=f"tor {d}")
    x = [0,pmax]
    plt.plot(x,x)
    plt.legend()
    plt.savefig("./toric.png")

if __name__ == "__main__":
    main()