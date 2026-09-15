-- Business question:
-- Which pending cases carry the most exposure, and how do they rank within each day?
WITH ranked AS (
    SELECT q.*,
           ROW_NUMBER() OVER (
               PARTITION BY queue_date
               ORDER BY expected_loss DESC, priority_score DESC
           ) AS exposure_rank
    FROM review_queue q
    WHERE status = 'pending'
)
SELECT queue_date, transaction_id, rank, exposure_rank, expected_loss, priority_score
FROM ranked
WHERE exposure_rank <= 25
ORDER BY queue_date DESC, exposure_rank;

