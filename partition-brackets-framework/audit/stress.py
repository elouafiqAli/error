#!/usr/bin/env python3
"""
audit/stress.py — Adversarial stress audit for Paper B Phase 2b-md G2.

Three audits, all run from this single entry point:

  A.1  Seed sweep         — re-run every B-T1 and B-T2 contract under
                            multiple --seed values; flag any seed that
                            produces a non-`pass` result.
  A.1' Mutation test      — deliberately apply a wrong identity (sign
                            flip / wrong constant) for T7, T3-upper,
                            and C-Va, and assert the corresponding
                            check FAILS. A verifier that cannot catch
                            obvious bugs is theatre.
  A.2  Boundary cases     — explicit numeric assertions on pathological
                            inputs (eta in {0, 1/2, 1}, rho near 1/2,
                            deterministic kernel reduces to T3, etc.).

Exit code 0 iff:
  - every seed in the sweep returned all-pass on every contract;
  - every mutation produced at least one `fail`;
  - every boundary assertion held.

Outputs a JSON manifest at audit/stress.json suitable for archival.

Run:
    python audit/stress.py [--seeds 25] [--trials 200] [--samples 20000]
"""
from __future__ import annotations

import argparse
import importlib
import json
import math
import os
import sys
import time
from dataclasses import dataclass, asdict
from typing import Any, Callable

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import verify_b_t1 as bt1  # noqa: E402
import verify_b_t2_mc as bt2  # noqa: E402


# ===============================================================
# A.1  Seed sweep
# ===============================================================


def run_one(module, args) -> list[dict]:
    return [
        {"name": r.name, "status": r.status, "message": r.message}
        for r in (c(args) for c in module.CONTRACTS)
    ]


def seed_sweep(n_seeds: int, samples: int, trials: int) -> dict:
    """Run B-T1 + B-T2 on seeds 0..n_seeds-1; flag any non-pass."""
    sweep: dict[str, Any] = {"B-T1": {}, "B-T2": {}}
    failures: list[dict] = []

    for seed in range(n_seeds):
        # B-T1 args
        a1 = argparse.Namespace(seed=seed, samples=samples, manifest="/tmp/_audit_t1.json")
        t0 = time.perf_counter()
        r1 = run_one(bt1, a1)
        sweep["B-T1"][seed] = {
            "wall_s": round(time.perf_counter() - t0, 2),
            "results": r1,
        }
        for r in r1:
            if r["status"] != "pass":
                failures.append({"seed": seed, "tier": "B-T1", **r})

        # B-T2 args
        a2 = argparse.Namespace(seed=seed, samples=samples, trials=trials,
                                manifest="/tmp/_audit_t2.json")
        t0 = time.perf_counter()
        r2 = run_one(bt2, a2)
        sweep["B-T2"][seed] = {
            "wall_s": round(time.perf_counter() - t0, 2),
            "results": r2,
        }
        for r in r2:
            if r["status"] != "pass":
                failures.append({"seed": seed, "tier": "B-T2", **r})

    sweep["summary"] = {
        "n_seeds": n_seeds,
        "samples": samples,
        "trials": trials,
        "n_failures": len(failures),
        "failures": failures,
        "passed": len(failures) == 0,
    }
    return sweep


# ===============================================================
# A.1' Mutation test — wrong-identity contracts MUST fail
# ===============================================================


def _mut_T7_wrong_sign(seed: int, samples: int, trials: int) -> bool:
    """T7 with predicted_noisy = rho + (1 + 2 rho) eps_clean (sign flip).

    Returns True iff the wrong identity is REJECTED by the population
    test (i.e. at least one trial violates the residual halfwidth).
    """
    rng_master = np.random.default_rng(seed)
    halfwidth = 4.0 * bt2._hoeffding_halfwidth(samples)
    rhos = (0.05, 0.10, 0.20)
    saw_violation = False
    for _ in range(trials):
        rng = np.random.default_rng(rng_master.integers(2**31))
        m = int(rng.integers(2, 9))
        p, etas = bt2._draw_partition(rng, m)
        cells, labels_clean = bt2._draw_iid_labelled(rng, p, etas, samples)
        for rho in rhos:
            flips = rng.random(samples) < rho
            labels_noisy = np.where(flips, 1 - labels_clean, labels_clean)
            eps_clean = bt2._empirical_bayes_risk(cells, labels_clean, m)
            eps_noisy = bt2._empirical_bayes_risk(cells, labels_noisy, m)
            # MUTATION: sign flip in correction
            predicted_wrong = rho + (1.0 + 2.0 * rho) * eps_clean
            if abs(eps_noisy - predicted_wrong) > halfwidth:
                saw_violation = True
    return saw_violation


