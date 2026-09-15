from __future__ import annotations

import numpy as np
import pandas as pd

from riskqueue.config import TRANSACTION_TYPES

REQUIRED_COLUMNS = {
    "step",
    "type",
    "amount",
    "nameOrig",
    "nameDest",
    "isFraud",
}


class DataValidationError(ValueError):
    """Raised when transaction data cannot be used safely."""


def _numeric_column(data: pd.DataFrame, column: str) -> pd.Series:
    """Return a finite numeric column or raise the public validation error."""
    try:
        values = pd.to_numeric(data[column], errors="raise")
        raw_values = values.to_numpy()
        if np.iscomplexobj(raw_values):
            raise ValueError
        numeric_values = raw_values.astype(float)
    except (TypeError, ValueError, OverflowError):
        raise DataValidationError(f"{column} must contain numeric values") from None
    if not np.isfinite(numeric_values).all():
        raise DataValidationError(f"{column} must contain finite numeric values")
    return values


def validate_transactions(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate the minimum PaySim-compatible contract and return a copy."""
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise DataValidationError(f"Missing columns: {', '.join(sorted(missing))}")
    data = frame.copy()
    if data.empty:
        raise DataValidationError("Dataset is empty")
    if data[list(REQUIRED_COLUMNS)].isnull().any().any():
        raise DataValidationError("Required columns contain null values")

    amount = _numeric_column(data, "amount")
    if (amount < 0).any():
        raise DataValidationError("amount must contain finite non-negative values")
    data["amount"] = amount.astype(float)

    step = _numeric_column(data, "step")
    if (step < 0).any() or (step % 1 != 0).any():
        raise DataValidationError("step must contain finite non-negative integers")
    if (step > np.iinfo(np.int64).max).any():
        raise DataValidationError("step exceeds the supported integer range")
    data["step"] = step.astype(np.int64)

    labels = _numeric_column(data, "isFraud")
    if not labels.isin([0, 1]).all():
        raise DataValidationError("isFraud must be binary")
    data["isFraud"] = labels.astype(np.int64)

    invalid_types = set(data["type"]).difference(TRANSACTION_TYPES)
    if invalid_types:
        raise DataValidationError(f"Invalid transaction types: {sorted(invalid_types)}")
    return data.sort_values(["step"], kind="stable").reset_index(drop=True)
