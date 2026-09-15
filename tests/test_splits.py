import pandas as pd
import pytest

from riskqueue.data.splits import temporal_split


def test_split_is_strictly_chronological(transactions):
    split = temporal_split(transactions, 0.5, 0.25)
    assert split.train.step.max() < split.validation.step.min()
    assert split.validation.step.max() < split.test.step.min()


def test_equal_steps_never_cross_partitions(transactions):
    duplicated = pd.concat(
        [transactions, transactions.assign(transaction_id=lambda x: "copy-" + x.transaction_id)]
    )
    split = temporal_split(duplicated, 0.5, 0.25)
    assert set(split.train.step).isdisjoint(split.validation.step)
    assert set(split.validation.step).isdisjoint(split.test.step)


@pytest.mark.parametrize("train,valid", [(0, 0.2), (0.7, 0), (0.9, 0.2)])
def test_bad_split_fractions(transactions, train, valid):
    with pytest.raises(ValueError):
        temporal_split(transactions, train, valid)


def test_too_few_steps(transactions):
    tiny = transactions.assign(step=1)
    with pytest.raises(ValueError, match="three"):
        temporal_split(tiny)