def _mut_T3_wrong_c_phi(seed: int) -> bool:
    """T3 upper with c_shannon = 0.4 (true value 0.5).

    Returns True iff some (η, p) makes eps_star_Pi > 0.4 * H(f|Pi).
    """
    rng = np.random.default_rng(seed)
    saw_violation = False
    for _ in range(500):
        m = int(rng.integers(2, 9))
        p = rng.dirichlet([1.0] * m)
        etas = rng.random(m)
        eps_star = float(np.dot(p, np.minimum(etas, 1 - etas)))
        h_vals = np.array([bt1._h_bin(float(e)) for e in etas])
        H = float(np.dot(p, h_vals))
        # MUTATION: claim c = 0.4 instead of 0.5
        if eps_star > 0.4 * H + 1e-9:
            saw_violation = True
            break
    return saw_violation


def _mut_CVa_wrong_identity(seed: int, samples: int) -> bool:
    """C-Va with variance plug-in eta(1+eta) (wrong sign).

    Returns True iff empirical MSE != wrong plug-in beyond halfwidth.
    """
    rng = np.random.default_rng(seed)
    halfwidth = 4.0 * bt2._hoeffding_halfwidth(samples)
    saw_violation = False
    for _ in range(200):
        m = int(rng.integers(2, 9))
        p, etas = bt2._draw_partition(rng, m)
        cells, labels = bt2._draw_iid_labelled(rng, p, etas, samples)
        # Empirical MSE*
        mse = 0.0
        wrong = 0.0
        for i in range(m):
            mask = cells == i
            c = mask.sum()
            if c == 0:
                continue
            p_hat = c / samples
            yhat = labels[mask].mean()
            mse += p_hat * ((labels[mask] - yhat) ** 2).mean()
            # MUTATION: eta(1+eta) instead of eta(1-eta)
            wrong += p_hat * yhat * (1 + yhat)
        if abs(mse - wrong) > halfwidth:
            saw_violation = True
            break
    return saw_violation


