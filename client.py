"""Full n-Qubit Statevector Quantum Simulator Engine.
100% Python Standard Library.
"""

import math

class QuantumStatevector:
    """Full n-qubit complex statevector quantum circuit simulator."""
    def __init__(self, num_qubits=2):
        self.num_qubits = num_qubits
        self.dim = 1 << num_qubits
        self.state = [complex(0, 0)] * self.dim
        self.state[0] = complex(1, 0)

    def apply_hadamard(self, target):
        inv_sqrt2 = 1.0 / math.sqrt(2)
        new_state = list(self.state)
        step = 1 << target
        for i in range(0, self.dim, step * 2):
            for j in range(step):
                i0 = i + j
                i1 = i + j + step
                v0 = self.state[i0]
                v1 = self.state[i1]
                new_state[i0] = (v0 + v1) * inv_sqrt2
                new_state[i1] = (v0 - v1) * inv_sqrt2
        self.state = new_state

    def apply_cnot(self, control, target):
        new_state = list(self.state)
        c_mask = 1 << control
        t_mask = 1 << target
        for i in range(self.dim):
            if (i & c_mask) and not (i & t_mask):
                pair = i | t_mask
                new_state[i], new_state[pair] = self.state[pair], self.state[i]
        self.state = new_state

    def get_probabilities(self):
        return [abs(a)**2 for a in self.state]
