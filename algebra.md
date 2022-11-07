# Introduction to the QEC algebra
In this document I will give an introduction to the Heisenberg picture, 
the stabilizer formalism, quantum circuit diagrams and some basic quantum error
correction codes.
## The Heisenberg notation & stabilizer formalism
- Look at operator evolution instead of state evolution
	- $Circuit(|\psi\rangle) \rightarrow Circuit(A) $
- Call Operators with +1 eigenvalue for all input states stabilizers
- By specifically looking at the evolution of operators to which system input
are Eigenstates, we can follow superposition states through a quantum circuit
	- $H|\psi\rangle=|\psi\rangle \forall |\psi\rangle \in Input state space$ 

		$\rightarrow Circuit(|\psi\rangle) = Circuit(H)(|\psi\rangle)$
- stuff about Pauli group and clifford group
## Quantum circuit diagrams
- Operator gates are applied along lines
- Time progresses left to right
- Multi-qubit gates such as CNOT are 