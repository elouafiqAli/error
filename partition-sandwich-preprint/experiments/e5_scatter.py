"""
e5_scatter.py — Experiment 5: achievable-region scatter.

For 1000 random (partition, binary label) pairs of varying size
n ∈ {4..32}, plot (H(f|Π), ε*(Π)) inside the "eye" between the Fano
curve H = H_bin(ε) and the Hellman–Raviv line ε = H/2.  Visualises
Theorem 1 + Corollary 2 (universal slack w* ≈ 0.1610 at ε = 1/5).

This is the Python twin of verify.jl, intended only for plotting.
verify.jl remains the certified verification artefact.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from common import (
    EPS_W_STAR, H_STAR, W_STAR, bracket_from_cells, hbin,
)

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"; RESULTS.mkdir(exist_ok=True)
FIGURES = HERE / "figures"; FIGURES.mkdir(exist_ok=True)

N_SAMPLES = 1000
SEED = 20260531


def random_sample(rng: random.Random):
    n = rng.randint(4, 32)
    k = rng.randint(1, n)
    cell_ids = [rng.randrange(k) for _ in range(n)]
    labels = [rng.randint(0, 1) for _ in range(n)]
    return cell_ids, labels


def main() -> None:
    rng = random.Random(SEED)
    Hs, Es = [], []
    max_upper_slack = 0.0
    violations = 0
    for _ in range(N_SAMPLES):
        cell_ids, labels = random_sample(rng)
        br = bracket_from_cells(cell_ids, labels)
        Hs.append(br.H)
        Es.append(br.eps_star)
        if br.eps_star > 0.5 * br.H + 1e-12 or br.eps_star + 1e-12 < br.lower:
            violations += 1
        max_upper_slack = max(max_upper_slack, 0.5 * br.H - br.eps_star)

    # boundary curves
    eps_grid = np.linspace(0.0, 0.5, 401)
    fano_H = np.array([hbin(float(e)) for e in eps_grid])    # ε = Hbin^{-1}(H) ⇔ H = Hbin(ε)
    hr_H = np.linspace(0.0, 1.0, 401)
    hr_eps = hr_H / 2.0

    fig, ax = plt.subplots(figsize=(5.4, 4.2))
    ax.plot(fano_H, eps_grid, "C0-", lw=1.8,
            label=r"Fano boundary $\varepsilon = H_{\mathrm{bin}}^{-1}(H)$")
    ax.plot(hr_H, hr_eps, "C3-", lw=1.8,
            label=r"Hellman–Raviv boundary $\varepsilon = H/2$")
    ax.scatter(Hs, Es, s=8, alpha=0.45, color="0.25",
               label=f"{N_SAMPLES} random partitions")
    ax.plot([H_STAR], [EPS_W_STAR], marker="*", color="C2",
            markersize=14, markeredgecolor="k", linestyle="none",
            label=rf"$w^*\approx{W_STAR:.4f}$ at $\varepsilon=1/5$")
    ax.annotate(rf"$w^*={W_STAR:.4f}$",
                xy=(H_STAR, EPS_W_STAR),
                xytext=(H_STAR - 0.32, EPS_W_STAR + 0.07),
                fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=0.7, color="0.3"))
    ax.set_xlim(0.0, 1.02); ax.set_ylim(0.0, 0.52)
    ax.set_xlabel(r"Partition-conditional entropy $H(f\mid\Pi)$ (bits)")
    ax.set_ylabel(r"Partition Bayes error $\varepsilon^{*}_{\Pi}$")
    ax.set_title("Achievable region of the bracket (Theorem 1)")
    ax.legend(loc="upper left", fontsize=8, framealpha=0.95)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    out_pdf = FIGURES / "e5_achievable_region_scatter.pdf"
    fig.savefig(out_pdf)
    plt.close(fig)

    summary = {
        "experiment": "E5 achievable-region scatter",
        "samples": N_SAMPLES, "seed": SEED,
        "violations": violations,
        "max_upper_slack_empirical": max_upper_slack,
        "w_star_analytic": W_STAR,
        "figure": str(out_pdf.relative_to(HERE)),
    }
    (RESULTS / "e5.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

    # verification gates
    assert violations == 0, f"E5: {violations} bracket violations"
    assert max_upper_slack <= W_STAR + 1e-9, \
        f"E5: empirical slack {max_upper_slack} exceeds w*={W_STAR}"


if __name__ == "__main__":
    main()
