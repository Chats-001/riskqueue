from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def build_session_factory(url: str | None = None):
    database_url = url or os.getenv(
        "DATABASE_URL", "postgresql+psycopg://riskqueue:riskqueue@localhost:5432/riskqueue"
    )
    engine = create_engine(database_url, pool_pre_ping=True)
    return sessionmaker(bind=engine, expire_on_commit=False)
