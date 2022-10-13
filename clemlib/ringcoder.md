# Ringcode
- ancillas go in between the two data qubits
- their values are the decoder input (so normally n-1, but on ring there is an additional ancilla between the last and first qubit)
- the parity check matrix has entries on each data qubit the ancillas touch
- parity check matrix * actual error = syndrome (measurement input to the decoder)
