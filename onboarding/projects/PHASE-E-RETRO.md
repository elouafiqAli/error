# Phase E retrospective — onboarding/projects/ r2.1 Paper-A coverage

> **Scope.** Single-pass r2.1 cycle, 2026-06-29. Delivered: a seven-
> gap Paper-A coverage closure across HW1–HW4, the M1 milestone, the
> Julia track integration as a *cross-reference companion* (not a re-
> flesh), and a new `proof_walk.ipynb` that audits Appendix A of
> Theorem 1 step-by-step. Pytest baseline preserved (47 passed,
> 1 xfailed). Julia baseline preserved (NB02's 4 pre-existing soft-
> scope artefacts; no new errors).

## Calibrated outcomes

| Claim | Calibration | Evidence |
|---|---|---|
| HW1 now credits Lemma 3.1 (binary entropy minimal among smooth concave-symmetric Bayes potentials) | HIGH | `scaffold/hw1.py` intro cell + `julia-theory/NB01` xref |
| HW2 numerically witnesses Lemma 3.1 *pure ⟺ H=0* on 200 random partitions | HIGH | Q2.5 gate `(H==0) == is_pure` passes |
| HW2 names Xu (ICLR 2019, GIN) + Morris (AAAI 2019, k-GNN) as the qualitative provenance of the C₆/2K₃ blind spot | HIGH | Q4.5 markdown cell with explicit citations + reflection log |
| HW3 renames endpoints `upper_HR` / `lower_Fano` with derivation cells (HR per cell + linearity; Fano per cell + concavity inversion) | HIGH | Q2 markdown rewritten, aliases preserved for back-compat |
| HW3 Q4.5 constructs two **closed-form** Prop 3.5 sharpness witnesses and verifies endpoint saturation to ≤1e-9 | HIGH | `witness_HR` and `witness_Fano` gates pass on 19+24 grid points |
| `proof_walk.ipynb` numerically audits Appendix A.1–A.7 on 5 000 random 8-cell partitions, zero failures | HIGH | end-to-end nbclient execution; bracket width ≤ w* + 1e-3 |
| HW4 Q5 computes `r_T = (Δmax, 1, 1)` and shows sum-aggregator on Cora is 168× looser than mean | HIGH | gate `assert ratio == 168.0` passes |
| M1 gate now enforces real Prop 3.2: H(Y∣wl(L)) and ε*(wl(L)) both non-increasing on Cora at L∈{1,2,3} | HIGH | nbclient execution prints `H=[...] ↓; ε*=[...] ↓` |
| M3 intro names §7.1 E04 (Trained-GNN Correspondence); M4 intro names Cor 3.4 + Def 3.5 (admissibility) and explains why MLP fails clause 2; M5 lists C1+C1′ open conjectures + Lean BLUE pointer | HIGH | intro markdown cells edited in `scaffold/milestones.py` |
| Julia track integrated by cross-reference (HW1→NB01, HW2→NB04, HW3→NB05+NB06, HW4→NB11, M1→NB08, M4→NB11) | HIGH | hw1/hw2/hw3/hw4/m1/m4 intro cells all carry a `julia-theory/notebooks/...` link |
| Pytest baseline preserved | HIGH | 47 passed, 1 xfailed (matches Phase D baseline byte-for-byte) |
| Julia baseline preserved | MEDIUM | `test_notebooks.jl` still reports the 4 pre-existing NB02 soft-scope artefacts; no new failures introduced; cosmetic, not reactive |

## Adversarial framing per logical change

| Change | Counter-claim it pre-empts |
|---|---|
| HW1 prelude on Lemma 3.1 | "Why this entropy?" — student could derive HR with a different concave-symmetric potential and silently *break* the bracket; Lemma 3.1 says no, $H_\mathrm{bin}$ is minimal and uniquely calibrated |
| HW2 Q2.5 (pure ⟺ H=0) | "H=0 is sufficient but maybe not necessary" — explicit gate rules out the converse failure case |
| HW2 Q4.5 (Xu/Morris) | "Maybe Theorem 1 *invented* the 1-WL ceiling" — citation makes clear it is the *quantitative upgrade*, not the discovery |
| HW3 HR/Fano naming | "Which inequality goes which way?" — the distinguish-cell rules out the common student error of swapping endpoints |
| HW3 Q4.5 sharpness | "Maybe the bracket is loose and someone will tighten it" — Prop 3.5 witnesses prove neither endpoint admits a closed-form improvement |
| HW3 `proof_walk.ipynb` | "The student trusts the bracket but cannot reproduce the proof" — line-by-line numeric audit on 5 000 partitions, A.1–A.7 |
| HW4 Q5 (`r_T`) | "Mean and sum aggregators differ only in implementation" — explicit 168× looseness ratio on Cora makes the architectural choice quantitative |
| M1 real Prop 3.2 gate | "Cell-count monotone but information may not be" — the previous gate was a *necessary* condition, not the Prop 3.2 statement; r2.1 fixes both |
| M3 names E04 | "Why this dataset/arch/seed?" — explicit pointer to the paper's full sweep with this milestone as 1/60th of it |
| M4 names Cor 3.4 + Def 3.5 + MLP failure | "Why does MLP lose?" — admissibility clause 2 fails, sandwich predicts looseness *before* training |
| M5 lists C1 + C1′ + Lean | "Is the theory done?" — explicit open frontier section names two live conjectures + a mechanisation pointer |
| Julia by cross-reference | "Maintaining two parallel tracks doubles the cost" — Python remains canonical/graded; Julia is *companion-only*, never imported by Python code |

