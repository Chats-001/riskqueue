from __future__ import annotations

import pandas as pd


def add_static_features(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["hour"] = result["step"] % 24
    result["day_index"] = result["step"] // 24
    return result
