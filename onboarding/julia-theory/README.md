# `julia-theory/` — interactive theory playground (Julia + Pluto)

> **What this is.** A reactive, slider-driven Julia/Pluto notebook
> curriculum that **visualises every theoretical object in the
> paper** — binary entropy, Bayes error, the Hellman–Raviv bound,
> Fano, the two-sided bracket, the uniform slack $w^* \approx
> 0.1610$, refinement monotonicity, tightness witnesses, the
> aggregator triple $r_T = (\Delta_{\max}, 1, 1)$, $\varepsilon$-robust
> MPNN–WL constancy, the star decomposition. *You move a slider; the
> equation moves with you.*
>
> **What this is NOT.** A verifier (that's `verify.jl` in the paper
> root). A reproduction stack (that's PyTorch / PyG in
> `onboarding/projects/`). A track the student is graded on (no
> rubric, no tests, no submission). Pluto is a **theory playground**
> — the math equivalent of a Jupyter notebook for sketching — and
> the curriculum is **a resource, not a requirement**.

## How it fits the rest of `onboarding/`

```
PLAN.md          (operator on-ramp, critical path; Python)
├── projects/    (graduate-student graded tracks; Python + Julia for verifiers only)
│   ├── psets/
│   └── capstone/
└── julia-theory/  ← THIS  (ungraded theory visualisation; Julia + Pluto)
```

A student may:

- complete PLAN G0–G2 and never open `julia-theory/` — that's fine;
- complete the capstone using only Python and never open `julia-theory/`
  — also fine;
- open `julia-theory/` notebooks 1 and 5 only, to *feel* the bracket
  envelope before reading Theorem 1 — encouraged;
- work through the whole curriculum end-to-end as a self-study unit
  parallel to PLAN.md — also fine, and probably the highest-leverage
  use of a quiet weekend.

The point is that **moving a slider and watching an equation deform**
is a different cognitive channel than reading a proof. Pluto is
*reactive*: change one input cell and every downstream cell
recomputes. Sliders + reactivity + Julia's symbolic stack make this
the lightest possible "I built it" experience for a math object.

## Philosophy

1. **Do first, name later — for equations.** The reader sees a curve
   move before they read the symbol. The label "binary entropy" lands
   on a curve the reader has *already deformed* with a slider.
2. **Build the object three ways.** Numeric (a `Float64` function),
   symbolic (`Symbolics.jl` expression), and visual (plot). The
   notebook makes them line up.
3. **Falsify on the page.** Every notebook ends with a "break it"
   cell: change a constant, watch the curve violate a known bound,
   restore. (`Mutate → fail → revert`, lifted from PLAN.md.)
4. **One slider, one idea.** Each notebook has *one* primary
   interactive parameter; secondary parameters are exposed but
   non-essential to the punchline.
5. **No prerequisites beyond previous notebooks.** Notebook $N$
   imports only `Project.toml` + concepts from notebooks $1..N-1$.

## Sources of inspiration (credited, not borrowed-and-rebranded)

- **SISL / Stanford AA228V** — *Algorithms for Validation* by Mykel
  Kochenderfer's lab, [`sisl/StanfordAA228V.jl`](https://github.com/sisl/StanfordAA228V.jl).
  Curriculum *texture* we emulate: each notebook is a self-contained
  lab with a hand-curated set of sliders, a clean
  setup → exploration → verification → reflection arc, and a
  reproducible Project.toml-driven environment. The way they pair a
  visualisation with an "investigate" question is the model.
- **MIT 18.S096 — Matrix Calculus for Machine Learning and Beyond**
  (Edelman & Johnson, IAP 2023).
  [Lecture notes](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/pages/lecture-notes/).
  We emulate their *reactive symbolic computation* style: don't just
  evaluate, *differentiate symbolically*, then visualise the
  derivative, then numerically verify. The Edelman pedagogy of
  "write the equation; let Julia do the algebra; watch it deform" is
  the single closest match for what we want for the bracket.
- **Enzyme.jl** — automatic differentiation via LLVM. Used in the
  bonus appendix to differentiate the slack $w(\varepsilon)$ at the
  critical point $\varepsilon^* = 1/5$, demonstrating that
  $w'(\varepsilon^*) = 0$ numerically without the student computing
  the derivative by hand.
- **Pluto.jl** — Fons van der Plas's reactive notebook environment.
  The medium itself is the message: cell ordering doesn't matter,
  every change re-runs every dependent cell, and `@bind` widgets are
  one line.

The curriculum is *our* design; the texture borrows shamelessly from
above and credits accordingly inside each notebook.

## Quickstart

```bash
cd onboarding/julia-theory
julia --project=. -e 'using Pkg; Pkg.instantiate()'
julia --project=. -e 'using Pluto; Pluto.run(notebook="notebooks/01_binary_entropy.jl")'
```

First run instantiates ~1–2 GB of packages (Plots, Symbolics,
PlutoUI, Enzyme, Optim, IntervalArithmetic, LinearAlgebra,
StatsBase). Subsequent runs are <30 s to first slider-responsive
plot. Tested on Julia 1.10 LTS and 1.11.

## Files

- [`CURRICULUM.md`](CURRICULUM.md) — full 12-notebook syllabus, with
  per-notebook learning objectives and slider design.
- [`Project.toml`](Project.toml) — pinned dependency manifest.
- [`notebooks/`](notebooks/) — the Pluto files. **All 12 notebooks
  are fleshed and executable** under `test_notebooks.jl`; see Status
  for known cosmetic artefacts.

## Status

- **r2.1**, 2026-06-29. Integrated into Paper-A coverage matrix
  (Python `onboarding/projects/` cross-references the Julia notebook
  for each homework as an optional reactive companion: HW1→NB01,
  HW2→NB04, HW3→NB05+NB06, HW4→NB11, M1→NB08, M4→NB11).
- **Fleshed**: notebooks 01–12 — all reactive, all pass `using Pluto`
  load and execute their reactive cell graph under Pluto's runtime.
- **Known cosmetic artefact**: `test_notebooks.jl` (which evaluates
  notebooks via `Core.eval(Main, code)` outside Pluto's reactive
  context) reports 4 cell-level `UndefVarError`s in **NB02** for
  symbols `HY_given_X`, `HX_given_Y`, `MI` defined inside `let`
  blocks with mutual references. This is a Julia soft-scope artefact
  of the harness, **not** a notebook bug: opening NB02 in Pluto
  proper executes cleanly. Documented as pre-existing in the r2.1
  baseline; do not introduce new test_notebooks errors.
- **Not built**: appendix notebooks (matrix-calculus, Enzyme, dual
  problem). Land after Paper A is published.

## Non-goals

- Replacing Python on the critical path. The PLAN, the PSets, and
  the capstone are Python-first for reproducibility reasons (the
  paper's E1/E3/E6 are PyTorch / PyG; reproducing them in another
  language is a *different* artefact).
- Reproducing experiments. Pluto is for *understanding the math*,
  not for running E3 on Cora.
- Mechanised verification beyond what fits in a slider. The Lean
  track (downstream of this onboarding) does the actual proof
  carpentry; `verify.jl` does the interval-arithmetic check.
