# Introduction to the QEC algebra
In this document I will give an introduction to the Heisenberg picture, 
the stabilizer formalism, quantum circuit diagrams and some basic quantum error
correction codes.
## Add simple example of both schroedinger and heisenberg picture
## Quantum circuit diagrams
- Operator gates are applied along lines
- Time progresses left to right
- Multi-qubit gates such as CNOT are drawn across lines
- Circles represent data qubits and squares represent connected ancillas.
- Output of circuits base
## The Heisenberg notation & stabilizer formalism

- **stuff about Pauli group and clifford group**
- Look at operator evolution instead of state evolution
	- $Circuit(|\psi\rangle) \rightarrow Circuit(A) $
- Call Operators with +1 eigenvalue for all input states stabilizers
- By specifically looking at the evolution of operators to which system input
are Eigenstates, we can efficiently calculate the output of a quantum circuit on multi-qubit superposition states
	- $H|\psi\rangle=|\psi\rangle \forall |\psi\rangle \in Input state space$ 

		$\rightarrow Circuit(|\psi\rangle) = Circuit(H)|\psi\rangle$


## Quantum error detection/correction
- Distance 3 circuit to detect bitflip error on repetition encoded logical 1.
The fourth and fitfth bit are called ancilla bits and tell us where error occured:
    ![](./img/bitflipSyndromeExtraction3Rep.png)

- Ancillas are responsible for syndrome extraction
- Repetition code:
    - E.g. Distance 3 X rep code stabilised by ZZI, IZZ
    - Connect each except border ancillas to 2 data qubits in such a way that data qubit leaving codespace leads to ancilla collapsing into 1.
    ![](./img/repcodeWithSyndrome.png)
        Distance 5 Repetition Code with 2 bitflip errors generating a syndrome.
        
- Ringcode
    - The Ringcode requires 1 fewer ancillas to operate, however it or its higher dimensional equivalents like the toric code are harder to implement due to the need for long-distance gates
    ![](./img/ringCodeWithSyndrome.png)
    - Distance 5 Ring Code with 2 bitflip errors generating a syndrome.
        
- Issue:
    - Only detect bitflip/phaseflip error, not both
    - Solution: 2D Codes to detect multiples types of errors, namely X and Z since this leads to Y because [X,Z]~Y
- Toric Code:
    - Hypergraph product code of two ringcodes
    - Repeat Ringcode along edges of lattice and loop around for X ancillas (black)
    - Place Z ancillas (green) on "Faces" of lattice, connecting to each data qubit that is adjacent to that face.
    ![](./img/toricCode.png)
- Surface Code:
    - Hypergraph product code of two rep codes
    - basically like toric code, except for no looping around and therefore border ancillas that connect to fewer data qubits
