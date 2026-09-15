from __future__ import annotations

import math
from typing import Literal

from pydantic import BaseModel, Field, field_validator

TransactionType = Literal["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]


class Transaction(BaseModel):
    transaction_id: str = Field(min_length=1, max_length=120)
    step: int = Field(ge=0)
    type: TransactionType
    amount: float = Field(ge=0)
    nameOrig: str = Field(min_length=1, max_length=120)
    nameDest: str = Field(min_length=1, max_length=120)

    @field_validator("amount")
    @classmethod
    def amount_is_finite(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("amount must be finite")
        return value


class BatchRequest(BaseModel):
    transactions: list[Transaction] = Field(min_length=1, max_length=1000)


class ScoreResponse(BaseModel):
    transaction_id: str
    fraud_probability: float
    expected_loss: float
    risk_band: str
    decision: str
    model_version: str


class QueueRequest(BaseModel):
    transactions: list[Transaction] = Field(min_length=1, max_length=1000)
    capacity: int = Field(default=100, ge=1, le=1000)
    strategy: Literal["probability", "expected_loss", "expected_review_value"] = "expected_loss"
