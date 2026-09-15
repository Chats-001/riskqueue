import numpy as np
import pytest

from riskqueue.decisions.review_queue import build_review_queue, queue_metrics


def test_probability_ranking(transactions):
    q = build_review_queue(transactions, [0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6], 3, "probability")
    assert q.transaction_id.tolist() == ["t1", "t3", "t5"]
    assert q["rank"].tolist() == [1, 2, 3]


def test_expected_loss_changes_order(transactions):
    probs = np.array([0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2])
    probability = build_review_queue(transactions, probs, 1, "probability")
    exposure = build_review_queue(transactions, probs, 1, "expected_loss")
    assert probability.iloc[0].transaction_id == "t0"
    assert exposure.iloc[0].transaction_id == "t5"


def test_queue_metrics(transactions):
    q = build_review_queue(transactions, [0.1, 0.2, 0.95, 0.3, 0.2, 0.9, 0.1, 0.8], 2)
    metrics = queue_metrics(q, transactions)
    assert metrics["precision"] == 1
    assert metrics["fraud_recall"] == pytest.approx(2 / 3)
    assert metrics["fraud_amount_captured"] == 175


def test_zero_capacity(transactions):
    assert build_review_queue(transactions, np.zeros(len(transactions)), 0).empty


def test_bad_probability_length(transactions):
    with pytest.raises(ValueError, match="one probability"):
        build_review_queue(transactions, [0.1], 1)


def test_unknown_strategy(transactions):
    with pytest.raises(ValueError, match="Unknown"):
        build_review_queue(transactions, np.zeros(len(transactions)), 1, "magic")
