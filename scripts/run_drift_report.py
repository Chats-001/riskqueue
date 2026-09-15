from __future__ import annotations

import argparse

import pandas as pd

from riskqueue.monitoring.drift import drift_status, population_stability_index


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("reference_csv")
    parser.add_argument("current_csv")
    parser.add_argument("--columns", nargs="+", default=["amount"])
    args = parser.parse_args()
    reference, current = pd.read_csv(args.reference_csv), pd.read_csv(args.current_csv)
    for column in args.columns:
        psi = population_stability_index(reference[column], current[column])
        print(f"{column}: PSI={psi:.3f} ({drift_status(psi)})")


if __name__ == "__main__":
    main()
