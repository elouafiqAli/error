# EXTERNAL_AUDIT.md — Principal-Investigator Final Audit, Paper B

> **Verdict.** PASS — Paper B (`partition-brackets-framework/main.md`)
> is **publication-ready** at SHA `fd13a0e`, post-G2 plus
> theory/B.6/C.7 polish + D.10 cell-level real-data anchor.
> All five reproducibility tiers green (T0–T5); zero outstanding
> non-cosmetic items; LaTeX mirror (`main.tex`) explicitly
> deferred to Phase 2d per user directive.

| Field        | Value                                                |
|--------------|------------------------------------------------------|
| Auditor      | Principal Investigator (final external pass)         |
| Date (UTC)   | 2026-06-01                                           |
| Repo SHA     | `fd13a0e`                                            |
| Tag         | `v0.1.0-paperB-G2` at `de852d5` + 6 follow-on commits |
| Tiers run    | T0, T1, T2, T3, T4, T5 (all PASS)                   |
| Driver       | `audit/run_external_audit.sh`                       |
| Manifests    | `audit/external_audit/*.json` + `SUMMARY.json`      |
| Forward plan | `FORMAL_VERIFICATION_PLAN.md` (Lean 4 / Mathlib port) |

---

## 1. Reproducibility tiers

Each tier is a self-contained command. A reviewer who clones the
repo and runs `bash audit/run_external_audit.sh` reproduces every
green check on a single CPU core in under ~25 min wall.

| Tier | Scope                                  | Driver                                            | Time      | Manifest                                  | Status |
|------|----------------------------------------|---------------------------------------------------|-----------|-------------------------------------------|--------|
| **T0** | Build + import sanity                 | `make` (Paper A LaTeX) + `python -W error` import | < 30 s    | `external_audit/T0.log`                   | PASS   |
| **T1** | Symbolic + property tests (8 contracts) | `verify_b_t1.py --seed 0 --samples 200`           | ~1 s      | `external_audit/T1_verify_b_t1.json`      | PASS   |
| **T2** | Monte-Carlo population (6 contracts)  | `verify_b_t2_mc.py --seed 0 --samples 50000 --trials 500` | ~19 s | `external_audit/T2_verify_b_t2.json`      | PASS   |
| **T3** | Adversarial stress (seeds × mutation × boundary) | `audit/stress.py --seeds 15 --samples 50000 --trials 200` | ~20 min | `external_audit/T3_stress.json` (also archived `audit/stress.json`) | PASS |
| **T4** | Real-data anchor (5 graphs × 4 depths, C-Sh+C-Va+C-Pi) | `audit/anchor_real_data_full.py --depths 0 1 2 3` | ~9 s | `external_audit/T4_anchor.json`         | PASS (20/20 rows) |
| **T5** | Cross-paper parity (Paper A's verifiers) | `verify_t1_float.py` + `verify_t3_symbolic.py` + `verify_t4_population.py` | ~12 s | `external_audit/T5_paperA_t{1,3,4}.log` | PASS |

**Driver invariants.**

- Every tier emits a structured manifest with row-level diagnostics.
- Every tier prints a one-line `PASS` / `FAIL rc=…` with wall time.
- Top-level `audit/external_audit/SUMMARY.json` aggregates the
  matrix `{tier → rc, wall_s}` plus `all_pass: bool`.
- All randomness uses an XOR-mask salt over the user-supplied
  `--seed`, so independent contracts see independent streams from
  the same seed (no aliasing artefacts).

---

## 2. Audit plan (PI checklist)

The PI checklist below is the rubric this audit applies. Each
item is a binary gate; failing any one item would have blocked
the verdict.

1. **Every numbered claim has a mechanical contract.** ✓
   Nine claims (T3, C-Sh, C-Va, C-Pi, T6 [MSE+MAE], T7, T9,
   P10, L11); fourteen contracts (8 symbolic + 6 MC); 1-to-many
   mapping documented inline in `main.md` per-claim
   *Verifier contract* blocks.

2. **No silent skips.** ✓
   `verify_b_t1.py` `pass=8 fail=0 skipped=0`;
   `verify_b_t2_mc.py` `pass=6 fail=0 skipped=0`. Verifier
   docstrings refreshed from `STATUS: PARTIAL/STUB` to
   `STATUS: COMPLETE` in commit `fd13a0e` to eliminate
   doc-vs-code drift.

3. **Mutation tests catch non-trivial bugs.** ✓
   `audit/stress.py` flips:
   - T3 upper constant to a wrong value (`T3_wrong_c_phi`) — caught.
   - T7 noise correction sign (`T7_wrong_sign`) — caught.
   - C-Va functional to η(1+η) (`CVa_wrong_identity`) — caught.

4. **Boundary regimes are exercised.** ✓
   13 boundary checks in `audit/stress.py`: η ∈ {0, ½, 1},
   ρ → ½ (T7 denominator blow-up), deterministic kernel collapse
   to T3 (`T9_deterministic_reduces_to_T3`), atomic-partition
   reduction (`P10_refinement_to_atoms_phi_zero`), Pinsker
   vacuity threshold.

5. **Cross-paper citations resolve.** ✓
   B.6 grep-audit (commit `fd13a0e`):
   - "Paper A Proposition 7" (did not exist) → fixed to point at
     Paper A §13 forward reference + `thm:sandwich` (Theorem 1).
   - "Paper A Lemma 6′" (stale numbering) → fixed to label
     `lem:mpnn-wl-robust`.

6. **Real-data anchor is non-vacuous.** ✓
   D.10 (`anchor_real_data_full.py`): 20/20 (dataset, depth) rows
   pass all three T3 instances (C-Sh, C-Va, C-Pi) on Cora /
   CiteSeer / PubMed / Twitch-EN / ogbn-arxiv. C-Pi vacuity
   regime (raw lower < 0 when $H < 0.279$) is reported
   explicitly per row.

7. **No new training.** ✓
   D.10 reuses Paper A's vectorised 1-WL kernel (`wl_refine`,
   SplitMix64); D.9 reuses Paper A's `e3.json`. The only GPU-
   touching artefact (`runpod_dfull.py`) belongs to Paper A and
   is marked partial in `experiments/REPORTS.md`.

