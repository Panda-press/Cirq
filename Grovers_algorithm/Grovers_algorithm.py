import cirq
from cirq.ops.measure_util import measure
import numpy as np
import random as rnd
import matplotlib.pyplot as plt

from numpy.lib.index_tricks import OGridClass

n = 3

qubits = cirq.LineQubit.range(n)

circuit = cirq.Circuit()

simulator = cirq.Simulator()

oracle_marix = [[0 for i in range(0, 2**n)] for j in range(0, 2**n)]

for i in range(0, len(oracle_marix)):
    oracle_marix[i][i] = 1

solutions = [0,1,2,3]
for solution in solutions:
    oracle_marix[solution][solution] = -1

oracle_marix = np.array(oracle_marix)

print(oracle_marix)

class Oracle(cirq.Gate):
    def __init__(self):
        super(Oracle, self)

    def _num_qubits_(self):
        return n

    def _unitary_(self):
        return oracle_marix

    def _circuit_diagram_info_(self, args):
        return ['oracle'] * self._num_qubits_()


#Apply haliltonian and oracle
circuit.append([cirq.H(qubits[i]) for i in range(0, n)])
circuit.append([Oracle().on(*qubits)])

#Apple Diffuser
circuit.append([cirq.H(qubits[i]) for i in range(0, n)])
circuit.append([cirq.X(qubits[i]) for i in range(0, n)])
circuit.append([cirq.Z(qubits[0]).controlled_by(*qubits[1:])])
circuit.append([cirq.X(qubits[i]) for i in range(0, n)])
circuit.append([cirq.H(qubits[i]) for i in range(0, n)])

#Measure
circuit.append([measure(*qubits)])

print(circuit)

results = np.array(list(simulator.run(circuit, repetitions=10000).measurements.items()))[0,1]

unique, frequency = np.unique(results, return_counts=True, axis=0)

unique = [''.join(unique[i].astype(str).tolist()) for i in range(len(unique))]

plt.bar(unique, frequency)
plt.xticks(rotation=90)
plt.show()
