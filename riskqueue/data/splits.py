from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class TemporalSplit:
    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame


def temporal_split(
    frame: pd.DataFrame, train_fraction: float = 0.70, validation_fraction: float = 0.15
) -> TemporalSplit:
    """Split whole time steps so no timestamp is shared across partitions."""
    if train_fraction <= 0 or validation_fraction <= 0:
        raise ValueError("split fractions must be positive")
    if train_fraction + validation_fraction >= 1:
        raise ValueError("train + validation fractions must be below 1")
    steps = sorted(frame["step"].unique())
    if len(steps) < 3:
        raise ValueError("at least three distinct time steps are required")
    train_end = max(1, int(len(steps) * train_fraction))
    valid_end = max(train_end + 1, int(len(steps) * (train_fraction + validation_fraction)))
    valid_end = min(valid_end, len(steps) - 1)
    train_steps = set(steps[:train_end])
    valid_steps = set(steps[train_end:valid_end])
    test_steps = set(steps[valid_end:])
    split = TemporalSplit(
        frame[frame.step.isin(train_steps)].copy(),
        frame[frame.step.isin(valid_steps)].copy(),
        frame[frame.step.isin(test_steps)].copy(),
    )
    if not (
        split.train.step.max() < split.validation.step.min()
        and split.validation.step.max() < split.test.step.min()
    ):
        raise AssertionError("temporal partitions overlap")
    return split
