from fastapi.testclient import TestClient

from riskqueue.api.main import app

client = TestClient(app)


def transaction(**overrides):
    payload = {
        "transaction_id": "tx-1",
        "step": 2,
        "type": "TRANSFER",
        "amount": 2500.0,
        "nameOrig": "C1",
        "nameDest": "M1",
    }
    return payload | overrides


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_single_score_contract():
    response = client.post("/v1/score", json=transaction())
    assert response.status_code == 200
    assert 0 <= response.json()["fraud_probability"] <= 1
    assert response.json()["expected_loss"] >= 0


def test_negative_amount_rejected():
    assert client.post("/v1/score", json=transaction(amount=-1)).status_code == 422


def test_infinite_amount_rejected():
    assert client.post("/v1/score", json=transaction(amount="Infinity")).status_code == 422


def test_invalid_transaction_type_rejected():
    assert client.post("/v1/score", json=transaction(type="WIRE")).status_code == 422


def test_batch_limit_is_enforced():
    payload = {"transactions": [transaction(transaction_id=f"t-{i}") for i in range(1001)]}
    assert client.post("/v1/score/batch", json=payload).status_code == 422


def test_review_queue_is_ranked_and_capacity_limited():
    payload = {
        "transactions": [
            transaction(transaction_id="small", amount=10),
            transaction(transaction_id="large", amount=100_000),
        ],
        "capacity": 1,
        "strategy": "expected_loss",
    }
    result = client.post("/v1/review-queue", json=payload)
    assert result.status_code == 200
    assert result.json()[0]["transaction_id"] == "large"
    assert result.json()[0]["rank"] == 1
