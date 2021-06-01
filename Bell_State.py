import cirq

simulator = cirq.Simulator()
q0, q1 = [cirq.LineQubit(x) for x in range(0,2)]

circuit = cirq.Circuit()

circuit.append([cirq.H(q0), cirq.CNOT(q0, q1)])
circuit.append([cirq.measure(q0), cirq.measure(q1)])

print(circuit)

results = simulator.run(circuit, repetitions=10)

print(results)
