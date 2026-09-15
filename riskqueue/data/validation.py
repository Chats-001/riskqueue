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
    if not np.isfinite(data["amount"].astype(float)).all() or (data["amount"] < 0).any():
        raise DataValidationError("amount must contain finite non-negative values")
    invalid_types = set(data["type"]).difference(TRANSACTION_TYPES)
    if invalid_types:
        raise DataValidationError(f"Invalid transaction types: {sorted(invalid_types)}")
    if not set(data["isFraud"].unique()).issubset({0, 1}):
        raise DataValidationError("isFraud must be binary")
    if (data["step"] < 0).any():
        raise DataValidationError("step must be non-negative")
    return data.sort_values(["step"], kind="stable").reset_index(drop=True)
