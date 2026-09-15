import numpy as np
import pytest

from riskqueue.decisions.economics import (
    expected_loss,
    expected_review_value,
    realized_decision_cost,
)


def test_expected_loss_vector():
    np.testing.assert_allclose(expected_loss([0.1, 0.8], [100, 50]), [10, 40])


def test_review_value_subtracts_cost():
    np.testing.assert_allclose(expected_review_value([0.1, 0.8], [100, 50], 4), [6, 36])


def test_realized_cost_combines_reviews_and_misses():
    assert realized_decision_cost([1, 0, 1], [True, True, False], [100, 50, 25], 4) == 33


@pytest.mark.parametrize("fraction,expected", [(0.5, 10), (1.0, 20), (1.5, 30)])
def test_loss_fraction(fraction, expected):
    assert expected_loss(0.2, 100, fraction) == pytest.approx(expected)
