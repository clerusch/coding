from typing import List
from numpy import array, vstack, hstack, zeros, uint8, ones, ndarray
from itertools import product
from random import random

def genSteaneLookupTable()->dict:
    
    # Generate Steane parity check matrix from identical
    # X and Z PCMs
    H = array([[1, 0, 0, 1, 0, 1, 1],
                  [0, 1, 0, 1, 1, 0, 1],
                  [0, 0, 1, 0, 1, 1, 1]])
    pcm = vstack((hstack((H, zeros(H.shape))),
                     hstack((zeros(H.shape), H))))

    # Generate lookup table
    lookup_table = {}
    for error in product([0, 1], repeat=14):
        syndrome = tuple(pcm @ error % 2)
        if syndrome in lookup_table:
            lookup_table[syndrome].append(error)
        else:
            lookup_table[syndrome] = [error]

    # Remove duplicates from lookup table
    for key in lookup_table:
        lookup_table[key] = list(set(lookup_table[key]))

    return lookup_table

def findMinWeight(predictions)-> ndarray:
    """
    Find the minimum weight tuple for a given prediction
    """
    curr_pred = ones(14,dtype=uint8)
    curr_best_weight = 100
    for pred in predictions:
        pred = array(pred)
        yweight = 0
        for i in range(int(len(pred)/2)):
            if pred[i] & pred[i+7] == 1:
                yweight += 1
                pred[i] = 0
                pred[i+7] = 0
        if yweight + sum(pred) < curr_best_weight:
            curr_pred = pred
            curr_best_weight = yweight + sum(pred)
    return curr_pred

def main():
    syndrome = array([1,1,1,0,0,0])

    possibles = genSteaneLookupTable()[tuple(syndrome)]

    print(f"The syndrome {syndrome}\n can be caused by the following errors: ")

    print(f"The most likely cause of this syndrome is\n {findMinWeight(possibles)}")

if __name__=="__main__":
    main()