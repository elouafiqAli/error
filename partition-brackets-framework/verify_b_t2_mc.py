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
# STUBS — promoted one commit at a time per FORMALISATION.md §7.
# ---------------------------------------------------------------


@contract
def check_CVa_variance_identity_population(args) -> ContractResult:
    return ContractResult(
        "CVa_variance_identity_population",
        "skipped",
        "STUB — lands in commit paper-b Phase 2b-md.C-Sh+C-Va",
    )


@contract
def check_T6_MSE_identity_population(args) -> ContractResult:
    return ContractResult(
        "T6_MSE_identity_population",
        "skipped",
        "STUB — lands in commit paper-b Phase 2b-md.T6+C-Pi",
    )


@contract
def check_T6_MAE_upper_population(args) -> ContractResult:
    return ContractResult(
        "T6_MAE_upper_population",
        "skipped",
        "STUB — lands in commit paper-b Phase 2b-md.T6+C-Pi",
    )


@contract
def check_T7_noise_correction_population(args) -> ContractResult:
    return ContractResult(
        "T7_noise_correction_population",
        "skipped",
        "STUB — lands in commit paper-b Phase 2b-md.T7",
    )


@contract
def check_T7_shannon_matches_paperA(args) -> ContractResult:
    return ContractResult(
        "T7_shannon_matches_paperA",
        "skipped",
        "STUB — lands in commit paper-b Phase 2b-md.T7",
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
