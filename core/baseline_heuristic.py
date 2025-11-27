
from .models import Loan

def greedy_heuristic(loans, pool_size_target: int = 20, min_fico: int = 680, max_ltv: float = 80.0):
    filtered = [
        l for l in loans
        if l.fico >= min_fico and l.ltv <= max_ltv
    ]
    filtered.sort(key=lambda l: l.rate, reverse=True)
    return filtered[:pool_size_target]
