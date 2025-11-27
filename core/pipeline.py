
from typing import List
import numpy as np

from .models import Loan
from .feature_engineering import engineer_features
from .qubo_builder import build_qubo, load_rules_config
from .qio_solver import quantum_inspired_solver
from .baseline_heuristic import greedy_heuristic
from .evaluation import compute_pool_metrics, compute_composite_score

def run_qio_single(loans: List[Loan]):
    prices = [l.rate for l in loans]  # simple proxy
    engineer_features(loans)
    Q = build_qubo(loans, prices)
    x = quantum_inspired_solver(Q)
    pool = [l for l, bit in zip(loans, x) if bit == 1]
    metrics = compute_pool_metrics(pool)
    score = compute_composite_score(metrics)
    return pool, metrics, score

def run_greedy_single(loans: List[Loan]):
    rules = load_rules_config()
    pool = greedy_heuristic(
        loans,
        pool_size_target=rules["pool_size_target"],
        min_fico=rules["credit_min"],
        max_ltv=rules["ltv_max"],
    )
    metrics = compute_pool_metrics(pool)
    score = compute_composite_score(metrics)
    return pool, metrics, score

def run_variance_experiment(loans: List[Loan]):
    rules = load_rules_config()
    runs = rules.get("runs_for_variance", 30)

    qio_scores = []
    greedy_scores = []

    for _ in range(runs):
        q_pool, q_metrics, q_score = run_qio_single(loans)
        g_pool, g_metrics, g_score = run_greedy_single(loans)
        if q_metrics and g_metrics:
            qio_scores.append(q_score)
            greedy_scores.append(g_score)

    def summarize(values):
        if not values:
            return {"mean": 0.0, "std": 0.0}
        arr = np.array(values)
        return {
            "mean": float(arr.mean()),
            "std": float(arr.std(ddof=1)) if len(arr) > 1 else 0.0,
        }

    return {
        "qio": summarize(qio_scores),
        "greedy": summarize(greedy_scores),
    }
