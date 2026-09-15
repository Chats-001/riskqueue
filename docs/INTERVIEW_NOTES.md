# Interview notes

## Data science

- **Why PR-AUC?** It focuses on rare positive retrieval and exposes the precision analysts experience.
- **Why temporal validation?** Future transaction behavior must not inform an earlier operating decision.
- **What leakage was avoided?** Post-transaction balance fields, the existing rule output, future history, and same-hour row ordering.
- **Why two models?** Logistic regression is a readable sanity check; boosting tests whether nonlinear interactions improve ranking.
- **Why calibration?** Expected loss uses probability magnitude, not only rank.
- **Why does threshold matter?** A score estimates risk; costs and capacity determine action.

## ML engineering

- The fitted preprocessing and model pipeline is versioned with metrics and its selected threshold.
- Pydantic rejects invalid types, negative/non-finite amounts, missing identifiers, and batches over 1,000.
- PostgreSQL stores model metadata, prediction events, and ranked queue entries.
- Production online features would require a time-aware state store or feature service.
- PSI and distribution comparisons warn when inputs or scores shift.
- CI lints and runs focused synthetic tests without retraining PaySim.

## Analytics and consulting

- The system supports allocation of scarce investigation time.
- Capacity changes both fraud recall and fraud dollars captured.
- Loss fraction, review cost, and calibration drive modeled ROI.
- Probability ranking can underweight a lower-probability but much larger exposure.
- A manager can compare queue policies and adjust assumptions in the dashboard.

