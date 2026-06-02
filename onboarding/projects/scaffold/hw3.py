"""HW3 — T1 verifier from scratch (hbin_inverse, bracket, random verifier, w*)."""
from __future__ import annotations

from pathlib import Path

from onboarding.projects.scaffold import Cell, write_pair, _setup_cells


HW3_CELLS: list[Cell] = [
    Cell("md",
         "# HW3 — Binary-entropy bracket verifier from scratch\n\n"
         "Goal: build `hbin_inverse`, `upper`, `lower`, a random "
         "verifier of $\\mathrm{lower}(H) \\le \\varepsilon \\le \\mathrm{upper}(H)$, "
         "and grid-search $(\\varepsilon^*, w^*) = (1/5, 0.1610)$."),
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
    Cell("md", "## Q2 — `upper(h) = h/2`, `lower(h) = H^{-1}(h)`, envelope plot.\n\n"
               "**Concept.** The bracket has width 0 at $h=0$ and at $h=1$; widest near $h \\approx H_\\mathrm{bin}(1/5) \\approx 0.7219$."),
    Cell("solution",
         "def upper(h: float) -> float:\n"
         "    return 0.5 * h\n"
         "\n"
         "def lower(h: float) -> float:\n"
         "    return hbin_inverse(h)\n"),
    Cell("md", "**Distinguish.** Upper is linear; lower is concave-then-convex inverse. Their gap is $w(h) = h/2 - H_\\mathrm{bin}^{-1}(h)$."),
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