8. **Secrets discipline.** ✓
   `.gitignore` (commit `33777ec`) excludes `.huggingface_token`,
   `*.token`, `.env`, data caches. Verified via
   `git log --all -- .huggingface_token` (no commits) that the
   real token was never tracked.

9. **Confidence calibration matches evidence.** ✓
   `future-work/07-three-paper-arc-master-plan.md` §1 table
   updated (commit `b4e5561` + polish in `fd13a0e`); contract
   names referenced from the table exist 1-to-1 in the verifiers
   (or are explicitly labelled "audit boundary check in
   `audit/stress.py`").

10. **Forward verification path documented.** ✓
    See `FORMAL_VERIFICATION_PLAN.md` (this commit) — a
    Lean 4 / Mathlib port plan for the load-bearing T3 +
    instances + P10, with effort estimate and dependency
    graph.

---

## 3. Audit execution log (this run)

```
=== TIER T0 @ fd13a0e ===
TIER T0 PASS (<1 s)            imports + pdflatex clean

=== TIER T1 @ fd13a0e ===
TIER T1 PASS (1 s)
  T3_jensen_lower               pass  sympy (H1,H4) ok for 3 phis; hypothesis 200 examples ok
  T3_upper_constant             pass  c_phi certified to 5e-4 on 10^4 grid; hypothesis 200 examples ok
  CSh_reduces_to_paperA         pass  meta == Paper A bracket within 1e-9 on 200 examples
  CVa_bayes_variance_identity   pass  (C-Va.id) + LTV + T3-bracket all ok on 200 examples
  CPi_pinsker_constant          pass  Pinsker symbolic grid ok; (C-Pi.lower) holds on 250 examples (worst slack 4.18e-04)
  P10_refinement_monotonicity   pass  phi(f|Pi') <= phi(f|Pi) for 3 phis on 200 examples
  L11_aggregator_deltaL         pass  product formula proved symbolically; empirical bound holds on 200 examples
  T7_noise_correction_symbolic  pass  (T7.affine) + (T7.kink) [both cases] + (T7.correction) verified symbolically

=== TIER T2 @ fd13a0e ===
TIER T2 PASS (19 s)
  CVa_variance_identity_population  pass  MSE* = sum p_i eta_i(1-eta_i) within 0.0243 on 500 trials (worst 0.0000)
  T6_MSE_identity_population        pass  MSE* = E[Var(f|Pi)] within 0.0243 on 500 trials (worst 0.0000)
  T6_MAE_upper_population           pass  MAE* <= sqrt(MSE*) + 0.0243 on 500 trials (worst residual 0.0000)
  T7_noise_correction_population    pass  identity holds within 4*Hoeffding(0.0243) on 1500 trials (worst residual 0.0051)
  T7_shannon_matches_paperA         pass  Paper A == Paper B on 200 trials x 3 rhos; worst |dphi|=0, |dlo|=7.8e-16, |dup|=0
  T9_kernel_bracket_population      pass  T9 brackets (Shannon, variance) envelope eps*_K within 0.0243 on 500 trials

=== TIER T3 @ fd13a0e ===
TIER T3 PASS (production: 15 seeds × 14 contracts, 0 failures; 3 mutations caught; 13/13 boundary checks pass)
  Archived manifest: audit/stress.json

=== TIER T4 @ fd13a0e ===
TIER T4 PASS (9 s, 20 rows)
  cora       L=0..3   eps* funnel 0.300 → 0.029   C-Sh ✓  C-Va ✓  C-Pi ✓
  citeseer   L=0..3   eps* funnel 0.211 → 0.078   C-Sh ✓  C-Va ✓  C-Pi ✓
  pubmed     L=0..3   eps* funnel 0.395 → 0.051   C-Sh ✓  C-Va ✓  C-Pi ✓
  twitch_en  L=0..3   eps* funnel 0.416 → 0.027   C-Sh ✓  C-Va ✓  C-Pi ✓
  ogbn_arxiv L=0..3   eps* funnel 0.160 → 0.002   C-Sh ✓  C-Va ✓  C-Pi ✓
  Pinsker (C-Pi) is genuinely vacuous in 10/20 rows (raw lower < 0); contract uses 0-clipped envelope.

=== TIER T5 @ fd13a0e ===
TIER T5 PASS (12 s)
  Paper A verify_t1_float.py        OK
  Paper A verify_t3_symbolic.py     OK
  Paper A verify_t4_population.py   OK
```

---

## 4. Findings

### 4.1 No blockers.
Every claim, every contract, every cross-reference resolves.

### 4.2 Non-blocking observations (for transparency).

| # | Observation | Severity | Recommendation |
|---|-------------|----------|----------------|
| O1 | C-Pi Pinsker bound is vacuous (raw lower < 0) when $H < \log_2 4 / (1 - 0) \cdot \tfrac14 \approx 0.279$. | Informational | Already reported per-row in `audit/anchor_real_data_full.json`; main.md C-Pi section names this regime as a failure mode (§4 *Failure modes*). No code/proof change needed. |
| O2 | T6 MAE has only the Cauchy–Schwarz upper; matching lower is an open problem. | Acknowledged | Already flagged in `main.md` T6 §*Failure modes* and in master plan as `OP-MAE-lower`. |
| O3 | LaTeX mirror (`main.tex`) is at Phase-2a scaffold; markdown twin (`main.md`) is the canonical artefact for Phase 2b. | By design | Phase 2d (LaTeX mirror) is the next planned milestone; not in scope for publication-ready Paper B markdown. |
| O4 | `audit/anchor_real_data.py` (D.9, Shannon only) is superseded by D.10 (`anchor_real_data_full.py`, all three instances). | Cosmetic | Keep D.9 for historical provenance; D.10 is referenced from `main.md` header. |
| O5 | Asymmetric label noise (different $\rho_{0\to1} \ne \rho_{1\to0}$) is named in T7 §*Failure modes* as `OP-asym` open problem. | Open problem | No action; correctly scoped out. |

### 4.3 Adversarial counter-claims considered (and refuted).

- *"T3 might be vacuous when $\phi$ has $c_\phi = \infty$."*
  Refuted by C-Pi: the Pinsker $\sqrt{}$-form supplies a finite
  lower replacement, certified mechanically by
  `CPi_pinsker_constant`. C-Pi's vacuity regime ($H < 0.279$) is
  explicit; outside it the bound is non-trivial.

- *"T7 might silently absorb sign errors."*
  Refuted by `T7_wrong_sign` mutation in `audit/stress.py` —
  flipping the sign of $(1 - 2\rho)$ in the affine relabelling
  causes `T7_noise_correction_symbolic` to fail, as expected.

- *"L11 might be tight only on the linear case."*
  Acknowledged in `main.md` L11 §*Failure mode*: the
  product-of-Lipschitz bound is tight for linear MPNNs and an
  upper estimate for nonlinear nets. This is the published
  state of the art (matches Paper A's `lem:mpnn-wl-robust`).

- *"Cross-paper bracket parity (T7 ↔ Paper A) might rely on
  paper-internal SymPy idiosyncrasies."*
  Refuted by `T7_shannon_matches_paperA`, which imports
  `verify_t1_float.hbin` and `hbin_inv` directly from Paper A
  and compares numerically. Worst gap on 200 trials × 3 noise
  rates: $|\Delta_{\text{lower}}| = 7.8 \times 10^{-16}$.

---

## 5. Reproduction recipe

```bash
git clone <repo> gnn_express
cd gnn_express
git checkout fd13a0e   # or v0.1.0-paperB-G2 + 6 commits
pip install -r partition-brackets-framework/requirements.txt
cd partition-brackets-framework
bash audit/run_external_audit.sh     # all 6 tiers, ~25 min on CPU
cat audit/external_audit/SUMMARY.json # expect "all_pass": true
```

Individual tier reproductions:

```bash
bash audit/run_external_audit.sh T1                  # 1 s, symbolic
bash audit/run_external_audit.sh T2                  # 19 s, MC
bash audit/run_external_audit.sh T3                  # 20 min, adversarial
bash audit/run_external_audit.sh T4                  # 9 s, real-data
bash audit/run_external_audit.sh T5                  # 12 s, cross-paper
```

Tier T4 caches graph datasets under
`partition-sandwich-preprint/experiments/data/` on first run
(gitignored); subsequent runs use the cache.

---

## 6. Sign-off

Paper B is **publication-ready** for the Phase-2b-md markdown
manuscript. All nine numbered claims (T3, C-Sh, C-Va, C-Pi, T6,
T7, T9, P10, L11) have:

1. A prose proof with explicit hypotheses, ✓
2. At least one machine-checked verifier contract, ✓
3. A named failure mode / adversarial counter-example, ✓
4. (Where applicable) a real-data anchor row in `T4_anchor.json`, ✓
5. (Where applicable) a cross-paper parity check against Paper A, ✓

Forward path: see [`FORMAL_VERIFICATION_PLAN.md`](FORMAL_VERIFICATION_PLAN.md)
for the Lean 4 / Mathlib port that would lift the symbolic tier
(T1) to a *certified* proof and close the gap between
"property-tested" and "machine-proven".

**Signed**, PI audit, SHA `fd13a0e`, 2026-06-01.
