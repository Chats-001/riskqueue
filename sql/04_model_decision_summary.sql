-- Business question:
-- How do decision volumes and scores differ across deployed model versions?
SELECT
    mv.model_version,
    mv.algorithm,
    mv.average_precision AS training_average_precision,
    pe.decision,
    COUNT(*) AS decisions,
    AVG(pe.fraud_probability) AS mean_score,
    SUM(pe.amount * pe.fraud_probability) AS expected_exposure
FROM model_versions mv
JOIN prediction_events pe USING (model_version)
GROUP BY mv.model_version, mv.algorithm, mv.average_precision, pe.decision
ORDER BY mv.model_version, pe.decision;

