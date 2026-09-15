from __future__ import annotations

import numpy as np


def population_stability_index(reference, current, bins: int = 10) -> float:
    """Compute PSI with reference quantiles and numerical safeguards."""
    reference = np.asarray(reference, dtype=float)
    current = np.asarray(current, dtype=float)
    if len(reference) == 0 or len(current) == 0:
        raise ValueError("reference and current arrays must be non-empty")
    edges = np.unique(np.quantile(reference, np.linspace(0, 1, bins + 1)))
    if len(edges) < 2:
        return 0.0 if np.allclose(reference[0], current) else float("inf")
    edges[0], edges[-1] = -np.inf, np.inf
    ref_counts = np.histogram(reference, bins=edges)[0] / len(reference)
    cur_counts = np.histogram(current, bins=edges)[0] / len(current)
    ref_counts = np.clip(ref_counts, 1e-6, None)
    cur_counts = np.clip(cur_counts, 1e-6, None)
    return float(np.sum((cur_counts - ref_counts) * np.log(cur_counts / ref_counts)))


def drift_status(psi: float) -> str:
    if psi < 0.1:
        return "stable"
    if psi < 0.25:
        return "watch"
    return "shifted"
