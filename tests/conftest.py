import pandas as pd
import pytest


@pytest.fixture
def transactions():
    return pd.DataFrame(
        {
            "transaction_id": [f"t{i}" for i in range(8)],
            "step": [0, 1, 2, 3, 4, 5, 6, 7],
            "type": [
                "PAYMENT",
                "TRANSFER",
                "CASH_OUT",
                "PAYMENT",
                "DEBIT",
                "TRANSFER",
                "CASH_IN",
                "CASH_OUT",
            ],
            "amount": [10.0, 20.0, 50.0, 30.0, 8.0, 100.0, 15.0, 75.0],
            "nameOrig": ["A", "A", "B", "A", "C", "A", "D", "B"],
            "nameDest": ["X", "Y", "X", "X", "Z", "Y", "X", "Y"],
            "isFraud": [0, 0, 1, 0, 0, 1, 0, 1],
        }
    )
