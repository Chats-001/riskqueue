from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CostConfig:
    """Transparent, simulated operating assumptions."""

    manual_review_cost: float = 4.0
    fraud_loss_fraction: float = 1.0
    review_capacity_per_day: int = 750
    minimum_fraud_recall: float = 0.70


ROOT = Path(__file__).resolve().parents[1]
LEAKAGE_COLUMNS = {
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "isFlaggedFraud",
}
TRANSACTION_TYPES = ("CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER")
