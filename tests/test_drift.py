import numpy as np
import pytest

from riskqueue.monitoring.drift import drift_status, population_stability_index


def test_identical_distributions_have_zero_psi():
    values = np.arange(100)
    assert population_stability_index(values, values) == pytest.approx(0)


def test_large_shift_is_detected():
    rng = np.random.default_rng(2)
    psi = population_stability_index(rng.normal(0, 1, 2000), rng.normal(3, 1, 2000))
    assert psi > 0.25
    assert drift_status(psi) == "shifted"


@pytest.mark.parametrize("psi,status", [(0.0, "stable"), (0.15, "watch"), (0.3, "shifted")])
def test_status_bands(psi, status):
    assert drift_status(psi) == status


def test_empty_input_rejected():
    with pytest.raises(ValueError):
        population_stability_index([], [1])
