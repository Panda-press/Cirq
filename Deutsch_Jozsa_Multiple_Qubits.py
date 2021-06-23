import cirq

q0, q1, q2, result = cirq.LineQubit.range(4)

simulator = cirq.Simulator()

constant_functions = [[], [cirq.X(q2)]]

balanced_functions = [[cirq.CNOT(q0, q2)],
                      [cirq.CNOT(q1, q2)],
                      [cirq.CNOT(q0, q2), cirq.CNOT(q1, q2)],
                      [cirq.CNOT(q0, q2), cirq.X(q2)],
                      [cirq.CNOT(q1, q2), cirq.X(q2)],
                      [cirq.CNOT(q0, q2), cirq.CNOT(q1, q2), cirq.X(q2)]]

def Create_Circuit(oracel):
    circuit = cirq.Circuit()

    #Prepare inital states
    circuit.append([cirq.X(q2)])

    #Applies hamaltonian accross all qubits
    circuit.append([cirq.H(q0), cirq.H(q1), cirq.H(q2)])

    #Adds the oracel
    circuit.append(oracel)

    #Applies hamaltonian accross input qubits
    circuit.append([cirq.H(q0), cirq.H(q1)])

    #Puts result on the result qubit
    circuit.append([cirq.X(q0), cirq.X(q1)])
    circuit.append([cirq.CCNOT(q0, q1, result)])
    circuit.append([cirq.X(result)])

    #Measures result qubit
    circuit.append([cirq.measure(result)])
    #1 represents a balanced function, 0 constant

    return circuit


circuit = Create_Circuit(balanced_functions[5])

print(circuit)

#1 represents a balanced function, 0 constant
results = simulator.run(circuit, repetitions=10)

print(results)