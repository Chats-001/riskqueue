from __future__ import annotations

import numpy as np
import pandas as pd

from riskqueue.decisions.economics import expected_loss, expected_review_value


def build_review_queue(
    frame: pd.DataFrame,
    probabilities,
    capacity: int,
    strategy: str = "expected_loss",
    manual_review_cost: float = 4.0,
    loss_fraction: float = 1.0,
) -> pd.DataFrame:
    if capacity < 0:
        raise ValueError("capacity must be non-negative")
    if len(frame) != len(probabilities):
        raise ValueError("one probability is required per transaction")
    queue = frame.copy()
    queue["fraud_probability"] = np.asarray(probabilities, dtype=float)
    queue["expected_loss"] = expected_loss(probabilities, queue.amount, loss_fraction)
    queue["expected_review_value"] = expected_review_value(
        probabilities, queue.amount, manual_review_cost, loss_fraction
    )
    score_columns = {
        "probability": "fraud_probability",
        "expected_loss": "expected_loss",
        "expected_review_value": "expected_review_value",
    }
    if strategy not in score_columns:
        raise ValueError(f"Unknown strategy: {strategy}")
    score = score_columns[strategy]
    queue = queue.sort_values([score, "amount"], ascending=False, kind="stable").head(capacity)
    queue["rank"] = np.arange(1, len(queue) + 1)
    queue["priority_score"] = queue[score]
    queue["risk_band"] = pd.cut(
        queue.fraud_probability,
        bins=[-np.inf, 0.1, 0.4, 0.75, np.inf],
        labels=["low", "guarded", "high", "critical"],
    ).astype(str)
    return queue


def queue_metrics(queue: pd.DataFrame, full_frame: pd.DataFrame) -> dict[str, float]:
    fraud_mask = queue.get("isFraud", pd.Series(0, index=queue.index)).astype(bool)
    total_fraud = float(full_frame.isFraud.sum())
    total_fraud_amount = float(full_frame.loc[full_frame.isFraud == 1, "amount"].sum())
    captured = float(queue.loc[fraud_mask, "amount"].sum())
    return {
        "reviews": float(len(queue)),
        "precision": float(fraud_mask.mean()) if len(queue) else 0.0,
        "fraud_recall": float(fraud_mask.sum() / total_fraud) if total_fraud else 0.0,
        "fraud_amount_captured": captured,
        "fraud_value_capture": captured / total_fraud_amount if total_fraud_amount else 0.0,
    }
