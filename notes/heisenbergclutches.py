"for all our matrix stuff"
import numpy as np

def measure(measurement, densitym):
    """
    Given a measurement operator and density matrix to operate on,
    return the density matrix resulting from the measurement
    """
    res = measurement @ densitym @ np.conj(np.transpose(measurement))
    return res

def triple(first,second,third):
    "does stuff for 3 qubit systems"
    return np.kron(first,np.kron(second,third))

def tensormaker3(matrices):
    retlist = []
    for matrix in matrices:
        for matrix2 in matrices:
            for matrix3 in matrices:
                retlist.append(triple(matrix, matrix2, matrix3))
    return retlist

def main():
    """main function idk """
    O = np.zeros((2,2),dtype=np.complex_)
    X = np.array([[0,1],
                  [1,0]])
    Z = np.array([[1,0],
                  [-1,0]])
    Y = X@Z
    I = np.array([[1,0],
                  [0,1]])
    X = X+O
    Y = Y+O
    Z = Z+O
    I = I+O
    tensors3 = tensormaker3([X,Y,Z,I])

    iii = triple(I,I,I)
    ixx = triple(I,X,X)
    izi = triple(I,Z,I)
    xxp =  iii + ixx

    print(measure(xxp, izi))

if __name__ == "__main__":
    main()
