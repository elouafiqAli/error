#!/usr/bin/env python3
"""
verify_t4_population.py  —  Tier T4: Monte-Carlo population concentration
=========================================================================

Purpose
-------
T4 (population concentration) sits between T2 (per-sample certified)
and the future T5 (interval branch-and-bound) in the verification
ladder, and is the empirical counterpart to Proposition 7
("Population extension") of the paper:

    T0  pen-and-paper proof          (main.tex)
    T1  float spot-check             (verify_t1_float.py)
    T2  certified per-sample audit   (verify.jl)
    T3  symbolic / closed-form       (verify_t3_symbolic.py)
→   T4  Monte-Carlo population test  (THIS FILE)
    T5  interval branch-and-bound    (future work)
    T6  Lean 4 / mathlib4 proof      (future work)

What T4 verifies
----------------
Proposition 7 of the paper claims that, under i.i.d. sampling
V = (v_1, …, v_n) from a distribution μ with cell masses
μ(C) ≥ δ > 0 and cell means π_C ∈ [η, 1-η], the empirical
quantities (ε*_Π, H(f|Π)) computed on V are within an additive
O(√(log m / n)) of their population counterparts (ε*_{Π,μ},
H_μ(f|Π)) with high probability.  Concretely, with probability
≥ 1 - δ_conf,

    |ε*_{Π,μ} - ε*_Π| + |H_μ(f|Π) - H(f|Π)|
        ≤ κ(δ, η) · √( log(4m / δ_conf) / n )

where κ(δ, η) = (1 + log_2((1-η)/η)) / √δ.

T4 runs a Monte-Carlo experiment that:
  1. fixes a finite population partition Π with m cells of
     population masses μ ≥ δ and cell means π in [η, 1-η];
  2. for each subsample size n in a logarithmic grid, draws K
     i.i.d. subsamples V of size n;
  3. computes the empirical bracket on V and the gap
       Δ_n := |ε*_pop - ε*_emp| + |H_pop - H_emp|;
  4. compares the empirical CDF of Δ_n to the analytic bound
     κ · √(log(4m / δ_conf) / n).  T4 asserts that the empirical
     coverage rate is at least 1 - δ_conf for every n.

Dependencies
------------
Python 3 + numpy only.  (Optional: scipy.special only used for
log; we use math.log instead.)

    pip install numpy

CLI
---
    python3 verify_t4_population.py
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np


# ----------------------------------------------------------------------
# 1. Primitives
# ----------------------------------------------------------------------

LOG2 = math.log(2.0)


def Hbin(p: float) -> float:
    """Binary entropy in bits, with endpoint convention Hbin(0)=Hbin(1)=0."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * math.log(p) + (1.0 - p) * math.log(1.0 - p)) / LOG2


def empirical_bracket_quantities(samples_per_cell):
    """
    Given a list of arrays `samples_per_cell` where each array holds the
    Bernoulli labels of vertices that fell into cell C, return the
    triple (eps_star, H_cond, q_cells) of the empirical
    partition-restricted minimum risk, conditional entropy, and
    empirical cell masses.

    Cells with zero samples are dropped from the entropy and risk
    sums (they contribute mass 0 to the average).
    """
    n_total = sum(len(arr) for arr in samples_per_cell)
    if n_total == 0:
        return 0.0, 0.0, []
    eps_star = 0.0
    H_cond   = 0.0
    qs = []
    for arr in samples_per_cell:
        sz = len(arr)
        if sz == 0:
            qs.append(0.0)
            continue
        q = sz / n_total
        P = float(arr.mean())
        eps_star += q * min(P, 1.0 - P)
        H_cond   += q * Hbin(P)
        qs.append(q)
    return eps_star, H_cond, qs


def population_bracket_quantities(mu, pi):
    """Population analogues from cell masses μ and cell means π."""
    eps_pop = sum(m * min(p, 1.0 - p) for m, p in zip(mu, pi))
    H_pop   = sum(m * Hbin(p) for m, p in zip(mu, pi))
    return eps_pop, H_pop


