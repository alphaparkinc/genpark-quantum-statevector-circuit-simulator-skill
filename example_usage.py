from client import QuantumStatevector

sim = QuantumStatevector(num_qubits=2)
sim.apply_hadamard(0)
sim.apply_cnot(0, 1)

probs = sim.get_probabilities()
print("Bell state probabilities (|00>, |01>, |10>, |11>):", probs)
