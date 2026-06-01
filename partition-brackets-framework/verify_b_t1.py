#!/usr/bin/env python3
"""
verify_b_t1.py — Paper B Tier B-T1 (symbolic identities + property tests)
=========================================================================

STATUS: STUB (Phase 2b-md.A013). All check_* functions return
ContractResult(status='skipped') until the corresponding main.md
claim is promoted from SKELETON to PROVEN. Each subsequent
Phase 2b-md commit lands one check_* and its main.md proof
together.

This file is the *only* tier on the Gate G2 critical path
besides B-T2 (Monte-Carlo). It carries TWO responsibilities:

  1. SymPy closed-form identity checks
     (the four-step proof template's Step 1+2 are reproduced as
     symbolic identities — anything that does not survive a
     SymPy `simplify` is not a proof).

  2. Hypothesis property tests
     (Step 3 sharpness witnesses and Step 4 failure modes are
     stress-tested on hundreds-to-thousands of random
     constructions, with automatic shrinking to minimal
     counterexamples).

This collapses what was three tiers in Phase 2b-md.A012 into
two: B-T1 absorbs symbolic + property, B-T2 stays Monte-Carlo
for population statements. Julia (`verify_b_optional.jl`) is
demoted to optional parity with Paper A and is NOT on the
critical path; see FORMALISATION.md §4 and §9 for rationale.

Run
---
    python verify_b_t1.py [--seed 0] [--samples 1000] [--hypothesis-deadline 5000]

Dependencies: sympy >= 1.12, numpy >= 1.24, hypothesis >= 6.100.
Pinned in requirements.txt.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from typing import Callable

# Imports deferred so the stub does not fail to import on a
# bare environment; each check imports what it needs.


@dataclass
class ContractResult:
    name: str
    status: str  # "pass" | "fail" | "skipped"
    message: str = ""


CONTRACTS: list[Callable[[argparse.Namespace], ContractResult]] = []


def contract(fn: Callable[[argparse.Namespace], ContractResult]):
    """Decorator registering a contract for the main runner."""
    CONTRACTS.append(fn)
    return fn


# ---------------------------------------------------------------
# STUB IMPLEMENTATIONS — promoted to real proofs one commit at a
# time, following FORMALISATION.md §7 sequencing.
# ---------------------------------------------------------------


@contract
def check_T3_jensen_lower(args: argparse.Namespace) -> ContractResult:
    return ContractResult(
        "T3_jensen_lower",
        "skipped",
        "STUB — proof lands in commit paper-b Phase 2b-md.T3",
    )


@contract
def check_T3_upper_constant(args: argparse.Namespace) -> ContractResult:
    return ContractResult(
        "T3_upper_constant",
        "skipped",
        "STUB — proof lands in commit paper-b Phase 2b-md.T3",
    )


@contract
def check_CSh_reduces_to_paperA(args: argparse.Namespace) -> ContractResult:
    return ContractResult(
        "CSh_reduces_to_paperA",
        "skipped",
        "STUB — proof lands in commit paper-b Phase 2b-md.C-Sh+C-Va",
    )


@contract
def check_CVa_bayes_variance_identity(args: argparse.Namespace) -> ContractResult:
    return ContractResult(
        "CVa_bayes_variance_identity",
        "skipped",
        "STUB — proof lands in commit paper-b Phase 2b-md.C-Sh+C-Va",
    )


@contract
def check_CPi_pinsker_constant(args: argparse.Namespace) -> ContractResult:
    return ContractResult(
        "CPi_pinsker_constant",
        "skipped",
        "STUB — proof lands in commit paper-b Phase 2b-md.T6+C-Pi",
    )


@contract
def check_P10_refinement_monotonicity(args: argparse.Namespace) -> ContractResult:
    return ContractResult(
        "P10_refinement_monotonicity",
        "skipped",
        "STUB — proof lands in commit paper-b Phase 2b-md.P10",
    )


@contract
def check_L11_aggregator_deltaL(args: argparse.Namespace) -> ContractResult:
    return ContractResult(
        "L11_aggregator_deltaL",
        "skipped",
        "STUB — proof lands in commit paper-b Phase 2b-md.L11",
    )


# ---------------------------------------------------------------
# Runner
# ---------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--samples", type=int, default=1000)
    parser.add_argument(
        "--manifest", default="verify_b_t1.json",
        help="JSON manifest output path",
    )
    args = parser.parse_args()

    results = [c(args) for c in CONTRACTS]
    n_pass = sum(r.status == "pass" for r in results)
    n_fail = sum(r.status == "fail" for r in results)
    n_skip = sum(r.status == "skipped" for r in results)

    print(f"{'contract':<35} {'status':<10} message")
    print("-" * 80)
    for r in results:
        print(f"{r.name:<35} {r.status:<10} {r.message}")
    print("-" * 80)
    print(f"pass={n_pass}  fail={n_fail}  skipped={n_skip}")

    manifest = {
        "tool": "verify_b_t1",
        "tier": "B-T1",
        "seed": args.seed,
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
