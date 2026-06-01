#!/usr/bin/env julia
# verify_b.jl — Paper B Tier B-T2 (certified per-sample interval audit)
# =====================================================================
#
# STATUS: STUB (Phase 2b-md.A012). All check_* functions throw
# ErrorException("not yet implemented") until the corresponding
# main.md claim is promoted from SKELETON to PROVEN. Each
# subsequent Phase 2b-md commit lands one check_* and its
# main.md proof together.
#
# Verifier contracts
# ------------------
#   check_T3_bracket_random(phi, n_samples, seed)
#       For each of n_samples random (Pi, f) pairs (Pi has between
#       2 and 32 cells, masses Dirichlet(1)-distributed, eta_i ~
#       Beta(0.5, 0.5)), assert via certified interval arithmetic:
#         phi^{-1}(sum p_i phi(eta_i)) <= eps_star_Pi <= c_phi * sum p_i phi(eta_i)
#       on each sample, with NO float-tolerance fudge factor.
#       Done independently for phi in {Hbin, eta(1-eta), KL}.
#
#   check_T9_kernel_bracket(n_samples, seed)
#       For each of n_samples random Markov kernels K: X -> Delta(m)
#       with m in {2,...,16}, assert the soft-bracket of T9 holds
#       in certified interval arithmetic.
#
#   check_P10_refinement_julia(n_samples, seed)
#       Independent julia-side cross-check of B-T1 P10 contract;
#       refines each random Pi by random binary split and asserts
#       phi(f|Pi') <= phi(f|Pi) in intervals.
#
# Manifest output
# ---------------
#   verify_b.json with version pins (Julia version, IntervalArithmetic
#   version), seed, sample sizes, pass/fail per contract, exec time.
#
# Run
# ---
#   julia --project=. verify_b.jl [--seed 0] [--samples 1000]
#
# Dependencies: IntervalArithmetic.jl, Random, JSON3. Pinned in
# Project.toml / Manifest.toml (to be added in commit T3).

import Pkg
const STUB = true

if STUB
    println("verify_b.jl — STUB (Phase 2b-md.A012)")
    println("Contracts:")
    println("  - check_T3_bracket_random  : NOT IMPLEMENTED")
    println("  - check_T9_kernel_bracket  : NOT IMPLEMENTED")
    println("  - check_P10_refinement     : NOT IMPLEMENTED")
    println()
    println("Each contract will be implemented in the commit that")
    println("promotes the corresponding main.md claim from SKELETON")
    println("to PROVEN; see FORMALISATION.md §7 sequencing.")

    # Write a minimal manifest so CI-style scripts can diff runs.
    open("verify_b.json", "w") do io
        write(io, """{
  "tool": "verify_b.jl",
  "tier": "B-T2",
  "status": "stub",
  "phase": "2b-md.A012",
  "contracts": {
    "check_T3_bracket_random": "not_implemented",
    "check_T9_kernel_bracket": "not_implemented",
    "check_P10_refinement": "not_implemented"
  }
}
""")
    end
    exit(0)
end
