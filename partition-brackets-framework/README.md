# Paper B — Partition Brackets: A Framework with Entropy, Variance, and Noise-Robust Instances

**Status: SCAFFOLD (Phase 2a).** All numbered statements are
skeletons with `\status{...}` markers; proofs are deferred to
Phase 2b (theory) and instances to Phase 2c. Do not cite or
distribute until Gate G2 closes.

## Thesis

The partition is the universal expressivity bottleneck;
[Paper A](../partition-sandwich-preprint/main.tex)'s elementary
binary-entropy bracket is one face of a one-line recipe — the
$\bar\varphi$-bracket meta-theorem — that applies to every
concave score functional $\bar\varphi$ with matched loss
$\ell_{\bar\varphi}$.

## Layout

- `main.tex` — paper source.
- `main.bib` — bibliography. `paperA` self-citation is the
  load-bearing reference; all results that "recover" or "match"
  Paper A go through it.
- `Makefile`, `tmlr.sty`, `tmlr.bst`, `fancyhdr.sty` — TMLR
  style files duplicated from Paper A (so this paper compiles
  standalone without symlinks).
- `experiments/` — to be populated in Phase 2c / Phase 3 with
  E8 (variance bracket overlay on Paper A partitions) and E9
  (label-noise stress test). Results gitignored under
  `experiments/results/`.

## Phase plan (mirror of `future-work/07-three-paper-arc-master-plan.md`)

| Phase | Output                                          | Gate |
|-------|-------------------------------------------------|------|
| 2a    | Scaffold (this commit): structure + statements  | —    |
| 2b    | Full proofs of T3, T4, T8, refinement prop      | G2   |
| 2c    | Instances + MPNN aggregator-typed lemma         | —    |
| 2d    | `main.md` KaTeX twin + clean build              | —    |
| 3     | Experiments E8, E9 (zero new training)          | G3   |
| 4     | Writing pass + section budget enforcement       | G4   |

## Build

```bash
make            # pdflatex -> bibtex -> pdflatex x 2
make clean
make distclean
```

The build will fail until Phase 2b lands the `paperA` bib entry's
arXiv ID and any other missing citations. Until then the
scaffold compiles with `?` placeholders for unresolved
references — acceptable for a skeleton commit, not for any
gated milestone.
