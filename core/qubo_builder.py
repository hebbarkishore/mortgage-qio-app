
import numpy as np
import yaml
from pathlib import Path

from .models import Loan

def load_rules_config(path: str = "config/rules_config.yaml"):
    with open(Path(path), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def build_qubo(loans, prices):
    cfg = load_rules_config()
    N = len(loans)
    Q = np.zeros((N, N))

    for i in range(N):
        Q[i][i] -= prices[i]

    target = cfg["pool_size_target"]
    pen = cfg["size_penalty"]
    for i in range(N):
        Q[i][i] += pen
        for j in range(i + 1, N):
            Q[i][j] += 2 * pen

    for i, loan in enumerate(loans):
        if loan.fico < cfg["credit_min"]:
            Q[i][i] += cfg["credit_penalty"]
        if loan.ltv > cfg["ltv_max"]:
            Q[i][i] += cfg["ltv_penalty"]

    total_balance = sum(l.balance for l in loans) or 1.0
    geo_pen = cfg["geo_penalty"]
    for state, limit in cfg.get("geo_limits", {}).items():
        indices = [i for i, l in enumerate(loans) if l.state == state]
        if not indices:
            continue
        maxbal = total_balance * limit
        for i in indices:
            frac = loans[i].balance / maxbal if maxbal > 0 else 0
            if frac > 1.0:
                Q[i][i] += geo_pen * frac

    return Q
