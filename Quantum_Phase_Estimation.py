import numpy as np
import cirq
from cirq.ops.common_gates import CZ, H
from cirq.ops.measure_util import measure
from cirq.ops.pauli_gates import X
from cirq.ops.swap_gates import SWAP
import matplotlib.pyplot as plt

circuit = cirq.Circuit()

simulator = cirq.Simulator()


n = 4

def U_Gate(power):
    class U(cirq.Gate):
        def __init__(self) -> None:
            super().__init__()
        
        def _num_qubits_(self) -> int:
            return n

        def _decompose_(self, qubits):
            for _ in range(power):
                yield SWAP(qubits[0], qubits[3])
                yield SWAP(qubits[2], qubits[1])

        def _circuit_diagram_info_(self, args):
            return ["U^{0}".format(power)] * self.num_qubits()
        
    gate = U()
    return gate

u_qubits = cirq.LineQubit.range(n)

u_circuit = cirq.Circuit.from_ops(U_Gate(1)._decompose_(u_qubits))

print("U circuit")
print(u_circuit)



phase_qubits = [cirq.GridQubit(0, j) for j in range(0, 2*n)]
function_qubits = [cirq.GridQubit(1, j) for j in range(0, n)]




def Inverse_QFT_Gate(n):
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


QFT = Inverse_QFT_Gate(2*n)

circuit.append([X(function_qubits[0])])

for qubit in phase_qubits:
    circuit.append(H(qubit))

for j in range(0, 2*n):
    U = U_Gate(2**j)
    circuit.append(U.controlled(1)(phase_qubits[j], *function_qubits))

circuit.append([QFT(*phase_qubits)])
circuit.append(measure(*phase_qubits))

print(circuit)

results = np.array(list(simulator.run(circuit, repetitions=10000).measurements.items()))[0,1]
# print(results)
unique, frequency = np.unique(results, return_counts=True, axis=0)

unique = [''.join(unique[i].astype(str).tolist()) for i in range(len(unique))]


print(unique)
# print(frequency)

plt.bar(unique, frequency)
plt.xticks(rotation=90)
plt.show()

