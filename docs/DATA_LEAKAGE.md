# Data leakage controls

Leakage occurs when a model receives information that would not safely exist at decision time. It can produce excellent-looking metrics that collapse in actual use.

RiskQueue excludes `oldbalanceOrg`, `newbalanceOrig`, `oldbalanceDest`, `newbalanceDest`, and `isFlaggedFraud` from the final model. Balance fields can encode post-transaction accounting relationships; `isFlaggedFraud` is an existing rule outcome and is retained only for baseline comparison. The central feature list raises an error if any excluded column is added.

Behavioral features are computed chronologically. A row’s state is updated only after its features are calculated. Transactions sharing an hour see state frozen at the beginning of that hour, so arbitrary row ordering cannot create same-hour peeking. Hand-written tests append extreme future transactions and confirm every earlier feature remains unchanged.

