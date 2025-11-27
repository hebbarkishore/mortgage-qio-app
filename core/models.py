
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Loan:
    id: str
    rate: float
    fico: int
    ltv: float
    dti: float
    state: str
    balance: float
    features: Dict[str, float] = field(default_factory=dict)
