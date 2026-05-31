#!/usr/bin/env python3
"""
verify_t1_float.py  —  Tier T1: floating-point spot-check
=========================================================

Purpose
-------
Quick, dependency-free smoke test of the two-sided Bayes-error bracket

       Hbin^{-1}( H(f | Π) )  ≤  ε*(Π)  ≤  ½ H(f | Π)              (B)

from "A Two-Sided Bayes-Error Bracket from Partition-Conditional
Entropy" (Theorem 1, Corollary 2).  T1 sits at the bottom of the
verification ladder

        T0  pen-and-paper proof          (main.tex)
    →   T1  float spot-check             (THIS FILE)
    →   T2  certified interval audit     (verify.jl)
    →   T3  symbolic / closed-form       (verify_t3_symbolic.py)
    →   T4  interval branch-and-bound    (future work)
    →   T5  Lean 4 / mathlib4 proof      (future work)

What T1 is good for
-------------------
* Fast feedback while editing the script that generates examples,
  partitions, or labels.
* A self-contained sanity check that anyone with Python 3 can run
  in one second, no Julia install required.
* Demonstrating, side-by-side with T2, the *gap* between heuristic
  numerical agreement and certified correctness.

What T1 is NOT good for
-----------------------
* T1 uses IEEE-754 double precision with NO rounding control.  The
  binary entropy  Hbin(p) = -p log2 p - (1-p) log2(1-p)  and its
  numerical inverse can be off by a few ULPs.  Near the saturating
  boundary  ε* = ε  with  P_C = ε  (the Feder witness, see
  Proposition 5 / §7), the lower inequality of (B) is sharp, and
  float round-off can flip the comparison either way.  T1 will
  therefore report rare "violations" that are NOT genuine
  counter-examples to (B) — they are floating-point noise.
* T1 uses an iterative bisection to invert Hbin, with no a-priori
  error bound.  T2 replaces it by  H ≤ Hbin(ε*)  evaluated as a
  rigorously rounded interval, which is the mathematically correct
  way to test "Hbin^{-1}(H) ≤ ε*" without ever computing Hbin^{-1}.

Reading T1 alongside T2 (verify.jl) is the clearest pedagogical
illustration of WHY certified numerics matter: T2's interval test
gives a yes/no with mathematical certainty, T1's float test does not.

CLI
---
    python3 verify_t1_float.py [N] [SEED]

defaults: N=1000, SEED=20260531  (same as verify.jl)
"""

import json
import math
import random
import sys
from pathlib import Path


# ----------------------------------------------------------------------
# Entropy primitives — IEEE-754 doubles, no rounding control (the point)
# ----------------------------------------------------------------------

def hbin(p: float) -> float:
    """Binary entropy in bits.  Endpoints handled exactly."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def hbin_inv(h: float, tol: float = 1e-15, max_iter: int = 200) -> float:
    """
    Inverse of  Hbin : [0, 1/2] → [0, 1]  by bisection.

    There is no closed form.  This is the canonical place where T1
    is weakest: the iterate has only float-double precision and no
    error bound, so equality cases (Π^F witness) are unreliable.
    """
    h = max(0.0, min(1.0, h))
    lo, hi = 0.0, 0.5
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        if hbin(mid) < h:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


# ----------------------------------------------------------------------
# Random partitions and labels — matched to the protocol of verify.jl
# ----------------------------------------------------------------------

def random_partition(rng: random.Random, n: int):
    """Random set partition of {0,…,n-1} into k ∈ {1,…,n} cells."""
    k = rng.randint(1, n)
    assign = [rng.randrange(k) for _ in range(n)]
    cells = [[i for i in range(n) if assign[i] == j] for j in range(k)]
    return [C for C in cells if C]


def random_label(rng: random.Random, n: int):
    """Random ±1 binary label vector of length n."""
    return [rng.randint(0, 1) for _ in range(n)]


def cell_stats(cells, label, n):
    """Return (q_C, P_C, e_C) as float lists for each cell C."""
    qs, Ps, es = [], [], []
    for C in cells:
        qs.append(len(C) / n)
        P = sum(label[i] for i in C) / len(C)
        Ps.append(P)
        es.append(min(P, 1.0 - P))
    return qs, Ps, es


# ----------------------------------------------------------------------
# The bracket audit
# ----------------------------------------------------------------------

def audit(cells, label, n):
    """
    Evaluate the two inequalities of (B) in pure float arithmetic.

    Returns a dict with fields used by the manifest writer downstream.
    A 'tol' parameter is folded into the comparisons to silence noise
    near saturation (see module docstring).  This is precisely the
    fudge-factor T2 makes unnecessary.
    """
    TOL = 1e-12
    qs, Ps, es = cell_stats(cells, label, n)
    eps_star = sum(q * e for q, e in zip(qs, es))
    H = sum(q * hbin(P) for q, P in zip(qs, Ps))

    upper_ok = eps_star <= 0.5 * H + TOL          # ε* ≤ ½ H
    lower_ok = hbin_inv(H) <= eps_star + TOL      # Hbin^{-1}(H) ≤ ε*

    return {
        "n": n,
        "m": len(cells),
        "eps_star": eps_star,
        "H": H,
        "Hbin_inv_H": hbin_inv(H),
        "upper_ok": upper_ok,
        "lower_ok": lower_ok,
        "upper_slack": 0.5 * H - eps_star,        # ≥ 0 expected
        "lower_slack": eps_star - hbin_inv(H),    # ≥ 0 expected
    }


# ----------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------

def main(N: int = 1000, seed: int = 20260531):
    rng = random.Random(seed)
    records = []
    violations = 0
    for _ in range(N):
        n = rng.randint(4, 32)
        cells = random_partition(rng, n)
        label = random_label(rng, n)
        v = audit(cells, label, n)
        records.append(v)
        if not (v["upper_ok"] and v["lower_ok"]):
            violations += 1

    summary = {
        "tier":              "T1 (float spot-check, NOT certified)",
        "samples":           N,
        "seed":              seed,
        "violations":        violations,
        "upper_passed":      all(v["upper_ok"] for v in records),
        "lower_passed":      all(v["lower_ok"] for v in records),
        "max_eps_star":      max(v["eps_star"]    for v in records),
        "max_upper_slack":   max(v["upper_slack"] for v in records),
        "max_lower_slack":   max(v["lower_slack"] for v in records),
        "min_upper_slack":   min(v["upper_slack"] for v in records),
        "min_lower_slack":   min(v["lower_slack"] for v in records),
        "caveat": ("Float arithmetic; use verify.jl (T2) for "
                   "rigorously certified verdicts."),
    }
    Path("verify_t1.json").write_text(json.dumps(summary, indent=2))

    print("verify_t1_float.py — T1 float spot-check (NOT certified)")
    print(f"  samples:          {N}")
    print(f"  violations:       {violations}  (T2 will be zero)")
    print(f"  max ε*:           {summary['max_eps_star']:.4f}")
    print(f"  max upper slack:  {summary['max_upper_slack']:.4f}  "
          f"(expected ≈ w* = 0.1610)")
    print(f"  max lower slack:  {summary['max_lower_slack']:.4f}")
    print(f"  manifest:         verify_t1.json")
    return summary


if __name__ == "__main__":
    N    = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20260531
    main(N, seed)
