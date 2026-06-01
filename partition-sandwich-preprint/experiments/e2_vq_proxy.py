"""
e2_vq_proxy.py — Experiment 2: vector-quantisation zero-shot proxy.

For k ∈ {2,4,8,16,32,64,128,256,512,1000}, build Π_k = KMeans(k) on
UCI Adult and:
  - compute the bracket from Π_k (training-free, sub-second);
  - compute ε*(Π_k) directly via majority-vote per cell;
  - train a downstream LogisticRegression on one-hot cell membership
    (its training error should equal ε*(Π_k); empirically validates
    the "training adds nothing beyond the partition" claim).

Dual-axis bar chart: classification error vs compute time (log s).
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

from common import bracket_from_cells, plug_in_predictions
from datasets import load_adult

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"; RESULTS.mkdir(exist_ok=True)
FIGURES = HERE / "figures"; FIGURES.mkdir(exist_ok=True)

KS = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1000]
SEED = 0


def main() -> None:
    X, y, _ = load_adult()
    rows = []
    for k in KS:
        # -- partition + bracket (training-free) ------------------------
        t0 = time.perf_counter()
        km = KMeans(n_clusters=k, random_state=SEED, n_init=5)
        cells = km.fit_predict(X)
        br = bracket_from_cells(cells, y)
        t_bracket = time.perf_counter() - t0

        # -- plug-in error (must equal eps*) ----------------------------
        plug = plug_in_predictions(cells, y)
        plug_err = float(np.mean(plug != y))

        # -- downstream LR on one-hot cells -----------------------------
        t0 = time.perf_counter()
        OH = OneHotEncoder(sparse_output=True, handle_unknown="ignore")
        X_oh = OH.fit_transform(cells.reshape(-1, 1))
        lr = LogisticRegression(max_iter=5000, solver="lbfgs",
                                tol=1e-8, C=1e6, random_state=SEED)
        lr.fit(X_oh, y)
        lr_err = float(np.mean(lr.predict(X_oh) != y))
        t_lr = time.perf_counter() - t0

        rows.append({
            "k": k, **br.as_dict(),
            "plug_err": plug_err,
            "lr_err":   lr_err,
            "t_bracket_s": t_bracket,
            "t_lr_s":      t_lr,
        })
        # data-dependent gates:
        #   - plug-in majority MUST equal eps* exactly (tautology check on impl).
        #   - LR on saturated one-hot of cells MUST match plug-in to numerical precision
        #     (the genuine "training adds nothing beyond the partition" claim).
        assert abs(plug_err - br.eps_star) < 1e-9, \
            f"k={k}: plug-in {plug_err} != eps* {br.eps_star}"
        assert abs(lr_err - br.eps_star) < 1e-3, \
            f"k={k}: LR err {lr_err} differs from eps* {br.eps_star} by >0.1%"
        print(f"  k={k:4d}  H={br.H:.4f}  eps*={br.eps_star:.4f}  "
              f"lower={br.lower:.4f}  LR={lr_err:.4f}  "
              f"bracket={t_bracket*1000:.0f}ms  LR={t_lr:.2f}s")

    ks   = np.array([r["k"] for r in rows])
    lower = np.array([r["lower"] for r in rows])
    epsst = np.array([r["eps_star"] for r in rows])
    lrerr = np.array([r["lr_err"] for r in rows])
    tbr   = np.array([r["t_bracket_s"] for r in rows])
    tlr   = np.array([r["t_lr_s"]      for r in rows])

    # dual-axis bar chart
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    x = np.arange(len(ks))
    w = 0.28
    ax.bar(x - w, lower, width=w, color="C0", alpha=0.85,
           label=r"lower bound $H_{\mathrm{bin}}^{-1}(H)$")
    ax.bar(x,     epsst, width=w, color="C2", alpha=0.85,
           label=r"$\varepsilon^{*}_{\Pi_k}$ (plug-in)")
    ax.bar(x + w, lrerr, width=w, color="C3", alpha=0.85,
           label="LR downstream error")
    ax.set_xticks(x); ax.set_xticklabels([str(k) for k in ks])
    ax.set_xlabel("Codebook size $k$")
    ax.set_ylabel("Classification error")
    ax.set_title("Zero-shot architecture selection on UCI Adult")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(axis="y", alpha=0.25)

    ax2 = ax.twinx()
    ax2.plot(x, tbr, "C0o--", lw=1.0, ms=4, label="bracket time")
    ax2.plot(x, tlr, "C3s--", lw=1.0, ms=4, label="LR fit time")
    ax2.set_yscale("log")
    ax2.set_ylabel("Compute time (s, log)")
    ax2.legend(loc="lower right", fontsize=8)

    fig.tight_layout()
    out_pdf = FIGURES / "e2_vq_zeroshot.pdf"
    fig.savefig(out_pdf)
    plt.close(fig)

    summary = {
        "experiment": "E2 vector-quantisation zero-shot proxy",
        "dataset": "UCI Adult", "seed": SEED, "ks": KS,
        "rows": rows,
        "figure": str(out_pdf.relative_to(HERE)),
    }
    (RESULTS / "e2.json").write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
