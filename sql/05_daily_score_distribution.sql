-- Business question:
-- Is the daily risk-score distribution moving away from recent behavior?
WITH daily AS (
    SELECT
        created_at::date AS score_date,
        COUNT(*) AS scored,
        AVG(fraud_probability) AS mean_score,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fraud_probability) AS median_score,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY fraud_probability) AS score_p95
    FROM prediction_events
    GROUP BY 1
)
SELECT *,
       AVG(mean_score) OVER (ORDER BY score_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
           AS trailing_7d_mean_score
FROM daily
ORDER BY score_date;

