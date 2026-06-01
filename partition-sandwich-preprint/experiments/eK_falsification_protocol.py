"""E-K: Kochenderfer-style falsification / verification protocol.

For each row in existing E1, E2, E6 results we already have the bracket
``[lower, upper]`` on the partition-induced Bayes-error proxy. For a list
of nominal target Bayes-error thresholds ``tau`` we classify the claim
"``eps* <= tau``" as:

  - FALSIFIED   if  tau < lower   (the bracket forbids it)
  - VERIFIED    if  tau >= upper  (the bracket guarantees it)
  - INCONCLUSIVE otherwise

Aggregated counts (falsified, verified, inconclusive) per source and per
threshold are written to ``results/eK.json`` and a markdown table is
appended to ``REPORTS.md``-style stdout.

Zero new training. Pure post-processing of existing JSON outputs.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"

SOURCES = ["e1", "e2", "e3", "e6"]
TAUS = [0.10, 0.15, 0.20, 0.25]


def classify(lower: float, upper: float, tau: float) -> str:
    if tau < lower:
        return "falsified"
    if tau >= upper:
        return "verified"
    return "inconclusive"


def iter_rows(path: Path) -> Iterable[dict]:
    with path.open() as fh:
        blob = json.load(fh)
    # Flat schema: top-level 'rows' list of dicts with 'lower'/'upper'.
    for r in blob.get("rows", []):
        if "lower" in r and "upper" in r:
            yield r
    # Nested schema (e3): top-level 'datasets' list, each with 'depths'.
    for ds in blob.get("datasets", []):
        for r in ds.get("depths", []):
            if "lower" in r and "upper" in r:
                yield r


def main() -> int:
    summary = {"taus": TAUS, "sources": {}}
    for src in SOURCES:
        path = RESULTS / f"{src}.json"
        if not path.exists():
            print(f"skip {src}: {path} not found", file=sys.stderr)
            continue
        rows = list(iter_rows(path))
        per_tau = {}
        for tau in TAUS:
            counts = {"falsified": 0, "verified": 0, "inconclusive": 0}
            for r in rows:
                counts[classify(r["lower"], r["upper"], tau)] += 1
            per_tau[f"{tau:.2f}"] = counts
        summary["sources"][src] = {"n_rows": len(rows), "per_tau": per_tau}

    out = RESULTS / "eK.json"
    out.write_text(json.dumps(summary, indent=2))
    print(f"wrote {out}")

    # Markdown summary table.
    print()
    print("| source | n | tau | falsified | verified | inconclusive |")
    print("|--------|---|-----|-----------|----------|--------------|")
    for src, blob in summary["sources"].items():
        n = blob["n_rows"]
        for tau_str, counts in blob["per_tau"].items():
            print(
                f"| {src} | {n} | {tau_str} | "
                f"{counts['falsified']} | {counts['verified']} | "
                f"{counts['inconclusive']} |"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
