#!/usr/bin/env python3
"""anchor_real_data.py — D.9: real-data empirical anchor for Paper B's
C-Sh (Shannon) instance.

Discipline mantra: zero new training. We reuse the JSON manifest from
Paper A's E3 WL-bracket experiment

    partition-sandwich-preprint/experiments/results/e3.json

which contains, for each of five real-world graph datasets and each
WL depth L = 0, 1, 2, ..., the population conditional entropy
H(f | Pi_L) and the Bayes error eps^*(Pi_L) computed on the dataset
itself (no model training; partition is the WL refinement).

Anchor contract. For every (dataset, depth) row we recompute the
C-Sh bracket from Paper B (verify_b_t1 primitives) and assert:

    1. lower_B = H_bin^{-1}(H)    <=    eps^*    (T3 lower, C-Sh)
    2. eps^*                       <=   H / 2    (T3 upper, C-Sh)
    3. lower_B  agrees with the JSON's stored 'lower' to <= 1e-6
    4. upper_B  agrees with the JSON's stored 'upper' to <= 1e-12

Conditions 1-2 are the substantive empirical claim ("the Paper B
bracket envelopes the real-data Bayes error on every (dataset, depth)
we have"). Conditions 3-4 are a cross-implementation sanity check
between Paper A's WL-bracket code (which produced e3.json) and
Paper B's verify_b_t1 primitives.

The C-Va (variance) and C-Pi (Pinsker) instances cannot be anchored
from e3.json because they require cell-level (q_C, P_C), which is
not stored. They remain anchored to synthetic / population MC at
audit/stress.json. This file is honest about that limitation.

Usage:
    python3 audit/anchor_real_data.py
    python3 audit/anchor_real_data.py --manifest audit/anchor_real_data.json

Exit code 0 iff every anchor row passes all four conditions.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
from typing import Any

# --- bring in Paper B's verified primitives -----------------------------------
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from verify_b_t1 import _h_bin, _h_bin_inv_on_lower_half  # noqa: E402

# --- Paper A E3 manifest ------------------------------------------------------
PAPER_A_E3 = (
    ROOT.parent / "partition-sandwich-preprint" / "experiments" / "results" / "e3.json"
)

# Tolerances (chosen against documented bisection depths)
TOL_LOWER = 1.0e-6     # bisection-vs-bisection on H_bin^{-1}
TOL_UPPER = 1.0e-12    # closed-form H/2 vs H/2
TOL_BRACKET = 1.0e-9   # eps^* must lie inside [lower, upper], modulo float noise


def _check_row(name: str, L: int, row: dict[str, float]) -> dict[str, Any]:
    H = float(row["H"])
    eps = float(row["eps_star"])
    json_lower = float(row["lower"])
    json_upper = float(row["upper"])
    n = int(row["n"])
    m = int(row["m"])

    # Recompute the C-Sh bracket independently with Paper B primitives.
    lower_B = _h_bin_inv_on_lower_half(H)
    upper_B = 0.5 * H

    cond1 = lower_B <= eps + TOL_BRACKET
    cond2 = eps <= upper_B + TOL_BRACKET
    cond3 = abs(lower_B - json_lower) <= TOL_LOWER
    cond4 = abs(upper_B - json_upper) <= TOL_UPPER

    status = "pass" if (cond1 and cond2 and cond3 and cond4) else "fail"
    return {
        "dataset": name,
        "L": L,
        "n": n,
        "m": m,
        "H": H,
        "eps_star": eps,
        "lower_paperA_json": json_lower,
        "upper_paperA_json": json_upper,
        "lower_paperB_recomputed": lower_B,
        "upper_paperB_recomputed": 0.5 * H,
        "abs_diff_lower": abs(lower_B - json_lower),
        "abs_diff_upper": abs(upper_B - json_upper),
        "T3_lower_envelope_ok": cond1,
        "T3_upper_envelope_ok": cond2,
        "cross_impl_lower_ok": cond3,
        "cross_impl_upper_ok": cond4,
        "status": status,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--source",
        default=str(PAPER_A_E3),
        help="Path to Paper A's e3.json (default: %(default)s)",
    )
    ap.add_argument(
        "--manifest",
        default=str(HERE / "anchor_real_data.json"),
        help="Output JSON manifest path",
    )
    args = ap.parse_args(argv)

    src = pathlib.Path(args.source)
    if not src.is_file():
        print(f"ERROR: Paper A e3 manifest not found at {src}", file=sys.stderr)
        return 2

    paperA = json.loads(src.read_text())
    rows: list[dict[str, Any]] = []
    for dset in paperA.get("datasets", []):
        name = dset.get("name", "?")
        for depth in dset.get("depths", []):
            L = int(depth.get("L", -1))
            rows.append(_check_row(name, L, depth))

    n_total = len(rows)
    n_fail = sum(1 for r in rows if r["status"] != "pass")
    worst_dlow = max((r["abs_diff_lower"] for r in rows), default=0.0)
    worst_dup = max((r["abs_diff_upper"] for r in rows), default=0.0)

    manifest = {
        "experiment": "D.9 real-data empirical anchor (Paper B C-Sh instance)",
        "source": str(src),
        "n_dataset_rows": n_total,
        "n_failures": n_fail,
        "worst_abs_diff_lower": worst_dlow,
        "worst_abs_diff_upper": worst_dup,
        "tolerances": {
            "TOL_LOWER": TOL_LOWER,
            "TOL_UPPER": TOL_UPPER,
            "TOL_BRACKET": TOL_BRACKET,
        },
        "datasets_seen": sorted({r["dataset"] for r in rows}),
        "rows": rows,
        "all_pass": n_fail == 0,
    }

    out = pathlib.Path(args.manifest)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2))

    # Pretty summary.
    print(f"=== D.9 real-data anchor (source: {src.name}) ===")
    print(f"  datasets seen : {manifest['datasets_seen']}")
    print(f"  rows checked  : {n_total}")
    print(f"  failures      : {n_fail}")
    print(f"  worst |dlow|  : {worst_dlow:.3e}  (tol {TOL_LOWER:.0e})")
    print(f"  worst |dup|   : {worst_dup:.3e}  (tol {TOL_UPPER:.0e})")
    print(f"  manifest      : {out}")
    if n_fail == 0:
        print("OVERALL: PASS")
        return 0
    print("OVERALL: FAIL")
    for r in rows:
        if r["status"] != "pass":
            print(
                f"  FAIL {r['dataset']} L={r['L']}: "
                f"H={r['H']:.4f} eps*={r['eps_star']:.4f} "
                f"lo_B={r['lower_paperB_recomputed']:.6f} up_B={r['upper_paperB_recomputed']:.6f} "
                f"(cond1={r['T3_lower_envelope_ok']} cond2={r['T3_upper_envelope_ok']} "
                f"cond3={r['cross_impl_lower_ok']} cond4={r['cross_impl_upper_ok']})"
            )
    return 1


if __name__ == "__main__":
    sys.exit(main())
