-- Business question:
-- How many transactions were reviewed each day, and how did their risk mix change?
WITH daily AS (
    SELECT
        created_at::date AS score_date,
        COUNT(*) FILTER (WHERE decision = 'review') AS reviews,
        COUNT(*) FILTER (WHERE decision = 'review' AND risk_band = 'critical') AS critical_reviews,
        AVG(fraud_probability) FILTER (WHERE decision = 'review') AS mean_review_score
    FROM prediction_events
    GROUP BY 1
)
SELECT *,
       critical_reviews::numeric / NULLIF(reviews, 0) AS critical_share
FROM daily
ORDER BY score_date;

