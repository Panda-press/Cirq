import cirq
from cirq.ops.common_gates import CZ, H
import numpy as np

n = 8

qubits = [cirq.LineQubit(i) for i in range(0, n)]

simulator = cirq.Simulator()

def QTF(n, qubits):    
    for i in range(0, n-1):
        yield cirq.H(qubits[i])

        for j in range(i + 1, n):
            yield cirq.CZ(qubits[j], qubits[i]) ** (2 ** -(j - i))

circuit = cirq.Circuit.from_ops(
    QTF(n, qubits)
)

# result = simulator.simulate(circuit)

print(circuit)

# print(np.round(result.final_state, 3))
