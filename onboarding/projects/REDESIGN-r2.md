# `onboarding/projects/` r2 redesign — tutorial-first notebooks on Modal

> **Status.** Design (r2), 2026-06-02. Author: Claude.
> **Supersedes** the r1 design captured in [`README.md`](README.md)
> §3, which structured HWs as `starter/*.py + tests/*.py + writeup.md`.
> r2 collapses each HW into one tutorial notebook with inline gates,
> a Modal harness for GPU cells, and a capstone reflection that
> incrementally aggregates across all HWs + milestones.
>
> **Trigger.** Operator directive 2026-06-02:
>
> > "Make sure they are Notebook level that can [run] on Modal, make
> > sure they have all the gates of verification, not as exercises
> > but as tutorial, and the TODO is the final implementation with
> > instructions as TODOs. By the end the user should progressively
> > reflect the experiments in full."
>
> **Inspirations.**
> - Udacity [`deep-learning`](https://github.com/udacity/deep-learning)
>   and [`deep-reinforcement-learning`](https://github.com/udacity/deep-reinforcement-learning)
>   — notebook-per-lesson, demo-first, fill-in-the-blank TODO cells,
>   solutions branch.
> - Stanford [`CS228-PGM`](https://github.com/florist-notes/CS228_PGM)
>   — theory → code → experiment in one flow, KaTeX-heavy markdown,
>   small reproducible examples per concept.
> - Retained from r1: Stanford-PSet rubric (correctness / pedagogy /
>   calibration with mis-calibration penalty); Distinguish + Mutate
>   drills.

---

## 1. The "tutorial-first, TODO-last" cell doctrine

Every concept in every notebook is exactly 8 cells, in fixed order:

| # | Type     | Purpose                                                                                  |
|---|----------|------------------------------------------------------------------------------------------|
| 1 | markdown | **Concept** — 1–3 paragraphs, KaTeX, with `§N.M` paper pointer                            |
| 2 | code     | **Demo** — fully runnable, prints/plots the concept's signature object. No `TODO`.       |
| 3 | markdown | **Distinguish** — X-vs-Y pair, named failure mode                                         |
| 4 | code     | **Replicate-and-vary** — fully runnable; varies one knob; produces the "second example"  |
| 5 | markdown | **Gate** — states the invariant the student's code must satisfy                           |
| 6 | code     | **TODO** — *single* named function, instructional `# TODO(...)` block, expected LOC      |
| 7 | code     | **Assertion gate** — `assert`s on the student's function; same checks as the pytest CI   |
| 8 | markdown | **Reflection** — 3 fixed prompts: surprise / mis-prediction / HIGH-MED-LOW for one claim |

Mechanical consequences:

- **Cells 1–5 always run green** from a fresh checkout. The notebook
  is a working demo *before* the student touches it.
- **Cell 6** is the *only* place the student types load-bearing
  code. It is at most ~20 LOC. The TODO comments call out the
  exact sub-steps; the student is filling in *names already
  scaffolded* by the demo in cells 2 and 4.
- **Cell 7** raises `AssertionError` on failure. No external test
  runner needed for the inner loop; CI runs the same assertions via
  `nbclient` for the grader-facing checks.
- **Cell 8** writes its third prompt's HIGH/MED/LOW entry to a
  growing `REFLECTION.ipynb` artefact via a small helper
  `reflect.log(concept, claim, level)`.

A 30-point HW question maps to 1–2 concept blocks (8–16 cells).
A 100-point HW becomes 30–40 cells of tutorial.

---

## 2. The Modal harness (`modal_app.py`)

A single Modal app at `onboarding/projects/modal_app.py` exposes:

```python
import modal

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install_from_requirements("onboarding/projects/requirements.txt")
)
app = modal.App("bracket-onboarding", image=image)

@app.function(gpu="T4", timeout=600)
def train_gcn(seed: int = 0, epochs: int = 200, hidden: int = 16) -> dict:
    """Run a 2-layer GCN on Cora; return loss/acc curves + predictions."""
    ...  # body defined in `train.py`, imported here

@app.function(cpu=2)
def compute_bracket(partition_blob: bytes) -> dict:
    """CPU-only: M2's bracket on a serialised Partition."""
    ...

@app.function(gpu="T4", timeout=1200)
def nas_sweep(arch_menu: list[str]) -> list[dict]:
    """Train each architecture in the menu; return acc + bracket-midpoint."""
    ...
```

**Inside notebooks**, the pattern is:

```python
import os, modal
if os.environ.get("USE_MODAL", "0") == "1":
    from onboarding.projects.modal_app import app, train_gcn
    with app.run():
        result = train_gcn.remote(seed=0, epochs=200)
else:
    # local CPU fallback
    from onboarding.projects.local_bench import train_gcn
    result = train_gcn(seed=0, epochs=20)  # shorter run
```

The student can flip `USE_MODAL=1` once they've installed `modal`
and run `modal token new`. CPU local runs always work. CI uses
local for HW1–HW4 and Modal for the capstone M3+M4.

**Setup, one-time, ~3 minutes:**

```bash
pip install modal
modal token new            # opens browser, paste token
modal volume create cora   # one-time, holds the PyG download
```

Inputs and outputs travel through a Modal Volume `cora` so each
notebook does not re-download Planetoid.

---

## 3. File-level layout (r2)

```
onboarding/projects/
├── REDESIGN-r2.md            # this file
├── README.md                 # updated to point at r2
├── modal_app.py              # the shared Modal app
├── local_bench.py            # CPU fallback for every Modal function
├── requirements.txt          # pinned; consumed by modal_app and locally
├── reflect.py                # reflection helper (.log / .render)
│
├── psets/
│   ├── README.md             # course preamble (unchanged)
│   ├── hw1_binary_entropy_and_HR.ipynb           # ~32 cells
│   ├── hw2_partitions_condent_1WL.ipynb          # ~36 cells
│   ├── hw3_T1_verifier_from_scratch.ipynb        # ~36 cells
│   ├── hw4_aggregator_inflation_on_C6_vs_2K3.ipynb  # ~32 cells
│   ├── ci/                   # pytest mirror that runs each notebook
│   │   ├── test_hw1.py       # uses nbclient to execute hw1 and check no assertion fired
│   │   ├── test_hw2.py
│   │   ├── test_hw3.py
│   │   └── test_hw4.py
│   └── solutions/            # gitignored; instructor-only `*_solution.ipynb`
│
├── capstone/
│   ├── README.md
│   ├── m1_data_and_partition.ipynb               # ~28 cells
│   ├── m2_bracket_computer.ipynb                 # ~30 cells
│   ├── m3_train_gcn_and_audit.ipynb              # ~36 cells (Modal-backed)
│   ├── m4_nas_prefilter.ipynb                    # ~32 cells (Modal-backed)
│   ├── m5_report_and_reflection.ipynb            # auto-assembled from earlier
│   ├── ci/
│   │   ├── test_m1.py … test_m5.py
│   │   └── test_end_to_end.py
│   └── solutions/            # gitignored
│
└── shared/                   # the *only* place students may import from
    ├── partition.py          # ⇐ from current capstone/milestone1/, exposed
    ├── bracket.py            # ⇐ from current capstone/milestone2/, exposed
    └── aggregators.py        # ⇐ from current psets/hw4/starter/, normalised
```

**Migration rule.** Existing `.py` starter files are *preserved*
under git in their current locations; r2 notebooks **import the
final shared modules** from `shared/`, and reproduce the relevant
TODO cells inline. r1's `starter/` and `tests/` directories remain
on disk as the pytest-only mirror — they are not deleted, just
demoted to "CI fixtures".

---

## 4. Per-notebook spine

Every HW notebook opens with the **same 5 preamble cells**:

1. (md) Title + paper section pointers + "what you'll know by the end" (4 bullets).
2. (md) Prerequisites + how to run on Modal vs locally.
3. (code) `import` block + `reflect.start(notebook="hwN")` to open the per-notebook reflection log.
4. (code) Smoke-test cell: imports `shared/`, runs a 3-line sanity check, asserts a known constant. **If this fails the notebook will not run; the student must fix their env first.**
5. (md) Roadmap: numbered list of the concepts covered, each linking to its first cell via anchor.

Every HW notebook closes with the **same 3 closing cells**:

- (md) **Reflection summary** — auto-rendered table from `reflect.dump()` of all HIGH/MED/LOW entries logged in cells 8.
- (code) `reflect.export(target="capstone/m5_report_and_reflection.ipynb")` — appends the per-concept reflections into the M5 capstone artefact under section `## From HWn`.
- (md) Next pointer to the next notebook.

---

## 5. The capstone reflection artefact (`m5_report_and_reflection.ipynb`)

This notebook is **mostly auto-generated** from the per-HW reflection logs. It contains:

| Section | Source                                                       |
|---|---|
| §1 Pitch                  | hand-written by student (one paragraph)              |
| §2 Dataset & partitions   | auto-imported from M1 cells; histogram from M1 cell 19 |
| §3 Bracket reproduction   | auto-imported from M2 cells; the $w^* \approx 0.1610$ assertion gate from M2 |
| §4 GCN audit              | auto-imported from M3 cells; scatter from M3 cell 27 |
| §5 NAS pre-filter         | auto-imported from M4 cells; Kendall-$\tau$ table from M4 cell 24 |
| §6 Distinguish entries    | auto-collected from every Distinguish cell across HW1–4 + M1–4 |
| §7 Mutate→fail→revert log | auto-collected from every Mutate cell                |
| §8 False leads            | hand-written + auto-collected from Reflection prompts |
| §9 Calibration table      | auto-rendered from `reflect.dump()` across **all** notebooks |
| §10 Next                  | hand-written                                          |

The student writes only §1, §8 (curation), §10. Everything else is
**collated from gates they passed in earlier notebooks** — this is
the "progressive reflection" the operator asked for.

The `reflect` helper persists to `onboarding/projects/.reflection.jsonl`
(gitignored); `reflect.render_capstone()` is a notebook-cell call
that updates §2–§7 and §9 in place using `nbformat`.

---

## 6. Cell-count target (auditable)

| Notebook | Concept blocks | Cells | Modal cells | Of which TODO cells |
|---|---|---|---|---|
| HW1 binary entropy + HR        | 4 | 32 + 5 + 3 = 40 | 0 | 4 |
| HW2 partitions + condent + 1WL | 4 | 32 + 5 + 3 = 40 | 0 | 4 |
| HW3 T1 verifier                | 4 | 32 + 5 + 3 = 40 | 0 | 4 |
| HW4 aggregator inflation       | 4 | 32 + 5 + 3 = 40 | 0 | 4 |
| M1 data + partition harness    | 3 | 24 + 5 + 3 = 32 | 0 | 3 |
| M2 bracket computer            | 3 | 24 + 5 + 3 = 32 | 0 | 3 |
| M3 train + audit GCN           | 4 | 32 + 5 + 3 = 40 | 2 | 3 |
| M4 NAS pre-filter              | 3 | 24 + 5 + 3 = 32 | 1 | 2 |
| M5 report + reflection         | — | ~20 (mostly md) | 0 | 0 |

Total: ~320 cells across 9 notebooks, of which 27 are
student-written TODO blocks (every TODO ≤ 20 LOC). The remaining
~85% is tutorial that runs on a fresh checkout.

---

## 7. Verification gate semantics

A **gate** is an assertion cell that:

1. Names exactly one invariant in its first comment line:
   `# Gate: <claim>`.
2. Computes the invariant.
3. `assert <invariant>, f"…diagnostic…"` with a one-line diagnostic
   that names the *most-common failure mode* (e.g. "did you forget
   the `1 - max(...)/n` for `e_C`?").
4. On success, prints a single line `[GATE OK] <claim>`.

The pytest CI mirror executes the notebook end-to-end with
`nbclient.execute_notebook` and asserts no `AssertionError` was
raised. Each notebook ships with a one-line `Makefile` target:

```
make hw1     # nbclient runs hw1, fails CI if any gate fails
make all     # runs hw1..hw4, m1..m5
make modal   # the GPU-backed subset, runs M3+M4 with USE_MODAL=1
```

---

## 8. Rubric (unchanged from r1 in spirit; mapped to notebook artefacts)

| Axis | Weight | Source of evidence |
|---|---|---|
| **Correctness** | 60% | All gate cells `[GATE OK]` in the saved `.ipynb` |
| **Pedagogy**    | 25% | Reflection cells (8th cell of each concept) have substantive answers; Distinguish entries are non-trivial |
| **Calibration** | 15% | `reflect.dump()` table in §9 of M5 is honest under adversarial review |

Mis-calibration penalty (double weight) and "Anti-pattern penalty"
(import of `scipy.stats.entropy` etc.) carry over unchanged from r1.

---

## 9. Migration plan (build order, gated)

A. **Scaffolding** (no notebooks yet):
   1. Create `shared/` and move (`git mv`) the canonical `.py`
      sources from current `capstone/milestone1/partition.py`,
      `capstone/milestone2/bracket.py`, `psets/hw4/starter/q1_aggregators.py`.
   2. Create `modal_app.py`, `local_bench.py`, `requirements.txt`,
      `reflect.py`. Smoke-test the Modal app with one trivial
      function (`@app.function(cpu=1) def ping(): return "pong"`).
   3. Add `Makefile` with `hw1`, `all`, `modal` targets (initially
      noop; populated as notebooks land).
   4. Add the pytest mirror under each `ci/`, initially asserting
      "the notebook file exists and parses as nbformat".

B. **HW1 end-to-end** (validate the doctrine):
   1. Author `hw1_binary_entropy_and_HR.ipynb` end-to-end.
   2. Wire `ci/test_hw1.py` to execute via nbclient.
   3. PING USER. **Do not flesh HW2 until operator approves shape.**

C. **HW2, HW3, HW4** in parallel after A+B sign-off.

D. **M1** end-to-end (validate Modal harness for the capstone half).
   PING USER.

E. **M2, M3, M4** in parallel after D sign-off.

F. **M5** auto-assembly (`reflect.render_capstone` polish).

G. Update top-level `README.md` and `SYLLABUS.md` to point at r2;
   keep r1 docs in place as "legacy".

H. **Confidence**: this whole plan is `MEDIUM`. The principal risks:

   - **MEDIUM**: Modal cold-start latency may make M3 painful for
     iteration. Mitigation: `local_bench.train_gcn` with `epochs=20`
     and `hidden=8` for inner-loop dev; Modal only for the "real"
     run that produces the M3 scatter.
   - **MEDIUM**: the reflection auto-collation across notebooks is
     novel; if `reflect.export` proves brittle, fall back to a
     hand-written §9 in M5 (lose 5 of the 15 calibration points).
   - **LOW**: students who skip the demo cells (1–4) and jump to
     the TODO (6) will struggle. The README will lead with a
     "read top-down" warning.

---

## 10. What is NOT changing

- Rubric weights (60/25/15) and mis-calibration penalty.
- The 4-HW / 5-milestone partition.
- The dataset (Cora via PyG).
- The bracket's canonical form: `lower = Hbin_inv(H)`, `upper = H/2`,
  `H = Σ q_C · Hbin(e_C)`, `ε = Σ q_C · e_C`.
- The "Distinguish, Mutate, Calibrate" pedagogy.
- The Julia/Pluto NB01–12 track in `onboarding/julia-theory/` —
  that track is the *theory mirror*; r2 is the *engineering mirror*.

---

## 11. Open questions for the operator

These cannot be silently chosen:

1. **Q11.1.** Modal billing — is the operator OK with up to ~$5
   per full M3+M4 run (T4 × ~15 min total)? If not, fall back to a
   CPU-only capstone (loses the "trained-GCN audit" pedagogy).
2. **Q11.2.** Do you want HW1–4 to be Modal-runnable too (overkill —
   all four are CPU-fast)? r2 design says NO; HW notebooks are
   strictly local. Confirm.
3. **Q11.3.** Solutions branch policy: do we maintain
   `solutions/*_solution.ipynb` files (Udacity-style, separate
   branch) or distribute via `nbgrader`-style metadata stripping?
   Default in r2: gitignored `solutions/` directory + manual cell
   strip; we can upgrade to `nbgrader` if you want.

Until these three are answered, **no notebook code lands**. The
scaffolding (`shared/`, `modal_app.py`, `reflect.py`, `Makefile`)
can land in parallel.
