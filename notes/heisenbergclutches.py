"for all our matrix stuff"
import numpy as np

def measure(measurement, densitym) -> np.ndarray:
    """
    Given a measurement operator and density matrix to operate on,
    return the density matrix resulting from the measurement
    """
    res: np.ndarray = measurement @ densitym @ \
        np.conj(np.transpose(measurement))
    return res

def triple(first,second,third) -> np.ndarray:
    "does stuff for 3 qubit systems"
    return np.kron(first,np.kron(second,third))

def tensormaker3(matrices) -> list[np.ndarray]:
    "makes a tensorproduct of three matrices"
    retlist: list[np.ndarray]= []
    for matrix in matrices:
        for matrix2 in matrices:
            for matrix3 in matrices:
                retlist.append(triple(matrix, matrix2, matrix3))
    return retlist

def main() -> None:
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
    #tensors3: list[np.ndarray] = tensormaker3([X,Z,I])
    iii: np.ndarray = triple(I,I,I)
    ixx: np.ndarray = triple(I,X,X)
    izi: np.ndarray = triple(I,Z,I)
    xxp: np.ndarray =  iii + ixx
    res: np.ndarray = measure(xxp, izi)
    print(res)
 

if __name__ == "__main__":
    main()
