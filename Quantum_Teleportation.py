import cirq
from cirq.ops import qubit_order
from numpy import random
from sympy.polys.specialpolys import random_poly

simulator = cirq.Simulator()
message, kept, sent = [cirq.LineQubit(x) for x in range(0,3)]

circuit = cirq.Circuit()

#sets up state of message bit
randx = random.random()
randy = random.random()
circuit.append([cirq.XPowGate(exponent=randx)(message), cirq.YPowGate(exponent=randy)(message)])
message_example_circuit = cirq.Circuit.from_ops([cirq.XPowGate(exponent=randx)(message), cirq.YPowGate(exponent=randy)(message)])
message_results = simulator.simulate(message_example_circuit)
message_state = cirq.bloch_vector_from_state_vector(message_results.final_state, 0)
print(message_state)


#sets up bell state
circuit.append([cirq.H(kept), cirq.CNOT(kept, sent)])


#prepares the message and sender bits for measurement and measures them
circuit.append([cirq.CNOT(message, kept)])
circuit.append([cirq.H(message)])
circuit.append([cirq.measure(message, kept)])


#performs the neccessary operations based of the measured value
circuit.append([cirq.CNOT(kept, sent), cirq.CZ(message, sent)])

results = simulator.simulate(circuit)

print(circuit)
print(results.final_state)
print(cirq.bloch_vector_from_state_vector(results.final_state, 2))

