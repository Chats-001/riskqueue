from __future__ import annotations

import numpy as np


def expected_loss(probability, amount, loss_fraction: float = 1.0):
    return np.asarray(probability, dtype=float) * np.asarray(amount, dtype=float) * loss_fraction


def expected_review_value(
    probability, amount, manual_review_cost: float = 4.0, loss_fraction: float = 1.0
):
    return expected_loss(probability, amount, loss_fraction) - manual_review_cost


def realized_decision_cost(
    labels, decisions, amounts, manual_review_cost: float = 4.0, loss_fraction: float = 1.0
) -> float:
    labels = np.asarray(labels, dtype=int)
    decisions = np.asarray(decisions, dtype=bool)
    amounts = np.asarray(amounts, dtype=float)
    review_cost = decisions.sum() * manual_review_cost
    missed_loss = amounts[(labels == 1) & ~decisions].sum() * loss_fraction
    return float(review_cost + missed_loss)
