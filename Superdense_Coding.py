import cirq

bit1 = 0
bit2 = 1

q0, q1 = cirq.LineQubit.range(2)
simulator = cirq.Simulator()

circuit = cirq.Circuit()
circuit.append([cirq.H(q0), cirq.CNOT(q0, q1)])

if bit2 == 1:
    circuit.append(cirq.X(q0))

if bit1 == 1:
    circuit.append(cirq.Z(q0))


circuit.append([cirq.CNOT(q0, q1)])
circuit.append([cirq.H(q0)])

circuit.append([cirq.measure(q0), cirq.measure(q1)])


results = simulator.run(circuit, repetitions=10)


print(circuit)
print("The measage is {0}{1}.".format(bit1, bit2))
print(results)