# Model card

## Intended use

Educational and portfolio fraud-operations decision support on synthetic transaction data.

## Not intended for

Actual banking, law-enforcement, credit, eligibility, or consumer financial decisions.

## Data and target

The production workflow targets PaySim and predicts `isFraud`. The checked-in visuals are generated from a separate deterministic demo scenario unless explicitly regenerated from PaySim.

## Validation and metrics

The primary evaluation is a 70/15/15 chronological split. Average precision is primary because fraud is rare and accuracy would hide poor minority-class retrieval. ROC-AUC, Brier score, log loss, precision, recall, F1, fraud dollars captured, and modeled decision cost provide complementary views.

## Decision policy

Review rankings use calibrated probability and transaction exposure. Costs and analyst capacity are simulated, configurable assumptions.

## Limitations

- PaySim is synthetic and cannot establish real-world effectiveness.
- No demographic, device, network, merchant, or account context is available.
- Historical features are batch-computed rather than maintained online.
- Review cost, loss fraction, capacity, and drift thresholds are illustrative.
- A distribution shift is a warning, not evidence of degraded model quality.
- Model contribution values are associations, not causal explanations.

