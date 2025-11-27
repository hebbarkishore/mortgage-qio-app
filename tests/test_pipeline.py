
from core.models import Loan
from core.pipeline import run_qio_single, run_greedy_single

def make_dummy_loans(n=30):
    loans = []
    for i in range(n):
        loans.append(
            Loan(
                id=str(i+1),
                rate=6.0 + (i % 5) * 0.1,
                fico=680 + (i % 40),
                ltv=70.0 + (i % 15),
                dti=35.0 + (i % 10),
                state="CA" if i % 3 == 0 else ("TX" if i % 3 == 1 else "FL"),
                balance=200000 + (i % 10) * 5000,
            )
        )
    return loans

def test_qio_and_greedy_run():
    loans = make_dummy_loans()
    q_pool, q_metrics, q_score = run_qio_single(loans)
    g_pool, g_metrics, g_score = run_greedy_single(loans)

    assert isinstance(q_pool, list)
    assert isinstance(g_pool, list)
    assert isinstance(q_metrics, dict)
    assert isinstance(g_metrics, dict)
