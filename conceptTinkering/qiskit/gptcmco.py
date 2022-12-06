#import qiskit
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
import matplotlib.pyplot as plt

#create quantum and classical registers
q = QuantumRegister(2)
c = ClassicalRegister(2)

#create a quantum circuit
qc = QuantumCircuit(q, c)

#add a CNOT gate
qc.cx(q[0], q[1])

#add ancilla measurements
qc.measure(q[0], c[0])
qc.measure(q[1], c[1])

#add conditional X and Z gates
qc.x(q[1]).c_if(c, 1)
qc.z(q[1]).c_if(c, 2)

#draw the circuit
qc.draw(output='mpl')
plt.plot()
plt.savefig("./bla.png")