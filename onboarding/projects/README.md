# `onboarding/projects/` — graduate-student practical track (r2)

> **Where this sits.** The [PLAN.md](../PLAN.md) on-ramp ends at **G2**:
> the operator can read the abstract, reproduce E3 on Cora, and
> whiteboard the bracket. This folder adds two structured-assessment
> tracks on top, both *optional, both gated by G1*:
>
> 1. **`capstone/milestone{1..6}/`** — six end-to-end notebooks that
>    take you from a fresh Cora dataset to a multi-dataset NAS sweep
>    run on a real Modal T4 GPU, and a reflection log written by
>    every notebook you've executed.
> 2. **`psets/hw{1..4}/`** — four notebook-form problem sets, each
>    1–2 days, with inline gates and a `GRADE=1` lane for the
>    student-facing unit tests.
>
> Both tracks share the **8-cell tutorial-first doctrine** codified
> in [REDESIGN-r2.md](REDESIGN-r2.md). Read it before authoring or
> auditing any notebook in this folder.

---

## 1. Doctrine snapshot (canonical: [REDESIGN-r2.md](REDESIGN-r2.md))

Every concept in every notebook follows an 8-cell rhythm:

| # | Type     | Purpose                                                                                  |
|---|----------|------------------------------------------------------------------------------------------|
| 1 | markdown | **Concept** — KaTeX, with `§N.M` paper pointer                                            |
| 2 | code     | **Demo** — fully runnable, no TODO                                                        |
| 3 | markdown | **Distinguish** — named X-vs-Y pair, named failure mode                                   |
| 4 | code     | **Replicate-and-vary** — vary one knob                                                    |
| 5 | markdown | **Gate** — states the invariant the student's code must satisfy                           |
| 6 | code     | **TODO** — *single* named function the student fills; ≤ 20 LOC                            |
| 7 | code     | **Assertion gate** — same checks as the pytest CI                                          |
| 8 | code     | **Reflect** — `reflect.log(concept, claim, HIGH/MED/LOW/UNVERIFIED)`                       |

Mechanical consequences: cells 1–5 are always green from a fresh
checkout; cell 6 is the only place the student types load-bearing
code; cell 7 raises `AssertionError` on failure; cell 8 grows
`.reflection.jsonl` that Milestone 5 reads back as a calibration
report.

**Modal-first GPU.** Cells in M3 and M4 are **not optional** —
they open `modal.app.run()` from inside the notebook, schedule
work on a T4, and assert `result["device"] == "cuda"`. Optional
GPU cells are dishonest pedagogy; if a notebook claims to train on
a GPU, the gate proves it did.

---

## 2. Layout

```
onboarding/projects/
├── README.md            # this file
├── REDESIGN-r2.md       # the 8-cell doctrine (canonical)
├── Makefile             # all CPU + GPU + GRADE=1 targets
├── requirements.txt
├── pytest.ini           # importlib mode
├── conftest.py          # excludes student-facing psets/hw*/tests by default
├── modal_app.py         # @app.function(gpu="T4") ping, train_gcn, nas_sweep
├── reflect.py           # reflect.start(), reflect.log() -> .reflection.jsonl
├── shared/              # partition.py, bracket.py, aggregators.py (+ tests)
├── scaffold/            # __init__.py (Cell, write_pair, execute)
│   ├── hw1.py … hw4.py  # one .py per HW, emits both _solution and student .ipynb
│   └── milestones.py    # emits m1..m6 .ipynb
├── ci/                  # presence + JSON-validity tests for every nb
├── psets/
│   ├── hw1/{hw,hw_solution}.ipynb + starter/ + tests/
│   ├── hw2/...
│   ├── hw3/...
│   └── hw4/...
└── capstone/
    ├── milestone1/m1.ipynb            # Cora label + 1-WL partitions
    ├── milestone2/m2.ipynb            # bracket audit on Cora
    ├── milestone3/m3.ipynb            # GCN CPU + real Modal T4
    ├── milestone4/m4.ipynb            # NAS CPU + real Modal T4 sweep
    ├── milestone5/m5.ipynb            # reflection report (reads .reflection.jsonl)
    └── milestone6/m6_advanced.ipynb   # Cora/Citeseer/Pubmed × {MLP,GCN,SAGE,GIN}
```

