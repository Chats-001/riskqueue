from __future__ import annotations

import argparse

from riskqueue.data.loader import load_paysim


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv")
    parser.add_argument("--sample-rows", type=int)
    args = parser.parse_args()
    frame = load_paysim(args.csv, sample_rows=args.sample_rows)
    print(f"Validated {len(frame):,} transactions across {frame.step.nunique():,} time steps")
    print(f"Fraud cases: {frame.isFraud.sum():,} ({frame.isFraud.mean():.4%})")


if __name__ == "__main__":
    main()
