# Notebooks

Numerical companion to `gnn.md`. The single master script
[nb_master.py](nb_master.py) regenerates every plot referenced in the
monograph in a deterministic run.

## Quickstart

```bash
cd reader-monograph
pip install -r requirements.txt
cd notebooks
python nb_master.py
```

Outputs land in [`../plots/`](../plots/).

## Plot index

| File                          | Chapter | Content                                           |
|-------------------------------|---------|---------------------------------------------------|
| `plot01_binary_entropy.png`   | Ch 2    | `H_bin(p)` and its inverse on `[0, 1/2]`         |
| `plot02_bridge_sandwich.png`  | Ch 2/12 | §2.4 Bridge envelopes vs. Bayes risk             |
| `plot03_slack_max.png`        | Ch 12   | Slack function `w(H)`; peak `w* ≈ 0.161` at 1/5  |
| `plot04_hvs_envelopes.png`    | Ch 13   | HVS-admissible envelopes (HR, Gini, sin, Bhatt.) |
| `plot05_massey.png`           | Ch 14   | `E[G]` lower bound vs. geometric extremal        |
| `plot06_ib_depth.png`         | Ch 15   | LossyWL trajectory in IB coordinates             |
| `plot07_prior_aware.png`      | Ch 16   | Prop 3.6 vs. §2.4 lower bound on `I(f;Π)`        |

## Design note

We consolidated the originally-planned 13 small notebooks (`nb01`–`nb13`)
into a single master script for reproducibility: one process, one seed
schedule, one set of pinned dependencies, deterministic output. The
plots cover every numerical illustration referenced in the prose.
Individual `.ipynb` files can be split out from `nb_master.py` if
interactive exploration is required.
