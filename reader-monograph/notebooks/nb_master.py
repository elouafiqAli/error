"""
nb_master.py — Master numerical-illustration script for the gnn.md monograph.

Generates all plots referenced in Chapters 2–16 in a single deterministic
run. Pins seeds to 0 / 1 / 2 / 3 for the four random sections. All
outputs land in ../plots/.

Usage:
    cd reader-monograph/notebooks
    python nb_master.py

Produced figures:
    plot01_binary_entropy.png       — H_bin and H_bin^{-1}
    plot02_bridge_sandwich.png      — §2.4 Bridge envelopes on [0, 1/2]
    plot03_slack_max.png            — w(H) = H/2 - H_bin^{-1}(H), peak at 0.161
    plot04_hvs_envelopes.png        — Ch 13: HR, Gini, sinusoidal, Bhattacharyya
    plot05_massey.png               — Ch 14: E[G] lower envelope vs. geometric
    plot06_ib_depth.png             — Ch 15: monotone (I(f;Pi), eps*) trajectory
    plot07_prior_aware.png          — Ch 16: d_KL(eps || eps_void) vs. 1-H_bin(eps)
"""
from __future__ import annotations

import os
import math

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

OUT = os.path.join(os.path.dirname(__file__), "..", "plots")
os.makedirs(OUT, exist_ok=True)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def h_bin(p: np.ndarray) -> np.ndarray:
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)


def h_bin_inv(y: float) -> float:
    """Inverse of binary entropy on [0, 1/2]."""
    if y <= 1e-9:
        return 0.0
    if y >= 1 - 1e-9:
        return 0.5
    return brentq(lambda p: h_bin(np.array([p])).item() - y, 1e-9, 0.5 - 1e-9)


# -----------------------------------------------------------------------------
# Plot 01 — Binary entropy and its inverse
# -----------------------------------------------------------------------------
def plot01():
    p = np.linspace(0, 1, 401)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(p, h_bin(p))
    axes[0].set_xlabel("p"); axes[0].set_ylabel("H_bin(p)")
    axes[0].set_title("Binary entropy H_bin(p)")
    axes[0].grid(True, alpha=0.3)

    y = np.linspace(0, 1, 201)
    inv = np.array([h_bin_inv(yy) for yy in y])
    axes[1].plot(y, inv)
    axes[1].set_xlabel("H"); axes[1].set_ylabel("H_bin^{-1}(H)")
    axes[1].set_title("Inverse on [0, 1/2] branch")
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "plot01_binary_entropy.png"), dpi=120)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Plot 02 — §2.4 / Ch 12 Bridge sandwich on [0, 1/2]
# -----------------------------------------------------------------------------
def plot02():
    eps = np.linspace(0, 0.5, 201)
    H = h_bin(eps)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(H, eps, label="Bayes risk ε*", linewidth=2)
    ax.plot(H, [h_bin_inv(h) for h in H], "--", label="lower: H_bin^{-1}(H)")
    ax.plot(H, H / 2, "--", label="upper: H/2 (Hellman–Raviv)")
    ax.set_xlabel("H(f|Π)"); ax.set_ylabel("ε*")
    ax.set_title("Ch 12 / §2.4 Bridge sandwich")
    ax.legend(); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "plot02_bridge_sandwich.png"), dpi=120)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Plot 03 — Slack function w(H) and its peak at 0.161
# -----------------------------------------------------------------------------
def plot03():
    H = np.linspace(0.01, 1, 200)
    w = H / 2 - np.array([h_bin_inv(h) for h in H])
    h_star = h_bin(np.array([0.2])).item()
    w_star = h_star / 2 - 0.2
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(H, w, label="w(H) = H/2 − H_bin^{-1}(H)")
    ax.axvline(h_star, color="red", ls=":", label=f"H* = H_bin(1/5) ≈ {h_star:.3f}")
    ax.axhline(w_star, color="red", ls=":", label=f"w* ≈ {w_star:.3f}")
    ax.set_xlabel("H"); ax.set_ylabel("w(H)")
    ax.set_title("Ch 12 Theorem 12.8 — worst-case bracket width")
    ax.legend(); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "plot03_slack_max.png"), dpi=120)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Plot 04 — HVS envelopes