---

## 3. How to run

### One-shot setup

```bash
cd onboarding/projects
make setup                # pip install -r requirements.txt
modal token new           # one-time, lands ~/.modal.toml
```

### CPU lane — everything that runs without a GPU

```bash
make all                  # unit tests + HW1..HW4 + M1 + M2 + M5
```

### GPU lane — invokes Modal T4 from inside the notebook

```bash
make modal-verify         # M3 + M4 + M6, ~5–10 min wall (incl. cold start)
```

### Student grading — opt back in to student-facing tests

```bash
make grade-hw1            # GRADE=1 pytest psets/hw1
make grade                # all four HWs
```

`GRADE=1` flips [`conftest.py`](conftest.py) to collect the
student-facing `psets/hw*/tests/` directories (otherwise hidden
because they intentionally raise `NotImplementedError` until the
student fills in the starter).

### Default pytest scope (CI)

```bash
pytest onboarding/projects -q     # 47 passed, 1 xfailed (shared + ci + capstone)
```

---

## 4. Two tracks — pick one

| | Capstone (`capstone/`) | PSets (`psets/`) |
|---|---|---|
| Shape | one project, six notebooks, integrated | four independent notebook assignments |
| Time | ~2 weeks part-time | ~1–2 days each |
| Output | working pipeline + reflection log + real T4 sweep | one filled notebook per HW + auto-graded gates |
| Failure mode | architecture creep | tunnel vision on individual lemmas |
| Best for | someone joining the lab and needing a fluency demo | someone studying solo who wants tightly-bounded reps |

A student does not need both. Both teach the same paper; neither
replaces G2.

---

## 5. Rubric (applies to both tracks)

| Axis | Weight | What it measures |
|---|---|---|
| **Correctness** | 60% | Cell-7 assertion gates pass; numbers match reference to declared precision; pytest green under `GRADE=1`. |
| **Pedagogy** | 25% | Cell-3 distinguishes the right pair; cell-8 reflection names the failure mode and cites `§N.M`. |
| **Calibration** | 15% | `reflect.log(..., HIGH/MED/LOW/UNVERIFIED)` entries are honest. |

**Mis-calibration penalty.** A `HIGH` claim that an adversarial
grader kills costs 2× the calibration weight. A `LOW` or
`UNVERIFIED` claim that survives costs nothing — calibration was
honest.

---

## 6. What is *not* graded here

- Proving Theorem 1 from scratch. (Verifier-level competence is
  enough; proof carpentry is downstream.)
- Lean / Julia / formal verification. (BLUE in PLAN.md.)
- Extending the bracket to $\phi$-families or k-WL. (Paper B / C.)
- Writing new theorems. (Research, not coursework.)

Bonus capped at +5 if a student goes there.

---

## 7. Status (r2)

- **Design version**: r2, 2026-06-03. Supersedes r1
  (`starter/*.py + tests/*.py + writeup.md`); see
  [REDESIGN-r2.md](REDESIGN-r2.md) §0 for the trigger.
- **HWs**: HW1–HW4 fully scaffolded, executed clean, committed
  (`e0f93ad`, `6997157`, `8084726`).
- **Capstones**: M1–M6 fully scaffolded, all six executed clean.
  M3 + M4 verified on Modal T4 (`device='cuda'`, M3
  `test_acc=0.805`). Commits `689cc05` → `5ea5707`.
- **Default-scope pytest**: 47 passed, 1 xfailed from both repo
  root and `onboarding/projects/` (audit fix `49039b3`).
- **Reflection log**: 30 calibrated entries (HW1–HW4 + M1–M4 + M6).
- **Verifier discipline**: every theorem cell has an assertion
  gate; every Modal cell asserts `device == "cuda"`.

### Regenerate any notebook from its scaffolder

```bash
python -m onboarding.projects.scaffold.hw1          # writes psets/hw1/hw{,_solution}.ipynb
python -m onboarding.projects.scaffold.milestones   # writes capstone/milestone{1..6}/m*.ipynb
```
