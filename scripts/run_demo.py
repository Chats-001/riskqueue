from __future__ import annotations

import argparse
from pathlib import Path

from riskqueue.data.splits import temporal_split
from riskqueue.demo import make_demo_transactions
from riskqueue.features.pipeline import build_features
from riskqueue.modeling.train import train_boosted, train_logistic
from riskqueue.reporting import generate_report_artifacts


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate truthful, labeled demo results")
    parser.add_argument("--rows", type=int, default=12_000)
    parser.add_argument("--output", type=Path, default=Path("artifacts/figures"))
    args = parser.parse_args()
    frame = build_features(make_demo_transactions(args.rows))
    split = temporal_split(frame)
    models = [
        train_logistic(split.train, split.train.isFraud),
        train_boosted(split.train, split.train.isFraud),
    ]
    validation_probs = {m.name: m.predict_proba(split.validation) for m in models}
    test_probs = {m.name: m.predict_proba(split.test) for m in models}
    best = max(
        models,
        key=lambda m: __import__("sklearn.metrics").metrics.average_precision_score(
            split.validation.isFraud, validation_probs[m.name]
        ),
    )
    summary = generate_report_artifacts(
        split.test,
        test_probs,
        args.output,
        (
            split.validation.isFraud.to_numpy(),
            validation_probs[best.name],
            split.validation.amount.to_numpy(),
        ),
    )
    print(f"Generated report for {summary['transactions']:,} held-out demo transactions")
    print(f"Best demo model: {summary['best_model']}")


if __name__ == "__main__":
    main()
