#!/usr/bin/env python3
"""Re-aggregate Paper-A harvest snapshots into Paper-B headline numbers.

Reads:    eK.snapshot.json, e7.snapshot.json, e3e.snapshot.json
Writes:   harvest_aggregate.json
Cites by: main.md footnotes [^bk-eK], [^bk-e7], [^bk-e3e]

Pure post-processing of snapshots. No new training, no Paper-A
dependency at run time (snapshots are immutable copies).
"""
from __future__ import annotations
import json
import pathlib

HERE = pathlib.Path(__file__).parent


def harvest_eK() -> dict:
    """Independent τ-thresholded falsifier corroborating ρ_M = 1."""
    d = json.loads((HERE / "eK.snapshot.json").read_text())
    taus = d["taus"]
    sources = d["sources"]
    totals = {"falsified": 0, "verified": 0, "inconclusive": 0}
    by_tau = {tau: {"falsified": 0, "verified": 0, "inconclusive": 0} for tau in taus}
    for src, info in sources.items():
        for tau_str, counts in info["per_tau"].items():
            tau = float(tau_str)
            for k in totals:
                totals[k] += counts[k]
                by_tau[tau][k] += counts[k]
    # Headlines used by [^bk-eK]:
    headline = {
        "n_sources": len(sources),
        "tau_levels": taus,
        "totals_across_all_tau": totals,
        "by_tau": by_tau,
        "tau_010_E6_falsified": sources["e6"]["per_tau"]["0.10"]["falsified"],
        "tau_025_E3_verified": sources["e3"]["per_tau"]["0.25"]["verified"],
    }
    return headline


def harvest_e7() -> dict:
    """Real-data witness that the McDiarmid bound is strictly conservative."""
    d = json.loads((HERE / "e7.snapshot.json").read_text())
    rows = d["rows"]
    # ratio p95 / bound across all rows = empirical-vs-bound conservativeness
    ratios = [r["delta_p95"] / r["bound"] for r in rows]
    coverages = [r["coverage"] for r in rows]
    return {
        "dataset": d["dataset"],
        "m": d["m"],
        "alpha": d["delta_conf"],
        "n_subsample_grid": [r["n"] for r in rows],
        "all_coverage_ge_1_minus_alpha": min(coverages) >= 1.0 - d["delta_conf"],
        "min_coverage": min(coverages),
        "p95_over_bound_min": min(ratios),
        "p95_over_bound_max": max(ratios),
        "bound_over_p95_min": min(1.0 / r for r in ratios),
        "bound_over_p95_max": max(1.0 / r for r in ratios),
        "gates": d["gates"],
        # Cited by [^bk-e7]: typical conservativeness factor ≈ bound / p95
        "headline_bound_over_p95_geomean": (
            (max(1.0 / r for r in ratios) * min(1.0 / r for r in ratios)) ** 0.5
        ),
    }


def harvest_e3e() -> dict:
    """Honest looseness disclaimer for L11 on real graphs."""
    d = json.loads((HERE / "e3e.snapshot.json").read_text())
    summary = []
    worst_looseness = 0.0
    worst_row = None
    for row in d["results"]:
        for sweep in row["sweep"]:
            for L_minus_1, loose in enumerate(sweep["looseness"]):
                if loose is None:
                    continue
                if loose > worst_looseness:
                    worst_looseness = loose
                    worst_row = {
                        "dataset": row["dataset"],
                        "L": L_minus_1,
                        "delta_0_param": sweep["delta_0_param"],
                        "delta_0_propagated": sweep["delta_0"],
                        "observed_D": sweep["D"][L_minus_1],
                        "bound_delta_l": sweep["delta_l_bound"][L_minus_1],
                        "looseness": loose,
                    }
        summary.append({
            "dataset": row["dataset"],
            "n": row["n"],
            "Delta_max": row["Delta_max"],
            "L": row["L"],
            "d_hidden": row["d_hidden"],
            "K_cells": row["K_cells"],
            "L_op_per_round": row["L_op_per_round"],
            "predicted_unit_envelope": row["predicted_unit_envelope"],
        })
    # Bound never violated ⇔ for every (row, δ, L), observed_D ≤ delta_l_bound.
    bound_never_violated = True
    for row in d["results"]:
        for sweep in row["sweep"]:
            for D, B in zip(sweep["D"], sweep["delta_l_bound"]):
                if D > B + 1e-12:
                    bound_never_violated = False
    return {
        "n_datasets": len(d["results"]),
        "per_dataset_summary": summary,
        "bound_never_violated": bound_never_violated,
        "worst_looseness_row": worst_row,
        "worst_looseness_orders_of_magnitude": (
            round(worst_looseness, 0) if worst_looseness > 0 else None
        ),
    }


def main() -> None:
    out = {
        "snapshot_paper_a_sha": "e8763fe",
        "snapshot_date_utc": "2026-06-01",
        "eK": harvest_eK(),
        "e7": harvest_e7(),
        "e3e": harvest_e3e(),
    }
    out_path = HERE / "harvest_aggregate.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(out_path)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
