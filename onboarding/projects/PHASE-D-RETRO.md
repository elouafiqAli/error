# Phase D retrospective — onboarding/projects/ end-to-end

> **Scope.** Commits `689cc05` → `306f51a` (10 atomic commits,
> 2026-06-02 → 2026-06-03). Delivered: six executed capstone
> notebooks (M1–M6), four executed homework notebooks (HW1–HW4,
> from earlier Phase B), a working pytest collection, the r2
> doctrine ratification, and a deployed Modal app.

## Calibrated outcomes

| Claim | Calibration | Evidence |
|---|---|---|
| All six milestones execute clean end-to-end | HIGH | `nbclient` run per milestone; final cell prints `[GATE OK]` |
| M3 trained a 2-layer GCN on a real Modal T4 | HIGH | `device='cuda'`, `test_acc=0.805`, 200 epochs, ~30s cold-start |
| M4 ran the 4-architecture NAS sweep on T4 | HIGH | `gpu_sweep['device']=='cuda'`, keys `['device','results']` |
| Default-scope pytest is green on both rootdirs | HIGH | `47 passed, 1 xfailed in 5.5s` (repo root *and* `projects/`) |
| `GRADE=1` lane fails loud per unfilled starter | HIGH | hw1–hw4: 10–20 `NotImplementedError` fails each |
| Modal Notebooks browser flow works end-to-end | MEDIUM | `modal deploy` succeeded; live `%modal` cell not tested in this session — Modal Notebooks UI is browser-only |

## Commit-by-commit

| Commit | Phase | Adversarial framing |
|---|---|---|
| `689cc05` | D/m1 | "Multi-class Bayes error can exceed 1/2." Gate bounds `e_C` by `(K-1)/K` *and* requires binarisation ∈ [0, 1/2]. |
| `4c18e86` | D/m2 | "K=7 e_C makes the binary-entropy bracket nonsense." `stats(P)` helper enforces binarisation before bracket invocation. |
| `1e34e51` | D/m3 | "Optional Modal cells = dishonest pedagogy." Mandates `device=='cuda'` + `|GPU-CPU|<0.10` from inside the notebook. |
| `220bac8` | D/m4 | "Unrigged sweep would not separate MLP from structural models." Sweep gate asserts at least one structural model beats MLP. |
| `5ea5707` | D/m5+m6 | "Calibration drift if no one reads the log." M5 reads `.reflection.jsonl` end-to-end; M6 stresses dataset dependence (Pubmed's MLP-friendly features). |
| `834c27c` | infra | "Near-miss: 16MB of Cora binaries almost landed in a code-only commit." `.gitignore` extended. |
| `49039b3` | D/audit | "Pytest had been silently broken since the psets were written." Importlib + GRADE=1 opt-in. |
| `a58f426` | D/doctrine | "Why does scaffold/ split cells the way it does?" REDESIGN-r2.md ratifies the 8-cell rhythm. |
| `5fa56d8` | D/doctrine | "r1 README described a system that no longer exists." README + SYLLABUS r2 entries. |
| `306f51a` | D/advanced | "What about students with no local Python?" `modal-deploy` + `%modal` cell-magic browser flow. |

## What worked

- **Atomic commits per milestone.** Made the audit `git reset --soft`
  trivial when the data/ binaries leaked. Discipline mantra paid off.
- **Mandatory GPU gates.** `assert gpu_result['device']=='cuda'`
  turned what would have been a "did the optional cell run?" hand-wave
  into a hard pass/fail signal.
- **GRADE=1 opt-in.** Cleanest way to keep student starters in the
  tree without polluting CI; lets graders run a single `make grade`.
- **Scaffolder-as-source-of-truth.** Every `.ipynb` regenerated from
  `scaffold/*.py` in a single command. No notebook-as-code-review
  pain.

## What to watch in Phase E

- **Modal Notebook `%modal` magic** not yet exercised in a live
  browser session — calibrated MEDIUM. Resolve by recording one
  end-to-end run before the next phase declares Modal coverage HIGH.
- **`.reflection.jsonl` is per-machine and gitignored.** M5 depends
  on it existing — a fresh-clone student will see M5's gate fail
  until they've executed at least one earlier notebook. Acceptable
  (it's the calibration loop) but should be loud in M5's intro.
- **Cora cache at `data/cora/Cora/`** is gitignored; first run on
  a fresh checkout will download ~3MB from `https://github.com/kimiyoung/planetoid`.
  Document this in §3 of `projects/README.md` if it surprises
  anyone.

## Numbers worth remembering

| Metric | Value |
|---|---|
| Capstone notebooks executed clean | 6 / 6 |
| HW notebooks executed clean | 4 / 4 (solutions); students fail at first TODO as designed |
| Default-scope pytest | 47 passed, 1 xfailed |
| Calibrated reflection entries | 30 (HW1–HW4 + M1–M4 + M6) |
| M3 T4 result | `device=cuda, test_acc=0.805, val_acc=0.766, loss_final=0.012` |
| M3 wall-time (incl. cold start) | ~90s |
| Modal app deploy time | 1.435s |
