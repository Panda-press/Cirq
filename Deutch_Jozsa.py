import cirq

simulator = cirq.Simulator()
q0, q1 = cirq.LineQubit.range(2)

circuit = cirq.Circuit()
circuit.append([cirq.X(q1), cirq.H(q0), cirq.H(q1)])

#Start of function being tested

circuit.append([cirq.CNOT(q0, q1)])
# circuit.append([cirq.X(q1)])

#End of function being tested

circuit.append([cirq.H(q0)])
circuit.append([cirq.measure(q0)])

print(circuit)

results = simulator.run(circuit, repetitions=10)

print(results)