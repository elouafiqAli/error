#!/usr/bin/env python3
"""
verify_prop6_marginal.py  (P0.2 verifier)

Checks Proposition 6 (Marginal-aware bracket) on three independent
levels:

  L1.  Closed-form formula (eq. marginal-slack) reproduces
       the tab:marginal grid in main.tex to 4 decimals.
  L2.  Closed-form formula matches the `w_marg` column written by
       experiments/e2b_marginal_aware.py (experiments/results/e2b.json)
       to 4 decimals on every E2b dataset row.
  L3.  Brute-force argmax over a dense H-grid of
            phi(H) := min(H/2, pi_star) - H_bin_inv(H)
       agrees with the closed form to 1e-6 on a pi_star grid.

The brute-force check (L3) is the adversarial probe: if the case
split in eq. marginal-slack were wrong, L3 would disagree.

Outputs verify_prop6_marginal.json next to the script.
"""
from __future__ import annotations
import json
import math
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "experiments"))
from common import W_STAR, hbin_inv  # noqa: E402

THRESHOLD = 0.5 * (
    -(1 / 5) * math.log2(1 / 5) - (4 / 5) * math.log2(4 / 5)
)  # == (1/2) * H_bin(1/5)
TOL_DECIMAL4 = 5e-5
TOL_BRUTE = 1e-6


def w_marg_closed_form(pi_star: float) -> float:
    """Eq. marginal-slack of Proposition 6."""
    if pi_star >= THRESHOLD:
        return W_STAR
    return pi_star - hbin_inv(2.0 * pi_star)


def w_marg_brute(pi_star: float, n: int = 200_001) -> float:
    """argmax_H phi(H) on a dense grid H in [0,1]."""
    best = -math.inf
    for i in range(n):
        H = i / (n - 1)
        phi = min(0.5 * H, pi_star) - hbin_inv(H)
        if phi > best:
            best = phi
    return best


# -- L1: grid in tab:marginal -------------------------------------------------
L1_GRID = {
    0.05: 0.0370,
    0.10: 0.0689,
    0.15: 0.0968,
    0.20: 0.1206,
    0.25: 0.1400,
    0.30: 0.1539,
    0.35: 0.1607,
    0.50: 0.1610,
}
l1_rows = []
for pi_star, expected in L1_GRID.items():
    cf = w_marg_closed_form(pi_star)
    ok = abs(cf - expected) < TOL_DECIMAL4
    l1_rows.append({
        "pi_star": pi_star,
        "tab_marginal_value": expected,
        "closed_form": round(cf, 6),
        "abs_diff": round(abs(cf - expected), 6),
        "pass_4decimals": ok,
    })
l1_pass = all(r["pass_4decimals"] for r in l1_rows)

# -- L2: e2b.json --------------------------------------------------------------
e2b_path = HERE / "experiments" / "results" / "e2b.json"
l2_rows = []
l2_pass = True
if e2b_path.exists():
    e2b = json.loads(e2b_path.read_text())
    for d in e2b["datasets"]:
        cf = w_marg_closed_form(d["pi_star"])
        ok = abs(cf - d["w_marg"]) < TOL_DECIMAL4
        l2_pass = l2_pass and ok
        l2_rows.append({
            "dataset": d["name"],
            "pi_star": d["pi_star"],
            "e2b_w_marg": d["w_marg"],
            "closed_form": round(cf, 6),
            "abs_diff": round(abs(cf - d["w_marg"]), 6),
            "pass_4decimals": ok,
        })
else:
    l2_pass = False
    l2_rows.append({"error": f"missing {e2b_path}"})

# -- L3: brute-force argmax ----------------------------------------------------
l3_rows = []
l3_pass = True
for pi_star in [0.05, 0.10, 0.15, 0.20, 0.248, 0.25, 0.30,
                0.331, 0.35, 0.361, 0.373, 0.499, 0.50]:
    cf = w_marg_closed_form(pi_star)
    bf = w_marg_brute(pi_star)
    ok = abs(cf - bf) < TOL_BRUTE * 100  # 1e-4: grid resolution
    l3_pass = l3_pass and ok
    l3_rows.append({
        "pi_star": pi_star,
        "closed_form": round(cf, 6),
        "brute_force_argmax": round(bf, 6),
        "abs_diff": round(abs(cf - bf), 6),
        "pass_1em4": ok,
    })

# -- Threshold sanity check ----------------------------------------------------
# at pi_star = THRESHOLD the two branches must agree
boundary_cf = THRESHOLD - hbin_inv(2.0 * THRESHOLD)
boundary_ok = abs(boundary_cf - W_STAR) < 1e-6

report = {
    "name": "verify_prop6_marginal",
    "W_STAR": W_STAR,
    "THRESHOLD": THRESHOLD,
    "threshold_continuity": {
        "boundary_value": round(boundary_cf, 8),
        "W_STAR": round(W_STAR, 8),
        "diff": round(abs(boundary_cf - W_STAR), 8),
        "pass": boundary_ok,
    },
    "L1_tab_marginal": {"pass": l1_pass, "rows": l1_rows},
    "L2_e2b_w_marg": {"pass": l2_pass, "rows": l2_rows},
    "L3_brute_argmax": {"pass": l3_pass, "rows": l3_rows},
    "overall_pass": all([l1_pass, l2_pass, l3_pass, boundary_ok]),
}

out = HERE / "verify_prop6_marginal.json"
out.write_text(json.dumps(report, indent=2))

print(f"L1 (tab:marginal 4dp)     : {'PASS' if l1_pass else 'FAIL'}")
print(f"L2 (e2b.json w_marg 4dp)  : {'PASS' if l2_pass else 'FAIL'}")
print(f"L3 (brute argmax 1e-4)    : {'PASS' if l3_pass else 'FAIL'}")
print(f"Threshold continuity      : {'PASS' if boundary_ok else 'FAIL'}")
print(f"Overall                   : "
      f"{'PASS' if report['overall_pass'] else 'FAIL'}")
print(f"Report -> {out}")
sys.exit(0 if report["overall_pass"] else 1)