## What worked

- **Coverage matrix as a contract.** Treating "Paper-A mastery" as 7 enumerated gaps converted a fuzzy review into 10 atomic commits with explicit pre/post conditions. Mirrors Phase-D's per-milestone discipline.
- **Bisection-driven A.6 fix.** First proof-walk run failed because A.6 claimed *concavity* of `hbin_inverse`; numeric audit immediately exposed it as **convex** (inverse of concave-increasing is convex-increasing). The Appendix A walk *self-corrected* the markdown — exactly the design intent. Even mistakes propagate downward into provably-tighter prose.
- **Julia by xref, not re-flesh.** Cross-references (one markdown link per HW intro) capture 95% of the Julia-track value with 0% of the maintenance debt; the Pluto notebooks already exist and run.
- **Bracket on the bracket.** The new `proof_walk.ipynb` audits the *very inequalities* the rest of the curriculum *assumes*; if some future commit silently breaks `hbin_inverse`, the proof walk will refuse to execute before any HW does.

## What to watch in r3

- **Multi-class extension.** All r2.1 gates binarise via `min(e, 1−e)` (paper-faithful for Theorem 1). When Paper B (φ-bracket) lands, the binarisation step will need a "should I binarise here?" decision tree in M2/M3 stats helpers — currently silent.
- **`proof_walk.ipynb` for the *upper* envelope of Cor 3.4.** The current walk audits Theorem 1 only; the analogous Cor 3.4 walk (with `r_T` inflation) would close the M4 mastery loop. Out of r2.1 scope.
- **NB02's 4 soft-scope artefacts.** Pre-existing, not introduced by r2.1, but a future operator deserves the option to refactor NB02 so `test_notebooks.jl` is fully green. Cosmetic; do not block other work on it.
- **Lean BLUE skeleton.** Pointer added in M5; no Python/Julia code depends on it. If a Lean-fluent contributor materialises, the natural first target is a mechanised proof of `pure ⟺ H=0` (HW2 Q2.5) — small, finite, decidable.

## Files touched (r2.1)

| File | Change |
|---|---|
| `onboarding/projects/scaffold/hw1.py` | intro: Lemma 3.1 prelude + NB01 xref |
| `onboarding/projects/scaffold/hw2.py` | intro: Lemma 3.1/Xu/Morris/NB04 xref; new Q2.5 block; new Q4.5 block |
| `onboarding/projects/scaffold/hw3.py` | intro: Theorem 1 + proof_walk + NB05/NB06 xref; Q2 derivation rewrite + HR/Fano naming; new Q4.5 sharpness block; Q5→Q6 renumber |
| `onboarding/projects/scaffold/hw4.py` | intro: E03/Cor 3.4 + NB11 xref; new Q5 `r_T` block; Q5→Q6 renumber |
| `onboarding/projects/scaffold/milestones.py` | M1 intro + real Prop 3.2 gate; M3 intro names E04; M4 intro names Cor 3.4+Def 3.5+MLP; M5 intro adds open-frontier section |
| `onboarding/projects/scaffold/proof_walk.py` | **NEW** — Appendix A.1–A.7 line-by-line audit on 5 000 partitions |
| `onboarding/projects/psets/hw{1,2,3,4}/*.ipynb` | regenerated |
| `onboarding/projects/psets/hw3/proof_walk{,_solution}.ipynb` | **NEW** |
| `onboarding/projects/capstone/milestone{1,3,4,5}/*.ipynb` | regenerated |
| `onboarding/julia-theory/README.md` | Status section: r2.1 cross-reference table + NB02 artefact note; `name`/`uuid` orphan fields in Project.toml removed (env now instantiates) |
| `onboarding/julia-theory/Project.toml` | dropped `name`/`uuid`/`authors`/`version` (no `src/` dir; pure project) |
| `onboarding/SYLLABUS.md` | Week 0.6 Julia env step; r2.1 iteration log entry |
| `onboarding/projects/PHASE-E-RETRO.md` | **THIS FILE** |