def theoretical_bound(delta_mass, eta_mean, m, delta_conf, n):
    """
    κ(δ, η) · √( log(4m / δ_conf) / n )

    where κ(δ, η) := (1 + log_2((1-η)/η)) / √δ.
    """
    kappa = (1.0 + math.log((1.0 - eta_mean) / eta_mean) / LOG2) / math.sqrt(delta_mass)
    rate  = math.sqrt(math.log(4.0 * m / delta_conf) / n)
    return kappa * rate, kappa, rate


# ----------------------------------------------------------------------
# 2. Population scenarios
# ----------------------------------------------------------------------

def scenario_balanced():
    """
    Three-cell partition, balanced and well-separated.

      Cell    1     2     3
      μ(C)   .4    .35   .25
      π_C    .15   .55   .85

    All cells have mass ≥ δ = 0.25, all means in [η, 1-η] = [.15, .85].
    Population ε*_{Π,μ} = .4·.15 + .35·.45 + .25·.15 = .255
                       = .060 + .1575 + .0375 = .255
    Population H_μ(f|Π) = .4·Hbin(.15) + .35·Hbin(.55) + .25·Hbin(.85)
                        ≈ .4·.610  + .35·.993 + .25·.610
                        ≈ .244 + .348 + .153 = .745
    """
    return {
        "name":  "balanced 3-cell",
        "mu":    np.array([0.40, 0.35, 0.25]),
        "pi":    np.array([0.15, 0.55, 0.85]),
        "delta": 0.25,
        "eta":   0.15,
    }


def scenario_unbalanced():
    """
    Five-cell partition, more skewed but still bounded away from
    {0, 1, ∅}.

      μ = (.05, .10, .20, .30, .35)   →  δ = .05
      π = (.10, .30, .50, .70, .90)   →  η = .10
    """
    return {
        "name":  "unbalanced 5-cell",
        "mu":    np.array([0.05, 0.10, 0.20, 0.30, 0.35]),
        "pi":    np.array([0.10, 0.30, 0.50, 0.70, 0.90]),
        "delta": 0.05,
        "eta":   0.10,
    }


def scenario_marginal_aware():
    """
    Heavily unbalanced label marginal — stress-test for Proposition 6
    interacting with Proposition 7.

      μ = (.5, .5),  π = (.05, .15)
      Global marginal π = .5·.05 + .5·.15 = .10  →  π_* = .10
      So Proposition 6 predicts w*(.10) ≈ .069.
    """
    return {
        "name":  "marginal-aware unbalanced",
        "mu":    np.array([0.50, 0.50]),
        "pi":    np.array([0.05, 0.15]),
        "delta": 0.50,
        "eta":   0.05,
    }


SCENARIOS = [scenario_balanced, scenario_unbalanced, scenario_marginal_aware]


# ----------------------------------------------------------------------
# 3. Monte-Carlo experiment
# ----------------------------------------------------------------------