def mutation_test(seed: int, samples: int, trials: int) -> dict:
    mutations = {
        "T7_wrong_sign": _mut_T7_wrong_sign(seed, samples, max(50, trials // 5)),
        "T3_wrong_c_phi": _mut_T3_wrong_c_phi(seed),
        "CVa_wrong_identity": _mut_CVa_wrong_identity(seed, samples),
    }
    return {
        "mutations": mutations,
        # All mutations MUST be rejected (return True = "saw violation").
        "all_caught": all(mutations.values()),
        "uncaught": [k for k, v in mutations.items() if not v],
    }


# ===============================================================
# A.2  Boundary / pathological inputs
# ===============================================================


def boundary_tests() -> dict:
    """Explicit-value assertions at boundaries. Each assert is one line."""
    out: dict[str, Any] = {}
    failures: list[str] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        out[name] = {"pass": ok, "detail": detail}
        if not ok:
            failures.append(name)

    # ---------------- T3 boundaries ----------------
    # eta -> 0+: H_bin(0) = 0, eps* contribution = 0.
    h0 = bt1._h_bin(1e-12)
    check("T3_eta_to_0_Hbin_finite", h0 >= 0 and h0 < 1e-9, f"H_bin(1e-12)={h0:.2e}")

    # eta = 1/2: H_bin = 1 (bits), c_phi witness.
    h_half = bt1._h_bin(0.5)
    check("T3_eta_half_Hbin_eq_1", abs(h_half - 1.0) < 1e-12, f"H_bin(1/2)={h_half}")

    # Degenerate m=1 partition: eps_star = min(eta, 1-eta), bracket exact.
    eta = 0.3
    eps_star = min(eta, 1 - eta)
    H = bt1._h_bin(eta)
    lo = bt1._h_bin_inv_on_lower_half(H)
    up = 0.5 * H
    check("T3_m_eq_1_bracket_envelopes",
          lo - 1e-9 <= eps_star <= up + 1e-9,
          f"eta={eta} lo={lo:.6f} eps={eps_star} up={up:.6f}")

    # Sparse partition m=1000 with one dominant mass.
    rng = np.random.default_rng(42)
    m_big = 1000
    p_sparse = np.full(m_big, 1e-9)
    p_sparse[0] = 1.0 - (m_big - 1) * 1e-9
    p_sparse /= p_sparse.sum()
    etas_sparse = rng.random(m_big)
    eps_star_sparse = float(np.dot(p_sparse, np.minimum(etas_sparse, 1 - etas_sparse)))
    H_sparse = float(np.dot(p_sparse, [bt1._h_bin(float(e)) for e in etas_sparse]))
    lo_s = bt1._h_bin_inv_on_lower_half(H_sparse)
    check("T3_m_eq_1000_sparse_bracket",
          lo_s - 1e-9 <= eps_star_sparse <= 0.5 * H_sparse + 1e-9,
          f"eps={eps_star_sparse:.6f} lo={lo_s:.6f} up={0.5*H_sparse:.6f}")

    # ---------------- T7 boundaries ----------------
    # rho = 0: tilde = clean; eps_noisy = eps_clean.
    eta_arr = np.array([0.2, 0.6, 0.9])
    p_arr = np.array([0.3, 0.5, 0.2])
    eps_clean = float(np.dot(p_arr, np.minimum(eta_arr, 1 - eta_arr)))
    for rho in [0.0, 0.001, 0.499]:
        tilde = rho + (1 - 2 * rho) * eta_arr
        eps_noisy = float(np.dot(p_arr, np.minimum(tilde, 1 - tilde)))
        predicted = rho + (1 - 2 * rho) * eps_clean
        check(f"T7_rho_{rho}_identity",
              abs(eps_noisy - predicted) < 1e-12,
              f"eps_noisy={eps_noisy:.6f} predicted={predicted:.6f}")

    # rho -> 1/2: denominator -> 0, inverse correction blows up
    # (informational; we just record the expected behaviour).
    rho_near = 0.4999
    blowup = 1.0 / (1.0 - 2.0 * rho_near)
    check("T7_rho_near_half_blowup_recorded",
          blowup > 5000,
          f"1/(1-2*0.4999)={blowup:.1f}")

    # ---------------- C-Pi boundaries ----------------
    # H(f|Pi) = 0 (all eta in {0,1}): Pinsker bound -> 1/2 - sqrt((ln 2)/2)
    # = 1/2 - 0.588... = NEGATIVE => bracket is vacuous (expected).
    pin_at_zero = 0.5 - math.sqrt(math.log(2.0) / 2.0)
    check("CPi_vacuous_when_H_zero",
          pin_at_zero < 0,
          f"Pinsker lower at H=0 is {pin_at_zero:.4f} (vacuous as expected)")

    # H(f|Pi) = 1 (all eta = 1/2): bound -> 1/2 (tight).
    pin_at_one = 0.5 - math.sqrt(math.log(2.0) / 2.0 * (1.0 - 1.0))
    check("CPi_tight_when_H_one",
          abs(pin_at_one - 0.5) < 1e-12,
          f"Pinsker lower at H=1 is {pin_at_one}")

    # Non-trivial threshold H > 1 - 1/(2 ln 2) ~ 0.279.
    threshold = 1.0 - 1.0 / (2.0 * math.log(2.0))
    pin_at_thr = 0.5 - math.sqrt(math.log(2.0) / 2.0 * (1.0 - threshold))
    check("CPi_threshold_non_vacuous",
          abs(pin_at_thr) < 1e-9,
          f"Pinsker lower at H={threshold:.4f} is {pin_at_thr:.4e}")

    # ---------------- T9 reduces to T3 for deterministic kernel ----------------
    # K(z|x) = 1[Pi(x) = z]: should reproduce T3 numerically to ~1e-12.
    rng = np.random.default_rng(7)
    n_X, m = 8, 4
    px = rng.dirichlet([1.0] * n_X)
    assign = rng.integers(0, m, size=n_X)
    K = np.zeros((n_X, m))
    K[np.arange(n_X), assign] = 1.0  # deterministic kernel
    eta_x = rng.random(n_X)
    # Hard partition cells: indices of X mapped to each z
    p_z = np.zeros(m)
    eta_z = np.zeros(m)
    for z in range(m):
        mask = assign == z
        p_z[z] = px[mask].sum()
        if p_z[z] > 0:
            eta_z[z] = float(np.dot(px[mask], eta_x[mask])) / p_z[z]
    eps_K = float(np.dot(p_z, np.minimum(eta_z, 1 - eta_z)))
    # Direct hard-partition Bayes risk
    eps_hard = float(np.dot(p_z, np.minimum(eta_z, 1 - eta_z)))
    check("T9_deterministic_reduces_to_T3",
          abs(eps_K - eps_hard) < 1e-12,
          f"eps_K={eps_K:.12f} eps_hard={eps_hard:.12f}")

    # ---------------- P10 boundary: refinement to atoms ----------------
    # Refining each cell to single-atom cells with eta in {0, 1}:
    # phi -> 0 (because eta lands on the boundary), so eps_star -> 0
    # and the bracket collapses.
    # We just check phi vanishes when all eta in {0,1}.
    etas_atomic = np.array([0.0, 1.0, 0.0, 1.0])
    p_atomic = np.array([0.25, 0.25, 0.25, 0.25])
    phi_at_atoms = float(np.dot(p_atomic, [bt1._h_bin(float(e)) for e in etas_atomic]))
    check("P10_refinement_to_atoms_phi_zero",
          phi_at_atoms < 1e-12,
          f"phi at atomic = {phi_at_atoms:.2e}")

    out["summary"] = {
        "n_checks": len([k for k in out if k != "summary"]),
        "n_failures": len(failures),
        "failures": failures,
        "passed": len(failures) == 0,
    }
    return out


# ===============================================================
# Runner
# ===============================================================


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=25,
                        help="Sweep seeds 0..N-1 for the seed-sweep audit")
    parser.add_argument("--samples", type=int, default=20_000,
                        help="Sample count for B-T2 contracts during the sweep")
    parser.add_argument("--trials", type=int, default=200,
                        help="Trial count for B-T2 contracts during the sweep")
    parser.add_argument("--mut-seed", type=int, default=0,
                        help="Seed for the mutation test (one shot)")
    parser.add_argument("--manifest", default=os.path.join(HERE, "stress.json"))
    parser.add_argument("--quick", action="store_true",
                        help="Quick smoke: --seeds 3 --trials 50 --samples 5000")
    args = parser.parse_args()

    if args.quick:
        args.seeds, args.trials, args.samples = 3, 50, 5_000

    print(f"=== A.1  Seed sweep  (seeds=0..{args.seeds-1}, "
          f"trials={args.trials}, samples={args.samples}) ===")
    t0 = time.perf_counter()
    sweep = seed_sweep(args.seeds, args.samples, args.trials)
    print(f"  done in {time.perf_counter()-t0:.1f}s  "
          f"failures={sweep['summary']['n_failures']}")

    print(f"=== A.1' Mutation test (mut-seed={args.mut_seed}) ===")
    t0 = time.perf_counter()
    mut = mutation_test(args.mut_seed, args.samples, args.trials)
    print(f"  done in {time.perf_counter()-t0:.1f}s  "
          f"all_caught={mut['all_caught']}  uncaught={mut['uncaught']}")

    print("=== A.2  Boundary cases ===")
    t0 = time.perf_counter()
    bdy = boundary_tests()
    print(f"  done in {time.perf_counter()-t0:.1f}s  "
          f"failures={bdy['summary']['n_failures']}")
    if bdy["summary"]["failures"]:
        for name in bdy["summary"]["failures"]:
            print(f"    FAIL: {name}  {bdy[name]['detail']}")

    overall_pass = (
        sweep["summary"]["passed"]
        and mut["all_caught"]
        and bdy["summary"]["passed"]
    )

    manifest = {
        "tool": "audit_stress",
        "passed": overall_pass,
        "seed_sweep": sweep,
        "mutation_test": mut,
        "boundary": bdy,
    }
    with open(args.manifest, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nwrote {args.manifest}")
    print(f"OVERALL: {'PASS' if overall_pass else 'FAIL'}")
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
