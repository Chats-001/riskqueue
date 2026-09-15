from __future__ import annotations

from datetime import UTC, datetime

from riskqueue.db.models import PredictionEvent


def log_prediction(session, payload: dict) -> PredictionEvent:
    event = PredictionEvent(created_at=datetime.now(UTC), **payload)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event
