"for all our matrix stuff"
import numpy as np


def triple(first, second, third) -> np.ndarray:
    "makes pauli tensorproduct for 3 qubit systems"

    return np.kron(first, np.kron(second, third))


def genpaulis() -> list[np.ndarray]:
    "generates the pauli matrices"

    pauli_0: np.ndarray = np.zeros((2, 2), dtype=np.complex_)
    pauli_x: np.ndarray = np.array([[0, 1],
                                    [1, 0]])
    pauli_z: np.ndarray = np.array([[1, 0],
                                    [0, -1]])
    pauli_y: np.ndarray = pauli_x@pauli_z
    pauli_i: np.ndarray = np.array([[1, 0],
                                    [0, 1]])
    pauli_x: np.ndarray = pauli_x + pauli_0
    pauli_y: np.ndarray = pauli_y+pauli_0
    pauli_z: np.ndarray = pauli_z + pauli_0
    pauli_i: np.ndarray = pauli_i + pauli_0

    return [pauli_x, pauli_z, pauli_i, pauli_y]


def measure(measurement, densitym) -> np.ndarray:
    """
    Given a measurement operator and density matrix to operate on,
    return the density matrix resulting from the measurement
    """
    res: np.ndarray = measurement @ densitym @ \
        np.conj(np.transpose(measurement))

    return res


def tensormaker3(matrices) -> list[np.ndarray]:
    "makes all tensorproducts of three matrices"

    retlist: list[np.ndarray] = []
    for matrix in matrices:
        for matrix2 in matrices:
            for matrix3 in matrices:
                retlist.append(triple(matrix, matrix2, matrix3))

    return retlist


def doescommute(m1: np.ndarray, m2: np.ndarray) -> np.ndarray:
    "Tells you wether to matrices commute or not"
    dim1 = m1.shape
    dim2 = m2.shape
    if dim1 != dim2:
        raise TypeError("matrices need same first dimensions")
    # zeros: np.ndarray = np.zeros(m1, dtype=np.complex_)

    return np.subtract(m1@m2, m2@m1)

def main() -> None:
    """main function idk """

    pauli_x, pauli_z, pauli_i = genpaulis()[0:3]
    # tensors3: list[np.ndarray] = tensormaker3([X,Z,I])
    iii: np.ndarray = triple(pauli_i, pauli_i, pauli_i)
    ixx: np.ndarray = triple(pauli_i, pauli_x, pauli_x)
    xxx: np.ndarray = triple(pauli_x, pauli_x, pauli_x)
    xxp: np.ndarray = iii + ixx
    ixi: np.ndarray = triple(pauli_i, pauli_x, pauli_i)
    izi: np.ndarray = triple(pauli_i, pauli_z, pauli_i)
    zzi: np.ndarray = triple(pauli_z, pauli_z, pauli_i)
    ziz: np.ndarray = triple(pauli_z, pauli_z, pauli_z)
    zeros: np.ndarray = np.zeros((8, 8), dtype=np.complex_)
    
    z3: np.ndarray = zzi@ziz
    abm: np.ndarray = izi@ixx
    bam: np.ndarray = ixx@izi
    minus: np.ndarray = zeros - izi
    abbac: np.ndarray = np.subtract(abm, bam)
    abbaa: np.ndarray = np.add(abm, bam)
    print(triple(pauli_i, pauli_i, pauli_z))

    print(z3, "hello")


if __name__ == "__main__":
    main()
