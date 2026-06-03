"""HW3 — T1 verifier from scratch (hbin_inverse, bracket, random verifier, w*)."""
from __future__ import annotations

from pathlib import Path

from onboarding.projects.scaffold import Cell, write_pair, _setup_cells


HW3_CELLS: list[Cell] = [
    Cell("md",
         "# HW3 — Binary-entropy bracket verifier from scratch — **Theorem 1**\n\n"
         "**Reading.** [`PAPER-ARXIV.md`](../../../../PAPER-ARXIV.md) **§3.2 Theorem 1** "
         "and **Appendix A** (the proof). See also the standalone walk-"
         "through in [`proof_walk.ipynb`](proof_walk.ipynb) — pure markdown + "
         "numeric checks of each algebraic step.\n\n"
         "**Goal.** Build `hbin_inverse`, `upper_HR`, `lower_Fano`, a random "
         "verifier of $\\mathrm{lower}(H) \\le \\varepsilon \\le \\mathrm{upper}(H)$, "
         "grid-search $(\\varepsilon^*, w^*) = (1/5, 0.1610)$, and (**Q5, new in r2.1**) "
         "explicitly construct the two extremal families of **Proposition 3.5** "
         "(no closed-form improvement of the sandwich): an HR-saturating sequence "
         "that drives $\\varepsilon \\to h/2$ and a Fano-saturating sequence "
         "that drives $\\varepsilon \\to H_\\mathrm{bin}^{-1}(h)$.\n\n"
         "**Julia companion (optional).** "
         "[`julia-theory/notebooks/05_bracket_envelope.jl`](../../../julia-theory/notebooks/05_bracket_envelope.jl) "
         "is the reactive slider twin of Q2; "
         "[`06_uniform_slack.jl`](../../../julia-theory/notebooks/06_uniform_slack.jl) "
         "derives $\\varepsilon^*=1/5$ symbolically via `Symbolics.jl` — read "
         "alongside Q4."),
    *_setup_cells("hw3"),
    Cell("demo",
         "from math import log2\n"
         "def hbin(p: float) -> float:\n"
         "    return 0.0 if (p <= 0 or p >= 1) else -(p*log2(p) + (1-p)*log2(1-p))\n"),

    # Q1 hbin_inverse
    Cell("md",
         "## Q1 — `hbin_inverse(h)` via bisection on $[0, 1/2]$.\n\n"
         "$H_\\mathrm{bin}$ is strictly increasing on $[0, 1/2]$, so its inverse on that branch is well-defined."),
    Cell("solution",
         "def hbin_inverse(h: float, tol: float = 1e-12) -> float:\n"
         "    if h <= 0.0:\n"
         "        return 0.0\n"
         "    if h >= 1.0:\n"
         "        return 0.5\n"
         "    lo, hi = 0.0, 0.5\n"
         "    while hi - lo > tol:\n"
         "        mid = 0.5 * (lo + hi)\n"
         "        if hbin(mid) < h:\n"
         "            lo = mid\n"
         "        else:\n"
         "            hi = mid\n"
         "    return 0.5 * (lo + hi)\n"),
    Cell("md", "**Distinguish.** Closed-form inverse is impossible (transcendental); we use bisection."),
    Cell("demo",
         "for eps in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5]:\n"
         "    print(f'  eps={eps:.2f} -> H={hbin(eps):.6f} -> H^{{-1}}(H)={hbin_inverse(hbin(eps)):.6f}')\n"),
    Cell("md", "**Gate Q1.** Round-trip error $< 10^{-9}$ on the grid."),
    Cell("gate",
         "for eps in [0.05, 0.10, 0.20, 0.30, 0.40, 0.50]:\n"
         "    rt = hbin_inverse(hbin(eps))\n"
         "    assert abs(rt - eps) < 1e-9, f'Q1: round-trip fails at eps={eps}: {rt}'\n"
         "print('[GATE OK] Q1: hbin_inverse round-trips to 1e-9 on six grid points')\n"),
    Cell("reflect", "reflect.log('Q3.Q1_hbin_inverse', 'bisection inverse round-trips ≤1e-9', 'HIGH')\n"),

    # Q2 bracket + envelope plot
    Cell("md", "## Q2 — `upper_HR(h) = h/2` (Hellman–Raviv) and `lower_Fano(h) = H^{-1}(h)` (Fano), envelope plot.\n\n"
               "**Concept (Theorem 1).** For binary $Y$ and any finite partition $\\Pi$,\n\n"
               "$$\nH_\\mathrm{bin}^{-1}\\!\\big(H(Y\\mid\\Pi)\\big) \\;\\le\\; \\varepsilon^*_\\Pi \\;\\le\\; \\tfrac{1}{2}\\, H(Y\\mid\\Pi).\n$$\n\n"
               "**Naming the endpoints (Appendix A).**\n\n"
               "- **Upper = Hellman–Raviv per cell + Jensen.** For each cell $C$, "
               "$e_C \\le \\tfrac{1}{2} H_\\mathrm{bin}(e_C)$ (Hellman–Raviv 1970). "
               "Multiply by $q_C$ and sum: $\\varepsilon^* = \\sum_C q_C e_C \\le \\tfrac{1}{2}\\sum_C q_C H_\\mathrm{bin}(e_C) = \\tfrac{1}{2} H(Y\\mid\\Pi)$. "
               "That is `upper_HR(h) = h/2` — no Jensen needed, just linearity.\n"
               "- **Lower = Fano per cell + concavity inversion.** Fano (1961) for "
               "binary $Y$ in cell $C$: $H_\\mathrm{bin}(e_C) \\le H(Y\\mid C)$ "
               "(here equality by construction). Apply $H_\\mathrm{bin}^{-1}$ on the "
               "$[0, 1/2]$ branch (monotone), then aggregate via concavity of $H_\\mathrm{bin}^{-1} \\circ H_\\mathrm{bin}$ — "
               "the **Jensen** step that gives `lower_Fano(h) = H_bin^{-1}(h)` "
               "is the only non-trivial inequality in the proof.\n\n"
               "The bracket has width 0 at $h=0$ and at $h=1$; widest near "
               "$h \\approx H_\\mathrm{bin}(1/5) \\approx 0.7219$ (Q4)."),
    Cell("solution",
         "def upper_HR(h: float) -> float:\n"
         "    \"\"\"Hellman–Raviv upper endpoint of Theorem 1: ε ≤ h/2.\"\"\"\n"
         "    return 0.5 * h\n"
         "\n"
         "def lower_Fano(h: float) -> float:\n"
         "    \"\"\"Fano lower endpoint of Theorem 1: ε ≥ H_bin^{-1}(h) on [0, 1/2].\"\"\"\n"
         "    return hbin_inverse(h)\n"
         "\n"
         "# Pedagogical aliases used by the rest of the curriculum.\n"
         "upper = upper_HR\n"
         "lower = lower_Fano\n"),
    Cell("md", "**Distinguish — *which* inequality goes which way.** A common error is to swap them. The mnemonic: **HR upper-bounds error by entropy/2** (cheap to compute), **Fano lower-bounds error by $H^{-1}$** (expensive — requires bisection). Their gap is $w(h) = h/2 - H_\\mathrm{bin}^{-1}(h)$, peaking at $w^* \\approx 0.1610$."),
    Cell("demo",
         "hs = np.linspace(0, 1, 401)\n"
         "ups = np.array([upper(h) for h in hs])\n"
         "los = np.array([lower(h) for h in hs])\n"
         "fig, ax = plt.subplots(figsize=(6, 4))\n"
         "ax.fill_between(hs, los, ups, color='C2', alpha=0.25, label='slack region')\n"
         "ax.plot(hs, ups, label='upper = h/2', lw=2)\n"
         "ax.plot(hs, los, label='lower = $H_{bin}^{-1}(h)$', lw=2)\n"
         "ax.set_xlabel('h = H(Y|Π)'); ax.set_ylabel('ε'); ax.legend()\n"
         "ax.set_title('Q2 — bracket envelope and slack')\n"
         "plt.tight_layout()\n"
         "_plots = _PROJECTS / 'psets' / 'hw3' / 'plots'; _plots.mkdir(exist_ok=True)\n"
         "fig.savefig(_plots / 'hw3_q2_envelope.png', dpi=120); plt.show()\n"),
    Cell("md", "**Gate Q2.** lower ≤ upper everywhere; widest near $h \\approx 0.72$ (corresponding to $\\varepsilon^* = 1/5$)."),
    Cell("gate",
         "assert np.all(los <= ups + 1e-12), 'Q2: lower > upper somewhere — bug'\n"
         "gap = ups - los\n"
         "h_argmax = hs[int(np.argmax(gap))]\n"
         "assert 0.65 < h_argmax < 0.78, f'Q2: argmax h={h_argmax} not in expected band near 0.72'\n"
         "assert gap.max() > 0.10, f'Q2: max gap={gap.max()} too small'\n"
         "print(f'[GATE OK] Q2: lower ≤ upper; max gap {gap.max():.4f} at h≈{h_argmax:.3f}')\n"),
    Cell("reflect", "reflect.log('Q3.Q2_bracket', 'lower ≤ upper; widest near h≈0.72', 'HIGH')\n"),

    # Q3 random-sample verifier
    Cell("md", "## Q3 — Random-sample verifier of $\\mathrm{lower}(H) \\le \\varepsilon \\le \\mathrm{upper}(H)$.\n\n"
               "Sample cell masses via Multinomial; sample per-cell errors uniformly in $[0, 1/2]$ (Bayes errors live there)."),
    Cell("solution",
         "def random_partition_stats(rng, m: int, n: int):\n"
         "    sizes = rng.multinomial(n, [1/m]*m)\n"
         "    q = sizes / n\n"
         "    e = rng.uniform(0.0, 0.5, size=m)\n"
         "    eps = float(np.sum(q * e))\n"
         "    H = float(np.sum(q * np.array([hbin(ei) for ei in e])))\n"
         "    return eps, H\n"
         "\n"
         "def verify_bracket(num_samples=2000, m_max=5, n=200, seed=0):\n"
         "    rng = np.random.default_rng(seed)\n"
         "    for _ in range(num_samples):\n"
         "        m = int(rng.integers(2, m_max + 1))\n"
         "        eps, H = random_partition_stats(rng, m, n)\n"
         "        assert lower(H) - 1e-9 <= eps <= upper(H) + 1e-9, \\\n"
         "            f'bracket violated: lower={lower(H)} eps={eps} upper={upper(H)}'\n"
         "    return True\n"),
    Cell("md", "**Distinguish.** Sampling errors $> 1/2$ would falsely violate; clamping to $[0, 1/2]$ is essential."),
    Cell("demo",
         "ok = verify_bracket(num_samples=2000)\n"
         "print(f'verify_bracket(2000) -> {ok}')\n"),
    Cell("md", "**Gate Q3.** `verify_bracket` returns True on 2000 samples."),
    Cell("gate",
         "assert ok is True, 'Q3: verifier did not return True'\n"
         "print('[GATE OK] Q3: 2000 random partitions all in bracket')\n"),
    Cell("reflect", "reflect.log('Q3.Q3_verifier', 'bracket holds on 2000 random multinomial+uniform partitions', 'HIGH')\n"),

    # Q4 w* grid search
    Cell("md", "## Q4 — Grid search $\\varepsilon^*, w^*$.\n\n"
               "Maximise $w(\\varepsilon) = H_\\mathrm{bin}(\\varepsilon)/2 - \\varepsilon$ on $[0, 1/2]$."),
    Cell("solution",
         "def find_w_star(grid: int = 5000):\n"
         "    eps_grid = np.linspace(1/grid, 0.5 - 1/grid, grid)\n"
         "    H_grid = np.array([hbin(e) for e in eps_grid])\n"
         "    slacks = H_grid/2.0 - eps_grid\n"
         "    idx = int(np.argmax(slacks))\n"
         "    return float(eps_grid[idx]), float(slacks[idx])\n"),
    Cell("md", "**Distinguish — false lead.** The slack maximum is NOT at $\\varepsilon = 1/2$ (the entropy maximum); first-order condition gives $H_\\mathrm{bin}'(\\varepsilon) = 2 \\Rightarrow \\varepsilon^* = 1/5$."),
    Cell("demo",
         "eps_star, w_star = find_w_star(5000)\n"
         "print(f'eps* = {eps_star:.4f} (expected 0.2000)')\n"
         "print(f'w*   = {w_star:.4f} (expected 0.1610)')\n"),
    Cell("md", "**Gate Q4.** $\\varepsilon^* \\in (0.199, 0.201)$ and $w^* \\in (0.160, 0.162)$."),
    Cell("gate",
         "assert 0.199 < eps_star < 0.201, f'Q4: eps*={eps_star} out of band'\n"
         "assert 0.160 < w_star  < 0.162, f'Q4: w*={w_star} out of band'\n"
         "print(f'[GATE OK] Q4: eps*={eps_star:.4f}, w*={w_star:.4f}')\n"),
    Cell("reflect", "reflect.log('Q3.Q4_wstar', f'eps*={eps_star:.4f}, w*={w_star:.4f}', 'HIGH')\n"),

    # Q4.5 Proposition 3.5 — sharpness witnesses
    Cell("md", "## Q4.5 — **Proposition 3.5** sharpness: both endpoints are saturated by explicit families.\n\n"
               "**Statement (Paper §3.2).** No closed-form improvement of the sandwich exists: for any $h \\in (0, 1)$ there are partition families $(\\Pi_\\alpha^\\mathrm{HR})_{\\alpha}$ and $(\\Pi_\\alpha^\\mathrm{J})_{\\alpha}$ with $H(Y\\mid\\Pi_\\alpha) \\to h$ such that $\\varepsilon^*(\\Pi_\\alpha^\\mathrm{HR}) \\to h/2$ (upper saturated) and $\\varepsilon^*(\\Pi_\\alpha^\\mathrm{J}) \\to H_\\mathrm{bin}^{-1}(h)$ (lower saturated).\n\n"
               "**Constructions.**\n\n"
               "- **HR-saturating** ($\\Pi^\\mathrm{HR}$, two-mass): one cell with mass $1-\\alpha$ and $e=0$, one cell with mass $\\alpha$ and $e=1/2$. Then $\\varepsilon = \\alpha/2$, $H = \\alpha$, so $\\varepsilon = H/2$ **exactly** — the upper endpoint is hit with equality.\n"
               "- **Fano-saturating** ($\\Pi^\\mathrm{J}$, constant-$e$): every cell has the same $e_C = e$ (any cell sizes). Then $H = H_\\mathrm{bin}(e)$ and $\\varepsilon = e = H_\\mathrm{bin}^{-1}(H)$ **exactly** — the lower endpoint is hit with equality."),
    Cell("solution",
         "def witness_HR(alpha: float):\n"
         "    \"\"\"Two-mass HR-saturator: returns (eps, H) hitting ε = H/2.\"\"\"\n"
         "    q = np.array([1 - alpha, alpha])\n"
         "    e = np.array([0.0, 0.5])\n"
         "    eps = float(np.sum(q * e))\n"
         "    H   = float(np.sum(q * np.array([hbin(ei) for ei in e])))\n"
         "    return eps, H\n"
         "\n"
         "def witness_Fano(e: float, m: int = 5):\n"
         "    \"\"\"Constant-e Fano-saturator on m equal-mass cells: returns (eps, H) hitting ε = H_bin^{-1}(H).\"\"\"\n"
         "    q = np.full(m, 1.0 / m)\n"
         "    ee = np.full(m, e)\n"
         "    eps = float(np.sum(q * ee))\n"
         "    H   = float(np.sum(q * np.array([hbin(ei) for ei in ee])))\n"
         "    return eps, H\n"),
    Cell("md", "**Distinguish — sharpness vs tightness.** Sharpness = endpoints are attained by *some* feasible $\\Pi$; tightness on a *specific* $\\Pi$ would mean *equality* there. Proposition 3.5 is about the envelope, not about any single problem."),
    Cell("demo",
         "alphas = np.linspace(0.05, 0.95, 19)\n"
         "hr_eps, hr_H = zip(*[witness_HR(a) for a in alphas])\n"
         "hr_eps, hr_H = np.array(hr_eps), np.array(hr_H)\n"
         "hr_residual = hr_eps - hr_H/2\n"
         "print(f'HR witness: max|ε - H/2| = {np.max(np.abs(hr_residual)):.2e}')\n"
         "\n"
         "es = np.linspace(0.02, 0.48, 24)\n"
         "fa_eps, fa_H = zip(*[witness_Fano(e) for e in es])\n"
         "fa_eps, fa_H = np.array(fa_eps), np.array(fa_H)\n"
         "fa_residual = fa_eps - np.array([hbin_inverse(h) for h in fa_H])\n"
         "print(f'Fano witness: max|ε - H_bin^{{-1}}(H)| = {np.max(np.abs(fa_residual)):.2e}')\n"
         "\n"
         "hs = np.linspace(0, 1, 401)\n"
         "fig, ax = plt.subplots(figsize=(7, 4.5))\n"
         "ax.fill_between(hs, [lower(h) for h in hs], [upper(h) for h in hs], color='C2', alpha=0.18, label='Theorem 1 bracket')\n"
         "ax.plot(hr_H, hr_eps, 'o-', color='C3', label='HR-saturating Π^HR (upper)')\n"
         "ax.plot(fa_H, fa_eps, 's-', color='C0', label='Fano-saturating Π^J (lower)')\n"
         "ax.set_xlabel('H(Y|Π)'); ax.set_ylabel('ε(Π)'); ax.legend()\n"
         "ax.set_title('Q4.5 — Proposition 3.5 sharpness witnesses')\n"
         "plt.tight_layout()\n"
         "_plots = _PROJECTS / 'psets' / 'hw3' / 'plots'; _plots.mkdir(exist_ok=True)\n"
         "fig.savefig(_plots / 'hw3_q45_sharpness.png', dpi=120); plt.show()\n"),
    Cell("md", "**Gate Q4.5.** Both residuals $< 10^{-9}$ on their respective grids."),
    Cell("gate",
         "assert np.max(np.abs(hr_residual)) < 1e-9, f'Q4.5: HR witness off by {np.max(np.abs(hr_residual))}'\n"
         "assert np.max(np.abs(fa_residual)) < 1e-9, f'Q4.5: Fano witness off by {np.max(np.abs(fa_residual))}'\n"
         "print(f'[GATE OK] Q4.5: both Proposition 3.5 witnesses saturate the bracket to ≤1e-9')\n"),
    Cell("reflect",
         "reflect.log('Q3.Q4.5_sharpness',\n"
         "            'Prop 3.5 witnesses constructed: 2-mass family saturates upper, constant-e family saturates lower (residual ≤1e-9)',\n"
         "            'HIGH')\n"),

    # Q5 writeup
    Cell("md", "## Q5 — Writeup & calibration."),
    Cell("reflect",
         "reflect.log('Q3.Q5_writeup', 'four sections + five calibration entries; bracket holds end-to-end', 'MEDIUM')\n"
         "print('HW3 reflection log:')\n"
         "for r in reflect.dump():\n"
         "    if 'hw3' in r['notebook']:\n"
         "        print(f\"  [{r['level']:>10}] {r['concept']}: {r['claim']}\")\n"),
    Cell("md", "**End of HW3.**"),
]


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "psets" / "hw3"
    sol, stu = write_pair(HW3_CELLS, out_dir=out, stem="hw3")
    print(f"wrote {sol.relative_to(out.parent.parent)} and {stu.relative_to(out.parent.parent)}")


if __name__ == "__main__":
    main()
