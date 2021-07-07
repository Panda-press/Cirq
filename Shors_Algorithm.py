from sympy.polys.domains.pythonintegerring import PythonIntegerRing
import cirq
from cirq.devices.grid_qubit import GridQubit
from cirq.ops.pauli_gates import X
from cirq.ops.swap_gates import SWAP
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 2*x MOD 15

qubits = [[cirq.GridQubit(i, j) for j in range(0, 8)] for i in range(0, 2)]

simulator = cirq.Simulator()

circuit = cirq.Circuit()

def U_Gate(a, power):
    if power in [1,2,4,8,16,32,64,128]:
        class U(cirq.Gate):
            def __init__(self) -> None:
                super().__init__()
            
            def _num_qubits_(self) -> int:
                return 4

            def _decompose_(self, qubits):
                q0, q1, q2, q3 = qubits
                for _ in range(power):
                    if a in [2,13]:
                        yield SWAP(q0, q1)
                        yield SWAP(q1, q2)
                        yield SWAP(q2, q3)
                    if a in [7,8]:
                        yield SWAP(q2,q3)
                        yield SWAP(q1,q2)
                        yield SWAP(q0,q1)
                    if a == 11:
                        yield SWAP(q1, q3)
                        yield SWAP(q0, q2)
                    if a in [7,11,13]:
                        X(q0)
                        X(q1)
                        X(q2)
                        X(q3)

            def _circuit_diagram_info_(self, args):
                return ["{0}^{1} MOD 15".format(a, power)] * self.num_qubits()
            
        gate = U()
        return gate
    else:
        print("Invalid power, must be a power of 2")


def QFT_Gate(n):
    class QTF(cirq.Gate):
        def __init__(self) -> None:
            super().__init__()
        
        def _num_qubits_(self) -> int:
            return n

        def _decompose_(self, qubits):
            for i in range(n-1, -1, -1):
                yield cirq.H(qubits[i])

                for j in range(i - 1, -1, -1):
                    yield cirq.CZ(qubits[i], qubits[j]) ** -(2 ** -(i - j))

        def _circuit_diagram_info_(self, args):
            return ["QTF^{0}".format(n)] * self.num_qubits()
        
    gate = QTF()
    return gate

print(qubits)

a = 7

u = [U_Gate(a, 1),
     U_Gate(a, 2),
     U_Gate(a, 4),
     U_Gate(a, 8),
     U_Gate(a, 16),
     U_Gate(a, 32),
     U_Gate(a, 64),
     U_Gate(a, 128)]

QFT = QFT_Gate(8)

for i in range(0, len(qubits)):
    for j in range(0, len(qubits[0])):
        if i == 0:
            circuit.append(cirq.H(qubits[i][j]))

for j in range(3,4):
    circuit.append(cirq.X(qubits[1][j]))

for i in range(0, 8):
    circuit.append([u[i].controlled(1)(qubits[0][i], qubits[1][0], qubits[1][1], qubits[1][2], qubits[1][3])])

circuit.append([QFT(qubits[0][0],
                    qubits[0][1],
                    qubits[0][2],
                    qubits[0][3],
                    qubits[0][4],
                    qubits[0][5],
                    qubits[0][6],
                    qubits[0][7])])

circuit.append([cirq.measure(qubits[0][0], 
                             qubits[0][1], 
                             qubits[0][2], 
                             qubits[0][3], 
                             qubits[0][4], 
                             qubits[0][5], 
                             qubits[0][6], 
                             qubits[0][7])])

results = np.array(list(simulator.run(circuit, repetitions=10000).measurements.items()))[0,1]


unique, frequency = np.unique(results, return_counts=True, axis=0)


unique = [''.join(unique[i].astype(str).tolist()) for i in range(len(unique))]

print(circuit)
print(unique)
print(frequency)

plt.bar(unique, frequency)
plt.xticks(rotation=90)
plt.show()
