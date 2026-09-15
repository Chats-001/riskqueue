from __future__ import annotations

import hashlib
import os

from fastapi import FastAPI

from riskqueue.api.schemas import BatchRequest, QueueRequest, ScoreResponse, Transaction

app = FastAPI(
    title="RiskQueue API",
    version="0.1.0",
    description="Auditable demo scoring and cost-aware analyst queue prioritization.",
)


def _demo_probability(tx: Transaction) -> float:
    """Stable demo scorer used only when a fitted artifact is unavailable."""
    risky_type = {"TRANSFER": 0.34, "CASH_OUT": 0.22}.get(tx.type, 0.03)
    amount_component = min(0.42, tx.amount / 100_000)
    hour_component = 0.08 if tx.step % 24 < 5 else 0.0
    jitter = int(hashlib.sha256(tx.transaction_id.encode()).hexdigest()[:4], 16) / 65535 * 0.04
    return min(0.99, 0.015 + risky_type + amount_component + hour_component + jitter)


def _score(tx: Transaction) -> ScoreResponse:
    probability = _demo_probability(tx)
    loss = probability * tx.amount
    band = (
        "critical"
        if probability >= 0.75
        else "high"
        if probability >= 0.4
        else "guarded"
        if probability >= 0.1
        else "low"
    )
    return ScoreResponse(
        transaction_id=tx.transaction_id,
        fraud_probability=round(probability, 6),
        expected_loss=round(loss, 2),
        risk_band=band,
        decision="review" if loss > 4 else "approve",
        model_version=os.getenv("MODEL_VERSION", "demo-policy-v1"),
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "model": os.getenv("MODEL_VERSION", "demo-policy-v1")}


@app.post("/v1/score", response_model=ScoreResponse)
def score(transaction: Transaction) -> ScoreResponse:
    return _score(transaction)


@app.post("/v1/score/batch", response_model=list[ScoreResponse])
def score_batch(request: BatchRequest) -> list[ScoreResponse]:
    return [_score(tx) for tx in request.transactions]


@app.post("/v1/review-queue")
def review_queue(request: QueueRequest) -> list[dict]:
    scored = [
        _score(tx).model_dump() | {"amount": tx.amount, "type": tx.type}
        for tx in request.transactions
    ]
    key = {
        "probability": "fraud_probability",
        "expected_loss": "expected_loss",
        "expected_review_value": "expected_loss",
    }[request.strategy]
    selected = sorted(scored, key=lambda row: (row[key], row["amount"]), reverse=True)[
        : request.capacity
    ]
    for rank, row in enumerate(selected, 1):
        row["rank"] = rank
        if request.strategy == "expected_review_value":
            row["priority_score"] = round(row["expected_loss"] - 4, 2)
        else:
            row["priority_score"] = row[key]
    return selected


@app.get("/v1/model/metrics")
def model_metrics() -> dict:
    return {
        "model_version": os.getenv("MODEL_VERSION", "demo-policy-v1"),
        "status": "demo",
        "notice": "Run scripts/run_demo.py or the PaySim training pipeline for measured metrics.",
    }
