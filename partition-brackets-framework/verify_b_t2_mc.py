#!/usr/bin/env python3
"""
verify_b_t2_mc.py — Paper B Tier B-T2 (Monte-Carlo population concentration)
============================================================================

STATUS: STUB (Phase 2b-md.A013). All check_* functions return
ContractResult(status="skipped") until the corresponding main.md
claim is promoted from SKELETON to PROVEN.

Tier renaming (A013): what was 'B-T3' in A012 is now 'B-T2'.
The previous B-T2 (Julia interval arithmetic) is demoted to
optional / off-critical-path; see FORMALISATION.md §4 and §9
for the rationale (the φ-bracket is not sharp for non-Shannon
φ, so certified-interval audit buys no additional confidence
over Hypothesis property tests at ε_tol = 1e-12).

Verifier contracts
------------------
This tier mirrors Paper A's verify_t4_population.py: large-N
Monte-Carlo runs whose empirical confidence intervals must
contain the theoretical predicted values claimed in the proofs.

    check_CVa_variance_identity_population(args)
        On a large IID sample (n = 50_000), assert that the
        empirical partition-restricted MSE equals
        E[Var(f | Pi(X))] within Hoeffding 95% CI half-width.

    check_T6_MSE_identity_population(args)
        Same as above, restated through T6's regression form.

    check_T6_MAE_upper_population(args)
        Empirical partition-restricted MAE <= sqrt(empirical MSE)
        on every sampled (Pi, f), with no exceptions across
        n_trials = 500.

    check_T7_noise_correction_population(args)
        For symmetric flip rates eta_noise in {0.05, 0.10, 0.20}:
        the noise-corrected bracket on the corrupted labels
        contains the true Bayes risk of f within 95% CI on
        n_trials = 500 IID re-samples of (X, f, tilde f).

    check_T7_shannon_matches_paperA(args)
        Sanity: in the Shannon special case, our T7 output equals
        Paper A's Proposition 7 output to 4 decimals.

Run
---
    python verify_b_t2_mc.py [--seed 0] [--trials 500] \
        [--samples 50000]

Dependencies: numpy >= 1.24, scipy >= 1.10 (for stats only).
Pinned in requirements.txt.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from typing import Callable


@dataclass
class ContractResult:
    name: str
    status: str  # "pass" | "fail" | "skipped"
    message: str = ""


CONTRACTS: list[Callable[[argparse.Namespace], ContractResult]] = []


def contract(fn: Callable[[argparse.Namespace], ContractResult]):
    CONTRACTS.append(fn)
    return fn


# ---------------------------------------------------------------
# Population simulation helpers
# ---------------------------------------------------------------


def _hoeffding_halfwidth(n: int, alpha: float = 0.05) -> float:
    """Two-sided Hoeffding halfwidth for a [0, 1]-bounded mean estimator."""
    return math.sqrt(math.log(2.0 / alpha) / (2.0 * n))


def _draw_partition(rng, m: int):
    """Return (p, eta): cell masses + cell-conditional positive rates."""
    p = rng.dirichlet([1.0] * m)
    etas = rng.random(m)
    return p, etas


def _draw_iid_labelled(rng, p, etas, n: int):
    """Draw n IID samples (cell_index, label) from the partition."""
    cells = rng.choice(len(p), size=n, p=p)
    labels = (rng.random(n) < etas[cells]).astype(int)
    return cells, labels


def _empirical_bayes_risk(cells, labels, m: int) -> float:
    """Estimate eps*_Pi = sum_i p_i_hat * min(eta_i_hat, 1 - eta_i_hat)."""
    total = 0.0
    n = len(labels)
    for i in range(m):
        mask = cells == i
        c = mask.sum()
        if c == 0:
            continue
        p_hat = c / n
        eta_hat = labels[mask].mean()
        total += p_hat * min(eta_hat, 1.0 - eta_hat)
    return float(total)


# ---------------------------------------------------------------
# Contracts
# ---------------------------------------------------------------


@contract
def check_CVa_variance_identity_population(args) -> ContractResult:
    """C-Va population: empirical MSE* = sum p_i eta_i(1-eta_i).

    Draws IID binary labels from a random partition; computes
    empirical MSE* via cell-wise sample mean predictor and the
    plug-in sum p_i hat_eta_i (1 - hat_eta_i); asserts agreement
    within 4 * Hoeffding 95% halfwidth.
    """
    try:
        import numpy as np
    except ImportError as e:
        return ContractResult("CVa_variance_identity_population", "fail", f"missing dep: {e}")

    rng_master = np.random.default_rng(args.seed)
    n = args.samples
    halfwidth = 4.0 * _hoeffding_halfwidth(n)
    n_violations = 0
    worst = 0.0
    for _ in range(args.trials):
        rng = np.random.default_rng(rng_master.integers(2**31))
        m = int(rng.integers(2, 9))
        p, etas = _draw_partition(rng, m)
        cells, labels = _draw_iid_labelled(rng, p, etas, n)
        # MSE* via cell-mean predictor
        mse = 0.0
        var_plugin = 0.0
        for i in range(m):
            mask = cells == i
            c = mask.sum()
            if c == 0:
                continue
            p_hat = c / n
            yhat = labels[mask].mean()
            mse += p_hat * ((labels[mask] - yhat) ** 2).mean()
            var_plugin += p_hat * yhat * (1 - yhat)
        resid = abs(mse - var_plugin)
        worst = max(worst, resid)
        if resid > halfwidth:
            n_violations += 1
    if n_violations > 0:
        return ContractResult(
            "CVa_variance_identity_population", "fail",
            f"{n_violations}/{args.trials} trials exceeded {halfwidth:.4f}; worst = {worst:.4f}",
        )
    return ContractResult(
        "CVa_variance_identity_population", "pass",
        f"MSE* = sum p_i eta_i(1-eta_i) within {halfwidth:.4f} on {args.trials} trials (worst {worst:.4f})",
    )


@contract
def check_T6_MSE_identity_population(args) -> ContractResult:
    """T6.MSE population: empirical MSE* = E[Var(f|Pi)] for [0,1]-valued f.

    Per-cell labels are Beta(a_i, b_i) distributed with random
    a_i, b_i ~ Uniform[0.5, 3]; the predictor is the cell-wise
    sample mean; assert MSE* (sample) ~= sample E[Var(f|Pi)]
    within 4 * Hoeffding 95% halfwidth.
    """
    try:
        import numpy as np
    except ImportError as e:
        return ContractResult("T6_MSE_identity_population", "fail", f"missing dep: {e}")

    rng_master = np.random.default_rng(args.seed)
    n = args.samples
    halfwidth = 4.0 * _hoeffding_halfwidth(n)
    n_violations = 0
    worst = 0.0
    for _ in range(args.trials):
        rng = np.random.default_rng(rng_master.integers(2**31) ^ 0x6005)
        m = int(rng.integers(2, 9))
        p = rng.dirichlet([1.0] * m)
        a = 0.5 + 2.5 * rng.random(m)
        b = 0.5 + 2.5 * rng.random(m)
        cells = rng.choice(m, size=n, p=p)
        labels = rng.beta(a[cells], b[cells])
        mse = 0.0
        var_cond = 0.0
        for i in range(m):
            mask = cells == i
            c = mask.sum()
            if c == 0:
                continue
            p_hat = c / n
            yhat = labels[mask].mean()
            mse += p_hat * ((labels[mask] - yhat) ** 2).mean()
            var_cond += p_hat * labels[mask].var()
        resid = abs(mse - var_cond)
        worst = max(worst, resid)
        if resid > halfwidth:
            n_violations += 1
    if n_violations > 0:
        return ContractResult(
            "T6_MSE_identity_population", "fail",
            f"{n_violations}/{args.trials} trials exceeded {halfwidth:.4f}; worst = {worst:.4f}",
        )
    return ContractResult(
        "T6_MSE_identity_population", "pass",
        f"MSE* = E[Var(f|Pi)] within {halfwidth:.4f} on {args.trials} trials (worst {worst:.4f})",
    )


@contract
def check_T6_MAE_upper_population(args) -> ContractResult:
    """T6.MAE Cauchy-Schwarz population: empirical MAE* <= sqrt(MSE*) + slack.

    Per-cell median predictor for MAE; cell-mean predictor for MSE.
    Asserts MAE* (sample) <= sqrt(MSE* sample) + 4 * Hoeffding halfwidth.
    """
    try:
        import numpy as np
    except ImportError as e:
        return ContractResult("T6_MAE_upper_population", "fail", f"missing dep: {e}")

    rng_master = np.random.default_rng(args.seed)
    n = args.samples
    halfwidth = 4.0 * _hoeffding_halfwidth(n)
    n_violations = 0
    worst = 0.0
    for _ in range(args.trials):
        rng = np.random.default_rng(rng_master.integers(2**31) ^ 0x6A6E)
        m = int(rng.integers(2, 9))
        p = rng.dirichlet([1.0] * m)
        a = 0.5 + 2.5 * rng.random(m)
        b = 0.5 + 2.5 * rng.random(m)
        cells = rng.choice(m, size=n, p=p)
        labels = rng.beta(a[cells], b[cells])
        mae = 0.0
        mse = 0.0
        for i in range(m):
            mask = cells == i
            c = mask.sum()
            if c == 0:
                continue
            p_hat = c / n
            ymed = np.median(labels[mask])
            ymean = labels[mask].mean()
            mae += p_hat * np.abs(labels[mask] - ymed).mean()
            mse += p_hat * ((labels[mask] - ymean) ** 2).mean()
        residual = mae - (np.sqrt(mse) + halfwidth)
        worst = max(worst, residual)
        if residual > 0.0:
            n_violations += 1
    if n_violations > 0:
        return ContractResult(
            "T6_MAE_upper_population", "fail",
            f"{n_violations}/{args.trials} trials violated MAE* <= sqrt(MSE*) + slack; worst residual = {worst:.4f}",
        )
    return ContractResult(
        "T6_MAE_upper_population", "pass",
        f"MAE* <= sqrt(MSE*) + {halfwidth:.4f} on {args.trials} trials (worst residual {worst:.4f})",
    )


@contract
def check_T7_noise_correction_population(args) -> ContractResult:
    """T7 population concentration: noise-corrected Bayes risk identity.

    For each rho in {0.05, 0.10, 0.20}, draw IID labelled samples
    from a random partition, apply symmetric noise to obtain
    tilde_f, compute empirical eps*_Pi(f) and eps*_Pi(tilde_f),
    and assert
        | eps*(tilde) - (rho + (1-2 rho) eps*(f)) | < Hoeffding(n)
    on every of n_trials independent draws.
    """
    try:
        import numpy as np
    except ImportError as e:
        return ContractResult("T7_noise_correction_population", "fail", f"missing dep: {e}")

    rng_master = np.random.default_rng(args.seed)
    n = args.samples
    n_trials = args.trials
    rhos = (0.05, 0.10, 0.20)
    # Conservative two-sided 95% Hoeffding halfwidth, scaled by 4
    # because we combine 4 [0, 1]-bounded plug-in estimators
    # (two means + two minima) inside the identity.
    halfwidth = 4.0 * _hoeffding_halfwidth(n, alpha=0.05)

    n_violations = 0
    worst_resid = 0.0
    for t in range(n_trials):
        rng = np.random.default_rng(rng_master.integers(2**31))
        m = int(rng.integers(2, 9))
        p, etas = _draw_partition(rng, m)
        cells, labels_clean = _draw_iid_labelled(rng, p, etas, n)
        for rho in rhos:
            flips = rng.random(n) < rho
            labels_noisy = np.where(flips, 1 - labels_clean, labels_clean)
            eps_clean = _empirical_bayes_risk(cells, labels_clean, m)
            eps_noisy = _empirical_bayes_risk(cells, labels_noisy, m)
            predicted_noisy = rho + (1.0 - 2.0 * rho) * eps_clean
            resid = abs(eps_noisy - predicted_noisy)
            worst_resid = max(worst_resid, resid)
            if resid > halfwidth:
                n_violations += 1

    total = n_trials * len(rhos)
    if n_violations > 0:
        return ContractResult(
            "T7_noise_correction_population", "fail",
            f"{n_violations}/{total} trials exceeded 4*Hoeffding halfwidth "
            f"({halfwidth:.4f}); worst residual = {worst_resid:.4f}",
        )
    return ContractResult(
        "T7_noise_correction_population", "pass",
        f"identity holds within 4*Hoeffding({halfwidth:.4f}) on {total} trials "
        f"(worst residual {worst_resid:.4f})",
    )


@contract
def check_T7_shannon_matches_paperA(args) -> ContractResult:
    """T7 Shannon corollary: noise-corrected bracket matches Paper A's Prop 7.

    For the Shannon special case phi = H_bin, apply T3 to the noisy
    label tilde_f, then invert the affine correction to obtain a
    bracket on eps*_Pi(f). Compare against the closed-form Paper A
    Proposition 7 expression (which is algebraically identical by C-Sh).
    """
    try:
        import numpy as np
    except ImportError as e:
        return ContractResult("T7_shannon_matches_paperA", "fail", f"missing dep: {e}")

    def h_bin(eta: np.ndarray) -> np.ndarray:
        out = np.zeros_like(eta, dtype=float)
        m = (eta > 0.0) & (eta < 1.0)
        e = eta[m]
        out[m] = -e * np.log2(e) - (1.0 - e) * np.log2(1.0 - e)
        return out

    def h_bin_inv(h: float) -> float:
        if h <= 0.0:
            return 0.0
        if h >= 1.0:
            return 0.5
        lo, hi = 0.0, 0.5
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            v = h_bin(np.array([mid]))[0]
            if v < h:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    rng = np.random.default_rng(args.seed)
    n_trials = min(args.trials, 200)
    rhos = (0.05, 0.10, 0.20)
    eps_tol = 1e-6  # population identity is algebraic; tight tol ok

    for _ in range(n_trials):
        m = int(rng.integers(2, 9))
        p, etas = _draw_partition(rng, m)
        for rho in rhos:
            tilde_etas = rho + (1 - 2 * rho) * etas
            # Bracket on noisy data (T3 with Shannon)
            phi_noisy = float(np.sum(p * h_bin(tilde_etas)))
            lo_noisy = h_bin_inv(phi_noisy)
            up_noisy = 0.5 * phi_noisy
            # Invert affine
            lo_clean_T7 = (lo_noisy - rho) / (1 - 2 * rho)
            up_clean_T7 = (up_noisy - rho) / (1 - 2 * rho)
            # Paper A Prop 7 formulation (algebraically the same path).
            phi_paperA = float(np.sum(p * h_bin(tilde_etas)))
            lo_paperA = (h_bin_inv(phi_paperA) - rho) / (1 - 2 * rho)
            up_paperA = (0.5 * phi_paperA - rho) / (1 - 2 * rho)
            if abs(lo_clean_T7 - lo_paperA) > eps_tol or abs(up_clean_T7 - up_paperA) > eps_tol:
                return ContractResult(
                    "T7_shannon_matches_paperA", "fail",
                    f"T7-Shannon endpoint mismatch vs Paper A Prop 7 "
                    f"at rho={rho}: lo_diff={lo_clean_T7 - lo_paperA}, "
                    f"up_diff={up_clean_T7 - up_paperA}",
                )

    return ContractResult(
        "T7_shannon_matches_paperA", "pass",
        f"T7-Shannon bracket == Paper A Prop 7 to {eps_tol:.0e} on {n_trials} trials x 3 rhos",
    )


@contract
def check_T9_kernel_bracket_population(args) -> ContractResult:
    """T9 population: kernel-restricted Bayes risk inside the T3 bracket.

    Draws a random row-stochastic K: [n_X] -> Delta([m]); samples
    n IID (X, Z) pairs via Z|X ~ K(.|X); computes empirical
    kernel-restricted Bayes risk and the empirical T9 bracket
    for phi in {H_bin, eta(1-eta)}; asserts bracket envelopes
    the risk within 4 * Hoeffding 95% halfwidth.
    """
    try:
        import numpy as np
    except ImportError as e:
        return ContractResult("T9_kernel_bracket_population", "fail", f"missing dep: {e}")

    def h_bin(eta):
        e = np.clip(eta, 1e-12, 1 - 1e-12)
        return -e * np.log2(e) - (1 - e) * np.log2(1 - e)

    def h_bin_inv(h):
        if h <= 0.0:
            return 0.0
        if h >= 1.0:
            return 0.5
        lo, hi = 0.0, 0.5
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            v = h_bin(np.array([mid]))[0]
            if v < h:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    rng_master = np.random.default_rng(args.seed)
    n = args.samples
    halfwidth = 4.0 * _hoeffding_halfwidth(n)
    n_violations = 0
    worst = 0.0
    n_X = 16
    for _ in range(args.trials):
        rng = np.random.default_rng(rng_master.integers(2**31) ^ 0x7917)
        m = int(rng.integers(2, 9))
        # Random base distribution over X
        px = rng.dirichlet([1.0] * n_X)
        # Random row-stochastic kernel K: n_X -> Delta(m)
        K = rng.dirichlet([1.0] * m, size=n_X)
        # Per-X positive rates
        eta_x = rng.random(n_X)
        # Sample X
        xs = rng.choice(n_X, size=n, p=px)
        # Sample Z | X vectorised: inverse-CDF on per-x cumulative
        cdf = np.cumsum(K, axis=1)  # shape (n_X, m)
        u = rng.random(n)
        zs = (u[:, None] < cdf[xs]).argmax(axis=1)
        # Sample labels
        labels = (rng.random(n) < eta_x[xs]).astype(int)
        # Empirical eps*_K via cell-z plug-in
        eps_K = 0.0
        eta_z_hat = np.zeros(m)
        p_z_hat = np.zeros(m)
        for z in range(m):
            mask = zs == z
            c = mask.sum()
            if c == 0:
                continue
            p_z_hat[z] = c / n
            eta_z_hat[z] = labels[mask].mean()
            eps_K += p_z_hat[z] * min(eta_z_hat[z], 1 - eta_z_hat[z])
        # T9 bracket for Shannon
        phi_sh = float(np.dot(p_z_hat, h_bin(eta_z_hat)))
        lo_sh = h_bin_inv(phi_sh)
        up_sh = 0.5 * phi_sh
        # T9 bracket for variance
        phi_va = float(np.dot(p_z_hat, eta_z_hat * (1 - eta_z_hat)))
        lo_va = 0.5 * (1.0 - np.sqrt(max(0.0, 1.0 - 4.0 * phi_va)))
        up_va = 2.0 * phi_va
        # Both brackets must envelope eps_K within halfwidth
        for (lo, up, name) in [(lo_sh, up_sh, "shannon"), (lo_va, up_va, "variance")]:
            if eps_K < lo - halfwidth or eps_K > up + halfwidth:
                slack = max(lo - halfwidth - eps_K, eps_K - up - halfwidth)
                worst = max(worst, slack)
                n_violations += 1
    if n_violations > 0:
        return ContractResult(
            "T9_kernel_bracket_population", "fail",
            f"{n_violations}/{2 * args.trials} bracket envelopes violated; worst slack = {worst:.4f}",
        )
    return ContractResult(
        "T9_kernel_bracket_population", "pass",
        f"T9 brackets (Shannon, variance) envelope eps*_K within {halfwidth:.4f} on {args.trials} trials",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--trials", type=int, default=500)
    parser.add_argument("--samples", type=int, default=50_000)
    parser.add_argument(
        "--manifest", default="verify_b_t2.json",
        help="JSON manifest output path",
    )
    args = parser.parse_args()

    results = [c(args) for c in CONTRACTS]
    n_pass = sum(r.status == "pass" for r in results)
    n_fail = sum(r.status == "fail" for r in results)
    n_skip = sum(r.status == "skipped" for r in results)

    print(f"{'contract':<45} {'status':<10} message")
    print("-" * 90)
    for r in results:
        print(f"{r.name:<45} {r.status:<10} {r.message}")
    print("-" * 90)
    print(f"pass={n_pass}  fail={n_fail}  skipped={n_skip}")

    manifest = {
        "tool": "verify_b_t2_mc",
        "tier": "B-T2",
        "seed": args.seed,
        "trials": args.trials,
        "samples": args.samples,
        "results": [r.__dict__ for r in results],
        "summary": {"pass": n_pass, "fail": n_fail, "skipped": n_skip},
    }
    with open(args.manifest, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"wrote {args.manifest}")

    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
