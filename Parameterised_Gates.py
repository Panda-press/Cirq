import matplotlib.pyplot as plt
import sympy

import cirq
from sympy.solvers.diophantine import length

q0 = cirq.LineQubit(0)
circuit = cirq.Circuit()
simulator = cirq.Simulator()

angle = sympy.Symbol('angle')

circuit.append(cirq.XPowGate(exponent=angle)(q0))
circuit.append(cirq.measure(q0, key='z'))

sweep = cirq.Linspace(key = angle.name, start=0.0, stop=2.0, length=100)

results = simulator.run_sweep(circuit, sweep, repetitions=1000)

print(results)

angles = [x[0][1] for x in sweep.param_tuples()]
zeroes = [results[i].histogram(key='z')[0] / 1000 for i in range(len(results))]

plt.plot(angles, zeroes, '--', linewidth=3)

plt.ylabel("Frequency of 0 Measurements")
plt.xlabel("Exponent of X gate")
plt.grid()
plt.show()