def run_scenario(scenario, ns, K, delta_conf, rng):
    """
    Run K i.i.d. trials per subsample size n and record:
      - empirical gap Δ_n,
      - theoretical bound κ · √(log(4m/δ_conf)/n),
      - coverage rate (fraction of trials with Δ_n ≤ bound).

    Returns a dict suitable for JSON serialisation.
    """
    mu    = scenario["mu"]
    pi    = scenario["pi"]
    delta = scenario["delta"]
    eta   = scenario["eta"]
    m     = len(mu)
    eps_pop, H_pop = population_bracket_quantities(mu, pi)

    rows = []
    for n in ns:
        bound, kappa, rate = theoretical_bound(delta, eta, m, delta_conf, n)
        deltas = np.empty(K)
        covers = 0
        bracket_holds = 0
        for k in range(K):
            # Sample cell assignments  c_v ~ μ.
            cells = rng.choice(m, size=n, p=mu)
            # Sample labels  f(v) | c_v=C  ~  Bernoulli(π_C).
            uniforms = rng.random(n)
            labels = (uniforms < pi[cells]).astype(np.int8)
            # Bucket per cell.
            buckets = [labels[cells == c] for c in range(m)]
            eps_emp, H_emp, _ = empirical_bracket_quantities(buckets)
            delta_n = abs(eps_pop - eps_emp) + abs(H_pop - H_emp)
            deltas[k] = delta_n
            if delta_n <= bound:
                covers += 1
            # Population-level sandwich check (Prop 7 corollary):
            # the empirical bracket inflated by `bound` should cover
            # the population point estimate.
            #   Hinv(H_pop) ≤ eps_pop ≤ ½ H_pop  (Theorem 1, population)
            # AND
            #   ½ H_emp - bound ≤ ½ H_pop ≤ ½ H_emp + bound
            #   Hinv(H_emp ± bound) brackets Hinv(H_pop)  (monotonicity)
            # We check the upper inequality
            #   eps_pop ≤ ½ H_emp + bound   (population minimum risk
            #                                  ≤ inflated empirical upper)
            if eps_pop <= 0.5 * H_emp + bound:
                bracket_holds += 1

        rows.append({
            "n":                 int(n),
            "K":                 int(K),
            "bound":             round(bound, 6),
            "kappa":             round(kappa, 6),
            "rate":              round(rate, 6),
            "delta_mean":        round(float(deltas.mean()), 6),
            "delta_max":         round(float(deltas.max()),  6),
            "delta_p95":         round(float(np.percentile(deltas, 95)), 6),
            "coverage_rate":     round(covers / K, 4),
            "bracket_holds":     round(bracket_holds / K, 4),
            "expected_coverage": 1.0 - delta_conf,
            "coverage_ok":       (covers / K) >= (1.0 - delta_conf),
        })

    return {
        "scenario":    scenario["name"],
        "m":           int(m),
        "delta_mass":  float(delta),
        "eta_mean":    float(eta),
        "delta_conf":  float(delta_conf),
        "eps_pop":     round(float(eps_pop), 6),
        "H_pop":       round(float(H_pop), 6),
        "rows":        rows,
        "all_ok":      all(r["coverage_ok"] for r in rows),
    }


# ----------------------------------------------------------------------
# 4. Driver
# ----------------------------------------------------------------------

def main():
    print("verify_t4_population.py — T4 Monte-Carlo concentration test")
    print("============================================================")

    ns         = [50, 100, 250, 500, 1000, 2500, 5000]
    K          = 500
    delta_conf = 0.05
    seed       = 20251225  # reproducibility; matches T2 seed style

    rng = np.random.default_rng(seed)

    scenarios = []
    for build in SCENARIOS:
        sc = build()
        print(f"\n--- scenario: {sc['name']} (m={len(sc['mu'])},"
              f" δ={sc['delta']}, η={sc['eta']}) ---")
        result = run_scenario(sc, ns=ns, K=K,
                              delta_conf=delta_conf, rng=rng)
        for r in result["rows"]:
            flag = "OK" if r["coverage_ok"] else "FAIL"
            print(f"  n={r['n']:>5}  Δ_mean={r['delta_mean']:.4f}"
                  f"  Δ_p95={r['delta_p95']:.4f}"
                  f"  bound={r['bound']:.4f}"
                  f"  coverage={r['coverage_rate']:.3f}"
                  f"  expected≥{r['expected_coverage']:.2f}  [{flag}]")
        scenarios.append(result)

    all_ok = all(s["all_ok"] for s in scenarios)
    manifest = {
        "tier":         "T4 (Monte-Carlo population concentration)",
        "seed":         seed,
        "ns":           ns,
        "K":            K,
        "delta_conf":   delta_conf,
        "scenarios":    scenarios,
        "all_ok":       all_ok,
    }
    Path("verify_t4.json").write_text(json.dumps(manifest, indent=2))

    print(f"\n  manifest:  verify_t4.json")
    print(f"  status:    {'ALL PASS' if all_ok else 'COVERAGE FAILURE — see above'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
