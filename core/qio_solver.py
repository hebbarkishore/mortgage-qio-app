
import numpy as np
import math
import random

from .qubo_builder import load_rules_config

def energy(Q, x):
    return float(x.T @ Q @ x)

def quantum_inspired_solver(Q):
    cfg = load_rules_config()
    iterations = cfg.get("iterations", 300)

    N = Q.shape[0]
    x = np.random.randint(0, 2, size=N)
    curr_E = energy(Q, x)

    T0, T1 = 5.0, 0.1

    for t in range(iterations):
        T = T0 + (T1 - T0) * (t / max(iterations, 1))
        i = random.randint(0, N - 1)
        x_new = x.copy()
        x_new[i] = 1 - x_new[i]

        E_new = energy(Q, x_new)
        dE = E_new - curr_E

        if dE < 0 or random.random() < math.exp(-dE / max(T, 1e-6)):
            x = x_new
            curr_E = E_new

    return x
