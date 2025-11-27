
import yaml
from pathlib import Path

from .models import Loan

def load_feature_config(path: str = "config/feature_config.yaml"):
    with open(Path(path), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def engineer_features(loans):
    cfg = load_feature_config()

    for loan in loans:
        features = {}

        features["rate_spread"] = loan.rate - cfg["benchmark_rate"]

        features["fico_band"] = 0
        for band in cfg["fico_bands"]:
            if band["min"] <= loan.fico <= band["max"]:
                features["fico_band"] = band["bucket"]
                break

        features["ltv_bucket"] = 0
        for bucket in cfg["ltv_buckets"]:
            if bucket["min"] <= loan.ltv <= bucket["max"]:
                features["ltv_bucket"] = bucket["bucket"]
                break

        hr = cfg["high_risk_rules"]
        high_risk_conditions = [
            loan.fico < hr["fico_min_threshold"],
            loan.ltv > hr["ltv_max_threshold"],
            loan.dti > hr["dti_max_threshold"],
        ]
        features["high_risk_flag"] = 1 if any(high_risk_conditions) else 0

        loan.features = features
