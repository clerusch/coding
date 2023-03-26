from betterlookup import genSteaneLookupTable, findMinWeight, findMinWeight
from random import random
from numpy import zeros, uint8, concatenate, array,\
    array_equal, linspace, vstack, hstack, zeros, ndarray
from matplotlib.pyplot import errorbar, legend, \
    savefig, xlabel, ylabel, plot

def genSteaneError(per)->ndarray:
    """ Generates an error vector on the Steane code"""
    empty7 = zeros(7, dtype=uint8)
    xerror = empty7.copy()
    zerror = empty7.copy()
    for i in range(len(xerror)):
        if random()<per:
            xerror[i] = 1
    for j in range(len(zerror)):
        if random()<per:
            zerror[j] = 1
    yerror = concatenate((xerror,zerror))
    for k, bit in enumerate(yerror[:6]):
        if random()<per:
            yerror[k] = (yerror[k] + 1)%2
            yerror[2*k] = (yerror[2*k]+1)%2
    error = (concatenate((xerror, empty7)) + yerror \
        + concatenate((empty7, zerror)))%2
    return error

def steaneLerCalc(steaneH, nr, per, logicals)->float:
    """Calculates the logical error rate of the steane 
    code decoded with a lookup table"""
    numErrors = 0
    looktable = genSteaneLookupTable()
    for _ in range(nr):
        actual_error = genSteaneError(per)
        syndrome = steaneH@actual_error %2
        predictions = looktable[tuple(syndrome)]
        pred = findMinWeight(predictions)
        pred_L_flips = logicals@pred %2
        actual_L_flips = logicals@actual_error %2
        if not array_equal(actual_L_flips, pred_L_flips):
            numErrors += 1
    return numErrors/nr

def makeHgpPcm(Hx, Hz)->ndarray:
    """
    Makes a full parity check matrix including x and z
    checks for a hypergraph product code of two other codes
    """
    Hx = hstack((Hx, zeros(Hx.shape, dtype=uint8)))
    Hz = hstack((zeros(Hz.shape, dtype=uint8), Hz))
    H = vstack((Hx, Hz))
    return H

def main():
    steanelogicals = \
        array([\
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]])
    steaneH = array([[1, 0, 0, 1, 0, 1, 1],
                     [0, 1, 0, 1, 1, 0, 1],
                     [0, 0, 1, 0, 1, 1, 1]])
    pers = linspace(5/100000, 5/10000, 30)
    lers = []
    nr = 10000
    H = makeHgpPcm(steaneH, steaneH)
    for per in pers:
        print(f"per={per}")
        lers.append(\
            steaneLerCalc(H, nr, per, steanelogicals))
    lers = array(lers)
    std_err = (lers*(1-lers)/nr)**0.5
    errorbar(pers, lers, yerr=std_err)
    plot(pers,pers)
    xlabel("Physical error rate")
    ylabel("Logical error rate")
    savefig("img/figures/steaneLookupThreshold.png")

if __name__ == "__main__":
    main()