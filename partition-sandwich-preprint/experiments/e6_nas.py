"""
e6_nas.py — Experiment 6: classical NAS by the bracket.

Search space: MLP architectures
    hidden_layer_sizes ∈ {(16,), (32,), (64,), (128,),
                          (16,16), (32,32), (64,64), (128,128),
                          (32,32,32), (64,64,64)}
    seeds ∈ {0, 1, 2}
= 30 candidate architectures.

For each candidate (X, y) on UCI Adult (80/20 split, fixed):

  TRAINING-FREE PROBE (the bracket-NAS shortcut):
    1. Init the MLP weights at the given seed (no training).
    2. Forward-pass X_train through the frozen random net, read the
       LAST hidden layer pre-activations Z ∈ R^{n × w}.
    3. Project signs(Z) onto a 12-bit hash → cell_id (cap |Π| ≤ 4096).
       This is the "activation-pattern partition" — the partition a
       ReLU network actually carves the training data into at init.
    4. bracket_from_cells(cell_id, y_train) → lower / upper bounds.

  GROUND-TRUTH (the expensive baseline we want to avoid):
    5. Fit MLPClassifier(hidden_layer_sizes, max_iter=200, seed) on
       X_train, y_train.
    6. Predict on X_test, record test error.

Headline metrics emitted:
  - Spearman ρ between (bracket lower bound at init) and (trained test
    error). Strongly positive ⇒ the bracket ranks architectures
    correctly without training any of them.
  - Top-3 overlap: of the 3 architectures with smallest bracket lower
    bound, how many are also in the 3 with smallest test error.
  - Compute saving: total_train_time / total_bracket_time.

Outputs: figures/e6_nas_scatter.pdf and results/e6.json.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from common import bracket_from_cells
from datasets import load_adult

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"; RESULTS.mkdir(exist_ok=True)
FIGURES = HERE / "figures"; FIGURES.mkdir(exist_ok=True)

ARCHS = [
    (16,), (32,), (64,), (128,),
    (16, 16), (32, 32), (64, 64), (128, 128),
    (32, 32, 32), (64, 64, 64),
]
SEEDS = [0]
HASH_BITS = 12           # max cells = 2**12 = 4096
TEST_SIZE = 0.20
SPLIT_SEED = 0


# --------------------------------------------------- random-init MLP probe
def activation_pattern_cells(X: np.ndarray,
                             hidden_layer_sizes: tuple[int, ...],
                             seed: int,
                             hash_bits: int = HASH_BITS) -> np.ndarray:
    """
    Frozen random ReLU forward pass.
    Returns a cell_id per row of X based on the sign pattern of the
    LAST hidden layer's pre-activations, projected to `hash_bits` bits
    so |Π| ≤ 2**hash_bits.
    """
    rng = np.random.default_rng(seed)
    h = X.astype(np.float32, copy=False)
    z = None
    for d_out in hidden_layer_sizes:
        d_in = h.shape[1]
        # He-init scaled
        W = rng.standard_normal((d_in, d_out)).astype(np.float32) \
            * np.float32(np.sqrt(2.0 / d_in))
        b = np.zeros(d_out, dtype=np.float32)
        z = h @ W + b
        h = np.maximum(z, 0.0)
    assert z is not None
    # project sign pattern of last z onto `hash_bits` bits
    width = z.shape[1]
    take = min(hash_bits, width)
    if width >= hash_bits:
        # random subset of coordinates
        idx = rng.choice(width, size=hash_bits, replace=False)
        signs = (z[:, idx] > 0).astype(np.uint64)
    else:
        # too narrow; pad by random projection rows
        P = rng.standard_normal((width, hash_bits)).astype(np.float32)
        signs = ((z @ P) > 0).astype(np.uint64)
    weights = (1 << np.arange(hash_bits, dtype=np.uint64))
    cell = (signs * weights).sum(axis=1)
    return cell


# ----------------------------------------------------------------- driver
def main() -> None:
    X, y, _ = load_adult()
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=SPLIT_SEED, stratify=y,
    )

    rows = []
    t_bracket_total = 0.0
    t_train_total   = 0.0
    for arch in ARCHS:
        for seed in SEEDS:
            # ---- training-free bracket probe ----------------------------
            t0 = time.perf_counter()
            cells = activation_pattern_cells(X_tr, arch, seed)
            br = bracket_from_cells(cells, y_tr)
            t_bracket = time.perf_counter() - t0
            t_bracket_total += t_bracket

            # ---- ground-truth full training -----------------------------
            t0 = time.perf_counter()
            mlp = MLPClassifier(
                hidden_layer_sizes=arch,
                max_iter=60, tol=1e-3, random_state=seed,
                early_stopping=True, validation_fraction=0.1, n_iter_no_change=5,
            )
            mlp.fit(X_tr, y_tr)
            train_err = float(np.mean(mlp.predict(X_tr) != y_tr))
            test_err  = float(np.mean(mlp.predict(X_te) != y_te))
            t_train = time.perf_counter() - t0
            t_train_total += t_train

            rows.append({
                "arch": list(arch), "seed": seed,
                **br.as_dict(),
                "train_err": train_err,
                "test_err":  test_err,
                "t_bracket_s": t_bracket,
                "t_train_s":   t_train,
            })
            print(f"  arch={str(arch):16s} seed={seed} "
                  f"m={br.m:4d}  lower={br.lower:.4f}  "
                  f"eps*={br.eps_star:.4f}  upper={br.upper:.4f}  "
                  f"test={test_err:.4f}  "
                  f"[bracket {t_bracket*1000:.1f}ms / train {t_train:.1f}s]")

    # ---- rank-correlation analysis ----------------------------------------
    lower    = np.array([r["lower"]    for r in rows])
    eps_star = np.array([r["eps_star"] for r in rows])
    test_err = np.array([r["test_err"] for r in rows])

    rho_lower,  p_lower  = spearmanr(lower,    test_err)
    rho_eps,    p_eps    = spearmanr(eps_star, test_err)

    K = 3
    top_by_bracket = set(np.argsort(lower)[:K].tolist())
    top_by_test    = set(np.argsort(test_err)[:K].tolist())
    top_overlap = len(top_by_bracket & top_by_test)

    speedup = t_train_total / max(t_bracket_total, 1e-9)

    # ---- figure: rank-correlation scatter ---------------------------------
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    ax.scatter(lower, test_err, s=42, alpha=0.75, color="C0",
               edgecolor="k", linewidth=0.4,
               label="MLP candidates")
    # mark top-3-by-bracket
    sel = np.argsort(lower)[:K]
    ax.scatter(lower[sel], test_err[sel], s=110, facecolor="none",
               edgecolor="C3", linewidth=2.0,
               label=f"top-{K} by bracket lower")
    # diagonal y = x for reference
    xs = np.linspace(min(lower.min(), test_err.min()),
                     max(lower.max(), test_err.max()), 64)
    ax.plot(xs, xs, "k:", lw=1.0, alpha=0.7, label="$y = x$")
    ax.set_xlabel(r"bracket lower bound $H_{\mathrm{bin}}^{-1}(H(f\mid\Pi))$ "
                  r"at random init (training-free)")
    ax.set_ylabel("MLP test error after full training")
    ax.set_title(
        f"NAS by bracket on UCI Adult: "
        rf"Spearman $\rho={rho_lower:.3f}$, "
        f"top-{K} overlap {top_overlap}/{K}, "
        f"speedup {speedup:.0f}×"
    )
    ax.legend(loc="upper left", fontsize=8, framealpha=0.95)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    out_pdf = FIGURES / "e6_nas_scatter.pdf"
    fig.savefig(out_pdf)
    plt.close(fig)

    summary = {
        "experiment": "E6 NAS by the bracket (MLP, UCI Adult)",
        "dataset": "UCI Adult", "n_train": int(len(y_tr)),
        "n_test": int(len(y_te)),
        "archs": [list(a) for a in ARCHS], "seeds": SEEDS,
        "hash_bits": HASH_BITS,
        "rows": rows,
        "spearman_lower_vs_test":   {"rho": float(rho_lower), "p": float(p_lower)},
        "spearman_eps_star_vs_test":{"rho": float(rho_eps),   "p": float(p_eps)},
        f"top_{K}_overlap": int(top_overlap),
        "t_bracket_total_s": t_bracket_total,
        "t_train_total_s":   t_train_total,
        "speedup_train_over_bracket": float(speedup),
        "figure": str(out_pdf.relative_to(HERE)),
    }
    (RESULTS / "e6.json").write_text(json.dumps(summary, indent=2))
    print(f"\nE6 done.  ρ(lower, test)={rho_lower:.3f}  "
          f"top-{K} overlap={top_overlap}/{K}  "
          f"speedup={speedup:.0f}×  figure → {out_pdf.name}")

    # ---- gates: weak but meaningful ---------------------------------------
    assert rho_lower > 0.0, \
        f"E6: bracket lower bound anti-correlates with test error " \
        f"(ρ={rho_lower:.3f}) — investigate hashing / init scale"
    assert speedup > 10.0, \
        f"E6: bracket not noticeably cheaper than training " \
        f"({speedup:.1f}×). Increase ARCHS or training max_iter?"


if __name__ == "__main__":
    main()
