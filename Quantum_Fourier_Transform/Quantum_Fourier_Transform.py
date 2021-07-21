import cirq
from cirq.ops.common_gates import CZ, H
import numpy as np

n = 4

qubits = [cirq.LineQubit(i) for i in range(0, n)]

simulator = cirq.Simulator()

def QTF(n, qubits):    
    for i in range(0, n-1):
        yield cirq.H(qubits[i])

        for j in range(i + 1, n):
            yield cirq.CZ(qubits[i], qubits[j]) ** (2 ** -(j - i))
    yield cirq.H(qubits[n-1])


def Inverse_QTF(n, qubits):   
    for i in range(n-1, -1, -1):
        yield cirq.H(qubits[i])

        for j in range(i - 1, -1, -1):
            yield cirq.CZ(qubits[i], qubits[j]) ** -(2 ** -(i - j))

circuit = cirq.Circuit.from_ops(
    QTF(n, qubits)
)

# result = simulator.simulate(circuit)

print(circuit)

# print(np.round(result.final_state, 3))
circuit = cirq.Circuit.from_ops(
    Inverse_QTF(n, qubits)
)

print(circuit)