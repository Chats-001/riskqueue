# Decision policy

A fraud probability is not a decision. RiskQueue makes the policy visible through three quantities:

```text
expected_loss = probability × transaction_amount × loss_fraction
expected_review_value = expected_loss − manual_review_cost
```

The default illustrative assumptions are a $4 review cost, 100% loss fraction, and 750 reviews per day. They are configurable and are not claimed to represent a bank.

The project compares a 0.50 threshold, the validation-set F1 optimum, the validation-set cost minimum, and a top-*k* capacity rule. Thresholds are selected on validation data and evaluated once on the final chronological test period. Queue policies compare probability, expected loss, and expected review value at capacities of 100, 250, 500, 750, and 1,000.

