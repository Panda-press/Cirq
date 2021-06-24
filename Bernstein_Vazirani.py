import cirq
import random as rnd

inputs_n = 8

input_qubits = [cirq.GridQubit(i, 0) for i in range(inputs_n)]
output_qubit = cirq.GridQubit(inputs_n, 0)

simulator = cirq.Simulator()

def Add_Oracle(circuit, input_qubits, output_qubit, inputs_n):    
    a = [rnd.randint(0,1) for _ in range(inputs_n)]

    for i in range(0, inputs_n):
        if (a[i] == 1):
            circuit.append([cirq.CNOT(input_qubits[i], output_qubit)])

    return circuit, a


circuit = cirq.Circuit()

#Set the output_qubit to |1>
circuit.append([cirq.X(output_qubit)])

#Apply hamaltonian acrross all qubits
circuit.append([cirq.H(input_qubits[i]) for i in range(0, inputs_n)])
circuit.append([cirq.H(output_qubit)])

#Add oracle
circuit, a = Add_Oracle(circuit, input_qubits, output_qubit, inputs_n)

#Apply hamaltonian across input qubits
circuit.append([cirq.H(input_qubits[i]) for i in range(0, inputs_n)])

#Measure all input qubits
circuit.append([cirq.measure(input_qubits[i]) for i in range(0, inputs_n)])

results = simulator.run(circuit, repetitions=1)
print(circuit)
print(a)
print(results)


