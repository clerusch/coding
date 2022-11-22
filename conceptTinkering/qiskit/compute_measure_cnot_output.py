from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit.compiler import transpile, assemble
from qiskit.visualization import *
import matplotlib.pyplot as plt

# load my IBMQ account (dunno if I have one)
provider = IBMQ.load_account()

# create a Quantum circuit acting on q register(?)
circuit = QuantumCircuit(2,2)

# add H gate on qubit 0
circuit.h(0)

# add CX control 0 target 1
circuit.cx(0,1)

# map the quantum measurement results to the classical bits
circuit.measure([0,1],[0,1])

# use Aer's qasm simulator
simulator = Aer.get_backend('qasm_simulator')

# execute the circuit on the qasm simulator
job = execute(circuit,simulator,shots=1000)

# grab results from the job
result = job.result()

# return counts
counts = result.get_counts(circuit)
print("\nTotal count for 00 and 11 are:",counts)

# draw the circuit
circuit.draw()
plt.show()

