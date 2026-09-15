# Data setup

RiskQueue is designed for **PaySim — Synthetic Financial Datasets for Fraud Detection**, introduced by E. A. Lopez-Rojas, A. Elmir, and S. Axelsson in “PaySim: A financial mobile money simulator for fraud detection” (EMSS 2016).

- Source: [Kaggle dataset page](https://www.kaggle.com/datasets/ealaxi/paysim1)
- Expected file: `data/raw/PS_20174392719_1491204439457_log.csv`
- License: refer to the dataset publisher’s current terms on the source page.
- Repository policy: the full dataset is never committed.

Place the CSV at the expected path, then run:

```bash
python scripts/validate_data.py data/raw/PS_20174392719_1491204439457_log.csv
python scripts/train_model.py data/raw/PS_20174392719_1491204439457_log.csv
```

For a quick interface check without downloading PaySim, `python scripts/run_demo.py` generates a deterministic synthetic scenario. Its results are labeled **demo** and must not be represented as PaySim findings.

