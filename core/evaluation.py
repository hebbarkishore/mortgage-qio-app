
import yaml
from pathlib import Path

from .models import Loan

def load_scoring_config(path: str = "config/scoring_config.yaml"):
    with open(Path(path), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def compute_pool_metrics(pool):
    total_balance = sum(l.balance for l in pool) or 0.0
    if total_balance == 0:
        return {}

    wac = sum(l.rate * l.balance for l in pool) / total_balance
    wa_fico = sum(l.fico * l.balance for l in pool) / total_balance
    wa_ltv = sum(l.ltv * l.balance for l in pool) / total_balance

    execution_value = total_balance * (wac / 100.0)
    risk_adjusted_return = wac - (wa_ltv / 100.0)
    prepayment_score = max(0.0, 1.0 - (wac / 10.0))
    servicing_cost_score = 1.0 / (1.0 + wa_ltv / 100.0)

    return {
        "WAC": wac,
        "WA_FICO": wa_fico,
        "WA_LTV": wa_ltv,
        "execution_value": execution_value,
        "risk_adjusted_return": risk_adjusted_return,
        "prepayment_score": prepayment_score,
        "servicing_cost_score": servicing_cost_score,
    }

def compute_composite_score(metrics):
    if not metrics:
        return 0.0
    weights = load_scoring_config()["weights"]
    return (
        weights["execution_value"]      * metrics["execution_value"] +
        weights["risk_adjusted_return"] * metrics["risk_adjusted_return"] +
        weights["prepayment"]           * metrics["prepayment_score"] +
        weights["servicing_cost"]       * metrics["servicing_cost_score"]
    )
