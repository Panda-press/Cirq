from operator import xor
import cirq
import numpy as np

q0, q1, q2, q3 = cirq.LineQubit.range(4)
circuit = cirq.Circuit()

#Prepare bell state
circuit.append([cirq.H(q0), cirq.CNOT(q0, q2)])


circuit.append([cirq.XPowGate(exponent=-0.25)(q0)])

#Prepares two 'input' qubits
circuit.append([cirq.H(q1), cirq.H(q3)])


#Performs controlled X gate with an exponent of 0.5 across the qubits
circuit.append([cirq.CNOT(q1, q0)**0.5, cirq.CNOT(q3, q2)**0.5])


#Measures all Qubits
circuit.append([cirq.measure(q0, key='a(x)'),
                cirq.measure(q1, key='x'),
                cirq.measure(q2, key='b(y)'),
                cirq.measure(q3, key='y')])

print(circuit)

simulator = cirq.Simulator()

repetitions = 100

results = simulator.run(circuit, repetitions=repetitions)
ax = np.array(results.measurements['a(x)']).flatten()
x = np.array(results.measurements['x']).flatten()
by = np.array(results.measurements['b(y)']).flatten()
y = np.array(results.measurements['y']).flatten()

axXORby = ax ^ by
xy = x & y
successes = (axXORby == xy)
successRate = np.sum(successes)/repetitions
#print(ax)
print(xy)
print(axXORby)
print(successes)
print(successRate)