from riskqueue.modeling.evaluate import classification_metrics


def test_perfect_ranking_metrics():
    result = classification_metrics([0, 0, 1, 1], [0.01, 0.1, 0.9, 0.99])
    assert result["average_precision"] == 1
    assert result["roc_auc"] == 1
    assert result["f1"] == 1


def test_metric_keys():
    result = classification_metrics([0, 1], [0.2, 0.8])
    assert set(result) == {
        "average_precision",
        "roc_auc",
        "brier",
        "log_loss",
        "precision",
        "recall",
        "f1",
    }
