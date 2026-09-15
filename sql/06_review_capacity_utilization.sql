-- Business question:
-- Are daily queues filling the configured 750-case capacity, and what exposure is selected?
WITH queue_daily AS (
    SELECT
        queue_date,
        COUNT(*) AS queued,
        COUNT(*) FILTER (WHERE status = 'completed') AS completed,
        SUM(expected_loss) AS selected_expected_loss
    FROM review_queue
    GROUP BY queue_date
)
SELECT
    queue_date,
    queued,
    completed,
    queued / 750.0 AS capacity_utilization,
    completed::numeric / NULLIF(queued, 0) AS completion_rate,
    selected_expected_loss
FROM queue_daily
ORDER BY queue_date DESC;

