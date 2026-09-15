from __future__ import annotations

import numpy as np
import pandas as pd

from riskqueue.config import TRANSACTION_TYPES


def make_demo_transactions(rows: int = 12_000, seed: int = 42) -> pd.DataFrame:
    """Generate a deterministic mobile-money scenario for UI/testing—not PaySim."""
    rng = np.random.default_rng(seed)
    steps = np.sort(rng.integers(0, 360, rows))
    tx_types = rng.choice(TRANSACTION_TYPES, rows, p=[0.11, 0.24, 0.08, 0.43, 0.14])
    senders = rng.integers(0, max(600, rows // 8), rows)
    recipients = rng.integers(0, max(900, rows // 6), rows)
    amount = np.exp(rng.normal(4.7, 1.25, rows))
    amount *= np.where(np.isin(tx_types, ["TRANSFER", "CASH_OUT"]), 1.8, 0.75)
    risky_type = np.isin(tx_types, ["TRANSFER", "CASH_OUT"])
    night = np.isin(steps % 24, [0, 1, 2, 3, 4])
    high_amount = amount > np.quantile(amount, 0.90)
    new_pair_proxy = ((senders * 31 + recipients * 17) % 9) < 5
    # A few percent fraud: rare enough for PR-AUC, large enough for a stable small demo.
    logit = -5.35 + 1.65 * risky_type + 1.55 * high_amount + 0.75 * night + 0.7 * new_pair_proxy
    probability = 1 / (1 + np.exp(-logit))
    fraud = rng.binomial(1, probability)
    frame = pd.DataFrame(
        {
            "transaction_id": [f"demo-{i:06d}" for i in range(rows)],
            "step": steps,
            "type": tx_types,
            "amount": np.round(amount, 2),
            "nameOrig": [f"C{x:07d}" for x in senders],
            "nameDest": [f"M{x:07d}" for x in recipients],
            "isFraud": fraud,
            "isFlaggedFraud": ((amount > 200_000) & (tx_types == "TRANSFER")).astype(int),
        }
    )
    return frame
