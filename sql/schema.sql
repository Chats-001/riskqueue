CREATE TABLE model_versions (
    model_version VARCHAR(80) PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL,
    algorithm VARCHAR(120) NOT NULL,
    training_end_step INTEGER NOT NULL,
    average_precision DOUBLE PRECISION NOT NULL,
    roc_auc DOUBLE PRECISION NOT NULL,
    brier DOUBLE PRECISION NOT NULL,
    decision_threshold DOUBLE PRECISION NOT NULL,
    git_commit CHAR(40)
);

CREATE TABLE prediction_events (
    prediction_id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    transaction_id VARCHAR(120) NOT NULL,
    model_version VARCHAR(80) NOT NULL REFERENCES model_versions(model_version),
    step INTEGER NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    amount NUMERIC(18,2) NOT NULL CHECK (amount >= 0),
    fraud_probability DOUBLE PRECISION NOT NULL CHECK (fraud_probability BETWEEN 0 AND 1),
    risk_band VARCHAR(20) NOT NULL,
    review_priority_score DOUBLE PRECISION NOT NULL,
    decision VARCHAR(20) NOT NULL
);

CREATE TABLE review_queue (
    queue_id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    transaction_id VARCHAR(120) NOT NULL,
    queue_date DATE NOT NULL,
    rank INTEGER NOT NULL,
    expected_loss NUMERIC(18,2) NOT NULL,
    priority_score DOUBLE PRECISION NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    UNIQUE (queue_date, rank)
);

CREATE INDEX ix_prediction_events_created_at ON prediction_events(created_at);
CREATE INDEX ix_prediction_events_transaction_id ON prediction_events(transaction_id);
CREATE INDEX ix_review_queue_date_status ON review_queue(queue_date, status);

