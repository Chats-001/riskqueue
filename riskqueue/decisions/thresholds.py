from __future__ import annotations

import numpy as np
from sklearn.metrics import f1_score

from riskqueue.decisions.economics import realized_decision_cost


def compare_thresholds(labels, probabilities, amounts, review_cost: float = 4.0):
    grid = np.unique(np.r_[np.linspace(0.01, 0.99, 99), 0.5])
    rows = []
    for threshold in grid:
        decisions = np.asarray(probabilities) >= threshold
        rows.append(
            {
                "threshold": float(threshold),
                "f1": float(f1_score(labels, decisions, zero_division=0)),
                "cost": realized_decision_cost(labels, decisions, amounts, review_cost),
                "reviews": int(decisions.sum()),
            }
        )
    return rows


def select_threshold(rows, objective: str = "cost") -> float:
    if objective == "cost":
        return min(rows, key=lambda x: (x["cost"], x["threshold"]))["threshold"]
    if objective == "f1":
        return max(rows, key=lambda x: (x["f1"], x["threshold"]))["threshold"]
    raise ValueError("objective must be 'cost' or 'f1'")
