"""Outcome metrics: contribution shares (for 80/20 measurement), concentration,
and summary statistics across seeds."""
from __future__ import annotations

from typing import Dict, List, Sequence
import numpy as np


def topk_share(shares: Sequence[float], k: int) -> float:
    """Share of total contribution held by the top-k contributors.

    Used with k = ceil(sqrt(n)) as the Price's-law-flavored concentration
    metric (de Solla Price: ~sqrt(n) do half the work -- descriptive folklore
    with a true heavy-tail kernel; org-science-brief sec 5). We MEASURE it;
    we do not assume it.
    """
    s = np.asarray(shares, dtype=float)
    tot = s.sum()
    if tot <= 0:
        return 0.0
    return float(np.sort(s)[::-1][:k].sum() / tot)


def summarize(values: Sequence[float]) -> Dict[str, float]:
    v = np.asarray(values, dtype=float)
    return {"mean": float(np.mean(v)),
            "std": float(np.std(v, ddof=1)) if len(v) > 1 else 0.0,
            "n": len(v)}


def gini(shares: Sequence[float]) -> float:
    s = np.sort(np.asarray(shares, dtype=float))
    tot = s.sum()
    if tot <= 0 or len(s) == 0:
        return 0.0
    n = len(s)
    idx = np.arange(1, n + 1)
    return float((2 * (idx * s).sum() / (n * tot)) - (n + 1) / n)