# -----------------------------------------------------------------------------
def plot04():
    p = np.linspace(1e-6, 1 - 1e-6, 401)
    g_min = np.minimum(p, 1 - p)
    g_s = 0.5 * np.sin(np.pi * p)
    g_hr = 0.5 * h_bin(p)
    g_g = 2 * p * (1 - p)
    g_b = np.sqrt(p * (1 - p))
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(p, g_min, "k", linewidth=2, label="min(p, 1-p) — Bayes risk")
    ax.plot(p, g_s, label="Sinusoidal g_S = (1/2)sin πp")
    ax.plot(p, g_g, label="Gini g_G = 2p(1-p)")
    ax.plot(p, g_hr, label="Hellman–Raviv g_HR = (1/2)H_bin")
    ax.plot(p, g_b, label="Bhattacharyya g_B = √(p(1-p))")
    ax.set_xlabel("p"); ax.set_ylabel("envelope")
    ax.set_title("Ch 13 — HVS-admissible upper envelopes on Bayes risk")
    ax.legend(); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "plot04_hvs_envelopes.png"), dpi=120)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Plot 05 — Massey lower bound on E[G] vs. entropy
# -----------------------------------------------------------------------------
def plot05():
    H = np.linspace(2, 10, 200)
    lower = 0.25 * 2 ** H + 1
    upper = (1 / math.e) * 2 ** H + 1  # tight on geometric
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(H, lower, label="Massey lower: (1/4)2^H + 1")
    ax.plot(H, upper, "--", label="Geometric achievable: (1/e)2^H + 1")
    ax.fill_between(H, lower, upper, alpha=0.15)
    ax.set_xlabel("H(X) (bits)"); ax.set_ylabel("E[G]")
    ax.set_title("Ch 14 — Massey guessing lower bound (factor 4/e gap)")
    ax.legend(); ax.grid(True, alpha=0.3); ax.set_yscale("log")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "plot05_massey.png"), dpi=120)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Plot 06 — IB-style depth trajectory on a synthetic LossyWL chain
# -----------------------------------------------------------------------------
def plot06():
    rng = np.random.default_rng(seed=3)
    # Simulate a refinement chain on n=24 vertices with labels prior 1/2
    n = 24
    f = rng.integers(0, 2, size=n)
    # Partition chain Π^(L): start trivial, refine by random splits
    parts = [[list(range(n))]]
    for L in range(1, 10):
        prev = parts[-1]
        new = []
        for cell in prev:
            if len(cell) <= 1:
                new.append(cell); continue
            mid = len(cell) // 2
            new.append(cell[:mid]); new.append(cell[mid:])
        parts.append(new)

    def H_cond(part):
        out = 0.0
        for cell in part:
            q = len(cell) / n
            P = np.mean([f[v] for v in cell])
            if 0 < P < 1:
                out += q * h_bin(np.array([P])).item()
        return out

    def eps_star(part):
        return sum((len(cell) / n) * min(np.mean([f[v] for v in cell]), 1 - np.mean([f[v] for v in cell])) for cell in part)

    Hs = [H_cond(p) for p in parts]
    epss = [eps_star(p) for p in parts]
    Pf = np.mean(f)
    Hf = h_bin(np.array([Pf])).item()
    Is = [Hf - h for h in Hs]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(Is, epss, "o-")
    for L, (i, e) in enumerate(zip(Is, epss)):
        ax.annotate(f"L={L}", (i, e), textcoords="offset points", xytext=(6, 6))
    ax.set_xlabel("I(f; Π) = H(f) − H(f|Π) (relevance, bits)")
    ax.set_ylabel("ε*_Π")
    ax.set_title("Ch 15 — LossyWL depth trajectory in IB-coordinates (seed=3)")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "plot06_ib_depth.png"), dpi=120)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Plot 07 — Prior-aware (Prop 3.6) vs symmetric §2.4 lower bound on I(f;Π)
# -----------------------------------------------------------------------------
def plot07():
    eps = np.linspace(0.001, 0.499, 200)
    for eps_void in [0.5, 0.3, 0.2, 0.1]:
        d = eps * np.log2(eps / eps_void) + (1 - eps) * np.log2((1 - eps) / (1 - eps_void))
        plt.plot(eps, d, label=f"d_KL(ε || {eps_void}) (Prop 3.6)")
    plt.plot(eps, 1 - h_bin(eps), "k--", linewidth=2, label="1 − H_bin(ε)  (§2.4 at Pf=1/2)")
    plt.xlabel("ε*_Π"); plt.ylabel("lower bound on I(f; Π)")
    plt.title("Ch 16 — Prior-aware sharpening; sharper for skewed Pf")
    plt.legend(); plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "plot07_prior_aware.png"), dpi=120)
    plt.close()


if __name__ == "__main__":
    for fn in [plot01, plot02, plot03, plot04, plot05, plot06, plot07]:
        print(f"running {fn.__name__} ...")
        fn()
    print(f"\nAll plots written to {os.path.abspath(OUT)}")
