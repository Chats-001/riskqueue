from __future__ import annotations

import pandas as pd

from riskqueue.features.behavioral import add_behavioral_features
from riskqueue.features.schema import MODEL_FEATURES, assert_leakage_safe
from riskqueue.features.static import add_static_features


def build_features(frame: pd.DataFrame) -> pd.DataFrame:
    assert_leakage_safe(MODEL_FEATURES)
    return add_static_features(add_behavioral_features(frame))
