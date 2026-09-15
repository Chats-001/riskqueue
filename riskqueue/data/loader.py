from __future__ import annotations

from pathlib import Path

import pandas as pd

from riskqueue.data.validation import validate_transactions


def load_paysim(path: str | Path, *, sample_rows: int | None = None) -> pd.DataFrame:
    """Load a PaySim CSV without silently changing its row order."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"PaySim file not found: {path}")
    frame = pd.read_csv(path, nrows=sample_rows)
    return validate_transactions(frame)
