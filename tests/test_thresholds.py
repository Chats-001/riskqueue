import pytest

from riskqueue.decisions.thresholds import compare_thresholds, select_threshold


def test_threshold_comparison_contains_default():
    rows = compare_thresholds([0, 0, 1, 1], [0.1, 0.4, 0.6, 0.9], [1, 1, 10, 10])
    assert any(row["threshold"] == 0.5 for row in rows)


@pytest.mark.parametrize("objective", ["cost", "f1"])
def test_selected_threshold_is_valid(objective):
    rows = compare_thresholds([0, 0, 1, 1], [0.1, 0.4, 0.6, 0.9], [1, 1, 10, 10])
    assert 0 < select_threshold(rows, objective) < 1


def test_unknown_objective_rejected():
    with pytest.raises(ValueError):
        select_threshold([], "accuracy")
