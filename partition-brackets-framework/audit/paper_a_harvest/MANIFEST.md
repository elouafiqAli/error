# Paper-A harvest manifest

> **Policy.** Paper A (`../../../partition-sandwich-preprint/`) is under
> review and is *read-only* from Paper B's perspective. This directory
> contains immutable snapshots of three Paper-A JSON result files so
> that Paper B can cite real-data anchors without depending on a
> moving target. Re-deriving these numbers requires re-running Paper-A
> experiments; the snapshots here are the auditable source-of-truth
> for the corresponding Paper-B footnotes.

## Provenance

| Field | Value |
|-------|-------|
| Paper-A snapshot SHA  | `e8763fe` |
| Paper-A snapshot date | 2026-06-01 (UTC) |
| Snapshot host        | local mac dev workspace |
| Paper-A status       | under review; awaiting `e3d_arch_full` GPU completion |

The Paper-A SHA above is the last commit that touched
`partition-sandwich-preprint/` at snapshot time. The `e3d_arch_full`
in-flight experiment is *not* harvested.

## Snapshots

Source files live in `partition-sandwich-preprint/experiments/results/`
which is `.gitignore`'d in Paper A — therefore the sha256 hashes below
are the only cryptographic anchor.

| Snapshot file              | Source                                  | sha256       | Bytes |
|----------------------------|-----------------------------------------|--------------|-------|
| `eK.snapshot.json`         | `…/results/eK.json`                     | `20ae9e7c…`  |  2078 |
| `e7.snapshot.json`         | `…/results/e7.json`                     | `7df44a84…`  |  2003 |
| `e3e.snapshot.json`        | `…/results/e3e.json`                    | `f0411d98…`  |  7915 |

Full hashes (re-verify with `shasum -a 256 *.snapshot.json`):

```
f0411d98d75cc0c9c674ba9ed37b5c6cf527c674629d2446d76584c3a3e80902  e3e.snapshot.json
7df44a847ed6bea9faf919feecf8d31819ab56bb7b53373e19423915ee61aca9  e7.snapshot.json
20ae9e7cf116017675fe9b4a046bb85472adb49edb53cbdcfd3593fa0ffbf0b0  eK.snapshot.json
```

## Per-snapshot mapping to Paper B claims

### `eK.snapshot.json` — Kochenderfer falsification protocol
- **Paper-A producer:** `experiments/eK_falsification_protocol.py`
- **Paper-A commit pedigree:** 4 commits, headline `6293e8c` ("Phase 1d: E-K Kochenderfer falsification/verification protocol")
- **Shape:** 4 τ-levels × 4 source experiments (E1, E2, E3, E6) → 102 rows
- **Paper-B claim anchored:** §0.5 Prop 0.4 + Appendix B.2 stress tier —
  an independent τ-thresholded falsifier corroborating the mutation-screen
  result `ρ_M = 1` (`audit/external_audit/T3_stress.json :: mutation_test.all_caught`).
- **Headline derived numbers** (see `harvest_aggregate.py :: harvest_eK`):
  - At τ = 0.10, source E6 falsifies **50 / 50** rows (strongest signal).
  - At τ = 0.25, source E3 verifies **20 / 27** rows (asymptotic stability).
  - Totals across 4 sources × 4 τ: **121 falsified, 89 verified, 198 inconclusive** (408 = 102 rows × 4 τ-levels).

### `e7.snapshot.json` — Proposition 7 concentration on Adult
- **Paper-A producer:** `experiments/e7_pop_concentration.py`
- **Paper-A commit pedigree:** 7 commits, headline `ea6b1e9`
  ("E7 audit fixes — bootstrap, tighter Hoeffding, drop n=45k")
- **Shape:** 7 subsample sizes n ∈ {200 … 20000}, K = 400 bootstrap reps,
  m = 16, α = δ_conf = 0.05, dataset = Adult
- **Paper-B claim anchored:** Proposition 0.4 (B-T2 McDiarmid form) —
  real-data witness that the McDiarmid / Hoeffding halfwidth is
  *strictly conservative* on a UCI dataset, mirroring the synthetic
  4× inflation argument.
- **Headline derived numbers** (see `harvest_aggregate.py :: harvest_e7`):
  - All 7 rows satisfy `coverage == 1.0 ≥ 1 − α = 0.95`.
  - `bound / delta_p95` ratio is **2.53 – 2.94** across all subsample sizes
    (geomean **2.72**); i.e. the Hoeffding bound is consistently **≈ 2.7×**
    the empirical p95 — the same "strictly conservative by a small
    constant factor" pattern as our `4 h ≈ 3.4 × h_union`.
  - `delta_mean` is monotone-decreasing in `n` (Gate `delta_mean_monotone_in_n`: PASS).

### `e3e.snapshot.json` — Lemma 6′ in-vivo on real graphs
- **Paper-A producer:** `experiments/e3e_robust_lemma.py`
- **Paper-A commit pedigree:** 1 bundled commit `af61ed6`
  ("vectorised WL kernel, E3 sub-experiments (E3a/b/d/e/f), …")
- **Shape:** 2 datasets (cora, …), L = 3, d_hidden = 32, δ ∈ {0, 0.001, 0.01, 0.1, 1.0}
- **Paper-B claim anchored:** Lemma L11 §6 — real-graph empirical
  *looseness* of the aggregator-typed Lipschitz bound. The bound holds
  in every row (`gates` pass), but is **6–7 orders of magnitude loose
  on real graphs**. This is an honest disclaimer footnote, not a
  victory headline.
- **Headline derived numbers** (see `harvest_aggregate.py :: harvest_e3e`):
  - Worst looseness on the (cora, citeseer) × δ × L grid: bound = **3.71 × 10⁷**,
    observed D = **4.03**, ratio = **9.23 × 10⁶** (~7 orders of magnitude).
  - The bound is *never* violated across the entire (dataset × δ × L) grid,
    so L11 is *correct, just conservative on real graphs*.

## Reproducibility

```bash
# Re-derive the headline numbers from the snapshots (no Paper-A needed):
cd partition-brackets-framework/audit/paper_a_harvest
python3 harvest_aggregate.py
#   -> writes harvest_aggregate.json with the per-claim summaries
#      that the Paper-B main.md footnotes [^bk-eK], [^bk-e7], [^bk-e3e]
#      cite by name.

# Re-derive against the LIVE Paper-A JSONs (requires Paper-A worktree
# at SHA e8763fe or newer):
shasum -a 256 ../../../partition-sandwich-preprint/experiments/results/{e7,eK,e3e}.json
# Compare with hashes table above; mismatch ⇒ Paper-A advanced past
# snapshot, re-snapshot deliberately.
```

## Discipline

- **No edits to Paper A.** This directory is *export-only* from Paper A.
- **Snapshots are immutable.** If Paper A re-runs an experiment, a new
  snapshot file (`eN.snapshot.YYYYMMDD.json`) is created; the old one
  is preserved for audit history.
- **Citations are derived numbers, not raw JSON.** Paper B's footnotes
  cite the *aggregated* fields produced by `harvest_aggregate.py`, so
  a reviewer can re-verify a number with `python3 harvest_aggregate.py`
  in ≤ 1 s, without touching Paper A.
