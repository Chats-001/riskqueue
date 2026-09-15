-- Business question:
-- Which transaction types contribute the most expected fraud exposure?
SELECT
    transaction_type,
    COUNT(*) AS transactions,
    AVG(fraud_probability) AS average_score,
    SUM(amount * fraud_probability) AS expected_exposure,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY fraud_probability) AS score_p95
FROM prediction_events
GROUP BY transaction_type
ORDER BY expected_exposure DESC;

