import pandas as pd
import pytest

from riskqueue.features.behavioral import add_behavioral_features
from riskqueue.features.pipeline import build_features
from riskqueue.features.schema import MODEL_FEATURES, assert_leakage_safe


def test_hand_calculated_history(transactions):
    result = build_features(transactions)
    a_at_step_3 = result[result.transaction_id == "t3"].iloc[0]
    assert a_at_step_3.sender_count_1h == 0
    assert a_at_step_3.sender_count_6h == 2
    assert a_at_step_3.sender_total_amount_24h == 30
    assert a_at_step_3.sender_historical_median_amount == 15
    assert a_at_step_3.sender_unique_recipients_24h == 2
    assert a_at_step_3.sender_hours_since_prior == 2
    assert a_at_step_3.prior_pair_count == 1
    assert a_at_step_3.first_time_recipient == 0


def test_recipient_history_is_correct(transactions):
    result = build_features(transactions)
    row = result[result.transaction_id == "t6"].iloc[0]
    assert row.recipient_incoming_count_24h == 3
    assert row.recipient_unique_senders_24h == 2
    assert row.recipient_total_received_24h == 90


def test_future_append_does_not_change_past(transactions):
    original = build_features(transactions)
    future = transactions.iloc[-1:].copy()
    future["transaction_id"] = "future"
    future["step"] = 100
    future["amount"] = 99_999_999
    expanded = build_features(pd.concat([transactions, future], ignore_index=True))
    pd.testing.assert_frame_equal(
        original[MODEL_FEATURES], expanded.iloc[: len(original)][MODEL_FEATURES]
    )


def test_equal_hour_rows_do_not_see_one_another():
    frame = pd.DataFrame(
        {
            "transaction_id": ["a", "b"],
            "step": [1, 1],
            "type": ["PAYMENT", "PAYMENT"],
            "amount": [10.0, 20.0],
            "nameOrig": ["S", "S"],
            "nameDest": ["X", "Y"],
            "isFraud": [0, 0],
        }
    )
    result = add_behavioral_features(frame)
    assert result.sender_count_1h.tolist() == [0, 0]


def test_leakage_columns_are_rejected():
    with pytest.raises(ValueError, match="Leakage-prone"):
        assert_leakage_safe(["amount", "isFlaggedFraud"])


def test_model_schema_is_leakage_safe():
    assert_leakage_safe(MODEL_FEATURES)
